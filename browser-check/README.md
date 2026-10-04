# browser-check

Małe narzędzie Node (ESM, bez kroku budowania) do szybkiego, deterministycznego sprawdzenia lokalnie
uruchomionej aplikacji webowej po implementacji. Tryb **matrix** robi macierz zrzutów ekranu
(rozmiary okna × motyw Light/Dark) dla listy tras i raportuje błędy konsoli oraz sieci.
Tryb **flows** (pętla Playwright + model decyzyjny Jev) to osobny moduł `lib/flows.mjs` — opis w [FLOWS.md](FLOWS.md).

## Uruchomienie

```powershell
cd D:\projects\DTCode\Claude_Skills\browser-check
$env:BC_LOGIN = 'wlasciciel.demo@zebrani.pl'; $env:BC_PASSWORD = '...'
node browser-check.mjs examples/zebrani-panel.json
```

```
node browser-check.mjs <scenario.json> [--out <dir>] [--only matrix|flows] [--headed] [--keep-auth]
```

| Opcja         | Znaczenie                                                                                     |
| ------------- | --------------------------------------------------------------------------------------------- |
| `--out <dir>` | Katalog wyników. Domyślnie `<katalog narzędzia>\out\<RRRRMMDD-HHMMSS-mmm>-<4 znaki hex>` (czas lokalny, unikalny). Pusta wartość, istniejący plik albo katalog z `report.json` to błąd użycia (kod 2). |
| `--only`      | `matrix` albo `flows` — uruchamia tylko wskazany tryb.                                        |
| `--headed`    | Tylko włącza tryb z oknem (nie ma odwrotności; bez flagi decyduje `browser.headless`).        |
| `--keep-auth` | Zostawia `<out>\.auth\storage-state.json` (domyślnie usuwany po przebiegu).                   |

Wymagania: Node 26, `playwright` (zależność z `package.json`) i zainstalowany Google Chrome
(`browser.channel: "chrome"`). Narzędzie **nie pobiera** przeglądarek.

### Kody wyjścia

- `0` — wszystko w porządku.
- `1` — błąd któregokolwiek zrzutu, nieudane logowanie, przejście (flow) ze statusem innym niż `PASS` albo z błędem
  artefaktu (`artifactError` — nieudany zrzut końcowy),
  przekroczenie `timeoutMs` (`aborted: "TIMEOUT"`), nieudany start przeglądarki albo nieudany zapis
  `report.json` (komunikat na stderr).
- `2` — błąd użycia lub scenariusza (brak pliku, zły JSON, błąd walidacji, brakująca zmienna środowiskowa,
  nieprawidłowe `--out`, błąd z `validateFlows`, nieutworzony katalog wyników).
- `130` / `143` — przerwanie sygnałem `SIGINT` / `SIGTERM` (plik stanu sesji jest wtedy usuwany, chyba że `--keep-auth`).

Kod wyjścia ustawiany jest przez `process.exitCode` (proces kończy się naturalnie), więc ostatnia linia
`RESULT …` nie ginie przy przekierowaniu stdout.

### Wyjście na stdout

Jedna linia na zrzut, np.:

```
SHOT ok   programy mobile/light 1.4s  out\...\programy__mobile__light.png  console:2 net:0
SHOT ok   programy desktop/light 1.3s  out\...\programy__desktop__light.png  console:1 net:1  REDIRECT -> /logowanie
SHOT FAIL sprzedawcy mobile/dark 5.6s  out\...\sprzedawcy__mobile__dark.png  console:0 net:0  <komunikat>
```

`console:N` to błędy konsoli, `net:N` — nieudane żądania; opcjonalnie `pageerr:`, `dialogs:`, `warn:`.
Na końcu: `RESULT ok|fail  shots 11/12  flows 0/0  report: <ścieżka>`.

## Scenariusz (JSON)

Każdy łańcuch może zawierać `${env:NAZWA}` — podstawiana jest wartość `process.env.NAZWA`; brak zmiennej
(lub pusta) to błąd scenariusza z samą nazwą zmiennej. **Haseł nie wpisuje się do plików scenariuszy.**
Podstawiona wartość krótsza niż 4 znaki to błąd scenariusza (kod 2: „za krótka do bezpiecznego maskowania”). Podstawione
wartości oraz `TYPESAFE_API_KEY` (jeśli ustawiony) są maskowane (`***`) w stdout, w raporcie, w komunikatach błędów
scenariusza i w stanie wysyłanym do modelu, także w formie `encodeURIComponent`, w formie zapisanej w JSON-ie i — gdy
różni się od surowej — w formie ze spłaszczonymi białymi znakami (`\s+` → spacja, bez brzegów; tekst ze strony bywa zwinięty).
`${env:…}` działa **wyłącznie w polach tekstowych** — liczby i wartości logiczne (`timeoutMs`, `width`,
`headless`, `fullPage` …) podaje się literalnie.

```json
{
  "baseUrl": "http://localhost:4300",
  "timeoutMs": 600000,
  "settleMs": 400,
  "browser": { "channel": "chrome", "headless": true },
  "login": {
    "url": "/logowanie",
    "fields": [
      { "label": "E-mail lub numer telefonu", "value": "${env:BC_LOGIN}" },
      { "target": { "label": "Hasło" }, "value": "${env:BC_PASSWORD}" }
    ],
    "submit": { "role": "button", "name": "Zaloguj się" },
    "successUrl": "**/panel/**",
    "viewport": "desktop"
  },
  "theme": {
    "toggle": { "role": "button", "name": "Przełącz motyw" },
    "toggleByViewport": { "mobile": [ { "role": "button", "name": "Menu użytkownika" }, { "role": "switch", "name": "Ciemny motyw" } ] },
    "darkClass": "app-dark",
    "settleMs": 900
  },
  "viewports": [ { "name": "mobile", "width": 360, "height": 530 }, { "name": "desktop", "width": 1280, "height": 720 } ],
  "themes": ["light", "dark"],
  "matrix": [
    { "name": "programy", "path": "/panel/programy", "waitFor": { "role": "heading", "name": "Programy", "exact": true },
      "fullPage": false, "timeoutMs": 15000, "steps": [] }
  ],
  "flows": []
}
```

Wartości domyślne: jak powyżej (`login.url`, `login.successUrl`, `login.viewport`, `theme.darkClass`,
`theme.settleMs`, `viewports`, `themes`, `timeoutMs`, `settleMs`, `browser`, `fullPage: false`, `steps: []`).

- **Wymagane:** `baseUrl`; gdy `matrix` niepuste — każda pozycja ma unikalne `name` (`[a-z0-9-]+`)
  i `path`. `login` jest opcjonalne (bez niego kontekst jest niezalogowany) — gdy jest, wykonuje się
  także przy `--only flows`. `theme` jest opcjonalne, ale wymagane, gdy `themes` zawiera `dark`.
- **Adresy:** `baseUrl` to wyłącznie `http(s)://host[:port]` bez ścieżki, zapytania i danych logowania
  (dopuszczalny końcowy `/`). `login.url`, `matrix[].path` i `flows[].startPath` zaczynają się od dokładnie
  jednego `/` (nie `//`), bez `\`, bez znaków sterujących (`U+0000–U+001F`, `U+007F`) i schematu. Każdy URL powstaje jako
  `new URL(path, baseUrl)` i musi zostać w originie `baseUrl` (inaczej błąd scenariusza).
- **Nazwy** viewportów, tras (`matrix[].name`) i przejść (`flows[].name`): `[a-z0-9-]+`, unikalne.
- **Ścisłe klucze:** nieznany klucz na najwyższym poziomie oraz w `browser`, `login`, `login.fields[]`,
  `theme`, `viewports[]`, `matrix[]` i `matrix[].steps[]` to błąd (np. `matrix[0].fulPage: nieznany klucz`).
  Wyjątki: `flows` i `flowDefaults` — ich klucze sprawdza moduł flows (patrz niżej).
- `timeoutMs` (scenariusza i trasy) ≤ 2147483647.
- `login.fields[]`: `label` (skrót dla `target: { label }`) albo `target`, plus `value`.
- `theme.toggle` — jeden target albo lista targetów klikanych po kolei. `theme.toggleByViewport`
  (opcjonalne) nadpisuje go dla viewportu o danej nazwie — potrzebne, gdy przełącznik motywu na małym
  ekranie jest schowany w menu (w Zebrani na `mobile` to przełącznik „Ciemny motyw” w arkuszu
  „Menu użytkownika”).
- `flows` — tablica obiektów; CLI waliduje tylko pola nawigacji startowej: `name`, `startPath`, opcjonalne
  `viewport` (musi istnieć; bez pola — musi istnieć viewport `desktop`), `theme` (`light`|`dark`; `dark`
  wymaga sekcji `theme`), `waitFor` (Target) i `timeoutMs`. Resztę pól waliduje moduł flows (`validateFlows`).
- `flowDefaults` — obiekt wartości domyślnych dla wszystkich flows; obsługiwane klucze: `maxSteps`, `confidenceThreshold`,
  `maxOptions`, `forbidden`, `model` (znaczenie i zakresy jak w polach flow — [FLOWS.md](FLOWS.md); `forbidden` sumuje się
  z `forbidden` flow). Nieznany klucz albo wartość spoza zakresu to błąd (kod 2). `validateFlows` sprawdza `flowDefaults`
  i flows przed uruchomieniem przeglądarki, gdy `flows` jest niepuste, a `--only` ≠ `matrix`.

### Target (opis elementu)

Dokładnie jedna z form: `{ "role": "...", "name": "...", "exact": true|false }` (`name` niepusty), `{ "label" }`, `{ "text" }`
(oba z opcjonalnym `exact`), `{ "placeholder" }`, `{ "testId" }`, `{ "css" }`. `exact` domyślnie `false`.
Inna forma albo kilka naraz — błąd. W krokach i czekaniach używany jest zawsze `.first()`.

### Kroki trasy (`steps[]`)

`{ "action": "click|fill|press|wait", "target": Target, "value": "...", "ms": 500, "optional": false }`

- `click` — klik w `target`; `fill` — wpisanie `value` w `target`; `press` — klawisz `value` (np. `Escape`)
  wciśnięty na `target` (z `target`) albo na stronie (bez `target`); `wait` — z `target`: czekanie na
  widoczność, bez `target`: pauza `ms` (`target` i `ms` naraz to błąd walidacji).
- Limit czasu kroków `click`, `fill`, `press` (z `target`) i `wait` (z `target`) to `matrix[].timeoutMs`,
  a gdy go brak — 5000 ms.
- Po każdym kroku pauza `settleMs`. Błąd kroku `optional: true` trafia do `warnings`; błąd kroku bez
  `optional` oznacza zrzut `ok: false` (zrzut stanu i tak powstaje jako dowód).

## Jak narzędzie ustawia stan strony

- **Logowanie** odbywa się raz, w osobnym kontekście; zapisywane są wyłącznie ciasteczka
  (`<out>\.auth\storage-state.json`, usuwany w `finally`). Następne konteksty startują z tych ciasteczek.
  **Refresh token jest jednorazowy** (rotowany przy każdym odtworzeniu sesji), dlatego plik stanu jest
  odświeżany przed zamknięciem każdego kontekstu (`persistSession()`); bez tego drugi viewport byłby
  wylogowany. W stanie nie ma `localStorage`, więc motyw wybrany w jednym kontekście nie przecieka dalej.
- **Motyw ciemny** ustawiany jest wyłącznie kliknięciem przełącznika, odczekaniem `theme.settleMs`
  i **przeładowaniem strony**; dopiero potem powstaje zrzut. Przełącznik wybierany jest po **nazwie**
  viewportu (`toggleByViewport[<nazwa>]`, w przeciwnym razie `theme.toggle`), nie po rozmiarze okna. Dowód motywu (bez oglądania obrazu):
  `themeEvidence.darkClass` i `themeEvidence.bodyBackground` w raporcie.
- **Dialogi** (np. `beforeunload`) są akceptowane automatycznie i odnotowane w `dialogs`.
- **Przekierowanie** (np. do logowania przy braku sesji) nie jest błędem: `redirected: true`,
  linia `REDIRECT -> <pathname>`. Liczone tylko po udanej nawigacji (`goto` + `waitForReady`); przy błędzie
  nawigacji `redirected: false`.
- **Plik sesji** (`<out>\.auth\storage-state.json`): katalog `.auth` z trybem `0700`, plik `0600` (na Windows
  bity są w dużej mierze ignorowane). `SIGINT`/`SIGTERM` usuwają plik synchronicznie (chyba że `--keep-auth`)
  i kończą proces kodem 130/143.

## Raport (`<out>\report.json`)

```json
{ "startedAt": "...", "finishedAt": "...", "durationMs": 0, "baseUrl": "...", "ok": true, "aborted": null,
  "login": { "ok": true, "durationMs": 0, "error": null, "screenshot": null },
  "matrix": [ /* Shot */ ], "flows": [], "flowsSkipped": false }
```

- `ok` = logowanie ok (lub brak) ∧ każdy zrzut `ok` ∧ każdy flow `PASS` ∧ brak przerwania.
- `aborted`: `null`, `"TIMEOUT"`, `"BROWSER_LAUNCH_FAILED"` albo `"ERROR"` (z `error`).
- `login` jest `null`, gdy scenariusz nie ma sekcji `login`.
- `flowsSkipped: true`, gdy scenariusz ma `flows`, a `lib/flows.mjs` nie istnieje (to nie błąd). Istniejący,
  ale wadliwy moduł (błąd importu, brak `runFlow`) jest błędem — komunikat na stderr, kod 1.
- Shot: `{ route, path, viewport, theme, ok, file, href, redirected, durationMs, themeEvidence: { darkClass,
  bodyBackground }, consoleErrors, pageErrors, failedRequests: [{ url, status }], dialogs, warnings, error? }`.
  Plik zrzutu: `<out>\<route>__<viewport>__<theme>.png`.
- Błędy sieci liczone są tylko dla tego samego originu co `baseUrl`; `status: 0` oznacza `requestfailed`.
  Błędy konsoli i `pageerror` nie są filtrowane po originie. Zdarzenia zebrane między zrzutami
  (spóźnione odpowiedzi poprzedniej strony) są odrzucane przed rozpoczęciem nowego zrzutu.
- Raport nie zawiera wartości pól logowania ani podstawionych zmiennych środowiskowych. Wartości tekstowe obiektu raportu są
  redagowane rekurencyjnie PRZED `JSON.stringify` (plik zawsze jest poprawnym JSON-em). Kanały diagnostyczne są maskowane
  u źródła (sekrety **i** dane osobowe: e-maile, numery): `consoleErrors` i `pageErrors` najpierw maskowane, potem
  skracane do 300 znaków, `failedRequests[].url` przez `maskUrl` (adres rozebrany `new URL`; ścieżka, hash, nazwy i
  wartości zapytania dekodowane i maskowane osobno — wynik jest zdekodowanym tekstem do raportu, nie adresem do
  nawigacji), błąd logowania (`login.error`) jak tekst, a jego adres przez `maskUrl`. Żądania przerwane przez nawigację
  (`ERR_ABORTED`) nie trafiają do `failedRequests`. W trybie matrix tak samo: `href` zrzutu przez `maskUrl`, `warnings`
  i `error` przez maskowanie sekretów i danych osobowych (flaga `redirected` liczona wcześniej, z surowego adresu).

## Ograniczenia

- Tylko Chrome (kanał `chrome`); brak pobierania przeglądarek.
- Zrzuty to dowód wizualny — ocenia je człowiek/architekt; narzędzie sprawdza tylko wymiary okna,
  dowód motywu, adres końcowy i błędy konsoli/sieci. Kontrastu WCAG nie mierzy.
- Trasy `/panel/**` są renderowane na serwerze i hydratowane; `settleMs`/`waitFor` mają dać
  hydratacji czas, ale wolne środowisko może wymagać większych wartości.
- Logowanie: pięć nieudanych prób blokuje konto demo — narzędzie powtarza próbę najwyżej raz, i tylko
  gdy po pierwszej nie było widocznego `[role="alert"]`. Do testu negatywnego używaj nieistniejącego konta.
- Jedna karta na kontekst; narzędzie nie uruchamia nic równolegle w jednym kontekście.
- Globalny limit czasu `timeoutMs` zamyka przeglądarkę, więc w toku zrzut kończy się błędem
  `... has been closed`; raport z dotychczasowymi wynikami jest zapisywany.

## Tryb flows

Przejścia (flows) wykonuje osobny moduł `lib/flows.mjs`; jego opis i format scenariuszy — [FLOWS.md](FLOWS.md).

Kontrakt CLI ↔ moduł:

- `validateFlows(scenario)` (opcjonalny, może być asynchroniczny) — wołany po wczytaniu scenariusza, **przed**
  uruchomieniem przeglądarki i logowaniem, gdy `flows` jest niepuste, a `--only` ≠ `matrix`. Rzucony
  `ScenarioError` (z `lib/scenario.mjs`) kończy przebieg kodem 2 (komunikat na stderr, po maskowaniu sekretów).
- `runFlow({ page, flow, scenario, outDir, log, collector })` → obiekt wyniku z `name` i `status`
  (`PASS` liczy się jako sukces). `page` jest już na `flow.startPath`, gotowa (`waitFor`) i w motywie `flow.theme`.
- `collector.drain()` → `{ consoleErrors, pageErrors, failedRequests, dialogs }` i czyści bufor. CLI woła
  `drain()` tuż przed `runFlow` (zdarzenia z nawigacji harnessu są odrzucane) i zaraz po nim; niepuste
  `consoleErrors` / `pageErrors` / `failedRequests` z drugiego wywołania są dopisywane do wyniku flow.
