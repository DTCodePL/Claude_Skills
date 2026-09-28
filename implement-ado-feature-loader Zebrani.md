---
name: implement-ado-feature-zebrani
description: >
  Planowanie i pełna implementacja feature'a / PBI / taska Zebrani.pl na
  podstawie linku lub numeru Azure DevOps — od Plan Mode (z makietami Figmy
  linkowanymi wprost, nie opisywanymi), przez otwarcie w ADO (PBI/Bug
  i taski do wykonania → In Progress), wykonanie etapami w falach briefów
  rozdzielanych na linie wykonawcze wg routingu z globalnego CLAUDE.md
  (sesja główna = architekt, dyspozytor i walidator — nigdy wykonawca),
  audyt SCSS i recenzję z innej rodziny modeli niż autor diffu, aż po bramę
  potwierdzenia użytkownika i domknięcie w ADO (commit/push, statusy tasków
  deweloperskich, PBI → Ready for tests, przypisanie do testera). Obejmuje
  też Bugi — test-first: czerwony test, łatka, ten sam test zielony. Cienki
  loader: pełną procedurę pobiera z GitHuba. UŻYWAJ ZAWSZE, gdy user poda
  link lub numer Epic/Feature/PBI/Task/Bug z Azure DevOps projektu
  Zebrani.pl i poprosi o zaplanowanie, zaimplementowanie i/lub naprawienie
  go — nawet jeśli nie padnie słowo "skill".
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
fale i rozdział briefów na linie wykonawcze, walidacja fal, audyt SCSS,
recenzja niezależna, brama potwierdzenia, domknięcie w ADO) jest trzymana
na GitHubie i to ona jest źródłem prawdy.

**Loader jest celowo neutralny silnikowo** — nie wymienia silników, modeli,
effortów ani przydziału briefów do linii. Jego streszczenie routingu
rozjeżdżało się ze źródłem przy każdej zmianie (2026-09-28: kopia w repo
wciąż mówiła „Opus `max`”, „Gemini do researchu” i nie znała
`wykonawca-opus`). Routing bierzesz wyłącznie z pobranej treści
i z globalnego `~/.claude/CLAUDE.md` — nie z tego pliku ani z pamięci.

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
procedurę faza po fazie: rolę sesji głównej, Fazę 1 (Plan Mode po polsku,
z kontrolą routingu planu), 1b (otwarcie w ADO), 2 (fale i rozdział
briefów), 3 (walidacja fal; dla Buga test-first), 4 / 4b (audyt SCSS
i recenzja niezależna), 5 (brama potwierdzenia) i 6 (domknięcie w ADO
i raport zużycia tokenów).

**3. Obsługa błędu pobierania** — jeśli `curl` zwróci 404, nie ma sieci albo plik
jest pusty/niepoprawny:

- poinformuj użytkownika, że nie udało się pobrać aktualnej wersji z GitHuba,
- **zatrzymaj się i zapytaj, czy kontynuować** — nie zgaduj procedury, tabeli
  linii ani stanów ADO z pamięci.

> ⚠️ Nie utrzymuj logiki zadań w tym pliku i nie próbuj go „aktualizować"
> lokalnie. Wszystkie zmiany w procedurze rób w repozytorium na GitHubie —
> loader zawsze pobierze najnowszą wersję. Wzorzec loadera:
> `Claude_Skills/implement-ado-feature-loader Zebrani.md`; kopie
> w `ZebraniFE` i `ZebraniBE` (`.claude/skills/implement-ado-feature-zebrani/SKILL.md`)
> są z nim identyczne bajt w bajt.
