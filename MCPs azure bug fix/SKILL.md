---
name: fix-devops-bug
description: >
  Naprawianie buga w projekcie TachoPing na podstawie linku lub numeru Azure DevOps.
  Użyj, gdy użytkownik poda link do work itema (np.
  https://dev.azure.com/DTCode/TachoPing/_workitems/edit/461) albo sam numer i poprosi
  o analizę/naprawę zgłoszenia. Skill pobiera work item i jego sub-taski (Fix/Retest),
  weryfikuje czy błąd występuje w kodzie, odtwarza buga w działającej aplikacji przez
  Playwright (test BEFORE), implementuje poprawkę zgodnie z CLAUDE.md, potwierdza
  Playwrightem że bug zniknął (test AFTER), uruchamia lint:fix + format, commituje
  i pushuje na main, a następnie aktualizuje statusy w DevOps (Fix → Done,
  Bug → Ready for tests) i przypisuje buga do testera.
language: pl
project: TachoPing
organization: DTCode
---

# Fix DevOps Bug – TachoPing

Pełny przepływ naprawy zgłoszenia z Azure DevOps: **pobierz → przeanalizuj → odtwórz buga
(Playwright) → napraw → potwierdź fix (Playwright) → zlintuj → commit/push → zaktualizuj
statusy**. Treści (commit, komentarze, plan) pisz
po polsku. Trzymaj się zasad z `.claude/CLAUDE.md` (i18n, kolory przez zmienne SCSS,
dostępność, Observable zamiast Promise itd.).

## Kontekst projektu (stałe)

- Organizacja: `DTCode`, projekt: `TachoPing`.
- **Struktura Buga:** Bug ma zwykle dwa sub-taski (Task): **„Fix"** (robi developer) i
  **„Retest"** (robi tester). Tester = osoba przypisana do „Retest".
- **Stany Buga** (dokładne nazwy): `New`, `In Progress`, `In Review`,
  `Ready for tests`, `Done`, `Rejected`, `Removed`.
- **Stany Taska:** `To Do`, `In Progress`, `Done`.
- **Git:** commity idą **bezpośrednio na `main`** (zgodnie z historią repo). Konwencja
  wiadomości: `typ(scope): #<id> opis` po polsku (np. `fix(public): #461 ...`).
- Po każdej implementacji: `npm run lint:fix` + `npm run format` (wymóg CLAUDE.md).
- **Dev server:** `npm start` (= `ng serve --host 0.0.0.0`) → **http://localhost:4200**.
  Strony prawne: `/public/privacy`, `/public/cookies`, `/public/terms`.
- **Viewporty testowe (stałe, obowiązkowe):** każdy test Playwright BEFORE i AFTER
  uruchamiaj na **obu** rozdzielczościach:
  - **mobile:** `360×520 px` (`browser_resize(width=360, height=520)`),
  - **desktop:** `1280×720 px` (`browser_resize(width=1280, height=720)`).

## Narzędzia

- Azure DevOps MCP (`mcp__azure-devops__*`): `wit_get_work_item`,
  `wit_get_work_items_batch_by_ids`, `wit_get_work_item_type`, `wit_update_work_item`,
  `wit_add_work_item_comment`. Schematy doładuj przez `ToolSearch`
  (`select:mcp__azure-devops__wit_get_work_item,...`).
- Figma MCP (jeśli repro odwołuje się do makiety): `get_design_context`,
  `get_variable_defs`, `get_screenshot`.
- **Playwright MCP** (`mcp__playwright__*`): `browser_navigate`, `browser_evaluate`,
  `browser_take_screenshot`, `browser_snapshot`, `browser_resize`, `browser_click`,
  `browser_wait_for`, `browser_console_messages`. Schematy doładuj przez `ToolSearch`.
- `Bash`/`PowerShell` do git, `npm`. Edycja kodu zwykłymi narzędziami plikowymi.

## Procedura

### 1. Zidentyfikuj work item

- Z linku `.../_workitems/edit/<ID>` wyciągnij `<ID>`. Jeśli użytkownik podał sam numer,
  użyj go. Projekt = `TachoPing`.
- `wit_get_work_item(id, project="TachoPing", expand="relations")` — pobierz `System.Title`,
  `Microsoft.VSTS.TCM.ReproSteps` (kroki naprawy + referencje Figma), `System.State`,
  `System.CreatedBy` oraz relacje (dzieci `Hierarchy-Forward`).
- Jeśli to **Bug**, wyłuskaj dzieci i pobierz je batchem
  `wit_get_work_items_batch_by_ids([...])` — znajdź Task **„Fix"** i Task **„Retest"**.
  Zapamiętaj `AssignedTo` z „Retest" (to tester).

### 2. Zweryfikuj, czy błąd występuje w kodzie

- Przeczytaj wskazane w repro pliki/komponenty (Grep/Glob/Read). **Potwierdź każdy punkt
  zgłoszenia faktem z kodu** (plik + linia). Nie zakładaj — sprawdź.
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
  `http://localhost:4200`). Backendowe ekrany wymagają działającego BE — jeśli strona
  zależy od BE, a go nie ma, zgłoś to i ustal z użytkownikiem.
- `browser_navigate` na właściwą trasę. **Przetestuj na obu stałych viewportach**
  (`browser_resize`): najpierw **mobile 360×520**, potem **desktop 1280×720**. Na każdym
  viewporcie ponów nawigację/odświeżenie, jeśli układ zależy od szerokości.
- Na **każdym** viewporcie wykonaj asercje (`browser_evaluate`) i zrób screenshot
  (`browser_take_screenshot`) jako dowód „przed". **Zapisz wynik baseline osobno dla
  mobile (360×520) i desktop (1280×720).**
- Jeśli bug z natury dotyczy tylko jednej szerokości (np. czysto mobilny), i tak uruchom
  asercję na obu viewportach — na drugim potwierdzasz brak problemu (baseline „zdrowy").
- Jeśli buga **nie da się odtworzyć** (asercja „przed" nie potwierdza problemu) —
  zatrzymaj się i skonsultuj z użytkownikiem; nie naprawiaj na ślepo.

### 4. Zaplanuj i wprowadź poprawkę

- Trzymaj się kierunku z repro i zasad CLAUDE.md. Reużywaj istniejących wzorców/zmiennych.
- Jeśli zgłoszenie dotyczy wielu bliźniaczych komponentów (jak strony prawne), zastosuj
  zmianę spójnie we wszystkich.
- Przy decyzjach niejednoznacznych (zakres, wartości z Figmy, branch vs main) użyj
  `AskUserQuestion` zamiast zgadywać.

### 5. Finalizacja kodu (wymóg CLAUDE.md)

```bash
npm run lint:fix
npm run format
```

Jeśli po `lint:fix` zostają błędy — przeczytaj i napraw ręcznie, powtórz aż do zera.

### 6. Zweryfikuj fix w działającej aplikacji — Playwright (AFTER)

**Obowiązkowe przed commitem.** Na tej samej trasie i na **obu** viewportach co krok 3
(**mobile 360×520** oraz **desktop 1280×720**) powtórz te same asercje i potwierdź, że bug
**zniknął**.

- Jeśli dev server był podniesiony, poczekaj na hot-reload (`browser_wait_for`) lub
  odśwież (`browser_navigate` ponownie).
- Dla **każdego** viewportu (`browser_resize` → 360×520, potem 1280×720) powtórz asercje
  (`browser_evaluate`) — teraz muszą zwracać stan oczekiwany (np. navy-700, brak poziomego
  scrolla). Zrób screenshot „po" na każdym viewporcie do porównania z odpowiednim baseline.
- Sprawdź **brak regresji**: `browser_console_messages` (zero nowych błędów) i szybki rzut
  oka na sąsiednie ekrany dzielące te same komponenty (np. wszystkie 3 strony prawne).
- **Jeśli asercja „po" na którymkolwiek viewporcie nadal pokazuje buga — NIE commituj.**
  Wróć do kroku 4 i popraw.

### 7. Commit + push na main -- zrób to tylko jeżeli wprost ci powiem, że masz pushować bezpośrednio na main

> ⚠️ **Pułapka:** `npm run lint:fix` potrafi zmodyfikować **niepowiązane** pliki
> (autofix). Sprawdź `git status` i **zestage'uj wyłącznie pliki, które świadomie
> zmieniłeś dla tego buga** (`git add <konkretne pliki>`), nigdy `git add -A`.
> Niepowiązane zmiany zostaw nietknięte i zgłoś je użytkownikowi.

- Pokaż `git diff --stat` zestage'owanych plików i **proponowaną treść commita** do
  akceptacji.
- Commit (stopka obowiązkowa):

```
fix(<scope>): #<id> <krótki opis po polsku>

<opcjonalnie 1–3 linie szczegółów>

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
```

- `git push origin main`.
- (Jeśli użytkownik woli PR: utwórz branch `fix/<id>-<slug>`, push, `repo_create_pull_request`
  z linkiem do work itema — zapytaj, gdy nie jest jasne.)

### 8. Zaktualizuj statusy w Azure DevOps (po udanym pushu)

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
- **Obowiązkowo** dodaj komentarz do Buga opisujący **co zostało naprawione** oraz **jak
  to zretestować ręcznie**. Pisz **nietechnicznie** — tak, żeby tester (nie programista)
  zrozumiał, co sprawdzić i jakiego efektu oczekiwać. Nie wklejaj kodu ani nazw
  plików/zmiennych; opisz zachowanie aplikacji z punktu widzenia użytkownika. Hash commita
  możesz dodać na końcu jako odnośnik. Użyj
  `wit_add_work_item_comment(workItemId=<bug>, project="TachoPing", comment=...)`.

  Szablon komentarza:

  ```
  Co zostało naprawione:
  <1–3 zdania prostym językiem, co teraz działa poprawnie>

  Jak zretestować ręcznie:
  1. <krok po kroku: gdzie wejść, co kliknąć / jaki ekran otworzyć, jaki viewport>
  2. <co należy zaobserwować — oczekiwany, poprawny efekt>
  3. <ewentualnie: gdzie wcześniej był błąd, żeby tester wiedział na co patrzeć>

  Naprawiono na main (commit <hash>).
  ```

### 9. Podsumuj użytkownikowi

Wypisz: które punkty potwierdzone w kodzie, **wynik testów Playwright (before → after** z
asercjami), zmienione pliki, hash commita, nowe statusy (#Fix=Done, #Bug=Ready for tests →
tester) oraz ewentualne niepowiązane zmiany pominięte w commicie. Załącz/wskaż screenshoty
„przed/po" i porównanie z Figmą.

## Testowanie w Playwright (MCP)

Zasada: **zamień każdy punkt repro w mierzalną asercję** i sprawdź ją tym samym kodem
przed i po fixie. Screenshot jest dowodem pomocniczym, ale werdykt daje `browser_evaluate`
(deterministyczny), nie „oko".

**Dwa obowiązkowe viewporty:** każdą asercję (BEFORE i AFTER) uruchamiaj na **mobile
360×520** (`browser_resize(360, 520)`) i **desktop 1280×720** (`browser_resize(1280, 720)`).
Trzymaj baseline i screenshot osobno dla każdego z nich.

**Start serwera:** odpal `npm start` w tle i poczekaj aż odpowie `http://localhost:4200`,
zanim wejdziesz `browser_navigate`. Po naprawie poczekaj na hot-reload przed asercją „po".

**Wzorce asercji (`browser_evaluate`):**

- **Kolor** — porównaj computed color do oczekiwanego RGB (np. navy-700 `#334e68` =
  `rgb(51, 78, 104)`; slate-800 `#1e293b` = `rgb(30, 41, 59)`):
  ```js
  () => getComputedStyle(document.querySelector('.cookie__title')).color
  ```
- **Poziomy scroll / wyjście poza kontener** — element się przewija, gdy `scrollWidth`
  przekracza `clientWidth`:
  ```js
  () => { const t = document.querySelector('.cookie__table-wrap');
    return { scrollW: t.scrollWidth, clientW: t.clientWidth, overflows: t.scrollWidth > t.clientWidth }; }
  ```
  (BEFORE: `overflows: true`; AFTER: `false`). Uruchom na obu stałych viewportach:
  `browser_resize(360, 520)` (mobile) i `browser_resize(1280, 720)` (desktop), i powtórz.
- **Spacing / rozmiary** — czytaj `getComputedStyle(el).marginBottom` / `fontSize` itp.
  i porównaj do wartości z Figmy.

**Pozostałe sygnały:**

- `browser_take_screenshot` — dowód „przed/po" (ten sam viewport i trasa).
- `browser_console_messages` — po fixie zero nowych błędów (regresja).
- `browser_snapshot` — drzewo dostępności (np. że tabela ma nadal `<th>`/role).
- Przy bugach interaktywnych użyj `browser_click`/`browser_fill_form` do odtworzenia kroków
  z repro, a stan sprawdzaj asercją jak wyżej.

> Selektory i oczekiwane wartości wyprowadzaj z repro + kodu/Figmy danego buga — powyższe
> `.cookie__*` to przykład ze stron prawnych, nie sztywny kontrakt.

## Checklista zamknięcia

- [ ] Każdy punkt repro potwierdzony w kodzie (plik:linia).
- [ ] **Playwright BEFORE:** asercja odtwarza buga na **mobile 360×520** i **desktop 1280×720** (+ screenshot każdy).
- [ ] Poprawka zgodna z CLAUDE.md (i18n, kolory ze zmiennych, dostępność, Observable).
- [ ] **Playwright AFTER:** ta sama asercja na **mobile 360×520** i **desktop 1280×720** potwierdza brak buga; zero nowych błędów w konsoli.
- [ ] `lint:fix` + `format` → zero błędów.
- [ ] Zestage'owane TYLKO pliki tej naprawy; niepowiązane zmiany zgłoszone.
- [ ] Commit `fix(scope): #<id> ...` + stopka Co-Authored-By; push na `main`.
- [ ] Fix → Done; Bug → Ready for tests + przypisany do testera; Retest bez zmian.
- [ ] **Komentarz do Buga dodany** — nietechniczny opis „co naprawiono" + „jak zretestować ręcznie".
- [ ] Podsumowanie + instrukcja weryfikacji przekazane użytkownikowi.