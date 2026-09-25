---
name: implement-ado-feature-zebrani
description: >
  Planowanie i pełna implementacja feature'a / PBI / taska Zebrani.pl na
  podstawie linku lub numeru Azure DevOps — od Plan Mode (z makietami Figmy
  linkowanymi wprost, nie opisywanymi), przez wykonanie w modelu: sesja
  główna Opus max = architekt, dyspozytor i walidator etapów (sama nigdy
  nie pisze kodu ani testów — implementacja na poziomie Opusa idzie do
  subagenta wykonawca-opus) / linie wykonawcze: briefy wysokiej stawki
  i za trudne dla Sonneta na wykonawca-opus (Opus xhigh, także ich ekrany
  z Figmy), pozostałe ekrany z Figmy i briefy z kontekstem sesji wyłącznie
  na wykonawca (Sonnet high), każdy brief bez Figmy i spoza wysokiej stawki
  na Sparka (xhigh/high, -Access write, bez limitu slotów), w fali resztę
  także na Gemini (agy, -Access write, nigdy wysoka stawka ani Figma);
  research na Sola, Codex w planie tylko do trudnego researchu i bramki
  Astry / recenzent zawsze z innej rodziny niż autor (diff Sparka → Gemini,
  diff Sonneta/Opusa/Codexa/Gemini → Spark, Sol tylko na limit; P0/P1 do
  obalenia jednym poleceniem), przez audyt SCSS na Sparku, aż po bramę
  potwierdzenia i domknięcie w ADO (commit/push, statusy tasków
  deweloperskich, PBI → Ready for tests, przypisanie do testera).
  Na starcie, po zatwierdzeniu planu, PBI/Bug i taski do wykonania idą na
  In Progress. Obejmuje też Bugi — test-first: czerwony test, łatka, ten
  sam test zielony. UŻYWAJ ZAWSZE, gdy user
  poda link lub numer Epic/Feature/PBI/Task/Bug
  z Azure DevOps projektu Zebrani.pl i poprosi o zaplanowanie, zaimplementowanie
  i/lub naprawienie go — nawet jeśli nie padnie słowo "skill".
version: '5.4'
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
2. **Dysponuje** — dzieli etap na fale briefów o rozłącznych zbiorach
   plików (reguła 14), przypisuje linie wg tabeli w Fazie 2 tak, żeby żadna
   nie stała, i wysyła niezależne briefy fali naraz w jednej wiadomości
   (subagenci Claude'a w tle + wrapper w tle) — razem z torami pobocznymi
   (Figma, dokumentacja, ADO, briefy kolejnej fali), gdy tylko decyzja,
   od której zależą, jest ustalona (Faza 2, „Tory poboczne").
3. **Waliduje raz na falę** — czyta diff, uruchamia lint/test/build, ogląda
   zrzuty 2×2, odsyła korekty do tej samej linii. Raport wykonawcy nigdy nie
   jest dowodem.
4. **Otwiera i domyka w ADO** — po zatwierdzeniu planu ustawia `In Progress`
   (Faza 1b); na końcu triażuje recenzje (Gemini, Spark, Sol, bramka Astry),
   prowadzi bramę potwierdzenia, robi commit/push i statusy końcowe (MCP do
   ADO mają też Spark i Gemini; Figmę — Claude i Codex).

**Sesja główna nie pisze kodu, nie pisze testów, nie przepisuje po wykonawcy
i nie czyta dwudziestu plików „żeby sprawdzić"** — każde z tych działań to
brief do właściwej linii. Implementacja wymagająca Opusa (brief wysokiej
stawki albo za trudny dla Sonneta) idzie do nazwanego subagenta
`wykonawca-opus` (opus `xhigh`, od 2026-09-25). Jedyny wyjątek to reguła 11
z globalnego `CLAUDE.md`: jednolinijkowa zmiana, przy której brief kosztuje
więcej niż robota. `max` na Opusie jest po to, żeby decyzje i walidacja były najlepsze
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
  „etap → fala → brief → linia" (z torami pobocznymi — Figma, dokumentacja,
  ADO — przypiętymi do decyzji, od której zależą, nie do końca etapu) plus
  liczba briefów per silnik. Sprawdzian
  przed pokazaniem planu — plan jest zroutowany źle, gdy zachodzi cokolwiek
  z: brief wysokiej stawki (lista w Fazie 4b) nie idzie na `wykonawca-opus`;
  ekran z Figmy idzie na kogokolwiek poza `wykonawca` / `wykonawca-opus`;
  Spark albo Gemini dostały cokolwiek zależnego od Figmy; Gemini dostała
  brief wysokiej stawki albo research; Codex ma w planie implementację albo
  coś poza trudnym researchem, recenzją zastępczą i bramką końcową Astry;
  recenzent któregoś etapu jest z tej samej rodziny co autor diffu.
  Popraw, zanim go pokażesz.
  Nie prosisz o odczyt `/usage` — kolejność Claude → Spark → Codex jest
  stała, a linia zmienia się dopiero po komunikacie o limicie z silnika.
- **Bramka końcowa Astry** — plan mówi wprost, czy feature jest wysokiej
  stawki (lista w Fazie 4b), i jeśli tak, przewiduje jedną recenzję Astry
  `max` całego diffu po recenzjach etapów.
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
4. **Marker zużycia tokenów.** Tuż po batchu ADO uruchom
   `python $env:USERPROFILE\.claude\bin\token-report.py start --task <numer PBI/Buga> --title "<tytuł work itemu>"`
   (PowerShell). Marker w `~/.claude/worker-status/tasks/<numer>.json`
   wyznacza początek liczenia i listę sesji Claude'a; przy wznowieniu
   zadania w nowej sesji (po `/clear`, w nowym oknie) wywołaj to samo
   polecenie ponownie — dopisze bieżącą sesję, nie zresetuje startu.
   Bez markera raport z Fazy 6 nie ma czego policzyć.

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
2. **Dzielisz na fale i dysponujesz** — briefy fali o rozłącznych zbiorach
   plików wysyłasz naraz w jednej wiadomości, każde na linię z tabeli
   poniżej; fala zależna od plików poprzedniej startuje dopiero po jej
   walidacji. Każdy brief dostaje pełną
   specyfikację plus właściwe sekcje CLAUDE.md, klauzulę "jeśli premisa w tej
   specyfikacji jest błędna, ZATRZYMAJ SIĘ i zgłoś zamiast wykonywać
   dosłownie" oraz wymaganą sekcję raportu "Co uważasz za błędne w tej
   specyfikacji?".
3. **Walidujesz raz na falę** — nigdy na słowo wykonawcy. Dowodem zamykającym
   zadanie jest diff, lint, testy, build, zrzut ekranu — nie deklaracja
   sukcesu.
4. **Zlecasz recenzję** niezależnemu recenzentowi (Faza 4b) — zanim zgłosisz
   gotowość do bramy potwierdzenia.

**Tory poboczne równolegle** (decyzja użytkownika 2026-09-25, reguła 14
globalnego `CLAUDE.md`). Gdy decyzja jest ustalona — w kodzie albo w planie —
prace pochodne ruszają naraz, w jednej wiadomości, a nie jedna po drugiej
po kodzie:

- **makiety w Figmie** → `wykonawca` (ma Figma MCP; Spark i Gemini nie);
- **dokumentacja produktowa** (`d:\projects\DTCode\Dokumentacja\Zebrani`,
  osobne repo, własny `AGENTS.md`, `status` w front matter) → Spark albo
  Gemini;
- **ADO** (nowe taski, komentarze, opisy) → Ty sam albo wykonawca z MCP ADO
  przy większej porcji;
- **briefy kolejnej fali**, które od tej decyzji zależą.

Czekają wyłącznie na decyzję, którą odzwierciedlają — nie na koniec etapu
ani na siebie nawzajem. Warunek jak w fali: rozłączne cele (inne pliki, inne
strony i ramki Figmy, inne work itemy). Brama potwierdzenia (Faza 5) nadal
wstrzymuje domknięcie — commit, push i statusy końcowe idą dopiero po niej.
Dwa znane ograniczenia współbieżności: Playwright MCP to jedna karta dla
wszystkich agentów (brief każe otworzyć własną kartę i sprawdzić
`location.href` przed każdym zrzutem), a równoległa przebudowa jednej sekcji
Figmy zostawia plik widocznie rozbebeszony — uprzedź o tym jednym zdaniem,
gdy użytkownik ogląda plik na żywo.

Dobór linii do zadania (pełna tabela z effortami, progami ciśnienia
i uzasadnieniem liczbowym: globalny `~/.claude/CLAUDE.md`; ta tabela jest jej
zastosowaniem do tego skilla; mechanika wywołań Sparka, Codexa i Gemini —
komendy, `-Access`, szablony briefów: skill `external-workers`). **Kolejność
Claude → Spark → Codex, wg rodzaju pracy, nie wg procentów.** Plan etapu
dzieli briefy na **fale** o rozłącznych zbiorach plików (reguła 14, próba od
2026-09-24): briefy wysokiej stawki i za trudne dla Sonneta → agent
`wykonawca-opus` (także ich ekrany z Figmy); pozostałe ekrany z Figmy
i briefy z kontekstem sesji → wyłącznie agent `wykonawca` (Sonnet nie
oddaje pracy — największa pula); resztę rozkładasz na Sonneta, Sparka
i Gemini tak, żeby żadna linia nie stała. W fali briefy idą naraz
(subagenci Claude'a w tle + wrapper w tle), każdy osobnym wywołaniem
wrappera (nie `Start-Job`), z zakazem gita zmieniającego stan i `npm
install` w briefie; wykonawca w fali sprawdza tylko własne pliki (`npx
--no-install eslint <pliki>`, `npx --no-install prettier --check <pliki>`,
`ng test --include <spec>`) i nigdy nie uruchamia `npm run lint:fix`,
`npm run format`, `npm run build` ani — przy > 1 wykonawcy BE w fali —
`dotnet build` / `dotnet test`; brief Sonneta i Opusa mówi to wprost
(nadpisuje „Finishing Every Implementation"). **Spark** (`xhigh` ciężkie /
`high` lekkie) dostaje każdy brief bez Figmy i spoza wysokiej stawki — od
2026-09-24 z `-Access write` (domyślnie) ma Node z Windows przez interop
(pętla lint/test na własnych plikach) oraz MCP ADO, Playwright, Angular,
QA Sphere, Mikrus. **Gemini** (`agy`, `gemini-3.8-flash-high`, `-Access
write`) to wykonawca w fali od 2026-09-24 (zostaje — nigdy wysokiej stawki
ani Figmy); pojedynczy drobiazg → `mechanik`.
**Codex w planie etapu to tylko trudny research i bramka końcowa Astry**
(Sol recenzuje wyłącznie, gdy właściwy recenzent ma limit) — Sol i Luna
implementują wyłącznie jako przelew po komunikacie o limicie z Claude'a
albo Sparka. Tańszy token GPT-6 niczego tu nie zmienia: widełki Codexa
(Sol 15–150 wiadomości / 5 h) są nadal najmniejsze w łańcuchu. Research —
rutynowy i trudny — idzie na Sola (`medium` / `high`, brief bez poleceń
powłoki); recenzje diffów: Sonneta, Opusa i Codexa z przelewu na Sparka,
Sparka na Gemini (reguła 13, stan po rozstrzygnięciu z 2026-09-23);
audyt SCSS na Sparka (próba trwa). O `/usage` nie prosisz — sygnałem jest
wyłącznie komunikat o limicie.

| Zadanie w planie                                                                                                                                                                                                                                                                                                                                                                                                                      | Linia                                                                                                            |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| decyzje, brief, WCAG/tokeny, walidacja dowodów, triaż recenzji, domknięcie ADO                                                                                                                                                                                                                                                                                                                                                        | **sesja główna — Opus `max`** (mózg operacji; nigdy nie pisze kodu ani testów — implementacja na poziomie Opusa idzie do `wykonawca-opus`) |
| **brief wysokiej stawki** (uwierzytelnianie i sesja, płatności Stripe, PIN sprzedawcy, migracje danych, naliczanie pieczątek i nagród, jednorazowe kody, limity prób — także ich ekrany z Figmy) albo **za trudny dla Sonneta** (współbieżność, niezmienniki bezpieczeństwa, logika przekrojowa z cichym błędem) — nie wolumen                                                                                                                                                                                                                                                                                  | agent **`wykonawca-opus`** (Opus `xhigh`, od 2026-09-25); diff recenzuje Spark                                   |
| **pozostałe ekrany z makiet Figmy i briefy z kontekstem sesji** (feature z dowodem w przeglądarce, ADO, Playwright, pętla lint/test/build u wykonawcy) — **wyłącznie ta linia**; do tego swoja część pozostałych briefów fali — bez limitu wielkości; w BE czyta `.claude/CLAUDE.md` (kopia `AGENTS.md`)                                                                                                                                                                                                                                                                               | agent **`wykonawca`** (Sonnet `high`) — największa pula, pracy nie oddaje                                       |
| **każdy brief bez Figmy i spoza wysokiej stawki**, ciężki czy lekki. Ciężkie: slice BE w C#, infrastruktura FE (guardy, trasy, interceptory, DTO, store), refaktor przekrojowy, hoisting, audyt (1M). Lekkie: ≤ 5 plików, klucze i18n hurtem, masówka > 10 plików. Od 2026-09-24 z `-Access write` (domyślnie): Node z Windows przez interop (pętla lint/test na własnych plikach) oraz MCP ADO, Playwright, Angular, QA Sphere, Mikrus. **Bez limitu slotów, w fali równolegle** (rozłączne pliki, zakaz gita zmieniającego stan i `npm install` w briefie, osobne wywołania wrappera w tle) | **Spark** `xhigh` (ciężkie) / `high` (lekkie wg gotowej spec)                                                    |
| **wykonawca w fali** (od 2026-09-24, zostaje) — briefy tekstowe spoza wysokiej stawki, z zapisem i pętlą lint/test natywnie na Windows oraz MCP ADO, Playwright, Angular, QA Sphere, Mikrus; **nigdy brief wysokiej stawki, nigdy Figma** (OAuth nierozwiązany); brief: ścieżki bezwzględne, `AGENTS.md` do przeczytania wprost, szablony w `external-workers`                                                                                                                                                                                                                              | **Gemini** `agy`, `gemini-3.8-flash-high`, `-Access write`                                                       |
| **przelew awaryjny** — wyłącznie po komunikacie o limicie z Claude'a albo Sparka, nigdy w planie etapu; porcje ≤ 5 plików                                                                                                                                                                                                                                                                                                             | **Codex** `gpt-6-sol` `high` (ciężkie) / `gpt-6-luna` `xhigh` (lekkie, masówka)                                   |
| speci Vitest / AXE / xunit; czerwony test do Buga                                                                                                                                                                                                                                                                                                                                                                                     | agent **`tester`** (Sonnet `medium`)                                                                             |
| klucz i18n × 2, rename, przeniesienie pliku — pojedynczo; masówka w porcjach, gdy Spark zgłosił limit                                                                                                                                                                                                                                                                                                                                                                              | agent **`mechanik`** (Haiku `low`)                                                                               |
| fakty z repo przed decyzją                                                                                                                                                                                                                                                                                                                                                                                                            | agent **`zwiadowca`** (Haiku `low`, tylko odczyt)                                                                |
| delegowany audyt kontrastu / fokusu / tokenów                                                                                                                                                                                                                                                                                                                                                                                         | agent **`audytor-a11y`** (Opus `high`)                                                                           |
| recenzja diffu etapu — **kod Sparka** (etap mieszany: po zbiorach plików)                                                                                                                                                                                                                                                                                                                                                                            | **Gemini** `gemini-3.8-flash-high`, `-Access read` (szablon w `external-workers`)                                 |
| recenzja diffu etapu — **kod Sonneta, Opusa (`wykonawca-opus`), Codexa z przelewu albo Gemini** (etap mieszany: po zbiorach plików)                                                                                                                                                                                                                                                                                                    | **Spark** `xhigh`, `-Access read`, brief tylko do odczytu (szablon w `external-workers`)                         |
| recenzja zastępcza — wyłącznie gdy właściwy recenzent ma limit                                                                                                                                                                                                                                                                                                                                                                       | **Codex** `-Mode review`, `gpt-6-sol` `high`                                                                      |
| bramka końcowa feature'a wysokiej stawki — **1 na feature**, po recenzjach etapów (Faza 4b)                                                                                                                                                                                                                                                                                                                                           | **Codex** `-Mode review`, `gpt-6-astra` `max`                                                                    |
| research rutynowy — trendy UI/UX, weryfikacja API biblioteki (Faza 1); brief bez poleceń powłoki                                                                                                                                                                                                                                                                                                                                     | **Codex** `gpt-6-sol` `medium`                                                                                   |
| research trudny — portal za JS-em (EUR-Lex, ISAP) albo źródło, do którego research rutynowy nie dotarł                                                                                                                                                                                                                                                                                                                               | **Codex** `gpt-6-sol` `high`                                                                                     |
| audyt SCSS przed bramą (Faza 4)                                                                                                                                                                                                                                                                                                                                                                                                       | **Spark** `xhigh`, tylko odczyt — próba trwa                                                                     |

Przykład dla planu o 4 etapach, każdy z FE + BE: etap 0 — fale: fala 1:
infrastruktura FE Spark, slice BE Gemini, ekran z makiet Sonnet; fala 2 po
walidacji fali 1. Etap 1 — FE z makiet Sonnet, BE Spark, klucze i18n Gemini;
etap 2 — hoisting komponentu Spark, ekrany Sonnet, BE Gemini; etap 3 — BE
Spark, FE Sonnet. Brief wysokiej stawki (np. naliczanie pieczątek) idzie do
`wykonawca-opus`, także jego ekran z Figmy. Diffy Sparka recenzuje Gemini,
diffy Sonneta i Opusa — Spark; Sol recenzuje wyłącznie, gdy właściwy
recenzent ma limit; przy feature'ze wysokiej stawki jedną bramkę Astry na
końcu — zero implementacji na Codexie w planie. Claude niesie ekrany
(ma Figma MCP i pętlę lint/test/build); resztę briefów fali rozkładasz na
Sonneta, Sparka i Gemini tak, żeby żadna linia nie stała — briefy jednej
fali równolegle, o rozłącznych zbiorach plików — a Ty walidujesz raz na
falę (diff, lint, format, testy, build) z rezerwą na 2–3 korekty, potem
recenzje krzyżowe. Najwyżej ~4 briefy z pętlą testów naraz, do ~10 briefów
na falę. Ocena po 3 etapach: czas etapu, poprawki po walidacji fali
i defekty z recenzji — per silnik-autor, na brief; gdy briefy Gemini
wymagają więcej poprawek niż Sparka i Sonneta, przedstawiasz to
użytkownikowi, zamiast samemu zdejmować linię. Trzy plany, które były
zroutowane błędnie:
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
  o limicie z silnika (rate-limit w sesji, błąd wrappera, trzykrotny 503
  u Gemini) — reguła ciśnienia: Spark zgłasza limit → jego briefy na Sonneta
  albo `mechanik`a w porcjach; Claude zgłasza limit → briefy tekstowe na
  Sparka, briefy `wykonawca-opus` na Sparka `xhigh` (nigdy na Gemini), a te
  z Figmą — jak pozostałe z Figmą — na Sola `high` w porcjach ≤ 5 plików
  (z linkami do makiet zamiast MCP), testy i mechanika na Lunę `xhigh`;
  oba zgłaszają limit → Sol `medium` w porcjach ≤ 5 plików; Codex zgłasza
  limit → trudny research i bramka Astry czekają; Gemini zgłasza limit →
  jego briefy wykonawcze na Sonneta albo Sparka, recenzje kodu Sparka na
  Sola `high`. Zmianę linii meldujesz jednym zdaniem; gdy limit puści,
  wracasz do podziału z tabeli. „Codex, bo czyta AGENTS.md" (Claude też
  czyta — kopię w `.claude/CLAUDE.md`), „Luna, bo tania" i „Sol, bo od GPT-6
  kosztuje tyle co Terra" to fałszywe uzasadnienia.
- **Brief dla Sparka nie może wymagać transkrypcji makiet.** Spark nie ma
  Figma MCP (dopiero po `muse mcp login figma` — do tego czasu makiet mu nie
  przepisujesz), Gemini nie ma go wcale — dostają wyłącznie zadania opisane
  w całości tekstem (nazwy, sygnatury, reguły). Ekran z makiet zawsze idzie
  do `wykonawca` (Sonnet) albo — przy wysokiej stawce lub zadaniu za trudnym
  dla Sonneta — do `wykonawca-opus`: sam pobiera `get_design_context`, sam
  kręci pętlę lint/test/build. Przepisywanie 16 ramek do briefu, żeby tani
  silnik pisał na ślepo, to najdroższy sposób wydania Opusa.
- **Start każdego subagenta Claude'a to ~58 k tokenów promptu.** Drobiazgi
  (kilka kluczy i18n, dwa rename'y) idą w jednym briefie do jednego
  `mechanik`a, nie w pięciu wywołaniach.
- **„Astra zawsze, byle na niższym effortcie" to fałszywa oszczędność.**
  Ok. 80 % kosztu recenzji to czytanie kodu (wejście po cenie Astry, 5×
  Sola), reasoning ~9 % — Astra `low` (Intelligence Index 45,8) daje poziom
  Sparka `xhigh` (45,1) za cenę Astry. Jedna recenzja Astry `max` całego
  PBI #2137 zjadła 66 pkt okna 5 h i 10 % tygodnia Codexa; dlatego raz na
  feature, na końcu, nie na etap.
- **Recenzent z tej samej rodziny co autor to nie recenzja.** Spark nie
  recenzuje kodu Sparka, Gemini — kodu Gemini, Sol — kodu Codexa, a Fable
  nie recenzuje wcale (rodzina Sonneta i Opusa). Sol nie dubluje właściwych
  recenzentów równolegle — recenzuje wyłącznie, gdy właściwy recenzent ma
  limit. Obaj stali recenzenci (Spark, Gemini) produkują fałszywe P0/P1,
  więc brief recenzenta wymaga sprawdzenia scenariusza P0/P1 przed
  zgłoszeniem, a Ty obalasz każde P0/P1 jednym poleceniem przed poprawką.

## Faza 3 — Implementacja etapu (linie wykonują, sesja główna waliduje)

Implementację wykonują linie z Fazy 2 wg briefów — **sesja główna nie pisze
kodu**. Jej robota w tej fazie to walidacja dowodów raz na falę: diff,
`npm run lint` / `npm test` / `npm run build` (FE) albo `dotnet build` /
`dotnet test` (BE), zrzuty 2×2 (360×530 i 1280×720, Light i Dark). Dowód
w przeglądarce (Playwright) dostarcza każdy wykonawca z `-Access write`
(`wykonawca`, `wykonawca-opus`, Spark albo Gemini) albo Codex na przelewie;
po briefie wykonawcy całą weryfikację robisz Ty, z rezerwą na 2–3 drobne
korekty.

Gdy coś wizualnego po korekcie nadal wygląda źle albo jest tylko przybliżone
„na oko" (np. odstęp liczony z tokenu paddingu zamiast z realnego renderu),
**nie zlecasz kolejnej rundy poprawek na oko** — zlecasz research właściwej
techniki (Sol `medium`; trudny — Sol `high`) i dopiero potem brief korekty
z konkretną metodą.

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
2. **Dopiero potem łatka — osobny brief na linię wg Fazy 2** (wysoka
   stawka → `wykonawca-opus`; ekran z Figmy albo MCP → `wykonawca`; spec
   tekstowa → Spark albo Gemini w fali) **— z zakazem edycji pliku testu.**
   Zmienia się kod produkcyjny,
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

Zanim zgłosisz zadanie jako gotowe do mojej akceptacji, zlecasz **Sparkowi**
(`xhigh`, tylko odczyt — próba trwa, 1 przebieg bez pominiętego pliku)
przegląd **wszystkich zmodyfikowanych plików SCSS** wg poniższych kryteriów
(brief: lista plików
z `git diff --name-only` — Spark nie uruchamia gita, listę dajesz Ty —
kryteria dosłownie, zakaz modyfikacji plików, raport „co zastąpić / co
wydzielić / co zostawić i dlaczego" na stdout; po przebiegu `git status`).
Gdy raport pominie plik z listy, audyt wraca na `wykonawca`. Decyzję
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

## Faza 4b — Recenzja niezależna (przed bramą)

Autor nie recenzuje sam siebie: po samoaudycie SCSS, a **przed**
zgłoszeniem gotowości, zlecasz przegląd niescommitowanego diffu etapu
recenzentowi **z innej rodziny modeli niż autor diffu** (reguła 13
globalnego `CLAUDE.md`):

| Autor diffu                                                        | Recenzent                                              |
| ------------------------------------------------------------------ | ------------------------------------------------------ |
| Spark                                                              | Gemini `gemini-3.8-flash-high`, `-Access read`         |
| Sonnet (`wykonawca`), Opus (`wykonawca-opus`), Codex z przelewu, Gemini | Spark `xhigh`, `-Access read`, brief tylko do odczytu |
| właściwy recenzent ma limit                                        | Sol `high` (`codex exec review`) — wyłącznie wtedy     |
| cały feature wysokiej stawki                                       | dodatkowo bramka końcowa Astry `max` (niżej)           |

Fable nie recenzuje — ta sama rodzina co Sonnet i Opus. Etap mieszany →
recenzje po zbiorach plików (Gemini dostaje pliki Sparka, Spark — pliki
Sonneta/Opusa). Liczby recenzji w etapie nie limitujesz. Brief recenzenta
wymaga sprawdzenia scenariusza każdego P0/P1 przed zgłoszeniem, a Ty
obalasz każde P0/P1 jednym poleceniem przed poprawką.

**Sol:**

```powershell
$env:USERPROFILE\.claude\bin\worker-run.ps1 `
  -Engine codex -Mode review `
  -Repo D:\projects\DTCode\ZebraniFE `
  -Model gpt-6-sol -Effort high `
  -Title "Recenzja PBI #<numer>"
```

(bez `-BriefFile` wrapper sam dokleja `--uncommitted`; dla ZebraniBE `-Repo`
wskazuje na to repo). Sol recenzuje wyłącznie, gdy właściwy recenzent ma
limit; `high` jest tu świadomym wydatkiem — recenzja to praca, w której
reasoning znajduje to, czego `medium` nie widzi — a nie darmowym dodatkiem:
waga wiadomości Codexa rośnie z effortem. Etap mieszany przy recenzji
zastępczej: Sol dostaje `-BriefFile` z listą plików danego autora jako
instrukcją przeglądu (wtedy wrapper nie dokleja `--uncommitted`).

**Spark:** wrapper nie ma dla niego trybu `review`, a Spark nie uruchamia
gita — diff plików Sonneta/Opusa/Codexa/Gemini (`git diff HEAD -- <pliki>`)
i listę nowych plików wklejasz do briefu wg szablonu „Recenzja przez Sparka"
z `external-workers`; `-Repo` to repozytorium, więc Spark czyta `AGENTS.md`
i dowolne pliki dla kontekstu. Po przebiegu `git status` — recenzja niczego
nie zmienia.

**Gemini:** `worker-run.ps1 -Engine gemini` (model domyślny
`gemini-3.8-flash-high`), z `-Access read`, brief wg szablonu „Recenzja
przez Gemini" z `external-workers`: diff plików Sparka wklejony do briefu,
**wszystkie ścieżki bezwzględne**, `AGENTS.md` wskazany do przeczytania
wprost (w trybie bez interfejsu nie ładuje się sam), zakaz poleceń powłoki.
Uprawnienia Antigravity dopuszczają tylko odczyt `D:\projects\DTCode`
i stron WWW, więc recenzja z definicji niczego nie zmienia.

**Stan po rozstrzygnięciu z 2026-09-23** (3 etapy: PBI #2282 + DomSztukiFE
×2): Spark przejął diffy Sonneta i Codexa, Gemini — diffy Sparka; Sol ich
nie dubluje (zostaje trudny research, bramka Astry i przelew).

**Bramka końcowa Astry — raz na feature wysokiej stawki.** Gdy feature
dotyka uwierzytelniania i sesji, płatności (Stripe), PIN-u sprzedawcy,
migracji danych, naliczania pieczątek i nagród, jednorazowych kodów albo
limitów prób, **po** recenzjach etapów i ich poprawkach, a przed bramą
potwierdzenia, zlecasz jedną recenzję całego niescommitowanego diffu
feature'a (ta sama komenda, `-Model gpt-6-astra -Effort max`,
`-Title "Bramka Astra PBI #<numer>"`). Astra **uzupełnia** recenzje etapów,
nigdy ich nie zastępuje. Wyłącznie `max`: ~80 % kosztu recenzji to czytanie
kodu, więc niższy effort daje cenę Astry bez jej przewagi (Astra `low` ≈
Spark `xhigh` w Intelligence Index). Koszt jest realny — bramka całego
PBI #2137 zjadła 66 pkt okna 5 h i 10 % tygodnia Codexa — i się opłacił:
po dwóch recenzjach Sola znalazła pięć realnych defektów (podwójny POST,
pominięte odświeżenie kart, `retryAfterSeconds` poza zakresem, zawieszone
żądanie po błędzie ładowania nakładki, brak sprawdzenia roli klienta).
Znaleziska triażujesz razem z recenzjami etapów; w raporcie przed bramą
zaznaczasz, co znalazła tylko Astra. Kryterium stawki wpisujesz do planu
(Faza 1), nie decydujesz o nim po fakcie.

Co robisz z wynikiem — **triaż, nie posłuszeństwo** (skill
`superpowers:receiving-code-review` obowiązuje):

1. Każde znalezisko klasyfikujesz: **defekt** (naprawić), **sporne**
   (rozstrzygasz Ty, z uzasadnieniem w raporcie), **fałszywy alarm** (recenzent
   nie zna konwencji repo — np. zgłasza brak `standalone: true`, `p-button`
   zamiast `[pButton]`, Cream zamiast białego jako „błąd"). Fałszywe alarmy
   wypisujesz z jednym zdaniem dlaczego; nie naprawiasz ich.
2. Defekty wracają **do tej samej linii, która pisała kod** (Spark do
   Sparka, Gemini do Gemini, `wykonawca` do `wykonawcy`, `wykonawca-opus`
   do `wykonawca-opus`) jako brief korekty — nie łatasz sam. Wyjątek: linia
   zgłosiła limit → korekta wg reguły ciśnienia (Spark → `wykonawca`;
   Gemini → Sonnet albo Spark).
3. Po korekcie **nie zlecasz drugiej recenzji** — weryfikujesz poprawkę
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
7. **Raport zużycia tokenów — ostatnia rzecz w komunikacie końcowym.**
   Uruchom `python $env:USERPROFILE\.claude\bin\token-report.py report --task <numer>`
   i wklej obie tabele bez zmian (per silnik → per model → sumy; szczegóły
   per rola/brief) wraz ze stopką. Raport liczy z zapisów na dysku
   (transkrypty Claude'a, rollouty Codexa, sesje muse) — nie szacuj, nie
   pytaj o `/usage`. Ostrzeżenia `⚠` z raportu przepisz dosłownie. Sumy
   pokazują kolumny cache osobno: surowa suma jest w większości odczytem
   cache'u i bez podziału nic nie mówi o koszcie.
