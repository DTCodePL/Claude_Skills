---
name: tachoping-design
description: Use this skill to generate well-branded interfaces and assets for TachoPing, either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping. TachoPing is a tachograph-deadline reminder service for small road-transport fleets (Polish, non-technical audience).
user-invocable: true
version: loader
mode: remote-loader
remote:
  github_raw: "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/TachoPing%20%E2%80%94%20Design%20System/SKILL.md"
  github_page: "https://github.com/DTCodePL/Claude_Skills/blob/main/TachoPing%20%E2%80%94%20Design%20System/SKILL.md"
---

# TachoPing — Design System (loader)

Ten plik jest **cienkim loaderem**. Nie zawiera definicji systemu projektowego —
pełna i zawsze aktualna wersja jest trzymana na GitHubie i to ona jest źródłem prawdy.

## Krok obowiązkowy — pobierz i zastosuj wersję z GitHuba

Zanim zaczniesz projektować jakikolwiek ekran, komponent, makietę lub asset
dla TachoPing:

**1. Pobierz pełny skill przez bash_tool:**
```bash
curl -sL "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/TachoPing%20%E2%80%94%20Design%20System/SKILL.md" \
  -o /tmp/tachoping_design_skill.md
cat /tmp/tachoping_design_skill.md
```

**2. Zastosuj pobraną treść ściśle** — to ona zawiera aktualne:
- kolory, tokeny CSS, typografię (Inter / DM Mono),
- wzorce komponentów (karty, przyciski, inputy, badge'e, tabele),
- UI Kit Kierowcy (dark PWA), Właściciela (dashboard) i Publiczny (marketing/auth),
- zasady animacji, ikon (FontAwesome 7.x) i szablony HTML/React.

**3. Obsługa błędu pobierania** — jeśli `curl` zwróci błąd, plik jest pusty
lub niedostępny:
- poinformuj użytkownika, że nie udało się pobrać aktualnej wersji z GitHuba,
- **zatrzymaj się i zapytaj, czy kontynuować** — nie zgaduj wartości designu z pamięci.

> ⚠️ Nie utrzymuj definicji designu w tym pliku i nie próbuj go „aktualizować"
> lokalnie. Wszystkie zmiany w systemie projektowym rób w repozytorium na GitHubie —
> loader zawsze pobierze najnowszą wersję.
