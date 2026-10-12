# Worker przeglądarkowy — Playwright CLI

Od 2026-10-12 worker przeglądarkowy steruje przeglądarką przez **Playwright CLI** z tego katalogu
wszędzie tam, gdzie CLI działa — dziś w linii **Spark**. W Gemini i Codexie CLI nie działa (patrz
[Wywołanie w każdej linii](#wywołanie-w-każdej-linii)), więc tam zostaje Playwright MCP z `--isolated`.
Linię wybiera architekt per brief; przewaga kosztowa CLI jest argumentem w tej kwalifikacji, nie stałą
trasą.

## Kolejność: najpierw `browser-check` z Jev

Worker nie zastępuje `browser-check`. Dowód w przeglądarce daje najpierw architekt tym narzędziem:
`matrix` bez modelu i `flows` z Jev ([FLOWS.md](FLOWS.md)). Worker wchodzi dopiero wtedy, gdy raport nie
rozstrzyga — `NEED_FALLBACK` (Jev poniżej progu pewności), `LOOP`, `MAX_STEPS`, FAIL, którego raport nie
wyjaśnia, wynik powtórzony po jednej powtórce — albo dla interakcji spoza scenariusza i błędu czysto
wizualnego Buga. Brief workera podaje ustalenia raportu, `forbidden` scenariusza i zakaz akcji
nieodwracalnych.

Rząd wielkości dla tych samych 5 przejść: Jev ~18 tys. tokenów i 18 s; worker przez CLI ~0,6 mln tokenów
i ~2,5 min; worker przez MCP ~2 mln tokenów i ~3,5 min.

## Pomiar (2026-10-12)

Spark `max`, 5 przejść konta demo właściciela, po 2 przebiegi na ramię (kolejność A1 B1 C1 C2 B2 A2),
wszystkie 30 przejść PASS, stan końcowy sprawdzony niezależnie.

| Ramię | Tury | Tokeny wejścia | Czas | Pełne snapshoty |
| --- | --- | --- | --- | --- |
| A — MCP, brief jak dotąd | 42 / 37 | 2,25 / 1,83 mln | 263 / 150 s | 16 / 13 |
| B — CLI + „Oszczędny sposób pracy” | 18 / 19 | 0,59 / 0,64 mln | 151 / 177 s | 0 / 0 |
| C — MCP + ta sama instrukcja | 50 / 43 | 2,16 / 1,77 mln | 255 / 189 s | 0 / 0 |

Zysk daje łączenie kilku poleceń CLI w jednym wywołaniu powłoki (17–18 wywołań niosło 46–53 polecenia),
nie samo unikanie snapshotów: C bez snapshotów zrobiło więcej tur i zużyło tyle co A. Łańcuch „akcja &&
sprawdzenie” łapie też ulotne toasty, które w A i C znikały przed kolejną turą.

## Wywołanie w każdej linii

| Linia | Playwright CLI | Powód / polecenie |
| --- | --- | --- |
| Spark (WSL, `-Access write`) | **tak** | `/mnt/d/projects/DTCode/Claude_Skills/browser-check/pwcli` |
| Git Bash (ręczne odtworzenie przez architekta) | tak | `/d/projects/DTCode/Claude_Skills/browser-check/pwcli` |
| Gemini (`agy`) | **nie → MCP** | `agy` po każdym `run_command` zabija drzewo procesów, także demona sesji CLI — kolejne wywołanie dostaje `Browser '<sesja>' is not open` (sonda 2026-10-12). Działa tylko łańcuch w jednym wywołaniu, a worker wchodzi właśnie po to, żeby oglądać wynik między krokami. |
| Codex (`workspace-write`) | **nie → MCP** | piaskownica blokuje zapis do `%LOCALAPPDATA%\ms-playwright` (rejestr sesji `daemon\` i przeglądarek `b\`) — `EPERM` (sonda 2026-10-12). Serwer MCP działa poza piaskownicą. |

- Sesja żyje między osobnymi wywołaniami powłoki w Sparku i w Git Bash (demon w tle; sprawdzone
  2026-10-12). Łańcuch `&&` służy oszczędności tur, nie utrzymaniu sesji.
- `pwcli` w WSL woła `node.exe` Windows wprost, z pominięciem `cmd.exe`, więc cudzysłowy i polskie
  znaki przechodzą nietknięte (sprawdzone 2026-10-12).
- Gdy linia nie ma CLI, brief workera z MCP dostaje tę samą sekcję „Oszczędny sposób pracy” w wersji
  MCP (`browser_find`, `browser_evaluate` zamiast pełnego `browser_snapshot`). Pomiar pokazał, że sama
  instrukcja w MCP nie obniża kosztu (ramię C), ale zatrzymuje rutynowe snapshoty.
- Wymaga `node_modules` tego katalogu (playwright 1.63). Instaluje je architekt (`npm ci` tutaj),
  nigdy worker.
- **Katalog roboczy workera (`-Repo`) to pusty katalog w scratchpadzie, nie repo produktu**: CLI zapisuje
  snapshoty po akcjach i zrzuty do `.playwright-cli/` w bieżącym katalogu.
- Każdy przebieg ma własną nazwaną sesję `-s=<nazwa>` — osobną przeglądarkę z profilem w pamięci.
  Równoległe przebiegi używają różnych nazw. Sesja startuje wylogowana: worker loguje się kontem
  testowym na początku i kończy `close`.

## Sekcja briefu (wklej, podstaw `{PW}` i `{SESJA}`)

```markdown
## Narzędzie — Playwright CLI
Przeglądarką sterujesz WYŁĄCZNIE przez Playwright CLI w powłoce: `{PW}` (poniżej `PW`). NIE używaj
serwera MCP `playwright` ani innych narzędzi przeglądarki. Nie instaluj niczego (żadnego `npm install`,
`npx` ani `@playwright/cli`), nie uruchamiaj git ani npm. Artefakty w `.playwright-cli/` tworzy samo CLI
w katalogu roboczym — to w porządku; ty plików nie zapisujesz.
Każde wywołanie: `PW -s={SESJA} <polecenie> [argumenty]` — zawsze z `-s={SESJA}` (twoja przeglądarka
żyje między wywołaniami do `close`). Przeglądarka startuje bez sesji — logujesz się sam na początku.
- `open <url>` (bez okna), `goto <url>`, `resize <szer> <wys>`, na koniec `close`.
- `click <cel>`, `fill <cel> <tekst>`, `press <klawisz>`, `select <cel> <wartość>`.
- `<cel>` = ref z `find` (np. `e15`) albo lokator Playwrighta w cudzysłowie, np.
  `"getByRole('button', { name: 'Zapisz' })"`, `"getByLabel('Imię')"`.
- `find <tekst>` albo `find --regex <wzorzec>` — tylko pasujące węzły, z refami.
- `snapshot [cel] [--depth=N]` — wypisuje drzewo do odpowiedzi (duże).
- `--raw eval <wyrażenie> [cel]` — sam wynik JS, np. `--raw eval "location.href"`,
  `--raw eval "el => el.value" e12`.
- `screenshot --filename=<nazwa>.png` — zrzut do katalogu roboczego (nie oglądasz go; podaj ścieżkę w raporcie).
- Po każdej akcji CLI wypisuje adres strony i ścieżkę pliku snapshotu, nie jego treść.

## Oszczędny sposób pracy (obowiązuje)
Każda tura to ponowne czytanie całej rozmowy, a pełny snapshot zostaje w niej na stałe. Dlatego:
1. Nie rób pełnego snapshotu rutynowo. Element lokalizuj przez `find`.
2. Gdy znasz widoczną nazwę elementu (etykieta, rola + nazwa), celuj lokatorem — bez snapshotu.
   Lokator niejednoznaczny albo chybiony → dopiero `find`; kilka pasujących → zawęź kontenerem.
3. Łącz kroki, których wyniku nie musisz oglądać pomiędzy: kilka poleceń połącz `&&` w jednym wywołaniu
   powłoki. Akcję z ulotnym skutkiem (toast) łącz z jej sprawdzeniem w tym samym wywołaniu.
4. Kryterium PASS sprawdzaj celowanym odczytem (`find`, `--raw eval`), nie pełnym snapshotem.
5. Pełny `snapshot` tylko wtedy, gdy powyższe nie wystarcza — ograniczony `--depth=N` albo celem.
```

Raport workera podaje: liczbę wywołań powłoki, liczbę poleceń CLI, liczbę pełnych snapshotów, wynik każdego
przejścia z dowodem (adres, odczytana wartość) i ścieżki zrzutów.

## Pułapki

- Jawne `snapshot` wkleja całe drzewo do kontekstu — tak samo jak `browser_snapshot` w MCP. Do pliku trafia
  tylko snapshot po akcji (oraz `snapshot --filename`).
- Dokumentacja CLI (`node_modules/playwright-core/lib/tools/skills/playwright-cli/SKILL.md`) każe przy braku
  polecenia instalować `@playwright/cli` globalnie — worker tego nie robi; zakaz stoi w sekcji briefu.
- Lokator dopasowany do kilku elementów kończy się błędem strict mode — np. dwa „Zapisz” na
  `/panel/ustawienia/program`. Zawężaj kontenerem (`locator('zeb-program-info').getByRole(...)`) albo refem.
- `&` w adresie: bash traktuje go jako przejście w tło — adres z parametrami zawsze w cudzysłowie.
- CLI działa domyślnie bez okna (`open --headed` tylko do podglądu); Playwright MCP — z oknem.
- Błąd czysto wizualny: wyliczony styl przez `--raw eval "el => getComputedStyle(el).color" <cel>`,
  zrzuty przez `screenshot --filename=...`; PNG ogląda architekt.
