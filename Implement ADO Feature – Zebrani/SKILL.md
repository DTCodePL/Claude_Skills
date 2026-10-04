---
name: implement-ado-feature-zebrani
description: >
  Planowanie i pełna implementacja feature'a / PBI / taska Zebrani.pl na
  podstawie linku lub numeru Azure DevOps — od Plan Mode z makietami Figmy,
  przez rozłączne fale wykonania, audyt i niezależną recenzję po każdej fali,
  aż po bramę potwierdzenia i domknięcie w ADO. Claude Opus xhigh pozostaje
  architektem, dyspozytorem i walidatorem w pilotażu; sesja główna nie pisze
  kodu ani testów. Dla każdego briefu najpierw kwalifikuje pary model–native
  effort według twardych ograniczeń, potem wybiera wykonawcę i recenzenta
  na podstawie lokalnych wyników, przewidywanych korekt, czasu do akceptacji
  i wiarygodnego sygnału dostępności. Codex jest pełnoprawnym kandydatem
  bez czekania na limit innej linii. Zachowuje ograniczenia high-stakes,
  dostęp do Figmy, reguły skilli pomocniczych, niezależność rodziny recenzenta
  i końcową bramkę Astra/Sol. Na starcie, po zatwierdzeniu planu, PBI/Bug
  i taski do wykonania idą na In Progress. Obejmuje też Bugi — test-first:
  czerwony test, łatka, ten sam test zielony. UŻYWAJ ZAWSZE, gdy user
  poda link lub numer Epic/Feature/PBI/Task/Bug z Azure DevOps projektu
  Zebrani.pl i poprosi o zaplanowanie, zaimplementowanie i/lub naprawienie go
  — nawet jeśli nie padnie słowo "skill".
version: '5.16'
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
Loader (wzorzec: `implement-ado-feature-loader Zebrani.md`) jest celowo
**neutralny silnikowo** — nie wymienia silników, modeli ani effortów, bo jego
streszczenie routingu rozjeżdżało się z tym plikiem przy każdej zmianie
(2026-09-28: loader w ZebraniFE wciąż mówił „Opus `max`”, „Gemini do
researchu”, „Codex recenzuje Sparka” i nie znał `wykonawca-opus`). Zmiana
routingu = ten plik + globalny `~/.claude/CLAUDE.md`; loadera nie ruszasz.
Skill zakłada, że w repo projektu obowiązuje `.claude/CLAUDE.md` (w ZebraniBE
kopia jako `AGENTS.md`) — nie duplikuj jego zasad w brifach dla subagentów,
tylko cytuj/linkuj właściwą sekcję ("a subagent does not inherit project
rules by osmosis").

## Rola sesji głównej — mózg operacji

**Sesja główna to Claude Opus na efforcie `xhigh` (od 2026-09-28). Jest architektem, dyspozytorem
i walidatorem — i niczym więcej.** Przez cały cykl (plan → etapy → recenzja →
brama → ADO) robi wyłącznie cztery rzeczy:

1. **Projektuje** — czyta ADO, dokumentację i makiety, podejmuje każdą decyzję
   (adresy, nazwy, kształt API, tokeny, przypadki brzegowe) i zapisuje je w
   planie oraz w briefach. Fakty z repo zbiera dla niej `zwiadowca`.
2. **Dysponuje** — dzieli etap na fale briefów o rozłącznych zbiorach
   plików (reguła 14), kwalifikuje pary model–native effort i wybiera
   wykonawcę oraz recenzenta per brief wg Faz 1–2; wysyła niezależne briefy
   fali naraz w jednej wiadomości
   (subagenci Claude'a w tle + wrapper w tle) — razem z torami pobocznymi
   (Figma, dokumentacja, ADO, briefy kolejnej fali), gdy tylko decyzja,
   od której zależą, jest ustalona (Faza 2, „Tory poboczne").
3. **Waliduje raz na falę** — czyta diff, uruchamia lint/test/build
   i `browser-check` (zrzuty 2×2, przejścia scenariusza), ogląda zrzuty,
   odsyła korekty do tej samej linii. Raport wykonawcy nigdy nie
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
więcej niż robota. `xhigh` sesji (od 2026-09-28 — `max` to przerost formy nad
treścią) jest po to, żeby decyzje i walidacja były najlepsze w całym łańcuchu
— nie po to, żeby tym effortem pisać komponenty.

## Dokumentacja produktowa — źródło prawdy, nigdy pomijana

Dokumentacja produktowa (`d:\projects\DTCode\Dokumentacja\Zebrani`) jest
**źródłem prawdy (SoT)** zachowania, napisów, reguł biznesowych i decyzji
Zebrani.pl. Kod, testy, przypadki QA Sphere i makiety idą za nią — nigdy
odwrotnie. **Nie wolno o niej zapomnieć ani jej pominąć w żadnym zadaniu**,
także w refaktorze i w Bugu:

- **Faza 1** — plan ma obowiązkowy punkt „Dokumentacja”: dokumenty, z których
  wynika zakres (id, ścieżka, `status`), i każda zmiana dokumentacji, której
  zadanie wymaga — albo wprost „bez zmian” z uzasadnieniem. Plan bez tego
  punktu jest niekompletny.
- **Fazy 2–4** — każda decyzja, która zmienia zachowanie, napis albo regułę
  albo rozstrzyga coś, czego dokument nie mówi, trafia do dokumentacji w tym
  samym zadaniu (tor poboczny tej samej fali). Dokument `zatwierdzony`
  zmieniasz datowaną rewizją zatwierdzoną przez właściciela. Zachowanie
  zastane w kodzie, którego dokument nie opisuje albo któremu przeczy,
  dopisujesz tak samo albo zgłaszasz właścicielowi do rozstrzygnięcia —
  nigdy nie przemilczasz.
- **Faza 5** — raport bramy ma punkt „Dokumentacja”: co zmieniono (plik,
  sekcja) albo dlaczego bez zmian.
- **Faza 6** — dokumentacja idzie commitem do repo `Dokumentacja` razem
  z kodem, z numerem PBI/Buga w gałęzi i w commicie. **Zadanie
  z nieaktualną dokumentacją nie jest skończone** — nie zamykasz go w ADO.

## Faza 1 — Plan (Plan Mode, po polsku)

Zanim zlecisz jakikolwiek kod, wejdź w Plan Mode i ustal:

- **Dokumentacja (źródło prawdy)** — punkt obowiązkowy planu, patrz sekcja
  „Dokumentacja produktowa — źródło prawdy, nigdy pomijana”.
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
- **Klasyfikacja każdego briefu przed doborem**, także recenzenckiego:
  stawka i skutki błędu (w tym lista high-stakes z Fazy 4b oraz pliki niosące
  niezmiennik); niepewność/nowość; zależności, zakres plików i wpływ przekrojowy;
  potrzebne narzędzia, uprawnienia i kontekst (Figma, repo FE/BE, Playwright,
  QA Sphere, kontekst sesji); dostępny **test oracle** (test jednostkowy,
  integracyjny, przegląd w przeglądarce, PRE lub inny dowód) i **dowody odbioru**
  wraz z kryteriami ukończenia. Niewiadoma dotycząca produktu, API,
  bezpieczeństwa, danych lub kryterium odbioru pozostaje pytaniem do
  właściciela; wykonawca nie rozstrzyga jej sam.
- **Dobór per brief w dwóch krokach**, opisany w Fazie 2: eliminacja
  niekwalifikujących się par według twardych ograniczeń, potem wybór
  najlepszej dopuszczonej pary na podstawie dowodów. Plan zawiera tabelę
  „etap → fala → brief → linia” z torami pobocznymi (Figma, dokumentacja, ADO)
  przypiętymi do decyzji, od której zależą. Dla wykonawcy **i recenzenta**
  zapisujesz dokładny **model + native effort**, krótkie uzasadnienie,
  **pewność** (`wysoka / średnia / niska`), **dopuszczone alternatywy**
  (linia/model/native effort, albo jawnie brak) i **status dostępności**
  (`znany / ostrzegawczy / zablokowany / nieznany`) ze źródłem i czasem
  odczytu sygnału. Brak lokalnych wyników podobnego briefu oznacza niską
  pewność. Nazwy effortów różnych dostawców nie oznaczają równoważnej jakości.
  Liczba briefów per linia to bilans obciążenia, nie kryterium poprawności.
- **Kontrola planu przed pokazaniem**: żaden wybór nie omija high-stakes,
  faktycznego dostępu do Figmy/narzędzi, uprawnień, jednej warstwy na brief,
  rozłączności celów fali, niezależności rodziny recenzenta ani ograniczeń
  skilli pomocniczych. Codex może dostać kwalifikującą się implementację
  już w planie. Nie dyskwalifikujesz planu na podstawie samej kategorii
  zadania ani proporcji przydziałów.
- **Dostępność bez zgadywania**: nie prosisz o `/usage`; hook
  `~/.claude/bin/limity-hook.mjs` dostarcza sygnały Claude'a, a wrappery
  rzeczywiste komunikaty limitu innych linii. Nie szacujesz procentu limitu
  na podstawie braku danych ani historii przydziałów. Blokada lub rzeczywiste
  niepowodzenie wymaga ponownej kwalifikacji wg Fazy 2, nie stałego fallbacku.
- **Bramka końcowa Astry** — plan mówi wprost, czy feature jest wysokiej
  stawki (lista w Fazie 4b), i jeśli tak, przewiduje jedną recenzję Astry
  `max` całego diffu po recenzjach etapów.
- **Scenariusz weryfikacji w przeglądarce** (`browser-check`, od 5.16):
  plik JSON w scratchpadzie sesji — specyfikacja odbioru, którą piszesz
  w planie jak kryteria akceptacji, nie test w repo produktu (E2E prowadzi
  kto inny); nie zastępuje czerwonego testu Buga z Fazy 3. `matrix`: trasy
  zmienione przez feature × 360×530 i 1280×720 × Light/Dark, z `waitFor`
  na elemencie gotowości. `flows` (opcjonalnie, 2–5 przejść): cel
  nazywający drogę słowami interfejsu (Jev czyta dosłownie), `forbidden`
  dla akcji nieodwracalnych i asercje **efektu** (wartość po zapisie,
  `within` dla elementów powtarzalnych, URL po `pathname`), których stan
  wyjściowy nie spełnia, nie samego komunikatu. `testData` wyłącznie
  syntetyczne — trafia do Jev jawnie (w tekście strony maskowane są tylko
  sekrety, e-maile i telefony; reszta też idzie do Jev).
  Akcje z zapisem w obszarach z listy high-stakes Fazy 4b nie idą do
  `flows` — ich dowodem są testy jednostkowe i integracyjne; w przeglądarce
  co najwyżej ekran bez akcji nieodwracalnej. Feature bez zmian UI:
  scenariusz pomijasz z uzasadnieniem w planie.
- **Gdy work item to Bug**, plan ma dodatkowo wskazać **test, który udowodni
  błąd**: jego rodzaj (spec Vitest / test xunit / Playwright, gdy błąd widać
  tylko w przeglądarce), plik i nazwę, dokładne kroki odtworzenia zamienione
  na asercje oraz oczekiwany wynik po naprawie. Bez tego punktu plan buga jest
  niekompletny — patrz Faza 3, „Bug: test first”.
- **SemVer i dostępność (komentarz z Fazy 6).** Dla każdego zmienionego repo
  aplikacji: wybrany bump (`major` / `minor` / `patch` / `none`),
  jednozdaniowe uzasadnienie z diffa oraz para stare→nowe z podglądu skryptu.
  Numeru nie zgadujesz — arytmetykę liczy skrypt.

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
   plików wysyłasz naraz w jednej wiadomości, każde na linię zakwalifikowaną
   i wybraną dla briefu; fala zależna od plików poprzedniej startuje dopiero
   po jej walidacji i niezależnej recenzji. Każdy brief dostaje pełną
   specyfikację plus właściwe sekcje CLAUDE.md, klauzulę "jeśli premisa w tej
   specyfikacji jest błędna, ZATRZYMAJ SIĘ i zgłoś zamiast wykonywać
   dosłownie" oraz wymaganą sekcję raportu "Co uważasz za błędne w tej
   specyfikacji?".
3. **Walidujesz raz na falę** — nigdy na słowo wykonawcy. Dowodem zamykającym
   zadanie jest diff, lint, testy, build, zrzut ekranu — nie deklaracja
   sukcesu.
4. **Zlecasz recenzję po każdej fali** niezależnemu recenzentowi (Faza 4b)
   z innej rodziny niż autor; architekt odbiera dowody tej fali przed
   rozpoczęciem zależnej. Nie zastępujesz jej okresową oceną routingu.

**Tory poboczne równolegle** (decyzja użytkownika 2026-09-25, reguła 14
globalnego `CLAUDE.md`). Gdy decyzja jest ustalona — w kodzie albo w planie —
prace pochodne ruszają naraz, w jednej wiadomości, a nie jedna po drugiej
po kodzie:

- **makiety w Figmie** → wybrana per brief linia z faktycznym dostępem
  do Figmy (Claude lub Codex po potwierdzeniu dostępu; Spark i Gemini nie);
- **dokumentacja produktowa** (`d:\projects\DTCode\Dokumentacja\Zebrani`,
  osobne repo, własny `AGENTS.md`, `status` w front matter) → linia
  kwalifikująca się do tego briefu; **obowiązkowo przy każdej zmianie
  zachowania, napisu, reguły albo decyzji** — to źródło prawdy, nigdy pomijane;
- **ADO** (nowe taski, komentarze, opisy) → Ty sam; większa porcja to brief
  na wybraną linię z potwierdzonym MCP ADO i właściwymi uprawnieniami;
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

### Dobór modelu i natywnego effortu per brief

Jednostką doboru jest brief, nie numer ani typ work itemu. Globalna matryca
`~/.claude/CLAUDE.md` opisuje możliwości i ograniczenia; nie stanowi stałego
przydziału „rodzaj pracy → model”. Mechanikę wywołań (komendy, `-Access`,
szablony briefów) opisuje `external-workers` — ten skill nie decyduje „kiedy”.

**Krok 1 — kwalifikacja kandydatów.** Na podstawie klasyfikacji z Fazy 1
odrzuć pary model–native effort niespełniające choć jednego twardego warunku:

- high-stakes: pliki niosące niezmiennik (uwierzytelnianie i sesja, płatności
  Stripe, PIN sprzedawcy, migracje danych, naliczanie pieczątek i nagród,
  jednorazowe kody, limity prób) oraz briefy za trudne dla Sonneta
  (współbieżność, niezmienniki bezpieczeństwa, logika przekrojowa z cichym
  błędem) pozostają na `wykonawca-opus` (Opus `xhigh`), nie ze względu
  na wolumen; zachowany wyjątek blokady hooka opisano niżej. Ekrany,
  szablony, style i i18n tych funkcji bez niezmiennika oceniasz osobno.
  Gemini nigdy nie dostaje briefu wysokiej stawki;
- Figma: wykonawca ekranu z makiety sam pobiera kontekst projektu;
  wymagany jest faktyczny dostęp do Figmy. Link lub transkrypcja makiety
  nie zastępuje dostępu. Spark i Gemini nie kwalifikują się do Figmy.
  Próba A/B linii Figmy (`wykonawca` Sonnet 5.5 `high` wobec
  `wykonawca-opus-medium` Opus 5.5 `medium`, reguła 14 globalnego
  `CLAUDE.md`) obejmuje briefy Figmy, które kwalifikacja kieruje do linii
  Claude'a; brief Figmy przydzielony Codexowi nie wchodzi do próby i jej
  nie przerywa — ramię wybierasz dla kolejnego briefu Claude'a. Wyjątek:
  w próbie A/B linii Figmy oba ramiona recenzuje Spark `xhigh` — stały
  recenzent jako kontrola eksperymentu; brief, którego Spark nie
  zrecenzuje, wypada z pomiaru;
- narzędzia, repozytoria, uprawnienia oraz potrzebny kontekst muszą być
  dostępne w wybranej linii; brak dziedziczenia sesji wymaga samodzielnego
  briefu, a brak nieprzenoszalnego kontekstu wyklucza kandydata;
- wykonawca musi móc bezpiecznie zapisywać i weryfikować własne pliki;
  recenzent działa tylko do odczytu, ma kompetencje do stawki i zakresu
  oraz pochodzi z innej rodziny niż autor (Faza 4b). Niezależność końcowej
  bramki Astra/Sol dotyczy plików niosących niezmiennik high-stakes: te
  zawsze pisze `wykonawca-opus` (wyjątek CZERWONEGO: Spark `xhigh`), więc
  bramka z rodziny Codex jest wobec nich niezależna. Codex może pisać
  briefy bez niezmiennika w funkcji high-stakes (ekrany, szablony, style,
  i18n, testy bez niezmiennika); ich niezależność zapewnia recenzja fali
  z rodziny innej niż Codex, a bramka czyta cały diff funkcji, także te
  pliki, ale dla nich nie zastępuje recenzji fali;
- każdy brief obejmuje jedną warstwę; równoległe cele muszą być rozłączne.
  Zakres i test oracle muszą być wykonalne zgodnie z regułami walidacji fali;
- obowiązują ograniczenia skilli pomocniczych. QA Sphere zachowuje własne
  reguły autora, recenzenta i skryptu publikującego `qas.py` — ogólny routing
  ich nie nadpisuje. Fable nadal nie jest recenzentem;
- model oraz natywny effort muszą być obsługiwane w danym narzędziu.
  Agent Claude'a musi być nazwany i nieść jawny effort w definicji;
  nie wolno obchodzić blokady hooka ani podstawiać dziedziczonego effortu.

**Krok 2 — wybór spośród dopuszczonych par.** Architekt wybiera wykonawcę
i recenzenta na podstawie lokalnych wyników podobnych briefów z
`docs/model-routing-evaluation.md` w repo `Claude_Skills`, przewidywanej
liczby/kosztu korekt, czasu do akceptacji i wiarygodnego sygnału dostępności.
Złożoność, niepewność/nowość briefu oraz jego zależności wpływają też na
dobór natywnego effortu.
Codex jest pełnoprawnym kandydatem do kwalifikujących się briefów już
w planie — nie czeka na limit innej linii. Działa jednak na ChatGPT Plus,
czyli najmniejszej puli (bramka Astra `max` na PBI #2137 zjadła ~66 pkt okna
5 h i ~10 % tygodnia): przy każdej kwalifikacji Codexa liczysz zużycie jego
puli (bez długich przebiegów i effortów nieuzasadnionych briefem). Sygnał
puli Codexa jest zwykle `nieznany` (wrapper nie podaje zapasu) — nie
szacujesz procentu z historii ani z ceny. W funkcji high-stakes przy sygnale
`nieznany` Codex dostaje co najwyżej krótkie briefy bez niezmiennika
(≤ 5 plików, effort nie wyższy niż `high`); dłuższe lub cięższe idą do innej
dopuszczonej linii. Po pierwszym komunikacie limitu Codexa przed bramką
(sygnał `zablokowany`) nie przydzielasz mu kolejnych briefów tej funkcji —
bramka ma pierwszeństwo. Wybór nie służy zużyciu wszystkich
limitów ani minimalizacji kosztu pierwszego przebiegu. Przy braku danych
lokalnych utrzymujesz wymagany poziom jakości i ryzyka oraz oznaczasz
pewność jako niską. Nie wymyślasz punktacji, sztywnego progu kosztu ani
rankingu z małej próbki. Publiczny ranking jest pomocniczą wskazówką,
nie rozstrzyga sam i nie może kompensować niespełnionej bramki.

Model i native effort zapisujesz jawnie także dla recenzenta, razem
z uzasadnieniem, pewnością, dopuszczonymi alternatywami i statusem
dostępności. `high`, `xhigh` czy `max` u różnych dostawców nie są
równoważne. W tabeli poniżej opcje effortu to znane konfiguracje danej linii,
nie automatyczna mapa „lekki/ciężki”; przed użyciem potwierdź obsługę
wybranej pary. Brak obsługi eliminuje ją w kroku 1.

**Walidacja wykonawców w fali pozostaje obowiązkowa.** Briefy idą naraz
(subagenci Claude'a w tle + wrapper w tle), każdy osobnym wywołaniem
wrappera (nie `Start-Job`), z zakazem gita zmieniającego stan i `npm install`.
Wykonawca sprawdza tylko własne pliki (`npx --no-install eslint <pliki>`,
`npx --no-install prettier --check <pliki>`, `ng test --include <spec>`)
i nigdy nie uruchamia `npm run lint:fix`, `npm run format`, `npm run build`
ani — przy > 1 wykonawcy BE w fali — `dotnet build` / `dotnet test`.
Brief każdej linii mówi to wprost (dla Sonneta/Opusa nadpisuje „Finishing
Every Implementation”). Architekt uruchamia pełne sprawdzenia po fali;
raport wykonawcy nie zastępuje dowodów.

**Dane zewnętrzne tylko pomocniczo.** Jeśli potrzebne, liczby indeksów
i ceny odczytujesz z API Artificial Analysis:
`GET https://artificialanalysis.ai/api/v2/data/llms/models`, nagłówek
`x-api-key: aa_BfuEueOGzcOvOENaiuiavHwaGvVNhrYK`. Potwierdź, jaki model i native
effort opisuje rekord — brak przyrostka nie dowodzi równoważności effortów.
Koszt zadania indeksu jest na stronie modelu
(`artificialanalysis.ai/models/<slug>`), nie jest kosztem lokalnego briefu.

Brief krótki = tani (reguła 15, od 2026-09-28 — 54–81 % kosztu każdej linii
Claude'a to ponowne czytanie kontekstu przy każdym wywołaniu narzędzia):
jeden brief = jedna warstwa, cel ≤ ~150 wywołań i ≤ ~300 tys. kontekstu
(koszt rośnie mniej więcej z kwadratem długości przebiegu); brief każe
uruchamiać sprawdzenia z cichym wyjściem, a raport wykonawcy jest zwięzły,
bez wklejonego diffu.

### Matryca możliwości i twardych ograniczeń

| Linia / model / znane natywne efforty | Możliwości i dostęp | Twarde ograniczenia w pilotażu |
| --- | --- | --- |
| sesja główna — Claude Opus `xhigh` | plan, decyzje, briefy, WCAG/tokeny, walidacja dowodów, triaż, domknięcie ADO | architekt; nigdy nie pisze kodu ani testów poza istniejącym jednolinijkowym wyjątkiem reguły 11 |
| `wykonawca-opus` — Opus `xhigh` | pliki niosące niezmiennik high-stakes; briefy za trudne dla Sonneta | nie wolumen, ekran, szablon, styl ani i18n bez niezmiennika; obowiązuje hook; rodzina Claude — nie recenzuje Claude'a |
| `wykonawca` — Sonnet 5.5 `high` | Figma MCP, kontekst sesji, repo FE/BE, implementacja; inne narzędzia po potwierdzeniu | jedna warstwa; wymagany faktyczny dostęp; nie przejmuje niezmienników wymagających Opusa; rodzina Claude — nie recenzuje Claude'a |
| `wykonawca-opus-medium` — Opus `medium` | Figma MCP, kontekst sesji; ekrany, szablony, style, i18n bez niezmiennika | wyłącznie ramię B próby A/B linii Figmy (reguła 14 globalnego `CLAUDE.md`); poza próbą wykluczony; nigdy pliki niezmiennika; obowiązuje hook; rodzina Claude — nie recenzuje Claude'a |
| Spark — `muse-spark-1.3-contributor` (`none|minimal|low|medium|high|xhigh|max|ultra`) | `-Access write`: Node z Windows przez interop, pętla własnych testów, MCP ADO, Playwright, Angular, QA Sphere, Mikrus; `-Access read`: audyt i recenzja | brak Figma MCP; high-stakes tylko w zachowanym wyjątku blokady hooka; bez gita i `npm install`; bez limitu slotów, ale rozłączne cele |
| Gemini — `agy`, `gemini-3.8-flash-low`, `gemini-3.8-flash-medium`, `gemini-3.8-flash-high` (effort zakodowany w sufiksie identyfikatora) | zapis i pętla lint/test na Windows oraz MCP ADO, Playwright, Angular, QA Sphere, Mikrus; `-Access read` do recenzji | nigdy high-stakes ani Figma; ścieżki absolutne, jawny odczyt `AGENTS.md`, zakaz powłoki w briefie recenzji zgodnie z `external-workers` |
| Codex — `gpt-6.1-sol` (`low|medium|high|xhigh|max|ultra`), `gpt-6-luna` (`low|medium|high|xhigh|max`) | implementacja, testy, research, audyt/recenzja; Figma i Playwright po potwierdzeniu dostępu w konkretnej sesji; `-Mode review` do odczytu | pełnoprawny kandydat, porcje ≤ 5 plików (implementacja/testy; recenzji nie dzielisz — bramka końcowa czyta cały diff w jednym przebiegu); nie zastępuje Opusa na high-stakes; nie recenzuje własnej rodziny; research bez poleceń powłoki; najmniejsza pula (Plus), sygnał zwykle `nieznany` — w funkcji high-stakes tylko krótkie briefy bez niezmiennika (≤ 5 plików, effort ≤ `high`), po limicie przed bramką brak kolejnych briefów tej funkcji |
| `tester` — Sonnet 5.5 `medium` | speci Vitest / AXE / xunit; czerwony test Buga | test przed łatką i bez edycji przez autora łatki; odrębne briefy testu i łatki |
| `mechanik` — Haiku `low` | pojedyncze klucze i18n, rename, przeniesienie pliku | mechaniczne drobiazgi, nie implementacja wysokiej stawki |
| `zwiadowca` — Haiku `low` | fakty z repo przed decyzją | tylko odczyt |
| `audytor-a11y` — Opus `high` | delegowany audyt kontrastu/fokusu/tokenów | audyt, nie przejęcie implementacji |
| QA Sphere — autor Spark `xhigh`; Gemini `-Access write`, gdy Spark zajęty albo z limitem | plik podglądu wg `qasphere-test-generator` | recenzja: plik Sparka → Gemini `-Access read`, plik Gemini → Spark `-Access read`; publikacja/poprawki/weryfikacja przez architekta skryptem `qas.py`; sesja nie pisze przypadków i nie woła `create_test_case` / `update_test_case` |
| bramka końcowa — `gpt-6-astra` `max` + próba `gpt-6.1-sol` `max` | cały feature high-stakes po recenzjach fal | istniejąca bramka i eksperyment z Fazy 4b; niezależna wobec plików niosących niezmiennik (pisze je Opus); nie zastępują recenzji fal, także dla plików bez niezmiennika pisanych przez Codex |

**Preferencje jakościowe — nie hard gates.** Dotychczasowe wyniki recenzji
Spark/Gemini, researchu Sola i audytu SCSS Sparka są wskazówkami do kroku 2.
Historyczna próba researchu Gemini z 2026-09-24 (raport bez adresów
źródeł) jest negatywnym sygnałem do ponownej oceny per brief — to nie hard
gate i nie oznacza stałego przydziału rutynowego researchu do Sola `medium`.
Nie ustanawiają wyłączności, kolejności silników ani automatycznych
przydziałów. Odpowiednie modele wybierasz per brief z dopuszczonego zbioru;
ograniczenia nazwanych agentów i skilli pomocniczych nadal obowiązują.
Nie zakładaj dostępu do narzędzi na podstawie samej nazwy modelu.

Przykład decyzji, nie szablon routingu: dla fali z ekranem, BE i i18n
najpierw wykluczasz kandydatów bez Figmy z briefu ekranu oraz bez wymaganego
test oracle z briefu BE. Plik niezmiennika high-stakes pozostaje na Opusie.
Dla pozostałych briefów porównujesz dopuszczone konfiguracje na podstawie
lokalnych wyników i sygnałów dostępności — Codex może wygrać już w planie.
Recenzent każdego zbioru zmian jest z innej rodziny niż autor. Wszystkie
briefy mają rozłączne pliki, a architekt odbiera diff, lint, format, testy,
build i wymagane dowody po każdej fali, z rezerwą na 2–3 korekty.
Zachowujesz najwyżej ~4 briefy z pętlą testów naraz i do ~10 briefów na falę.
Ocena routingu odbywa się wg rejestru, nie zamiast recenzji kodu fali.

Pułapki, które w tym skillu kosztowały najwięcej:

- **Gołe `Agent` z samym `model` dziedziczy effort sesji (`xhigh`).** Subagenta
  Claude'a wywołujesz wyłącznie jako nazwanego agenta z listy wyżej — tylko
  definicja agenta niesie `effort`.
- **Status dostępności jest jawny.** `znany` oznacza wiarygodny bieżący
  odczyt, `ostrzegawczy` — komunikat ostrzegawczy (np. ŻÓŁTY hooka),
  `zablokowany` — blokadę (np. CZERWONY hooka albo rzeczywisty limit
  wrappera), a `nieznany` — brak wiarygodnego odczytu zapasu.
  Zapisujesz źródło i czas odczytu; historia przydziałów nie daje procentu
  pozostałego limitu. Hook `~/.claude/bin/limity-hook.mjs` czyta endpoint
  co ≤ 90 s i dopisuje `[limity Claude]`; nie prosisz o `/usage`.
  ŻÓŁTY ostrzega, nie blokuje mocnego wykonawcy na zapas. CZERWONY blokuje
  subagentów Claude'a poza `zwiadowca` i `mechanik`. Zachowany wyjątek
  `[konieczny: powód]` dla krytycznego briefu wymaga zgłoszenia użytkownikowi;
  nie rozszerzasz go z powodów kosztowych.
- **Limit albo rzeczywiste niepowodzenie = ponowna kwalifikacja.** Odbierz
  stan artefaktów, zaktualizuj sygnał (limit → `zablokowany`), ponownie
  wylicz dopuszczone pary dla wykonania lub recenzji wg kroków 1–2 i zapisz
  model/native effort, uzasadnienie, pewność i alternatywy nowej decyzji.
  Zachowany wyjątek przy CZERWONYM: brief `wykonawca-opus` może trafić
  do Sparka `xhigh` (nigdy do Gemini, Sonneta ani Codexa) albo czeka;
  ten wyjątek nie otwiera high-stakes na Codexa. Figma nadal wymaga
  rzeczywistego dostępu, testy właściwego oracle, recenzja innej rodziny.
  Bramka Astra/Sol zachowuje własne modele i efforty; jej limit nie
  dopuszcza słabszej bramki. Gemini po trzykrotnym 503 traktujesz jako
  rzeczywiste niepowodzenie linii i ponownie kwalifikujesz kandydatów.
  Jeśli nie ma bezpiecznej dostępnej linii, **zatrzymaj zadanie i zgłoś
  blokadę** wraz z brakującym warunkiem; nie wymuszaj niedopuszczonego
  fallbacku. Zmianę linii meldujesz jednym zdaniem. Po resecie dostępności
  ponownie oceniasz kandydatów, nie wracasz automatycznie do stałej mapy.
  Sama cena tokenu albo odczyt `AGENTS.md` nie uzasadnia wyboru.
- **Brief dla Sparka nie może wymagać transkrypcji makiet.** Spark i Gemini
  nie mają Figma MCP; dostają wyłącznie briefy opisane w całości tekstem.
  Ekran z makiety wymaga linii z faktycznym dostępem do Figmy (Claude
  lub kwalifikujący się Codex). Wykonawca sam pobiera `get_design_context`
  i weryfikuje własne pliki zgodnie z regułami fali; pełny build robi
  architekt. Ekran funkcji high-stakes bez niezmiennika to osobny brief.
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
  nie recenzuje wcale (rodzina Sonneta i Opusa). Nie dublujesz recenzentów
  równolegle poza zachowaną próbą Astra/Sol. Wybór recenzenta per brief
  zawsze przechodzi kwalifikację. Brief wymaga sprawdzenia scenariusza
  P0/P1 przed zgłoszeniem, a Ty obalasz każde P0/P1 jednym poleceniem
  przed poprawką.

## Faza 3 — Implementacja etapu (linie wykonują, sesja główna waliduje)

Implementację wykonują linie z Fazy 2 wg briefów — **sesja główna nie pisze
kodu**. Jej robota w tej fazie to walidacja dowodów raz na falę: diff,
`npm run lint` / `npm test` / `npm run build` (FE) albo `dotnet build` /
`dotnet test` (BE), zrzuty 2×2 (360×530 i 1280×720, Light i Dark). Dowód
w przeglądarce dajesz sam narzędziem **`browser-check`**
(`D:\projects\DTCode\Claude_Skills\browser-check`, `README.md` i `FLOWS.md`):
FE (`npx ng serve --port 4300`) i BE (`dotnet run --launch-profile http`
w `ZebraniBE\ZebraniBE`) uruchamiasz sam w tle — gdy nie wstają lokalnie,
zatrzymujesz się i zgłaszasz brak dowodu. Potem `node browser-check.mjs
<bezwzględna ścieżka scenariusza> --out <katalog w scratchpadzie>`
z `BC_LOGIN`/`BC_PASSWORD` (konta demo), gdy scenariusz loguje, i kluczem
`TYPESAFE_API_KEY` ze zmiennych użytkownika, gdy ma `flows`
(`[Environment]::GetEnvironmentVariable('TYPESAFE_API_KEY','User')`, nigdy
nie wypisywany). Exit 0 nie dowodzi czystości: oglądasz PNG i czytasz
`consoleErrors`, `pageErrors`, `failedRequests` w `report.json`; PASS
z `passedWithoutActions` to wada scenariusza (asercje spełnione na starcie).
Wynik inny niż PASS triażujesz z raportu: defekt aplikacji → korekta do
autora; wada scenariusza (cel, asercja, lokator) → poprawka i powtórka;
`ERROR`, `TIMEOUT` lub `artifactError` → jedna powtórka. Worker z Playwright
MCP — wybrana per brief linia (Spark, Gemini lub Codex po potwierdzeniu
narzędzia), nie subagent Claude'a (reguła 15 — zrzuty stron szybko puchną
w kontekście) — wchodzi przy `NEED_FALLBACK`, `LOOP`, `MAX_STEPS`, FAIL,
którego raport nie wyjaśnia, wyniku powtarzającym się po powtórce albo
dla interakcji spoza scenariusza. Jego brief podaje przejście, stan
wyjściowy, ustalenia raportu, `forbidden` scenariusza, zakaz akcji
nieodwracalnych i akcji z zapisem z listy high-stakes Fazy 4b, a także
własną kartę i `location.href` przed każdym zrzutem.
Po każdej fali całą weryfikację robisz Ty, z rezerwą na 2–3 drobne korekty,
i odbierasz niezależną recenzję z Fazy 4b.

**Raport przekazania zamiast raportu końcowego** (reguła 15, strażnik
kontekstu od 2026-09-28). Hook `~/.claude/bin/kontekst-hook.mjs` każe
subagentowi Claude'a przy 300 tys. kontekstu (Haiku: 120 tys.) domknąć
bieżącą jednostkę pracy i oddać raport przekazania, a przy 450 tys. (Haiku:
160 tys.) nie zaczynać nowej. Taki raport walidujesz jak każdy wynik — diff
tego, co zrobione — a resztę zlecasz **świeżemu agentowi tej samej linii**:
pierwotny brief + raport przekazania (decyzje i pułapki dosłownie) + „nie
powtarzaj zrobionego, zacznij od sprawdzenia stanu poleceniem X”. Nie
wznawiasz starego agenta przez `SendMessage` — jego długi kontekst to
właśnie koszt, przed którym chroni strażnik. W ocenie fal liczysz rundy
korekty briefów z kontynuacją osobno od briefów bez niej. Workerów
zewnętrznych (Spark, Gemini, Codex) strażnik nie widzi — ich pilnuje podział
briefu na jedną warstwę.

Gdy coś wizualnego po korekcie nadal wygląda źle albo jest tylko przybliżone
„na oko" (np. odstęp liczony z tokenu paddingu zamiast z realnego renderu),
**nie zlecasz kolejnej rundy poprawek na oko** — zlecasz research właściwej
techniki (kwalifikacja i wybór modelu/native effort per brief wg Fazy 2)
i dopiero potem brief korekty
z konkretną metodą.

Weryfikacja wizualna zawsze w prawdziwej przeglądarce (dev server), zgodnie
z CLAUDE.md · FE · Finishing Every Implementation — jsdom/AXE nie dowodzi
kontrastu ani interakcji nakładek.

### Bug: test first — czerwony test przed łatką, ten sam test zielony po niej

Gdy work item to **Bug**, kolejność jest obowiązkowa i niezmienna:

1. **Najpierw test, który udowadnia błąd — osobny brief testowy.**
   Wykonawcę i recenzenta kwalifikujesz i wybierasz wg Fazy 2 (nazwany
   `tester` pozostaje kandydatem z własnym modelem i effortem).
   Zautomatyzowany test (spec Vitest / test xunit; Playwright tylko wtedy,
   gdy błąd jest widoczny wyłącznie w prawdziwej przeglądarce) odtwarzający
   dokładnie scenariusz ze zgłoszenia i asertujący **zachowanie poprawne**.
   Tester uruchamia go na kodzie bez poprawki — **musi być czerwony**, i to
   z powodu buga, nie z powodu literówki w teście czy brakującego providera —
   i wkleja wynik (nazwa testu, komunikat asercji) do raportu. Ty sprawdzasz,
   że czerwień pochodzi z buga.
2. **Dopiero potem łatka — osobny brief na linię zakwalifikowaną i wybraną
   wg Fazy 2**, z zachowaniem high-stakes i dostępu do Figmy/narzędzi
   **— z zakazem edycji pliku testu.**
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

## SemVer — niezależne wersje FE/BE (od 5.12, korekta 5.13)

Każde zmienione repo aplikacji (`ZebraniFE`, `ZebraniBE`) dostaje w tym zadaniu niezależny bump SemVer. Poziom wybierasz Ty na podstawie faktycznego diffa, nigdy wyłącznie po typie work itemu w ADO: `major` — breaking contract / usunięte publiczne zachowanie; `minor` — kompatybilna nowa funkcja; `patch` — fix, security, performance, refaktor/build zmieniający artefakt; `none` — sama dokumentacja/testy bez zmian artefaktu. Z całej zmiany bierzesz najwyższy poziom. Uzasadnienie (poziom + które zmiany go wymuszają) wpisujesz do planu (Faza 1) i raportu bramy (Faza 5); o decyzję pytasz tylko przy rzeczywiście niejasnej kompatybilności — nigdy rutynowo o numer.

Arytmetykę liczy deterministyczny skrypt stdlib (kwalifikacja semantyczna jest Twoja — skrypt nie wykrywa breaking change z diffa): `scripts/release_version.py` — pełna lokalna ścieżka Windows: `D:\projects\DTCode\Claude_Skills\Implement ADO Feature – Zebrani\scripts\release_version.py` (w briefach i wywołaniach podawaj zawsze pełną, żeby uruchomienie z cwd repo aplikacji nie było niejednoznaczne) — `--repo` absolutny katalog `--work-item` numer `--bump major|minor|patch|none` [`--initial X.Y.Z`] [`--write`]; bez `--write` tylko podgląd, nic nie zmienia.

- Źródło: `version.json` (`{"version":"X.Y.Z","lastRelease":{"workItem":2290,"baseVersion":"X.Y.Z","bump":"minor"}}`; strikt `X.Y.Z` bez zer wiodących, bez prerelease/build). Brak `version.json` w istniejącym repo to jednorazowe ustalenie `--initial` — honoruj już podaną decyzję startową (FE/BE: `1.0.0`); inicjalizacja zapisuje pierwsze wydanie tego work itemu (`version`=base, `bump:"none"`, `initialized:true`), a powtórzenie tego samego work itemu z dowolnym bumpem zostaje przy tej wersji, bez dodatkowego bumpa. Inny work item gubi `initialized` i bumpuje normalnie od bieżącej wersji.
- Powtórzenie tego samego PBI (poza markerem inicjalizującym) przelicza od `baseVersion` (upgrade patch→minor/major przed wydaniem możliwy, downgrade nigdy); inne PBI startuje od bieżącej wersji. `none` nie rusza markera ani plików. Niespójny lub nieprawidłowy zapis to błąd bez zapisu.
- Idempotencja PBI chroni przygotowanie przed wydaniem: po opublikowaniu wersji każda dalsza zmiana artefaktu wymaga nowego wydania / nowego work itemu, nigdy nadpisania opublikowanego `X.Y.Z`. Przed wydaniem zwaliduj aktualną bazę repo i rozbieżności równoległej pracy — bez automatycznego zgadywania konfliktów. Skrypt nie sprawdza zdalnego opublikowania.
- FE: `package.json` + `package-lock.json` (top `version` i `packages[""].version`); BE: jawny `<Version>X.Y.Z</Version>` w pierwszym `PropertyGroup` w `ZebraniBE/ZebraniBE.csproj`, bez ruszania `PackageReference Version` i reszty XML. Niepoprawny XML, warunkowy pierwszy `PropertyGroup`, warunkowy `<Version>`, wiele `<Version>` albo `<Version>` poza pierwszym `PropertyGroup` to błąd bez zapisu. Repo rozpoznane po plikach; brak albo niejednoznaczność to błąd. Zapis atomowy pojedynczych plików — to nie transakcja FS, więc skrypt weryfikuje każdy plik po zapisie. Bez gita, tagów i `npm`.
- Kolejność: podgląd po stabilizacji zakresu, zapis **przed** quality gates i końcową bramą, przez delegowanego wykonawcę (brief z doborem per brief wg Fazy 2 — sesja główna nie pisze). Wersja, bump, ID PBI i manifesty muszą opisywać ten sam artefakt; pliki wersji wchodzą do commita Fazy 6 jak reszta plików zadania. Brak zgody na commit/push nie blokuje lokalnego przygotowania wersji.
- Deploy/restart/rollback nie robią bumpa; rollback pokazuje wersję obrazu. Numeru tego skilla tym narzędziem nie podbijasz.

## Faza 4 — Audyt SCSS przed zgłoszeniem gotowości

Zanim zgłosisz zadanie jako gotowe do mojej akceptacji, zlecasz przegląd
**wszystkich zmodyfikowanych plików SCSS** wykonawcy audytu dobranemu
wg kroków 1–2 Fazy 2. Spark `xhigh` pozostaje preferencją na podstawie
dotychczasowej próby, nie wyłącznym przydziałem. Audyt: tylko odczyt,
jeden przebieg bez pominiętego pliku; jawny model/native effort,
uzasadnienie, pewność i alternatywy. Jeśli audyt pełni także rolę recenzji
z Fazy 4b, wymaga innej rodziny niż autor; sam audyt jej nie zastępuje.
Brief zawiera listę plików z `git diff --name-only` dostarczoną przez
architekta (Spark nie uruchamia gita), kryteria dosłownie, zakaz modyfikacji
i raport „co zastąpić / co wydzielić / co zostawić i dlaczego” na stdout;
po przebiegu `git status`. Gdy raport pominie plik, audyt nie jest odebrany:
ponownie kwalifikujesz i wybierasz linię do pełnego przeglądu.
Decyzję o wydzieleniu mixinu albo komponentu podejmujesz Ty na podstawie
raportu — nie czytasz sam każdego SCSS. Kryteria:

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

Autor nie recenzuje sam siebie: **po każdej fali**, przed rozpoczęciem
zależnej i przed bramą potwierdzenia, zlecasz przegląd niescommitowanego
diffu recenzentowi **z innej rodziny modeli niż autor diffu** (reguła 13
globalnego `CLAUDE.md`). Po audycie SCSS zachowujesz kontrolę kompletności
recenzji przed bramą. Okresowa ocena routingu nie zastępuje recenzji fali.

Recenzenta kwalifikujesz i wybierasz wg kroków 1–2 Fazy 2: tylko odczyt,
narzędzia i kontekst, kompetencje do zakresu i stawki oraz niezależna
rodzina. Dla wyższej stawki wymagana jest wyższa klasa recenzji; tania
konfiguracja bez tej zdolności odpada w kroku 1. Model/native effort,
uzasadnienie, pewność, alternatywy i status dostępności zapisujesz
w briefie recenzenckim. Sol jest kandydatem bez czekania na limit, ale
nie recenzuje kodu rodziny Codexa; Spark nie recenzuje Sparka, Gemini
Gemini. Fable nie recenzuje (ta sama rodzina co Sonnet i Opus).
Wyjątek: w próbie A/B linii Figmy oba ramiona recenzuje Spark `xhigh` —
stały recenzent jako kontrola eksperymentu; brief, którego Spark nie
zrecenzuje, wypada z pomiaru.

Fala mieszana → recenzje po zbiorach plików per autor, każda przez inną
rodzinę niż ten autor. Liczby recenzji nie limitujesz. Brief recenzenta
wymaga sprawdzenia scenariusza każdego P0/P1 przed zgłoszeniem, a Ty
obalasz każde P0/P1 jednym poleceniem przed poprawką. Architekt odbiera
rzeczywisty diff, lint, format, testy, build i wymagane dowody po każdej fali;
raport wykonawcy ani recenzenta nie jest sam w sobie dowodem.

**Sol:**

```powershell
$env:USERPROFILE\.claude\bin\worker-run.ps1 `
  -Engine codex -Mode review `
  -Repo D:\projects\DTCode\ZebraniFE `
  -Model gpt-6.1-sol -Effort high `
  -Title "Recenzja PBI #<numer>"
```

(bez `-BriefFile` wrapper sam dokleja `--uncommitted`; dla ZebraniBE `-Repo`
wskazuje na to repo). To przykład wywołania Sola `high`, nie automatyczny
przydział; `-Model` i `-Effort` mają odpowiadać parze wybranej w briefie.
Przy mieszanej fali Sol dostaje `-BriefFile` z listą plików danego autora
jako instrukcją przeglądu (wtedy wrapper nie dokleja `--uncommitted`).
Nie wolno objąć recenzją kodu własnej rodziny.

**Spark:** wrapper nie ma dla niego trybu `review`, a Spark nie uruchamia
gita — diff przydzielonego zbioru plików innej rodziny (`git diff HEAD -- <pliki>`)
i listę nowych plików wklejasz do briefu wg szablonu „Recenzja przez Sparka"
z `external-workers`; `-Repo` to repozytorium, więc Spark czyta `AGENTS.md`
i dowolne pliki dla kontekstu. Po przebiegu `git status` — recenzja niczego
nie zmienia.

**Gemini:** `worker-run.ps1 -Engine gemini` z jawną konfiguracją
pary `model/native effort` zapisanej w briefie po kwalifikacji i `-Access read`;
effort musi odpowiadać suffixowi identyfikatora modelu, więc pomiń `-Effort`
albo podaj wartość zgodną z suffixem — nigdy sprzeczną. Brief wg szablonu
„Recenzja przez Gemini" z `external-workers`: diff przydzielonych plików
innej rodziny wklejony do briefu,
**wszystkie ścieżki bezwzględne**, `AGENTS.md` wskazany do przeczytania
wprost (w trybie bez interfejsu nie ładuje się sam), zakaz poleceń powłoki.
Uprawnienia Antigravity dopuszczają tylko odczyt `D:\projects\DTCode`
i stron WWW, więc recenzja z definicji niczego nie zmienia.

**Lokalny sygnał jakości z 2026-09-23** (3 etapy: PBI #2282 +
DomSztukiFE ×2) wspierał recenzje Spark/Gemini. To preferencja do
weryfikowania w rejestrze, nie wyłączność ani warunek limitu dla Sola.

**Bramka końcowa Astry — raz na feature wysokiej stawki.** Gdy feature
dotyka uwierzytelniania i sesji, płatności (Stripe), PIN-u sprzedawcy,
migracji danych, naliczania pieczątek i nagród, jednorazowych kodów albo
limitów prób, **po** recenzjach etapów i ich poprawkach, a przed bramą
potwierdzenia, zlecasz jedną recenzję całego niescommitowanego diffu
feature'a (ta sama komenda, `-Model gpt-6-astra -Effort max`,
`-Title "Bramka Astra PBI #<numer>"`). Astra **uzupełnia** recenzje etapów,
nigdy ich nie zastępuje. Jej niezależność dotyczy plików niosących
niezmiennik high-stakes (pisze je `wykonawca-opus`, w wyjątku CZERWONEGO
Spark `xhigh`); briefy bez niezmiennika, także pisane przez Codex, mają
niezależność z recenzji fali z rodziny innej niż Codex — bramka czyta
cały diff funkcji w jednym przebiegu (recenzji nie dzielisz na porcje
≤ 5 plików, te dotyczą implementacji/testów Codexa), ale dla nich nie
zastępuje recenzji fali. Wyłącznie `max`: ~80 % kosztu recenzji to czytanie
kodu, więc niższy effort daje cenę Astry bez jej przewagi (Astra `low` ≈
Spark `xhigh` w Intelligence Index). Koszt jest realny — bramka całego
PBI #2137 zjadła 66 pkt okna 5 h i 10 % tygodnia Codexa — i się opłacił:
po dwóch recenzjach Sola znalazła pięć realnych defektów (podwójny POST,
pominięte odświeżenie kart, `retryAfterSeconds` poza zakresem, zawieszone
żądanie po błędzie ładowania nakładki, brak sprawdzenia roli klienta).
Znaleziska triażujesz razem z recenzjami etapów; w raporcie przed bramą
zaznaczasz, co znalazła tylko Astra. Kryterium stawki wpisujesz do planu
(Faza 1), nie decydujesz o nim po fakcie.

**Próba bramki (od 2026-09-30, reguła 6 globalnego `CLAUDE.md`).** 6.1 Sol
`max` ma prawie Intelligence Index Astry `max` (51,8 wobec 52,7) za 4,5×
niższy koszt zadania (0,72 $ wobec 3,26 $). Na najbliższym feature'ze
wysokiej stawki puszczasz bramkę równolegle drugi raz — ta sama komenda
z `-Model gpt-6.1-sol -Effort max`, `-Title "Bramka Sol 6.1 PBI #<numer>"`
— i po triażu porównujesz znaleziska (wspólne / tylko Astra / tylko Sol,
z priorytetem). Wynik zapisujesz w regule 6 i w pamięci; 6.1 Sol przejmuje
bramkę, jeśli nie przegapił żadnego P1 Astry i znalazł co najmniej tyle
realnych defektów.

Co robisz z wynikiem — **triaż, nie posłuszeństwo** (skill
`superpowers:receiving-code-review` obowiązuje):

1. Każde znalezisko klasyfikujesz: **defekt** (naprawić), **sporne**
   (rozstrzygasz Ty, z uzasadnieniem w raporcie), **fałszywy alarm** (recenzent
   nie zna konwencji repo — np. zgłasza brak `standalone: true`, `p-button`
   zamiast `[pButton]`, Cream zamiast białego jako „błąd"). Fałszywe alarmy
   wypisujesz z jednym zdaniem dlaczego; nie naprawiasz ich.
2. Defekty wracają **do tej samej linii, która pisała kod** (Spark do
   Sparka, Gemini do Gemini, `wykonawca` do `wykonawcy`, `wykonawca-opus`
   do `wykonawca-opus`, Codex do wybranej linii Codexa) jako brief korekty
   — nie łatasz sam. Po limicie albo rzeczywistym niepowodzeniu ponownie
   kwalifikujesz i wybierasz pary wg Fazy 2; brak bezpiecznej linii oznacza
   zatrzymanie i zgłoszenie blokady.
3. Po korekcie **nie zlecasz drugiej recenzji** — weryfikujesz poprawkę
   dowodem (diff + lint + testy). Druga runda tylko wtedy, gdy korekta
   dotknęła > ~5 plików albo zmieniła kształt API.
4. Do raportu przed bramą dołączasz: liczbę znalezisk w każdej klasie
   i listę spornych z Twoim rozstrzygnięciem.

Pomijasz tę fazę wyłącznie, gdy diff jest czysto mechaniczny (i18n, rename,
przeniesienie pliku) — wtedy piszesz to wprost w raporcie.

### Rejestr istotnych briefów i okresowa ocena routingu

Po istotnym briefie architekt zapewnia wpis do
`docs/model-routing-evaluation.md` w repozytorium `Claude_Skills`,
zgodnie z kanonicznymi polami wpisu (szablon w sekcji 4 rejestru): neutralny identyfikator lub typ
zadania bez treści biznesowej; archetyp; stawka; niepewność; linia/model/
native effort wykonawcy i recenzenta; dopuszczone alternatywy; powód,
sygnał dostępności i pewność; wynik pierwszego podejścia; liczba rund korekt;
czas do akceptacji; potwierdzone i odrzucone znaleziska z priorytetem;
defekty po odbiorze; wymagane testy i dowody. Wpis obejmuje rzeczywiste
wyniki i zmiany linii; dane jeszcze nieustalone oznaczasz jawnie, zamiast
zgadywać, i uzupełniasz po odbiorze lub wykryciu defektu. Mechaniczne
drobiazgi bez istotnej pracy nie wymagają wpisu.

Rejestr nie zawiera promptów, diffów, danych osobowych, poświadczeń,
tajemnic handlowych ani surowych zestawień tokenów. Nie dubluje
`token-report.py` ani raportu per ADO; Faza 1b i Faza 6 nadal je stosują.

Pierwszy przegląd po **10–15 istotnych briefach**, kolejne po kolejnych
**10–15** albo istotnej zmianie modeli/pomiaru limitów. Istotny błąd lub
kilka kosztownych poprawek uruchamia dodatkowy przegląd. Wyniki oceniasz
per archetyp; mała próbka nie uzasadnia rankingu. To rytm operacyjny,
nie próg statystycznej wystarczalności ani scoring. Recenzja kodu oraz
odbiór dowodów przez architekta nadal odbywają się **po każdej fali**.

## Faza 5 — Brama potwierdzenia (nie zamykaj ADO sam)

Po zakończeniu implementacji **ZATRZYMAJ SIĘ i czekaj na moje potwierdzenie**.
Nie ruszaj statusów w ADO (poza `In Progress` z Fazy 1b, które już stoi) ani
nie commituj samodzielnie na tym etapie.

Raport bramy zawiera punkt **„Dokumentacja”**: zmienione pliki i sekcje
dokumentacji produktowej albo uzasadnienie „bez zmian” — oraz punkt
**„SemVer”**: bump z uzasadnieniem i pary stare→nowe per zmienione repo
(z podglądu/zapisu skryptu). Gdy commit/push nie jest autoryzowany, raport
niesie też gotowy tekst komentarza dostępności (wypełniony szablon z Fazy 6,
pkt 4) — bez ogłaszania publikacji. Bez tych punktów brama nie jest gotowa.
Raport potwierdza też recenzję i odbiór dowodów każdej fali, spełnienie
ograniczeń routingu oraz wpisy istotnych briefów do rejestru (albo
uzasadnione mechaniczne pominięcia); dla high-stakes zawiera wynik
niezmienionej bramki końcowej i obowiązującego eksperymentu Astra/Sol.

- Jeśli zgłoszę poprawki → wprowadź je → wróć do tej samej bramy.
- Jeśli potwierdzę, że jest OK → przejdź do Fazy 6.

## Faza 6 — Domknięcie po potwierdzeniu

Wykonaj w tej kolejności:

1. **Commit i push** na `main` — numer PBI w branchu i w commicie
   (CLAUDE.md · Git Workflow). Dokumentację produktową commitujesz
   i pushujesz w tym samym kroku w repo `Dokumentacja` — nigdy „później”.
   Do commita wchodzą jawnie także pliki wersji z procedury SemVer:
   `version.json` oraz manifesty zmienionych repo (FE: `package.json`
   i `package-lock.json`; BE: `ZebraniBE/ZebraniBE.csproj`) — jak reszta
   plików zadania.
   `git add` **jawnie, tylko pliki z briefów
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

4. **Komentarz dostępności wersji — obowiązkowy, do SAMEGO PBI albo Buga,
   po autoryzowanym commicie/pushu, PRZED zmianą stanu na `Ready for tests`.**
   Dla Buga nie piszesz drugiego komentarza — sekcję dostępności dopisujesz
   do komentarza pieczętującego z pkt 3. Bez autoryzacji commit/push NIE
   ogłaszasz publikacji ani NIE wysyłasz tego komentarza — wypełniony szablon
   odkładasz do raportu bramy (Faza 5). Bram autoryzacji ten punkt nie zmienia.

   Szablon — pola w `<…>` to placeholdery do wypełnienia danymi tego zadania,
   NIE gotowe fakty:

   ```text
   Dostępność funkcji / poprawki:
   - FE: od <SemVer zawierający zmianę>; commit <pełny SHA>.
   - BE: od <SemVer zawierający zmianę>; commit <pełny SHA>.
   Weryfikacja PRE — <czas odczytu UTC>:
   - FE wdrożony: <SemVer + SHA + build/run> albo "niezweryfikowane / niewdrożone".
   - BE wdrożony: <SemVer + SHA + build/run> albo "niezweryfikowane / niewdrożone".
   - Odczyt: https://pre.zebrani.pl/version.json i https://pre.zebrani.pl/api/version; w UI pasek/stopka FE · BE (dopiero gdy endpointy/UI istnieją — przed ich implementacją jawnie brak mechanizmu).
   - Warunek rozpoczęcia retestu: live zawiera commit funkcji/fix po obu wymaganych stronach; numer i commit porównane do komentarza; FE w otwartej karcie może być starszy niż aktualny endpoint — odświeżyć i sprawdzić wersję ZAŁADOWANEGO FE.
   ```

   Zasady wypełniania:

   - Wersję dostępności bierzesz z `version.json` COMMITOWANEGO/wybudowanego
     artefaktu, nigdy z bieżącego lokalnego HEAD po dalszych zmianach.
     Zmieniona strona dostaje zawsze konkretny nowy numer. Jawnie rozróżniasz
     wersję zawierającą zmianę od wersji LIVE.
   - Strona niezmieniona w tym zadaniu: „bez zmian w tym zadaniu; wymagana
     `<potwierdzona wersja kontraktu>`" — tylko gdy wersja kontraktu jest
     naprawdę ustalona; w przeciwnym razie „bez zmian w tym zadaniu; wersja
     bazowa nieustalona". Nigdy nie wymyślasz nowego numeru ani „dowolna".
   - Samo `SemVer live >= docelowej` to NIE dowód dostępności (inne branche,
     rollback, rebuild, różna historia). Dowodem jest dokładny docelowy SHA
     albo zweryfikowane zawieranie docelowego commita przez live SHA
     (ancestry) + zgodność manifestu z artefaktem. Bez weryfikacji ancestry
     wpisujesz „dostępność niepotwierdzona", nigdy PASS.
   - Brak deployu albo odczyt niepotwierdzający nowej pary NIE blokuje
     `Ready for tests` (po autoryzacji, wg dotychczasowego procesu) — ale
     komentarz mówi wprost, że retest jest zablokowany do wdrożenia.
     Automatycznego deployu nie dodajesz ani nie domagasz się uprawnień do niego.
   - Wersje FE/BE są niezależne i mogą się różnić — tester porównuje
     wymagania osobno, per strona.

5. **Stan PBI / Buga → "Ready for tests".** Przed zapisem zweryfikuj dokładną
   nazwę stanu dla typu work itemu (`Task`, `Product Backlog Item` i `Bug`
   mogą się różnić) przez `mcp__azure-devops__wit_work_item`
   `action: get_type`, żeby nie trafić błędem API na literówkę w nazwie stanu.
6. **Przypisanie PBI / Buga** (`System.AssignedTo`) na testera — **Piotr
   Tuński**, `Piotr.Tunski@DTCode.pl`.
7. Zmiany 2, 5 i 6 rób przez `mcp__azure-devops__wit_work_item_write`
   `action: update_batch`, jednym wywołaniem na wszystkie PBI/taski naraz,
   gdzie to możliwe. **Zweryfikuj przez zwróconą treść odpowiedzi API** —
   deklaracja sukcesu nie jest dowodem, dopiero zwrócony stan pola jest.
8. **Raport zużycia tokenów — ostatnia rzecz w komunikacie końcowym.**
   Uruchom `python $env:USERPROFILE\.claude\bin\token-report.py report --task <numer>`
   i wklej obie tabele bez zmian (per silnik → per model → sumy; szczegóły
   per rola/brief) wraz ze stopką. Raport liczy z zapisów na dysku
   (transkrypty Claude'a, rollouty Codexa, sesje muse) — nie szacuj, nie
   pytaj o `/usage`. Ostrzeżenia `⚠` z raportu przepisz dosłownie. Sumy
   pokazują kolumny cache osobno: surowa suma jest w większości odczytem
   cache'u i bez podziału nic nie mówi o koszcie.
