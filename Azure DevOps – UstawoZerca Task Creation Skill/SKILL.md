---
name: azure-devops-ustawozerca
description: >
  Zasady tworzenia tasków w Azure DevOps dla projektu UstawoŻerca.
  Obsługuje dwa tryby: Bug (z sub-taskami Fix i Retest) oraz PBI
  (z pełnym zestawem tasków FE/BE/DB/Figma/Manual tests/E2e tests).
  Wymusza weryfikację hierarchii Epic→Feature przed utworzeniem PBI,
  pilnuje przypisań i sprintów, treści pisze po polsku, linkuje do Figmy.
version: "1.0"
language: pl
project: UstawoŻerca
organization: DTCode
remote:
  github_raw: "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/Azure%20DevOps%20%E2%80%93%20UstawoZerca%20Task%20Creation%20Skill/SKILL.md"
  github_page: "https://github.com/DTCodePL/Claude_Skills/blob/main/Azure%20DevOps%20%E2%80%93%20UstawoZerca%20Task%20Creation%20Skill/SKILL.md"
---

# Azure DevOps – UstawoŻerca Task Creation Skill

## ⚡ Auto-aktualizacja — WYKONAJ JAKO PIERWSZY KROK

**Zanim cokolwiek zrobisz**, sprawdź czy istnieje nowsza wersja skilla na GitHubie i ewentualnie zaktualizuj lokalną kopię.

### Procedura (wykonaj zawsze przy wczytaniu skilla)

**Krok 1 — Pobierz zdalną wersję przez bash_tool:**
```bash
curl -sL "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/Azure%20DevOps%20%E2%80%93%20UstawoZerca%20Task%20Creation%20Skill/SKILL.md" -o /tmp/skill_remote.md
head -10 /tmp/skill_remote.md
```

**Krok 2 — Porównaj wersje:**
- Wyciągnij `version:` z pobranego pliku (`grep 'version:' /tmp/skill_remote.md`)
- Porównaj z lokalną wersją (frontmatter `version:` w tym pliku)
- Jeśli zdalna wersja > lokalna → przejdź do Kroku 3
- Jeśli zdalna = lokalna → pomiń aktualizację, przejdź do zadania

**Krok 3 — Nadpisz lokalny skill (tylko jeśli nowsza wersja):**
```bash
cp /tmp/skill_remote.md /mnt/skills/user/azure-devops-ustawozerca/SKILL.md
```

**Krok 4 — Wczytaj nową wersję:**
```
view /mnt/skills/user/azure-devops-ustawozerca/SKILL.md
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
| Organizacja | `DTCode` |
| Projekt | `UstawoŻerca` |
| Team | `UstawoŻerca Team` |
| Sprint 1 URL | `https://dev.azure.com/DTCode/Ustawo%C5%BBerca/_sprints/taskboard/Ustawo%C5%BBerca%20Team/Ustawo%C5%BBerca/Sprint%201` |
| E2e Sprint URL | `https://dev.azure.com/DTCode/Ustawo%C5%BBerca/_sprints/taskboard/Ustawo%C5%BBerca%20Team/Ustawo%C5%BBerca/E2e%20Sprint` |

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

Używając narzędzia `get_screenshot` lub `use_figma` z Figma MCP pobierz PNG dla odpowiedniego node-id z projektu UstawoŻerca (klucz pliku: `NF2sMo5czLt2RCVpVHDDnb`).

```
get_screenshot(fileKey: "NF2sMo5czLt2RCVpVHDDnb", nodeId: "<node-id>")
```

Wynik to plik PNG (binarny lub base64). Zapisz go lokalnie do pliku tymczasowego.

**Krok 2 — Wgraj PNG jako załącznik do ADO**

Użyj ADO REST API (nie MCP — MCP nie obsługuje uploadu binarnych plików). Endpoint przyjmuje **nazwę projektu** (`Ustawo%C5%BBerca`) zamiast GUID — działa tak samo:

```powershell
$PAT   = "<token>"
$B64   = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(":$PAT"))
$hdrs  = @{ Authorization = "Basic $B64"; "Content-Type" = "application/octet-stream" }
$bytes = [IO.File]::ReadAllBytes("C:\tmp\screen.png")
$resp  = Invoke-WebRequest `
  -Uri "https://dev.azure.com/DTCode/Ustawo%C5%BBerca/_apis/wit/attachments?fileName=screen.png&api-version=7.1" `
  -Method Post -Headers $hdrs -Body $bytes -UseBasicParsing
$url = ($resp.Content | ConvertFrom-Json).url
```

`$url` to czysty URL załącznika — np. `https://dev.azure.com/DTCode/Ustawo%C5%BBerca/_apis/wit/attachments/{guid}?fileName=screen.png`.

> 🔑 PAT znajdziesz w `C:\Users\Damian\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude_desktop_config.json` pod kluczem `PERSONAL_ACCESS_TOKEN` (wartość jest base64 — zdekoduj ją najpierw).

**Krok 3 — Wstaw URL do opisu (czysty, bez enkodowania)**

W HTML opisu używaj bezpośrednio zwróconego URL-a w atrybucie `src`. **Nigdy nie owijaj go cudzysłowami wewnątrz łańcucha ani nie URL-enkoduj:**

```html
<!-- ✅ POPRAWNIE -->
<img src="https://dev.azure.com/DTCode/Ustawo%C5%BBerca/_apis/wit/attachments/abc-123?fileName=screen.png" style="max-width:100%;border:1px solid #e2e8f0;border-radius:8px;margin:12px 0;display:block;" />

<!-- ❌ ŹLE — podwójne enkodowanie, cudzysłowy w URL -->
<img src="%22https%3a//dev.azure.com/...%22" />
```

**Krok 4 — Dodaj opis z obrazkami przez `wit_update_work_item`**

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

| Narzędzie | Do czego | Uwagi |
|---|---|---|
| `wit_create_work_item` | Tworzenie Feature / PBI / Bug (tytuł + pola podstawowe) | **Nigdy nie przekazuj opisu tu — zrób to osobno przez update** |
| `wit_add_child_work_items` | Tworzenie 6 tasków pod jednym PBI — tworzy I linkuje w jednym wywołaniu | ⚠️ **NIE obsługuje `assignedTo` per item** — po wywołaniu ZAWSZE wykonaj batch update assignee (patrz Wzorzec 5) |
| `wit_work_items_link` | Przypięcie rodzica (Epic→Feature, Feature→PBI) | Działa batchowo — do 6+ linków naraz |
| `wit_update_work_item` | Dodanie opisu HTML i kryteriów akceptacji do PBI | Osobne wywołanie po utworzeniu |
| `wit_update_work_items_batch` | Masowa aktualizacja pól wielu elementów naraz — używane do ustawienia assignee na taskach | Wymaga niepustej tablicy `updates` |

---

### Wzorzec 1 — Tworzenie Feature / PBI / Task

Wywołaj `wit_create_work_item` z wypełnioną tablicą `fields`. **Tablica nigdy nie może być pusta** — minimum to `System.Title`.

```
wit_create_work_item(
  project: "UstawoŻerca",
  workItemType: "Feature",          // lub "Product Backlog Item" / "Task" / "Bug"
  fields: [
    { name: "System.Title",         value: "Landing page" },
    { name: "System.AssignedTo",    value: "kontakt@DTCode.pl" },
    { name: "System.IterationPath", value: "UstawoŻerca\\Sprint 1" }
  ]
)
→ zanotuj id z odpowiedzi
```

> ⚠️ **NIE DODAWAJ** `System.Description` ani `Microsoft.VSTS.Common.AcceptanceCriteria` w tym kroku — ADO je zignoruje lub zwróci błąd. Opis dodaj osobno (Wzorzec 3).

---

### Wzorzec 2 — Linkowanie rodzica

Po utworzeniu elementu (lub grupy elementów) przypnij go do rodzica przez `wit_work_items_link`. Działa batchowo — możesz podać do kilkunastu par naraz.

```
wit_work_items_link(
  project: "UstawoŻerca",
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

Po utworzeniu i zlinkowaniu elementu zaktualizuj opis i AC przez `wit_update_work_item`. Format musi być `Html` — ustaw go **na poziomie każdego obiektu update**, nie globalnie.

```
wit_update_work_item(
  id: <ID_elementu>,
  updates: [
    {
      path:   "/fields/System.Description",
      value:  "<h3>User Story</h3><p>Jako ... chcę ... żeby ...</p><h3>Opis</h3><ul><li>...</li></ul>",
      format: "Html"
    },
    {
      path:   "/fields/Microsoft.VSTS.Common.AcceptanceCriteria",
      value:  "<ul><li>Kryterium 1</li><li>Kryterium 2</li></ul>",
      format: "Html"
    }
  ]
)
```

**Zasady HTML w opisach ADO:**
- Używaj tagów: `<h3>`, `<p>`, `<ul>`, `<li>`, `<strong>`, `<em>`, `<code>`
- `&` w URL-ach zamieniaj na `&amp;` (np. `?node-id=178-4595&amp;m=dev`)
- Polskie znaki (ą, ę, ó, ź itd.) działają bezpośrednio w `value`
- Nie używaj `<h1>`, `<h2>` — ADO renderuje je zbyt duże; `<h3>` jest odpowiednie dla sekcji

---

### Wzorzec 4 — Optymalny przepływ dla wielu PBI naraz

Gdy tworzysz np. 6 PBI pod jednym Feature, nie twórz → linkuj → opisuj → twórz taski każdego osobno. Zrób to w 5 etapach:

```
ETAP 1 — Utwórz wszystkie PBI (sam tytuł + podstawowe pola)
  wit_create_work_item(PBI #1) → ID: 331
  wit_create_work_item(PBI #2) → ID: 332
  ...
  wit_create_work_item(PBI #6) → ID: 336

ETAP 2 — Zlinkuj wszystkie PBI naraz (jeden batch call)
  wit_work_items_link(updates: [
    { id: 331, linkToId: <featureId>, type: "parent" },
    ...
    { id: 336, linkToId: <featureId>, type: "parent" }
  ])

ETAP 3 — Zaktualizuj opisy i AC jeden po jednym
  wit_update_work_item(331, description + AC)
  wit_update_work_item(332, description + AC)
  ...
  wit_update_work_item(336, description + AC)

ETAP 4 — Utwórz 6 tasków pod każdym PBI (wit_add_child_work_items)
  wit_add_child_work_items(parentId: 331, items: [FE, BE, DB, Figma, Manual tests, E2e tests])
  wit_add_child_work_items(parentId: 332, items: [...])
  ...
  wit_add_child_work_items(parentId: 336, items: [...])
  → zanotuj ID wszystkich zwróconych tasków (kolejność: FE, BE, DB, Figma, Manual, E2e)

ETAP 5 — Ustaw assignee na WSZYSTKICH taskach (wit_update_work_items_batch)
  ⚠️ wit_add_child_work_items NIE ustawia assignedTo — ten etap jest OBOWIĄZKOWY
  → batch update FE/BE/DB (pozycje 1-3 każdego PBI) → kontakt@DTCode.pl
  → batch update Figma/Manual/E2e (pozycje 4-6 każdego PBI) → Piotr.Tunski@DTCode.pl
```

> ⛔ **STOP po Etapie 3 = błąd.** PBI bez tasków to niekompletna praca. Etapy 4 i 5 są obowiązkowe i nierozłączne.

---

### Wzorzec 5 — Tworzenie tasków pod PBI i ustawianie assignee

Używaj `wit_add_child_work_items` per PBI (tworzy i linkuje jednym wywołaniem), a następnie `wit_update_work_items_batch` dla assignee. To jedyna poprawna kolejność — narzędzie nie obsługuje `assignedTo` per item.

```
// KROK A — Utwórz 6 tasków pod PBI (auto-linkuje do rodzica)
wit_add_child_work_items(
  parentId: <pbiId>,
  workItemType: "Task",
  project: "UstawoŻerca",
  items: [
    { title: "FE",           iterationPath: "UstawoŻerca\\Sprint 1",   description: "" },
    { title: "BE",           iterationPath: "UstawoŻerca\\Sprint 1",   description: "" },
    { title: "DB",           iterationPath: "UstawoŻerca\\Sprint 1",   description: "" },
    { title: "Figma",        iterationPath: "UstawoŻerca\\Sprint 1",   description: "" },
    { title: "Manual tests", iterationPath: "UstawoŻerca\\Sprint 1",   description: "" },
    { title: "E2e tests",    iterationPath: "UstawoŻerca\\E2e Sprint",  description: "" }
  ]
)
→ Odpowiedź zwraca IDs w tej samej kolejności: [FE_id, BE_id, DB_id, Figma_id, Manual_id, E2e_id]
```

```
// KROK B — Ustaw assignee w batch (kontakt dla FE/BE/DB, Piotr dla Figma/Manual/E2e)
// Dla 6 PBI = 18 tasków kontakt + 18 tasków Piotr — wszystko w 2 wywołaniach batch

wit_update_work_items_batch(updates: [
  // FE/BE/DB wszystkich PBI → kontakt
  { id: <FE_331>, path: "/fields/System.AssignedTo", value: "kontakt@DTCode.pl" },
  { id: <BE_331>, path: "/fields/System.AssignedTo", value: "kontakt@DTCode.pl" },
  { id: <DB_331>, path: "/fields/System.AssignedTo", value: "kontakt@DTCode.pl" },
  ... (analogicznie dla pozostałych PBI)
])

wit_update_work_items_batch(updates: [
  // Figma/Manual/E2e wszystkich PBI → Piotr
  { id: <Figma_331>, path: "/fields/System.AssignedTo", value: "Piotr.Tunski@DTCode.pl" },
  { id: <Manual_331>, path: "/fields/System.AssignedTo", value: "Piotr.Tunski@DTCode.pl" },
  { id: <E2e_331>,   path: "/fields/System.AssignedTo", value: "Piotr.Tunski@DTCode.pl" },
  ... (analogicznie dla pozostałych PBI)
])
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
| ✅ Rodzic (Feature) | `wit_work_items_link` |
| ✅ Opis HTML (User Story + szczegóły + Figma) | `System.Description` via `wit_update_work_item` |
| ✅ Kryteria akceptacji HTML | `AcceptanceCriteria` via `wit_update_work_item` |
| ✅ 6 tasków: FE, BE, DB, Figma, Manual tests, E2e tests | `wit_add_child_work_items` |
| ✅ FE/BE/DB → kontakt@DTCode.pl, Sprint 1 | `wit_update_work_items_batch` |
| ✅ Figma/Manual → Piotr.Tunski@DTCode.pl, Sprint 1 | `wit_update_work_items_batch` |
| ✅ E2e tests → Piotr.Tunski@DTCode.pl, E2e Sprint | `wit_update_work_items_batch` |

---

### Częste błędy i jak ich uniknąć

| Błąd | Przyczyna | Rozwiązanie |
|---|---|---|
| `Cannot convert undefined or null to object` | Przekazano pustą tablicę `[]` do `fields` lub `items` | Zawsze podaj co najmniej `System.Title` w tablicy |
| Opis nie pojawia się w ADO | Próba dodania `System.Description` w `wit_create_work_item` | Twórz najpierw bez opisu, potem `wit_update_work_item` |
| HTML renderuje się jako plain text | Brak `format: "Html"` przy update | Dodaj `format: "Html"` do każdego obiektu w `updates` |
| Link rodzic-dziecko nie działa | Użyto złego `type` | Dla hierarchii zawsze `type: "parent"` (nie `"child"`) |
| `&` w URL uszkadza HTML | Dosłowny `&` w atrybucie href | Zamień na `&amp;` w wartości pola HTML |
| FE/BE/DB bez assignee po `wit_add_child_work_items` | Narzędzie nie obsługuje `assignedTo` per item | Po każdym wywołaniu `wit_add_child_work_items` obowiązkowo `wit_update_work_items_batch` dla FE/BE/DB → kontakt@DTCode.pl |
| PBI bez tasków po zakończeniu bulk-flow | Bot zatrzymał się na opisach, nie wykonał Etapów 4-5 | Wzorzec 4 ma 5 etapów — Etapy 4 i 5 (taski + assignee) są obowiązkowe, nie opcjonalne |
