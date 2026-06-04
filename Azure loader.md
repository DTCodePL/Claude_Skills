---
name: azure-devops-tachoping
description: >
  Zasady tworzenia tasków w Azure DevOps dla projektu TachoPing.
  Obsługuje dwa tryby: Bug (z sub-taskami Fix i Retest) oraz PBI
  (z pełnym zestawem tasków FE/BE/DB/Figma/Manual tests/E2e tests).
  Wymusza weryfikację hierarchii Epic→Feature przed utworzeniem PBI,
  pilnuje przypisań i sprintów, treści pisze po polsku, linkuje do Figmy.
language: pl
project: TachoPing
organization: dtcode
mode: remote-loader
remote:
  github_raw: "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/Azure%20DevOps%20%E2%80%93%20TachoPing%20Task%20Creation%20Skill/SKILL.md"
  github_page: "https://github.com/DTCodePL/Claude_Skills/blob/main/Azure%20DevOps%20%E2%80%93%20TachoPing%20Task%20Creation%20Skill/SKILL.md"
---

# Azure DevOps – TachoPing (loader)

Ten plik jest **cienkim loaderem**. Nie zawiera logiki zadań — pełna i zawsze
aktualna wersja zasad jest trzymana na GitHubie i to ona jest źródłem prawdy.

## Krok obowiązkowy — pobierz i zastosuj wersję z GitHuba

Zanim wykonasz jakiekolwiek zadanie związane z tworzeniem Bug / PBI / tasków
w projekcie TachoPing:

**1. Pobierz pełny skill przez bash_tool:**
```bash
curl -sL "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/Azure%20DevOps%20%E2%80%93%20TachoPing%20Task%20Creation%20Skill/SKILL.md" -o /tmp/tachoping_skill.md
cat /tmp/tachoping_skill.md
```

**2. Wykonaj zadanie ściśle według pobranej treści** — to ona zawiera aktualne
tryby (Bug / PBI), wzorce tworzenia work itemów, przypisania, sprinty i zasady
linkowania do Figmy.

**3. Obsługa błędu pobierania** — jeśli `curl` zwróci 404, nie ma sieci albo plik
jest pusty/niepoprawny:
- poinformuj użytkownika, że nie udało się pobrać aktualnej wersji z GitHuba,
- **zatrzymaj się i zapytaj, czy kontynuować** — nie zgaduj zasad z pamięci.

> ⚠️ Nie utrzymuj logiki zadań w tym pliku i nie próbuj go „aktualizować"
> lokalnie. Wszystkie zmiany w zasadach rób w repozytorium na GitHubie —
> loader zawsze pobierze najnowszą wersję.
