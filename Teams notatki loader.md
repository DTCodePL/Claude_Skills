---
name: teams-notatki
description: >
  Tworzy notatki po polsku ze spotkań Microsoft Teams na podstawie transkrypcji,
  przez mostek HTTPS teamsnotes.tojest.dev (Damian/Piotr, DTCode).
  Wyzwalacze: „notatki ze spotkania”, „transkrypcja Teams”, link
  teams.microsoft.com/meet/... albo .../l/meetup-join/..., „spotkanie w piątek /
  wczoraj / o 10”, „podsumuj spotkanie”, „co ustaliliśmy na spotkaniu”.
  UŻYWAJ ZAWSZE, gdy user chce notatkę, podsumowanie lub listę zadań ze
  spotkania Microsoft Teams — nawet jeśli nie padnie słowo skill.
user-invocable: true
version: loader
language: pl
organization: DTCode
mode: remote-loader
remote:
  github_raw: 'https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/teams-notatki/SKILL.md'
  github_page: 'https://github.com/DTCodePL/Claude_Skills/blob/main/teams-notatki/SKILL.md'
---

# Teams — notatki ze spotkania (loader)

Ten plik jest **cienkim loaderem**. Nie zawiera logiki zadania — pełna, zawsze
aktualna i **wersjonowana** wersja skilla (razem z CLI `scripts/bridge.py` i
szablonem notatki) jest trzymana na GitHubie i to ona jest źródłem prawdy.

## Krok obowiązkowy — pobierz i zastosuj wersję z GitHuba

Zanim zrobisz notatkę, podsumowanie albo listę zadań ze spotkania Microsoft
Teams:

**1. Pobierz pełny skill przez bash_tool (albo PowerShell — patrz niżej):**

```bash
curl -sL "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/teams-notatki/SKILL.md" \
  -o /tmp/teams_notatki_skill.md
cat /tmp/teams_notatki_skill.md
```

PowerShell:

```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/teams-notatki/SKILL.md" `
  -OutFile "$env:TEMP\teams_notatki_skill.md"
Get-Content "$env:TEMP\teams_notatki_skill.md"
```

**2. Wykonaj zadanie ściśle według pobranej treści** — to ona zawiera
aktualne:

- adres mostka i sposób konfiguracji (`TEAMS_NOTATKI_URL` / `TEAMS_NOTATKI_TOKEN`,
  oba opcjonalne — CLI działa bez żadnego ustawiania),
- pełny przebieg: sprawdzenie mostka → identyfikacja spotkania → wybór
  kandydata → pobranie transkrypcji → notatka → wynik,
- listę dodatkowych plików do pobrania (`scripts/bridge.py`,
  `references/szablon-notatki.md`, `references/api.md`) i komendy `curl` /
  `Invoke-WebRequest`, którymi je ściągnąć,
- tryb awaryjny bez mostka (`parse-vtt` na pliku `.vtt` pobranym ręcznie z
  Teams) i tabelę częstych błędów.

**3. Obsługa błędu pobierania** — jeśli `curl`/`Invoke-WebRequest` zwróci 404,
nie ma sieci albo plik jest pusty/niepoprawny:

- poinformuj użytkownika, że nie udało się pobrać aktualnej wersji z GitHuba,
- **zatrzymaj się i zapytaj, czy kontynuować** — nie zgaduj adresu mostka,
  przebiegu ani formatu notatki z pamięci.

> ⚠️ Nie utrzymuj logiki zadania w tym pliku i nie próbuj go „aktualizować”
> lokalnie. Wszystkie zmiany w skillu robi się w repozytorium na GitHubie —
> loader zawsze pobierze najnowszą wersję.
