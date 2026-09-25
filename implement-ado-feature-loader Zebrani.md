---
name: implement-ado-feature-zebrani
description: >
  Planowanie i pełna implementacja feature'a / PBI / taska Zebrani.pl na
  podstawie linku lub numeru Azure DevOps — od Plan Mode (z makietami Figmy
  linkowanymi wprost, nie opisywanymi), przez wykonanie w modelu: sesja
  główna Opus max = architekt, dyspozytor i walidator etapów (sama nigdy
  nie pisze kodu ani testów — implementacja na poziomie Opusa idzie do
  subagenta wykonawca-opus) / linie wykonawcze: briefy wysokiej stawki
  i za trudne dla Sonneta na wykonawca-opus (Opus xhigh, także ich ekrany
  z Figmy), pozostałe ekrany z Figmy i briefy z kontekstem sesji wyłącznie
  na wykonawca (Sonnet high), każdy brief bez Figmy i spoza wysokiej stawki
  na Sparka (xhigh/high, -Access write, bez limitu slotów), w fali resztę
  także na Gemini (agy, -Access write, nigdy wysoka stawka ani Figma);
  research na Sola, Codex w planie tylko do trudnego researchu i bramki
  Astry / recenzent zawsze z innej rodziny niż autor (diff Sparka → Gemini,
  diff Sonneta/Opusa/Codexa/Gemini → Spark, Sol tylko na limit; P0/P1 do
  obalenia jednym poleceniem), przez audyt SCSS na Sparku, aż po bramę
  potwierdzenia i domknięcie w ADO (commit/push, statusy tasków
  deweloperskich, PBI → Ready for tests, przypisanie do testera).
  Na starcie, po zatwierdzeniu planu, PBI/Bug i taski do wykonania idą na
  In Progress. Obejmuje też Bugi — test-first: czerwony test, łatka, ten
  sam test zielony. UŻYWAJ ZAWSZE, gdy user
  poda link lub numer Epic/Feature/PBI/Task/Bug
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
fale i rozdział briefów na linie wykonawcze, walidacja fal, audyt SCSS,
recenzja niezależna, brama potwierdzenia, domknięcie w ADO) jest trzymana
na GitHubie i to ona jest źródłem prawdy.

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

- **rola sesji głównej** — Opus `max` jako architekt, dyspozytor
  i walidator; sama nigdy nie pisze kodu ani testów (implementacja
  na poziomie Opusa idzie do subagenta `wykonawca-opus`),
- **Faza 1 — Plan Mode po polsku**: makiety Figmy linkowane, nie opisywane;
  PrimeNG przed własnym CSS, grid Bootstrapa; enumy zamiast union types;
  bilans obciążenia silników; dla Buga — test, który udowodni błąd,
- **Faza 1b — otwarcie w ADO**: PBI/Bug i taski przewidziane do wykonania
  → `In Progress`, nieadekwatne → `Rejected` z komentarzem, marker zużycia
  tokenów (`token-report.py start`),
- **Faza 2 — fale i rozdział briefów** w stałej kolejności
  Claude → Spark → Codex: wysoka stawka i briefy za trudne dla Sonneta
  na `wykonawca-opus` (Opus xhigh, także ich ekrany z Figmy), pozostałe
  ekrany z Figmy i briefy z kontekstem sesji wyłącznie na `wykonawca`
  (Sonnet), każdy brief bez Figmy i spoza wysokiej stawki na Sparka
  bez limitu slotów, w fali resztę także na Gemini (nigdy wysoka stawka
  ani Figma); research rutynowy i trudny na Sola, Codex w planie tylko
  do trudnego researchu i bramki Astry; testy na `tester`, drobiazgi na
  `mechanik`a, fakty z repo od `zwiadowcy`; tory poboczne (Figma,
  dokumentacja, ADO, briefy kolejnej fali) ruszają równolegle, gdy tylko
  decyzja, od której zależą, jest ustalona; bez odczytów `/usage` —
  linia zmienia się po komunikacie o limicie,
- **Faza 3 — walidacja fal** dowodem (diff, lint/test/build, zrzuty 2×2),
  raz na falę; dla Buga czerwony test → łatka → ten sam test zielony,
- **Faza 4 / 4b — audyt SCSS** na Sparku (Bootstrap, deduplikacja; próba
  trwa) i **recenzja z innej rodziny niż autor diffu** (diff Sparka →
  Gemini, diff Sonneta/Opusa/Codexa/Gemini → Spark, Sol tylko gdy właściwy
  recenzent ma limit; przy feature'ze wysokiej stawki bramka końcowa Astry)
  z triażem, nie posłuszeństwem,
- **Faza 5 — brama potwierdzenia**: stop i czekanie na decyzję usera,
- **Faza 6 — domknięcie**: commit/push z numerem PBI, taski deweloperskie
  → `Done`/`Rejected`, komentarz pieczętujący Buga, PBI/Bug → `Ready for
  tests`, przypisanie do testera, raport zużycia tokenów per silnik i model
  (`token-report.py report`).

**3. Obsługa błędu pobierania** — jeśli `curl` zwróci 404, nie ma sieci albo plik
jest pusty/niepoprawny:

- poinformuj użytkownika, że nie udało się pobrać aktualnej wersji z GitHuba,
- **zatrzymaj się i zapytaj, czy kontynuować** — nie zgaduj procedury, tabeli
  linii ani stanów ADO z pamięci.

> ⚠️ Nie utrzymuj logiki zadań w tym pliku i nie próbuj go „aktualizować"
> lokalnie. Wszystkie zmiany w procedurze rób w repozytorium na GitHubie —
> loader zawsze pobierze najnowszą wersję.
