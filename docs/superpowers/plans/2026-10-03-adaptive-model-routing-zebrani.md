# Adaptacyjne routowanie modeli dla ADO Zebrani — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Zmienić kanoniczny skill ADO tak, by dla każdego briefu osobno dobierał dopuszczony model i jego natywny effort, a wyniki routingu oceniał na podstawie zaakceptowanej pracy.

**Architecture:** Opus pozostaje architektem i podejmuje decyzje na podstawie ryzyka, narzędzi, lokalnych wyników i sygnałów dostępności. Twarde ograniczenia określają dopuszczone linie; wśród nich wybierane są model i effort dla wykonawcy oraz niezależnego recenzenta. Krótkie wpisy w rejestrze umożliwią okresową ocenę bez wprowadzania automatycznego routera ani nieuzasadnionej punktacji.

**Tech Stack:** Markdown, Claude Code, istniejący skrypt synchronizacji `sync-routing.py`; bez zmian kodu aplikacji i bez nowych zależności.

## Global Constraints

- Jednostką routingu jest brief wykonawczy lub recenzencki, nie typ ani numer work itemu ADO.
- Twarde ograniczenia ryzyka, narzędzi, uprawnień, niezależności recenzenta i skilli pomocniczych odrzucają niedopuszczone pary przed porównaniem kosztu.
- Każdy istotny brief ma model, natywny effort, krótkie uzasadnienie, pewność wyboru i dopuszczone alternatywy.
- W pierwszym pilotażu architektem pozostaje Opus `xhigh`; Codex jest pełnoprawnym kandydatem do kwalifikujących się briefów.
- Po każdej fali niezależna rodzina recenzuje diff, a architekt sprawdza artefakty i dowody. Recenzja całego feature’a high-stakes zachowuje obecną bramkę i trwające porównanie Astry/Sola.
- Dostępność oznaczamy jako znaną, ostrzegawczą, zablokowaną albo nieznaną. Nie dopisujemy nieznanych procentów limitu.
- Rejestr nie zawiera promptów, diffów, danych osobowych ani surowych zestawień tokenów. Wykorzystanie ADO pozostaje w istniejącym raporcie.
- Mechanika uruchamiania workerów w `external-workers`, ograniczenia `qasphere-test-generator` i adapter Codexa pozostają bez zmian; korekta obejmuje wyłącznie nieaktualne opisy routingu w `external-workers`.
- Nie zmieniamy dokumentacji produktowej Zebrani, statusów ADO, wrappera ani `token-report.py`.
- Usuwamy literalne poświadczenie API z edytowanych instrukcji i zastępujemy je odwołaniem do `$env:ARTIFICIAL_ANALYSIS_API_KEY`; nie ujawniamy jego wartości i nie wykonujemy rotacji poświadczenia w tym wdrożeniu.
- Nie wykonujemy testów aplikacji dla zmian dokumentacyjnych. Nie commitujemy ani nie pushujemy bez osobnego polecenia.

---

## Zakres i mapa plików

1. `Implement ADO Feature – Zebrani/SKILL.md` — kanoniczna procedura, aktualizacja wersji `5.14` → `5.15`, kryteria doboru dla każdego briefu i przeglądu.
2. `docs/model-routing-evaluation.md` — nowy schemat wpisów z pilotażu i rytm okresowej oceny.
3. `C:\Users\Damian\.claude\CLAUDE.md` — nadrzędne reguły oraz macierz możliwości, ograniczeń i dostępności wspólnych linii.
4. `D:\projects\DTCode\ZebraniFE\.claude\CLAUDE.md` — źródło wspólnej sekcji routingu dla projektów DTCode.
5. Kopie wspólnej sekcji zapisywane przez `C:\Users\Damian\.claude\bin\sync-routing.py`:
   - `ZebraniFE/AGENTS.md`
   - `ZebraniBE/.claude/CLAUDE.md`
   - `ZebraniBE/AGENTS.md`
   - `DTCodeBE/.claude/CLAUDE.md`
   - `DTCodeBE/AGENTS.md`
   - `DTCodeFE/.claude/CLAUDE.md`
   - `DTCodeFE/AGENTS.md`
   - `DomSztukiFE/.claude/CLAUDE.md`
   - `DomSztukiFE/AGENTS.md`
   - `TachoPingBE/.claude/CLAUDE.md`
   - `TachoPingFE/.claude/CLAUDE.md`
   - `UstawoZercaBE/.claude/CLAUDE.md`
   - `UstawoZercaFE/.claude/CLAUDE.md`
   - `UstawoZerca/Resureces/CLAUDE.md`

Źródłowy dokument Zebrani opisuje zmiany kopii FE i BE. Lokalna instrukcja w `ZebraniFE/.claude/CLAUDE.md` ustanawia jednak tę samą sekcję jako wspólną dla wszystkich projektów DTCode, a istniejący synchronizator zapisuje ją do 14 powyższych plików. Plan zachowuje ten udokumentowany mechanizm, więc propaguje zmianę routingu poza dwa repozytoria Zebrani.

`ZebraniFE/AGENTS.md` ma obecnie 63 845 B, a synchronizator ostrzega przy 64 000 B. Zaktualizowana wspólna sekcja musi być na tyle krótka, by żaden docelowy `AGENTS.md` nie przekroczył tego limitu; szczególnie pilnujemy pliku FE. Przy zmianach listy plików, które synchronizator zapisuje, kolejność jest sekwencyjna: najpierw źródło, potem wygenerowane kopie.

Poza zakresem edycji pozostają `C:\Users\Damian\.codex\skills\implement-ado-feature-zebrani\SKILL.md`, mechanika skilla `external-workers`, skill `qasphere-test-generator`, skrypty routingu/telemetrii i kod aplikacji. W `external-workers` korygowane są tylko routingowe akapity.

## Plan realizacji

### Task 1: Utworzyć rejestr oceny routingu

**Files:**
- Create: `docs/model-routing-evaluation.md`

**Interfaces:**
- Dostarcza kanoniczny zestaw pól, z którego korzysta skill ADO w Task 2.

- [x] Dodać krótki cel rejestru oraz regułę, że wpis dotyczy istotnego briefu, nie mechanicznego drobiazgu.
- [x] Zdefiniować pola: identyfikator lub typ zadania bez treści biznesowej; archetyp; stawka; niepewność; linia, model i effort wykonawcy i recenzenta; dopuszczone alternatywy; powód, sygnał dostępności i pewność; wynik pierwszego podejścia; liczba rund korekt; czas do akceptacji; potwierdzone/odrzucone znaleziska recenzji z priorytetem; defekty po odbiorze; wymagane testy i dowody.
- [x] Dodać pusty, gotowy do skopiowania wiersz wpisu bez przykładowych danych biznesowych ani tokenów.
- [x] Zapisać rytm: pierwszy przegląd po 10–15 istotnych briefach, potem po kolejnych 10–15 lub istotnej zmianie modeli/pomiaru limitów; dodatkowy przegląd po istotnym błędzie albo kilku kosztownych poprawkach. Wyniki oceniać per archetyp; mała próbka nie uzasadnia rankingu.
- [x] Wyraźnie wskazać, że wykorzystanie/tokeny pozostają w istniejącym raporcie per ADO, a rejestr nie przechowuje promptów, diffów, PII ani surowych tokenowych zestawień.
- [x] Sprawdzić przez `rg -n` obecność każdego z pól i reguły rytmu; oczekiwany wynik: wszystkie pola są nazwane, a nie ma przykładów zawierających dane konkretnego zadania.

### Task 2: Zmienić kanoniczny skill ADO na dobór per brief

**Files:**
- Modify: `Implement ADO Feature – Zebrani/SKILL.md`
- Reference: `docs/model-routing-evaluation.md`

**Interfaces:**
- Używa schematu rejestru z Task 1.
- Zachowuje dotychczasowe fazy ADO, fale, kryteria akceptacji produktu i bramę potwierdzenia.

- [x] Zaktualizować opis routingu w nagłówku i metadane wersji z `5.14` na `5.15`.
- [x] W Fazie 1 wymagać dla każdego briefu klasyfikacji stawki, niepewności/nowości, zależności i zakresu plików, potrzebnych narzędzi/kontekstu oraz dostępnego test oracle i dowodów odbioru.
- [x] Zastąpić stałe „rodzaj pracy → model” decyzją w dwóch krokach: najpierw eliminacja niekwalifikujących się par model–effort według twardych ograniczeń, potem wybór najlepszej dopuszczonej pary na podstawie lokalnych wyników podobnych briefów, przewidywanych poprawek, czasu do akceptacji i wiarygodnego sygnału dostępności.
- [x] Utrzymać matrycę jako opis możliwości i ograniczeń. Rozdzielić twarde warunki od preferencji opartych na dotychczasowej jakości; nie dodawać punktacji ani sztywnego progu kosztu bez danych z pilotażu.
- [x] Wymagać jawnego modelu i jego natywnego effortu dla wykonawcy oraz recenzenta, krótkiego uzasadnienia, pewności i dopuszczonych alternatyw. Nie traktować nazw effortu u różnych dostawców jako równoważnych.
- [x] Dopuścić Codexa do kwalifikujących się briefów bez czekania na limit innej linii; zachować Claude Opus `xhigh` jako architekta w pilotażu.
- [x] Zachować jako twarde ograniczenia listę high-stakes, dostęp do Figmy, podział na rozłączne fale, niezależność rodziny recenzenta, reguły walidacji wykonawców i ograniczenia skilli pomocniczych. QA Sphere nadal używa własnych reguł autora, recenzenta i skryptu publikującego.
- [x] Po limicie lub rzeczywistym niepowodzeniu nakazać ponownie wyliczyć dopuszczone pary. Jeśli nie ma bezpiecznej linii, zatrzymać zadanie i zgłosić blokadę.
- [x] Wymagać jawnego statusu dostępności `znany / ostrzegawczy / zablokowany / nieznany`; zakazać szacowania procentu limitu na podstawie braku danych.
- [x] Zachować recenzję po każdej fali przez inną rodzinę, odbiór dowodów przez architekta po każdej fali oraz istniejący końcowy przegląd high-stakes i eksperyment Astra/Sol.
- [x] Dodać wpis do rejestru po istotnym briefie, bez dublowania raportu tokenów, i wskazać jego okresowy rytm oceny.
- [x] Przejrzeć cały skill pod kątem powtórzonych, sprzecznych mapowań w Fazie 1, 2, audycie i bramce. Usunąć tylko reguły preferencji, które stały się stałym routingiem; nie osłabiać żadnej twardej bramki.
- [x] W miejscu instrukcji wywołania Artificial Analysis zastąpić osadzoną wartość nagłówka `x-api-key` odwołaniem do `$env:ARTIFICIAL_ANALYSIS_API_KEY`; nie wypisywać ani nie kopiować wartości poświadczenia.
- [x] Sprawdzić przez `rg -n` wersję, wymagane pola briefu, Codex jako kandydata, statusy dostępności i zachowanie recenzji po fali; oczekiwany wynik: brak pozostałych instrukcji mówiących, że Codex jest wyłącznie przelewem albo że model wybiera się wyłącznie według kategorii zadania.

### Task 3: Zaktualizować nadrzędne reguły Claude Code

**Files:**
- Modify: `C:\Users\Damian\.claude\CLAUDE.md`
- Reference: `Implement ADO Feature – Zebrani/SKILL.md`
- Reference: `docs/model-routing-evaluation.md`

**Interfaces:**
- Globalna polityka musi być zgodna z kanonicznym skillem i pozostaje wiążąca dla projektowych streszczeń.

- [x] Zmienić reguły globalne i tabelę routingu tak, by opisywały dopuszczalność kandydatów, możliwości narzędzi/uprawnień, rodzinę recenzenta, natywne efforty i sygnały dostępności, bez stałego przydziału zwykłych briefów do jednej linii.
- [x] Oddzielić hard gates od przesłanek preferencyjnych. Zachować listę high-stakes, zakazy wynikające z dostępu, Figmę wymagającą właściwego MCP, limity równoległości i wymóg niezależnego recenzenta.
- [x] Ustalić, że lokalne wyniki zaakceptowanych briefów są główną przesłanką jakości; rankingi publiczne pozostają kontekstem pomocniczym i nie rozstrzygają samodzielnie.
- [x] Pozostawić ograniczenia kosztu i effortu dla każdego silnika, ale kierować ich użyciem per brief. Zachować bieżące porównania i próby (w tym Astra/Sol i próba Figmy) jako ograniczone eksperymenty, nie uniwersalne przypisania modeli.
- [x] Dostosować reguły limitów i recenzji do statusów dostępności oraz ponownej kwalifikacji po limicie. Nie dodawać wymyślonych procentów ani żądania ręcznego `/usage` tam, gdzie obecna procedura tego zabrania.
- [x] Zachować decyzję, że architekt sam wybiera silnik i nie pyta użytkownika o routowanie, oraz odpowiedzialność architekta za brief, dowody i końcową akceptację.
- [x] Nie kopiować sekretu z istniejących instrukcji do nowej treści, diffu, raportu ani logu.
- [x] W instrukcji pobierania danych Artificial Analysis zastąpić osadzoną wartość nagłówka `x-api-key` odwołaniem do `$env:ARTIFICIAL_ANALYSIS_API_KEY`; nie ujawniać wartości i nie wykonywać rotacji.
- [x] Sprawdzić przez `rg -n` i lekturę zmienionych sekcji: brak sprzeczności z kryteriami skillu ADO, zachowane ograniczenia high-stakes i eksperymenty, brak ujawnionych poświadczeń.

### Task 4: Zaktualizować wspólną sekcję i zsynchronizować kopie

**Files:**
- Modify: `D:\projects\DTCode\ZebraniFE\.claude\CLAUDE.md` — źródło sekcji `Working Mode — Orchestrator + Subagents (both stacks)`.
- Generated by the existing synchronizer: 14 plików wymienionych w mapie zakresu.
- Run: `C:\Users\Damian\.claude\bin\sync-routing.py`.

**Interfaces:**
- Sekcja źródłowa streszcza globalne i ADO zasady w języku projektu; nie zastępuje pełnej procedury skillu.
- Skrypt synchronizujący pozostaje bez zmian i zapisuje dokładnie sekcję ze źródła do listy `TARGETS`.

- [x] Zastąpić w źródle sekcji stałe kierowanie zwykłych briefów krótkim opisem selekcji per brief, wyboru effortu oraz odrębnego doboru recenzenta.
- [x] Przed synchronizacją zastąpić osadzoną wartość nagłówka `x-api-key` odwołaniem do `$env:ARTIFICIAL_ANALYSIS_API_KEY`, aby synchronizator nie rozpropagował poświadczenia do kopii projektu.
- [x] Zachować w streszczeniu wszystkie twarde ograniczenia architekta, high-stakes, dostępu do Figmy, narzędzi, rozłącznych fal, walidacji i niezależnej rodziny recenzenta.
- [x] Zwięźle wskazać rolę lokalnych wyników, sygnałów dostępności, procedury limitu i okresowej oceny; szczegóły pozostawić w skillu/globalnych regułach.
- [x] Uruchomić synchronizator z repozytorium `D:\projects\DTCode`: `python C:\Users\Damian\.claude\bin\sync-routing.py`.
- [x] Sprawdzić rozmiar wszystkich plików `AGENTS.md` po synchronizacji. Oczekiwany wynik: każdy ma mniej niż 64 000 B, a skrypt nie zgłasza przekroczenia limitu Sparka.
- [x] Uruchomić kontrolę tylko do odczytu: `python C:\Users\Damian\.claude\bin\sync-routing.py --check`. Oczekiwany kod wyjścia: `0`; każda z 14 kopii ma stan `zgodna`.
- [x] Sprawdzić `git status --short` we wszystkich dotkniętych repozytoriach i zachować istniejące, niezwiązane zmiany bez edycji.

### Task 5: Końcowa kontrola zgodności dokumentów

**Files:**
- Review: `Implement ADO Feature – Zebrani/SKILL.md`
- Review: `docs/model-routing-evaluation.md`
- Review: `C:\Users\Damian\.claude\CLAUDE.md`
- Review: wspólna sekcja źródłowa i jej zsynchronizowane kopie
- Review and align routing-only passages: `C:\Users\Damian\.claude\skills\external-workers\SKILL.md`
- Review only, bez edycji: adapter Codexa i `qasphere-test-generator`

**Interfaces:**
- Każda instrukcja routingu ma zgodne twarde ograniczenia; szczegółowy proces pozostaje w kanonicznym skillu.

- [x] Przejrzeć diffy w każdym repozytorium dotkniętym synchronizacją i potwierdzić, że zmieniła się tylko wspólna sekcja routingu, zatwierdzone pliki skilla/rejestru oraz routingowe akapity `external-workers`; adapter Codexa i `qasphere-test-generator` pozostają bez zmian.
- [x] Uruchomić `git diff --check` w każdym dotkniętym repozytorium. Oczekiwany wynik: brak błędów białych znaków.
- [x] Powtórzyć `python C:\Users\Damian\.claude\bin\sync-routing.py --check`; oczekiwany kod wyjścia `0`.
- [x] Przeszukać zmienione instrukcje pod kątem sprzecznych pozostałości takich jak `Codex ... wyłącznie ... przelew`, stałych przypisań zwykłych briefów do Spark/Gemini/Sonnet i recenzenta przypisanego wyłącznie po autorze. Pozostawić wystąpienia historyczne lub opisujące hard gate tylko wtedy, gdy są wyraźnie oznaczone jako takie i nie przeczą nowemu wyborowi per brief.
- [x] Potwierdzić wersję `5.15`, komplet pól briefu i rejestru, rytm oceny, zachowanie recenzji po każdej fali, bramkę high-stakes, nieznany status limitu oraz brak zmiany adaptera Codexa i `qasphere-test-generator`.
- [x] Sprawdzić zmienione instrukcje pod kątem wzorca literalnych kluczy `aa_…`; oczekiwany wynik: brak osadzonych wartości, a wszystkie instrukcje wskazują zmienną środowiskową.
- [x] Nie uruchamiać lintów, testów ani buildów aplikacji: wdrożenie zmienia wyłącznie Markdown i reguły narzędzi.
- [x] Zakończyć bez commita, pushu, publikacji skilla ani zmian statusów ADO.

## Weryfikacja planu

- Każdy obszar zaakceptowanej specyfikacji ma przypisane zadanie: wybór per brief i per recenzent (Task 2–4), bramki bezpieczeństwa i narzędzi (Task 2–4), Codex jako kandydat (Task 2–3), status dostępności i limity (Task 2–4), przegląd po każdej fali i odbiór architekta (Task 2–4), trwały rejestr oraz rytm okresowy (Task 1–2), korekta routingowych akapitów `external-workers` i zachowanie mechaniki adaptera Codexa oraz `qasphere-test-generator` (Task 5).
- Plan nie dodaje scoringu, automatycznego routingu, telemetrycznych zmian ani prac nad produktem.
- Plan uwzględnia dodatkowy skutek synchronizatora: propagację wspólnej reguły do 14 kopii w projektach DTCode.
- Plan uwzględnia próg 64 000 B synchronizatora i obecny rozmiar `ZebraniFE/AGENTS.md` wynoszący 63 845 B.
- Plan usuwa ryzyko skopiowania literalnego poświadczenia przy edycji wspólnych instrukcji; rotacja jest poza tym wdrożeniem.
- Nie ma kroków implementacyjnych dotyczących kodu aplikacji ani testów jednostkowych, bo spec obejmuje wyłącznie instrukcje i rejestr Markdown.
