---
name: teams-notatki
description: >
  Tworzy notatki po polsku ze spotkań Microsoft Teams na podstawie transkrypcji,
  przez mostek HTTPS teamsnotes.tojest.dev (Damian/Piotr, DTCode).
  Wyzwalacze: „notatki ze spotkania”, „transkrypcja Teams”, link
  teams.microsoft.com/meet/..., .../l/meetup-join/... albo .../l/meetingrecap?...
  (link „Podsumowanie”, także z połączenia 1:1), „spotkanie w piątek /
  wczoraj / o 10”, „podsumuj spotkanie”, „co ustaliliśmy na spotkaniu”,
  „jakie PBI / test case'y / makiety / dokumenty wynikają ze spotkania”.
  Rozwiązuje spotkanie po linku albo po dacie/godzinie/tytule, pobiera
  transkrypcję, renderuje notatkę wg szablonu (podsumowanie, decyzje, zadania,
  otwarte pytania, następne kroki) ze znacznikami czasu. Ma tryb awaryjny bez
  mostka — parsowanie lokalnego pliku .vtt pobranego ręcznie z Teams.
  UŻYWAJ ZAWSZE, gdy user chce notatkę, podsumowanie lub listę zadań ze
  spotkania Microsoft Teams — nawet jeśli nie padnie słowo skill.
version: '1.2'
language: pl
organization: DTCode
remote:
  github_raw: 'https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/teams-notatki/SKILL.md'
  github_page: 'https://github.com/DTCodePL/Claude_Skills/blob/main/teams-notatki/SKILL.md'
---

# Teams — notatki ze spotkania

Notatka po polsku z nagranego/transkrybowanego spotkania Microsoft Teams
(Damian i Piotr, DTCode). Transkrypcję pobiera mostek HTTPS
`https://teamsnotes.tojest.dev` — adres i token są **wbudowane w
`scripts/bridge.py`**, nic nie trzeba konfigurować na nowym urządzeniu.

## 1. Auto-aktualizacja — WYKONAJ JAKO PIERWSZY KROK

**Zanim cokolwiek zrobisz**, sprawdź, czy na GitHubie jest nowsza wersja tego
skilla, i ewentualnie zaktualizuj lokalną kopię.

**Krok 1 — pobierz zdalną wersję:**

```bash
curl -sL "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/teams-notatki/SKILL.md" -o /tmp/teams-notatki-remote.md
grep "version:" /tmp/teams-notatki-remote.md | head -1
```

PowerShell:

```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/teams-notatki/SKILL.md" -OutFile "$env:TEMP\teams-notatki-remote.md"
Select-String -Path "$env:TEMP\teams-notatki-remote.md" -Pattern "version:" | Select-Object -First 1
```

**Krok 2 — porównaj wersje:** wyciągnięte `version:` z pobranego pliku vs.
frontmatter tego pliku (`version: '1.2'`). Zdalna wyższa → użyj treści
pobranego pliku jako źródła prawdy do reszty zadania. Równa → kontynuuj z tym
plikiem. Nie da się pobrać (404, brak sieci, plik pusty) → poinformuj o tym i
kontynuuj z tą lokalną kopią (nie blokuj zadania z powodu braku sieci — to
tylko sprawdzenie aktualności, nie krok krytyczny).

## 2. Zasoby

Skill potrzebuje, obok tego `SKILL.md`, czterech plików:

- `scripts/bridge.py`
- `references/szablon-notatki.md`
- `references/szablon-spisu-zmian.md`
- `references/api.md`

Jeżeli ich nie ma (loader na urządzeniu pobrał tylko `SKILL.md`), pobierz je
`curl -sL` do katalogu tymczasowego, **razem, jednym blokiem, zanim przejdziesz
do „Przebiegu”**:

**bash (Git Bash / Linux/macOS):**

```bash
mkdir -p /tmp/teams-notatki/scripts /tmp/teams-notatki/references
curl -sL "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/teams-notatki/scripts/bridge.py" -o /tmp/teams-notatki/scripts/bridge.py
curl -sL "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/teams-notatki/references/szablon-notatki.md" -o /tmp/teams-notatki/references/szablon-notatki.md
curl -sL "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/teams-notatki/references/szablon-spisu-zmian.md" -o /tmp/teams-notatki/references/szablon-spisu-zmian.md
curl -sL "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/teams-notatki/references/api.md" -o /tmp/teams-notatki/references/api.md
```

**PowerShell (Codex desktop / Windows):**

```powershell
New-Item -ItemType Directory -Force "$env:TEMP\teams-notatki\scripts" | Out-Null
New-Item -ItemType Directory -Force "$env:TEMP\teams-notatki\references" | Out-Null
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/teams-notatki/scripts/bridge.py" -OutFile "$env:TEMP\teams-notatki\scripts\bridge.py"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/teams-notatki/references/szablon-notatki.md" -OutFile "$env:TEMP\teams-notatki\references\szablon-notatki.md"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/teams-notatki/references/szablon-spisu-zmian.md" -OutFile "$env:TEMP\teams-notatki\references\szablon-spisu-zmian.md"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/teams-notatki/references/api.md" -OutFile "$env:TEMP\teams-notatki\references\api.md"
```

Katalog tymczasowy: `/tmp/teams-notatki` (bash) / `$env:TEMP\teams-notatki`
(PowerShell). Uruchamiaj skrypt jako `python /tmp/teams-notatki/scripts/bridge.py ...`
(bash) albo `python "$env:TEMP\teams-notatki\scripts\bridge.py" ...` / `py -3 ...`
(PowerShell, gdy `python` nie jest na PATH).

**Jeśli Pythona nie ma w ogóle** (ani `python`, ani `py -3`) — pomiń
`scripts/bridge.py` i pracuj wyłącznie na podstawie `references/api.md`:
wywołania `curl` do mostka bezpośrednio, ręczne budowanie JSON, ręczne
odczytywanie pól odpowiedzi. Sekcja „Typowe błędy” niżej i sam
`references/api.md` mają gotowe przykłady `curl` na każdy endpoint.

## 3. Przebieg

### 3.1 Sprawdzenie mostka

```bash
python /tmp/teams-notatki/scripts/bridge.py health
```

Kod wyjścia ≠ 0 → mostek `https://teamsnotes.tojest.dev` nie odpowiada.
Powiedz to użytkownikowi i zaproponuj tryb awaryjny: niech pobierze plik
`.vtt` z Teams (**Teams → nagranie spotkania → Transkrypcja → Pobierz jako
plik → .vtt**) i wskaże jego ścieżkę — dalej idziesz do `parse-vtt` (patrz
3.4).

### 3.2 Identyfikacja spotkania

- W wiadomości jest link Teams (`teams.microsoft.com/meet/...` albo
  `.../l/meetup-join/...`) albo gołe 12–15 cyfr ID spotkania (ewentualnie ze
  spacjami) → `resolve --link "<link albo cyfry>"`.
- W wiadomości jest link `teams.microsoft.com/l/meetingrecap?...` (link
  „Podsumowanie” — działa też dla połączeń 1:1 z czatu, które nie mają
  zdarzenia w kalendarzu) → `resolve --link "<link>"`.
- Inaczej wyprowadź `--date` / `--time` / `--title` z języka naturalnego:
  - „dziś” / „wczoraj” / „w piątek” — **nie zgaduj dnia tygodnia**: sprawdź
    dzisiejszą datę systemową komendą `date` (bash) albo `Get-Date`
    (PowerShell), a potem policz właściwy dzień względem niej. „W piątek”
    bez dalszego kontekstu = **ostatni piątek** względem tej daty (jeśli dziś
    jest piątek, to dzisiejsza data).
  - „o 10” → `--time 10:00`.
  - Tytuł = to, co użytkownik nazwał tematem, jak najkrócej i bez ozdobników
    (np. „spotkanie o statusie projektu” → `--title "status projektu"`).
  - Podano wyłącznie tytuł, bez daty → `resolve --title "..."` (mostek szuka
    w ostatnich 30 dniach).
- Nie da się wyprowadzić ani linku, ani daty, ani tytułu → **zapytaj
  użytkownika** o jedno z nich, zanim wywołasz `resolve`.

### 3.3 Wybór kandydata

Wywołaj `resolve` **bez `--text`** (domyślny JSON) i parsuj wynik samodzielnie —
potrzebujesz **pełnych** `account.id` i `meetingId` do kroku 3.4 (`--text`
skraca je do czterech znaków + „…” tylko dla czytelności wobec człowieka; do
identyfikacji zawsze bierz wartości z JSON-a, nigdy z obciętego tekstu).

- **0 kandydatów** → powiedz użytkownikowi, czego szukałeś (data/okno/tytuł,
  które konto/konta), i zaproponuj: poszerzenie okna (`--window-days 3`),
  podanie linku, albo plik `.vtt`.
- **1 kandydat** → idź do 3.4.
- **>1 kandydatów** → pokaż użytkownikowi numerowaną listę (możesz sformatować
  ją sam z JSON-a albo odpalić `resolve ... --text` wyłącznie do wyświetlenia)
  i zapytaj, które spotkanie ma na myśli.
- Kandydat z `"transcripts": []` → wyjaśnij, że transkrypcja pojawia się kilka
  minut po zakończeniu spotkania i tylko wtedy, gdy była włączona; zaproponuj
  ponowienie za chwilę albo plik `.vtt`.
- Kandydat ma `kind`: `onlineMeeting` to zwykłe spotkanie, `adhocCall` to
  połączenie z czatu; dla `adhocCall` `subject` może być `null`.

### 3.4 Pobranie transkrypcji

```bash
python /tmp/teams-notatki/scripts/bridge.py transcript \
  --account "<account.id>" --meeting "<meetingId>" \
  --out /tmp/teams-notatki/transkrypcja.md
```

Gdy wybrany kandydat ma `kind == "onlineMeeting"` → `transcript --meeting`
(jak wyżej); gdy `kind == "adhocCall"` → `transcript --call "<callId>"`:

```bash
python /tmp/teams-notatki/scripts/bridge.py transcript \
  --account "<account.id>" --call "<callId>" \
  --out /tmp/teams-notatki/transkrypcja.md
```

Tryb awaryjny (mostek nie odpowiada / spotkanie spoza Waszych kont) — użytkownik
wskazuje plik `.vtt` pobrany z Teams:

```bash
python /tmp/teams-notatki/scripts/bridge.py parse-vtt \
  --file "<ścieżka do pliku.vtt>" --out /tmp/teams-notatki/transkrypcja.md
```

Przeczytaj cały plik `/tmp/teams-notatki/transkrypcja.md`, zanim zaczniesz
pisać notatkę.

### 3.5 Notatka

Wypełnij `references/szablon-notatki.md` na podstawie transkrypcji. Reguły
twarde, bez wyjątków:

- Tylko treści **obecne w transkrypcji** — nic nie dopowiadaj, nie zgaduj, nie
  uzupełniaj z wiedzy ogólnej.
- Nazwiska mówców dokładnie jak w transkrypcji (nie poprawiaj, nie normalizuj).
- Każda decyzja i każde zadanie ma znacznik czasu `[MM:SS]` wskazujący, gdzie w
  rozmowie to padło.
- Fragmenty niepewne (błędy rozpoznawania mowy, urwane zdania, niejasny
  kontekst) oznacz dopiskiem „(niepewne)”.
- Język notatki = język transkrypcji, chyba że użytkownik wyraźnie prosi o
  inny.
- Brak treści w jakiejś sekcji (np. zero decyzji) → napisz „brak”, nie
  wymyślaj czegoś, żeby sekcja nie była pusta.
- **Organizator** w nagłówku szablonu to imię i nazwisko — jeśli masz je z
  kroku 3.3 (`organizer.name` z wyniku `resolve`), użyj go; plik transkrypcji
  z `bridge.py` niesie tylko `organizerId` (identyfikator), nie imię i
  nazwisko (patrz `references/api.md`). Dla `adhocCall` `organizer.name` też
  pochodzi z `resolve`.

### 3.6 Wynik

Pokaż notatkę w rozmowie. Jeśli użytkownik podał ścieżkę zapisu albo powiedział
„zapisz” → zapisz `.md` pod tą ścieżką. Jeśli chce zapisać, ale nie podał
nazwy → `YYYY-MM-DD-<slug-tytułu>-notatki.md` w bieżącym katalogu roboczym, i
powiedz, gdzie plik wylądował. Nie zapisuj surowej transkrypcji poza katalogiem
tymczasowym, chyba że użytkownik wyraźnie o to poprosi („daj mi też
transkrypcję”). **Nigdy nie wypisuj tokenu ani nagłówka `Authorization` w
rozmowie** — nawet do debugowania.

### 3.7 Spis zmian w systemach (ADO · QA Sphere · Figma · Dokumentacja)

Notatka to nie koniec. Gdy spotkanie dotyczy produktu DTCode (w transkrypcji
pada Zebrani / TachoPing / UstawoŻerca albo ich funkcje), **po pokazaniu
notatki przygotuj spis zmian** wg `references/szablon-spisu-zmian.md`: dla
każdego z czterech systemów cztery listy — **do utworzenia / do zaktualizowania /
do usunięcia / już istnieje bez zmian**. Spotkanie bez produktu (rozmowa organizacyjna, prywatna) →
napisz jedno zdanie, że spisu nie ma, i zakończ.

**To jest propozycja, nie wykonanie.** Nie tworzysz, nie edytujesz i nie
usuwasz niczego w żadnym z systemów. Wykonanie następuje dopiero po
zatwierdzeniu przez użytkownika, każdą pozycję właściwym skillem:
`azure-devops-<produkt>` (ADO), `qasphere-test-generator` (QA Sphere),
`figma-use` (Figma), edycja plików w katalogu dokumentacji. Tu tylko
inwentaryzujesz.

Skąd bierzesz stan istniejący (odczyt, nigdy zapis):

| System | Narzędzie | Co sprawdzasz |
| --- | --- | --- |
| Azure DevOps | MCP `azure-devops`: `search_workitem`, `wit_query`, `wit_work_item` (projekt z `azure-devops-<produkt>`) | czy PBI/Bug o tym temacie już istnieje, jego stan i rodzica (Feature/Epic) |
| QA Sphere | REST `GET .../project`, `.../tcase/folders`, `.../tcase` (klucz i adres w `qasphere-test-generator`) | czy test case na ten scenariusz już jest, w którym folderze |
| Figma | MCP Figma: `get_metadata` / `search_design_system` na pliku produktu (klucz pliku w skillu `<produkt>-design`) | czy ramka/komponent istnieje, na której stronie |
| Dokumentacja | `Grep`/`Glob` w `d:\projects\DTCode\Dokumentacja\<Produkt>` | który dokument opisuje temat i jaki ma `status` w front matter |

Reguły spisu — te same co dla notatki, plus:

- **Pozycja rodzi się wyłącznie z sekcji „Decyzje” albo „Zadania” notatki**
  i ma jej znacznik `[MM:SS]`. Otwarte pytanie nie jest pozycją. Zdanie
  z „ewentualnie / może / kiedyś / do rozważenia” też nie — to opcja, nie
  decyzja; wymień je jednym wierszem pod spisem jako „Pominięte (opcje bez
  decyzji)”, żeby nie zginęło.
- **Zadanie z notatki, które w systemie już jest 1:1** (ten sam zakres, nic
  do zmiany) → lista „już istnieje bez zmian” z identyfikatorem i stanem.
  Nie wciskaj go do „do zaktualizowania” z opisem „brak zmian” i nie pomijaj
  — to, że backlog już to ma, jest najważniejszym wynikiem tego kroku.
- „Do zaktualizowania” i „do usunięcia” wymagają identyfikatora istniejącego
  artefaktu (`#id` ADO, `seq` QA Sphere, nazwa węzła Figmy, ścieżka pliku)
  **odczytanego z systemu**, nie z pamięci. Nie znalazłeś → pozycja idzie do
  „do utworzenia” z dopiskiem „(nie znaleziono istniejącego: szukałem X)”.
- „Do utworzenia” w ADO podaje rodzica znalezionego w hierarchii: dla PBI
  Feature, dla Buga **PBI (user story), którego dotyczy** — brak pasującego
  rodzica → „brak — zaproponuj” z nazwą, nie wymyślony numer.
- Dokumentacji się nie kasuje — „do usunięcia” oznacza zmianę `status` na
  `wycofany`. Test case'ów w QA Sphere też nie (API nie ma `DELETE`) — pozycja
  mówi, na jaki test case go nadpisać.
- Brak narzędzia (w Codexie i Sparku nie ma MCP ADO ani Figmy; brak klucza
  QA Sphere) **albo odpowiedź narzędzia sprzeczna z innym źródłem** (np.
  Figma `get_metadata` zwraca 2 strony, a PBI linkują makiety na innych) →
  spis dla tego systemu robisz z samej notatki, bez kolumn z identyfikatorami,
  i wpisujesz go w sekcji „Nie dało się zweryfikować” z powodem. Nie
  zgadujesz identyfikatorów i nie wnioskujesz „nie istnieje” z niepełnej
  odpowiedzi. Dla Figmy pytaj o konkretne strony/węzły (ID z linków w PBI
  albo ze skilla `<produkt>-design`), nie o korzeń pliku.
- Pusta lista → „brak”. Spis z samymi „brak” w trzech systemach jest
  poprawnym wynikiem, jeśli spotkanie dotyczyło jednego.

Wynik: pokaż spis w rozmowie pod notatką. Zapis do pliku na tych samych
zasadach co notatka (`YYYY-MM-DD-<slug>-spis-zmian.md`). Na końcu jedno
zdanie: „Które pozycje wykonać?” — i czekasz.

## 4. Typowe błędy

| Błąd (`code`)                | Co to znaczy                                                     | Co zrobić                                                                 |
| ----------------------------- | ------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| `unauthorized`                 | Token wbudowany w `bridge.py` jest nieaktualny                    | Poinformuj i poproś Damiana o rotację tokenu (patrz README, rotacja)      |
| `meeting_not_found`            | Spotkanie spoza kont Damiana/Piotra albo z innego tenanta          | Zaproponuj plik `.vtt` pobrany ręcznie z Teams                            |
| `transcript_access_disabled`   | Administrator wyłączył dostęp do transkrypcji w Teams Admin Center | Poinformuj użytkownika — to decyzja administracyjna, nie błąd skilla      |
| `transcript_not_found`         | Spotkanie jest, transkrypcja jeszcze niedostępna                   | Zaproponuj odczekanie kilku minut albo plik `.vtt`                        |
| `graph_forbidden` przy linku recap | Aplikacja nie ma uprawnienia `CallTranscripts.Read.All` (patrz `bridge/README.md`) | Poinformuj użytkownika i poproś Damiana o zgodę administratora w Entra |
| brak Pythona na urządzeniu     | Nie da się uruchomić `bridge.py`                                   | Fallback na `curl` wg `references/api.md`                                 |
| mostek nie odpowiada (sieć)    | `health` zwrócił kod ≠ 0, komunikat mówi o błędzie połączenia      | Zaproponuj plik `.vtt` + `parse-vtt` (patrz 3.1 i 3.4 wyżej)              |
