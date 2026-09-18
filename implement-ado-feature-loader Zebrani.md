---
name: implement-ado-feature-zebrani
description: >
  Planowanie i pełna implementacja feature'a / PBI / taska Zebrani.pl na
  podstawie linku lub numeru Azure DevOps — od Plan Mode (z makietami Figmy
  linkowanymi wprost, nie opisywanymi), przez wykonanie w modelu: sesja
  główna Opus max = architekt, dyspozytor i walidator etapów (nigdy
  wykonawca) / linie wykonawcze rozdzielone proporcjonalnie do pul (Sonnet
  domyślnie, Spark i Terra jako sloty, Luna lekkie) / niezależny recenzent
  Codex, przez zlecony audyt SCSS pod kątem Bootstrapa i deduplikacji, aż po
  bramę mojego potwierdzenia i dopiero wtedy domknięcie w ADO (commit/push,
  statusy tasków deweloperskich, PBI → Ready for tests, przypisanie do
  testera). Na starcie, tuż po zatwierdzeniu planu, PBI/Bug i taski
  przewidziane do wykonania idą na In Progress. Obejmuje też naprawę Bugów —
  wtedy obowiązuje zasada test-first: najpierw czerwony test dowodzący błędu,
  potem łatka, ten sam test bez zmian zielony. UŻYWAJ ZAWSZE, gdy user poda
  link lub numer Epic/Feature/PBI/Task/Bug
  z Azure DevOps projektu Zebrani.pl i poprosi o zaplanowanie, zaimplementowanie
  i/lub naprawienie go — nawet jeśli nie padnie słowo "skill".
user-invocable: true
version: loader
language: pl
project: Zebrani.pl
organization: DTCode
mode: remote-loader
remote:
  github_raw: 'https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/Implement%20ADO%20Feature%20%E2%80%93%20Zebrani/SKILL.md'
  github_page: 'https://github.com/DTCodePL/Claude_Skills/blob/main/Implement%20ADO%20Feature%20%E2%80%93%20Zebrani/SKILL.md'
---

# Implement ADO Feature – Zebrani.pl (loader)

Ten plik jest **cienkim loaderem**. Nie zawiera logiki zadań — pełna, zawsze
aktualna i **wersjonowana** procedura (plan w Plan Mode, otwarcie w ADO,
rozdział briefów na linie wykonawcze, walidacja etapów, audyt SCSS, recenzja
Codex, brama potwierdzenia, domknięcie w ADO) jest trzymana na GitHubie i to
ona jest źródłem prawdy.

## Krok obowiązkowy — pobierz i zastosuj wersję z GitHuba

Zanim zaplanujesz lub zaczniesz implementować jakikolwiek Epic / Feature /
PBI / Task / Bug z Azure DevOps w projekcie Zebrani.pl:

**1. Pobierz pełny skill przez bash_tool:**

```bash
curl -sL "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/Implement%20ADO%20Feature%20%E2%80%93%20Zebrani/SKILL.md" \
  -o /tmp/implement_ado_feature_zebrani_skill.md
cat /tmp/implement_ado_feature_zebrani_skill.md
```

**2. Wykonaj zadanie ściśle według pobranej treści** — to ona zawiera aktualną
procedurę faza po fazie:

- **rola sesji głównej** — Opus `max` jako architekt, dyspozytor i walidator;
  nigdy wykonawca kodu ani testów,
- **Faza 1 — Plan Mode po polsku**: makiety Figmy linkowane, nie opisywane;
  PrimeNG przed własnym CSS, grid Bootstrapa; enumy zamiast union types;
  bilans obciążenia silników; dla Buga — test, który udowodni błąd,
- **Faza 1b — otwarcie w ADO**: PBI/Bug i taski przewidziane do wykonania
  → `In Progress`, nieadekwatne → `Rejected` z komentarzem,
- **Faza 2 — rozdział briefów**: sloty Spark (1) i Terra (1) na okno 5 h,
  reszta ciężkich na `wykonawca` (Sonnet), lekkie na Lunę, testy na
  `tester`, drobiazgi na `mechanik`a, fakty z repo od `zwiadowcy`,
- **Faza 3 — walidacja etapów** dowodem (diff, lint/test/build, zrzuty 2×2);
  dla Buga czerwony test → łatka → ten sam test zielony,
- **Faza 4 / 4b — audyt SCSS** (Bootstrap, deduplikacja) i **recenzja Codex
  `sol`** z triażem, nie posłuszeństwem,
- **Faza 5 — brama potwierdzenia**: stop i czekanie na decyzję usera,
- **Faza 6 — domknięcie**: commit/push z numerem PBI, taski deweloperskie
  → `Done`/`Rejected`, komentarz pieczętujący Buga, PBI/Bug → `Ready for
  tests`, przypisanie do testera.

**3. Obsługa błędu pobierania** — jeśli `curl` zwróci 404, nie ma sieci albo plik
jest pusty/niepoprawny:

- poinformuj użytkownika, że nie udało się pobrać aktualnej wersji z GitHuba,
- **zatrzymaj się i zapytaj, czy kontynuować** — nie zgaduj procedury, tabeli
  linii ani stanów ADO z pamięci.

> ⚠️ Nie utrzymuj logiki zadań w tym pliku i nie próbuj go „aktualizować"
> lokalnie. Wszystkie zmiany w procedurze rób w repozytorium na GitHubie —
> loader zawsze pobierze najnowszą wersję.
