---
name: fix-devops-bug-zebrani
description: >
  Naprawianie buga w projekcie Zebrani.pl na podstawie linku lub numeru Azure DevOps.
  Użyj, gdy użytkownik poda link do work itema (np.
  https://dev.azure.com/DTCode/Zebrani.pl/_workitems/edit/123) albo sam numer i poprosi
  o analizę/naprawę zgłoszenia. Skill pobiera work item i jego sub-taski (Fix/Retest),
  weryfikuje czy błąd występuje w kodzie, odtwarza buga w działającej aplikacji przez
  Playwright na macierzy 2×2 (mobile 360×530 i desktop 1280×720, każdy w Light i Dark)
  — test BEFORE, implementuje poprawkę zgodnie z CLAUDE.md, potwierdza Playwrightem
  że bug zniknął (test AFTER), uruchamia lint:fix + format, commituje i pushuje,
  proponuje ręczne uruchomienie deployu pre-prod, a następnie aktualizuje statusy
  w DevOps (Fix → Done, Bug → Ready for tests) i przypisuje buga do testera.
version: '1.0'
language: pl
project: Zebrani.pl
organization: DTCode
remote:
  github_raw: 'https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/Fix%20DevOps%20Bug%20%E2%80%93%20Zebrani/SKILL.md'
  github_page: 'https://github.com/DTCodePL/Claude_Skills/blob/main/Fix%20DevOps%20Bug%20%E2%80%93%20Zebrani/SKILL.md'
---

# Fix DevOps Bug – Zebrani.pl

Pełny przepływ naprawy zgłoszenia z Azure DevOps: **pobierz → przeanalizuj → odtwórz buga
(Playwright) → napraw → potwierdź fix (Playwright) → zlintuj → commit/push → deploy →
zaktualizuj statusy**. Treści (commit, komentarze, plan) pisz po polsku. Trzymaj się zasad
z `.claude/CLAUDE.md` w `ZebraniFE` (i18n w `pl` **i** `en`, kolory wyłącznie z tokenów,
Signal Forms, Observable zamiast Promise, brak `@deprecated`, dostępność WCAG AA).

## Kontekst projektu (stałe)

- Organizacja: `DTCode`, projekt: **`Zebrani.pl`**, team `Zebrani.pl Team`.
  Iteracje: `Zebrani.pl\Sprint 1` (bieżąca) … `Sprint 6` oraz `Zebrani.pl\E2e Sprint`.
- **Struktura Buga:** Bug ma zwykle dwa sub-taski (Task): **„Fix"** (robi developer) i
  **„Retest"** (robi tester). Tester = osoba przypisana do „Retest"
  (zwykle `Piotr.Tunski@DTCode.pl`, Piotr Tuński).
- **Stany Buga** (odczytane z API 2026-08-02, dokładne nazwy): `New`, `In Progress`,
  `In Review`, `Ready for tests`, `Done`, `Postponed`, `Rejected`, `Removed`.
- **Stany Taska:** `To Do`, `In Progress`, `In Review`, `Ready for tests`, `Done`,
  `Postponed`, `Rejected`, `Removed`.
  > ⚠️ Zestaw jest **szerszy niż w innych projektach DTCode** — Task w Zebrani ma m.in.
  > `In Review` i `Ready for tests`. Nie zakładaj trójki `To Do / In Progress / Done`.
- **Stany PBI:** `New`, `Ready to develop`, `In Progress`, `In Review`, `Ready for tests`,
  `Done`, `Postponed`, `Rejected`, `Removed`.
- **Repozytoria:**
  - FE: `DTCodePL/ZebraniFE` — `d:\projects\DTCode\ZebraniFE` (Angular 22, SSR, zoneless).
  - BE: `DTCodePL/ZebraniBE` — **repozytorium jest puste (samo README)**. Backend Zebrani
    jeszcze nie istnieje (patrz „Bug backendowy" niżej).
- **Git:** commity idą na `main`. Konwencja wiadomości: `fix(<scope>): #<idBuga> opis`
  po polsku (np. `fix(public): #123 ...`).
  - CLAUDE.md Zebrani wymaga numeru work itema w commicie — **numer buga tę regułę
    spełnia**. Nie doklejaj numeru PBI rodzica i nie wymyślaj go.
- Po każdej implementacji: `npm run lint:fix` + `npm run format` (wymóg CLAUDE.md).
- **Dev server:** `npm start` (= `ng serve`) → **http://localhost:4200**.
  Konkretne trasy do przetestowania wyprowadź z repro / work itema (nie zakładaj stałej listy).
- **Środowisko pre-prod:** `jan211.mikrus.xyz`, FE port `40192`, BE port `40193`.
  Prod **nie istnieje** — nigdy nie kieruj testera na `zebrani.pl`.

### Macierz testowa — 2 viewporty × 2 motywy (stała, obowiązkowa)

Każdy test Playwright BEFORE i AFTER uruchamiaj na **czterech** kombinacjach:

|                   | Light                | Dark                |
| ----------------- | -------------------- | ------------------- |
| **mobile 360×530**  | baseline M-L         | baseline M-D        |
| **desktop 1280×720** | baseline D-L         | baseline D-D        |

- `browser_resize(width=360, height=530)` — mobile (zgodnie z CLAUDE.md Zebrani).
- `browser_resize(width=1280, height=720)` — desktop.
- Light + Dark są w Zebrani **obowiązkowe w całej aplikacji**, publiczny obszar włącznie.
  Regresje tokenów kolorów najczęściej ujawniają się tylko w jednym motywie — dlatego
  oba są w macierzy nawet dla bugów, które „wyglądają na niezwiązane z kolorem".

## Narzędzia

- Azure DevOps MCP (`mcp__azure-devops__*`): `wit_get_work_item`,
  `wit_get_work_items_batch_by_ids`, `wit_get_work_item_type`, `wit_update_work_item`,
  `wit_add_work_item_comment`. Schematy doładuj przez `ToolSearch`
  (`select:mcp__azure-devops__wit_get_work_item,...`).
  - ⚠️ Jeśli MCP/API zwróci `203` albo stronę logowania — **PAT wygasł**. Zgłoś to
    użytkownikowi i zatrzymaj część devopsową; nie obchodź tego innym tokenem.
- Figma MCP (jeśli repro odwołuje się do makiety): `get_design_context`,
  `get_variable_defs`, `get_screenshot`. Klucz pliku Figma Zebrani.pl:
  `ZvXQhQILd9smr1Q1Gnzn5F`.
- **Playwright MCP** (`mcp__playwright__*`): `browser_navigate`, `browser_evaluate`,
  `browser_take_screenshot`, `browser_snapshot`, `browser_resize`, `browser_click`,
  `browser_wait_for`, `browser_console_messages`. Schematy doładuj przez `ToolSearch`.
- **MSSQL MCP** (`mcp__mssql__execute_sql`) — 🛈 **na dziś nieaktywne dla Zebrani:
  backend i baza jeszcze nie istnieją, `ZebraniBE` to samo README. Pomiń tę sekcję,
  dopóki BE nie ruszy.** Gdy baza powstanie, obowiązują poniższe zasady:
  - ✅ **Bez pytania dozwolone tylko odczyty** — wyłącznie `SELECT` (ewentualnie
    `SELECT` w CTE). Nic, co zmienia stan bazy.
  - ⛔ **Każda zmiana danych lub schematu wymaga wcześniejszej zgody użytkownika.** Zanim
    wykonasz `INSERT`, `UPDATE`, `DELETE`, `MERGE` albo DDL (`ALTER`, `CREATE`, `DROP`,
    `TRUNCATE`) — **zatrzymaj się i wprost zapytaj o akceptację** (`AskUserQuestion`),
    podając dokładne zapytanie SQL i czego dotyczy.
  - 🛈 Zmiany schematu i tak realizujemy przez **numerowane skrypty SQL**
    (`ZebraniBE/Scripts/Script{NNNNN}...`, wymóg CLAUDE.md), a nie przez ten MCP.
- `Bash`/`PowerShell` do git, `npm`. Edycja kodu zwykłymi narzędziami plikowymi.
- **`gh` CLI** (GitHub) — do uruchomienia deployu pre-prod i odczytania numeru runa
  (krok 8). Uruchamiaj w shellu z dostępem do sieci i zalogowanym `gh` — zwykle
  **PowerShell**, bo Bash bywa w sandboxie bez sieci/DNS.

## Procedura

### 1. Zidentyfikuj work item

- Z linku `.../_workitems/edit/<ID>` wyciągnij `<ID>`. Jeśli użytkownik podał sam numer,
  użyj go. Projekt = `Zebrani.pl`.
- `wit_get_work_item(id, project="Zebrani.pl", expand="relations")` — pobierz `System.Title`,
  `Microsoft.VSTS.TCM.ReproSteps` (kroki naprawy + referencje Figma), `System.State`,
  `System.CreatedBy` oraz relacje (dzieci `Hierarchy-Forward`).
- Jeśli to **Bug**, wyłuskaj dzieci i pobierz je batchem
  `wit_get_work_items_batch_by_ids([...])` — znajdź Task **„Fix"** i Task **„Retest"**.
  Zapamiętaj `AssignedTo` z „Retest" (to tester).

### 2. Zweryfikuj, czy błąd występuje w kodzie

- Przeczytaj wskazane w repro pliki/komponenty (Grep/Glob/Read). **Potwierdź każdy punkt
  zgłoszenia faktem z kodu** (plik + linia). Nie zakładaj — sprawdź.
- **Bug backendowy:** jeśli repro dotyczy API, danych, bazy albo logiki serwerowej —
  `ZebraniBE` jest puste, więc nie ma czego naprawiać. **Zatrzymaj się, zgłoś to
  użytkownikowi i zapytaj o dalsze kroki.** Nie szukaj „gdzieś indziej" i nie próbuj
  załatać tego w FE, jeśli zgłoszenie tego nie mówi wprost.
- Jeśli repro dotyczy koloru, kontrastu albo powierzchni — sprawdź **oba motywy**
  w `theme/palette.ts` i `theme/app.preset.ts`. Pamiętaj o pułapce Aury: wypełnione
  warianty przycisku żyją pod `button.root.<severity>`, a token wpisany w złej ścieżce
  jest **po cichu ignorowany** (brak błędu kompilacji).
- Jeśli repro odwołuje się do Figmy (node-id w URL): spróbuj `get_design_context` /
  `get_variable_defs` dla węzła. Gdy MCP zwróci „nothing selected", **poproś użytkownika,
  by zaznaczył węzeł w Figma desktop** (albo podał wartości), lub działaj wg wartości
  podanych w repro.
- Jeśli błędu **nie ma** w kodzie (np. już naprawiony) — zatrzymaj się, zgłoś to
  użytkownikowi i zapytaj o dalsze kroki zamiast „naprawiać na siłę".

### 3. Odtwórz buga w działającej aplikacji — Playwright (BEFORE)

**Obowiązkowe przed naprawą.** Najpierw zamień każdy punkt repro na **mierzalną asercję**
(patrz „Testowanie w Playwright"), potem uruchom aplikację i potwierdź, że bug realnie
występuje.

- Upewnij się, że dev server działa (`npm start` w tle; poczekaj aż wstanie na
  `http://localhost:4200`). Ekrany zależne od backendu **nie zadziałają** — BE nie istnieje;
  jeśli repro tego wymaga, zgłoś to i ustal z użytkownikiem.
- `browser_navigate` na właściwą trasę, a następnie przejdź **całą macierz 2×2**:
  1. `browser_resize(360, 530)` → Light → asercja + screenshot
  2. `browser_resize(360, 530)` → Dark → asercja + screenshot
  3. `browser_resize(1280, 720)` → Light → asercja + screenshot
  4. `browser_resize(1280, 720)` → Dark → asercja + screenshot
- Po każdej zmianie szerokości ponów nawigację/odświeżenie, jeśli układ zależy od szerokości.
- **Zapisz cztery baseline'y osobno** — porównanie „po" robisz parami, nie zbiorczo.
- Jeśli bug z natury dotyczy jednej kombinacji (np. tylko Dark na mobile), i tak uruchom
  asercję na wszystkich czterech — pozostałe potwierdzają baseline „zdrowy".
- Jeśli buga **nie da się odtworzyć** (asercja „przed" nie potwierdza problemu) —
  zatrzymaj się i skonsultuj z użytkownikiem; nie naprawiaj na ślepo.

#### Przełączanie motywu Light ⇄ Dark

Motyw w Zebrani steruje serwis `ThemeMode` (`core/theme/`), który przełącza klasę
`.app-dark` na elemencie root. SSR **zawsze renderuje Light** — motyw z pamięci wraca
dopiero po hydracji.

1. **Preferowany sposób:** kliknij realny przełącznik motywu w interfejsie
   (`browser_click`) — testujesz wtedy też jego działanie.
2. **Fallback** (gdy na danym ekranie nie ma przełącznika):

   ```js
   // włącz Dark
   () => { document.documentElement.classList.add('app-dark'); return document.documentElement.className; }
   // wróć do Light
   () => { document.documentElement.classList.remove('app-dark'); return document.documentElement.className; }
   ```

3. Po przełączeniu odczekaj na przerysowanie (`browser_wait_for`) zanim odczytasz
   computed style — inaczej złapiesz wartości sprzed zmiany.

### 4. Zaplanuj i wprowadź poprawkę

- Trzymaj się kierunku z repro i zasad CLAUDE.md. Reużywaj istniejących wzorców i tokenów.
- **Nigdy nie wprowadzaj surowego koloru** (hex/rgb/hsl) — kolory pochodzą wyłącznie
  z `var(--p-*)` / `dt('…')`. Jeśli żaden istniejący token nie pasuje — **zatrzymaj się
  i zapytaj**, zamiast dodawać nowy jednostronnie.
- **Nie nadpisuj PrimeNG własnym CSS** — bez `::ng-deep`, bez celowania w `.p-*`.
  Poprawki wyglądu komponentów PrimeNG idą przez preset.
- Jeśli zgłoszenie dotyczy wielu bliźniaczych komponentów (powtarzalne sekcje/strony),
  zastosuj zmianę spójnie we wszystkich.
- Przy decyzjach niejednoznacznych (zakres, wartości z Figmy, nowy token) użyj
  `AskUserQuestion` zamiast zgadywać.

### 5. Finalizacja kodu (wymóg CLAUDE.md)

```bash
npm run lint:fix   # eslint --fix + stylelint --fix
npm run format     # prettier --write .
```

Jeśli po `lint:fix` zostają błędy — przeczytaj i napraw ręcznie, powtórz aż do zera.

Dodatkowo zweryfikuj (wymogi CLAUDE.md Zebrani):

- każdy nowy/zmieniony klucz i18n istnieje **jednocześnie** w `src/assets/i18n/pl.json`
  **i** `src/assets/i18n/en.json`,
- zero hardkodowanych kolorów poza `theme/`,
- zero użyć symboli `@deprecated` (m.in. `p-button`, `MultiSelect`, `withFetch()`),
- AXE przechodzi.

### 6. Zweryfikuj fix w działającej aplikacji — Playwright (AFTER)

**Obowiązkowe przed commitem.** Na tej samej trasie powtórz asercje na **całej macierzy
2×2** (mobile 360×530 / desktop 1280×720 × Light / Dark) i potwierdź, że bug **zniknął**.

- Jeśli dev server był podniesiony, poczekaj na hot-reload (`browser_wait_for`) lub
  odśwież (`browser_navigate` ponownie).
- Dla **każdej z czterech kombinacji** powtórz asercje (`browser_evaluate`) — teraz muszą
  zwracać stan oczekiwany. Zrób screenshot „po" do porównania z **odpowiadającym**
  baseline'em (M-L z M-L, M-D z M-D itd.).
- Sprawdź **brak regresji**: `browser_console_messages` (zero nowych błędów) i szybki rzut
  oka na sąsiednie ekrany dzielące te same komponenty.
- **Jeśli asercja „po" w którejkolwiek kombinacji nadal pokazuje buga — NIE commituj.**
  Wróć do kroku 4 i popraw.

### 7. Commit + push -- zrób to tylko jeżeli wprost ci powiem, że masz pushować

> ⚠️ **Pułapka:** `npm run lint:fix` i `npm run format` potrafią zmodyfikować
> **niepowiązane** pliki (autofix). Sprawdź `git status` i **zestage'uj wyłącznie pliki,
> które świadomie zmieniłeś dla tego buga** (`git add <konkretne pliki>`), nigdy `git add -A`.
> Niepowiązane zmiany zostaw nietknięte i zgłoś je użytkownikowi.

- Pokaż `git diff --stat` zestage'owanych plików i **proponowaną treść commita** do
  akceptacji.
- Commit (stopka obowiązkowa):

```
fix(<scope>): #<idBuga> <krótki opis po polsku>

<opcjonalnie 1–3 linie szczegółów>

Co-Authored-By: Claude <noreply@anthropic.com>
```

- `git push origin main`.
- (Jeśli użytkownik woli PR: utwórz branch `fix/<idBuga>-<slug>`, push, PR z linkiem do
  work itema — zapytaj, gdy nie jest jasne.)

### 8. Deploy pre-prod i aktualizacja statusów w Azure DevOps

#### 8a. Deploy jest RĘCZNY — zapytaj

W Zebrani deploy **nie odpala się po pushu**. Workflow `deploy-preprod.yml`
(„Build & Deploy (FE) — pre-prod") ma wyłącznie `workflow_dispatch`. Dopóki go nie
uruchomisz, fix **nie jest dostępny dla testera**.

Po udanym pushu zadaj pytanie (`AskUserQuestion`): *„Odpalić deploy pre-prod, żeby tester
mógł zretestować?"*

- **Zgoda →** uruchom i poczekaj:

  ```powershell
  gh workflow run deploy-preprod.yml --repo DTCodePL/ZebraniFE -f runner=github
  # po chwili odczytaj numer runa:
  gh run list --repo DTCodePL/ZebraniFE --workflow deploy-preprod.yml --limit 1 --json number,headSha,status,conclusion
  ```

  - Run dispatchowany po Twoim pushu ma `headSha` **równy hashowi Twojego commita** —
    sprawdź to i weź `number` wprost. **Nie stosuj heurystyki „ostatni + 1"** znanej
    z projektów z deployem na push; tutaj jest błędna.
  - Poczekaj na `conclusion: success`. Jeśli run padnie — **nie pisz testerowi, że fix
    jest dostępny**; zgłoś awarię deployu użytkownikowi.
  - Do komentarza wpisz `FE: <number>+`.

- **Odmowa →** w komentarzu napisz: „Fix jest na `main`, ale środowisko pre-prod wymaga
  ręcznego deployu — retest po najbliższym wdrożeniu."

- **BE:** dopóki `ZebraniBE` jest puste, w komentarzu zawsze `BE: N/D`.

Format numeru: liczba z **plusem** (np. `FE: 12+`) — oznacza „ten build lub nowszy".

#### 8b. Statusy

- Task **„Fix"** → `Done`:
  `wit_update_work_item(id=<fix>, [{op:"add", path:"/fields/System.State", value:"Done"}])`
- **Bug** → `Ready for tests` **i** przypisz testerowi (assignee z „Retest"):

  ```
  wit_update_work_item(id=<bug>, [
    {op:"add", path:"/fields/System.State", value:"Ready for tests"},
    {op:"add", path:"/fields/System.AssignedTo", value:"<email_testera>"}
  ])
  ```

- Task **„Retest"** — **bez zmian** (czeka na test).

#### 8c. Komentarz do Buga (obowiązkowy)

Dodaj komentarz opisujący **co zostało naprawione** oraz **jak to zretestować ręcznie**.
Pisz **nietechnicznie** — tak, żeby tester (nie programista) zrozumiał, co sprawdzić
i jakiego efektu oczekiwać. Nie wklejaj kodu ani nazw plików/zmiennych. Hash commita
możesz dodać na końcu jako odnośnik. **Pierwszy punkt sekcji „Co zostało naprawione"
MUSI podać build do retestów.** Użyj
`wit_add_work_item_comment(workItemId=<bug>, project="Zebrani.pl", comment=...)`.

Szablon:

```
Co zostało naprawione:
Fix dostępny od builda FE: <X>+ i BE: N/D
(albo: „Fix jest na main — środowisko pre-prod wymaga ręcznego deployu, retest po najbliższym wdrożeniu.")
<1–3 zdania prostym językiem, co teraz działa poprawnie>

Jak zretestować ręcznie:
1. <gdzie wejść, co kliknąć / jaki ekran otworzyć>
2. <na jakiej szerokości: telefon i komputer>
3. <w jakim motywie: jasny i ciemny — jeśli zgłoszenie dotyczyło wyglądu>
4. <co należy zaobserwować — oczekiwany, poprawny efekt>
5. <ewentualnie: gdzie wcześniej był błąd, żeby tester wiedział na co patrzeć>

Naprawiono na main (commit <hash>).
```

> 🛈 Adres do retestu to środowisko **pre-prod** (`jan211.mikrus.xyz`, port FE `40192`).
> Produkcja nie istnieje — nigdy nie kieruj testera na `zebrani.pl`.

### 9. Podsumuj użytkownikowi

Wypisz: które punkty potwierdzone w kodzie (plik:linia), **wynik testów Playwright
(before → after) dla wszystkich czterech kombinacji**, zmienione pliki, hash commita,
czy deploy został uruchomiony i z jakim numerem, nowe statusy (#Fix=Done,
#Bug=Ready for tests → tester) oraz ewentualne niepowiązane zmiany pominięte w commicie.
Wskaż screenshoty „przed/po" i porównanie z Figmą.

## Testowanie w Playwright (MCP)

Zasada: **zamień każdy punkt repro w mierzalną asercję** i sprawdź ją tym samym kodem
przed i po fixie. Screenshot jest dowodem pomocniczym, ale werdykt daje `browser_evaluate`
(deterministyczny), nie „oko".

**Cztery obowiązkowe kombinacje:** mobile `360×530` i desktop `1280×720`, każda w Light
i Dark. Trzymaj baseline i screenshot osobno dla każdej.

**Start serwera:** odpal `npm start` w tle i poczekaj aż odpowie `http://localhost:4200`,
zanim wejdziesz `browser_navigate`. Po naprawie poczekaj na hot-reload przed asercją „po".

**Wzorce asercji (`browser_evaluate`):**

- **Kolor z tokenu** — odczytaj realnie wyrenderowaną wartość i porównaj z wartością
  tokenu, a nie z wpisanym „na sztywno" RGB (kolory w Zebrani pochodzą z presetu
  PrimeNG i zmieniają się między motywami):

  ```js
  () => {
    const el = document.querySelector('.target-element');
    const cs = getComputedStyle(el);
    const root = getComputedStyle(document.documentElement);
    return {
      color: cs.color,
      background: cs.backgroundColor,
      token: root.getPropertyValue('--p-primary-color').trim(),
      dark: document.documentElement.classList.contains('app-dark'),
    };
  }
  ```

- **Kontrast (WCAG AA)** — gdy zgłoszenie mówi „nieczytelne" / „za jasne", policz
  kontrast z realnie wyrenderowanych wartości. Kolory oparte na `color-mix()`
  rozwiązują się do `color(srgb … / a)` — **spłaszcz je na tle powierzchni**, zanim
  policzysz; półprzezroczysty kolor nie może być oceniany jak nieprzezroczysty.
- **Poziomy scroll / wyjście poza kontener** — element się przewija, gdy `scrollWidth`
  przekracza `clientWidth`:

  ```js
  () => { const t = document.querySelector('.target-wrap');
    return { scrollW: t.scrollWidth, clientW: t.clientWidth, overflows: t.scrollWidth > t.clientWidth }; }
  ```

  (BEFORE: `overflows: true`; AFTER: `false`). Uruchom na obu szerokościach.

- **Typografia** — `getComputedStyle(el).fontSize` / `lineHeight` / `fontWeight`
  i porównaj ze skalą `--zeb-text-*`. Sprawdź też, czy element **nie** deklaruje własnego
  `font-family` — w Zebrani wszystko dziedziczy Figtree z `body`.
- **Spacing / rozmiary** — `marginBottom`, `padding`, `gap` porównane do wartości z Figmy.

**Pozostałe sygnały:**

- `browser_take_screenshot` — dowód „przed/po" (ta sama kombinacja viewport + motyw).
- `browser_console_messages` — po fixie zero nowych błędów (regresja).
- `browser_snapshot` — drzewo dostępności (role, nagłówki, etykiety `aria-*`).
- Przy bugach interaktywnych użyj `browser_click`/`browser_fill_form` do odtworzenia kroków
  z repro, a stan sprawdzaj asercją jak wyżej.

> Selektory i oczekiwane wartości wyprowadzaj z repro + kodu/Figmy danego buga — powyższe
> `.target-*` to przykładowe nazwy, nie sztywny kontrakt.

## Checklista zamknięcia

- [ ] Każdy punkt repro potwierdzony w kodzie (plik:linia).
- [ ] Bug backendowy → zatrzymany i zgłoszony (`ZebraniBE` jest puste), nie „załatany" w FE.
- [ ] **Playwright BEFORE:** asercja odtwarza buga na wszystkich czterech kombinacjach
      (mobile 360×530 / desktop 1280×720 × Light / Dark) + screenshot każdej.
- [ ] Poprawka zgodna z CLAUDE.md: brak surowych kolorów, brak `::ng-deep` i `.p-*`,
      brak `@deprecated`, i18n w `pl.json` **i** `en.json`, dostępność WCAG AA.
- [ ] **Playwright AFTER:** te same asercje na wszystkich czterech kombinacjach potwierdzają
      brak buga; zero nowych błędów w konsoli.
- [ ] `lint:fix` + `format` → zero błędów; AXE przechodzi.
- [ ] Zestage'owane TYLKO pliki tej naprawy; niepowiązane zmiany zgłoszone.
- [ ] Commit `fix(<scope>): #<idBuga> ...` + stopka Co-Authored-By; push po wyraźnej zgodzie.
- [ ] **Deploy pre-prod:** zapytano użytkownika; przy zgodzie run zakończony sukcesem
      i numer odczytany po `headSha` (bez „ostatni + 1").
- [ ] Fix → Done; Bug → Ready for tests + przypisany do testera; Retest bez zmian.
- [ ] **Komentarz do Buga dodany** — nietechniczny opis „co naprawiono" + „jak zretestować
      ręcznie" (szerokości i motywy wprost), pierwszy punkt podaje build (`FE: <n>+`,
      `BE: N/D`) albo informację o oczekiwaniu na ręczny deploy.
- [ ] Podsumowanie + instrukcja weryfikacji przekazane użytkownikowi.
