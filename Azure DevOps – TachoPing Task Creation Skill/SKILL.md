---
name: azure-devops-tachoping
description: >
  Zasady tworzenia tasków w Azure DevOps dla projektu TachoPing.
  Obsługuje dwa tryby: Bug (z sub-taskami Fix i Retest) oraz PBI
  (z pełnym zestawem tasków FE/BE/DB/Figma/Manual tests/E2e tests).
  Wymusza weryfikację hierarchii Epic→Feature przed utworzeniem PBI,
  pilnuje przypisań i sprintów, treści pisze po polsku, linkuje do Figmy.
version: "1.7"
language: pl
project: TachoPing
organization: dtcode
remote:
  github_raw: "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/Azure%20DevOps%20%E2%80%93%20TachoPing%20Task%20Creation%20Skill/SKILL.md"
  github_page: "https://github.com/DTCodePL/Claude_Skills/blob/main/Azure%20DevOps%20%E2%80%93%20TachoPing%20Task%20Creation%20Skill/SKILL.md"
---

# Azure DevOps – TachoPing Task Creation Skill

## ⚡ Auto-aktualizacja — WYKONAJ JAKO PIERWSZY KROK

**Zanim cokolwiek zrobisz**, sprawdź czy istnieje nowsza wersja skilla na GitHubie i ewentualnie zaktualizuj lokalną kopię.

### Procedura (wykonaj zawsze przy wczytaniu skilla)

**Krok 1 — Pobierz zdalną wersję przez bash_tool:**
```bash
curl -sL "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/Azure%20DevOps%20%E2%80%93%20TachoPing%20Task%20Creation%20Skill/SKILL.md" -o /tmp/skill_remote.md
head -10 /tmp/skill_remote.md
```

**Krok 2 — Porównaj wersje:**
- Wyciągnij `version:` z pobranego pliku (`grep 'version:' /tmp/skill_remote.md`)
- Porównaj z lokalną wersją (frontmatter `version:` w tym pliku)
- Jeśli zdalna wersja > lokalna → przejdź do Kroku 3
- Jeśli zdalna = lokalna → pomiń aktualizację, przejdź do zadania

**Krok 3 — Nadpisz lokalny skill (tylko jeśli nowsza wersja):**
```bash
cp /tmp/skill_remote.md /mnt/skills/user/azure-devops-tachoping/SKILL.md
```

**Krok 4 — Wczytaj nową wersję:**
```
view /mnt/skills/user/azure-devops-tachoping/SKILL.md
```
Poinformuj użytkownika: „Zaktualizowałem skill v{stara} → v{nowa}. Przechodzę do zadania."

### Obsługa błędów pobierania

| Sytuacja | Co zrobić |
|---|---|
| `curl` zwraca 404 | Repo prawdopodobnie prywatne — pomiń aktualizację, użyj lokalnej wersji, poinformuj użytkownika |
| `curl` zwraca inny błąd / brak sieci | Pomiń aktualizację, użyj lokalnej wersji |
| Plik pusty lub niepoprawny YAML | Pomiń aktualizację, użyj lokalnej wersji |

> ⚠️ Aktualizacja jest **opcjonalna** jeśli niedostępna — nigdy nie blokuj zadania z powodu braku dostępu do GitHuba.

## Projekt / organizacja

| Pole | Wartość |
|---|---|
| Organizacja | `dtcode` |
| Projekt | `TachoPing` |
| Team | `TachoPing Team` |
| Sprint 1 URL | `https://dev.azure.com/dtcode/TachoPing/_sprints/taskboard/TachoPing%20Team/TachoPing/Sprint%201` |
| E2e Sprint URL | `https://dev.azure.com/dtcode/TachoPing/_sprints/taskboard/TachoPing%20Team/TachoPing/E2e%20Sprint` |

---

## TRYB A – Tworzenie Buga

### Krok 1 – Utwórz główny Bug

- Typ: `Bug`
- Przypisany do: `kontakt@DTCode.pl`
- Iteracja (sprint): **Sprint 1**

### Krok 2 – Utwórz sub-task: **Fix**

- Typ: `Task`
- Tytuł: `Fix`
- Rodzic: ← ID głównego buga z kroku 1
- Przypisany do: `kontakt@DTCode.pl`
- Iteracja (sprint): **Sprint 1**

### Krok 3 – Utwórz sub-task: **Retest**

- Typ: `Task`
- Tytuł: `Retest`
- Rodzic: ← ID głównego buga z kroku 1
- Przypisany do: `Piotr.Tunski@DTCode.pl`
- Iteracja (sprint): **Sprint 1**

### Kolejność wykonania dla Buga

```
1. Utwórz Bug → zanotuj ID
2. Utwórz Task "Fix"   (parent = Bug ID, sprint = Sprint 1)
3. Utwórz Task "Retest" (parent = Bug ID, sprint = Sprint 1)
```

---

## TRYB B – Tworzenie PBI (Product Backlog Item)

### Krok 0 – Weryfikacja hierarchii (OBOWIĄZKOWA przed utworzeniem)

Przed jakimkolwiek tworzeniem elementów sprawdź, czy masz wszystkie potrzebne informacje:

#### Epic
- Jeśli użytkownik **podał ID lub nazwę istniejącego epica** → użyj go.
- Jeśli nie podał → **zapytaj użytkownika**:
  > „Nie mam wskazanego Epica. Podaj:
  > - **ID istniejącego** epica, LUB
  > - **Zaakceptuj nazwę** którą zaproponuję i sam go utworzę, LUB
  > - **Wpisz nazwę**, której mam użyć"

#### Feature
- Jeśli użytkownik **podał ID lub nazwę istniejącego featura** → użyj go.
- Jeśli nie podał → **zapytaj użytkownika**:
  > „Nie mam wskazanego Feature. Podaj:
  > - **ID istniejącego** featura, LUB
  > - **Zaakceptuj nazwę** którą zaproponuję i sam go utworzę, LUB
  > - **Wpisz nazwę**, której mam użyć"
- Nowo tworzony Feature musi być przypięty do ustalonego Epica.

> ⚠️ **Nie twórz PBI ani żadnych tasków dopóki nie masz potwierdzenia zarówno Epica jak i Featura.**

---

### Krok 1 – (opcjonalnie) Utwórz Epic

Tylko jeśli uzgodniono z użytkownikiem:

- Typ: `Epic`
- Tytuł: ← uzgodniony z użytkownikiem

### Krok 2 – (opcjonalnie) Utwórz Feature

Tylko jeśli uzgodniono z użytkownikiem:

- Typ: `Feature`
- Tytuł: ← uzgodniony z użytkownikiem
- Rodzic: ← ID Epica (z kroku 1 lub podany przez użytkownika)

### Krok 3 – Utwórz PBI

- Typ: `Product Backlog Item`
- Rodzic: ← ID Featura (z kroku 2 lub podany przez użytkownika)
- Przypisany do: `kontakt@DTCode.pl`
- Iteracja (sprint): **Sprint 1**

### Krok 4 – Utwórz 6 tasków pod PBI

Każdy task: Typ = `Task`, Rodzic = ID PBI z kroku 3.

| # | Tytuł | Przypisany do | Sprint |
|---|---|---|---|
| 1 | `FE` | `kontakt@DTCode.pl` | Sprint 1 |
| 2 | `BE` | `kontakt@DTCode.pl` | Sprint 1 |
| 3 | `DB` | `kontakt@DTCode.pl` | Sprint 1 |
| 4 | `Figma` | `Piotr.Tunski@DTCode.pl` | Sprint 1 |
| 5 | `Manual tests` | `Piotr.Tunski@DTCode.pl` | Sprint 1 |
| 6 | `E2e tests` | `Piotr.Tunski@DTCode.pl` | **E2e Sprint** |

### Kolejność wykonania dla PBI

```
0. Potwierdź Epic i Feature (zapytaj jeśli brakuje)
1. (opcjonalnie) Utwórz Epic        → zanotuj ID
2. (opcjonalnie) Utwórz Feature     → zanotuj ID
3. Utwórz PBI                       → zanotuj ID
4. Utwórz Task "FE"          (parent = PBI, sprint = Sprint 1)
5. Utwórz Task "BE"          (parent = PBI, sprint = Sprint 1)
6. Utwórz Task "DB"          (parent = PBI, sprint = Sprint 1)
7. Utwórz Task "Figma"       (parent = PBI, sprint = Sprint 1)
8. Utwórz Task "Manual tests" (parent = PBI, sprint = Sprint 1)
9. Utwórz Task "E2e tests"   (parent = PBI, sprint = E2e Sprint)
```

---

## Opis PBI — styl i treść

### Dla kogo jest opis

Opis w PBI jest przeznaczony **dla testera, który nie jest technicznym programistą**. Tester musi zrozumieć:
- Co nowa funkcjonalność robi z perspektywy użytkownika
- Jak ją przetestować ręcznie (co kliknąć, co powinno się stać)
- Czego oczekiwać (co jest wynikiem poprawnego działania)

> ⚠️ **Nigdy nie pisz opisu technicznego** — bez nazw klas, metod, endpointów API, nazw kolumn DB, nazw plików, architektury ani terminologii z kodu. Opis ma opisywać **zachowanie widoczne dla użytkownika**, nie implementację.

### Struktura opisu PBI

```html
<h3>Co zostało zrobione</h3>
<p>Krótkie zdanie podsumowujące cel funkcjonalności (1-2 zdania).</p>

<h3>Jak to działa</h3>

<h4>1. Krok / scenariusz pierwszy</h4>
<p>Opis kroków jakie wykonuje użytkownik i co się wtedy dzieje.</p>
<img src="..." style="max-width:100%;border:1px solid #e2e8f0;border-radius:8px;margin:12px 0;display:block;" />

<h4>2. Krok / scenariusz drugi</h4>
<p>Opis kolejnego scenariusza.</p>
<img src="..." style="max-width:100%;" />
```

Przykłady dobrego i złego opisu:

| ❌ ZŁE (techniczne) | ✅ DOBRE (dla testera) |
|---|---|
| „Dodano endpoint `PUT /owner/language` który zapisuje `LanguageId` do tabeli `Users`" | „Po kliknięciu Zapisz wybrany język jest zapamiętywany na koncie — po ponownym zalogowaniu na innym urządzeniu interfejs nadal wyświetla się w tym języku" |
| „`AuthService.me()` synchronizuje język po zalogowaniu via `LanguageService.setLanguageById()`" | „Zaraz po zalogowaniu aplikacja automatycznie przełącza się na język zapisany na koncie, niezależnie od ustawień przeglądarki" |
| „Komponent `LanguageBottomSheet` wstrzykuje `OwnerService` i wywołuje `updateLanguage()`" | „Na mobile: kliknij wiersz Język → pojawi się panel z listą języków → wybierz i kliknij Zapisz" |

---

## Screenshoty w opisie PBI — jak dodawać

### Źródło screenshotów: wyłącznie Figma

Screenshoty dołączane do opisu PBI **muszą pochodzić z Figmy** — nie z przeglądarki, nie z Playwright, nie z implementacji.

Powód: Figma zawiera zaakceptowane mockupy, które tester ma weryfikować. Screenshot z implementacji pokazuje „jak jest", a nie „jak powinno być".

### Procedura dodawania screenshotów

**Krok 1 — Pobierz screenshot z Figmy**

Używając narzędzia `get_screenshot` lub `use_figma` z Figma MCP pobierz adres zrzutu PNG dla odpowiedniego node-id z projektu TachoPing (klucz pliku: `aF4IGcuZGCT2rgdl1o9E7g`).

```
get_screenshot(fileKey: "aF4IGcuZGCT2rgdl1o9E7g", nodeId: "14:4653")
```

`get_screenshot` zwraca **krótkotrwały adres URL** do wyrenderowanego PNG — **nie zapisuj tego adresu w plikach ani w opisach ADO**. Od razu pobierz z niego plik PNG lokalnie do katalogu tymczasowego:

```powershell
Invoke-WebRequest -Uri "<krótkotrwały_url_z_get_screenshot>" -OutFile "C:\tmp\screen.png" -UseBasicParsing
```

**Krok 2 — Wgraj PNG jako załącznik do ADO**

**Sposób 1 (preferowany) — MCP `wit_work_item_attachment_upload`:**

Serwer MCP obsługuje upload plików binarnych zakodowanych w Base64. Zakoduj bajty pobranego PNG do czystego ciągu Base64 (bez prefiksu `data:image/png;base64,` i bez znaków nowej linii):

```powershell
$content = [Convert]::ToBase64String([IO.File]::ReadAllBytes("C:\tmp\screen.png"))
```

Przekaż zakodowany ciąg jako `content`:

```
wit_work_item_attachment_upload(
  project:  "TachoPing",
  fileName: "screen.png",
  content:  "<czysty_base64_z_$content>"
)
→ zwrócony JSON zawiera pole `url`, np. https://dev.azure.com/DTCode/2588c384-a691-4407-b553-194b87829089/_apis/wit/attachments/{guid}?fileName=screen.png
```

Jeśli chcesz dodatkowo przypiąć plik w zakładce Attachments work itema (poza samym `<img>` w opisie), użyj `wit_work_item_attachment_link(project: "TachoPing", workItemId: <ID>, attachmentUrl: "<url>")`.

**Sposób 2 (zapasowy, np. dla dużych plików PNG z dysku) — ADO REST API:**

Wartość `PERSONAL_ACCESS_TOKEN` w konfiguracji MCP jest **już zakodowana Base64 do nagłówka `Basic`**, więc odczytaj ją w tym samym skrypcie z `~/.claude.json` do zmiennej i przekaż bezpośrednio jako `"Basic " + wartość` — **bez wklejania tokenu do polecenia, bez wypisywania, bez dekodowania ani ponownego kodowania Base64**. Przed parsowaniem odpowiedzi sprawdź status HTTP:

```powershell
$cfgPath = Join-Path $HOME ".claude.json"
$cfg     = Get-Content -Raw -Path $cfgPath | ConvertFrom-Json
$b64     = $cfg.mcpServers.'azure-devops'.env.PERSONAL_ACCESS_TOKEN
if ([string]::IsNullOrWhiteSpace($b64)) {
  throw "Brak wartości mcpServers.azure-devops.env.PERSONAL_ACCESS_TOKEN w ~/.claude.json"
}

$hdrs  = @{ Authorization = "Basic $b64"; "Content-Type" = "application/octet-stream" }
$bytes = [IO.File]::ReadAllBytes("C:\tmp\screen.png")

try {
  $resp = Invoke-WebRequest `
    -Uri "https://dev.azure.com/DTCode/2588c384-a691-4407-b553-194b87829089/_apis/wit/attachments?fileName=screen.png&api-version=7.1" `
    -Method Post -Headers $hdrs -Body $bytes -UseBasicParsing
  $status = [int]$resp.StatusCode
} catch {
  if ($_.Exception.Response) {
    $status = [int]$_.Exception.Response.StatusCode
  } else {
    throw
  }
}

if ($status -in 203, 401) {
  throw "Błąd uwierzytelnienia ADO (HTTP $status) — wygasły token PAT albo błędny nagłówek Authorization."
}
if ($status -ne 201) {
  throw "Nieoczekiwany status ADO przy wgrywaniu załącznika: HTTP $status"
}

$url = ($resp.Content | ConvertFrom-Json).url
if ([string]::IsNullOrWhiteSpace($url)) {
  throw "Odpowiedź 201 Created nie zawiera pola url."
}
```

Dopiero po potwierdzeniu statusu `201 Created` i niepustego `$url` (np. `https://dev.azure.com/DTCode/2588c384-a691-4407-b553-194b87829089/_apis/wit/attachments/{guid}?fileName=screen.png`) podpinaj załącznik przez `wit_work_item_attachment_link` albo wstawiaj obraz do opisu.

> 🔑 Skrypt odczytuje token z `~/.claude.json` (`mcpServers.azure-devops.env.PERSONAL_ACCESS_TOKEN`). W środowiskach korzystających z innej ścieżki konfiguracji MCP (np. `~/.gemini/config/mcp_config.json`) podmień `$cfgPath`.
>
> ⚠️ Odpowiedź `203` (zwrócona strona logowania) lub `401` oznacza **wygasły token PAT albo błędnie zbudowany nagłówek `Authorization`** (np. ponowne kodowanie Base64 już zakodowanej wartości). Najpierw sprawdź budowę nagłówka (`"Basic " + wartość` bez ponownego Base64); jeśli nagłówek jest poprawny albo `203`/`401` zwraca samo wywołanie MCP, **nie kombinuj z innymi tokenami** — PAT wygasł, zgłoś użytkownikowi konieczność odnowienia.
> Nigdy nie wypisuj wartości tokenu ani nagłówka w odpowiedzi ani w logach.

**Krok 3 — Wstaw URL do opisu (czysty, bez enkodowania)**

W HTML opisu używaj bezpośrednio zwróconego URL-a w atrybucie `src`. **Nigdy nie owijaj go cudzysłowami wewnątrz łańcucha ani nie URL-enkoduj:**

```html
<!-- ✅ POPRAWNIE -->
<img src="https://dev.azure.com/DTCode/2588c384-a691-4407-b553-194b87829089/_apis/wit/attachments/abc-123?fileName=screen.png" style="max-width:100%;border:1px solid #e2e8f0;border-radius:8px;margin:12px 0;display:block;" />

<!-- ❌ ŹLE — podwójne enkodowanie, cudzysłowy w URL -->
<img src="%22https%3a//dev.azure.com/...%22" />
```

**Krok 4 — Dodaj opis z obrazkami przez `wit_work_item_write` (`action: "update"`)**

Przekaż HTML z czystymi URL-ami (Wzorzec 3). Sprawdź wynik — jeśli obrazki nie są widoczne, to URL jest nieprawidłowy.

### Kiedy dodawać screenshoty

- **Zawsze, gdy istnieją odpowiednie node-idy w Figmie** dla danej funkcjonalności.
- Minimum jeden screenshot na PBI (chyba że funkcjonalność jest czysto backendowa i nie ma UI).
- Preferowane: oddzielny screenshot dla widoku desktop i mobile (jeśli obie wersje istnieją w Figmie).

---

## Ogólne zasady

- Zawsze twórz elementy **sekwencyjnie** – potrzebujesz ID rodzica przed utworzeniem dziecka.
- Używaj narzędzia `azure-devops` (MCP) do wszystkich operacji.
- Po zakończeniu wypisz podsumowanie z ID i linkami do wszystkich utworzonych elementów.
- Jeśli jakikolwiek krok się nie powiedzie, zatrzymaj się i zgłoś błąd użytkownikowi.

---

## Język i treść zadań

- **Wszystkie treści** (tytuły, opisy, kryteria akceptacji, komentarze, kroki do reprodukcji) pisz **wyłącznie po polsku**.
- Tytuły tasków stałych (`Fix`, `Retest`, `FE`, `BE`, `DB`, `Figma`, `Manual tests`, `E2e tests`) pozostają w oryginalnej formie – są identyfikatorami, nie opisami.

---

## Linkowanie do Figmy

- Jeśli użytkownik poda link do Figmy lub konkretnego mockupu, **dołącz go do opisu** odpowiedniego elementu (PBI, Bug lub task `Figma`).
- Jeśli użytkownik nie poda linka, a zadanie dotyczy widoku/ekranu – **zapytaj**, czy jest odpowiedni mockup w Figmie, który możesz dołączyć.
- Linki do Figmy wstawiaj w opisie w formacie:

  ```
  🎨 Mockup: [Nazwa ekranu / sekcji](https://figma.com/...)
  ```

- Jeśli do jednego zadania pasuje kilka mockupów, dołącz wszystkie z krótkim opisem czego dotyczą.

---

## Instrukcja MCP — Jak wywoływać narzędzia (wzorce z praktyki)

> Sekcja opisuje **konkretne wywołania MCP** sprawdzone w praktyce. Skup się na niej zanim zaczniesz tworzyć elementy.

### Narzędzia i kiedy ich używać

| Narzędzie i akcja | Do czego | Uwagi |
|---|---|---|
| `wit_work_item_write` (`action: "create"`) | Tworzenie Feature / PBI / Bug / Task (tytuł + pola podstawowe) | **Nie przekazuj opisu tu — dodaj go osobno przez `action: "update"`** |
| `wit_work_item_write` (`action: "add_child"`) | Tworzenie 6 tasków pod jednym PBI — tworzy I linkuje w jednym wywołaniu | ⚠️ **NIE obsługuje `assignedTo` per item** — po wywołaniu ZAWSZE wykonaj `update_batch` dla assignee (Wzorzec 5) |
| `wit_work_item_link_write` (`action: "link"`) | Przypięcie rodzica (Epic→Feature, Feature→PBI) | Działa batchowo — do 6+ linków naraz |
| `wit_work_item_write` (`action: "update"`) | Dodanie opisu HTML i kryteriów akceptacji do pojedynczego elementu | Przyjmuje `updates` (`op`, `path`, `value`; **bez pola `format`**) |
| `wit_work_item_write` (`action: "update_batch"`) | Masowa aktualizacja pól wielu elementów naraz — m.in. ustawienie assignee na taskach | Wymaga niepustej tablicy `batchUpdates` (tu dostępne jest pole `format: "Html" \| "Markdown"`) |
| `wit_work_item_attachment_upload` | Wgranie załącznika (np. PNG z Figmy jako czysty Base64) | Zwraca `url` do użycia w `<img src="...">`; opcjonalnie podpięcie przez `wit_work_item_attachment_link` |

---

### Wzorzec 1 — Tworzenie Feature / PBI / Task

Wywołaj `wit_work_item_write` z `action: "create"` i wypełnioną tablicą `fields`. **Tablica nigdy nie może być pusta** — minimum to `System.Title`.

```
wit_work_item_write(
  action: "create",
  project: "TachoPing",
  workItemType: "Feature",          // lub "Product Backlog Item" / "Task" / "Bug"
  fields: [
    { name: "System.Title",         value: "Landing page" },
    { name: "System.AssignedTo",    value: "kontakt@DTCode.pl" },
    { name: "System.IterationPath", value: "TachoPing\\Sprint 1" }
  ]
)
→ zanotuj id z odpowiedzi
```

> ⚠️ **NIE DODAWAJ** `System.Description` ani `Microsoft.VSTS.Common.AcceptanceCriteria` w tym kroku — opis i kryteria dodaj osobno (Wzorzec 3).

---

### Wzorzec 2 — Linkowanie rodzica

Po utworzeniu elementu (lub grupy elementów) przypnij go do rodzica przez `wit_work_item_link_write` z `action: "link"`. Działa batchowo — możesz podać do kilkunastu par naraz.

```
wit_work_item_link_write(
  action: "link",
  project: "TachoPing",
  updates: [
    { id: <ID_dziecka_1>, linkToId: <ID_rodzica>, type: "parent" },
    { id: <ID_dziecka_2>, linkToId: <ID_rodzica>, type: "parent" },
    ...
  ]
)
```

**Typowe łańcuchy:**
- Feature → Epic: `{ id: <featureId>, linkToId: <epicId>, type: "parent" }`
- PBI → Feature: `{ id: <pbiId>, linkToId: <featureId>, type: "parent" }`
- Task → PBI: `{ id: <taskId>, linkToId: <pbiId>, type: "parent" }`

---

### Wzorzec 3 — Dodanie opisu i kryteriów akceptacji (HTML)

Po utworzeniu i zlinkowaniu elementu zaktualizuj opis i AC przez `wit_work_item_write` z `action: "update"`. Schemat `updates` akceptuje wyłącznie `op`, `path`, `value` (**bez pola `format`** — jego dodanie powoduje błąd walidacji). Dla świeżo utworzonego elementu zapisuj HTML wprost do `/fields/System.Description` i `/fields/Microsoft.VSTS.Common.AcceptanceCriteria` — nowe pola wieloliniowe są domyślnie w formacie HTML. Pole raz przełączone na Markdown nie wraca do HTML.

```
wit_work_item_write(
  action: "update",
  id: <ID_elementu>,
  updates: [
    {
      op:    "add",
      path:  "/fields/System.Description",
      value: "<h3>User Story</h3><p>Jako ... chcę ... żeby ...</p><h3>Opis</h3><ul><li>...</li></ul>"
    },
    {
      op:    "add",
      path:  "/fields/Microsoft.VSTS.Common.AcceptanceCriteria",
      value: "<ul><li>Kryterium 1</li><li>Kryterium 2</li></ul>"
    }
  ]
)
```

> 🛈 Jeśli aktualizujesz opisy wielu nowych elementów naraz przez `wit_work_item_write` z `action: "update_batch"` (struktura `batchUpdates` jak w Wzorcu 5, Krok B), możesz podać we wpisach `format: "Html"` (parametr `format` istnieje w `batchUpdates`, `fields` przy `create` oraz `items` przy `add_child`, gdzie domyślnie ma wartość `"Markdown"`).

**Zasady HTML w opisach ADO:**
- Używaj tagów: `<h3>`, `<p>`, `<ul>`, `<li>`, `<strong>`, `<em>`, `<code>`
- `&` w URL-ach zamieniaj na `&amp;` (np. `?node-id=178-4595&amp;m=dev`)
- Polskie znaki (ą, ę, ó, ź itd.) działają bezpośrednio w `value`
- Nie używaj `<h1>`, `<h2>` — ADO renderuje je zbyt duże; `<h3>` jest odpowiednie dla sekcji

---

### Wzorzec 4 — Optymalny przepływ dla wielu PBI naraz

Gdy tworzysz np. 6 PBI pod jednym Feature, nie twórz → linkuj → opisuj → twórz taski każdego osobno. Zrób to w 5 etapach (pełne parametry wywołań w Wzorcach 1, 2, 3 i 5):

```
ETAP 1 — Utwórz wszystkie PBI (sam tytuł + podstawowe pola)
  Dla każdego PBI (#1…#6) wywołaj wit_work_item_write z action: "create"
  według Wzorca 1 (project: "TachoPing", workItemType: "Product Backlog Item",
  fields z System.Title, System.AssignedTo, System.IterationPath)
  → zanotuj ID zwrócone z odpowiedzi (np. 331…336).

ETAP 2 — Zlinkuj wszystkie PBI naraz (jeden batch call według Wzorca 2)
  wit_work_item_link_write(action: "link", project: "TachoPing", updates: [
    { id: 331, linkToId: <featureId>, type: "parent" },
    ...
    { id: 336, linkToId: <featureId>, type: "parent" }
  ])

ETAP 3 — Zaktualizuj opisy i AC jeden po jednym
  Dla każdego PBI (331…336) wywołaj wit_work_item_write z action: "update"
  według Wzorca 3 (id + updates z HTML dla /fields/System.Description
  i /fields/Microsoft.VSTS.Common.AcceptanceCriteria).

ETAP 4 — Utwórz 6 tasków pod każdym PBI
  Dla każdego PBI (331…336) wywołaj wit_work_item_write z action: "add_child"
  według Wzorca 5 (Krok A): podaj parentId, workItemType: "Task",
  project: "TachoPing" oraz items jako obiekty z polami title, description,
  iterationPath i format: "Html".
  → zanotuj ID wszystkich zwróconych tasków (kolejność: FE, BE, DB, Figma, Manual, E2e)

ETAP 5 — Ustaw assignee na WSZYSTKICH taskach
  ⚠️ action: "add_child" NIE ustawia assignedTo — ten etap jest OBOWIĄZKOWY.
  Wywołaj wit_work_item_write z action: "update_batch" według Wzorca 5 (Krok B):
  → batchUpdates dla FE/BE/DB (pozycje 1-3 każdego PBI) → kontakt@DTCode.pl
  → batchUpdates dla Figma/Manual/E2e (pozycje 4-6 każdego PBI) → Piotr.Tunski@DTCode.pl
```

> ⛔ **STOP po Etapie 3 = błąd.** PBI bez tasków to niekompletna praca. Etapy 4 i 5 są obowiązkowe i nierozłączne.

---

### Wzorzec 5 — Tworzenie tasków pod PBI i ustawianie assignee

Używaj `wit_work_item_write` z `action: "add_child"` per PBI (tworzy i linkuje jednym wywołaniem), a następnie `wit_work_item_write` z `action: "update_batch"` (`batchUpdates`) dla assignee. To jedyna poprawna kolejność — `add_child` nie obsługuje `assignedTo` per item.

```
// KROK A — Utwórz 6 tasków pod PBI (auto-linkuje do rodzica)
wit_work_item_write(
  action: "add_child",
  parentId: <pbiId>,
  workItemType: "Task",
  project: "TachoPing",
  items: [
    { title: "FE",           iterationPath: "TachoPing\\Sprint 1",   description: "", format: "Html" },
    { title: "BE",           iterationPath: "TachoPing\\Sprint 1",   description: "", format: "Html" },
    { title: "DB",           iterationPath: "TachoPing\\Sprint 1",   description: "", format: "Html" },
    { title: "Figma",        iterationPath: "TachoPing\\Sprint 1",   description: "", format: "Html" },
    { title: "Manual tests", iterationPath: "TachoPing\\Sprint 1",   description: "", format: "Html" },
    { title: "E2e tests",    iterationPath: "TachoPing\\E2e Sprint", description: "", format: "Html" }
  ]
)
→ Odpowiedź zwraca IDs w tej samej kolejności: [FE_id, BE_id, DB_id, Figma_id, Manual_id, E2e_id]
```

```
// KROK B — Ustaw assignee w batch (kontakt dla FE/BE/DB, Piotr dla Figma/Manual/E2e)
// Dla 6 PBI = 18 tasków kontakt + 18 tasków Piotr — wszystko w 2 wywołaniach batch

wit_work_item_write(
  action: "update_batch",
  batchUpdates: [
    // FE/BE/DB wszystkich PBI → kontakt
    { id: <FE_331>, op: "Add", path: "/fields/System.AssignedTo", value: "kontakt@DTCode.pl" },
    { id: <BE_331>, op: "Add", path: "/fields/System.AssignedTo", value: "kontakt@DTCode.pl" },
    { id: <DB_331>, op: "Add", path: "/fields/System.AssignedTo", value: "kontakt@DTCode.pl" },
    ... (analogicznie dla pozostałych PBI)
  ]
)

wit_work_item_write(
  action: "update_batch",
  batchUpdates: [
    // Figma/Manual/E2e wszystkich PBI → Piotr
    { id: <Figma_331>,  op: "Add", path: "/fields/System.AssignedTo", value: "Piotr.Tunski@DTCode.pl" },
    { id: <Manual_331>, op: "Add", path: "/fields/System.AssignedTo", value: "Piotr.Tunski@DTCode.pl" },
    { id: <E2e_331>,    op: "Add", path: "/fields/System.AssignedTo", value: "Piotr.Tunski@DTCode.pl" },
    ... (analogicznie dla pozostałych PBI)
  ]
)
```

> ⚠️ Można też zrobić oba batche w jednym wywołaniu (FE/BE/DB + Figma/Manual/E2e razem = 36 wpisów).

---

### Definicja ukończenia (Definition of Done) dla PBI

Przed zakończeniem sprawdź, że każde PBI ma wszystkie poniższe elementy. **Brak któregokolwiek = praca niekompletna.**

| Element | Pole/narzędzie |
|---|---|
| ✅ Tytuł | `System.Title` |
| ✅ Przypisany do: kontakt@DTCode.pl | `System.AssignedTo` |
| ✅ Sprint 1 | `System.IterationPath` |
| ✅ Rodzic (Feature) | `wit_work_item_link_write` (`action: "link"`) |
| ✅ Opis HTML (User Story + szczegóły + Figma) | `System.Description` via `wit_work_item_write` (`action: "update"`) |
| ✅ Kryteria akceptacji HTML | `AcceptanceCriteria` via `wit_work_item_write` (`action: "update"`) |
| ✅ 6 tasków: FE, BE, DB, Figma, Manual tests, E2e tests | `wit_work_item_write` (`action: "add_child"`) |
| ✅ FE/BE/DB → kontakt@DTCode.pl, Sprint 1 | `wit_work_item_write` (`action: "update_batch"`) |
| ✅ Figma/Manual → Piotr.Tunski@DTCode.pl, Sprint 1 | `wit_work_item_write` (`action: "update_batch"`) |
| ✅ E2e tests → Piotr.Tunski@DTCode.pl, E2e Sprint | `wit_work_item_write` (`action: "update_batch"`) |

---

### Częste błędy i jak ich uniknąć

| Błąd | Przyczyna | Rozwiązanie |
|---|---|---|
| `Cannot convert undefined or null to object` | Przekazano pustą tablicę `[]` do `fields`, `items`, `updates` lub `batchUpdates` | Zawsze podaj niepustą tablicę (dla `create` minimum `System.Title`) |
| Opis nie pojawia się w ADO | Próba dodania `System.Description` w `wit_work_item_write(action: "create")` | Twórz najpierw bez opisu, potem `wit_work_item_write(action: "update")` |
| Błąd walidacji `format` przy `action: "update"` lub HTML jako plain text | `updates` w `action: "update"` nie przyjmuje pola `format` (`additionalProperties: false`), a pole raz przełączone na Markdown nie wraca do HTML | Dla świeżo utworzonych elementów zapisuj HTML wprost w `/fields/System.Description` i `/fields/Microsoft.VSTS.Common.AcceptanceCriteria` (domyślnie HTML), bez pola `format`; w `add_child` podawaj `format: "Html"` (domyślnie jest `"Markdown"`) |
| Błąd w `action: "update_batch"` (`batchUpdates is required`) | Przekazano parametr `updates` zamiast `batchUpdates` | Dla `action: "update_batch"` użyj tablicy `batchUpdates` (z `op: "Add" \| "Replace" \| "Remove"`) |
| Link rodzic-dziecko nie działa | Użyto złego `type` w `wit_work_item_link_write` | Dla hierarchii zawsze `type: "parent"` (nie `"child"`) |
| `&` w URL uszkadza HTML | Dosłowny `&` w atrybucie href | Zamień na `&amp;` w wartości pola HTML |
| FE/BE/DB bez assignee po `wit_work_item_write(action: "add_child")` | Akcja `add_child` nie obsługuje `assignedTo` per item | Po każdym wywołaniu `wit_work_item_write(action: "add_child")` obowiązkowo `wit_work_item_write(action: "update_batch")` dla FE/BE/DB → kontakt@DTCode.pl |
| PBI bez tasków po zakończeniu bulk-flow | Bot zatrzymał się na opisach, nie wykonał Etapów 4-5 | Wzorzec 4 ma 5 etapów — Etapy 4 i 5 (taski + assignee) są obowiązkowe, nie opcjonalne |
| ADO zwraca `203` / `401` lub stronę logowania | Wygasły PAT albo błędnie zbudowany nagłówek `Authorization` (np. podwójny Base64) | Dla REST sprawdź status przed parsowaniem i budowę nagłówka (`"Basic " + wartość` bez ponownego kodowania Base64); jeśli nagłówek jest poprawny lub błąd zwraca MCP, zgłoś użytkownikowi konieczność odnowienia tokenu |
