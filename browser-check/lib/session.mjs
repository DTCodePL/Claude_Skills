// Przeglądarka, logowanie, strony z kolektorami zdarzeń, motyw, gotowość strony.
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { chromium } from 'playwright';
import { describeTarget, toLocator } from './locators.mjs';
import { maskText, maskUrl } from './mask.mjs';

const MAX_CONSOLE_LENGTH = 300;

export function findViewport(scenario, name) {
  const viewport = scenario.viewports.find((candidate) => candidate.name === name);
  if (!viewport) throw new Error(`nie ma viewportu "${name}" (dostępne: ${scenario.viewports.map((v) => v.name).join(', ')})`);
  return viewport;
}

export async function launchBrowser(scenario, { headed = false } = {}) {
  return chromium.launch({
    channel: scenario.browser.channel,
    headless: !headed && scenario.browser.headless,
  });
}

async function visibleAlerts(page) {
  const texts = await page.locator('[role="alert"]:visible').allInnerTexts();
  return texts.map((text) => text.replace(/\s+/g, ' ').trim()).filter(Boolean);
}

async function fillAndVerify(page, fields) {
  const locators = fields.map((field) => toLocator(page, field.target).first());
  for (let index = 0; index < fields.length; index++) await locators[index].fill(fields[index].value);
  // Weryfikacja po wypełnieniu wszystkich pól (hydratacja mogła wyczyścić wcześniejsze); jedna powtórka.
  for (let index = 0; index < fields.length; index++) {
    if ((await locators[index].inputValue()) !== fields[index].value) await locators[index].fill(fields[index].value);
  }
  for (let index = 0; index < fields.length; index++) {
    if ((await locators[index].inputValue()) !== fields[index].value) {
      throw new Error(`pole nie zachowało wartości: ${describeTarget(fields[index].target)}`);
    }
  }
}

async function submitAndWait(page, config) {
  await fillAndVerify(page, config.fields);
  await toLocator(page, config.submit).first().click({ timeout: 10000 });
  try {
    await page.waitForURL(config.successUrl, { timeout: 15000 });
    return true;
  } catch {
    return false;
  }
}

/**
 * Zapisuje same ciasteczka kontekstu (bez localStorage — motyw wybrany w jednym kontekście nie może
 * przeciekać do następnego). Refresh token jest jednorazowy i rotowany przy każdym odtworzeniu sesji,
 * więc plik stanu trzeba odświeżać przed zamknięciem kontekstu, z którego korzystał kolejny kontekst.
 */
export async function saveCookies(context, filePath) {
  const state = await context.storageState();
  await mkdir(path.dirname(filePath), { recursive: true, mode: 0o700 });
  await writeFile(filePath, JSON.stringify({ cookies: state.cookies, origins: [] }), { encoding: 'utf8', mode: 0o600 });
}

/** Ścieżka pliku stanu sesji dla katalogu wyników (używa jej login() i handler sygnałów w CLI). */
export function storageStateFile(outDir) {
  return path.join(outDir, '.auth', 'storage-state.json');
}

/** Loguje w osobnym kontekście i zapisuje storageState. Wartości pól nigdy nie trafiają do wyniku. */
export async function login(browser, scenario, outDir) {
  const startedAt = Date.now();
  const config = scenario.login;
  const viewport = findViewport(scenario, config.viewport);
  const context = await browser.newContext({
    viewport: { width: viewport.width, height: viewport.height },
    colorScheme: 'light',
    baseURL: scenario.baseUrl,
  });
  const page = await context.newPage();
  page.on('dialog', (dialog) => dialog.accept().catch(() => {}));
  try {
    try {
      await page.goto(new URL(config.url, scenario.baseUrl).href, { waitUntil: 'domcontentloaded', timeout: 30000 });
      await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});
      let success = await submitAndWait(page, config);
      if (!success && (await visibleAlerts(page)).length === 0) success = await submitAndWait(page, config);
      if (success) {
        const storageStatePath = storageStateFile(outDir);
        await saveCookies(context, storageStatePath);
        return { ok: true, durationMs: Date.now() - startedAt, storageStatePath };
      }
      const alerts = await visibleAlerts(page);
      return await failure(page, scenario, outDir, startedAt, alerts.length > 0 ? alerts.join(' | ') : `timeout waiting for ${config.successUrl}`);
    } catch (error) {
      return await failure(page, scenario, outDir, startedAt, firstLine(error));
    }
  } finally {
    await context.close().catch(() => {});
  }
}

async function failure(page, scenario, outDir, startedAt, message) {
  const screenshot = path.join(outDir, 'login-failed.png');
  let shotPath = null;
  try {
    await page.screenshot({ path: screenshot });
    shotPath = screenshot;
  } catch {
    // brak zrzutu nie zmienia wyniku
  }
  let url = null;
  try {
    url = page.url();
  } catch {
    // ignoruj
  }
  return { ok: false, durationMs: Date.now() - startedAt, error: maskText(scenario, url ? `${message} (url: ${maskUrl(scenario, url)})` : message), screenshot: shotPath };
}

function firstLine(error) {
  return String(error?.message ?? error).split('\n')[0].trim();
}

/** Strona w nowym kontekście + kolektor błędów (tylko ten sam origin dla sieci). */
export async function openPage(browser, scenario, { viewport, storageStatePath } = {}) {
  const options = {
    viewport: { width: viewport.width, height: viewport.height },
    colorScheme: 'light',
    baseURL: scenario.baseUrl,
  };
  if (storageStatePath) options.storageState = storageStatePath;
  const context = await browser.newContext(options);
  const page = await context.newPage();
  const origin = new URL(scenario.baseUrl).origin;
  const sameOrigin = (url) => {
    try {
      return new URL(url).origin === origin;
    } catch {
      return false;
    }
  };

  // Maskowanie (sekrety i dane osobowe) przed skróceniem — inaczej cięcie mogłoby zostawić ucięty, niemaskowalny sekret.
  const clip = (text) => maskText(scenario, text).slice(0, MAX_CONSOLE_LENGTH);

  let state = { consoleErrors: [], pageErrors: [], failedRequests: [], dialogs: [] };
  page.on('console', (message) => {
    if (message.type() === 'error') state.consoleErrors.push(clip(message.text()));
  });
  page.on('pageerror', (error) => state.pageErrors.push(clip(String(error?.message ?? error))));
  page.on('response', (response) => {
    if (response.status() >= 400 && sameOrigin(response.url())) {
      state.failedRequests.push({ url: maskUrl(scenario, response.url()), status: response.status() });
    }
  });
  page.on('requestfailed', (request) => {
    if (!sameOrigin(request.url())) return;
    if (String(request.failure()?.errorText ?? '').includes('ERR_ABORTED')) return; // anulowania przez nawigację
    state.failedRequests.push({ url: maskUrl(scenario, request.url()), status: 0 });
  });
  page.on('dialog', (dialog) => {
    state.dialogs.push(dialog.type());
    dialog.accept().catch(() => {});
  });

  const persistSession = async () => {
    if (storageStatePath) await saveCookies(context, storageStatePath);
  };
  const collector = {
    drain() {
      const drained = state;
      state = { consoleErrors: [], pageErrors: [], failedRequests: [], dialogs: [] };
      return drained;
    },
  };
  return { context, page, collector, persistSession };
}

/** route: pełna trasa albo obiekt z samym waitFor/timeoutMs. */
export async function waitForReady(page, scenario, route = {}) {
  if (route.waitFor) {
    await toLocator(page, route.waitFor)
      .first()
      .waitFor({ state: 'visible', timeout: route.timeoutMs ?? 15000 });
  } else {
    await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});
  }
  await page.evaluate(() => document.fonts.ready.then(() => true));
  await page.waitForTimeout(scenario.settleMs);
}

async function readTheme(page, darkClass) {
  return page.evaluate(
    (className) => ({
      darkClass: document.documentElement.classList.contains(className),
      bodyBackground: getComputedStyle(document.body).backgroundColor,
    }),
    darkClass,
  );
}

/** Cele kliknięć przełączające motyw: nadpisanie per viewport (np. mobile: arkusz menu użytkownika) albo `theme.toggle`. */
function toggleTargets(scenario, viewportName) {
  const byViewport = scenario.theme.toggleByViewport;
  const chosen = Object.hasOwn(byViewport, viewportName) ? byViewport[viewportName] : scenario.theme.toggle;
  return Array.isArray(chosen) ? chosen : [chosen];
}

/** Ustawia motyw WYŁĄCZNIE przez kliknięcie przełącznika + przeładowanie strony. `viewportName` wybiera `toggleByViewport`. */
export async function ensureTheme(page, scenario, wanted, route, viewportName) {
  const darkClass = scenario.theme?.darkClass ?? 'app-dark';
  const matches = (state) => state.darkClass === (wanted === 'dark');
  let state = await readTheme(page, darkClass);
  if (matches(state)) return state;
  if (!scenario.theme) {
    if (wanted === 'dark') throw new Error('theme mismatch: wanted dark, scenario has no "theme" section');
    return state;
  }
  const clicks = toggleTargets(scenario, viewportName);
  for (const [index, target] of clicks.entries()) {
    if (index > 0) await page.waitForTimeout(scenario.settleMs);
    await toLocator(page, target).first().click({ timeout: 5000 });
  }
  await page.waitForTimeout(scenario.theme.settleMs);
  await page.reload({ waitUntil: 'domcontentloaded' });
  await waitForReady(page, scenario, route);
  state = await readTheme(page, darkClass);
  if (!matches(state)) {
    throw new Error(`theme mismatch: wanted ${wanted}, got ${state.darkClass ? 'dark' : 'light'}`);
  }
  return state;
}
