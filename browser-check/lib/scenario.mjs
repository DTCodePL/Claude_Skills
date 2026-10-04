// Wczytanie scenariusza: JSON -> podstawienia ${env:NAZWA} -> wartości domyślne -> walidacja.
import { readFile } from 'node:fs/promises';
import { validateTarget } from './locators.mjs';
import { maskSecrets } from './mask.mjs';

export class ScenarioError extends Error {
  constructor(message) {
    super(message);
    this.name = 'ScenarioError';
  }
}

const ENV_PATTERN = /\$\{env:([^}]*)\}/g;
const NAME_PATTERN = /^[a-z0-9-]+$/;
const STEP_ACTIONS = ['click', 'fill', 'press', 'wait'];
const THEMES = ['light', 'dark'];
const MIN_SECRET_LENGTH = 4;
const MAX_TIMEOUT_MS = 2147483647; // górna granica setTimeout (int32); powyżej timer odpala natychmiast

const TOP_LEVEL_KEYS = ['baseUrl', 'timeoutMs', 'settleMs', 'browser', 'login', 'theme', 'viewports', 'themes', 'matrix', 'flows', 'flowDefaults'];
const BROWSER_KEYS = ['channel', 'headless'];
const LOGIN_KEYS = ['url', 'successUrl', 'viewport', 'submit', 'fields'];
const LOGIN_FIELD_KEYS = ['label', 'target', 'value'];
const THEME_KEYS = ['toggle', 'toggleByViewport', 'darkClass', 'settleMs'];
const VIEWPORT_KEYS = ['name', 'width', 'height'];
const MATRIX_KEYS = ['name', 'path', 'waitFor', 'timeoutMs', 'fullPage', 'steps'];
const STEP_KEYS = ['action', 'target', 'value', 'ms', 'optional'];

const DEFAULT_VIEWPORTS = [
  { name: 'mobile', width: 360, height: 530 },
  { name: 'desktop', width: 1280, height: 720 },
];

/** Podstawia ${env:X} w każdym łańcuchu (rekurencyjnie). Zbiera podstawione wartości do `secrets`. */
function substitute(node, where, secrets) {
  if (typeof node === 'string') {
    return node.replace(ENV_PATTERN, (_, name) => {
      const value = process.env[name];
      if (value === undefined || value === '') {
        throw new ScenarioError(`Brak zmiennej środowiskowej ${name} (użyta w ${where})`);
      }
      if (value.length < MIN_SECRET_LENGTH) {
        throw new ScenarioError(
          `Zmienna środowiskowa ${name} (użyta w ${where}) jest za krótka do bezpiecznego maskowania (minimum ${MIN_SECRET_LENGTH} znaki)`,
        );
      }
      secrets.add(value);
      return value;
    });
  }
  if (Array.isArray(node)) return node.map((item, index) => substitute(item, `${where}[${index}]`, secrets));
  if (node !== null && typeof node === 'object') {
    const result = {};
    for (const [key, value] of Object.entries(node)) {
      result[key] = substitute(value, where === '' ? key : `${where}.${key}`, secrets);
    }
    return result;
  }
  return node;
}

/**
 * Formy zapisu każdego sekretu, które mogą trafić na stdout/do raportu: surowa, zakodowana
 * `encodeURIComponent` (np. w adresie URL) i zakodowana jak w łańcuchu JSON (raport jest maskowany po
 * `JSON.stringify`, więc `"` i `\` występują tam z ukośnikiem). Najdłuższe pierwsze.
 */
function secretForms(secrets) {
  const forms = new Set();
  for (const secret of secrets) {
    // Forma ze spłaszczonymi białymi znakami (tekst ze strony bywa zwinięty) — tylko gdy różni się od surowej.
    const flat = secret.replace(/\s+/g, ' ').trim();
    const variants = flat !== secret && flat.length >= MIN_SECRET_LENGTH ? [secret, flat] : [secret];
    for (const variant of variants) {
      forms.add(variant);
      forms.add(encodeURIComponent(variant));
      forms.add(JSON.stringify(variant).slice(1, -1));
      forms.add(encodeURIComponent(variant).replace(/%20/g, '+')); // zapytanie w formie application/x-www-form-urlencoded
    }
  }
  return [...forms].sort((a, b) => b.length - a.length);
}

function fail(where, message) {
  throw new ScenarioError(`${where}: ${message}`);
}

function isObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

/** Ścisłe klucze: nieznany klucz to błąd z jego pełną ścieżką (np. `matrix[0].fulPage`). */
function checkKeys(object, allowed, where) {
  for (const key of Object.keys(object)) {
    if (!allowed.includes(key)) fail(where === '' ? key : `${where}.${key}`, `nieznany klucz (dozwolone: ${allowed.join(', ')})`);
  }
}

function checkTarget(target, where) {
  try {
    validateTarget(target);
  } catch (error) {
    fail(where, error.message);
  }
}

function checkPositiveInt(value, where) {
  if (!Number.isInteger(value) || value <= 0) fail(where, 'musi być dodatnią liczbą całkowitą');
}

function checkTimeout(value, where) {
  checkPositiveInt(value, where);
  if (value > MAX_TIMEOUT_MS) fail(where, `nie może przekraczać ${MAX_TIMEOUT_MS}`);
}

function checkNonNegativeInt(value, where) {
  if (!Number.isInteger(value) || value < 0) fail(where, 'musi być liczbą całkowitą >= 0');
}

/** Ścieżka względna: dokładnie jeden wiodący "/", bez "\" i bez schematu; URL powstaje przez `new URL(path, baseUrl)`. */
function checkPath(value, where) {
  if (typeof value !== 'string' || !/^\/(?!\/)/.test(value)) fail(where, 'musi być ścieżką zaczynającą się od jednego "/" (bez "//" i schematu)');
  if (value.includes('\\')) fail(where, 'nie może zawierać "\\"');
  // URL ignoruje tabulatory i znaki nowej linii, więc "/<TAB>/host/x" stałoby się "//host/x".
  if (/[\u0000-\u001F\u007F]/.test(value)) fail(where, 'nie może zawierać znaków sterujących');
}

/** Po walidacji składni: adres zbudowany ze ścieżki musi zostać w originie `baseUrl`. */
function checkSameOrigin(value, where, baseUrl) {
  let origin = null;
  try {
    origin = new URL(value, baseUrl).origin;
  } catch {
    // niepoprawny adres — błąd poniżej
  }
  if (origin !== new URL(baseUrl).origin) fail(where, 'ścieżka wychodzi poza origin baseUrl');
}

function normalizeBaseUrl(value) {
  if (typeof value !== 'string') fail('baseUrl', 'wymagane');
  if (!/^https?:\/\/[^/?#@\s]+\/?$/i.test(value)) {
    fail('baseUrl', 'musi mieć postać http(s)://host[:port] bez ścieżki, zapytania i danych logowania (dopuszczalny końcowy "/")');
  }
  try {
    new URL(value);
  } catch {
    fail('baseUrl', 'nie jest poprawnym adresem http(s)');
  }
  return value.replace(/\/+$/, '');
}

function normalizeViewports(raw) {
  const viewports = raw ?? DEFAULT_VIEWPORTS;
  if (!Array.isArray(viewports) || viewports.length === 0) fail('viewports', 'musi być niepustą tablicą');
  const names = new Set();
  viewports.forEach((viewport, index) => {
    const where = `viewports[${index}]`;
    if (!isObject(viewport)) fail(where, 'musi być obiektem');
    checkKeys(viewport, VIEWPORT_KEYS, where);
    if (typeof viewport.name !== 'string' || !NAME_PATTERN.test(viewport.name)) fail(`${where}.name`, 'wymagane, wzorzec [a-z0-9-]+');
    if (names.has(viewport.name)) fail(`${where}.name`, `duplikat "${viewport.name}"`);
    names.add(viewport.name);
    checkPositiveInt(viewport.width, `${where}.width`);
    checkPositiveInt(viewport.height, `${where}.height`);
  });
  return viewports;
}

function normalizeLogin(raw, viewports) {
  if (raw === undefined || raw === null) return null;
  if (!isObject(raw)) fail('login', 'musi być obiektem');
  checkKeys(raw, LOGIN_KEYS, 'login');
  const login = {
    url: raw.url ?? '/logowanie',
    successUrl: raw.successUrl ?? '**/panel/**',
    viewport: raw.viewport ?? 'desktop',
    submit: raw.submit,
    fields: raw.fields,
  };
  checkPath(login.url, 'login.url');
  if (typeof login.successUrl !== 'string' || login.successUrl === '') fail('login.successUrl', 'musi być niepustym łańcuchem');
  if (!viewports.some((viewport) => viewport.name === login.viewport)) {
    fail('login.viewport', `nie ma takiego viewportu: "${login.viewport}"`);
  }
  if (login.submit === undefined) fail('login.submit', 'wymagane');
  checkTarget(login.submit, 'login.submit');
  if (!Array.isArray(login.fields) || login.fields.length === 0) fail('login.fields', 'musi być niepustą tablicą');
  login.fields = login.fields.map((field, index) => {
    const where = `login.fields[${index}]`;
    if (!isObject(field)) fail(where, 'musi być obiektem');
    checkKeys(field, LOGIN_FIELD_KEYS, where);
    if (field.label !== undefined && field.target !== undefined) fail(where, 'podaj "label" albo "target", nie oba');
    const target = field.target ?? (field.label !== undefined ? { label: field.label } : undefined);
    if (target === undefined) fail(where, 'wymagane "label" albo "target"');
    checkTarget(target, `${where}.target`);
    if (typeof field.value !== 'string') fail(`${where}.value`, 'musi być łańcuchem');
    return { target, value: field.value };
  });
  return login;
}

function checkToggle(toggle, where) {
  if (toggle === undefined) fail(where, 'wymagane');
  const targets = Array.isArray(toggle) ? toggle : [toggle];
  if (targets.length === 0) fail(where, 'lista kliknięć nie może być pusta');
  targets.forEach((target, index) => checkTarget(target, Array.isArray(toggle) ? `${where}[${index}]` : where));
}

function normalizeTheme(raw, themes, viewports) {
  if (raw === undefined || raw === null) {
    if (themes.includes('dark')) fail('theme', 'wymagane, gdy "themes" zawiera "dark"');
    return null;
  }
  if (!isObject(raw)) fail('theme', 'musi być obiektem');
  checkKeys(raw, THEME_KEYS, 'theme');
  const theme = {
    toggle: raw.toggle,
    toggleByViewport: raw.toggleByViewport ?? {},
    darkClass: raw.darkClass ?? 'app-dark',
    settleMs: raw.settleMs ?? 900,
  };
  checkToggle(theme.toggle, 'theme.toggle');
  if (!isObject(theme.toggleByViewport)) fail('theme.toggleByViewport', 'musi być obiektem {nazwaViewportu: target | [target, ...]}');
  for (const [name, toggle] of Object.entries(theme.toggleByViewport)) {
    if (!viewports.some((viewport) => viewport.name === name)) fail(`theme.toggleByViewport.${name}`, 'nie ma takiego viewportu');
    checkToggle(toggle, `theme.toggleByViewport.${name}`);
  }
  if (typeof theme.darkClass !== 'string' || theme.darkClass === '') fail('theme.darkClass', 'musi być niepustym łańcuchem');
  checkNonNegativeInt(theme.settleMs, 'theme.settleMs');
  return theme;
}

function normalizeStep(step, where) {
  if (!isObject(step)) fail(where, 'musi być obiektem');
  checkKeys(step, STEP_KEYS, where);
  if (!STEP_ACTIONS.includes(step.action)) fail(`${where}.action`, `dozwolone: ${STEP_ACTIONS.join(', ')}`);
  if (step.target !== undefined) checkTarget(step.target, `${where}.target`);
  switch (step.action) {
    case 'click':
      if (step.target === undefined) fail(where, 'click wymaga "target"');
      break;
    case 'fill':
      if (step.target === undefined) fail(where, 'fill wymaga "target"');
      if (typeof step.value !== 'string') fail(`${where}.value`, 'fill wymaga "value" (łańcuch)');
      break;
    case 'press':
      if (typeof step.value !== 'string' || step.value === '') fail(`${where}.value`, 'press wymaga "value" (klawisz)');
      break;
    case 'wait':
      if (step.target !== undefined && step.ms !== undefined) fail(where, 'wait przyjmuje "target" albo "ms", nie oba');
      if (step.target === undefined) checkNonNegativeInt(step.ms, `${where}.ms`);
      break;
  }
  if (step.optional !== undefined && typeof step.optional !== 'boolean') fail(`${where}.optional`, 'musi być true/false');
  return { ...step, optional: step.optional ?? false };
}

function normalizeMatrix(raw) {
  const matrix = raw ?? [];
  if (!Array.isArray(matrix)) fail('matrix', 'musi być tablicą');
  const names = new Set();
  return matrix.map((route, index) => {
    const where = `matrix[${index}]`;
    if (!isObject(route)) fail(where, 'musi być obiektem');
    checkKeys(route, MATRIX_KEYS, where);
    if (typeof route.name !== 'string' || !NAME_PATTERN.test(route.name)) fail(`${where}.name`, 'wymagane, wzorzec [a-z0-9-]+');
    if (names.has(route.name)) fail(`${where}.name`, `duplikat "${route.name}"`);
    names.add(route.name);
    checkPath(route.path, `${where}.path`);
    if (route.waitFor !== undefined) checkTarget(route.waitFor, `${where}.waitFor`);
    if (route.timeoutMs !== undefined) checkTimeout(route.timeoutMs, `${where}.timeoutMs`);
    if (route.fullPage !== undefined && typeof route.fullPage !== 'boolean') fail(`${where}.fullPage`, 'musi być true/false');
    const steps = route.steps ?? [];
    if (!Array.isArray(steps)) fail(`${where}.steps`, 'musi być tablicą');
    return {
      ...route,
      fullPage: route.fullPage ?? false,
      steps: steps.map((step, stepIndex) => normalizeStep(step, `${where}.steps[${stepIndex}]`)),
    };
  });
}

/** Waliduje tylko pola wspólne dla CLI (nawigacja startowa); resztę flow przepuszcza — sprawdza ją moduł flows. */
function normalizeFlows(raw, viewports, theme) {
  const flows = raw ?? [];
  if (!Array.isArray(flows)) fail('flows', 'musi być tablicą');
  const names = new Set();
  flows.forEach((flow, index) => {
    const where = `flows[${index}]`;
    if (!isObject(flow)) fail(where, 'musi być obiektem');
    if (typeof flow.name !== 'string' || !NAME_PATTERN.test(flow.name)) fail(`${where}.name`, 'wymagane, wzorzec [a-z0-9-]+');
    if (names.has(flow.name)) fail(`${where}.name`, `duplikat "${flow.name}"`);
    names.add(flow.name);
    checkPath(flow.startPath, `${where}.startPath`);
    const viewportName = flow.viewport ?? 'desktop';
    if (!viewports.some((viewport) => viewport.name === viewportName)) {
      const hint = flow.viewport === undefined ? ' (domyślny dla flow bez pola "viewport")' : '';
      fail(`${where}.viewport`, `nie ma takiego viewportu: "${viewportName}"${hint}`);
    }
    if (flow.theme !== undefined) {
      if (!THEMES.includes(flow.theme)) fail(`${where}.theme`, `dozwolone: ${THEMES.join(', ')}`);
      if (flow.theme === 'dark' && theme === null) fail(`${where}.theme`, '"dark" wymaga sekcji "theme" w scenariuszu');
    }
    if (flow.waitFor !== undefined) checkTarget(flow.waitFor, `${where}.waitFor`);
    if (flow.timeoutMs !== undefined) checkPositiveInt(flow.timeoutMs, `${where}.timeoutMs`);
  });
  return flows;
}

/** Wczytuje i waliduje scenariusz. Rzuca ScenarioError (z `secrets` do maskowania komunikatu). */
export async function loadScenario(path) {
  let text;
  try {
    text = await readFile(path, 'utf8');
  } catch (error) {
    throw new ScenarioError(`Nie można odczytać pliku scenariusza "${path}": ${error.code ?? error.message}`);
  }
  let parsed;
  try {
    parsed = JSON.parse(text.replace(/^﻿/, ''));
  } catch (error) {
    throw new ScenarioError(`Plik scenariusza "${path}" nie jest poprawnym JSON-em: ${error.message}`);
  }
  if (!isObject(parsed)) throw new ScenarioError('Scenariusz musi być obiektem JSON');

  const secrets = new Set();
  // Klucz API modelu nie pochodzi ze scenariusza, ale nie może trafić do stanu, stdout ani raportów.
  const apiKey = process.env.TYPESAFE_API_KEY;
  if (apiKey && apiKey.length >= MIN_SECRET_LENGTH) secrets.add(apiKey);
  let scenario;
  try {
    scenario = buildScenario(parsed, secrets);
  } catch (error) {
    // Komunikat mógł zacytować podstawioną wartość — CLI maskuje go przez redact(error, ...).
    if (error instanceof ScenarioError) Object.defineProperty(error, 'secrets', { value: secretForms(secrets), enumerable: false });
    throw error;
  }
  Object.defineProperty(scenario, 'secrets', { value: secretForms(secrets), enumerable: false });
  return scenario;
}

function buildScenario(parsed, secrets) {
  const raw = substitute(parsed, '', secrets);
  checkKeys(raw, TOP_LEVEL_KEYS, '');

  const baseUrl = normalizeBaseUrl(raw.baseUrl);

  const timeoutMs = raw.timeoutMs ?? 600000;
  checkTimeout(timeoutMs, 'timeoutMs');
  const settleMs = raw.settleMs ?? 400;
  checkNonNegativeInt(settleMs, 'settleMs');

  if (raw.browser !== undefined && !isObject(raw.browser)) fail('browser', 'musi być obiektem');
  checkKeys(raw.browser ?? {}, BROWSER_KEYS, 'browser');
  const browserConfig = { channel: 'chrome', headless: true, ...raw.browser };
  if (typeof browserConfig.channel !== 'string' || browserConfig.channel === '') fail('browser.channel', 'musi być niepustym łańcuchem');
  if (typeof browserConfig.headless !== 'boolean') fail('browser.headless', 'musi być true/false');

  const viewports = normalizeViewports(raw.viewports);
  const themes = raw.themes ?? ['light', 'dark'];
  if (!Array.isArray(themes) || themes.length === 0 || themes.some((theme) => !THEMES.includes(theme))) {
    fail('themes', `musi być niepustą tablicą z wartości: ${THEMES.join(', ')}`);
  }

  const login = normalizeLogin(raw.login, viewports);
  const theme = normalizeTheme(raw.theme, themes, viewports);
  const matrix = normalizeMatrix(raw.matrix);
  const flows = normalizeFlows(raw.flows, viewports, theme);

  if (login) checkSameOrigin(login.url, 'login.url', baseUrl);
  matrix.forEach((route, index) => checkSameOrigin(route.path, `matrix[${index}].path`, baseUrl));
  flows.forEach((flow, index) => checkSameOrigin(flow.startPath, `flows[${index}].startPath`, baseUrl));

  const scenario = { baseUrl, timeoutMs, settleMs, browser: browserConfig, login, theme, viewports, themes, matrix, flows };
  if (raw.flowDefaults !== undefined) scenario.flowDefaults = raw.flowDefaults; // bez walidacji — czyta ją moduł flows
  return scenario;
}

/** Maskuje w tekście wartości podstawione ze zmiennych środowiskowych (też w formach URL i JSON). `source`: scenariusz albo ScenarioError. */
export function redact(source, text) {
  return maskSecrets(source, text);
}

/**
 * Redakcja rekurencyjna: maskuje wartości tekstowe obiektu PRZED `JSON.stringify`, więc wynik zostaje poprawnym
 * JSON-em dla dowolnego sekretu (np. "null", "true", cudzysłów) — liczby, wartości logiczne i `null` nie są ruszane.
 */
export function redactDeep(source, value) {
  if (typeof value === 'string') return redact(source, value);
  if (Array.isArray(value)) return value.map((item) => redactDeep(source, item));
  if (value !== null && typeof value === 'object') {
    const result = {};
    for (const [key, item] of Object.entries(value)) result[key] = redactDeep(source, item);
    return result;
  }
  return value;
}
