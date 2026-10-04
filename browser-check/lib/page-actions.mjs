// Wyliczenie elementów i akcji strony, podsumowanie strony dla modelu oraz wykonanie akcji (Playwright).
// Moduł jest ogólny: nie zna żadnej aplikacji, ekranu ani tekstu.
import { createHash } from 'node:crypto';
import { toLocator, describeTarget } from './locators.mjs';
import { maskText, maskUrl, rawLimitFor, safeText, secretSafeText } from './mask.mjs';

export { maskPii } from './mask.mjs';

/**
 * Prywatne odciski tożsamości elementów — wyłącznie w pamięci procesu. WeakMap kluczowana obiektem elementu stanu
 * (`state.elements[i]`): odcisk nie jest polem obiektu, więc nie trafia do `state` dla Jev, raportów ani migawek
 * (`JSON.stringify`/`redactDeep` go nie widzą). Wartość: `{ hash, options }` — `hash` = SHA-1 z `rola|nazwa` (nazwa
 * surowa po maskowaniu SEKRETÓW, bez maskowania PII), `options` = mapa indeks opcji → SHA-1 tekstu opcji (jw.).
 */
const identities = new WeakMap();

function sha1(text) {
  return createHash('sha1').update(text).digest('hex');
}

/** Odcisk opcji `select` zebrany razem ze stanem (albo `undefined`, gdy elementu/opcji nie zebrano). */
export function optionIdentityOf(element, optionIndex) {
  return identities.get(element)?.options.get(optionIndex);
}

const CANDIDATE_SELECTOR = [
  'a[href]',
  'button',
  'input:not([type=hidden])',
  'textarea',
  'select',
  '[role=button]',
  '[role=link]',
  '[role=menuitem]',
  '[role=menuitemcheckbox]',
  '[role=menuitemradio]',
  '[role=option]',
  '[role=tab]',
  '[role=checkbox]',
  '[role=radio]',
  '[role=switch]',
  '[role=combobox]',
  '[contenteditable=true]',
].join(', ');
const MODAL_SELECTOR = '[role=dialog], [role=alertdialog], [aria-modal=true]';
const SEMANTIC_OVERLAY_SELECTOR = `${MODAL_SELECTOR}, [role=listbox], [role=menu]`;
const MESSAGE_SELECTOR = '[role=alert], [role=status], [aria-live], .p-toast-message, .p-message';
const REGION_RANK = { overlay: 0, main: 1, dialog: 2, nav: 3, header: 4, aside: 5, footer: 6, other: 7 };
const TRANSIENT_ERROR = /Execution context was destroyed|has been closed|Target closed|navigat/i;

export const FORBIDDEN_LOCATOR_INVALID = 'FORBIDDEN_LOCATOR_INVALID';

function firstLine(error) {
  return String(error?.message ?? error).split('\n')[0].trim();
}

/** Konfiguracja skanu; `rawLimit` zależy od długości sekretów scenariusza (długość nie jest sekretem). */
function scanConfig(scenario) {
  return {
    candidateSelector: CANDIDATE_SELECTOR,
    modalSelector: MODAL_SELECTOR,
    semanticSelector: SEMANTIC_OVERLAY_SELECTOR,
    messageSelector: MESSAGE_SELECTOR,
    rawLimit: rawLimitFor(scenario),
  };
}

/**
 * Kod wykonywany w przeglądarce (jeden page.evaluate). Zwraca SUROWE teksty (bez spłaszczania białych znaków, obcięte
 * tylko do twardego limitu technicznego `config.rawLimit`) — maskowanie, spłaszczanie i przycinanie robi Node
 * (kolejność: sekrety, spłaszczenie, PII, przycięcie; sekrety nie trafiają do przeglądarki).
 * Tryb skanu: zbiera kandydatów, zakres nakładki, opisy i podsumowanie; kandydaci dostają tymczasowy atrybut
 * data-bc-tmp (numer w kolejności DOM), numery eN nadaje faza końcowa.
 * Tryb inspekcji (`config.inspectId`): zwraca aktualną rolę, nazwę i użyteczność elementu `[data-bc-id=…]`.
 */
function scanInBrowser(config) {
  const RAW_LIMIT = config.rawLimit;
  // `flat` służy WYŁĄCZNIE do logiki (puste/niepuste, porównania, klucze grup); zwracane teksty są surowe (`cap`):
  // bez spłaszczania białych znaków i bez przycinania poniżej twardego limitu technicznego.
  const flat = (text) => String(text ?? '').replace(/\s+/g, ' ').trim();
  const has = (text) => flat(text) !== '';
  const pick = (...texts) => texts.find(has) ?? '';
  const cap = (text) => String(text ?? '').slice(0, RAW_LIMIT);
  const shown = (element) => {
    if (!element.isConnected) return false;
    if (typeof element.checkVisibility === 'function' && !element.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true })) return false;
    const rect = element.getBoundingClientRect();
    return rect.width > 0 && rect.height > 0;
  };
  const textOf = (element) => String(element.innerText ?? element.textContent ?? '');

  const isDisabled = (element) => element.matches(':disabled') || element.getAttribute('aria-disabled') === 'true';
  const usable = (element) => shown(element) && !isDisabled(element);

  const labelledBy = (element) => {
    const ids = element.getAttribute('aria-labelledby');
    if (!ids) return '';
    return ids
      .split(/\s+/)
      .map((id) => {
        const target = document.getElementById(id);
        return target ? String(target.innerText ?? target.textContent ?? '') : '';
      })
      .join(' ');
  };

  const TEXT_TYPES = ['', 'text', 'email', 'tel', 'search', 'number', 'password', 'url'];
  const kindOf = (element) => {
    const tag = element.tagName;
    if (tag === 'TEXTAREA') return 'text';
    if (tag === 'INPUT' && TEXT_TYPES.includes(element.type)) return 'text';
    if (tag === 'SELECT') return 'select';
    if (element.getAttribute('contenteditable') === 'true') return 'contenteditable';
    return 'click';
  };

  // Tekst etykiety bez zagnieżdżonych kontrolek (etykieta otaczająca <select> nie może wciągnąć listy opcji).
  const labelText = (label) => {
    const copy = label.cloneNode(true);
    for (const control of copy.querySelectorAll('select, textarea, input, button')) control.remove();
    return String(copy.textContent ?? '');
  };

  const nameOf = (element, kind) => {
    const aria = element.getAttribute('aria-label');
    if (has(aria)) return aria;
    const byIds = labelledBy(element);
    if (has(byIds)) return byIds;
    if (element.labels && element.labels.length > 0) {
      const text = [...element.labels].map(labelText).join(' ');
      if (has(text)) return text;
    }
    if (kind === 'click') {
      const text = textOf(element);
      if (has(text)) return text;
      const image = element.querySelector('img[alt]:not([alt=""])');
      if (image && has(image.getAttribute('alt'))) return image.getAttribute('alt');
      if (element.tagName === 'INPUT' && has(element.value)) return element.value;
    }
    return pick(element.getAttribute('title'), element.getAttribute('placeholder'));
  };

  const roleOf = (element) => {
    const explicit = flat(element.getAttribute('role')).split(' ')[0];
    if (explicit) return explicit;
    const tag = element.tagName;
    if (tag === 'A') return 'link';
    if (tag === 'BUTTON') return 'button';
    if (tag === 'SELECT') return 'combobox';
    if (tag === 'TEXTAREA') return 'textbox';
    if (tag === 'INPUT') {
      const type = element.type;
      if (['button', 'submit', 'reset', 'image'].includes(type)) return 'button';
      if (type === 'checkbox' || type === 'radio') return type;
      if (type === 'range') return 'slider';
      if (TEXT_TYPES.includes(type)) return 'textbox';
      return 'input';
    }
    if (element.getAttribute('contenteditable') === 'true') return 'textbox';
    return 'generic';
  };

  if (config.inspectId) {
    const live = document.querySelector(`[data-bc-id="${config.inspectId}"]`);
    if (!live) return { found: false };
    return { found: true, role: roleOf(live), name: cap(nameOf(live, kindOf(live))), usable: usable(live) };
  }

  for (const old of document.querySelectorAll('[data-bc-id],[data-bc-tmp]')) {
    old.removeAttribute('data-bc-id');
    old.removeAttribute('data-bc-tmp');
  }

  // Korzeń aplikacji: element z ng-version / #root / #app, w ostateczności największy bezpośredni potomek <body>.
  const bodyKids = [...document.body.children];
  let appRoot = null;
  const rootHint = document.querySelector('[ng-version], #root, #app, #__next, #__nuxt');
  if (rootHint) appRoot = bodyKids.find((kid) => kid === rootHint || kid.contains(rootHint)) ?? null;
  if (!appRoot) {
    let best = -1;
    for (const kid of bodyKids) {
      const size = kid.getElementsByTagName('*').length;
      if (size > best) {
        best = size;
        appRoot = kid;
      }
    }
  }

  // Nakładka: (a) element modalny (role=dialog|alertdialog albo aria-modal=true) gdziekolwiek w DOM albo (b) bezpośredni
  // potomek <body> inny niż korzeń aplikacji, który jest pozycjonowany `fixed|absolute` (sam albo pierwszy potomek) lub ma
  // semantykę dialogu/listy/menu. Nakładka MODALNA zawsze zawęża zakres (także bez kontrolek); niemodalna (np.
  // podpowiedź, lista) tylko gdy zawiera coś operowalnego.
  const NON_VISUAL = ['SCRIPT', 'STYLE', 'LINK', 'NOSCRIPT', 'TEMPLATE'];
  const floating = (element) => {
    const isFloating = (node) => Boolean(node) && ['fixed', 'absolute'].includes(getComputedStyle(node).position);
    return isFloating(element) || isFloating(element.firstElementChild);
  };
  const overlayPool = new Map(); // element -> czy modalny
  for (const element of document.querySelectorAll(config.modalSelector)) overlayPool.set(element, true);
  for (const kid of bodyKids) {
    if (kid === appRoot || NON_VISUAL.includes(kid.tagName) || kid.getAttribute('aria-hidden') === 'true') continue;
    const modal = overlayPool.get(kid) === true || kid.matches(config.modalSelector) || kid.querySelector(config.modalSelector) !== null;
    const semantic = kid.matches(config.semanticSelector) || kid.querySelector(config.semanticSelector) !== null;
    if (modal || semantic || floating(kid)) overlayPool.set(kid, modal);
  }
  const hasUsable = (container) => [...container.querySelectorAll(config.candidateSelector)].some(usable);
  const overlays = [...overlayPool.entries()]
    .filter(([element, modal]) => {
      if (!shown(element)) return false;
      const rect = element.getBoundingClientRect();
      return rect.width >= 4 && rect.height >= 4 && (modal || hasUsable(element));
    })
    .sort((a, b) => (a[0].compareDocumentPosition(b[0]) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1));
  const overlayEl = overlays.length > 0 ? overlays[overlays.length - 1][0] : null;

  const headingText = (container) => {
    const heading = container.querySelector('h1, h2, h3, h4, [role=heading]');
    return heading ? cap(heading.innerText ?? heading.textContent) : '';
  };
  let overlayDesc = null;
  if (overlayEl) {
    const dialog = overlayEl.matches(config.modalSelector) ? overlayEl : overlayEl.querySelector(config.modalSelector);
    if (dialog) overlayDesc = { kind: 'dialog', name: cap(pick(dialog.getAttribute('aria-label'), labelledBy(dialog), headingText(dialog))) };
    else overlayDesc = { kind: 'overlay', name: headingText(overlayEl) };
  }

  const landmarkOf = (element) => {
    for (let ancestor = element.parentElement; ancestor && ancestor !== document.body; ancestor = ancestor.parentElement) {
      const role = ancestor.getAttribute('role');
      const tag = ancestor.tagName.toLowerCase();
      let kind = null;
      if (role === 'navigation' || tag === 'nav') kind = 'nav';
      else if (role === 'banner' || tag === 'header') kind = 'header';
      else if (role === 'main' || tag === 'main') kind = 'main';
      else if (role === 'complementary' || tag === 'aside') kind = 'aside';
      else if (role === 'contentinfo' || tag === 'footer') kind = 'footer';
      if (kind) return { kind, label: cap(pick(ancestor.getAttribute('aria-label'), labelledBy(ancestor))) };
    }
    return { kind: 'other', label: '' };
  };

  const scope = overlayEl ? [...(overlayEl.matches(config.candidateSelector) ? [overlayEl] : []), ...overlayEl.querySelectorAll(config.candidateSelector)] : [...document.querySelectorAll(config.candidateSelector)];
  const seen = new Set();
  const items = [];
  const nodes = [];
  for (const element of scope) {
    if (seen.has(element) || !usable(element)) continue;
    seen.add(element);
    const kind = kindOf(element);
    const name = cap(nameOf(element, kind));
    const parentCandidate = element.parentElement ? element.parentElement.closest(config.candidateSelector) : null;
    if (parentCandidate && has(name) && flat(nameOf(parentCandidate, kindOf(parentCandidate))) === flat(name)) continue;
    const item = { role: roleOf(element), name, kind };
    if (kind === 'text') item.value = element.type === 'password' ? (element.value ? '•••' : '') : cap(element.value);
    else if (kind === 'contenteditable') item.value = cap(element.innerText);
    else if (kind === 'select') {
      item.value = cap(element.selectedOptions[0]?.text ?? '');
      item.options = [...element.options].map((option, index) => ({ index, text: cap(option.text) }));
    }
    if (element.tagName === 'INPUT' && (element.type === 'checkbox' || element.type === 'radio')) item.checked = element.checked;
    else if (element.hasAttribute('aria-checked')) item.checked = element.getAttribute('aria-checked') === 'true';
    if (element.hasAttribute('aria-expanded')) item.expanded = element.getAttribute('aria-expanded') === 'true';
    item.region = overlayEl ? { kind: 'overlay', label: '' } : landmarkOf(element);
    item.tmp = items.length;
    element.setAttribute('data-bc-tmp', String(item.tmp));
    items.push(item);
    nodes.push(element);
  }

  // Elementy o tej samej roli i nazwie (np. "Rozwiń" na każdej karcie listy) dostają kontekst: tekst największego
  // przodka, który zawiera tylko ten element z całej grupy duplikatów (zwykle karta/wiersz listy).
  const contextOf = (container) => {
    const heading = container.querySelector('h1, h2, h3, h4, h5, h6, [role=heading]');
    return cap(pick(heading && (heading.innerText ?? heading.textContent), container.innerText, container.textContent));
  };
  const groups = new Map();
  items.forEach((item, index) => {
    const key = `${item.role}|${flat(item.name)}`;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(index);
  });
  for (const members of groups.values()) {
    if (members.length < 2) continue;
    for (const index of members) {
      let best = null;
      for (let ancestor = nodes[index].parentElement; ancestor && ancestor !== document.body; ancestor = ancestor.parentElement) {
        if (members.some((other) => other !== index && ancestor.contains(nodes[other]))) break;
        best = ancestor;
      }
      if (best) items[index].context = contextOf(best);
    }
  }

  const headings = [];
  const headingNodes = [...document.querySelectorAll('h1, h2, h3')].filter(shown);
  if (overlayEl) headingNodes.sort((a, b) => Number(overlayEl.contains(b)) - Number(overlayEl.contains(a)));
  for (const node of headingNodes) {
    const text = cap(node.innerText ?? node.textContent);
    if (has(text) && headings.length < 8) headings.push(text);
  }

  const messages = [];
  const taken = [];
  for (const node of document.querySelectorAll(config.messageSelector)) {
    if (messages.length >= 5) break;
    if (node.getAttribute('aria-live') === 'off' || !shown(node)) continue;
    if (taken.some((outer) => outer.contains(node))) continue;
    const text = cap(node.innerText ?? node.textContent);
    if (!has(text) || messages.includes(text)) continue;
    taken.push(node);
    messages.push(text);
  }

  return {
    summary: { url: location.pathname + location.search, title: cap(document.title), headings, messages, overlay: overlayDesc },
    items,
  };
}

function finalizeInBrowser(mapping) {
  for (const old of document.querySelectorAll('[data-bc-id],[data-bc-tmp]')) {
    old.removeAttribute('data-bc-id');
    if (!(old.getAttribute('data-bc-tmp') in mapping)) old.removeAttribute('data-bc-tmp');
  }
  for (const [tmp, id] of Object.entries(mapping)) {
    const element = document.querySelector(`[data-bc-tmp="${tmp}"]`);
    if (element) {
      element.setAttribute('data-bc-id', id);
      element.removeAttribute('data-bc-tmp');
    }
  }
  for (const rest of document.querySelectorAll('[data-bc-tmp]')) rest.removeAttribute('data-bc-tmp');
}

/**
 * Cele wyłączone z puli akcji: `forbidden` flow + przełączniki motywu scenariusza (CLI ustawia motyw sam).
 * Z listy kliknięć przełącznika wyłączany jest tylko OSTATNI cel (ten, który faktycznie przełącza motyw);
 * wcześniejsze to otwieracze menu (np. "Menu użytkownika"), potrzebne do nawigacji, więc zostają dostępne.
 */
function excludedTargets(forbidden, scenario) {
  const targets = [...(forbidden ?? [])];
  const theme = scenario?.theme;
  if (theme) {
    const toggles = [theme.toggle, ...Object.values(theme.toggleByViewport ?? {})];
    for (const toggle of toggles) targets.push(Array.isArray(toggle) ? toggle[toggle.length - 1] : toggle);
  }
  return targets;
}

/**
 * Wartości atrybutu `attribute` (`data-bc-tmp` / `data-bc-id`) tych kandydatów, którzy pasują do celu zakazu: leżą
 * WEWNĄTRZ pasującego elementu (także nim samym) albo pasujący element leży wewnątrz nich (najbliższy kandydat-przodek).
 * Błąd lokatora (np. niepoprawny CSS) to błąd z kodem FORBIDDEN_LOCATOR_INVALID — nigdy ciche zdjęcie zakazu;
 * przejściowe błędy nawigacji lecą dalej bez zmian.
 */
async function matchedOwners(page, target, attribute, scenario) {
  try {
    return await toLocator(page, target).evaluateAll((elements, attr) => {
      const owners = new Set();
      const candidates = [...document.querySelectorAll(`[${attr}]`)];
      for (const element of elements) {
        const own = element.closest(`[${attr}]`);
        if (own) owners.add(own.getAttribute(attr));
        for (const candidate of candidates) if (element.contains(candidate)) owners.add(candidate.getAttribute(attr));
      }
      return [...owners];
    }, attribute);
  } catch (error) {
    if (TRANSIENT_ERROR.test(String(error?.message ?? error))) throw error;
    // Opis lokatora i błąd mogą zawierać wartości podstawione ze scenariusza albo tekst strony — maskowanie u źródła.
    const wrapped = new Error(maskText(scenario, `${FORBIDDEN_LOCATOR_INVALID}: ${describeTarget(target)}: ${firstLine(error)}`));
    wrapped.code = FORBIDDEN_LOCATOR_INVALID;
    throw wrapped;
  }
}

async function resolveExcluded(page, targets, scenario) {
  const excluded = new Set();
  for (const target of targets) {
    for (const owner of await matchedOwners(page, target, 'data-bc-tmp', scenario)) excluded.add(Number(owner));
  }
  return excluded;
}

function regionText(region, overlayText, mask) {
  if (region.kind === 'overlay') return overlayText ?? '';
  if (region.kind === 'other') return '';
  const label = mask(region.label, 60);
  return label ? `${region.kind} "${label}"` : region.kind;
}

/**
 * Zbiera stan strony: podsumowanie, elementy (z maskowaniem), liczbę odciętych i odcisk palca.
 * Elementy dostają w DOM atrybut data-bc-id="eN" (N od 1 w kolejności DOM). Maskowanie (sekrety scenariusza, e-maile,
 * telefony) następuje przed przycięciem. Rzuca błąd z kodem FORBIDDEN_LOCATOR_INVALID, gdy lokator zakazu jest wadliwy.
 */
export async function collectPageState(page, { maxOptions, forbidden, scenario }) {
  const scan = await page.evaluate(scanInBrowser, scanConfig(scenario));
  const mask = (text, max) => safeText(scenario, text, max);
  // Wartości prywatne (sekrety zamaskowane, PII NIE) — tylko do odcisków wewnątrz procesu.
  const secretSafe = (text) => secretSafeText(scenario, text);

  const excluded = await resolveExcluded(page, excludedTargets(forbidden, scenario), scenario);
  let items = scan.items.filter((item) => !excluded.has(item.tmp));
  let truncated = 0;
  if (items.length > maxOptions) {
    const ranked = [...items].sort((a, b) => REGION_RANK[a.region.kind] - REGION_RANK[b.region.kind] || a.tmp - b.tmp);
    const keep = new Set(ranked.slice(0, maxOptions).map((item) => item.tmp));
    truncated = items.length - maxOptions;
    items = items.filter((item) => keep.has(item.tmp));
  }

  const overlay = scan.summary.overlay;
  let overlayText = null;
  if (overlay !== null) {
    const name = mask(overlay.name, 80);
    overlayText = name ? `${overlay.kind} "${name}"` : overlay.kind;
  }

  const mapping = {};
  const privateLines = [];
  const elements = items.map((item, index) => {
    const id = `e${index + 1}`;
    mapping[item.tmp] = id;
    const privateName = secretSafe(item.name);
    privateLines.push(`${item.role}|${privateName}|${item.value === undefined ? '' : secretSafe(item.value)}|${item.checked ?? ''}|${item.expanded ?? ''}`);
    const element = { id, role: item.role, name: mask(item.name, 80), kind: item.kind };
    if (item.value !== undefined) element.value = mask(item.value, 40);
    if (item.checked !== undefined) element.checked = item.checked;
    if (item.expanded !== undefined) element.expanded = item.expanded;
    if (item.options !== undefined) {
      const kept = item.options.map((option) => ({ index: option.index, text: mask(option.text, 80) })).filter((option) => option.text !== '');
      element.options = kept.map((option) => option.text);
      element.optionIndexes = kept.map((option) => option.index);
    }
    element.region = regionText(item.region, overlayText, mask);
    if (item.context) element.context = mask(item.context, 70);
    identities.set(element, {
      hash: sha1(`${item.role}|${privateName}`),
      options: new Map((item.options ?? []).map((option) => [option.index, sha1(secretSafe(option.text))])),
    });
    return element;
  });
  await page.evaluate(finalizeInBrowser, mapping);

  const summary = {
    url: maskUrl(scenario, scan.summary.url),
    title: mask(scan.summary.title, 120),
    headings: scan.summary.headings.map((text) => mask(text, 80)),
    messages: scan.summary.messages.map((text) => mask(text, 160)),
    overlay: overlayText,
  };
  // Odcisk stanu liczony z wartości prywatnych (sekrety zamaskowane, PII nie), nie z zamaskowanych opisów: zmiana
  // numeru telefonu czy e-maila w tym samym widoku zmienia odcisk. Sam odcisk nie opuszcza procesu.
  const privateOverlay = overlay === null ? '' : `${overlay.kind}|${secretSafe(overlay.name)}`;
  const fingerprint = sha1([secretSafe(scan.summary.url), privateOverlay, ...privateLines].join('\n')).slice(0, 16);
  return { summary, elements, truncated, fingerprint };
}

/**
 * Tuż przed wykonaniem akcji na elemencie `eN`: odczytuje jego AKTUALNY opis (rola + nazwa, w tym samym potoku
 * maskowania co stan wysłany do modelu) i sprawdza zakazy (element ani żaden jego przodek nie może pasować do `forbidden`
 * / przełącznika motywu). `{ ok: true }` albo `{ ok: false, detail: 'missing' | 'changed' | 'forbidden' }`.
 * Błąd lokatora zakazu rzuca błąd z kodem FORBIDDEN_LOCATOR_INVALID.
 */
export async function verifyElementBeforeAction(page, element, { forbidden, scenario }) {
  const live = await page.evaluate(scanInBrowser, { ...scanConfig(scenario), inspectId: element.id });
  if (!live.found || !live.usable) return { ok: false, detail: 'missing' };
  // Porównanie z prywatnym odciskiem (rola + nazwa po maskowaniu sekretów, bez maskowania PII): dwa opisy różniące się
  // tylko zamaskowaną daną osobową (np. dwa różne e-maile) mają ten sam opis dla modelu, ale inny odcisk.
  const expected = identities.get(element)?.hash;
  if (expected === undefined || sha1(`${live.role}|${secretSafeText(scenario, live.name)}`) !== expected) return { ok: false, detail: 'changed' };
  for (const target of excludedTargets(forbidden, scenario)) {
    if ((await matchedOwners(page, target, 'data-bc-id', scenario)).includes(element.id)) return { ok: false, detail: 'forbidden' };
  }
  return { ok: true };
}

/** Opis elementu dla modelu i historii: `<role> "<name>" in <region>`. */
export function describeElement(element) {
  const name = element.name === '' ? '(no name)' : `"${element.name}"`;
  return `${element.role} ${name}${element.region ? ` in ${element.region}` : ''}${element.context ? ` (item: "${element.context}")` : ''}`;
}

/**
 * Akcje (etykieta → opis dla modelu). `textbox`/`contenteditable` → fill (tylko gdy są dane testowe), natywny select →
 * select, reszta → click; dodatkowo back, press:Escape (otwarta nakładka) i none (zawsze ostatnia).
 * Otwarta nakładka bez żadnego dostępnego elementu (modalna bez kontrolek) zostawia tylko press:Escape i none.
 */
export function buildActions(elements, { hasTestData, canGoBack, overlayOpen }) {
  const actions = {};
  for (const element of elements) {
    const described = describeElement(element);
    if (element.kind === 'text' || element.kind === 'contenteditable') {
      if (!hasTestData) continue;
      actions[`fill:${element.id}`] = `Type into ${described} (current: "${element.value ?? ''}")`;
    } else if (element.kind === 'select') {
      actions[`select:${element.id}`] = `Choose an option in ${described} (current: "${element.value ?? ''}")`;
    } else {
      let state = '';
      if (element.checked !== undefined) state += element.checked ? ' (checked)' : ' (not checked)';
      if (element.expanded !== undefined) state += element.expanded ? ' (expanded)' : ' (collapsed)';
      actions[`click:${element.id}`] = `Click ${described}${state}`;
    }
  }
  if (canGoBack && !(overlayOpen && elements.length === 0)) actions.back = 'Go back to the previous page';
  if (overlayOpen) actions['press:Escape'] = 'Press Escape to close the open overlay';
  actions.none = 'No listed action moves toward the goal';
  return actions;
}

function readField(locator) {
  return locator.evaluate((element) => ('value' in element ? element.value : (element.innerText ?? element.textContent ?? '')));
}

/**
 * Weryfikacja wpisu (tylko heurystyka ponowienia i ostrzeżenie `valueMatched`, NIE werdykt): wartość pola równa
 * oczekiwanej albo — gdy oczekiwana to numer — cyfry pola kończą się cyframi oczekiwanej (maski telefonu dodają
 * prefiks i spacje). O wyniku przejścia rozstrzygają asercje, które mają ścisłą semantykę (`prefix`).
 */
function typedValueMatches(actual, expected) {
  if (actual === expected) return true;
  if (!/^[\d\s+()-]+$/.test(expected) || !/\d/.test(expected)) return false;
  const wanted = expected.replace(/\D/g, '');
  return wanted !== '' && actual.replace(/\D/g, '').endsWith(wanted);
}

async function settle(page, settleMs) {
  await page.waitForLoadState('domcontentloaded').catch(() => {});
  await page.waitForLoadState('networkidle', { timeout: 3000 }).catch(() => {});
  await page.waitForTimeout(settleMs).catch(() => {});
}

/**
 * Wykonuje akcję (`click:eN`, `fill:eN`, `select:eN`, `back`, `press:Escape`). Bez `force`.
 * `select` wybiera ORYGINALNĄ opcję po indeksie (`optionIndex`), nigdy po zamaskowanej etykiecie, i tuż przed wyborem
 * sprawdza prywatny odcisk jej tekstu (`expectedOptionIdentity` z `optionIdentityOf`); różnica → `{ ok: false, stale: true }`.
 */
export async function executeAction(page, action, { value, optionIndex, expectedOptionIdentity, scenario, timeoutMs = 8000, settleMs = 400 } = {}) {
  const startedAt = Date.now();
  try {
    const result = { ok: true };
    if (action === 'back') {
      await page.goBack({ waitUntil: 'domcontentloaded', timeout: timeoutMs });
    } else if (action === 'press:Escape') {
      await page.keyboard.press('Escape');
    } else {
      const parsed = /^(click|fill|select):(e\d+)$/.exec(action);
      if (!parsed) return { ok: false, error: `unknown action "${action}"` };
      const locator = page.locator(`[data-bc-id="${parsed[2]}"]`);
      if (parsed[1] === 'click') {
        await locator.click({ timeout: timeoutMs });
      } else if (parsed[1] === 'select') {
        if (!Number.isInteger(optionIndex) || optionIndex < 0) return { ok: false, error: 'select without option index' };
        // Tuż przed wyborem: tekst opcji pod tym indeksem musi mieć ten sam prywatny odcisk co w zebranym stanie
        // (lista opcji mogła się zmienić: [Alpha, Beta] -> [Beta, Alpha]). Brak odcisku = fail-closed.
        const limit = rawLimitFor(scenario);
        const liveText = await locator.evaluate((select, args) => (select.options?.[args.index] ? String(select.options[args.index].text ?? '').slice(0, args.limit) : null), { index: optionIndex, limit }, { timeout: timeoutMs });
        if (liveText === null || expectedOptionIdentity === undefined || sha1(secretSafeText(scenario, liveText)) !== expectedOptionIdentity) {
          return { ok: false, stale: true, detail: 'changed', error: 'STALE_ELEMENT' };
        }
        // Odczyt opcji zużył część budżetu (`timeoutMs` = min(limit akcji, czas do terminu)): po nim nie wolno już wybierać.
        const left = timeoutMs - (Date.now() - startedAt);
        if (left <= 0) return { ok: false, error: 'TIMEOUT' };
        await locator.selectOption({ index: optionIndex }, { timeout: left });
      } else {
        await locator.fill(value, { timeout: timeoutMs });
        let actual = await readField(locator);
        if (!typedValueMatches(actual, value)) {
          await locator.clear({ timeout: timeoutMs });
          await locator.pressSequentially(value, { delay: 30, timeout: timeoutMs });
          actual = await readField(locator);
        }
        result.valueMatched = typedValueMatches(actual, value);
      }
    }
    await settle(page, settleMs);
    return result;
  } catch (error) {
    await page.waitForTimeout(settleMs).catch(() => {});
    return { ok: false, error: firstLine(error) };
  }
}
