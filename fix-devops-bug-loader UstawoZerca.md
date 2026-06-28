---
name: fix-devops-bug-ustawozerca
description: >
  Naprawianie buga w projekcie UstawoŻerca na podstawie linku lub numeru Azure DevOps.
  Użyj, gdy użytkownik poda link do work itema (np.
  https://dev.azure.com/DTCode/Ustawo%C5%BBerca/_workitems/edit/123) albo sam numer i poprosi
  o analizę/naprawę zgłoszenia. Skill pobiera work item i jego sub-taski (Fix/Retest),
  weryfikuje czy błąd występuje w kodzie, odtwarza buga w działającej aplikacji przez
  Playwright (test BEFORE), implementuje poprawkę zgodnie z CLAUDE.md, potwierdza
  Playwrightem że bug zniknął (test AFTER), uruchamia lint:fix + format, commituje
  i pushuje na main, a następnie aktualizuje statusy w DevOps (Fix → Done,
  Bug → Ready for tests) i przypisuje buga do testera.
language: pl
project: UstawoŻerca
organization: DTCode
mode: remote-loader
remote:
  github_raw: 'https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/Fix%20DevOps%20Bug%20%E2%80%93%20UstawoZerca/SKILL.md'
  github_page: 'https://github.com/DTCodePL/Claude_Skills/blob/main/Fix%20DevOps%20Bug%20%E2%80%93%20UstawoZerca/SKILL.md'
---

# Fix DevOps Bug – UstawoŻerca (loader)

Ten plik jest **cienkim loaderem**. Nie zawiera logiki zadań – pełna i zawsze
aktualna wersja procedury (pobranie work itema, testy Playwright before/after,
naprawa, lint/format, commit/push na main, aktualizacja statusów) jest trzymana
na GitHubie i to ona jest źródłem prawdy.

## Krok obowiązkowy – pobierz i zastosuj wersję z GitHuba

Zanim ruszysz naprawę jakiegokolwiek buga z Azure DevOps w projekcie UstawoŻerca:

**1. Pobierz pełny skill przez bash_tool:**

```bash
curl -sL "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/Fix%20DevOps%20Bug%20%E2%80%93%20UstawoZerca/SKILL.md" -o /tmp/fix_devops_bug_ustawozerca_skill.md
cat /tmp/fix_devops_bug_ustawozerca_skill.md
```

**2. Wykonaj zadanie ściśle według pobranej treści** – to ona zawiera aktualną
procedurę krok po kroku (identyfikacja work itema i sub-tasków Fix/Retest,
weryfikacja buga w kodzie, test Playwright BEFORE, naprawa wg CLAUDE.md, test
Playwright AFTER, `lint:fix` + `format`, commit/push na `main`, statusy DevOps:
Fix → Done, Bug → Ready for tests + przypisanie testerowi) oraz wzorce asercji
Playwright.

**3. Obsługa błędu pobierania** – jeśli `curl` zwróci 404, nie ma sieci albo plik
jest pusty/niepoprawny:

- poinformuj użytkownika, że nie udało się pobrać aktualnej wersji z GitHuba,
- **zatrzymaj się i zapytaj, czy kontynuować** – nie zgaduj procedury z pamięci.

> ⚠️ Nie utrzymuj logiki zadań w tym pliku i nie próbuj go „aktualizować"
> lokalnie. Wszystkie zmiany w procedurze rób w repozytorium na GitHubie –
> loader zawsze pobierze najnowszą wersję.
