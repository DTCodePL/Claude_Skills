---
name: implement-ado-feature-zebrani
description: >
  Planowanie i pełna implementacja feature'a / PBI / taska Zebrani.pl na
  podstawie linku lub numeru Azure DevOps — od Plan Mode (z makietami Figmy
  linkowanymi wprost, nie opisywanymi), przez wykonanie w modelu: sesja
  główna Opus max = architekt, dyspozytor i walidator etapów (nigdy
  wykonawca) / linie wykonawcze w stałej kolejności Claude → Spark → Codex
  (Sonnet do Figmy/MCP, Spark do wszystkiego tekstowego bez limitu slotów,
  Codex tylko recenzja i research) / niezależny recenzent Codex, przez
  zlecony audyt SCSS pod kątem Bootstrapa i deduplikacji, aż po bramę mojego
  potwierdzenia i dopiero wtedy domknięcie w ADO (commit/push,
  statusy tasków deweloperskich, PBI → Ready for tests, przypisanie do
  testera). Na starcie, tuż po zatwierdzeniu planu, PBI/Bug i taski
  przewidziane do wykonania idą na In Progress. Obejmuje też naprawę Bugów —
  wtedy obowiązuje zasada test-first: najpierw czerwony test dowodzący błędu,
  potem łatka, ten sam test bez zmian zielony. UŻYWAJ ZAWSZE, gdy user poda
  link lub numer Epic/Feature/PBI/Task/Bug
  z Azure DevOps projektu Zebrani.pl i poprosi o zaplanowanie, zaimplementowanie
  i/lub naprawienie go — nawet jeśli nie padnie słowo "skill".
version: '5.0'
language: pl
project: Zebrani.pl
organization: DTCode
remote:
  github_raw: 'https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/Implement%20ADO%20Feature%20%E2%80%93%20Zebrani/SKILL.md'
  github_page: 'https://github.com/DTCodePL/Claude_Skills/blob/main/Implement%20ADO%20Feature%20%E2%80%93%20Zebrani/SKILL.md'
---

# Implementacja feature'a Zebrani.pl na podstawie ADO

Ten plik jest **źródłem prawdy** procedury — repozytoria projektu
(`ZebraniFE`, `ZebraniBE`) trzymają wyłącznie cienki loader
`implement-ado-feature-zebrani`, który pobiera tę treść z GitHuba (tak samo
jak `azure-devops-zebrani` / `fix-devops-bug-zebrani` /
`qasphere-test-generator`). Zmiany w procedurze rób tutaj, nigdy w loaderze.
Skill zakłada, że w repo projektu obowiązuje `.claude/CLAUDE.md` (w ZebraniBE
kopia jako `AGENTS.md`) — nie duplikuj jego zasad w brifach dla subagentów,
tylko cytuj/linkuj właściwą sekcję ("a subagent does not inherit project
rules by osmosis").

## Rola sesji głównej — mózg operacji

**Sesja główna to Claude Opus na efforcie `max`. Jest architektem, dyspozytorem
i walidatorem — i niczym więcej.** Przez cały cykl (plan → etapy → recenzja →
brama → ADO) robi wyłącznie cztery rzeczy:

1. **Projektuje** — czyta ADO, dokumentację i makiety, podejmuje każdą decyzję
   (adresy, nazwy, kształt API, tokeny, przypadki brzegowe) i zapisuje je w
   planie oraz w briefach. Fakty z repo zbiera dla niej `zwiadowca`.
2. **Dysponuje** — dzieli etap na briefy, przypisuje linie wg tabeli w Fazie 2
   (z rozdziałem proporcjonalnym do pul), wysyła niezależne briefy w jednej
   wiadomości równolegle.
3. **Waliduje każdy etap** — czyta diff, uruchamia lint/test/build, ogląda
   zrzuty 2×2, odsyła korekty do tej samej linii. Raport wykonawcy nigdy nie
   jest dowodem.
4. **Otwiera i domyka w ADO** — po zatwierdzeniu planu ustawia `In Progress`
   (Faza 1b); na końcu triażuje recenzję Sol, prowadzi bramę potwierdzenia,
   robi commit/push i statusy końcowe (jedyne MCP do ADO ma Claude).

**Sesja główna nie pisze kodu, nie pisze testów, nie przepisuje po wykonawcy
i nie czyta dwudziestu plików „żeby sprawdzić"** — każde z tych działań to
brief do właściwej linii. Jedyny wyjątek to reguła 11 z globalnego
`CLAUDE.md`: jednolinijkowa zmiana, przy której brief kosztuje więcej niż
robota. `max` na Opusie jest po to, żeby decyzje i walidacja były najlepsze
w całym łańcuchu — nie po to, żeby tym effortem pisać komponenty.

## Faza 1 — Plan (Plan Mode, po polsku)

Zanim zlecisz jakikolwiek kod, wejdź w Plan Mode i ustal:

- **Makiety z Figmy.** Pobierz makiety pod linkami podanymi w opisie PBI i w
  planie odwołuj się do nich linkami/node-id, nigdy własnym opisem "na oko"
  — UI ma być 1:1 zgodne z Figmą. Do rzeczy, których Figma nie pokazuje
  (mikrointerakcje, hover, animacje wejścia/wyjścia), zrób research aktualnych
  trendów UI/UX i dobierz rozwiązanie świadomie, nie przez zgadywanie.
- **PrimeNG maksymalnie, stylowania minimalnie.** Komponenty, design system
  PrimeNG i nasze tokeny kolorów — unikaj w jak najwyższym stopniu stylowania
  per komponent (własny CSS/SCSS). Do układu i responsywności strony używaj
  grida Bootstrapa (`src/vendor/bootstrap-grid.min.css`) zamiast własnych
  media query/flexboksa tam, gdzie grid wystarcza.
- **Enumy zamiast union types** — również w szkicach sygnatur w brifach dla
  subagentów, nie tylko w finalnym kodzie.
- **Taski, które nie mają sensu dla tego zadania** (typowo BE/DB przy czysto
  frontendowej zmianie) pomiń w planie realizacji i wypisz je w planie
  z uzasadnieniem — w ADO pójdą na `Rejected` z tym komentarzem w Fazie 1b,
  tuż po zatwierdzeniu planu, nie na koniec.
- Jeżeli w PBI albo w Figmie brakuje specyfikacji potrzebnej do decyzji,
  **zatrzymaj się i zapytaj** zamiast zgadywać.
- **Bilans obciążenia silników** jako obowiązkowy element planu: tabela
  „etap → brief → linia" plus liczba briefów per silnik. Sprawdzian przed
  pokazaniem planu — plan jest zroutowany źle, gdy zachodzi cokolwiek z:
  Codex ma w planie coś poza recenzją Sol i researchem Terry; Spark dostał
  cokolwiek zależnego od Figmy; jakikolwiek brief w całości tekstowy poszedł
  na Sonneta, choć Spark nie zgłosił limitu. Popraw, zanim go pokażesz.
  Nie prosisz o odczyt `/usage` — kolejność Claude → Spark → Codex jest
  stała, a linia zmienia się dopiero po komunikacie o limicie z silnika.
- **Gdy work item to Bug**, plan ma dodatkowo wskazać **test, który udowodni
  błąd**: jego rodzaj (spec Vitest / test xunit / Playwright, gdy błąd widać
  tylko w przeglądarce), plik i nazwę, dokładne kroki odtworzenia zamienione
  na asercje oraz oczekiwany wynik po naprawie. Bez tego punktu plan buga jest
  niekompletny — patrz Faza 3, „Bug: test first”.

## Faza 1b — Otwarcie w ADO (po zatwierdzeniu planu, przed pierwszym briefem)

Pierwsze działanie po wyjściu z Plan Mode, **zanim wyślesz jakikolwiek
brief**: praca, która zaraz ruszy, ma być widoczna w ADO jako trwająca.
Jeden `mcp__azure-devops__wit_work_item_write` `action: update_batch`:

1. **PBI / Bug → `In Progress`.**
2. **Wszystkie taski deweloperskie, które plan przewiduje do wykonania**
   (FE/BE/DB/Figma; dla Buga sub-task `Fix`) **→ `In Progress` — od razu
   wszystkie, nie etap po etapie.** Stan mówi „tym się zajmuję lub zaraz
   zajmę", nie „to właśnie się dzieje w tej minucie". `Manual tests` /
   `E2e tests` (dla Buga `Retest`) zostają nietknięte — to praca testera.
3. **Taski wypisane w planie jako nieadekwatne → `Rejected`** z komentarzem
   uzasadniającym z planu (`wit_work_item_comment_write` przed zmianą stanu).

Przed zapisem zweryfikuj nazwę stanu przez `mcp__azure-devops__wit_work_item`
`action: get_type` dla każdego typu (`Task`, `Product Backlog Item`, `Bug`) —
`In Progress` istnieje na wszystkich trzech (odczyt API 2026-08-02), ale
literówka w nazwie stanu to błąd API dopiero po całym batchu. **Zweryfikuj
przez zwróconą treść odpowiedzi** — dowodem jest stan pola w odpowiedzi, nie
brak wyjątku. Work item już w `In Progress` pomiń bez błędu; work item
w `Done` / `Rejected` / `Removed` zgłoś mi zamiast cofać jego stan.

Jeśli plan wraca do poprawy po tej fazie, stany zostają — tylko nowo
odrzucone taski dostają `Rejected`, a taski przywrócone do zakresu
`In Progress`.

## Faza 2 — Wykonanie: architekt + linie wykonawcze + recenzent

Główny wątek nigdy nie jest wykonawcą tego, co da się zlecić:

1. **Projektujesz** — podejmujesz z góry każdą decyzję (nazwy, pliki, tokeny,
   kształt API, przypadki brzegowe), żeby wykonawca nie musiał zgadywać.
   Fakty z repo, których potrzebujesz do decyzji, zbiera `zwiadowca` — nie
   czytasz dwudziestu plików w sesji architekta.
2. **Dzielisz i dysponujesz** — niezależne zadania wysyłasz w jednej wiadomości
   równolegle, każde na linię z tabeli poniżej. Każdy brief dostaje pełną
   specyfikację plus właściwe sekcje CLAUDE.md, klauzulę "jeśli premisa w tej
   specyfikacji jest błędna, ZATRZYMAJ SIĘ i zgłoś zamiast wykonywać
   dosłownie" oraz wymaganą sekcję raportu "Co uważasz za błędne w tej
   specyfikacji?".
3. **Walidujesz** — nigdy na słowo wykonawcy. Dowodem zamykającym zadanie jest
   diff, lint, testy, build, zrzut ekranu — nie deklaracja sukcesu.
4. **Zlecasz recenzję** niezależnemu recenzentowi (Faza 4b) — zanim zgłosisz
   gotowość do bramy potwierdzenia.

Dobór linii do zadania (pełna tabela z effortami, progami ciśnienia
i uzasadnieniem liczbowym: globalny `~/.claude/CLAUDE.md`; ta tabela jest jej
zastosowaniem do tego skilla). **Kolejność Claude → Spark → Codex, wg
rodzaju pracy, nie wg procentów**: brief, który potrzebuje MCP (Figma, ADO,
Playwright) albo pętli lint/test/build u wykonawcy → Sonnet `wykonawca`;
brief w całości tekstowy, ciężki czy lekki → **Spark, bez limitu slotów,
równolegle** — jak subagenci Claude'a: rozłączne zbiory plików, zakaz
`git`/`npm`/`dotnet` w briefie, każdy brief osobnym wywołaniem wrappera
w tle (nie `Start-Job`); pojedynczy drobiazg → `mechanik`.
**Codex w planie etapu to tylko recenzja Sol i research Terry** — Terra
i Luna implementują wyłącznie jako przelew po komunikacie o limicie
z Claude'a albo Sparka. O `/usage` nie prosisz.

| Zadanie w planie                                                                                                                                                                                                                                                                                                                                                                                                                      | Linia                                                                                                            |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| decyzje, brief, WCAG/tokeny, walidacja dowodów, triaż recenzji, domknięcie ADO                                                                                                                                                                                                                                                                                                                                                        | **sesja główna — Opus `max`** (mózg operacji; nigdy nie pisze kodu ani testów)                                   |
| **brief z Figmą, ADO, Playwrightem albo pętlą lint/test/build u wykonawcy** (ekran z makiet, feature z dowodem w przeglądarce) — **domyślnie dla wszystkiego, czego nie da się opisać samym tekstem**                                                                                                                                                                                                                                                                                                                                                      | agent **`wykonawca`** (Sonnet `high`) — bez limitu wielkości; w BE czyta `.claude/CLAUDE.md` (kopia `AGENTS.md`) |
| **każdy brief, ciężki czy lekki, spełniający oba warunki**: zero zależności od Figmy (spec w całości tekstowa) i weryfikacja po stronie architekta wystarczy (Spark w WSL nie ma Node ani .NET — pisze na ślepo, lint/test/build robisz Ty). Ciężkie: slice BE w C#, infrastruktura FE (sesja, guardy, trasy, interceptory, DTO, store), refaktor przekrojowy, hoisting, audyt (1M). Lekkie: ≤ 5 plików bez MCP, klucze i18n hurtem, masówka > 10 plików. **Bez limitu slotów, równolegle** (rozłączne pliki, zakaz `git`/`npm`/`dotnet` w briefie, osobne wywołania wrappera w tle) — linia pusta tylko wtedy, gdy w etapie nie ma nic tekstowego; ekranu się jej nie wciska | **Spark** `xhigh` (ciężkie) / `high` (lekkie wg gotowej spec)                                                    |
| **przelew awaryjny** — wyłącznie po komunikacie o limicie z Claude'a albo Sparka, nigdy w planie etapu; porcje ≤ 5 plików                                                                                                                                                                                                                                                                                                             | **Codex** `gpt-5.6-terra` `xhigh` (ciężkie) / `gpt-5.6-luna` `xhigh` (lekkie, masówka)                            |
| zadanie z Figma/ADO przez MCP, z kontekstem sesji                                                                                                                                                                                                                                                                                                                                                                                     | agent **`wykonawca`** (Sonnet `high`) — tylko Claude ma te MCP                                                   |
| speci Vitest / AXE / xunit; czerwony test do Buga                                                                                                                                                                                                                                                                                                                                                                                     | agent **`tester`** (Sonnet `medium`)                                                                             |
| klucz i18n × 2, rename, przeniesienie pliku — pojedynczo; masówka w porcjach, gdy Spark zgłosił limit                                                                                                                                                                                                                                                                                                                                                                              | agent **`mechanik`** (Haiku `low`)                                                                               |
| fakty z repo przed decyzją                                                                                                                                                                                                                                                                                                                                                                                                            | agent **`zwiadowca`** (Haiku `low`, tylko odczyt)                                                                |
| delegowany audyt kontrastu / fokusu / tokenów                                                                                                                                                                                                                                                                                                                                                                                         | agent **`audytor-a11y`** (Opus `high`)                                                                           |
| recenzja diffu etapu przed bramą — **1 na etap**                                                                                                                                                                                                                                                                                                                                                                                      | **Codex** `-Mode review`, `gpt-5.6-sol` `high`                                                                   |
| research trendów UI/UX, weryfikacja API biblioteki (Faza 1)                                                                                                                                                                                                                                                                                                                                                                           | **Codex** `gpt-5.6-terra` `medium`                                                                               |

Przykład dla planu o 4 etapach, każdy z FE + BE: etap 0 — infrastruktura FE
(sesja, guardy, trasy, interceptory) Spark, slice BE Spark, ekran z makiet
Sonnet; etap 1 — FE z makiet Sonnet, BE Spark, klucze i18n Spark `high`;
etap 2 — hoisting komponentu Spark, ekrany Sonnet, BE Spark; etap 3 — BE
Spark, FE Sonnet. Codex dostaje 4 recenzje Sol i research — zero
implementacji; Claude niesie ekrany (ma Figma MCP i pętlę lint/test/build);
Spark niesie każdy brief tekstowy — briefy jednego etapu równolegle, o ile
nie dotykają tych samych plików — a Ty po nich uruchamiasz lint/test/build
z rezerwą na 2–3 korekty. Trzy plany, które były zroutowane błędnie:
Claude tylko plan i testy, Codex 8 ciężkich (2026-09-16); Spark dostał
ekrany „bo 16 ramek Figmy", których nie widzi, więc architekt musiałby
przepisać makiety do tekstu, a potem Sonnet naprawiać kod pisany bez lintu
(2026-09-16); Spark 1 slot na okno, Terra i Luna implementują — Spark stał
na < 1 % tygodnia, Codex wyczerpywał widełki (2026-09-18, powód tej wersji).

Pułapki, które w tym skillu kosztowały najwięcej:

- **Gołe `Agent` z samym `model` dziedziczy effort sesji (`max`).** Subagenta
  Claude'a wywołujesz wyłącznie jako nazwanego agenta z listy wyżej — tylko
  definicja agenta niesie `effort`.
- **Progi procentowe nie działają, bo ich nie widzisz.** Tabela z „Spark
  1 slot, Terra 1 slot, Luna lekkie" wymagała odczytu `/usage` od
  użytkownika i i tak dała Sparka na < 1 % tygodnia przy wyczerpywanym
  Codexie (2026-09-18). Kolejność Claude → Spark → Codex jest stała i zależy
  od rodzaju pracy; jedynym sygnałem do zmiany linii jest komunikat
  o limicie z silnika (rate-limit w sesji, błąd wrappera) — wtedy Spark →
  Sonnet, Claude → Terra/Luna w porcjach ≤ 5 plików, i meldujesz zmianę
  jednym zdaniem. „Terra, bo czyta AGENTS.md" (Claude też czyta — kopię
  w `.claude/CLAUDE.md`) i „Luna, bo tania" to fałszywe uzasadnienia.
- **Brief dla Sparka nie może wymagać transkrypcji makiet.** Spark nie ma
  Figma MCP, a w WSL nie ma Node'a ani .NET — dostaje wyłącznie zadania
  opisane w całości tekstem (nazwy, sygnatury, reguły), a lint/test/build po
  nim uruchamia architekt. Ekran z makiet zawsze idzie do `wykonawca`
  (Sonnet): sam pobiera `get_design_context`, sam kręci pętlę lint/test/build.
  Przepisywanie 16 ramek do briefu, żeby tani silnik pisał na ślepo, to
  najdroższy sposób wydania Opusa.
- **Start każdego subagenta Claude'a to ~58 k tokenów promptu.** Drobiazgi
  (kilka kluczy i18n, dwa rename'y) idą w jednym briefie do jednego
  `mechanik`a, nie w pięciu wywołaniach.

## Faza 3 — Implementacja etapu (linie wykonują, sesja główna waliduje)

Implementację wykonują linie z Fazy 2 wg briefów — **sesja główna nie pisze
kodu**. Jej robota w tej fazie to walidacja dowodów po każdym briefie: diff,
`npm run lint` / `npm test` / `npm run build` (FE) albo `dotnet build` /
`dotnet test` (BE), zrzuty 2×2 (360×530 i 1280×720, Light i Dark). Zrzuty
dostarcza `wykonawca` (ma Playwright MCP) albo Terra (ma Playwright); Spark
nie ma żadnego MCP i nie uruchomi lint/test/build w WSL — po jego briefie
całą weryfikację robisz Ty, z rezerwą na 2–3 drobne korekty.

Gdy coś wizualnego po korekcie nadal wygląda źle albo jest tylko przybliżone
„na oko" (np. odstęp liczony z tokenu paddingu zamiast z realnego renderu),
**nie zlecasz kolejnej rundy prób i błędów** — zlecasz research właściwej
techniki (Terra `medium`) i dopiero potem brief korekty z konkretną metodą.

Weryfikacja wizualna zawsze w prawdziwej przeglądarce (dev server), zgodnie
z CLAUDE.md · FE · Finishing Every Implementation — jsdom/AXE nie dowodzi
kontrastu ani interakcji nakładek.

### Bug: test first — czerwony test przed łatką, ten sam test zielony po niej

Gdy work item to **Bug**, kolejność jest obowiązkowa i niezmienna:

1. **Najpierw test, który udowadnia błąd — brief do agenta `tester`.**
   Zautomatyzowany test (spec Vitest / test xunit; Playwright tylko wtedy,
   gdy błąd jest widoczny wyłącznie w prawdziwej przeglądarce) odtwarzający
   dokładnie scenariusz ze zgłoszenia i asertujący **zachowanie poprawne**.
   Tester uruchamia go na kodzie bez poprawki — **musi być czerwony**, i to
   z powodu buga, nie z powodu literówki w teście czy brakującego providera —
   i wkleja wynik (nazwa testu, komunikat asercji) do raportu. Ty sprawdzasz,
   że czerwień pochodzi z buga.
2. **Dopiero potem łatka — osobny brief do Sparka, gdy spec łatki jest
   tekstowa, albo do `wykonawca`, gdy potrzebny jest MCP lub dowód
   w przeglądarce — z zakazem edycji pliku testu.** Zmienia się kod produkcyjny,
   nie test. Jeśli wykonawca zgłosi, że test źle opisał oczekiwane
   zachowanie, wracasz do kroku 1 z poprawionym briefem dla testera **przed**
   łatką — nigdy „dostrajanie” testu pod gotową łatkę.
3. **Ten sam test, bez zmian, ma być zielony** — plus cały pakiet
   (`npm test` / `dotnet test`), żeby łatka niczego nie rozjechała. Diff
   pliku testu między krokiem 1 a 3 ma być pusty — sprawdzasz to sam
   (`git diff` pliku testu); jeśli nie jest, dowód nie jest dowodem i wracasz
   do kroku 1.
4. Test zostaje w repozytorium na stałe jako test regresyjny, nazwany po
   zachowaniu (nie po numerze buga w nazwie metody; numer buga idzie do
   komentarza/opisu i do commita). Zanotuj jego ścieżkę, `describe`/klasę i
   nazwę oraz oba wyniki (czerwony/zielony) — trafią do komentarza
   pieczętującego Buga w ADO (Faza 6, pkt 3).

Nigdy jeden brief „napisz test i napraw" — to dwa briefy do dwóch linii,
a Ty porównujesz oba wyniki, nie deklarację. Błąd niemożliwy do złapania żadnym testem (np. czysto wizualny odcień
koloru) to wyjątek do **zgłoszenia i uzasadnienia** w planie — wtedy dowodem
są zrzuty BEFORE/AFTER w macierzy 2×2 z `fix-devops-bug-zebrani`, ale nie
domyślna droga.

## Faza 4 — Audyt SCSS przed zgłoszeniem gotowości

Zanim zgłosisz zadanie jako gotowe do mojej akceptacji, zlecasz agentowi
`wykonawca` przegląd **wszystkich zmodyfikowanych plików SCSS** wg poniższych
kryteriów (brief: lista plików z `git diff --name-only`, kryteria dosłownie,
raport „co zastąpić / co wydzielić / co zostawić i dlaczego"). Decyzję
o wydzieleniu mixinu albo komponentu podejmujesz Ty, na podstawie raportu —
nie czytasz sam każdego SCSS. Kryteria:

- Co da się zastąpić już zvendorowanym gridem/klasami Bootstrapa? Sprawdź
  realnie, nie zakładaj — jeśli zamiana rozbija jedną regułę na dwa miejsca
  bez realnego zysku (np. bo klasa której potrzebujesz, jak `.gap-*`, nie jest
  w ogóle zvendorowana), to nie jest to zysk i nie rób tego.
- To, czego nie da się zastąpić, a **powtarza się w kilku komponentach**,
  wydziel do wspólnego, reużywalnego kodu: mixin SCSS jako punkt wyjścia,
  a jeśli duplikacja jest strukturalna (to samo zachowanie/API, nie tylko
  wygląd — np. ta sama nakładka rozwijanej listy) — osobny współdzielony
  komponent Angulara, nie tylko style.

## Faza 4b — Recenzja niezależna (Codex `sol`, przed bramą)

Autor nie recenzuje sam siebie. Po samoaudycie SCSS, a **przed** zgłoszeniem
gotowości, zlecasz przegląd niescommitowanego diffu recenzentowi z innej
rodziny modeli niż wykonawca:

```powershell
$env:USERPROFILE\.claude\bin\worker-run.ps1 `
  -Engine codex -Mode review `
  -Repo D:\projects\DTCode\ZebraniFE `
  -Model gpt-5.6-sol -Effort high `
  -Title "Recenzja PBI #<numer>"
```

(bez `-BriefFile` wrapper sam dokleja `--uncommitted`; dla ZebraniBE `-Repo`
wskazuje na to repo). Jedna wiadomość Sol na feature; `high` jest tu
świadomym wydatkiem — recenzja to praca, w której reasoning znajduje to,
czego `medium` nie widzi — a nie darmowym dodatkiem: waga wiadomości
Codexa rośnie z effortem.

Co robisz z wynikiem — **triaż, nie posłuszeństwo** (skill
`superpowers:receiving-code-review` obowiązuje):

1. Każde znalezisko klasyfikujesz: **defekt** (naprawić), **sporne**
   (rozstrzygasz Ty, z uzasadnieniem w raporcie), **fałszywy alarm** (recenzent
   nie zna konwencji repo — np. zgłasza brak `standalone: true`, `p-button`
   zamiast `[pButton]`, Cream zamiast białego jako „błąd"). Fałszywe alarmy
   wypisujesz z jednym zdaniem dlaczego; nie naprawiasz ich.
2. Defekty wracają **do tej samej linii, która pisała kod** (Spark do Sparka,
   `wykonawca` do `wykonawcy`) jako brief korekty — nie łatasz sam. Wyjątek:
   Spark zgłosił limit → korekta na `wykonawca`.
3. Po korekcie **nie zlecasz drugiej recenzji Sol** — weryfikujesz poprawkę
   dowodem (diff + lint + testy). Druga runda tylko wtedy, gdy korekta
   dotknęła > ~5 plików albo zmieniła kształt API.
4. Do raportu przed bramą dołączasz: liczbę znalezisk w każdej klasie
   i listę spornych z Twoim rozstrzygnięciem.

Pomijasz tę fazę wyłącznie, gdy diff jest czysto mechaniczny (i18n, rename,
przeniesienie pliku) — wtedy piszesz to wprost w raporcie.

## Faza 5 — Brama potwierdzenia (nie zamykaj ADO sam)

Po zakończeniu implementacji **ZATRZYMAJ SIĘ i czekaj na moje potwierdzenie**.
Nie ruszaj statusów w ADO (poza `In Progress` z Fazy 1b, które już stoi) ani
nie commituj samodzielnie na tym etapie.

- Jeśli zgłoszę poprawki → wprowadź je → wróć do tej samej bramy.
- Jeśli potwierdzę, że jest OK → przejdź do Fazy 6.

## Faza 6 — Domknięcie po potwierdzeniu

Wykonaj w tej kolejności:

1. **Commit i push** na `main` — numer PBI w branchu i w commicie
   (CLAUDE.md · Git Workflow). `git add` **jawnie, tylko pliki z briefów
   tego zadania** — w drzewie bywa cudza praca w toku z równoległej sesji,
   nigdy `git add -A`.
2. **Statusy tasków deweloperskich** PBI (FE/BE/DB itd. — nie Manual
   tests/E2e tests, te zostają otwarte, zwykle już przypisane do testera):
   `Done` dla zrobionych (z `In Progress` ustawionego w Fazie 1b),
   `Rejected` z komentarzem uzasadniającym dla pominiętych (zwykle już
   ustawione w Fazie 1b — tu tylko te, które wypadły z zakresu później).
   - **Task „Figma” zamykaj tylko wtedy, gdy makiety rzeczywiście istnieją
     — i sprawdź to, zanim ustawisz `Done`.** Dowodem jest makieta w pliku
     Figma, nie opis taska ani link w PBI: pobierz metadane wskazanych
     node-id (`mcp__claude_ai_Figma__get_metadata`, ew. `get_screenshot`)
     i potwierdź, że każda kompozycja wymieniona w opisie taska (strony,
     zestawy komponentów, warianty Desktop/Mobile × Light/Dark, koperta
     itp.) faktycznie tam jest. Makiety z Fazy 1 zwykle już to spełniają —
     wtedy Figma idzie do `Done` w tym samym batchu co FE/BE/DB. Jeśli
     opis obiecuje więcej, niż plik zawiera, task zostaje otwarty, a w
     komentarzu wpisz, czego brakuje. PBI bez warstwy UI → `Rejected`
     z uzasadnieniem, jak każdy inny nieadekwatny task.
   - **Gdy work item to Bug**, sub-taski to `Fix` i `Retest` (patrz
     `azure-devops-zebrani`): `Fix` → `Done`, `Retest` zostaje otwarty dla
     testera.
3. **Komentarz pieczętujący Buga — obowiązkowy, przed zmianą stanu.** Po
   naprawieniu buga dodaj do work itemu Buga (`wit_work_item_comment_write`)
   komentarz z **nazwą i lokalizacją testu, który go pieczętuje**, w stałym
   układzie:
   - **Test pieczętujący:** `<ścieżka pliku od korzenia repo>` ›
     `<describe/klasa>` › `<nazwa testu>` (repo `ZebraniFE` / `ZebraniBE`);
   - **Przed łatką:** czerwony — wklej komunikat asercji z przebiegu na
     kodzie bez poprawki;
   - **Po łatce:** zielony, test bez zmian; wynik całego pakietu
     (`npm test` / `dotnet test` — liczby);
   - **Commit:** hash i gałąź z `(Bug #<numer>)`.

   Bez tego komentarza nie przechodzisz do pkt 4 — tester ma wiedzieć, co
   dokładnie chroni tę naprawę i gdzie to znaleźć, bez czytania diffu. Jeśli
   zaszedł wyjątek z Fazy 3 (błąd niełapalny testem), komentarz mówi to
   wprost i niesie zrzuty BEFORE/AFTER zamiast wyniku testu.

4. **Stan PBI / Buga → "Ready for tests".** Przed zapisem zweryfikuj dokładną
   nazwę stanu dla typu work itemu (`Task`, `Product Backlog Item` i `Bug`
   mogą się różnić) przez `mcp__azure-devops__wit_work_item`
   `action: get_type`, żeby nie trafić błędem API na literówkę w nazwie stanu.
5. **Przypisanie PBI / Buga** (`System.AssignedTo`) na testera — **Piotr
   Tuński**, `Piotr.Tunski@DTCode.pl`.
6. Zmiany 2, 4 i 5 rób przez `mcp__azure-devops__wit_work_item_write`
   `action: update_batch`, jednym wywołaniem na wszystkie PBI/taski naraz,
   gdzie to możliwe. **Zweryfikuj przez zwróconą treść odpowiedzi API** —
   deklaracja sukcesu nie jest dowodem, dopiero zwrócony stan pola jest.
