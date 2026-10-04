// Tryb flows: przejście funkcjonalne opisane celem (język naturalny), danymi testowymi i asercjami.
// Pętla: Playwright zbiera elementy strony, model Jev wybiera następną akcję, Playwright ją wykonuje;
// o wyniku rozstrzygają wyłącznie asercje (model niczego nie ocenia). Moduł jest ogólny — bez wiedzy o aplikacji.
import { writeFile } from 'node:fs/promises';
import path from 'node:path';
import { checkAssertions, describeAssertion, validateAssertion } from './assertions.mjs';
import { validateTarget } from './locators.mjs';
import { buildActions, collectPageState, describeElement, executeAction, FORBIDDEN_LOCATOR_INVALID, optionIdentityOf, verifyElementBeforeAction } from './page-actions.mjs';
import { createJevPolicy } from './jev-policy.mjs';
import { maskText, maskUrl } from './mask.mjs';
import { redact, redactDeep, ScenarioError } from './scenario.mjs';

const HARNESS_KEYS = ['name', 'startPath', 'viewport', 'theme', 'waitFor', 'timeoutMs'];
const FLOW_ONLY_KEYS = ['goal', 'subgoals', 'testData', 'assertions'];
const DEFAULT_KEYS = ['maxSteps', 'confidenceThreshold', 'maxOptions', 'forbidden', 'model'];
const DEFAULTS = { maxSteps: 20, confidenceThreshold: 0.75, maxOptions: 80, model: 'jev-latest' };
const DEFAULT_FLOW_TIMEOUT_MS = 120000;
const ACTION_TIMEOUT_MS = 8000;
const REPEAT_STATE_LIMIT = 4;

function isObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

function firstLine(error) {
  return String(error?.message ?? error).split('\n')[0].trim();
}

function checkTuning(object, where, problems) {
  if (object.maxSteps !== undefined && (!Number.isInteger(object.maxSteps) || object.maxSteps < 1 || object.maxSteps > 50)) {
    problems.push(`${where}.maxSteps: liczba całkowita 1–50`);
  }
  if (object.confidenceThreshold !== undefined && (typeof object.confidenceThreshold !== 'number' || !(object.confidenceThreshold >= 0 && object.confidenceThreshold <= 1))) {
    problems.push(`${where}.confidenceThreshold: liczba 0–1`);
  }
  if (object.maxOptions !== undefined && (!Number.isInteger(object.maxOptions) || object.maxOptions < 5 || object.maxOptions > 200)) {
    problems.push(`${where}.maxOptions: liczba całkowita 5–200`);
  }
  if (object.model !== undefined && (typeof object.model !== 'string' || object.model === '')) {
    problems.push(`${where}.model: niepusty łańcuch`);
  }
  if (object.forbidden !== undefined) {
    if (!Array.isArray(object.forbidden)) {
      problems.push(`${where}.forbidden: musi być tablicą targetów`);
    } else {
      object.forbidden.forEach((target, index) => {
        try {
          validateTarget(target);
        } catch (error) {
          problems.push(`${where}.forbidden[${index}]: ${error.message}`);
        }
      });
    }
  }
}

/** Walidacja pól flows, których nie waliduje CLI. Rzuca ScenarioError z listą wszystkich problemów. */
export function validateFlows(scenario) {
  const problems = [];
  const flows = Array.isArray(scenario.flows) ? scenario.flows : [];

  if (scenario.flowDefaults !== undefined) {
    if (!isObject(scenario.flowDefaults)) {
      problems.push('flowDefaults: musi być obiektem');
    } else {
      for (const key of Object.keys(scenario.flowDefaults)) {
        if (!DEFAULT_KEYS.includes(key)) problems.push(`flowDefaults.${key}: nieznany klucz (dozwolone: ${DEFAULT_KEYS.join(', ')})`);
      }
      checkTuning(scenario.flowDefaults, 'flowDefaults', problems);
    }
  }

  flows.forEach((flow, index) => {
    const where = `flows[${index}]`;
    if (!isObject(flow)) return; // CLI zgłosi to wcześniej
    const allowed = [...HARNESS_KEYS, ...FLOW_ONLY_KEYS, ...DEFAULT_KEYS];
    for (const key of Object.keys(flow)) {
      if (!allowed.includes(key)) problems.push(`${where}.${key}: nieznany klucz (dozwolone: ${allowed.join(', ')})`);
    }
    if (typeof flow.goal !== 'string' || flow.goal.trim() === '') problems.push(`${where}.goal: wymagany niepusty łańcuch`);
    if (flow.subgoals !== undefined && (!Array.isArray(flow.subgoals) || flow.subgoals.some((item) => typeof item !== 'string' || item === ''))) {
      problems.push(`${where}.subgoals: musi być tablicą niepustych łańcuchów`);
    }
    if (flow.testData !== undefined) {
      if (!isObject(flow.testData)) {
        problems.push(`${where}.testData: musi być obiektem łańcuch → łańcuch`);
      } else {
        for (const [key, value] of Object.entries(flow.testData)) {
          if (typeof value !== 'string') problems.push(`${where}.testData.${key}: wartość musi być łańcuchem`);
          if (key === 'none') problems.push(`${where}.testData.none: klucz "none" jest zarezerwowany dla modelu`);
        }
      }
    }
    if (!Array.isArray(flow.assertions) || flow.assertions.length === 0) {
      problems.push(`${where}.assertions: wymagana niepusta tablica asercji`);
    } else {
      flow.assertions.forEach((assertion, assertionIndex) => {
        problems.push(...validateAssertion(assertion, `${where}.assertions[${assertionIndex}]`));
      });
    }
    checkTuning(flow, where, problems);
  });

  if (flows.length > 0 && !process.env.TYPESAFE_API_KEY) {
    problems.push('TYPESAFE_API_KEY: brak zmiennej środowiskowej (klucz API modelu Jev)');
  }
  if (problems.length > 0) {
    throw new ScenarioError(`Nieprawidłowe flows (${problems.length}):\n  ${problems.join('\n  ')}`);
  }
}

function resolveConfig(flow, scenario) {
  const defaults = scenario.flowDefaults ?? {};
  const pick = (key) => flow[key] ?? defaults[key] ?? DEFAULTS[key];
  return {
    maxSteps: pick('maxSteps'),
    confidenceThreshold: pick('confidenceThreshold'),
    maxOptions: pick('maxOptions'),
    model: pick('model'),
    forbidden: [...(defaults.forbidden ?? []), ...(flow.forbidden ?? [])],
  };
}

function seconds(ms) {
  return (ms / 1000).toFixed(1);
}

async function safeCollect(page, options) {
  try {
    return await collectPageState(page, options);
  } catch (error) {
    // Komunikat błędu może zawierać wartości ze scenariusza albo tekst strony — maskowanie u źródła.
    return { error: maskText(options.scenario, firstLine(error)), code: error?.code };
  }
}

function originOf(page) {
  try {
    return new URL(page.url()).origin;
  } catch {
    return null; // strona zamknięta
  }
}

/**
 * Blokuje nawigacje GŁÓWNEJ ramki (dowolnej karty kontekstu) poza origin `baseUrl`. Zasoby podrzędne (skrypty, czcionki,
 * iframe — np. Turnstile) przechodzą. Przerwane żądanie zostawia stronę na starym adresie, więc `state.blocked`
 * jest osobnym dowodem próby wyjścia.
 */
export async function installOriginGuard(context, baseOrigin, onBlocked) {
  const state = { blocked: 0 };
  const foreign = (url) => url.origin !== baseOrigin;
  const handler = async (route, request) => {
    let mainFrameNavigation = false;
    try {
      mainFrameNavigation = request.isNavigationRequest() && request.frame().parentFrame() === null;
    } catch {
      // żądanie bez ramki (np. service worker) — nie jest nawigacją
    }
    if (mainFrameNavigation) {
      state.blocked++;
      onBlocked(request.url());
      await route.abort('blockedbyclient').catch(() => {});
      return;
    }
    await route.fallback().catch(() => {});
  };
  await context.route(foreign, handler);
  return { state, dispose: () => context.unroute(foreign, handler).catch(() => {}) };
}

export async function runFlow({ page, flow, scenario, outDir, log, collector }) {
  void collector; // zdarzenia konsoli/sieci drenuje CLI
  const config = resolveConfig(flow, scenario);
  const startedAt = Date.now();
  const deadline = startedAt + (flow.timeoutMs ?? DEFAULT_FLOW_TIMEOUT_MS);
  const remaining = () => deadline - Date.now();
  const baseOrigin = new URL(scenario.baseUrl).origin;
  const testData = flow.testData ?? {};
  const emit = (line) => log(redact(scenario, line));
  const policy = createJevPolicy({ model: config.model, confidenceThreshold: config.confidenceThreshold });

  const warnings = [];
  const steps = [];
  const history = [];
  const stateCounts = new Map();
  const doneActions = new Set();
  let consecutiveErrors = 0;
  let passedWithoutActions = false;
  let outcome = null; // { status, reason? }
  let fastResults = null;

  const onNewPage = (opened) => {
    warnings.push(`new tab opened and closed: ${maskUrl(scenario, opened.url() || 'about:blank')}`);
    opened.close().catch(() => {});
  };
  const context = page.context();
  context.on('page', onNewPage);
  const guard = await installOriginGuard(context, baseOrigin, (url) => {
    let target = 'unknown';
    try {
      target = new URL(url).origin;
    } catch {
      // zostaw "unknown"
    }
    warnings.push(`blocked navigation outside baseUrl origin: ${maskUrl(scenario, target)}`);
  });
  const originOk = () => guard.state.blocked === 0 && originOf(page) === baseOrigin;

  const finish = (status, reason) => {
    if (outcome === null) outcome = { status, ...(reason ? { reason } : {}) };
  };

  try {
    while (outcome === null) {
      if (remaining() <= 0) {
        finish('FAIL', 'TIMEOUT');
        break;
      }
      if (!originOk()) {
        finish('FAIL', 'OFF_ORIGIN');
        break;
      }
      if (steps.length >= config.maxSteps) break; // końcowe asercje rozstrzygną (MAX_STEPS)

      const fast = await checkAssertions(page, flow.assertions);
      if (fast.ok) {
        if (remaining() <= 0) {
          finish('FAIL', 'TIMEOUT'); // nigdy PASS po terminie
          break;
        }
        if (!originOk()) {
          finish('FAIL', 'OFF_ORIGIN'); // nigdy PASS po wyjściu poza origin (także w trakcie przebiegu asercji)
          break;
        }
        passedWithoutActions = steps.length === 0;
        fastResults = fast.results;
        finish('PASS');
        break;
      }

      const state = await safeCollect(page, { maxOptions: config.maxOptions, forbidden: config.forbidden, scenario });
      if (state.error) {
        warnings.push(`collectPageState: ${state.error}`);
        finish('ERROR', state.code === FORBIDDEN_LOCATOR_INVALID ? state.error : `PAGE_STATE: ${state.error}`);
        break;
      }

      const count = (stateCounts.get(state.fingerprint) ?? 0) + 1;
      stateCounts.set(state.fingerprint, count);
      if (count >= REPEAT_STATE_LIMIT) {
        finish('LOOP', `SAME_STATE_${REPEAT_STATE_LIMIT}X`);
        break;
      }

      const actions = buildActions(state.elements, {
        hasTestData: Object.keys(testData).length > 0,
        canGoBack: history.length > 0,
        overlayOpen: state.summary.overlay !== null,
      });
      const decision = await policy.decide({
        goal: flow.goal,
        subgoals: flow.subgoals,
        testData,
        summary: state.summary,
        history,
        actions,
        elements: state.elements,
        remainingMs: remaining,
      });

      const step = {
        n: steps.length + 1,
        url: state.summary.url,
        options: state.elements.length,
        truncated: state.truncated,
        overlay: state.summary.overlay,
        action: decision.action ?? null,
        target: null,
        ...(decision.valueKey !== undefined ? { valueKey: decision.valueKey } : {}),
        confidence: decision.confidence ?? null,
        top3: decision.top3 ?? [],
        ...(decision.stage2 ? { stage2: decision.stage2 } : {}),
        jevMs: decision.jevMs,
        actionMs: 0,
      };
      const element = decision.action ? state.elements.find((candidate) => decision.action.endsWith(`:${candidate.id}`)) : undefined;
      step.target = element ? describeElement(element) : decision.action ?? null;
      steps.push(step);

      if (decision.status !== 'OK') {
        step.error = decision.status === 'ERROR' ? decision.error : `${decision.status}: ${decision.reason}`;
        emit(`FLOW ${flow.name} #${step.n} ${decision.action ?? '-'} ${step.target ?? ''} ${decision.status} ${decision.reason ?? decision.error ?? ''} jev ${decision.jevMs}ms`);
        if (remaining() <= 0) finish('FAIL', 'TIMEOUT');
        else if (decision.status === 'ERROR') finish('ERROR', decision.error);
        else finish('NEED_FALLBACK', decision.reason);
        break;
      }

      const pairKey = `${state.fingerprint}|${decision.action}|${decision.valueKey ?? ''}|${decision.optionIndex ?? ''}`;
      if (doneActions.has(pairKey)) {
        step.error = 'LOOP: action already executed in the same page state';
        emit(`FLOW ${flow.name} #${step.n} ${decision.action} ${step.target} LOOP repeated action`);
        finish('LOOP', 'REPEATED_ACTION');
        break;
      }

      if (remaining() <= 0) {
        step.error = 'TIMEOUT';
        finish('FAIL', 'TIMEOUT');
        break;
      }

      // Tuż przed akcją: aktualny opis elementu musi zgadzać się z pokazanym modelowi i nie może być zakazany.
      if (element) {
        let verdict;
        try {
          verdict = await verifyElementBeforeAction(page, element, { forbidden: config.forbidden, scenario });
        } catch (error) {
          if (error?.code !== FORBIDDEN_LOCATOR_INVALID) throw error;
          step.error = firstLine(error);
          finish('ERROR', step.error);
          break;
        }
        if (!verdict.ok) {
          step.error = 'STALE_ELEMENT';
          step.staleDetail = verdict.detail;
          emit(`FLOW ${flow.name} #${step.n} ${decision.action} ${step.target} STALE_ELEMENT ${verdict.detail}`);
          consecutiveErrors++;
          if (consecutiveErrors >= 2) {
            finish('FAIL', 'ACTION_ERROR');
            break;
          }
          continue; // stan zbierany od nowa
        }
      }

      // Weryfikacja też zajmuje czas — po terminie akcja nie jest wykonywana.
      if (remaining() <= 0) {
        step.error = 'TIMEOUT';
        finish('FAIL', 'TIMEOUT');
        break;
      }

      const actionStartedAt = Date.now();
      const executed = await executeAction(page, decision.action, {
        value: decision.value,
        optionIndex: decision.optionIndex,
        expectedOptionIdentity: element && decision.optionIndex !== undefined ? optionIdentityOf(element, decision.optionIndex) : undefined,
        scenario,
        timeoutMs: Math.max(1, Math.min(ACTION_TIMEOUT_MS, remaining())),
        settleMs: scenario.settleMs,
      });
      step.actionMs = Date.now() - actionStartedAt;
      if (executed.stale) {
        // Lista opcji zmieniła się między decyzją a wyborem — nic nie zostało wybrane (jak STALE_ELEMENT przed akcją).
        step.error = 'STALE_ELEMENT';
        step.staleDetail = executed.detail;
        emit(`FLOW ${flow.name} #${step.n} ${decision.action} ${step.target} STALE_ELEMENT ${executed.detail}`);
        consecutiveErrors++;
        if (consecutiveErrors >= 2) {
          finish('FAIL', 'ACTION_ERROR');
          break;
        }
        continue;
      }
      if (executed.valueMatched !== undefined) step.valueMatched = executed.valueMatched;
      if (executed.valueMatched === false) warnings.push(`step ${step.n}: field value differs from test data after typing`);

      let urlAfter = '';
      try {
        const after = new URL(page.url());
        urlAfter = after.pathname + after.search;
      } catch {
        urlAfter = page.url();
      }
      history.push({
        step: step.n,
        action: decision.action,
        target: step.target,
        ...(decision.valueKey !== undefined ? { valueKey: decision.valueKey } : {}),
        ...(decision.optionLabel !== undefined ? { option: decision.optionLabel } : {}),
        ...(executed.ok ? {} : { failed: true }),
        urlAfter: maskUrl(scenario, urlAfter),
      });

      emit(
        `FLOW ${flow.name} #${step.n} ${decision.action}${decision.valueKey ? `(${decision.valueKey})` : ''} ${step.target} ` +
          `conf ${decision.confidence?.toFixed(2)} jev ${decision.jevMs}ms act ${step.actionMs}ms${executed.ok ? '' : ` ERR ${executed.error}`}`,
      );

      if (!originOk()) {
        finish('FAIL', 'OFF_ORIGIN');
        break;
      }

      if (executed.ok) {
        doneActions.add(pairKey);
        consecutiveErrors = 0;
      } else {
        step.error = executed.error;
        consecutiveErrors++;
        if (consecutiveErrors >= 2) {
          finish('FAIL', 'ACTION_ERROR');
          break;
        }
      }
    }
  } catch (error) {
    finish('ERROR', maskText(scenario, firstLine(error)));
  }

  // Końcowe asercje. Strażnik originu (i zamykanie nowych kart) zostaje zainstalowany AŻ DO ich końca, więc przekierowanie
  // na obcy origin w trakcie końcowego oczekiwania jest przerywane i widoczne w `originOk()`. Origin i termin rozstrzygają
  // PRZED asercjami i jeszcze raz bezpośrednio przed przyjęciem PASS: po wyjściu poza origin albo po terminie nigdy PASS.
  let assertionResults = fastResults;
  try {
    const pageOnOrigin = originOf(page) === baseOrigin;
    if (outcome === null && !originOk()) finish('FAIL', 'OFF_ORIGIN');
    if (outcome === null && remaining() <= 0) finish('FAIL', 'TIMEOUT');
    if (assertionResults === null) {
      if (pageOnOrigin) {
        try {
          const waiting = outcome === null; // tylko wyjście przez MAX_STEPS czeka na asercje (do 5 s, nie dłużej niż termin)
          const final = await checkAssertions(page, flow.assertions, { final: waiting, until: deadline });
          assertionResults = final.results;
          if (waiting) {
            if (!originOk()) outcome = { status: 'FAIL', reason: 'OFF_ORIGIN' };
            else if (!final.ok) outcome = { status: 'FAIL', reason: 'MAX_STEPS' };
            else if (remaining() <= 0) outcome = { status: 'FAIL', reason: 'TIMEOUT' };
            else outcome = { status: 'PASS' };
          }
        } catch (error) {
          assertionResults = [];
          finish('ERROR', maskText(scenario, firstLine(error)));
        }
      } else {
        assertionResults = flow.assertions.map((assertion) => ({
          assertion: describeAssertion(assertion),
          ok: false,
          actual: 'not evaluated (page outside baseUrl origin)',
        }));
      }
    }
  } finally {
    context.off('page', onNewPage);
    await guard.dispose();
  }
  // `actual` pochodzi ze strony (adres, wartość pola) — maskowanie jak dla stanu wysyłanego do modelu.
  assertionResults = assertionResults.map((item, index) => {
    if (item.actual === undefined) return item;
    const isUrl = flow.assertions[index]?.url !== undefined;
    return { ...item, actual: isUrl ? maskUrl(scenario, item.actual) : maskText(scenario, item.actual) };
  });

  const screenshot = path.join(outDir, `flow-${flow.name}-final.png`);
  const snapshot = path.join(outDir, `flow-${flow.name}-final.json`);
  const artifactErrors = [];
  let screenshotPath = null;
  let snapshotPath = null;
  let finalUrl = null;
  try {
    finalUrl = maskUrl(scenario, page.url());
  } catch {
    // ignoruj
  }
  try {
    await page.screenshot({ path: screenshot });
    screenshotPath = screenshot;
  } catch (error) {
    warnings.push(`screenshot: ${firstLine(error)}`);
    artifactErrors.push(`screenshot: ${firstLine(error)}`);
  }
  // Migawki nie robimy dla obcej strony (poza originem baseUrl; sprawdzane ponownie po zdjęciu strażnika).
  const snapshotOnOrigin = originOf(page) === baseOrigin;
  const finalState = snapshotOnOrigin
    ? await safeCollect(page, { maxOptions: config.maxOptions, forbidden: config.forbidden, scenario })
    : { error: 'page outside baseUrl origin - snapshot skipped', skipped: true };
  if (finalState.error && !finalState.skipped) {
    // Nie zebrano stanu do migawki: to błąd artefaktu (CLI liczy flow jako nieudany).
    warnings.push(`snapshot state: ${finalState.error}`);
    artifactErrors.push(`snapshot state: ${finalState.error}`);
  }
  // Wadliwy lokator zakazu: fail-closed, status ERROR niezależnie od wcześniejszych asercji.
  if (finalState.code === FORBIDDEN_LOCATOR_INVALID) outcome = { status: 'ERROR', reason: finalState.error };
  try {
    const payload = finalState.error
      ? { error: finalState.error }
      : { summary: finalState.summary, elements: finalState.elements, truncated: finalState.truncated };
    await writeFile(snapshot, JSON.stringify(redactDeep(scenario, payload), null, 2), 'utf8');
    snapshotPath = snapshot;
  } catch (error) {
    warnings.push(`snapshot: ${firstLine(error)}`);
    artifactErrors.push(`snapshot: ${firstLine(error)}`);
  }

  const totals = {
    steps: steps.length,
    jevCalls: policy.totals.jevCalls,
    jevMs: policy.totals.jevMs,
    inputTokens: policy.totals.inputTokens,
    outputTokens: policy.totals.outputTokens,
    durationMs: Date.now() - startedAt,
  };
  const result = {
    name: flow.name,
    status: outcome.status,
    ...(outcome.reason ? { reason: outcome.reason } : {}),
    ...(artifactErrors.length > 0 ? { artifactError: artifactErrors.join('; ') } : {}),
    passedWithoutActions,
    steps,
    totals,
    finalUrl,
    assertions: assertionResults,
    warnings,
    screenshot: screenshotPath,
    snapshot: snapshotPath,
    model: policy.totals.model,
  };
  emit(
    `FLOW ${flow.name} ${outcome.status}${outcome.reason ? ` ${outcome.reason}` : ''} ${steps.length} steps ${seconds(totals.durationMs)}s ` +
      `jev ${seconds(totals.jevMs)}s tokens ${totals.inputTokens + totals.outputTokens}`,
  );
  if (artifactErrors.length > 0) emit(`FLOW ${flow.name} artifact error: ${result.artifactError}`);
  if (outcome.status !== 'PASS') {
    for (const item of assertionResults.filter((entry) => !entry.ok)) emit(`FLOW ${flow.name} assertion FAIL ${item.assertion} actual: ${item.actual ?? '-'}`);
  }
  return result;
}
