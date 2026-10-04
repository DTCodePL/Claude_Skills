// Tłumaczenie opisu elementu (target) na Locator Playwrighta.
// Wolno podać dokładnie jedną z form; dodatkowe klucze są dozwolone tylko tam, gdzie wymienione.

const FORMS = {
  role: ['name', 'exact'],
  label: ['exact'],
  text: ['exact'],
  placeholder: [],
  testId: [],
  css: [],
};

/** Sprawdza kształt targetu; rzuca Error z opisem. */
export function validateTarget(target) {
  if (target === null || typeof target !== 'object' || Array.isArray(target)) {
    throw new Error('target musi być obiektem');
  }
  const present = Object.keys(FORMS).filter((key) => target[key] !== undefined);
  if (present.length !== 1) {
    throw new Error(
      `target musi mieć dokładnie jedną z form (${Object.keys(FORMS).join(', ')}); podano: ${present.join(', ') || 'żadnej'}`,
    );
  }
  const form = present[0];
  if (typeof target[form] !== 'string' || target[form] === '') {
    throw new Error(`target.${form} musi być niepustym łańcuchem`);
  }
  const allowed = new Set([form, ...FORMS[form]]);
  for (const key of Object.keys(target)) {
    if (!allowed.has(key)) throw new Error(`target.${key} nie jest dozwolone w formie "${form}"`);
  }
  if (target.name !== undefined && (typeof target.name !== 'string' || target.name === '')) {
    throw new Error('target.name musi być niepustym łańcuchem');
  }
  if (target.exact !== undefined && typeof target.exact !== 'boolean') throw new Error('target.exact musi być true/false');
}

/** scope: Page albo Locator. Zwraca Locator (bez .first()). */
export function toLocator(scope, target) {
  validateTarget(target);
  const exact = target.exact ?? false;
  if (target.role !== undefined) {
    const options = { exact };
    if (target.name !== undefined) options.name = target.name;
    return scope.getByRole(target.role, options);
  }
  if (target.label !== undefined) return scope.getByLabel(target.label, { exact });
  if (target.text !== undefined) return scope.getByText(target.text, { exact });
  if (target.placeholder !== undefined) return scope.getByPlaceholder(target.placeholder);
  if (target.testId !== undefined) return scope.getByTestId(target.testId);
  return scope.locator(target.css);
}

/** Krótki opis do raportów, np. `role=button name="Zapisz"`. */
export function describeTarget(target) {
  if (target === null || typeof target !== 'object') return String(target);
  if (target.role !== undefined) {
    return `role=${target.role}` + (target.name !== undefined ? ` name="${target.name}"` : '') + (target.exact ? ' exact' : '');
  }
  if (target.label !== undefined) return `label="${target.label}"` + (target.exact ? ' exact' : '');
  if (target.text !== undefined) return `text="${target.text}"` + (target.exact ? ' exact' : '');
  if (target.placeholder !== undefined) return `placeholder="${target.placeholder}"`;
  if (target.testId !== undefined) return `testId=${target.testId}`;
  if (target.css !== undefined) return `css=${target.css}`;
  return JSON.stringify(target);
}
