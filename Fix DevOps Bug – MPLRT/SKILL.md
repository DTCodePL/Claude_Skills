---
name: fix-devops-bug-mplrt
description: >
  Naprawianie buga w projekcie MPLRT na podstawie linku lub numeru Azure DevOps.
  Użyj, gdy użytkownik poda link do work itema (np.
  https://dev.azure.com/DTCode/MPLRT/_workitems/edit/123) albo sam numer i poprosi
  o analizę/naprawę zgłoszenia. Skill pobiera work item i jego sub-taski (Fix/Retest),
  weryfikuje czy błąd występuje w kodzie, odtwarza buga w działającej aplikacji przez
  Playwright na macierzy ekranów odniesienia (telefon 360×560, tablet 768×1024, HD 1280×720, każdy w motywie jasnym i ciemnym)
  — test BEFORE, implementuje poprawkę zgodnie z CLAUDE.md, potwierdza Playwrightem
  że bug zniknął (test AFTER), sprawdza zgodność dokumentacji produktowej (źródła
  prawdy) z poprawką i ją aktualizuje, uruchamia lint:fix + format, commituje i pushuje,
  obsługuje deploy pre-prod, a następnie aktualizuje statusy
  w DevOps (Fix → Done, Bug → Ready for tests) i przypisuje buga do testera.
version: '1.0'
language: pl
project: MPLRT
organization: DTCode
remote:
  github_raw: 'https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/Fix%20DevOps%20Bug%20%E2%80%93%20MPLRT/SKILL.md'
  github_page: 'https://github.com/DTCodePL/Claude_Skills/blob/main/Fix%20DevOps%20Bug%20%E2%80%93%20MPLRT/SKILL.md'
---

# Fix DevOps Bug – MPLRT

Pełny przepływ naprawy zgłoszenia z Azure DevOps: **pobierz → przeanalizuj (kod
i dokumentacja) → odtwórz buga (Playwright) → napraw → potwierdź fix (Playwright) →
sprawdź zgodność dokumentacji → zlintuj → commit/push → deploy → zaktualizuj statusy**.
Treści (commit, komentarze, plan) pisz po polsku. Trzymaj się zasad
z `.claude/CLAUDE.md` w `MPLRT_FE` (i18n wyłącznie w `pl`, kolory wyłącznie z tokenów,
Signal Forms, Observable zamiast Promise, brak `@deprecated`, dostępność WCAG AA).
Obowiązuje reguła **„Kod dla człowieka, nie dla agentów”** (właściciel, 2026-11-20):
kod łatwo czytelny dla człowieka bez historii zadania, proste nazwy i przepływ,
wczesne returny, bez sprytnych jednolinijkowców i abstrakcji „na zapas”, jedna deklaracja
na plik, komentarz wyjaśnia „dlaczego” w 1–3 zdaniach.

## Kontekst projektu (stałe)

- Organizacja: `DTCode`, projekt: **`MPLRT`**, team `MPLRT Team` (id `9dd0b33d-cfd4-4a55-a01f-6b702f9f1bdc`).
  Iteracje: `MPLRT\Sprint 1` (bieżąca) … `Sprint 6` (brak dedykowanej iteracji E2e).
- **Struktura Buga:** Bug ma zwykle dwa sub-taski (Task): **„Fix"** (robi developer: `kontakt@DTCode.pl`) i
  **„Retest"** (robi tester: `Piotr.Tunski@DTCode.pl`, Piotr Tuński). Tester = osoba przypisana do „Retest".
- **Stany Buga** (odczytane z API 2026-11-24, dokładne nazwy): `New`, `In Progress`,
  `In Review`, `Ready for tests`, `Ready for Review`, `QA Blocked`, `Conflict`, `Done`, `Postponed`, `Rejected`, `Removed`.
- **Stany Taska:** `To Do`, `In Progress`, `In Review`, `Ready for tests`, `Ready for Review`,
  `QA Blocked`, `Conflict`, `Done`, `Postponed`, `Rejected`, `Removed`.
- **Stany PBI:** `New`, `Ready to develop`, `In Progress`, `In Review`, `Ready for tests`,
  `Ready for Review`, `QA Blocked`, `Conflict`, `Done`, `Postponed`, `Rejected`, `Removed`.
- **Repozytoria:**
  - FE: `DTCodePL/MPLRTFE` — `d:\projects\DTCode\MPLRT_FE` (Angular 22, SSR, zoneless).
  - BE: `DTCodePL/MPLRTBE` — **repozytorium jest puste (samo README)**. Backend MPLRT
    dopiero powstaje (patrz „Bug backendowy" niżej).
- **Dokumentacja produktowa — źródło prawdy:** `d:\projects\DTCode\Dokumentacja\MPLRT`
  (osobne repozytorium; przed zmianą przeczytaj jego `AGENTS.md` i stosuj `INSTRUKCJA-DLA-AI.md`).
  Kod, testy, przypadki QA Sphere i makiety idą za nią — nigdy odwrotnie. Status
  w front matter: `zatwierdzony` wiąże; `do-weryfikacji` to propozycja czekająca na
  decyzję; `szkic` jeszcze nie jest wymaganiem; `wycofany` to historia i nigdy nie jest
  podstawą poprawki. **Każda naprawa sprawdza dokumentację i — gdy trzeba — aktualizuje
  ją w tej samej naprawie** (kroki 2, 4 i 6b). Naprawa z nieaktualną dokumentacją nie
  jest skończona — nie zamykasz jej w ADO.
- **Git:** commity idą na `main`. Konwencja wiadomości: `fix(<scope>): #<idBuga> opis`
  po polsku (np. `fix(public): #123 ...`).
  - CLAUDE.md wymaga numeru work itema w commicie — **numer buga tę regułę
    spełnia**. Nie doklejaj numeru PBI rodzica i nie wymyślaj go.
- Po każdej implementacji: `npm run lint:fix` + `npm run format` (wymóg CLAUDE.md).
- **Dev server:** `npm start` (= `ng serve`) → **http://localhost:4200**.
  Konkretne trasy do przetestowania wyprowadź z repro / work itema (nie zakładaj stałej listy).
- **Środowisko pre-prod:** **nie istnieje** — serwery, porty i workflow nie zostały jeszcze
  ustalone (`AT-DOMENA-I-HOSTING`). Nigdy nie kieruj testera na `mplrt.eu` (produkcja nie istnieje).

### Macierz testowa — 3 ekrany odniesienia × 2 motywy (stała, obowiązkowa)

Każdy test Playwright BEFORE i AFTER uruchamiaj na **sześciu** kombinacjach — ekrany odniesienia
z `Dokumentacja\MPLRT\wymagania-przekrojowe\czytelnosc-i-nawigacja.md` × oba motywy:

| Klasa | Ekran odniesienia | Rozdzielczość | Light | Dark |
| --- | --- | --- | --- | --- |
| **Telefon** | format telefonu | `360×560` | baseline T-L | baseline T-D |
| **Tablet** | tablet pionowo | `768×1024` | baseline TAB-L | baseline TAB-D |
| **HD** | format HD | `1280×720` | baseline HD-L | baseline HD-D |

- `browser_resize(width=360, height=560)` — telefon (mobile-first).
- `browser_resize(width=768, height=1024)` — tablet.
- `browser_resize(width=1280, height=720)` — HD.
- Ekran szerszy niż HD sprawdzasz tylko wtedy, gdy zgłoszenie go dotyczy.
- Light + Dark są w MPLRT **obowiązkowe na całej stronie**, panel redaktora włącznie (`DEC-MOTYW-JASNY-I-CIEMNY`).
  Regresje tokenów kolorów najczęściej ujawniają się tylko w jednym motywie — dlatego
  oba są w macierzy także dla bugów, które „wyglądają na niezwiązane z kolorem”.

## Narzędzia

- Azure DevOps MCP (`mcp__azure-devops__*`): `wit_get_work_item`,
  `wit_get_work_items_batch_by_ids`, `wit_get_work_item_type`, `wit_update_work_item`,
  `wit_add_work_item_comment` (oraz skrypt pomocniczy `ado-wi.py`). Schematy doładuj przez `ToolSearch`.
  - ⚠️ Jeśli MCP/API zwróci `203` albo stronę logowania — **PAT wygasł**. Zgłoś to
    użytkownikowi i zatrzymaj część devopsową; nie obchodź tego innym tokenem.
- Figma MCP (warunkowo, gdy ekran ma makietę w pliku MPLRT, fileKey `4wlzvrRUg5fr89LjGDS5Bd`):
  `get_design_context`, `get_variable_defs`, `get_screenshot`. Ekran bez makiety opisuje wyłącznie
  dokumentacja w `interfejsy/`. Biblioteka `Primeng Design system (MPLRT)` jest kopią Zebrani
  w trakcie dostosowania — jej kolory i fonty Zebrani nie są wzorcem MPLRT.
- **Playwright MCP** (`mcp__playwright__*`): `browser_navigate`, `browser_evaluate`,
  `browser_take_screenshot`, `browser_snapshot`, `browser_resize`, `browser_click`,
  `browser_wait_for`, `browser_console_messages`. Schematy doładuj przez `ToolSearch`.
- **MSSQL MCP** (`mcp__mssql__execute_sql`) — 🛈 **na dziś nieaktywne dla MPLRT:
  backend i baza jeszcze nie istnieją, `MPLRTBE` to samo README. Pomiń tę sekcję,
  dopóki BE nie ruszy.** Gdy baza powstanie, obowiązują poniższe zasady:
  - ✅ **Bez pytania dozwolone tylko odczyty** — wyłącznie `SELECT` (ewentualnie
    `SELECT` w CTE). Nic, co zmienia stan bazy.
  - ⛔ **Każda zmiana danych lub schematu wymaga wcześniejszej zgody użytkownika.** Zanim
    wykonasz `INSERT`, `UPDATE`, `DELETE`, `MERGE` albo DDL (`ALTER`, `CREATE`, `DROP`,
    `TRUNCATE`) — **zatrzymaj się i wprost zapytaj o akceptację** (`AskUserQuestion`),
    podając dokładne zapytanie SQL i czego dotyczy.
  - 🛈 Zmiany schematu i tak realizujemy przez **numerowane skrypty SQL**
    (`MPLRTBE/Scripts/Script{NNNNN}...`, wymóg CLAUDE.md), a nie przez ten MCP.
- `Bash`/`PowerShell` do git, `npm`. Edycja kodu zwykłymi narzędziami plikowymi.
- **`gh` CLI** (GitHub) — krok deployu pre-prod na dziś nieaktywny (środowisko jeszcze nie istnieje).

## Procedura

### 1. Zidentyfikuj work item

- Z linku `.../_workitems/edit/<ID>` wyciągnij `<ID>`. Jeśli użytkownik podał sam numer,
  użyj go. Projekt = `MPLRT`.
- `wit_get_work_item(id, project="MPLRT", expand="relations")` — pobierz `System.Title`,
  `Microsoft.VSTS.TCM.ReproSteps` (kroki naprawy + referencje), `System.State`,
  `System.CreatedBy` oraz relacje (dzieci `Hierarchy-Forward`).
- Jeśli to **Bug**, wyłuskaj dzieci i pobierz je batchem
  `wit_get_work_items_batch_by_ids([...])` — znajdź Task **„Fix"** i Task **„Retest"**.
  Zapamiętaj `AssignedTo` z „Retest" (to tester: `Piotr.Tunski@DTCode.pl`).

### 2. Zweryfikuj, czy błąd występuje w kodzie

- Przeczytaj wskazane w repro pliki/komponenty (Grep/Glob/Read). **Potwierdź każdy punkt
  zgłoszenia faktem z kodu** (plik + linia). Nie zakładaj — sprawdź.
- **Znajdź źródło prawdy w dokumentacji** dla zachowania ze zgłoszenia: wyszukaj
  w `Dokumentacja\MPLRT` po nazwie ekranu, reguły, napisie i ID (`interfejsy/`,
  `reguly-biznesowe/`, `procesy-biznesowe/`, `wymagania-przekrojowe/`, `decyzje/`)
  i zapisz **mapę dokumentacji**: dokument, sekcja, `id`, `status` — albo jawnie „brak
  dokumentu opisującego to zachowanie". Potem ustal przypadek:
  - dokument opisuje zachowanie, którego oczekuje zgłoszenie, a kod od niego odbiega —
    to błąd; poprawka idzie za dokumentem;
  - żaden dokument tego zachowania nie opisuje (albo opisuje je tylko `szkic` /
    `do-weryfikacji`, które nie wiążą) — naprawiasz i dopisujesz je do dokumentacji
    w kroku 6b;
  - dokument opisuje zachowanie, które zgłoszenie nazywa błędem, albo zgłoszenie żąda
    czegoś innego niż dokument — to nie bug, tylko zmiana wymagania: **zatrzymaj się
    i zapytaj użytkownika** (`AskUserQuestion`, z cytatem dokumentu i zgłoszenia);
    nigdy nie naprawiasz wbrew dokumentowi;
  - dwa dokumenty sobie przeczą — zatrzymaj się; konflikt idzie do `kwestie-otwarte/`
    (§13 instrukcji repo), decyzja należy do człowieka.
- **Bug backendowy:** jeśli repro dotyczy API, danych, bazy albo logiki serwerowej —
  `MPLRTBE` jest puste, więc nie ma czego naprawiać. **Zatrzymaj się, zgłoś to
  użytkownikowi i zapytaj o dalsze kroki.** Nie szukaj „gdzieś indziej" i nie próbuj
  załatać tego w FE, jeśli zgłoszenie tego nie mówi wprost.
- Jeśli repro dotyczy koloru, kontrastu albo powierzchni — sprawdź tokeny
  w presetach motywu. Pamiętaj o pułapce Aury: wypełnione warianty przycisku żyją pod
  `button.root.<severity>`, a token wpisany w złej ścieżce jest **po cichu ignorowany**
  (brak błędu kompilacji). Kolory zawsze z tokenów.
- Jeśli repro odwołuje się do Figmy: gdy ekran nie ma makiety w pliku MPLRT, odnieś się do specyfikacji
  ekranu w `Dokumentacja\MPLRT\interfejsy/`. Gdy makieta istnieje — pobierz kontekst węzła przez Figma MCP.
- Jeśli błędu **nie ma** w kodzie (np. już naprawiony) — zatrzymaj się, zgłoś to
  użytkownikowi i zapytaj o dalsze kroki zamiast „naprawiać na siłę".

### 3. Odtwórz buga w działającej aplikacji — Playwright (BEFORE)

**Obowiązkowe przed naprawą.** Najpierw zamień każdy punkt repro na **mierzalną asercję**
(patrz „Testowanie w Playwright"), potem uruchom aplikację i potwierdź, że bug realnie
występuje.

- Upewnij się, że dev server działa (`npm start` w tle; poczekaj aż wstanie na
  `http://localhost:4200`). Ekrany zależne od backendu **nie zadziałają** — BE nie istnieje;
  jeśli repro tego wymaga, zgłoś to i ustal z użytkownikiem.
- `browser_navigate` na właściwą trasę, a następnie przejdź **całą macierz 3×2**:
  1. `browser_resize(360, 560)` → Light → asercja + screenshot
  2. `browser_resize(360, 560)` → Dark → asercja + screenshot
  3. `browser_resize(768, 1024)` → Light → asercja + screenshot
  4. `browser_resize(768, 1024)` → Dark → asercja + screenshot
  5. `browser_resize(1280, 720)` → Light → asercja + screenshot
  6. `browser_resize(1280, 720)` → Dark → asercja + screenshot
- Po każdej zmianie szerokości ponów nawigację/odświeżenie, jeśli układ zależy od szerokości.
- **Zapisz sześć baseline'ów osobno** — porównanie „po" robisz parami, nie zbiorczo.
- Jeśli bug z natury dotyczy jednej kombinacji (np. tylko Dark na telefonie), i tak uruchom
  asercję na wszystkich sześciu — pozostałe potwierdzają baseline „zdrowy".
- Jeśli buga **nie da się odtworzyć** (asercja „przed" nie potwierdza problemu) —
  zatrzymaj się i skonsultuj z użytkownikiem; nie naprawiaj na ślepo.

#### Przełączanie motywu Light ⇄ Dark

Motyw w MPLRT steruje serwis `ThemeMode` (`core/theme/`), który przełącza klasę
`.app-dark` na elemencie root. SSR **zawsze renderuje Light** — motyw z pamięci wraca
dopiero po hydracji. Aplikacja i przełącznik jeszcze nie istnieją, a sposób wyboru
motywu przez odwiedzającego jest otwarty (`KO-NAWIGACJA-I-MATERIALY`), więc dopóki
przełącznika nie ma w interfejsie, używasz fallbacku.

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
- Stosuj zasadę **„Kod dla człowieka, nie dla agentów”** (właściciel, 2026-11-20):
  kod łatwo czytelny dla człowieka bez historii zadania, proste nazwy i przepływ,
  wczesne returny, bez sprytnych jednolinijkowców i abstrakcji „na zapas”, jedna deklaracja na plik.
  Komentarz wyjaśnia „dlaczego” w 1–3 zdaniach prostymi słowami.
- Poprawka realizuje zachowanie z dokumentów z mapy (krok 2). Gdy w trakcie naprawy
  okaże się, że kod musi zachować się inaczej, niż mówi dokument (ograniczenie
  techniczne, przypadek brzegowy, którego dokument nie przewidział), **od razu**
  zanotuj to jako rozbieżność do kroku 6b — nie odkładaj na koniec. Jeśli zmienia to
  regułę biznesową, zachowanie widoczne dla użytkownika albo napis z dokumentu
  `zatwierdzony`, zatrzymaj się i zapytaj, zanim to wdrożysz.
- **Nigdy nie wprowadzaj surowego koloru** (hex/rgb/hsl) — kolory pochodzą wyłącznie
  z tokenów `var(--p-*)` / `dt('…')`. Jeśli żaden istniejący token nie pasuje — **zatrzymaj się
  i zapytaj**, zamiast dodawać nowy jednostronnie.
- **Nie nadpisuj PrimeNG własnym CSS** — bez `::ng-deep`, bez celowania w `.p-*`.
  Poprawki wyglądu komponentów PrimeNG idą przez preset Aury.
- Jeśli zgłoszenie dotyczy wielu bliźniaczych komponentów (powtarzalne sekcje/strony),
  zastosuj zmianę spójnie we wszystkich.
- Przy decyzjach niejednoznacznych użyj `AskUserQuestion` zamiast zgadywać.

### 5. Finalizacja kodu (wymóg CLAUDE.md)

```bash
npm run lint:fix   # eslint --fix + stylelint --fix
npm run format     # prettier --write .
```

Jeśli po `lint:fix` zostają błędy — przeczytaj i napraw ręcznie, powtórz aż do zera.

Dodatkowo zweryfikuj (wymogi CLAUDE.md MPLRT):

- każdy nowy/zmieniony klucz i18n istnieje w `src/assets/i18n/pl.json` (zgodnie z decyzją C3 jedyny plik i język to `pl`, brak pliku `en.json`),
- zero hardkodowanych kolorów poza konfiguracją motywu,
- zero użyć symboli `@deprecated` (m.in. `p-button`, `MultiSelect`, `withFetch()`),
- AXE przechodzi.

### 6. Zweryfikuj fix w działającej aplikacji — Playwright (AFTER)

**Obowiązkowe przed commitem.** Na tej samej trasie powtórz asercje na **całej macierzy
3×2** (telefon `360×560`, tablet `768×1024`, HD `1280×720` × Light / Dark) i potwierdź, że bug **zniknął**.

- Jeśli dev server był podniesiony, poczekaj na hot-reload (`browser_wait_for`) lub
  odśwież (`browser_navigate` ponownie).
- Dla **każdej z sześciu kombinacji** powtórz asercje (`browser_evaluate`) — teraz muszą
  zwracać stan oczekiwany. Zrób screenshot „po" do porównania z **odpowiadającym**
  baseline'em (T-L z T-L, T-D z T-D, HD-L z HD-L, HD-D z HD-D, FHD-L z FHD-L, FHD-D z FHD-D).
- Sprawdź **brak regresji**: `browser_console_messages` (zero nowych błędów) i szybki rzut
  oka na sąsiednie ekrany dzielące te same komponenty.
- **Jeśli asercja „po" w którejkolwiek kombinacji nadal pokazuje buga — NIE commituj.**
  Wróć do kroku 4 i popraw.

### 6b. Przegląd zgodności dokumentacji z poprawką (przed commitem)

**Obowiązkowe w każdej naprawie, także czysto wizualnej.** Po potwierdzonym AFTER
porównaj mapę dokumentacji z kroku 2 i rozbieżności z kroku 4 z tym, co faktycznie
zmieniłeś (`git diff`, `git status`) — w obie strony:

- **dokument → kod:** każde twierdzenie z sekcji mapy, którego dotyka poprawka
  (zachowanie, stan ekranu, napis — tekst dokumentu wobec `pl.json`,
  walidacja, limit, komunikat błędu, kontrakt API), zgadza się z kodem po poprawce;
- **kod → dokument:** każde zachowanie, napis i reguła z poprawki, widoczne dla
  użytkownika albo istotne biznesowo, jest opisane w źródle prawdy, nie w kopii.

Wynik zapisz jako macierz (trafi do podsumowania w kroku 9):

| Dokument › sekcja (id, `status`) | Twierdzenie albo zachowanie | Kod (`plik:linia`) | Werdykt | Akcja |
| --- | --- | --- | --- | --- |

Werdykty: `zgodne` · `dokument nieaktualny` · `kod odbiega` · `brak w dokumencie` · `brak w kodzie`.

- `kod odbiega` / `brak w kodzie` → poprawka nie jest skończona: wróć do kroku 4,
  potem powtórz AFTER (krok 6).
- `dokument nieaktualny` / `brak w dokumencie` → aktualizujesz dokumentację **teraz**,
  wg procedury repo (`INSTRUKCJA-DLA-AI.md`: modyfikacja wymagania §10, kontrola wpływu
  §12, raport końcowy §17):
  - `szkic` / `do-weryfikacji` — zmiana wprost w treści, status bez zmian;
  - `zatwierdzony` — datowana rewizja (`## Rewizja RRRR-MM-DD — …`) i zmiana **treści
    normatywnej**, nie samego znacznika rewizji. Treść rewizji (co obowiązywało, co
    obowiązuje) pokazujesz użytkownikowi i bez jego zgody jej nie commitujesz — AI nie
    zatwierdza dokumentów;
  - decyzja produktowa, której nikt nie podjął — pytanie do użytkownika, nie rewizja
    z domysłu.
- Naprawa, która nie zmienia niczego opisanego w dokumentacji i niczego do niej nie
  dodaje (np. drobna korekta marginesu), kończy się macierzą „wszystko
  `zgodne`" albo „brak dokumentu w zakresie" z uzasadnieniem — nigdy pominięciem kroku.

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
- **Dokumentacja w tym samym kroku, nigdy „później":** osobny commit w repo
  `d:\projects\DTCode\Dokumentacja\MPLRT` — `git add` wyłącznie plików zmienionych
  w kroku 6b, wiadomość `docs(<scope>): #<idBuga> <krótki opis po polsku>` z tą samą stopką,
  push razem z kodem. Rewizja dokumentu `zatwierdzony` wchodzi do commita tylko po zgodzie
  użytkownika z kroku 6b.
- (Jeśli użytkownik woli PR: utwórz branch `fix/<idBuga>-<slug>`, push, PR z linkiem do
  work itema — zapytaj, gdy nie jest jasne.)

### 8. Deploy pre-prod i aktualizacja statusów w Azure DevOps

#### 8a. Deploy pre-prod — środowisko jeszcze nie istnieje

W projekcie MPLRT środowisko pre-prod jeszcze **nie istnieje** — serwery, porty, baza danych
ani workflow GitHub Actions nie zostały skonfigurowane (kontrakt B oraz sekcja „Environments” w `AGENTS.md`).

- Krok deployu jest **pomijany i zgłaszany użytkownikowi**.
- Poinformuj użytkownika: *„Środowisko pre-prod jeszcze nie istnieje — deploy został pominięty. Fix znajduje się na gałęzi `main`.”*
- Nie uruchamiaj żadnego workflow ani nie zakładaj adresu hosta, dopóki sekcja „Environments” w `AGENTS.md` repozytorium nie poda serwera i nazwy workflow.
- Do komentarza w work itemie wpisz informację: `Fix jest na main — środowisko pre-prod nie istnieje / wymaga konfiguracji i wdrożenia.`

#### 8b. Statusy

Statusy zmieniasz dopiero, gdy dokumentacja jest zaktualizowana i wypchnięta razem
z kodem albo krok 6b wykazał „bez zmian" z uzasadnieniem.

- Task **„Fix"** → `Done`:
  `wit_update_work_item(id=<fix>, [{op:"add", path:"/fields/System.State", value:"Done"}])`
- **Bug** → `Ready for tests` **i** przypisz testerowi (assignee z „Retest”, czyli `Piotr.Tunski@DTCode.pl`):

  ```
  wit_update_work_item(id=<bug>, [
    {op:"add", path:"/fields/System.State", value:"Ready for tests"},
    {op:"add", path:"/fields/System.AssignedTo", value:"Piotr.Tunski@DTCode.pl"}
  ])
  ```

- Task **„Retest"** — **bez zmian** (czeka na test).

#### 8c. Komentarz do Buga (obowiązkowy)

Dodaj komentarz opisujący **co zostało naprawione** oraz **jak to zretestować ręcznie**.
Pisz **nietechnicznie** — tak, żeby tester (nie programista) zrozumiał, co sprawdzić
i jakiego efektu oczekiwać. Nie wklejaj kodu ani nazw plików/zmiennych. Hash commita
możesz dodać na końcu jako odnośnik. **Pierwszy punkt sekcji „Co zostało naprawione"
podaje status wdrożenia.** Użyj
`wit_add_work_item_comment(workItemId=<bug>, project="MPLRT", comment=...)`.

Szablon:

```
Co zostało naprawione:
Fix jest na main (środowisko pre-prod jeszcze nie istnieje — deploy pominięty, retest lokalny na dev serverze lub po wdrożeniu środowiska).
<1–3 zdania prostym językiem, co teraz działa poprawnie>

Jak zretestować ręcznie:
1. <gdzie wejść, co kliknąć / jaki ekran otworzyć>
2. <na jakiej szerokości: telefon (360×560), tablet (768×1024) lub HD (1280×720)>
3. <w jakim motywie: jasny i ciemny — jeśli zgłoszenie dotyczyło wyglądu>
4. <co należy zaobserwować — oczekiwany, poprawny efekt>
5. <ewentualnie: gdzie wcześniej był błąd, żeby tester wiedział na co patrzeć>

<tylko gdy zmieniła się dokumentacja: Dokumentacja: <jednym zdaniem, który opis albo
regułę uzupełniono — prostym językiem, bez nazw plików>>

Naprawiono na main (commit <hash>).
```

### 9. Podsumuj użytkownikowi

Wypisz: które punkty potwierdzone w kodzie (plik:linia), **wynik testów Playwright
(before → after) dla wszystkich sześciu kombinacji (3 ekrany odniesienia × Light / Dark)**, zmienione pliki, hash commita,
informację o pominięciu deployu (brak środowiska pre-prod), nowe statusy (#Fix=Done,
#Bug=Ready for tests → tester) oraz ewentualne niepowiązane zmiany pominięte w commicie.
Wskaż screenshoty „przed/po" i zgodność ze specyfikacją interfejsów / Figmą. Punkt **„Dokumentacja"**: mapa
z kroku 2, macierz z kroku 6b (każda rozbieżność z rozstrzygnięciem), zmienione pliki
dokumentacji i hash commita w repo `Dokumentacja`, rewizje czekające na zgodę — albo
„bez zmian" z uzasadnieniem.

## Testowanie w Playwright (MCP)

Zasada: **zamień każdy punkt repro w mierzalną asercję** i sprawdź ją tym samym kodem
przed i po fixie. Screenshot jest dowodem pomocniczym, ale werdykt daje `browser_evaluate`
(deterministyczny), nie „oko".

**Sześć obowiązkowych kombinacji:** telefon `360×560`, tablet `768×1024`, HD `1280×720`, każda w Light i Dark. Trzymaj baseline i screenshot osobno dla każdej.

**Start serwera:** odpal `npm start` w tle i poczekaj aż odpowie `http://localhost:4200`,
zanim wejdziesz `browser_navigate`. Po naprawie poczekaj na hot-reload przed asercją „po".

**Wzorce asercji (`browser_evaluate`):**

- **Kolor z tokenu** — odczytaj realnie wyrenderowaną wartość i porównaj z wartością
  tokenu, a nie z wpisanym „na sztywno" RGB (kolory w MPLRT pochodzą z presetu
  PrimeNG):

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

  (BEFORE: `overflows: true`; AFTER: `false`). Uruchom na ekranach odniesienia.

- **Typografia** — `getComputedStyle(el).fontSize` / `lineHeight` / `fontWeight`
  i porównaj ze zdefiniowaną skalą typograficzną projektu. Sprawdź też, czy element **nie**
  deklaruje własnego `font-family` poza konfiguracją fontów w aplikacji.
- **Spacing / rozmiary** — `marginBottom`, `padding`, `gap` porównane do wartości ze specyfikacji / makiety.

**Pozostałe sygnały:**

- `browser_take_screenshot` — dowód „przed/po" (ta sama kombinacja ekran odniesienia + motyw).
- `browser_console_messages` — po fixie zero nowych błędów (regresja).
- `browser_snapshot` — drzewo dostępności (role, nagłówki, etykiety `aria-*`).
- Przy bugach interaktywnych użyj `browser_click`/`browser_fill_form` do odtworzenia kroków
  z repro, a stan sprawdzaj asercją jak wyżej.

> Selektory i oczekiwane wartości wyprowadzaj z repro + kodu/dokumentacji danego buga — powyższe
> `.target-*` to przykładowe nazwy, nie sztywny kontrakt.

## Checklista zamknięcia

- [ ] Każdy punkt repro potwierdzony w kodzie (plik:linia).
- [ ] Bug backendowy → zatrzymany i zgłoszony (`MPLRTBE` jest puste), nie „załatany" w FE.
- [ ] **Mapa dokumentacji** z kroku 2 (dokument, sekcja, id, status); zgłoszenie sprzeczne
      z dokumentem → zatrzymane i zgłoszone, nie „naprawione" wbrew dokumentowi.
- [ ] **Playwright BEFORE:** asercja odtwarza buga na wszystkich sześciu kombinacjach
      (telefon, tablet, HD × Light / Dark) + screenshot każdej.
- [ ] Poprawka zgodna z CLAUDE.md: brak surowych kolorów, brak `::ng-deep` i `.p-*`,
      brak `@deprecated`, i18n wyłącznie w `src/assets/i18n/pl.json`, dostępność WCAG AA,
      zasada „Kod dla człowieka, nie dla agentów”.
- [ ] **Playwright AFTER:** te same asercje na wszystkich sześciu kombinacjach potwierdzają
      brak buga; zero nowych błędów w konsoli.
- [ ] **Krok 6b:** macierz zgodności dokumentacji z poprawką; dokumentacja zaktualizowana
      (rewizja dokumentu `zatwierdzony` po zgodzie użytkownika) albo „bez zmian"
      z uzasadnieniem.
- [ ] `lint:fix` + `format` → zero błędów; AXE przechodzi.
- [ ] Zestage'owane TYLKO pliki tej naprawy; niepowiązane zmiany zgłoszone.
- [ ] Commit `fix(<scope>): #<idBuga> ...` + stopka Co-Authored-By; push po wyraźnej zgodzie.
- [ ] Commit `docs(<scope>): #<idBuga> ...` w repo `Dokumentacja` (tylko pliki tej naprawy),
      wypchnięty razem z kodem.
- [ ] **Deploy pre-prod:** pominięty z powodu braku środowiska, użytkownik poinformowany.
- [ ] Fix → Done; Bug → Ready for tests + przypisany do testera (`Piotr.Tunski@DTCode.pl`); Retest bez zmian.
- [ ] **Komentarz do Buga dodany** — nietechniczny opis „co naprawiono" + „jak zretestować
      ręcznie" (ekrany odniesienia i motywy wprost), informacja o braku środowiska pre-prod.
- [ ] Podsumowanie + instrukcja weryfikacji przekazane użytkownikowi.
