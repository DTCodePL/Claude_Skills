# Skille Azure DevOps dla Zebrani.pl — projekt

Data: 2026-08-02
Status: zatwierdzony przez użytkownika

## Cel

Dodać do repozytorium `DTCodePL/Claude_Skills` dwa skille obsługujące projekt
**Zebrani.pl** w Azure DevOps — tworzenie work itemów oraz naprawę bugów — wraz
z cienkimi loaderami zainstalowanymi w repozytorium `ZebraniFE`.

Bazą są istniejące skille UstawoŻercy; różnice wynikają wyłącznie z realnego
stanu projektu Zebrani, nie z inwencji.

## Architektura

Wzorzec z repo pozostaje bez zmian: **pełny skill na GitHubie jest źródłem
prawdy**, lokalnie leży tylko cienki loader, który pobiera go przez `curl`.

### Pliki w `Claude_Skills`

| Plik                                                | Rola                                             |
| --------------------------------------------------- | ------------------------------------------------ |
| `Azure DevOps – Zebrani Task Creation Skill/SKILL.md` | pełny skill `azure-devops-zebrani`, `version: 1.0` |
| `Azure loader Zebrani.md`                             | źródłowa kopia loadera skilla A                  |
| `Fix DevOps Bug – Zebrani/SKILL.md`                   | pełny skill `fix-devops-bug-zebrani`             |
| `fix-devops-bug-loader Zebrani.md`                    | źródłowa kopia loadera skilla B                  |

### Instalacja loaderów

Do `ZebraniFE/.claude/skills/<name>/SKILL.md`, dokładnie jak zainstalowany
`qasphere-test-generator` (`user-invocable: true`, `version: loader`,
`mode: remote-loader`):

- `ZebraniFE/.claude/skills/azure-devops-zebrani/SKILL.md`
- `ZebraniFE/.claude/skills/fix-devops-bug-zebrani/SKILL.md`

Loadery działają dopiero po wypchnięciu plików do `DTCodePL/Claude_Skills` —
wcześniej `curl` zwróci 404 i skill zatrzyma się z pytaniem (zachowanie zgodne
z jego własną instrukcją, nie błąd).

## Stałe projektu

| Pole              | Wartość                                                    |
| ----------------- | ---------------------------------------------------------- |
| Organizacja       | `DTCode`                                                   |
| Projekt ADO       | `Zebrani.pl`                                               |
| Team              | `Zebrani.pl Team`                                          |
| Iteracja domyślna | `Zebrani.pl\Sprint 1`                                      |
| Iteracja E2e      | `Zebrani.pl\E2e Sprint`                                    |
| Dev               | `kontakt@DTCode.pl`                                        |
| Tester            | `Piotr.Tunski@DTCode.pl`                                   |
| Figma fileKey     | `ZvXQhQILd9smr1Q1Gnzn5F`                                   |
| Repo FE           | `DTCodePL/ZebraniFE`                                       |
| Repo BE           | `DTCodePL/ZebraniBE` (puste — samo README)                 |
| Workflow deployu  | `deploy-preprod.yml`, **wyłącznie `workflow_dispatch`**    |
| Dev server        | `npm start` → `http://localhost:4200`                      |

**Weryfikacja w API (2026-08-02):** wszystkie powyższe stałe zostały odczytane z REST
API Azure DevOps po odnowieniu PAT. Wynik:

- projekt `Zebrani.pl` (id `0270081e-6915-4582-a075-01075af5e4af`), jedyny team
  `Zebrani.pl Team` — zgodnie z założeniem;
- iteracje zastane: `Sprint 1` (bieżąca) … `Sprint 6`; **`E2e Sprint` nie istniał**
  i został utworzony w ramach tej pracy (`Zebrani.pl\E2e Sprint`, przypisany do teamu);
- konta `kontakt@dtcode.pl` (Damian D) i `piotr.tunski@dtcode.pl` (Piotr Tuński)
  istnieją w organizacji;
- typy WIT: `Epic`, `Feature`, `Product Backlog Item`, `Task`, `Bug` + custom
  `Bug standalone` (nieużywany domyślnie);
- area: tylko korzeń `Zebrani.pl`, bez pod-obszarów;
- **stany są szersze niż w UstawoŻerca** — Task ma m.in. `In Review`, `Ready for tests`
  i `Postponed`, PBI dodatkowo `Ready to develop`. Skille przepisane z UstawoŻercy
  podawały zawężony zestaw; poprawione;
- projekt zawiera **0 work itemów** — jest całkowicie pusty.

Skill A zachowuje procedurę awaryjną na wypadek późniejszej zmiany konfiguracji: gdy
`System.IterationPath` lub `System.AssignedTo` zostanie odrzucone, wylistuj realne
wartości i zapytaj użytkownika zamiast zgadywać.

## Skill A — `azure-devops-zebrani`

Odwzorowanie skilla UstawoŻercy: tryb Bug (Bug + sub-taski Fix/Retest), tryb PBI
(weryfikacja hierarchii Epic→Feature, PBI, **pełne 6 tasków**: FE, BE, DB, Figma,
Manual tests, E2e tests), wzorce MCP 1–5, styl opisu „dla testera, nie dla
programisty", upload screenshotów z Figmy przez REST API, Definition of Done,
tabela częstych błędów.

Różnice względem UstawoŻercy:

1. **Weryfikacja stałych przy pierwszym użyciu** — patrz wyżej.
2. **Dokumentacja produktowa jako źródło opisu** — `d:\projects\DTCode\Dokumentacja\Zebrani`
   ma `status` we front matter. Treść PBI czerpiemy z `zatwierdzony`;
   `do-weryfikacji` i `szkic` to propozycje wymagające decyzji człowieka;
   z `wycofany` nigdy nie implementujemy.
3. **Screenshoty Light/Dark** — jeśli mockup istnieje w obu motywach, dołącz oba
   (Light i Dark są w Zebrani obowiązkowe w całej aplikacji).

## Skill B — `fix-devops-bug-zebrani`

Procedura 9-krokowa z UstawoŻercy (identyfikacja work itema → weryfikacja
w kodzie → Playwright BEFORE → naprawa → lint/format → Playwright AFTER →
commit/push → statusy ADO + komentarz → podsumowanie).

Różnice względem UstawoŻercy:

1. **Macierz testowa 2×2** zamiast dwóch viewportów. Każda asercja BEFORE i AFTER
   na: mobile `360×530` i desktop `1280×720`, każdy w Light i Dark. Przełączanie
   motywu: preferowany realny toggle `ThemeMode`, fallback — klasa `.app-dark`
   na elemencie root. Cztery baseline'y i cztery screenshoty na buga.
2. **Deploy jest ręczny.** Po pushu skill pyta (`AskUserQuestion`), czy odpalić
   `gh workflow run deploy-preprod.yml --repo DTCodePL/ZebraniFE -f runner=github`.
   Po zgodzie czeka na run i wpisuje realny numer do komentarza (`FE: <n>+`).
   Po odmowie komentarz mówi „fix na main, dostępny po najbliższym ręcznym
   deployu pre-prod". Heurystyka „ostatni numer + 1" z UstawoŻercy **nie ma tu
   zastosowania** — run dispatchowany po pushu ma `headSha` równy naszemu
   commitowi, więc numer odczytujemy wprost.
3. **Backendu nie ma.** Jeśli repro jest backendowe — zatrzymaj się i zgłoś.
   Sekcja MSSQL MCP zostaje w treści z adnotacją „baza Zebrani jeszcze nie
   istnieje — pomiń", gotowa do użycia po starcie BE.
4. **Bramka jakości wg CLAUDE.md Zebrani** w checkliście zamknięcia:
   `lint:fix` (eslint + stylelint) + `format` do zera błędów, klucze i18n obecne
   w `pl.json` **i** `en.json`, zero hardkodowanych kolorów, zero `@deprecated`,
   AXE przechodzi.

Commit: `fix(<scope>): #<idBuga> <opis po polsku>`. Bug jest work itemem
powiązanym z pushem, więc wymóg CLAUDE.md („numer work itema w commicie i nazwie
brancha") jest spełniony numerem buga — skill zapisuje to wprost, żeby nie było
wątpliwości. Push na `main` wyłącznie po wyraźnym poleceniu użytkownika.

## Zmiany w konfiguracji ADO wykonane przy okazji

- Utworzono iterację `Zebrani.pl\E2e Sprint` i przypisano ją do teamu `Zebrani.pl Team`
  (wcześniej projekt miał tylko `Sprint 1`…`Sprint 6`).
- Odnowiono `PERSONAL_ACCESS_TOKEN` w `claude_desktop_config.json`
  (`mcpServers.azure-devops.env`, wartość base64). Backup:
  `claude_desktop_config.json.bak-20260802`. Wymaga restartu Claude Desktop.

## Dług do spłacenia

- **Sekcja MSSQL i taski BE/DB** ożyją, gdy `ZebraniBE` przestanie być pustym repo.
- **Deploy prod** nie istnieje — gdy powstanie `deploy-prod.yml`, skill B będzie
  wymagał rozszerzenia o wybór środowiska.
