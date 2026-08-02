---
name: fix-devops-bug-zebrani
description: >
  Naprawianie buga w projekcie Zebrani.pl na podstawie linku lub numeru Azure DevOps.
  Użyj, gdy użytkownik poda link do work itema (np.
  https://dev.azure.com/DTCode/Zebrani.pl/_workitems/edit/123) albo sam numer i poprosi
  o analizę/naprawę zgłoszenia. Skill pobiera work item i jego sub-taski (Fix/Retest),
  weryfikuje czy błąd występuje w kodzie, odtwarza buga w działającej aplikacji przez
  Playwright na macierzy 2×2 (mobile 360×530 i desktop 1280×720, każdy w Light i Dark)
  — test BEFORE, implementuje poprawkę zgodnie z CLAUDE.md, potwierdza Playwrightem
  że bug zniknął (test AFTER), uruchamia lint:fix + format, commituje i pushuje,
  proponuje ręczne uruchomienie deployu pre-prod, a następnie aktualizuje statusy
  w DevOps (Fix → Done, Bug → Ready for tests) i przypisuje buga do testera.
user-invocable: true
version: loader
language: pl
project: Zebrani.pl
organization: DTCode
mode: remote-loader
remote:
  github_raw: 'https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/Fix%20DevOps%20Bug%20%E2%80%93%20Zebrani/SKILL.md'
  github_page: 'https://github.com/DTCodePL/Claude_Skills/blob/main/Fix%20DevOps%20Bug%20%E2%80%93%20Zebrani/SKILL.md'
---

# Fix DevOps Bug – Zebrani.pl (loader)

Ten plik jest **cienkim loaderem**. Nie zawiera logiki zadań — pełna, zawsze
aktualna i **wersjonowana** procedura (pobranie work itema, testy Playwright
before/after, naprawa, lint/format, commit/push, ręczny deploy pre-prod,
aktualizacja statusów) jest trzymana na GitHubie i to ona jest źródłem prawdy.

## Krok obowiązkowy — pobierz i zastosuj wersję z GitHuba

Zanim ruszysz naprawę jakiegokolwiek buga z Azure DevOps w projekcie Zebrani.pl:

**1. Pobierz pełny skill przez bash_tool:**

```bash
curl -sL "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/Fix%20DevOps%20Bug%20%E2%80%93%20Zebrani/SKILL.md" \
  -o /tmp/fix_devops_bug_zebrani_skill.md
cat /tmp/fix_devops_bug_zebrani_skill.md
```

**2. Wykonaj zadanie ściśle według pobranej treści** — to ona zawiera aktualną
procedurę krok po kroku:

- identyfikacja work itema i sub-tasków Fix/Retest, weryfikacja buga w kodzie,
- **macierz testowa 2×2** — mobile `360×530` i desktop `1280×720`, każdy w Light
  i Dark (przełączanie motywu przez `ThemeMode` / klasę `.app-dark`),
- naprawa wg `.claude/CLAUDE.md` (tokeny kolorów, i18n `pl` + `en`, brak
  `@deprecated`, brak `::ng-deep`, WCAG AA),
- `lint:fix` + `format`, commit `fix(<scope>): #<idBuga> …`, push po zgodzie,
- **ręczny deploy pre-prod** (`deploy-preprod.yml`, `workflow_dispatch`) — skill
  pyta, czy go odpalić, i odczytuje numer runa po `headSha`,
- statusy DevOps: Fix → Done, Bug → Ready for tests + przypisanie testerowi,
  oraz nietechniczny komentarz z instrukcją retestu.

**3. Obsługa błędu pobierania** — jeśli `curl` zwróci 404, nie ma sieci albo plik
jest pusty/niepoprawny:

- poinformuj użytkownika, że nie udało się pobrać aktualnej wersji z GitHuba,
- **zatrzymaj się i zapytaj, czy kontynuować** — nie zgaduj procedury z pamięci.

> ⚠️ Nie utrzymuj logiki zadań w tym pliku i nie próbuj go „aktualizować"
> lokalnie. Wszystkie zmiany w procedurze rób w repozytorium na GitHubie —
> loader zawsze pobierze najnowszą wersję.
