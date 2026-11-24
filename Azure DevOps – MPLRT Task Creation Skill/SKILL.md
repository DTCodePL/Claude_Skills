---
name: azure-devops-mplrt
description: >
  Zasady tworzenia tasków w Azure DevOps dla projektu MPLRT.
  Obsługuje dwa tryby: Bug (z sub-taskami Fix i Retest) oraz PBI
  (z pełnym zestawem tasków FE/BE/DB/Figma/Manual tests/E2e tests).
  Wymusza weryfikację hierarchii Epic→Feature przed utworzeniem PBI,
  pilnuje przypisań i sprintów, treści pisze po polsku, czerpie opisy
  z zatwierdzonej dokumentacji produktowej i linkuje do dokumentacji interfejsów lub Figmy.
version: '1.0'
language: pl
project: MPLRT
organization: DTCode
remote:
  github_raw: 'https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/Azure%20DevOps%20%E2%80%93%20MPLRT%20Task%20Creation%20Skill/SKILL.md'
  github_page: 'https://github.com/DTCodePL/Claude_Skills/blob/main/Azure%20DevOps%20%E2%80%93%20MPLRT%20Task%20Creation%20Skill/SKILL.md'
---

# Azure DevOps – MPLRT Task Creation Skill

## ⚡ Auto-aktualizacja — WYKONAJ JAKO PIERWSZY KROK

**Zanim cokolwiek zrobisz**, sprawdź czy istnieje nowsza wersja skilla na GitHubie i ewentualnie zaktualizuj lokalną kopię.

### Procedura (wykonaj zawsze przy wczytaniu skilla)

**Krok 1 — Pobierz zdalną wersję przez bash_tool:**

```bash
curl -sL "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/Azure%20DevOps%20%E2%80%93%20MPLRT%20Task%20Creation%20Skill/SKILL.md" -o /tmp/skill_remote.md
head -20 /tmp/skill_remote.md
```

**Krok 2 — Porównaj wersje:**

- Wyciągnij `version:` z pobranego pliku (`grep 'version:' /tmp/skill_remote.md`)
- Porównaj z lokalną wersją (frontmatter `version:` w tym pliku)
- Jeśli zdalna wersja > lokalna → przejdź do Kroku 3
- Jeśli zdalna = lokalna → pomiń aktualizację, przejdź do zadania

**Krok 3 — Nadpisz lokalny skill (tylko jeśli nowsza wersja):**

```bash
cp /tmp/skill_remote.md <ścieżka_do_lokalnego_SKILL.md>
```

**Krok 4 — Wczytaj nową wersję** i poinformuj użytkownika: „Zaktualizowałem skill v{stara} → v{nowa}. Przechodzę do zadania."

### Obsługa błędów pobierania

| Sytuacja                              | Co zrobić                                                                     |
| ------------------------------------- | ----------------------------------------------------------------------------- |
| `curl` zwraca 404                     | Repo prywatne lub plik jeszcze niewypchnięty — użyj lokalnej wersji, poinformuj |
| `curl` zwraca inny błąd / brak sieci  | Pomiń aktualizację, użyj lokalnej wersji                                       |
| Plik pusty lub niepoprawny YAML       | Pomiń aktualizację, użyj lokalnej wersji                                       |

> ⚠️ Aktualizacja jest **opcjonalna** jeśli niedostępna — nigdy nie blokuj zadania z powodu braku dostępu do GitHuba.

---

## Projekt / organizacja

> ✅ **Zweryfikowane w API Azure DevOps 2026-11-24** — nazwa projektu, team, ścieżki iteracji,
> typy work itemów i konta użytkowników zostały odczytane z REST API, nie przyjęte przez analogię.

| Pole             | Wartość                                                                                              |
| ---------------- | ---------------------------------------------------------------------------------------------------- |
| Organizacja      | `DTCode`                                                                                             |
| Projekt          | `MPLRT` (id `c400858f-3365-4c1a-b9d7-32b5c1e27e9d`)                                                  |
| Team             | `MPLRT Team` (id `9dd0b33d-cfd4-4a55-a01f-6b702f9f1bdc`; jedyny team w projekcie)                    |
| Iteracja domyślna | `MPLRT\Sprint 1` (bieżąca; istnieją też `Sprint 2`…`Sprint 6`, wszystkie w `MPLRT`)                  |
| Iteracja E2e     | **Brak** — w projekcie MPLRT nie istnieje dedykowana iteracja E2e; task `E2e tests` trafia do iteracji PBI (`MPLRT\Sprint 1`) |
| Area             | `MPLRT` — jedyna, bez pod-obszarów; nie ustawiaj `System.AreaPath` ręcznie                          |
| Projekt (URL)    | `https://dev.azure.com/DTCode/MPLRT`                                                                 |
| Sprint 1 URL     | `https://dev.azure.com/DTCode/MPLRT/_sprints/taskboard/MPLRT%20Team/MPLRT/Sprint%201`                 |
| E2e Sprint URL   | *brak* (nie istnieje osobna iteracja)                                                                |
| Repo FE          | `https://github.com/DTCodePL/MPLRTFE` (folder lokalny `D:\projects\DTCode\MPLRT_FE`)                  |
| Repo BE          | `https://github.com/DTCodePL/MPLRTBE` (folder lokalny `D:\projects\DTCode\MPLRT_BE`)                  |
| Figma            | **brak pliku** — do czasu makiety ekrany opisuje wyłącznie `interfejsy/` w dokumentacji produktowej  |
| Dokumentacja     | `d:\projects\DTCode\Dokumentacja\MPLRT` (po polsku, ze `status` we front matter)                     |

### Konta i typy work itemów (zweryfikowane)

| Rola   | Konto                      | Wyświetlana nazwa | Status weryfikacji API (2026-11-24) |
| ------ | -------------------------- | ----------------- | ----------------------------------- |
| Dev    | `kontakt@DTCode.pl`        | Damian D          | Zweryfikowane: Project Administrator, członek `MPLRT Team` |
| Tester | `Piotr.Tunski@DTCode.pl`   | Piotr Tuński      | Zweryfikowane: Project Administrator, uprawnienia w projekcie potwierdzone |

Dostępne typy: `Epic`, `Feature`, `Product Backlog Item`, `Task`, `Bug` — plus proces
zawiera custom `Bug standalone` (stany zweryfikowane w API: `New`, `Ready for tests`,
`In Progress`, `Done`). **Używaj zwykłego `Bug`**, chyba że użytkownik wprost
poprosi o `Bug standalone`.

### Jeśli stałe przestaną się zgadzać

Konfiguracja projektu może się zmienić po dacie weryfikacji. Gdy utworzenie work itema
zwróci błąd na `System.IterationPath` albo `System.AssignedTo`:

- **nie próbuj wariantów na ślepo** — wylistuj realne iteracje / sprawdź konto,
  pokaż wynik użytkownikowi i **zapytaj, czego użyć**,
- po ustaleniu poprawnych wartości **zaproponuj aktualizację tego skilla** na GitHubie
  (podbicie `version:`), żeby kolejne uruchomienie miało już właściwe stałe.

---

## TRYB A – Tworzenie Buga

### Krok 1 – Utwórz główny Bug

- Typ: `Bug`
- Przypisany do: `kontakt@DTCode.pl`
- Iteracja (sprint): **Sprint 1** (`MPLRT\Sprint 1`)

### Krok 2 – Utwórz sub-task: **Fix**

- Typ: `Task`
- Tytuł: `Fix`
- Rodzic: ← ID głównego buga z kroku 1
- Przypisany do: `kontakt@DTCode.pl`
- Iteracja (sprint): **Sprint 1** (`MPLRT\Sprint 1`)

### Krok 3 – Utwórz sub-task: **Retest**

- Typ: `Task`
- Tytuł: `Retest`
- Rodzic: ← ID głównego buga z kroku 1
- Przypisany do: `Piotr.Tunski@DTCode.pl`
- Iteracja (sprint): **Sprint 1** (`MPLRT\Sprint 1`)

### Kolejność wykonania dla Buga

```
1. Utwórz Bug → zanotuj ID
2. Utwórz Task "Fix"    (parent = Bug ID, sprint = Sprint 1)
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
  >
  > - **ID istniejącego** epica, LUB
  > - **Zaakceptuj nazwę** którą zaproponuję i sam go utworzę, LUB
  > - **Wpisz nazwę**, której mam użyć"

#### Feature

- Jeśli użytkownik **podał ID lub nazwę istniejącego featura** → użyj go.
- Jeśli nie podał → **zapytaj użytkownika**:
  > „Nie mam wskazanego Feature. Podaj:
  >
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
- Iteracja (sprint): **Sprint 1** (`MPLRT\Sprint 1`)

### Krok 4 – Utwórz 6 tasków pod PBI

Każdy task: Typ = `Task`, Rodzic = ID PBI z kroku 3.

| #   | Tytuł          | Przypisany do            | Sprint   |
| --- | -------------- | ------------------------ | -------- |
| 1   | `FE`           | `kontakt@DTCode.pl`      | Sprint 1 |
| 2   | `BE`           | `kontakt@DTCode.pl`      | Sprint 1 |
| 3   | `DB`           | `kontakt@DTCode.pl`      | Sprint 1 |
| 4   | `Figma`        | `Piotr.Tunski@DTCode.pl` | Sprint 1 |
| 5   | `Manual tests` | `Piotr.Tunski@DTCode.pl` | Sprint 1 |
| 6   | `E2e tests`    | `Piotr.Tunski@DTCode.pl` | Sprint 1 |

> 🛈 **Zestaw jest pełny nawet teraz, gdy `MPLRTBE` jest jeszcze pustym repozytorium.**
> Backend MPLRT dopiero powstaje — taski `BE` i `DB` tworzymy planowo, a nie warunkowo.
> Nie pomijaj ich „bo backendu nie ma". Podobnie task `Figma` tworzymy planowo,
> mimo że plik makiety Figmy jeszcze nie powstał (do tego czasu ekrany specyfikuje dokumentacja interfejsów).
> W projekcie MPLRT brak dedykowanej iteracji E2e — task `E2e tests` trafia do iteracji PBI (Sprint 1).

### Kolejność wykonania dla PBI

```
0. Potwierdź Epic i Feature (zapytaj jeśli brakuje)
1. (opcjonalnie) Utwórz Epic        → zanotuj ID
2. (opcjonalnie) Utwórz Feature     → zanotuj ID
3. Utwórz PBI                       → zanotuj ID
4. Utwórz Task "FE"           (parent = PBI, sprint = Sprint 1)
5. Utwórz Task "BE"           (parent = PBI, sprint = Sprint 1)
6. Utwórz Task "DB"           (parent = PBI, sprint = Sprint 1)
7. Utwórz Task "Figma"        (parent = PBI, sprint = Sprint 1)
8. Utwórz Task "Manual tests" (parent = PBI, sprint = Sprint 1)
9. Utwórz Task "E2e tests"    (parent = PBI, sprint = Sprint 1)
```

---

## Źródło treści — dokumentacja produktowa MPLRT

Opisy PBI i Featurów **wyprowadzaj z dokumentacji produktowej**
(`d:\projects\DTCode\Dokumentacja\MPLRT`, po polsku), a nie z własnych domysłów.

Każdy dokument ma we front matter pole `status`. Traktuj je dosłownie:

| `status`         | Jak traktować                                                                        |
| ---------------- | ------------------------------------------------------------------------------------ |
| `zatwierdzony`   | **Wiążące** — to jest wymaganie, z tego piszesz opis i kryteria akceptacji            |
| `do-weryfikacji` | Propozycja czekająca na decyzję człowieka — **zapytaj użytkownika**, zanim ją utrwalisz |
| `szkic`          | Jeszcze nie wymaganie — nie twórz z niego PBI bez wyraźnej zgody                      |
| `wycofany`       | Historia — **nigdy** nie twórz z niego work itema ani nie cytuj go jako wymagania     |

Jeśli dokumentacja i polecenie użytkownika się rozjeżdżają, **zgłoś rozbieżność**
i zapytaj, która wersja obowiązuje. Nie „scalaj po cichu".

---

## Opis PBI — styl i treść

### Dla kogo jest opis

Opis w PBI jest przeznaczony **dla testera, który nie jest technicznym programistą**. Tester musi zrozumieć:

- Co nowa funkcjonalność robi z perspektywy użytkownika
- Jak ją przetestować ręcznie (co kliknąć, co powinno się stać)
- Czego oczekiwać (co jest wynikiem poprawnego działania)

> ⚠️ **Nigdy nie pisz opisu technicznego** — bez nazw klas, metod, endpointów API, nazw kolumn DB, nazw plików, architektury ani terminologii z kodu. Opis ma opisywać **zachowanie widoczne dla użytkownika**, nie implementację.

W MPLRT pamiętaj o dwóch kontekstach dostępu — to zmienia treść kroków testowych:

- **publiczny** (bez logowania: strona główna, aktualności, harmonogram, regulaminy i wyniki w formacie PDF, lista zawodników, sponsorzy, galeria, dojazd i noclegi, kontakt, regulamin zapisów i płatności, płatności i polityka prywatności; link do zewnętrznego systemu rejestracji i opłat — serwis sam nie przetwarza płatności),
- **panel redaktora** (jedno wspólne konto redaktora, bez ról i bez zarządzania użytkownikami — logowanie do panelu do publikowania i edycji treści, wgrywania PDF-ów oraz zdjęć do galerii; brak multi-tenancy).

Jeśli scenariusz dotyczy panelu, napisz wprost, że tester loguje się na wspólne konto redaktora.

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

| ❌ ZŁE (techniczne)                                                                        | ✅ DOBRE (dla testera)                                                                                                             |
| ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| „Dodano endpoint `POST /api/news` który zapisuje rekord w tabeli `News`"                    | „Redaktor w panelu wypełnia formularz aktualności, klika Publikuj i nowa wiadomość pojawia się na górze listy na stronie głównej" |
| „`UploadService` zapisuje plik PDF w katalogu `/documents` i zwraca guid do bazy"           | „Redaktor wgrywa plik PDF z regulaminem zawodów, a na stronie publicznej w sekcji Regulamin pojawia się aktywny link do pobrania" |
| „Komponent `FooterLinks` renderuje `routerLink` do `/regulamin`" | „Kliknięcie „Regulamin zapisów i płatności" w stopce otwiera stronę z pełną treścią regulaminu" |

---

## Screenshoty w opisie PBI — jak dodawać

### Źródło screenshotów: wyłącznie Figma

Screenshoty dołączane do opisu PBI **muszą pochodzić z Figmy** — nie z przeglądarki, nie z Playwright, nie z implementacji.

Powód: Figma zawiera zaakceptowane mockupy, które tester ma weryfikować. Screenshot z implementacji pokazuje „jak jest", a nie „jak powinno być".

> 🛈 **Warunek braku pliku Figmy:** W projekcie MPLRT plik makiety Figmy jeszcze nie powstał (kontrakt B: do czasu makiety ekrany opisuje wyłącznie `interfejsy/` w dokumentacji). Dopóki plik Figmy nie istnieje, opis PBI **zamiast screenshotów linkuje odpowiedni dokument z `Dokumentacja\MPLRT\interfejsy/`**. Gdy makieta w Figmie powstanie, screenshoty dodawaj ściśle według poniższej procedury.

### Procedura dodawania screenshotów

**Krok 1 — Pobierz screenshot z Figmy (gdy plik powstanie)**

Używając `get_screenshot` lub `use_figma` z Figma MCP pobierz PNG dla odpowiedniego node-id z pliku MPLRT (gdy zostanie utworzony).

```
get_screenshot(fileKey: "<fileKey>", nodeId: "<node-id>")
```

Wynik to plik PNG (binarny lub base64). Zapisz go lokalnie do pliku tymczasowego.

**Krok 2 — Wgraj PNG jako załącznik do ADO**

Użyj ADO REST API (nie MCP — MCP nie obsługuje uploadu binarnych plików). Endpoint przyjmuje
**nazwę projektu** zamiast GUID — działa tak samo:

```powershell
$PAT   = "<token>"
$B64   = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(":$PAT"))
$hdrs  = @{ Authorization = "Basic $B64"; "Content-Type" = "application/octet-stream" }
$bytes = [IO.File]::ReadAllBytes("C:\tmp\screen.png")
$resp  = Invoke-WebRequest `
  -Uri "https://dev.azure.com/DTCode/MPLRT/_apis/wit/attachments?fileName=screen.png&api-version=7.1" `
  -Method Post -Headers $hdrs -Body $bytes -UseBasicParsing
$url = ($resp.Content | ConvertFrom-Json).url
```

`$url` to czysty URL załącznika — np. `https://dev.azure.com/DTCode/MPLRT/_apis/wit/attachments/{guid}?fileName=screen.png`.

> 🔑 PAT znajdziesz w pliku konfiguracyjnym MCP (`~/.claude.json` pod kluczem `mcpServers.azure-devops.env.PERSONAL_ACCESS_TOKEN`).
>
> ⚠️ Jeśli upload lub wywołanie MCP kończy się `203` (zwrócona strona logowania) albo `401`, **nie kombinuj z innymi tokenami** — to znaczy, że PAT wygasł; zgłoś użytkownikowi konieczność odnowienia.
> Nigdy nie wypisuj wartości tokenu w odpowiedzi ani w logach.

**Krok 3 — Wstaw URL do opisu (czysty, bez enkodowania)**

W HTML opisu używaj bezpośrednio zwróconego URL-a w atrybucie `src`. **Nigdy nie owijaj go cudzysłowami wewnątrz łańcucha ani nie URL-enkoduj:**

```html
<!-- ✅ POPRAWNIE -->
<img
  src="https://dev.azure.com/DTCode/MPLRT/_apis/wit/attachments/abc-123?fileName=screen.png"
  style="max-width:100%;border:1px solid #e2e8f0;border-radius:8px;margin:12px 0;display:block;"
/>

<!-- ❌ ŹLE — podwójne enkodowanie, cudzysłowy w URL -->
<img src="%22https%3a//dev.azure.com/...%22" />
```

**Krok 4 — Dodaj opis z obrazkami przez `wit_update_work_item`**

Przekaż HTML z czystymi URL-ami (Wzorzec 3). Sprawdź wynik — jeśli obrazki nie są widoczne, to URL jest nieprawidłowy.

### Kiedy dodawać screenshoty

- **Dopóki plik Figmy nie istnieje:** Opis PBI linkuje dokument specyfikacji z `Dokumentacja\MPLRT\interfejsy/`.
- **Gdy plik Figmy powstanie:** Zawsze, gdy istnieją odpowiednie node-idy w Figmie dla danej funkcjonalności.
- Minimum jeden screenshot na PBI (chyba że funkcjonalność jest czysto backendowa i nie ma UI).
- Preferowane: oddzielny screenshot dla widoku **telefon (mobile)**, **HD** i **Full HD** (zgodnie z ekranami odniesienia MPLRT).
- **Light i Dark:** w MPLRT oba motywy są obowiązkowe na całej stronie, panel redaktora włącznie (`DEC-MOTYW-JASNY-I-CIEMNY`). Jeśli mockup istnieje w obu wariantach — dołącz oba i podpisz je („Light” / „Dark”), żeby tester wiedział, że ma sprawdzić oba.

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

- Jeśli makieta w Figmie istnieje i użytkownik poda link do Figmy lub konkretnego mockupu, **dołącz go do opisu** odpowiedniego elementu (PBI, Bug lub task `Figma`).
- Do czasu powstania pliku Figmy, linkuj bezpośrednio dokument specyfikacji ekranu:
  ```
  📄 Specyfikacja ekranu: [Nazwa ekranu / sekcji](Dokumentacja/MPLRT/interfejsy/...)
  ```
- Gdy plik Figmy powstanie, linki wstawiaj w formacie:
  ```
  🎨 Mockup: [Nazwa ekranu / sekcji](https://figma.com/...)
  ```
- Jeśli do jednego zadania pasuje kilka mockupów lub dokumentów, dołącz wszystkie z krótkim opisem czego dotyczą.

---

## Instrukcja MCP — Jak wywoływać narzędzia (wzorce z praktyki)

> Sekcja opisuje **konkretne wywołania MCP** sprawdzone w praktyce. Skup się na niej zanim zaczniesz tworzyć elementy.

### Narzędzia i kiedy ich używać

| Narzędzie                    | Do czego                                                                                     | Uwagi                                                                                                             |
| ---------------------------- | -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `wit_create_work_item`       | Tworzenie Feature / PBI / Bug (tytuł + pola podstawowe)                                       | **Nigdy nie przekazuj opisu tu — zrób to osobno przez update**                                                     |
| `wit_add_child_work_items`   | Tworzenie 6 tasków pod jednym PBI — tworzy I linkuje w jednym wywołaniu                        | ⚠️ **NIE obsługuje `assignedTo` per item** — po wywołaniu ZAWSZE wykonaj batch update assignee (patrz Wzorzec 5)   |
| `wit_work_items_link`        | Przypięcie rodzica (Epic→Feature, Feature→PBI)                                                 | Działa batchowo — do 6+ linków naraz                                                                               |
| `wit_update_work_item`       | Dodanie opisu HTML i kryteriów akceptacji do PBI                                               | Osobne wywołanie po utworzeniu                                                                                     |
| `wit_update_work_items_batch` | Masowa aktualizacja pól wielu elementów naraz — używane do ustawienia assignee na taskach      | Wymaga niepustej tablicy `updates`                                                                                 |

---

### Wzorzec 1 — Tworzenie Feature / PBI / Task

Wywołaj `wit_create_work_item` z wypełnioną tablicą `fields`. **Tablica nigdy nie może być pusta** — minimum to `System.Title`.

```
wit_create_work_item(
  project: "MPLRT",
  workItemType: "Feature",          // lub "Product Backlog Item" / "Task" / "Bug"
  fields: [
    { name: "System.Title",         value: "Publikacja regulaminu zawodów" },
    { name: "System.AssignedTo",    value: "kontakt@DTCode.pl" },
    { name: "System.IterationPath", value: "MPLRT\\Sprint 1" }
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
  project: "MPLRT",
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
- `&` w URL-ach zamieniaj na `&amp;`
- Polskie znaki (ą, ę, ó, ź itd.) działają bezpośrednio w `value`
- Nie używaj `<h1>`, `<h2>` — ADO renderuje je zbyt duże; `<h3>` jest odpowiednie dla sekcji

---

### Wzorzec 4 — Optymalny przepływ dla wielu PBI naraz

Gdy tworzysz np. 6 PBI pod jednym Feature, nie twórz → linkuj → opisuj → twórz taski każdego osobno. Zrób to w 5 etapach:

```
ETAP 1 — Utwórz wszystkie PBI (sam tytuł + podstawowe pola)
  wit_create_work_item(PBI #1) → ID: 331
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
  ...
  wit_update_work_item(336, description + AC)

ETAP 4 — Utwórz 6 tasków pod każdym PBI (wit_add_child_work_items)
  wit_add_child_work_items(parentId: 331, items: [FE, BE, DB, Figma, Manual tests, E2e tests])
  ...
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
// W MPLRT brak osobnej iteracji E2e — wszystkie taski, w tym E2e tests, trafiają do sprintu PBI (Sprint 1)
wit_add_child_work_items(
  parentId: <pbiId>,
  workItemType: "Task",
  project: "MPLRT",
  items: [
    { title: "FE",           iterationPath: "MPLRT\\Sprint 1", description: "" },
    { title: "BE",           iterationPath: "MPLRT\\Sprint 1", description: "" },
    { title: "DB",           iterationPath: "MPLRT\\Sprint 1", description: "" },
    { title: "Figma",        iterationPath: "MPLRT\\Sprint 1", description: "" },
    { title: "Manual tests", iterationPath: "MPLRT\\Sprint 1", description: "" },
    { title: "E2e tests",    iterationPath: "MPLRT\\Sprint 1", description: "" }
  ]
)
→ Odpowiedź zwraca IDs w tej samej kolejności: [FE_id, BE_id, DB_id, Figma_id, Manual_id, E2e_id]
```

```
// KROK B — Ustaw assignee w batch (kontakt dla FE/BE/DB, Piotr dla Figma/Manual/E2e)
wit_update_work_items_batch(updates: [
  { id: <FE_331>, path: "/fields/System.AssignedTo", value: "kontakt@DTCode.pl" },
  { id: <BE_331>, path: "/fields/System.AssignedTo", value: "kontakt@DTCode.pl" },
  { id: <DB_331>, path: "/fields/System.AssignedTo", value: "kontakt@DTCode.pl" },
  { id: <Figma_331>,  path: "/fields/System.AssignedTo", value: "Piotr.Tunski@DTCode.pl" },
  { id: <Manual_331>, path: "/fields/System.AssignedTo", value: "Piotr.Tunski@DTCode.pl" },
  { id: <E2e_331>,    path: "/fields/System.AssignedTo", value: "Piotr.Tunski@DTCode.pl" }
  ... (analogicznie dla pozostałych PBI)
])
```

> ⚠️ Można zrobić wszystkie przypisania w jednym wywołaniu batch (dla 6 PBI = 36 wpisów).

---

### Definicja ukończenia (Definition of Done) dla PBI

Przed zakończeniem sprawdź, że każde PBI ma wszystkie poniższe elementy. **Brak któregokolwiek = praca niekompletna.**

| Element                                                  | Pole/narzędzie                                       |
| -------------------------------------------------------- | ---------------------------------------------------- |
| ✅ Tytuł                                                  | `System.Title`                                       |
| ✅ Przypisany do: kontakt@DTCode.pl                       | `System.AssignedTo`                                  |
| ✅ Sprint 1 (`MPLRT\Sprint 1`)                            | `System.IterationPath`                               |
| ✅ Rodzic (Feature)                                       | `wit_work_items_link`                                |
| ✅ Opis HTML (User Story + szczegóły + link do interfejsu / Figmy) | `System.Description` via `wit_update_work_item`      |
| ✅ Kryteria akceptacji HTML                               | `AcceptanceCriteria` via `wit_update_work_item`      |
| ✅ 6 tasków: FE, BE, DB, Figma, Manual tests, E2e tests   | `wit_add_child_work_items`                           |
| ✅ FE/BE/DB → kontakt@DTCode.pl, Sprint 1                 | `wit_update_work_items_batch`                        |
| ✅ Figma/Manual → Piotr.Tunski@DTCode.pl, Sprint 1        | `wit_update_work_items_batch`                        |
| ✅ E2e tests → Piotr.Tunski@DTCode.pl, Sprint 1          | `wit_update_work_items_batch`                        |

---

### Częste błędy i jak ich uniknąć

| Błąd                                              | Przyczyna                                                 | Rozwiązanie                                                                                          |
| ------------------------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `Cannot convert undefined or null to object`      | Przekazano pustą tablicę `[]` do `fields` lub `items`      | Zawsze podaj co najmniej `System.Title` w tablicy                                                     |
| Opis nie pojawia się w ADO                        | Próba dodania `System.Description` w `wit_create_work_item` | Twórz najpierw bez opisu, potem `wit_update_work_item`                                                |
| HTML renderuje się jako plain text                | Brak `format: "Html"` przy update                          | Dodaj `format: "Html"` do każdego obiektu w `updates`                                                 |
| Link rodzic-dziecko nie działa                    | Użyto złego `type`                                         | Dla hierarchii zawsze `type: "parent"` (nie `"child"`)                                                |
| `&` w URL uszkadza HTML                           | Dosłowny `&` w atrybucie href                              | Zamień na `&amp;` w wartości pola HTML                                                                |
| FE/BE/DB bez assignee po `wit_add_child_work_items` | Narzędzie nie obsługuje `assignedTo` per item             | Po każdym wywołaniu obowiązkowo `wit_update_work_items_batch` dla FE/BE/DB → kontakt@DTCode.pl        |
| PBI bez tasków po zakończeniu bulk-flow           | Bot zatrzymał się na opisach, nie wykonał Etapów 4-5       | Wzorzec 4 ma 5 etapów — Etapy 4 i 5 (taski + assignee) są obowiązkowe, nie opcjonalne                 |
| Błąd przy `System.IterationPath`                  | Nazwa iteracji inna niż przyjęta w tym skillu              | Wylistuj realne iteracje projektu i **zapytaj użytkownika** — nie zgaduj wariantów (patrz „Weryfikacja stałych") |
| ADO zwraca `203` / stronę logowania               | PAT wygasł                                                 | Zgłoś użytkownikowi konieczność odnowienia tokenu; nie próbuj obejść                                  |
