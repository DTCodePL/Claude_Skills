---
name: azure-devops-zebrani
description: >
  Zasady tworzenia tasków w Azure DevOps dla projektu Zebrani.pl.
  Obsługuje dwa tryby: Bug (z sub-taskami Fix i Retest) oraz PBI
  (z pełnym zestawem tasków FE/BE/DB/Figma/Manual tests/E2e tests).
  Wymusza weryfikację hierarchii Epic→Feature przed utworzeniem PBI,
  pilnuje przypisań i sprintów, treści pisze po polsku, czerpie opisy
  z zatwierdzonej dokumentacji produktowej i linkuje do Figmy.
  UŻYWAJ ZAWSZE, gdy user prosi o utworzenie buga, PBI, featura, epica
  lub tasków w Azure DevOps dla Zebrani.pl.
user-invocable: true
version: loader
language: pl
project: Zebrani.pl
organization: DTCode
mode: remote-loader
remote:
  github_raw: 'https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/Azure%20DevOps%20%E2%80%93%20Zebrani%20Task%20Creation%20Skill/SKILL.md'
  github_page: 'https://github.com/DTCodePL/Claude_Skills/blob/main/Azure%20DevOps%20%E2%80%93%20Zebrani%20Task%20Creation%20Skill/SKILL.md'
---

# Azure DevOps – Zebrani.pl (loader)

Ten plik jest **cienkim loaderem**. Nie zawiera logiki zadań — pełna, zawsze
aktualna i **wersjonowana** wersja zasad jest trzymana na GitHubie i to ona jest
źródłem prawdy.

## Krok obowiązkowy — pobierz i zastosuj wersję z GitHuba

Zanim wykonasz jakiekolwiek zadanie związane z tworzeniem Bug / PBI / Feature /
Epic / tasków w projekcie Zebrani.pl:

**1. Pobierz pełny skill przez bash_tool:**

```bash
curl -sL "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/Azure%20DevOps%20%E2%80%93%20Zebrani%20Task%20Creation%20Skill/SKILL.md" \
  -o /tmp/zebrani_ado_skill.md
cat /tmp/zebrani_ado_skill.md
```

**2. Wykonaj zadanie ściśle według pobranej treści** — to ona zawiera aktualne:

- stałe projektu (organizacja `DTCode`, projekt `Zebrani.pl`, team, iteracje, przypisania),
- tryby Bug (Fix + Retest) i PBI (pełne 6 tasków: FE / BE / DB / Figma / Manual tests / E2e tests),
- wzorce wywołań MCP `azure-devops` (tworzenie, linkowanie, opisy HTML, batch assignee),
- zasady czerpania treści z dokumentacji produktowej wg pola `status`,
- procedurę dołączania screenshotów z Figmy (Light i Dark) jako załączników ADO,
- Definition of Done i tabelę częstych błędów.

**3. Obsługa błędu pobierania** — jeśli `curl` zwróci 404, nie ma sieci albo plik
jest pusty/niepoprawny:

- poinformuj użytkownika, że nie udało się pobrać aktualnej wersji z GitHuba,
- **zatrzymaj się i zapytaj, czy kontynuować** — nie zgaduj zasad, iteracji ani
  przypisań z pamięci.

> ⚠️ Nie utrzymuj logiki zadań w tym pliku i nie próbuj go „aktualizować"
> lokalnie. Wszystkie zmiany w zasadach rób w repozytorium na GitHubie —
> loader zawsze pobierze najnowszą wersję.
