// Polityka decyzyjna oparta na modelu Jev (SDK @typesafe-ai/sdk): wybór kolejnej akcji w dwóch etapach.
// Model nie generuje tekstu i nie widzi obrazów — odpowiada wyłącznie wyborem jednej z podanych etykiet.
import { TypeSafeClient, choice } from '@typesafe-ai/sdk';

const MAX_HISTORY = 8;
const MAX_SELECT_OPTIONS = 50;
const CLIENT_TIMEOUT_MS = 30000;

/** Instrukcja etapu 1 (ostateczne brzmienie; opisana też w FLOWS.md). */
export const ACTION_INSTRUCTIONS =
  'You operate a web application to reach the goal. Choose the single next action that best moves toward the goal. ' +
  'Use the history: do not repeat an action that already succeeded unless the page changed. ' +
  'If an earlier action opened a menu or a panel and its items are now listed, choose among those items instead of opening it again. ' +
  'Fill empty or incorrect fields before pressing a submit button. ' +
  "Choose 'none' if no listed action helps.";

export function valueInstructions(fieldDescription) {
  return `Which test data value should be typed into the field ${fieldDescription} to progress toward the goal?`;
}

/** Opis kryterium etapu 2 dla jednej wartości danych testowych. */
export function valueCriterion(key, value) {
  return `Type the value "${value}" (test data "${key}")`;
}

export function optionInstructions(fieldDescription) {
  return `Which option should be selected in ${fieldDescription} to progress toward the goal?`;
}

function sanitize(message) {
  let text = String(message ?? '').split('\n')[0];
  const key = process.env.TYPESAFE_API_KEY;
  if (key) text = text.split(key).join('***');
  return text.slice(0, 300);
}

function topThree(probabilities) {
  return Object.entries(probabilities ?? {})
    .sort((a, b) => b[1] - a[1])
    .slice(0, 3)
    .map(([label, p]) => ({ label, p: Math.round(p * 1000) / 1000 }));
}

/** Jeden klient na przebieg przejścia. `decide` zwraca { status: 'OK' | 'NEED_FALLBACK' | 'ERROR', ... }. */
export function createJevPolicy({ model, confidenceThreshold }) {
  const client = new TypeSafeClient({ timeout: CLIENT_TIMEOUT_MS });
  const totals = { jevCalls: 0, jevMs: 0, inputTokens: 0, outputTokens: 0, model };

  async function ask(state, instructions, criteria, remainingMs) {
    const startedAt = Date.now();
    // Czas na wywołanie = min(30 s, pozostały czas przejścia); sygnał ogranicza też ponowienia SDK.
    const budget = Math.max(1, Math.min(CLIENT_TIMEOUT_MS, remainingMs()));
    const response = await client.systemOne(
      { state, questions: { next: choice(instructions, criteria) }, model },
      { timeout: budget, signal: AbortSignal.timeout(budget) },
    );
    const ms = Date.now() - startedAt;
    totals.jevCalls++;
    totals.jevMs += ms;
    totals.inputTokens += response.usage?.input_tokens ?? 0;
    totals.outputTokens += response.usage?.output_tokens ?? 0;
    if (response.model) totals.model = response.model;
    const answer = response.answers.next;
    return { choice: answer.choice, confidence: answer.confidence, top3: topThree(answer.probabilities), ms };
  }

  /**
   * input: { goal, subgoals, testData, summary, history, actions, elements, remainingMs }.
   * `remainingMs()` zwraca pozostały czas przejścia (limit wywołania Jev = min(30 s, ten czas)).
   * Wynik OK: { action, value?, valueKey?, optionLabel?, optionIndex?, confidence, top3, stage2?, jevMs }.
   * Opcje natywnego `select` trafiają do modelu jako etykiety `o1…oN` z zamaskowanymi opisami; wybór wraca jako
   * indeks oryginalnej opcji (`optionIndex`), a `optionLabel` to zamaskowany opis (do historii).
   */
  async function decide({ goal, subgoals, testData, summary, history, actions, elements, remainingMs = () => CLIENT_TIMEOUT_MS }) {
    const meta = { jevMs: 0 };
    try {
      const state = {
        goal,
        ...(subgoals && subgoals.length > 0 ? { subgoals } : {}),
        ...(testData && Object.keys(testData).length > 0 ? { testData } : {}),
        page: summary,
        history: history.slice(-MAX_HISTORY),
      };
      const first = await ask(state, ACTION_INSTRUCTIONS, actions, remainingMs);
      meta.jevMs += first.ms;
      Object.assign(meta, { action: first.choice, confidence: first.confidence, top3: first.top3 });

      if (first.choice === 'none') return { status: 'NEED_FALLBACK', reason: 'NONE_CHOSEN', ...meta };
      if (first.confidence < confidenceThreshold) return { status: 'NEED_FALLBACK', reason: 'LOW_CONFIDENCE', ...meta };

      const [verb, elementId] = first.choice.split(':');
      if (verb !== 'fill' && verb !== 'select') return { status: 'OK', ...meta };
      const element = elements.find((candidate) => candidate.id === elementId);
      const description = actions[first.choice].replace(/^(Type into|Choose an option in) /, '').replace(/ \(current: .*\)$/, '');
      const stateTwo = {
        goal,
        ...(subgoals && subgoals.length > 0 ? { subgoals } : {}),
        field: { description, current: element?.value ?? '' },
        ...(verb === 'fill' ? { testData } : {}),
        page: { url: summary.url, overlay: summary.overlay },
        history: history.slice(-MAX_HISTORY),
      };

      let second;
      if (verb === 'fill') {
        const criteria = {};
        for (const [key, value] of Object.entries(testData ?? {})) criteria[key] = valueCriterion(key, value);
        criteria.none = 'None of these values belongs in this field';
        second = await ask(stateTwo, valueInstructions(description), criteria, remainingMs);
      } else {
        const labels = (element?.options ?? []).slice(0, MAX_SELECT_OPTIONS);
        const indexes = (element?.optionIndexes ?? []).slice(0, MAX_SELECT_OPTIONS);
        if (labels.length === 0 || indexes.length !== labels.length) return { status: 'NEED_FALLBACK', reason: 'NO_OPTIONS', ...meta };
        const criteria = {};
        labels.forEach((label, position) => {
          criteria[`o${position + 1}`] = label;
        });
        second = await ask(stateTwo, optionInstructions(description), criteria, remainingMs);
      }
      meta.jevMs += second.ms;
      meta.stage2 = { choice: second.choice, confidence: second.confidence };

      if (verb === 'fill') {
        if (second.choice === 'none') return { status: 'NEED_FALLBACK', reason: 'NO_TEST_DATA_MATCH', ...meta };
        if (second.confidence < confidenceThreshold) return { status: 'NEED_FALLBACK', reason: 'LOW_CONFIDENCE', ...meta };
        return { status: 'OK', valueKey: second.choice, value: testData[second.choice], ...meta };
      }
      if (second.confidence < confidenceThreshold) return { status: 'NEED_FALLBACK', reason: 'LOW_CONFIDENCE', ...meta };
      const position = Number(/^o(\d+)$/.exec(second.choice)?.[1]) - 1;
      const labels = element?.options ?? [];
      if (!Number.isInteger(position) || position < 0 || position >= labels.length) {
        return { status: 'ERROR', error: 'Jev API: unexpected option label', ...meta };
      }
      return { status: 'OK', optionLabel: labels[position], optionIndex: element.optionIndexes[position], ...meta };
    } catch (error) {
      return { status: 'ERROR', error: `Jev API: ${sanitize(error?.message ?? error)}`, ...meta };
    }
  }

  return { decide, totals };
}
