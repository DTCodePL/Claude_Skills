// Asercje przejść (flows): deterministyczne sprawdzenia Playwrighta — to one rozstrzygają o wyniku, nie model.
// Trzy formy (dokładnie jedna na obiekt):
//   { target, state: 'visible'|'hidden', hasText?, within? }
//   { url: 'glob' }
//   { target, value: '…', match?: 'exact'|'digits', prefix?, within? }
// `within` (Target) zawęża wyszukiwanie `target` do pierwszego WIDOCZNEGO dopasowania zakresu.
import { describeTarget, toLocator, validateTarget } from './locators.mjs';

const STATES = ['visible', 'hidden'];
const MATCHES = ['exact', 'digits'];
const ALLOWED_KEYS = ['target', 'state', 'hasText', 'url', 'value', 'match', 'prefix', 'within'];
const FINAL_TIMEOUT_MS = 5000;
const FINAL_POLL_MS = 200;

function isObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

/** Waliduje jedną asercję; zwraca listę problemów (pusta = poprawna). `path` to ścieżka pola w komunikatach. */
export function validateAssertion(assertion, path) {
  if (!isObject(assertion)) return [`${path}: asercja musi być obiektem`];
  const problems = [];
  for (const key of Object.keys(assertion)) {
    if (!ALLOWED_KEYS.includes(key)) problems.push(`${path}.${key}: nieznany klucz (dozwolone: ${ALLOWED_KEYS.join(', ')})`);
  }
  if (problems.length > 0) return problems;

  if (assertion.url !== undefined) {
    const extra = Object.keys(assertion).filter((key) => key !== 'url');
    if (extra.length > 0) problems.push(`${path}: forma "url" nie przyjmuje innych pól (podano: ${extra.join(', ')})`);
    if (typeof assertion.url !== 'string' || assertion.url === '') problems.push(`${path}.url: musi być niepustym łańcuchem (glob)`);
    return problems;
  }

  if (assertion.target === undefined) return [`${path}: wymagane "url" albo "target" (+ "state" albo "value")`];
  try {
    validateTarget(assertion.target);
  } catch (error) {
    problems.push(`${path}.target: ${error.message}`);
  }
  if (assertion.within !== undefined) {
    try {
      validateTarget(assertion.within);
    } catch (error) {
      problems.push(`${path}.within: ${error.message}`);
    }
  }
  const hasState = assertion.state !== undefined;
  const hasValue = assertion.value !== undefined;
  if (hasState === hasValue) {
    problems.push(`${path}: podaj dokładnie jedno z "state" albo "value"`);
    return problems;
  }
  if (hasState) {
    if (!STATES.includes(assertion.state)) problems.push(`${path}.state: dozwolone ${STATES.join(', ')}`);
    if (assertion.hasText !== undefined && (typeof assertion.hasText !== 'string' || assertion.hasText === '')) {
      problems.push(`${path}.hasText: musi być niepustym łańcuchem`);
    }
    if (assertion.match !== undefined) problems.push(`${path}.match: dozwolone tylko z "value"`);
    if (assertion.prefix !== undefined) problems.push(`${path}.prefix: dozwolone tylko z "value" i match "digits"`);
  } else {
    if (typeof assertion.value !== 'string') problems.push(`${path}.value: musi być łańcuchem`);
    if (assertion.match !== undefined && !MATCHES.includes(assertion.match)) problems.push(`${path}.match: dozwolone ${MATCHES.join(', ')}`);
    if (assertion.hasText !== undefined) problems.push(`${path}.hasText: dozwolone tylko ze "state"`);
    if (assertion.prefix !== undefined) {
      if (assertion.match !== 'digits') problems.push(`${path}.prefix: dozwolone tylko z match "digits"`);
      if (typeof assertion.prefix !== 'string' || !/^\d+$/.test(assertion.prefix)) problems.push(`${path}.prefix: musi być łańcuchem samych cyfr`);
    }
  }
  return problems;
}

/**
 * Glob URL: `**` = dowolny ciąg, `*` = dowolny ciąg bez `/`, reszta dosłownie (w tym `?`).
 * Zwraca RegExp zakotwiczony na całym łańcuchu (zob. `urlSubject` — co jest dopasowywane).
 */
export function globToRegExp(glob) {
  let source = '';
  for (let index = 0; index < glob.length; index++) {
    const char = glob[index];
    if (char === '*') {
      if (glob[index + 1] === '*') {
        source += '.*';
        index++;
      } else {
        source += '[^/]*';
      }
    } else {
      source += char.replace(/[\\^$.*+?()[\]{}|/-]/g, '\\$&');
    }
  }
  return new RegExp(`^${source}$`, 's');
}

/**
 * Co dopasowuje glob URL: `pathname` (bez zapytania i hasha); gdy glob zawiera `?` — `pathname + search`.
 * Origin pilnuje pętla (OFF_ORIGIN), nie asercja.
 */
export function urlSubject(glob, url) {
  const parsed = new URL(url);
  return glob.includes('?') ? parsed.pathname + parsed.search : parsed.pathname;
}

export function describeAssertion(assertion) {
  if (assertion.url !== undefined) return `url ~ "${assertion.url}"`;
  const scope = assertion.within === undefined ? '' : ` within ${describeTarget(assertion.within)}`;
  if (assertion.state !== undefined) {
    return `${describeTarget(assertion.target)}${scope} ${assertion.state}${assertion.hasText !== undefined ? ` hasText "${assertion.hasText}"` : ''}`;
  }
  const digits = assertion.match === 'digits' ? ` (digits${assertion.prefix === undefined ? '' : `, prefix ${assertion.prefix}`})` : '';
  return `${describeTarget(assertion.target)}${scope} value "${assertion.value}"${digits}`;
}

function digitsOf(text) {
  return String(text).replace(/\D/g, '');
}

/**
 * Porównanie wartości pola: `exact` = równość; `digits` = cyfry wartości rzeczywistej RÓWNE cyfrom oczekiwanej albo
 * `<prefix><oczekiwane>` (prefix: same cyfry, np. numer kierunkowy dodawany przez maskę pola). Bez innych prefiksów.
 */
export function valueMatches(actual, expected, match = 'exact', prefix = undefined) {
  if (match === 'digits') {
    const wanted = digitsOf(expected);
    if (wanted === '') return false;
    const found = digitsOf(actual);
    return found === wanted || (prefix !== undefined && prefix !== '' && found === `${prefix}${wanted}`);
  }
  return actual === expected;
}

async function readValue(locator) {
  return locator.evaluate((element) => ('value' in element ? element.value : (element.innerText ?? element.textContent ?? '')));
}

/** Pierwsze widoczne dopasowanie zakresu albo null. */
async function visibleScope(page, within) {
  const candidates = await toLocator(page, within).all();
  for (const candidate of candidates) {
    if (await candidate.isVisible().catch(() => false)) return candidate;
  }
  return null;
}

async function checkOnce(page, assertion) {
  if (assertion.url !== undefined) {
    const url = page.url();
    let subject;
    try {
      subject = urlSubject(assertion.url, url);
    } catch {
      return { ok: false, actual: url };
    }
    return { ok: globToRegExp(assertion.url).test(subject), actual: url };
  }

  let scope = page;
  if (assertion.within !== undefined) {
    scope = await visibleScope(page, assertion.within);
    if (scope === null) return { ok: false, actual: 'scope not visible' };
  }
  let locator = toLocator(scope, assertion.target);

  if (assertion.state !== undefined) {
    if (assertion.hasText !== undefined) locator = locator.filter({ hasText: assertion.hasText });
    const total = await locator.count();
    const visible = await locator.filter({ visible: true }).count();
    return { ok: assertion.state === 'visible' ? visible > 0 : visible === 0, actual: `${visible} visible of ${total} matching` };
  }

  const shown = locator.filter({ visible: true });
  const visible = await shown.count();
  if (visible === 0) return { ok: false, actual: 'no visible element' };
  if (visible > 1) return { ok: false, actual: `ambiguous (${visible} visible)` };
  const actual = await readValue(shown.first());
  return { ok: valueMatches(actual, assertion.value, assertion.match, assertion.prefix), actual };
}

async function onePass(page, assertions) {
  const results = [];
  for (const assertion of assertions) {
    let outcome;
    try {
      outcome = await checkOnce(page, assertion);
    } catch (error) {
      outcome = { ok: false, actual: `error: ${String(error?.message ?? error).split('\n')[0]}` };
    }
    results.push({ assertion: describeAssertion(assertion), ok: outcome.ok, ...(outcome.actual === undefined ? {} : { actual: outcome.actual }) });
  }
  return { ok: results.every((result) => result.ok), results };
}

/**
 * Sprawdza listę asercji (koniunkcja). Tryb szybki (domyślny): jeden przebieg całego zestawu, bez czekania.
 * `final: true`: cały zestaw jest ponawiany co ~200 ms do 5 s (lub do `until` — znacznik czasu, jeśli wcześniejszy);
 * sukces dopiero, gdy w JEDNYM przebiegu wszystkie asercje są spełnione naraz. Przebieg sprawdza asercje kolejno (nie
 * jest migawką), więc w OBU trybach udany przebieg potwierdza drugi — stan, który zmienił się w trakcie pierwszego
 * (A zniknęło, zanim zobaczyliśmy B), nie przejdzie obu. Zwracany jest ostatni przebieg.
 */
export async function checkAssertions(page, assertions, { final = false, until = Number.POSITIVE_INFINITY } = {}) {
  const limit = Math.min(Date.now() + FINAL_TIMEOUT_MS, until);
  for (;;) {
    let pass = await onePass(page, assertions);
    if (pass.ok) pass = await onePass(page, assertions);
    if (pass.ok || !final || Date.now() >= limit) return pass;
    await page.waitForTimeout(FINAL_POLL_MS).catch(() => {});
  }
}
