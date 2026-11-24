---
name: fix-devops-bug-mplrt
description: >
  Naprawianie buga w projekcie MPLRT na podstawie linku lub numeru Azure DevOps.
  Użyj, gdy użytkownik poda link do work itema (np.
  https://dev.azure.com/DTCode/MPLRT/_workitems/edit/123) albo sam numer i poprosi
  o analizę/naprawę zgłoszenia. Skill pobiera work item i jego sub-taski (Fix/Retest),
  weryfikuje czy błąd występuje w kodzie, odtwarza buga w działającej aplikacji przez
  Playwright na macierzy ekranów odniesienia (telefon 360×560, HD 1280×720, Full HD 1920×1080, każdy w motywie jasnym i ciemnym)
  — test BEFORE, implementuje poprawkę zgodnie z CLAUDE.md, potwierdza Playwrightem
  że bug zniknął (test AFTER), uruchamia lint:fix + format, commituje i pushuje,
  zgłasza kwestię deployu pre-prod, a następnie aktualizuje statusy
  w DevOps (Fix → Done, Bug → Ready for tests) i przypisuje buga do testera.
user-invocable: true
version: loader
language: pl
project: MPLRT
organization: DTCode
mode: remote-loader
remote:
  github_raw: 'https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/Fix%20DevOps%20Bug%20%E2%80%93%20MPLRT/SKILL.md'
  github_page: 'https://github.com/DTCodePL/Claude_Skills/blob/main/Fix%20DevOps%20Bug%20%E2%80%93%20MPLRT/SKILL.md'
---

# Fix DevOps Bug – MPLRT (loader)

Ten plik jest **cienkim loaderem**. Nie zawiera logiki zadań — pełna, zawsze
aktualna i **wersjonowana** procedura (pobranie work itema, testy Playwright
before/after, naprawa, lint/format, commit/push, obsługa deployu pre-prod,
aktualizacja statusów) jest trzymana na GitHubie i to ona jest źródłem prawdy.

## Krok obowiązkowy — pobierz i zastosuj wersję z GitHuba

Zanim ruszysz naprawę jakiegokolwiek buga z Azure DevOps w projekcie MPLRT:

**1. Pobierz pełny skill przez bash_tool:**

```bash
curl -sL "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/Fix%20DevOps%20Bug%20%E2%80%93%20MPLRT/SKILL.md" \
  -o /tmp/fix_devops_bug_mplrt_skill.md
cat /tmp/fix_devops_bug_mplrt_skill.md
```

**2. Wykonaj zadanie ściśle według pobranej treści** — to ona zawiera aktualną
procedurę krok po kroku:

- identyfikacja work itema i sub-tasków Fix/Retest, weryfikacja buga w kodzie,
- **macierz testowa 3×2 (6 kombinacji)** — ekrany odniesienia (telefon 360×560; HD 1280×720; Full HD 1920×1080), każdy w Light i Dark (przełączanie motywu przez `ThemeMode` / klasę `.app-dark`),
- naprawa wg `.claude/CLAUDE.md` (tokeny kolorów, i18n wyłącznie `pl`, brak
  `@deprecated`, brak `::ng-deep`, WCAG AA),
- `lint:fix` + `format`, commit `fix(<scope>): #<idBuga> …`, push po zgodzie,
- **deploy pre-prod** — środowisko nie istnieje; krok pomijany i zgłaszany użytkownikowi, dopóki sekcja „Environments” w `AGENTS.md` repo nie poda serwera i workflow,
- statusy DevOps: Fix → Done, Bug → Ready for tests + przypisanie testerowi,
  oraz nietechniczny komentarz z instrukcją retestu.

**3. Obsługa błędu pobierania** — jeśli `curl` zwróci 404, nie ma sieci albo plik
jest pusty/niepoprawny:

- poinformuj użytkownika, że nie udało się pobrać aktualnej wersji z GitHuba,
- **zatrzymaj się i zapytaj, czy kontynuować** — nie zgaduj procedury z pamięci.

> ⚠️ Nie utrzymuj logiki zadań w tym pliku i nie próbuj go „aktualizować"
> lokalnie. Wszystkie zmiany w procedurze rób w repozytorium na GitHubie —
> loader zawsze pobierze najnowszą wersję.
