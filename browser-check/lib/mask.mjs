// Maskowanie danych wrażliwych w tekstach, które opuszczają proces (stan wysyłany do Jev, stdout, raporty, migawki).
// Dwie klasy: sekrety (wartości podstawione ze zmiennych środowiskowych + klucz API; `source.secrets`) i dane
// osobowe (e-maile, numery telefonów). Moduł jest ogólny — bez wiedzy o aplikacji.

// E-mail, także zakodowany procentowo (`%40` zamiast `@`, `%2B` zamiast `+` w części lokalnej).
const EMAIL_PATTERN = /(?:[\w.+-]|%2B)+(?:@|%40)[\w-]+(?:\.[\w-]+)+/gi;

// „Numer” = grupy cyfr (także w nawiasach) rozdzielone co najwyżej dwoma znakami spacji, kropki lub myślnika,
// z opcjonalnym wiodącym `+`. Maskowany od 9 cyfr (po usunięciu separatorów).
const PHONE_PATTERN = /\+?(?:\(\d+\)|\d+)(?:[\s.-]{0,2}(?:\(\d+\)|\d+))*/g;
const PHONE_MIN_DIGITS = 9;

// Ciągi `%XX` oznaczające drukowalne znaki ASCII (0x20–0x7E).
const PERCENT_PRINTABLE = /%([2-7][0-9a-f])/gi;

const MIN_RAW_LIMIT = 600;
const PLACEHOLDER_ORIGIN = 'http://placeholder.invalid';

/** Dekoduje fragmentami (nie całym tekstem) tylko `%XX` należące do drukowalnego ASCII; reszta zostaje bez zmian. */
function decodePrintable(text) {
  return text.replace(PERCENT_PRINTABLE, (match, hex) => {
    const code = parseInt(hex, 16);
    return code >= 0x20 && code < 0x7f ? String.fromCharCode(code) : match;
  });
}

/** Maskowanie danych osobowych: e-maile → `<email>`, numery (≥ 9 cyfr) → `<phone>`. Najpierw dekoduje `%XX` drukowalnego ASCII. */
export function maskPii(text) {
  return decodePrintable(String(text))
    .replace(EMAIL_PATTERN, '<email>')
    .replace(PHONE_PATTERN, (run) => (run.replace(/\D/g, '').length >= PHONE_MIN_DIGITS ? '<phone>' : run));
}

/** Maskowanie sekretów znanych scenariuszowi (formy: surowa, spłaszczona, `encodeURIComponent`, JSON). `source`: scenariusz albo błąd. */
export function maskSecrets(source, text) {
  let result = String(text);
  for (const secret of source?.secrets ?? []) result = result.split(secret).join('***');
  return result;
}

/** Spłaszcza białe znaki (`\s+` → spacja) i przycina brzegi. */
export function flattenText(text) {
  return String(text ?? '').replace(/\s+/g, ' ').trim();
}

/**
 * Tekst „prywatny”: sekrety zamaskowane na tekście SUROWYM, potem spłaszczenie białych znaków (i drugi przebieg sekretów —
 * dla form spłaszczonych), BEZ maskowania danych osobowych i bez przycinania. Tylko do użytku wewnątrz procesu (odciski,
 * tożsamość elementów) — nigdy do wysłania ani zapisu.
 */
export function secretSafeText(source, text) {
  return maskSecrets(source, flattenText(maskSecrets(source, text)));
}

/**
 * Twardy limit techniczny długości tekstu zwracanego przez przeglądarkę: musi być na tyle duży, by sekret (nawet w formie
 * zakodowanej) zaczynający się w widocznym prefiksie nie został ucięty przed maskowaniem w Node. Długość sekretów
 * nie jest sekretem; same sekrety nie trafiają do przeglądarki.
 */
export function rawLimitFor(source) {
  let longest = 0;
  for (const secret of source?.secrets ?? []) longest = Math.max(longest, secret.length);
  return Math.max(MIN_RAW_LIMIT, 2 * longest + MIN_RAW_LIMIT);
}

/** Sekrety, potem dane osobowe — dla każdego tekstu wysyłanego do modelu lub zapisywanego w raporcie. */
export function maskText(source, text) {
  return maskPii(maskSecrets(source, text));
}

function safeDecode(text) {
  try {
    return decodeURIComponent(text);
  } catch {
    return text;
  }
}

/** Ścieżka: dekodowanie procentowe PO SEGMENCIE (błąd jednego segmentu nie blokuje pozostałych), maskowanie każdego osobno. */
function maskPath(source, pathname) {
  return pathname
    .split('/')
    .map((segment) => maskText(source, safeDecode(segment)))
    .join('/');
}

/** Zapytanie (bez `?`): `URLSearchParams` (formularzowy `+` = spacja), nazwa i wartość maskowane osobno. */
function maskQuery(source, query) {
  return query
    .split('&')
    .filter((part) => part !== '')
    .map((part) => {
      const [name, value] = [...new URLSearchParams(part)][0] ?? ['', ''];
      return part.includes('=') ? `${maskText(source, name)}=${maskText(source, value)}` : maskText(source, name);
    })
    .join('&');
}

/** Hash: jak ścieżka; fragment po pierwszym `?` (trasa SPA z parametrami) jak zapytanie. */
function maskHash(source, hash) {
  const split = hash.indexOf('?');
  if (split === -1) return maskPath(source, hash);
  return `${maskPath(source, hash.slice(0, split))}?${maskQuery(source, hash.slice(split + 1))}`;
}

/**
 * Adres: sekrety (formy surowa/zakodowana) w całym tekście, potem rozbiór `new URL` (względny adres — względem
 * zastępczego originu, który nie trafia do wyniku), dekodowanie po segmentach i maskowanie PII osobno dla ścieżki,
 * każdej nazwy i wartości zapytania oraz hasha. Wynik jest tekstem do raportu (zdekodowanym), nie adresem do nawigacji.
 * Gdy adresu nie da się rozebrać — całość jako tekst.
 */
export function maskUrl(source, url) {
  const text = maskSecrets(source, url);
  try {
    const absolute = /^[a-z][a-z0-9+.-]*:/i.test(text);
    const parsed = absolute ? new URL(text) : new URL(text, PLACEHOLDER_ORIGIN);
    let prefix = '';
    if (absolute) {
      if (parsed.origin === 'null') throw new Error('non-hierarchical URL');
      prefix = parsed.origin;
    } else if (parsed.origin !== PLACEHOLDER_ORIGIN) {
      prefix = `//${parsed.host}`; // adres protokołowo-względny (//host/ścieżka)
    }
    const onlyQueryOrHash = !absolute && /^[?#]/.test(text);
    const pathname = onlyQueryOrHash ? '' : maskPath(source, parsed.pathname);
    const query = parsed.search.length > 1 ? `?${maskQuery(source, parsed.search.slice(1))}` : '';
    const hash = parsed.hash.length > 1 ? `#${maskHash(source, parsed.hash.slice(1))}` : '';
    return `${prefix}${pathname}${query}${hash}`;
  } catch {
    return maskText(source, safeDecode(text));
  }
}

/** Przycięcie do `max` znaków (z wielokropkiem) — wywoływane PO maskowaniu. */
export function clipText(text, max) {
  const value = flattenText(text);
  return value.length > max ? `${value.slice(0, max - 1)}…` : value;
}

/**
 * Maskuje, potem przycina — jedyna poprawna kolejność dla tekstów ze strony: sekrety na tekście surowym, spłaszczenie,
 * (sekrety w formie spłaszczonej), dane osobowe, przycięcie.
 */
export function safeText(source, text, max) {
  return clipText(maskPii(secretSafeText(source, text)), max);
}
