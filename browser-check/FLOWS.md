# Tryb flows

Przejście funkcjonalne opisujesz **celem w języku naturalnym**, **danymi testowymi** i **deterministycznymi asercjami**.
Pętla Playwright + model **Jev** (`@typesafe-ai/sdk`) sama znajduje drogę w UI. **Jev niczego nie ocenia** — wynik
rozstrzygają wyłącznie asercje Playwrighta. Silnik jest ogólny: nie zna żadnej aplikacji, ekranu ani tekstu.

Uruchomienie (tylko przejścia, bez macierzy zrzutów):

```powershell
cd D:\projects\DTCode\Claude_Skills\browser-check
$env:TYPESAFE_API_KEY = [Environment]::GetEnvironmentVariable('TYPESAFE_API_KEY','User')
$env:BC_LOGIN = 'wlasciciel.demo@zebrani.pl'; $env:BC_PASSWORD = '...'
node browser-check.mjs examples/zebrani-flows.json --only flows
```

Klucz `TYPESAFE_API_KEY` jest wymagany (brak = błąd scenariusza, kod 2, przed startem przeglądarki). Nigdy nie trafia do
logu, raportu ani stanu wysyłanego do modelu (komunikaty błędów SDK są czyszczone z klucza, a klucz jest dopisywany do
sekretów maskowanych we wszystkich tekstach).

## Format

Obiekt w `flows[]` (pola nawigacji startowej waliduje CLI, resztę `validateFlows`):

| Pole | Typ | Opis |
| --- | --- | --- |
| `name`, `startPath`, `viewport`, `theme`, `waitFor`, `timeoutMs` | — | jak w README (harness: nawigacja, gotowość, motyw). `timeoutMs` to też limit czasu całego przejścia (domyślnie 120000). |
| `goal` | string | **wymagane**, niepusty. Cel w języku naturalnym. |
| `subgoals` | string[] | opcjonalne, wskazówki kolejnych kroków. |
| `testData` | obiekt string → string | opcjonalne. Wartości wolno wpisywać w pola. Klucz `none` jest zarezerwowany. Bez `testData` model nie dostaje akcji `fill`. |
| `assertions` | Assertion[] | **wymagane**, niepuste. Wszystkie muszą być spełnione. |
| `maxSteps` | int 1–50 | domyślnie 20. |
| `confidenceThreshold` | 0–1 | domyślnie 0,75. |
| `maxOptions` | int 5–200 | domyślnie 80. |
| `forbidden` | Target[] | elementy, których pętla nigdy nie wybierze. |
| `model` | string | domyślnie `jev-latest`. |

`scenario.flowDefaults` może zawierać wyłącznie `maxSteps`, `confidenceThreshold`, `maxOptions`, `forbidden`, `model`
(sprawdza je `validateFlows`, gdy `flows` jest niepuste i `--only` ≠ `matrix`). Wartość z flow wygrywa, a `forbidden` się
**sumuje**. Nieznany klucz we flow lub w `flowDefaults` to błąd (z pełną ścieżką pola; wszystkie problemy naraz).

**Zakazy (`forbidden`).** Kandydat jest wykluczany, gdy **sam albo którykolwiek jego przodek** pasuje do celu zakazu
(zakaz na kontenerze zamyka też jego potomków), a także gdy pasujący element leży wewnątrz niego (najbliższy kandydat-przodek).
Tuż przed wykonaniem akcji zakazy są sprawdzane ponownie na żywym elemencie. **Błąd lokatora zakazu** (np. niepoprawny
CSS) kończy przejście `ERROR` / `FORBIDDEN_LOCATOR_INVALID` — nigdy cichym zdjęciem zakazu. Składni `css` nie da się sprawdzić
statycznie bez przeglądarki, więc `validateFlows` tego nie robi; kontrola odbywa się w czasie wykonania.

Przełączniki motywu ze scenariusza (`theme.toggle`, `theme.toggleByViewport`) są zawsze wyłączone z akcji — CLI ustawia
motyw sam. Z listy kliknięć wyłączany jest tylko **ostatni** cel (ten, który przełącza motyw); wcześniejsze (np. „Menu
użytkownika”) to otwieracze menu i zostają dostępne.

### Asercje

Dokładnie jedna forma na obiekt:

```json
{ "target": { "role": "heading", "name": "Ustawienia", "exact": true }, "state": "visible", "hasText": "…", "within": { "role": "dialog", "name": "Dodaj" } }
{ "url": "**/panel/ustawienia/konto" }
{ "target": { "label": "Telefon", "exact": true }, "value": "509123456", "match": "digits", "prefix": "48", "within": { "role": "dialog" } }
```

- `state`: `visible` (jakiś pasujący element widoczny) albo `hidden` (**żaden** pasujący element nie jest widoczny — sprawdzane
  są wszystkie dopasowania, bez limitu); `hasText` (opcjonalne) to filtr lokatora.
- `within` (opcjonalne, tylko z `target`): `Target` zakresu. Lokator `target` jest szukany **wewnątrz pierwszego widocznego**
  dopasowania zakresu; brak widocznego zakresu = asercja niespełniona (`actual: "scope not visible"`), także dla `hidden`.
  Walidowany jak `target`.
- `value`: czyta wyłącznie **widoczne** dopasowania. 0 widocznych → niespełniona (`no visible element`); więcej niż 1 →
  niespełniona (`ambiguous (N visible)`); dokładnie 1 → wartość pola (`value`) albo tekst elementu. `match: "exact"`
  (domyślnie) = równość. `match: "digits"`: cyfry wartości rzeczywistej muszą być **równe** cyfrom oczekiwanej albo równe
  `<prefix><oczekiwane>`, gdzie `prefix` (opcjonalne, tylko z `match: "digits"`, same cyfry, np. `"48"`) to prefiks dodawany
  przez maskę pola. Żaden inny prefiks nie przechodzi.
- `url`: glob dopasowywany do **`pathname`** adresu (bez zapytania i hasha); gdy glob zawiera `?`, do `pathname + search`.
  `**` = dowolny ciąg, `*` = dowolny ciąg bez `/`, reszta dosłownie. Origin pilnuje pętla (`OFF_ORIGIN`), nie asercja.
- **Koniunkcja:** wszystkie asercje muszą być spełnione **naraz**. Przed każdą decyzją zestaw jest sprawdzany jednym
  przebiegiem, bez czekania. Na końcu (po `maxSteps`) cały zestaw jest ponawiany co ~200 ms do 5 s (nie dłużej niż termin
  przejścia). W obu trybach sukces wymaga przebiegu, w którym spełnione są wszystkie asercje, i potwierdzającego go
  przebiegu bezpośrednio po nim (przebieg sprawdza asercje kolejno, nie jest migawką). To zawęża okno wyścigu, ale go
  nie zamyka: atomowe sprawdzenie zestawu wymagałoby jednego `page.evaluate` z własną implementacją lokatorów.

### Jak pisać asercje

Asercja ma sprawdzać **efekt celu**, nie sam komunikat o nim:

- **Wartość, stan po zapisie, tożsamość obiektu.** Toast „Zapisano” nie dowodzi, że zapisano właściwą rzecz — dołóż
  asercję wartości pola (`value`) albo nagłówka/nazwy obiektu, którego dotyczył cel. Sam toast, sam adres albo sam nagłówek
  strony rzadko wystarczają.
- **Elementy powtarzalne** (karty, wiersze listy, wiele dialogów) zakresuj przez `within` — inaczej asercja może spełnić się
  na innym egzemplarzu (np. inna karta niż ta, o którą chodzi w celu). Zakres wybieraj po tożsamości (nazwa dialogu, tekst
  karty), nie po pozycji.
- **URL po pathname.** Glob pasuje do ścieżki bez zapytania i hasha, więc `**/panel/ustawienia/konto` nie przepuści
  `/panel/ustawienia/konto-usun`, ale też nie zwiąże się z parametrem zapytania — gdy parametr jest częścią efektu, wpisz `?`
  do globu (`**/lista?filtr=aktywni`).
- **Ograniczenie: stan po przeładowaniu.** Asercje działają na bieżącej stronie; kontrakt nie ma kroku przeładowania, więc
  trwałość zapisu (czy wartość przetrwa odświeżenie) nie jest potwierdzana. Asercja wartości pola po zapisie dowodzi
  stanu formularza, nie bazy danych — trwałość potwierdza osobny test.
- Asercje, które spełniają się **przed** jakąkolwiek akcją, dają `passedWithoutActions: true` — przejście niczego nie
  sprawdziło; dobieraj asercje tak, by stan początkowy ich nie spełniał.

## Algorytm

Na każdym kroku:

1. Limit czasu przejścia (`timeoutMs`) → `FAIL` / `TIMEOUT`. Termin jest sprawdzany też przed każdą akcją i przed końcowymi
   asercjami — **po terminie nigdy `PASS`**. Wywołanie Jev dostaje limit `min(30 s, pozostały czas)`, a akcja
   `min(8 s, pozostały czas)`.
2. Origin: strona poza originem `baseUrl` albo wcześniejsza zablokowana próba wyjścia → `FAIL` / `OFF_ORIGIN` (**przed**
   asercjami). Strażnik originu (przerywanie nawigacji głównej ramki poza origin `baseUrl`) i zamykanie nowych kart
   działają **do końca końcowych asercji**, nie tylko do końca pętli.
3. Szybkie asercje (jeden przebieg całego zestawu, przy sukcesie potwierdzony drugim); wszystkie spełnione → **ponowne
   sprawdzenie originu** (strona na originie `baseUrl` i zero zablokowanych nawigacji; inaczej `FAIL` / `OFF_ORIGIN`),
   dopiero potem `PASS` (na kroku 0: `passedWithoutActions: true`).
4. `collectPageState`: widoczne, niewyłączone elementy interaktywne, podsumowanie strony, odcisk palca.
5. Ten sam odcisk po raz 4. → `LOOP` / `SAME_STATE_4X`. Odcisk (adres + nakładka + lista `rola|nazwa|wartość|stan`)
   jest liczony z wartości **prywatnych** — po zamaskowaniu sekretów, ale BEZ maskowania danych osobowych — więc zmiana
   numeru telefonu czy e-maila w nazwie lub wartości elementu, w adresie albo w nakładce daje inny odcisk, choć opis dla
   modelu (`<phone>`, `<email>`) jest ten sam. Tytuł, nagłówki i komunikaty do odcisku nie wchodzą.
   Odcisk nie opuszcza procesu (nie ma go w stanie dla Jev, raporcie ani migawce).
6. Decyzja Jev (dwa etapy, niżej). Para (odcisk, akcja) już **wykonana z powodzeniem** → `LOOP` / `REPEATED_ACTION`.
7. **Element tuż przed akcją:** odczytywany jest aktualny opis żywego elementu `[data-bc-id=eN]` (rola + nazwa) i
   porównywany z **prywatnym odciskiem** elementu zebranym ze stanem (SHA-1 z `rola|nazwa`, nazwa po zamaskowaniu
   sekretów, BEZ maskowania danych osobowych), więc dwa elementy różniące się tylko zamaskowaną daną (np. `Usuń jan@…` →
   `Usuń ewa@…` pod tym samym `eN`) są rozróżniane, choć model widzi ten sam opis. Odciski trzyma `WeakMap` w
   `page-actions.mjs` kluczowana obiektem elementu — nie są polem elementu, więc `JSON.stringify`/raport/migawka/stan dla
   Jev ich nie widzą. Ponownie sprawdzane są też zakazy. Odcisk inny, element zniknął/wyłączony albo zakazany → akcja
   **nie jest wykonywana**; krok dostaje `error: "STALE_ELEMENT"` (`staleDetail`: `missing` / `changed` /
   `forbidden`), stan jest zbierany od nowa, a błąd liczy się do limitu z pkt 9. Termin jest sprawdzany jeszcze raz po tej
   weryfikacji, przed akcją (`TIMEOUT`, akcja niewykonana). Dla `select:eN` tuż przed `selectOption({ index })`
   sprawdzany jest prywatny odcisk tekstu opcji pod tym indeksem (np. `[Alpha, Beta]` → `[Beta, Alpha]`); różnica →
   `STALE_ELEMENT` / `changed`, nic nie zostaje wybrane.
8. Wykonanie akcji (Playwright, bez `force`); potem `domcontentloaded`, `networkidle` (≤ 3 s, timeout połykany) i
   `settleMs`. Nawigacje **głównej ramki** poza origin `baseUrl` są w kontekście przejścia przerywane (zasoby podrzędne —
   skrypty, czcionki, iframe, np. Turnstile — przechodzą); próba wyjścia kończy przejście `FAIL` / `OFF_ORIGIN`.
9. Błąd akcji (także `STALE_ELEMENT`): pierwszy zapisywany i pętla trwa; drugi z rzędu → `FAIL` / `ACTION_ERROR`.

Po `maxSteps` krokach: końcowe asercje (`final`) — spełnione (i w terminie) → `PASS`, inaczej `FAIL` / `MAX_STEPS`. Przy
każdym zakończeniu powstaje zrzut `flow-<name>-final.png` i migawka `flow-<name>-final.json` (podsumowanie + elementy;
dla strony poza originem migawki nie ma); wynik asercji po `maxSteps` jest liczony z czekaniem (do 5 s), po innym
zakończeniu niepowodzeniem — jednym przebiegiem, tylko do raportu (status się nie zmienia). Błąd zrzutu lub migawki
(także błąd zebrania stanu do migawki) to `result.artifactError`: przejście liczy się wtedy w CLI jako nieudane (kod
wyjścia 1), mimo statusu asercji. Gdy zebranie stanu do migawki kończy się `FORBIDDEN_LOCATOR_INVALID`, status to `ERROR`
niezależnie od wcześniejszych asercji (fail-closed). Origin jest sprawdzany ponownie bezpośrednio przed przyjęciem `PASS`
(także końcowego); zrzut i migawka powstają już po zdjęciu strażnika (migawki nie ma dla strony poza originem).
Nowe karty (`window.open`) są zamykane od razu i odnotowane w `warnings`.

### Elementy i zakres

Kandydaci: `a[href]`, `button`, `input`, `textarea`, `select`, role interaktywne (`button`, `link`, `menuitem*`, `option`,
`tab`, `checkbox`, `radio`, `switch`, `combobox`) i `contenteditable`. Tylko widoczne (`checkVisibility` +
niezerowy prostokąt) i niewyłączone (`disabled`, `aria-disabled`). Element, którego przodek-kandydat ma tę samą nazwę,
jest pomijany.

**Zakres nakładki:** gdy widoczna jest nakładka, kandydaci pochodzą wyłącznie z **ostatniej** takiej nakładki w kolejności
DOM. Nakładką jest (a) element **modalny** — `[role=dialog]`, `[role=alertdialog]` albo `[aria-modal=true]` — albo (b)
bezpośredni potomek `<body>` inny niż korzeń aplikacji, który ma `position: fixed|absolute` (sam albo jego pierwszy
potomek) lub semantykę dialogu/listy/menu (`dialog`, `alertdialog`, `listbox`, `menu`, `aria-modal`). PrimeNG renderuje
nakładki, listy i menu w `body`; Drawer nie ma `role=dialog`. **Nakładka modalna zawsze zawęża zakres, także bez
żadnej dostępnej kontrolki** — wtedy modelowi zostają tylko `press:Escape` i `none` (bez `back`). Filtr „zawiera coś
operowalnego” dotyczy wyłącznie nakładek niemodalnych: podpowiedź (tooltip), pusta maska albo ukryty kontener nie
zawężają zakresu.

Opis elementu dla modelu: `<rola> "<nazwa>" in <region>` (+ `(item: "…")`, gdy kilka elementów ma tę samą rolę i nazwę —
np. „Rozwiń” na każdej karcie listy: kontekst to tekst największego przodka zawierającego tylko ten element z grupy
duplikatów). Pola mają `(current: "…")`. Gdy kandydatów jest więcej niż `maxOptions`, zostają w kolejności: nakładka >
`main` > `dialog` > `nav` > `header` > `aside` > `footer` > reszta (w obrębie — kolejność DOM); liczba odciętych to
`truncated`.

**Maskowanie przed wysłaniem do modelu** (kolejność w Node: sekrety na tekście SUROWYM, spłaszczenie białych znaków, dane
osobowe, przycięcie). Przeglądarka zwraca teksty surowe — nie spłaszcza ich i nie obcina poniżej twardego limitu
technicznego `rawLimit = max(600, 2 × najdłuższa forma sekretu + 600)` (długość sekretów nie jest sekretem; same sekrety
nie trafiają do przeglądarki), więc sekret nie zostanie ucięty ani zwinięty, zanim Node go zamaskuje:

- **Sekrety:** każda wartość podstawiona z `${env:…}` (surowa, `encodeURIComponent`, forma JSON, forma ze spłaszczonymi
  białymi znakami, o ile różni się od surowej) oraz `TYPESAFE_API_KEY` → `***`, w każdym tekście strony. Wartość `${env:…}` krótsza niż 4 znaki jest błędem scenariusza (kod 2) — za krótka, by
  ją bezpiecznie maskować.
- **Dane osobowe:** najpierw dekodowane są (fragmentami) ciągi `%XX` oznaczające drukowalny ASCII, potem e-maile (także
  zakodowane procentowo) → `<email>`; numery → `<phone>`, gdy „numer” (grupy cyfr
  rozdzielone co najwyżej dwoma znakami spacji, kropki lub myślnika, nawiasy, wiodący `+`) ma ≥ 9 cyfr.
- Dotyczy nazw, wartości, nagłówków, komunikatów, tytułu, opisów regionów, **opcji `select`** i adresów (`summary.url`,
  `history[].urlAfter`, `finalUrl`, `failedRequests[].url`): adres jest rozbierany `new URL` (względny — względem
  zastępczego originu, który nie trafia do wyniku; błąd rozbioru → całość jako tekst), ścieżka i hash są dekodowane
  procentowo **po segmencie** (błędny segment nie blokuje pozostałych), zapytanie przez `URLSearchParams` (`+` = spacja), a
  ścieżka, każda nazwa i każda wartość są maskowane osobno. Wynik jest zdekodowanym tekstem do raportu, nie adresem do
  nawigacji. Komunikaty błędów (w tym `FORBIDDEN_LOCATOR_INVALID` z opisem lokatora) też przechodzą przez maskowanie
  przed zapisem do `reason`, `warnings` i stdout. `consoleErrors`/`pageErrors` są maskowane (sekrety i PII) przed
  przycięciem do 300 znaków. Wartości `testData` wysyłane są jawnie.
- Raport i migawki: wartości tekstowe obiektu są redagowane **przed** `JSON.stringify` (plik zawsze jest poprawnym JSON-em,
  także gdy sekretem jest np. `null`); `assertions[].actual` jest maskowane jak tekst strony.

### Akcje i polityka Jev

Akcje (etykieta → opis): pola tekstowe i `contenteditable` → `fill:eN` (tylko z `testData`); natywny `select` →
`select:eN`; reszta → `click:eN`; ponadto `back` (gdy w historii jest krok), `press:Escape` (otwarta nakładka) i `none`.

- **Etap 1** — `choice(instrukcja, akcje)`; `state` = `{ goal, subgoals, testData, page: podsumowanie, history: ostatnie 8 kroków }`.
- **Etap 2** — dla `fill:eN` wybór klucza z `testData` (+ `none`), dla `select:eN` wybór opcji (≤ 50). Opcje trafiają do
  modelu jako etykiety `o1…oN` z zamaskowanymi opisami (bez deduplikacji); wykonawca wybiera **oryginalną** opcję po
  indeksie (`selectOption({ index })`), nie po zamaskowanym tekście. `state` etapu 2 to cel, opis pola z bieżącą wartością,
  `testData`, adres i historia.
- Próg: `confidence` (pole odpowiedzi) obu etapów ≥ `confidenceThreshold`; inaczej `NEED_FALLBACK` (`LOW_CONFIDENCE`).
  Wybór `none` → `NEED_FALLBACK` (`NONE_CHOSEN` w etapie 1, `NO_TEST_DATA_MATCH` w etapie 2).
- Wyjątek SDK → `ERROR` z komunikatem (bez klucza).

**Ostateczne brzmienie instrukcji etapu 1** (angielska, ogólna — bez odniesień do konkretnej aplikacji):

> You operate a web application to reach the goal. Choose the single next action that best moves toward the goal. Use the
> history: do not repeat an action that already succeeded unless the page changed. If an earlier action opened a menu or a
> panel and its items are now listed, choose among those items instead of opening it again. Fill empty or incorrect fields
> before pressing a submit button. Choose 'none' if no listed action helps.

Zmiana względem wersji startowej: dodane zdanie o menu/panelu (bez niego model wybierał ponownie otwieracz menu zamiast
jego pozycji, z pewnością tuż pod progiem). Instrukcja etapu 2: „Which test data value should be typed into the field
`<opis pola>` to progress toward the goal?”; kryterium wartości: `Type the value "<wartość>" (test data "<klucz>")`, kryterium
odrzucenia `none`: „None of these values belongs in this field”. Opis wartości (zamiast samej wartości) podniósł pewność
etapu 2 z 0,66 do 1,00 przy jednej wartości testowej.

## Statusy

| Status | Znaczenie |
| --- | --- |
| `PASS` | wszystkie asercje spełnione (przed akcjami, w trakcie albo po `maxSteps`) |
| `FAIL` | `reason`: `TIMEOUT` (także gdy asercje są spełnione po terminie), `OFF_ORIGIN`, `ACTION_ERROR`, `MAX_STEPS` |
| `NEED_FALLBACK` | model nie umie dobrać akcji: `LOW_CONFIDENCE`, `NONE_CHOSEN`, `NO_TEST_DATA_MATCH`, `NO_OPTIONS` — do rozstrzygnięcia przez człowieka/architekta |
| `LOOP` | `SAME_STATE_4X` albo `REPEATED_ACTION` |
| `ERROR` | błąd API Jev, nieczytelna strona (`PAGE_STATE`), wadliwy lokator zakazu (`FORBIDDEN_LOCATOR_INVALID`, także przy zbieraniu migawki końcowej — wtedy niezależnie od asercji) albo wyjątek silnika |

Tylko `PASS` liczy się jako sukces w kodzie wyjścia CLI.

## Wynik (`report.json` › `flows[]`)

```
{ name, status, reason?, passedWithoutActions,
  steps: [{ n, url, options, truncated, overlay, action, target, valueKey?, confidence, top3: [{label,p}],
            stage2?: { choice, confidence }, jevMs, actionMs, valueMatched?, error?, staleDetail? }],
  totals: { steps, jevCalls, jevMs, inputTokens, outputTokens, durationMs },
  artifactError?, finalUrl, assertions: [{ assertion, ok, actual? }], warnings, screenshot, snapshot, model }
```

Do wyniku CLI dopisuje `consoleErrors`, `pageErrors`, `failedRequests` zebrane w trakcie przejścia (anulowania żądań przez
nawigację — `ERR_ABORTED` — są pomijane). Log: jedna linia na
krok (`FLOW <name> #3 click:e12 button "Zapisz" in dialog "…" conf 0.91 jev 260ms act 410ms`) i podsumowanie
(`FLOW <name> PASS 5 steps 3.2s jev 1.4s tokens 9123`). Teksty przechodzą przez `redact`.

## Ograniczenia

- Model wybiera wyłącznie spośród listy etykiet; nie widzi obrazów i nie generuje tekstu. Najlepiej działa po angielsku,
  ale cele po polsku przy polskim UI też się sprawdzają (pomiar: `examples/`).
- **Cel musi nazywać drogę w języku UI.** Gdy jedyna ścieżka do wyniku ma inną nazwę niż cel (np. cel „pokaż kod karty”,
  a w UI przycisk „Odbierz nagrodę …”), model odpowiada `none` lub z pewnością poniżej progu → `NEED_FALLBACK`.
- Ukryte wizualnie kontrolki (`opacity: 0`, np. natywne `input` checkboxa schowane pod własnym wyglądem) nie są
  kandydatami (`checkVisibility` z `checkOpacity`).
- Nakładka **niemodalna** bez operowalnego elementu nie zawęża zakresu; nakładka modalna zawęża zawsze (zob. Zakres nakładki).
- Składnia `css` w `forbidden` jest sprawdzana dopiero w czasie wykonania (`FORBIDDEN_LOCATOR_INVALID`), nie w `validateFlows`.
- `fill` tylko dla pól tekstowych (`text`, `email`, `tel`, `search`, `number`, `password`, `url`), `textarea` i
  `contenteditable`; daty, suwaki i pola plików nie są wypełniane.
- Pula akcji jest ograniczona do `maxOptions`; przy dużych stronach ważne elementy spoza `main`/nakładki mogą zostać odcięte.
- Akcje są wykonywane na prawdziwej bazie — to, czego pętla nie ma dotykać, wpisz w `forbidden`
  (np. przyciski wylogowania, usuwania i zatwierdzania formularza).
- Asercje nie potwierdzają stanu po przeładowaniu strony (zob. „Jak pisać asercje”).
- Przejście bez `testData` nie dostaje akcji `fill`; przejście z `testData` może wpisać dane w pole wyszukiwania, jeśli cel
  nie wyklucza tego jednoznacznie.
