# Rejestr oceny routingu modeli (Model Routing Evaluation)

## 1. Cel rejestru i reguła kwalifikacji

Niniejszy rejestr służy do gromadzenia ustrukturyzowanych danych operacyjnych na potrzeby okresowej ewaluacji i kalibracji adaptacyjnego doboru modeli oraz natywnego effortu per brief w procedurach ADO projektów DTCode.

**Reguła kwalifikacji wpisów:**
- Wpis w rejestrze dotyczy wyłącznie **istotnego briefu wykonawczego** (posiadającego nietrywialny zakres implementacyjny, architektoniczny, testowy lub merytoryczny).
- Wpisu **nie tworzy się** dla mechanicznych drobiazgów (np. pojedyncza zmiana wersji, poprawka literówki w komentarzu, drobna zmiana kosmetyczna formatowania bez logiki).

## 2. Zasady poufności i minimalizacji danych

- **Wykorzystanie i tokeny:** Dokładne zestawienia zużycia tokenów i kosztów pozostają w istniejącym raporcie per ADO (`token-report.py` / raport ADO). Rejestr nie dubluje tych danych.
- **Brak treści wrażliwych:** Rejestr nie przechowuje promptów, diffów kodu, danych osobowych (PII), tajemnic handlowych ani surowych tokenowych zestawień.
- **Brak treści biznesowej w identyfikatorze:** W polu identyfikatora stosuje się wyłącznie neutralne oznaczenia techniczne lub ogólne typy zadań bez ujawniania logiki biznesowej ani domenowej.

## 3. Kanoniczne pola rejestru

Każdy wpis rejestru definiuje następujący zestaw pól (w tej kolejności, zgodnie z szablonem z sekcji 4):

1. **Identyfikator lub typ zadania bez treści biznesowej** — neutralny identyfikator techniczny briefu (np. oznaczenie fali i numeru briefu) lub ogólny typ zadania, bez ujawniania logiki biznesowej.
2. **Archetyp** — kategoria techniczna briefu (np. Frontend UI / Figma, Backend API / CRUD, Refactoring / Architektura, Algorytmika / Logika, Konfiguracja / DevOps, Testy E2E / QA).
3. **Stawka** — poziom ryzyka i skutki ewentualnego błędu (niska, średnia, wysoka / high-stakes, krytyczna).
4. **Niepewność** — stopień nowości technicznej oraz niepewności rozwiązania (niska, średnia, wysoka).
5. **Wykonawca (linia / model / native effort)** — linia (rodzina), dokładny model oraz natywny effort rozumiany w ramach danego silnika.
6. **Recenzent (linia / model / native effort)** — niezależny recenzent z innej rodziny niż autor: linia, dokładny model oraz natywny effort w ramach danego silnika.
7. **Dopuszczone alternatywy** — zestaw innych zweryfikowanych par linia/model/effort, które spełniały twarde bramki kwalifikacyjne dla danego briefu.
8. **Powód wyboru** — zwięzłe uzasadnienie dopasowania modelu i effortu do specyfiki briefu.
9. **Sygnał dostępności** — stan abonamentu lub przepustowości (`znany`, `ostrzegawczy`, `zablokowany` albo `nieznany` — bez zgadywania wartości procentowych) wraz ze źródłem i czasem odczytu.
10. **Pewność decyzji** — pewność decyzji routingu (`wysoka`, `średnia`, `niska`).
11. **Wynik pierwszego podejścia** — stan po zakończeniu pierwszego wykonania przed ewentualnymi poprawkami (np. zaakceptowano, wymagane korekty, odrzucono / błąd).
12. **Rundy korekt** — liczba kolejnych iteracji i poprawek wykonanych przed akceptacją (0 dla pierwszego podejścia zakończonego sukcesem, 1, 2 itd.).
13. **Czas do akceptacji** — całkowity czas od rozpoczęcia realizacji briefu do ostatecznej akceptacji przez architekta.
14. **Znaleziska recenzji (potwierdzone/odrzucone, priorytet)** — zestawienie uwag recenzenta zweryfikowanych przez architekta z podziałem na potwierdzone i odrzucone wraz z ich priorytetami (np. potwierdzone z priorytetem P1-P3, odrzucone z priorytetem P1-P3).
15. **Defekty po odbiorze** — ewentualne wady lub regresje zidentyfikowane po akceptacji briefu w kolejnych falach lub integracji (lub informacja o braku defektów).
16. **Wymagane testy i dowody** — rezultat wykonania wymaganego test oracle oraz dowodów odbioru (np. wynik testów jednostkowych, integracyjnych, weryfikacji w przeglądarce, PRE lub innych dowodów).

## 4. Wpisy

Poniższy szablon jest kanoniczną postacią wpisu. W rejestrze nie umieszcza się przykładowych danych biznesowych ani wartości tokenów. Nowy wpis dopisuj na końcu podsekcji „Wpisy” (przed sekcją 5), kopiując szablon.

```markdown
### <identyfikator briefu bez treści biznesowej> — <data RRRR-MM-DD>
- Archetyp:
- Stawka:
- Niepewność:
- Wykonawca (linia / model / native effort):
- Recenzent (linia / model / native effort):
- Dopuszczone alternatywy:
- Powód wyboru:
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas):
- Pewność decyzji:
- Wynik pierwszego podejścia:
- Rundy korekt:
- Czas do akceptacji:
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet):
- Defekty po odbiorze:
- Wymagane testy i dowody:
```

### Dane historyczne sprzed rejestru (2026-09-16…2026-10-03)

Zbiorcze obserwacje z ocen etapów prowadzonych przed rejestrem. To nie są
wpisy per brief i nie tworzą rankingu — punkt wyjścia o niskiej pewności,
który kolejne wpisy mają potwierdzić albo obalić.

**Błędne kształty planu (routing, nie jakość kodu):**

- 2026-09-16 — plan z ośmioma ciężkimi briefami na Codexie, Claude tylko
  planował i testował; odrzucony przez właściciela — przeciążenie
  najmniejszej puli (Plus).
- 2026-09-18 — Spark bezczynny przy < 1 % tygodnia, gdy Codex niósł po dwa
  ciężkie briefy na etap — niewykorzystana tania pula.
- 2026-09-25…28 — `wykonawca-opus` robił ekrany FE (44 % jego kosztu),
  a Sonnet briefy tekstowe, które mogły iść do Sparka lub Gemini. Skutek:
  4 limity okna 5 h w 3 dni, każdy w oknie z `wykonawca-opus`; Opus (sesja
  + wykonawca) = 61–74 % kosztu tych okien. Przebieg `wykonawca-opus`
  średnio 31,7 $, `wykonawca` 14,7 $ (ceny API); 54–81 % kosztu każdej
  linii to ponowne czytanie kontekstu, wyjście 9–18 %.
- 2026-10-03 — przepisanie zasad routingu orkiestrowane w Codexie przez
  `gpt-6-luna` (`xhigh`/`max`) zamiast architekta Opus `xhigh`: ok. 6 h,
  6 kompakcji kontekstu, korekta Sola zepsuła semantykę wyjątku high-stakes,
  Spark zmienił końce linii i sąsiedni wiersz; niezależna recenzja Claude'a
  znalazła potem jeszcze 3×P1 niespójności między plikami.

**Wykonawcy — rundy korekty (etapy 2026-09-25…30):**

- Gemini (BE, dokumentacja, testy FE): zwykle 0–1 rundy na brief; od
  2026-09-28 często niedostępny (429 na starcie fali, limit tygodniowy) —
  briefy przechodziły na Sparka.
- Spark (logika FE, testy, dokumentacja, przypadki QA Sphere, weryfikacja
  w przeglądarce): przeważnie 0–1 rundy, znaczna część rund z winy planu;
  przypadki QA Sphere 1–3 rundy. Przejął brief `wykonawca-opus` przy
  CZERWONYM i uruchomił `dotnet` przez interop bez problemu. Raz uruchomił
  `git status` wbrew zakazowi (tylko odczyt).
- Sonnet `wykonawca` (ekrany wg Figmy, poprawki FE): 1–3 rundy na brief,
  7 rund na 5 briefów w ocenie z 2026-09-26 — podstawa próby A/B linii
  Figmy. Rozpoznanie Figmy (`get_metadata`) potrafiło zjeść ~300 tys.
  kontekstu bez kodu.
- `wykonawca-opus` (pliki niezmiennika high-stakes): 0–1 rundy z walidacji
  fal, ale 2–5 rund łącznie z recenzjami i bramką Astry. Kontynuacje po
  przekazaniu strażnika kontekstu — bez regresji.
- `tester`: 2 rundy (pułapki środowiska testowego); `mechanik`: 0 rund.
- Błędne przesłanki architekta: 2–5 na etap; wyłapywali je wykonawcy
  i recenzenci dzięki klauzuli STOP.

**Recenzenci:**

- Astra `max` (bramka końcowa): w trzech funkcjach high-stakes po
  wszystkich recenzjach fal znalazła jeszcze realne P1 (na jednej 2×P1 +
  4×P2) — niezastąpiona przy wysokiej stawce. Kilka przebiegów zablokował
  limit Codexa; dwa razy zastąpił ją Opus 5.5 tylko do odczytu (decyzja
  właściciela).
- Spark `xhigh`: zwykle „poprawny” 0,8–0,85; przeoczył P1, które znalazła
  Astra; zawyża priorytety, kilka fałszywych P0/P1 obalonych dowodem;
  urwał raport przy briefie 140 KB z wklejonym diffem (diff podawać
  ścieżką lub ograniczać).
- Gemini: kod — bez fałszywych P0/P1, pewność 0,95–0,98; dokumentacja —
  1 fałszywe P0 i zawyżone P1.
- Sol `high` (zastępstwo przy limicie Gemini): kilka przebiegów, 0
  fałszywych P0/P1, realne P2.
- Sonnet tylko do odczytu (zastępstwo przy limicie Codexa i Gemini): 0
  fałszywych P0/P1, realne P3.

### Wpisy

### routing-docs-B1 — 2026-10-04
- Archetyp: dokumentacja / polityka routingu (pliki globalne i definicje agentów)
- Stawka: średnia — cicha sprzeczność reguł wpływa na każdy kolejny plan
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Claude / Opus 5.5 / `xhigh` (`wykonawca-opus`)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh`, `-Access read`
- Dopuszczone alternatywy: Claude / Sonnet 5.5 / `high` (`wykonawca`); Spark / `xhigh` `-Access write` (wtedy recenzent z innej rodziny); Codex odrzucony — brak zapisu do `~/.claude` w poprzednim przebiegu, pula Plus
- Powód wyboru: tekst przekrojowy z cichym błędem; przy poprzednim przepisaniu workerzy dwukrotnie zepsuli semantykę
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany, ZIELONY (hook, 2026-10-04 rano); Spark nieznany
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: wymagane korekty
- Rundy korekt: 1 (plus 3 jednolinijkowe poprawki architekta)
- Czas do akceptacji: ok. 40 min (start fali → recenzja kontrolna)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): recenzja fali B1–B3: 3×P1, 2×P2, 2×P3 potwierdzone, 0 odrzuconych; kontrolna: poprawny 0,85, 2×P3 potwierdzone; raport wykonawcy błędnie podał CRLF (pliki w LF)
- Defekty po odbiorze: brak (stan na 2026-10-04)
- Wymagane testy i dowody: grep kryteriów, kontrola końców linii Pythonem, `sync-routing.py --check` 14/14

### routing-docs-B2 — 2026-10-04
- Archetyp: dokumentacja / kanoniczny skill ADO + rejestr routingu
- Stawka: średnia
- Niepewność: niska — brzmienie decyzji podane w briefie
- Wykonawca (linia / model / native effort): Claude / Sonnet 5.5 / `high` (`wykonawca`)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh`, `-Access read`
- Dopuszczone alternatywy: Claude / Opus 5.5 / `xhigh`; Spark / `xhigh` `-Access write`
- Powód wyboru: edycje o zadanym brzmieniu w jednym repo, bez niezmiennika
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany, ZIELONY (hook, 2026-10-04 rano); Spark nieznany
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: wymagane korekty (jedno zdanie rejestru poprawił architekt)
- Rundy korekt: 1
- Czas do akceptacji: ok. 40 min (wspólna fala)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): w recenzji fali m.in. brak wiersza `wykonawca-opus-medium` i stałego recenzenta próby A/B (P1), potwierdzone; kontrolna: 2×P3 w skillu, poprawione przez architekta
- Defekty po odbiorze: brak (stan na 2026-10-04)
- Wymagane testy i dowody: `yaml.safe_load` front matter, kontrola LF, grep kryteriów

### routing-docs-B3 — 2026-10-04
- Archetyp: dokumentacja / wspólna sekcja routingu (źródło synchronizacji 14 kopii)
- Stawka: średnia — sekcja trafia do 10 repozytoriów
- Niepewność: niska
- Wykonawca (linia / model / native effort): Claude / Sonnet 5.5 / `high` (`wykonawca`)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh`, `-Access read`
- Dopuszczone alternatywy: Spark / `xhigh` `-Access write`; Gemini / `gemini-3.8-flash-high` `-Access write`
- Powód wyboru: krótkie edycje o zadanym brzmieniu; limit 64 000 B `AGENTS.md`
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany, ZIELONY (hook, 2026-10-04 rano)
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: wymagane korekty
- Rundy korekt: 1
- Czas do akceptacji: ok. 40 min (wspólna fala)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): w recenzji fali brak `wykonawca-opus-medium` na liście dyspozycji (P1) i reguła puli Codexa przy sygnale `nieznany` (P2), potwierdzone
- Defekty po odbiorze: brak (stan na 2026-10-04)
- Wymagane testy i dowody: grep neutralności sekcji, identyczność akapitu Zebrani w 4 plikach, rozmiar `AGENTS.md` 60 290 B, `sync-routing.py --check` 14/14

### browser-check-W1 (rdzeń CLI + tryb zrzutów) — 2026-10-04
- Archetyp: narzędzie Node / Playwright (CLI do weryfikacji w przeglądarce, poza repo produktu)
- Stawka: średnia — fałszywy dowód odbioru i sekrety sesji na dysku
- Niepewność: średnia — logowanie i motyw aplikacji ustalone zwiadem, sesja nieznana
- Wykonawca (linia / model / native effort): Claude / Sonnet 5.5 / `high` (`wykonawca`)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh`, `-Access read`
- Dopuszczone alternatywy: Codex / `gpt-6.1-sol` / `high` (porcje ≤ 5 plików); Spark / `xhigh` `-Access write`
- Powód wyboru: wymagał żywej aplikacji, przeglądarki i iteracji na środowisku sesji; bez niezmiennika high-stakes
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany, ZIELONY (hook, 2026-10-04 ok. 12:20); Spark nieznany
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: wymagane korekty; wykonawca obalił 2 premisy briefu (przełącznik motywu na mobile, jednorazowy refresh token) i miał rację
- Rundy korekt: 1
- Czas do akceptacji: ok. 35 min (13 min wykonania + recenzja 8 min + korekta)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 22 zgłoszone (1×P0, 9×P1, 11×P2, 1×P3), przyjęte w 14 scalonych poprawkach; P0 krótkich sekretów przeszeregowane
- Defekty po odbiorze: tak — recenzja całości (Codex, fala 2) znalazła w plikach fali 1 dalsze defekty redakcji i walidacji ścieżek (P1/P2); domknięte w korekcie fali 2
- Wymagane testy i dowody: `node --check`, matryca 12/12 PNG na żywej aplikacji, przypadki błędów → exit 2, brak `.auth` po przebiegu

### browser-check-W2 (tryb przejść z modelem decyzyjnym + korekty 2–3) — 2026-10-04
- Archetyp: narzędzie Node / Playwright + zewnętrzny model klasyfikujący (pętla decyzyjna z deterministycznymi asercjami)
- Stawka: średnia — fałszywy PASS i dane osobowe wysyłane do zewnętrznego API
- Niepewność: wysoka — nowy model, nowy wzorzec pętli
- Wykonawca (linia / model / native effort): Claude / Sonnet 5.5 / `high` (`wykonawca`; korekty: świeży agent tej samej linii); 3 kilkulinijkowe poprawki architekta
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (runda 1 i 2); Spark / `muse-spark-1.3-contributor` / `xhigh`, `-Access read` (runda 3, sam diff korekty)
- Dopuszczone alternatywy: wykonawca Claude / Opus 5.5 / `xhigh` (logika przekrojowa z cichym błędem); Codex / `gpt-6.1-sol` / `high` (porcje ≤ 5 plików); recenzent Spark / `xhigh` w rundach 1–2
- Powód wyboru: wykonawca z dostępem do żywej aplikacji i iteracją na środowisku sesji; recenzent rundy 1 — najwyższa klasa recenzji spoza Claude'a dla nowego, przekrojowego kodu; runda 3 — mały diff, inna rodzina, oszczędność puli Plus
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany, ZIELONY (hook, 2026-10-04 13:00–14:50); Codex i Spark nieznany
- Pewność decyzji: średnia — z perspektywy wyniku przekrojowa logika maskowania i rozstrzygania PASS była na granicy Sonneta (2 rundy korekt z P1)
- Wynik pierwszego podejścia: wymagane korekty — działał (5/5 PASS), ale recenzja wykazała fałszywe PASS i wycieki do modelu
- Rundy korekt: 2 (plus 3 kilkulinijkowe poprawki architekta)
- Czas do akceptacji: ok. 2 h (fala 2 do 11:19 UTC → odbiór ok. 12:55 UTC; recenzje 12 + 14,5 + 6 min)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): runda 1: 16×P1, 7×P2, 1×P3 potwierdzone (część przeszeregowana), 0 odrzuconych; runda 2: 7×P1 + 3×P2 zgłoszone — 1×P1 potwierdzone bez zmian, 5 przeszeregowanych do P2, 2 do P3, 3×P2 potwierdzone, 0 odrzuconych; runda 3: 1×P2 + 2×P3 potwierdzone, 1×P3 odrzucone (celowe maskowanie)
- Defekty po odbiorze: brak (stan na 2026-10-04)
- Wymagane testy i dowody: testy-atrapy w prawdziwym Chrome dla każdej poprawki (wykonawca), przejścia właściciela ×3 i klienta ×3, matryca 12/12, skan artefaktów na hasła/e-maile/klucz API = 0 trafień (architekt); przejście bliskie progu pewności (0,73–0,79 przy progu 0,75) raz dało NEED_FALLBACK

### routing-docs-browser-check — 2026-10-04
- Archetyp: dokumentacja / polityka procesu (skill ADO, reguła globalna, sekcja wspólna 14 kopii)
- Stawka: średnia — zmienia dowód odbioru każdej fali we wszystkich projektach z UI
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Claude / Opus 5.5 / `xhigh` (architekt, reguła 11 — brzmienie = decyzja)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh`, `-Access read` (recenzja + kontrolna)
- Dopuszczone alternatywy: Claude / Sonnet 5.5 / `high` (`wykonawca`) jako autor; Codex / `gpt-6.1-sol` / `high` jako recenzent
- Powód wyboru: krótkie akapity o zadanym brzmieniu; recenzent spoza rodziny Claude, z dostępem do dokumentacji narzędzia w workspace
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany, ZIELONY (hook, 2026-10-04 ok. 15:00); Spark nieznany
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: wymagane korekty — tekst pomijał jawne `testData`, statusy inne niż FAIL/NEED_FALLBACK, błędy konsoli przy exit 0 i dziedziczenie zakazów przez workera MCP
- Rundy korekt: 2
- Czas do akceptacji: ok. 40 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): recenzja: 2×P0 (przeszeregowane do P1), 6×P1, 4×P2, 2×P3 zgłoszone; potwierdzone 2 (z P0) + 6×P1 + 2×P2 + 1×P3; odrzucone 2×P2 + 1×P3; kontrolna: skill naprawiony w całości, streszczenia w regule i sekcji gubiły pusty PASS i zakaz akcji nieodwracalnych — 2×P1 + 2×P2 potwierdzone, 1×P3 odrzucone
- Defekty po odbiorze: brak (stan na 2026-10-04)
- Wymagane testy i dowody: `sync-routing.py --check` 14/14, rozmiar `ZebraniFE/AGENTS.md` 61 148 B < 64 000 B

### jev-skill-analysis — 2026-10-04
- Archetyp: analiza / research procesu (gdzie model klasyfikujący daje wymierny zysk w skillu ADO)
- Stawka: niska — wynik to rekomendacja dla architekta
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh`, `-Access read`
- Recenzent (linia / model / native effort): brak osobnego — ocena architekta (Claude / Opus 5.5 / `xhigh`) względem skilla
- Dopuszczone alternatywy: Codex / `gpt-6.1-sol` / `medium` (research bez powłoki); Gemini / `gemini-3.8-flash-high`
- Powód wyboru: równoległy tor do fali Claude'a, inna pula; Spark miał wtedy wolne miejsce
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark nieznany (brak odczytu zapasu)
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowano (6 kandydatów J1–J6; architekt przyjął 1 warunkowo, 1 odrzucił)
- Rundy korekt: 0
- Czas do akceptacji: ok. 5 min (3 min przebiegu)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): nie dotyczy
- Defekty po odbiorze: brak (stan na 2026-10-04)
- Wymagane testy i dowody: odwołania do faz skilla sprawdzone przez architekta w `SKILL.md`

### browser-check-mcp-baseline — 2026-10-04
- Archetyp: pomiar porównawczy / weryfikacja w przeglądarce przez Playwright MCP (linia odniesienia dla trybu flows)
- Stawka: niska — wynik pomiarowy
- Niepewność: niska
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh`, `-Access write` (Playwright MCP przez interop)
- Recenzent (linia / model / native effort): brak — wynik porównany przez architekta z raportem narzędzia
- Dopuszczone alternatywy: Codex / `gpt-6.1-sol` / `high` (MCP po potwierdzeniu); Gemini / `gemini-3.8-flash-high`
- Powód wyboru: linia, która dziś robi zrzuty i przejścia po fali w skillu — porównanie miało mierzyć obecną praktykę
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark nieznany
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowano — 5/5 przejść zgodnych z narzędziem
- Rundy korekt: 0
- Czas do akceptacji: ok. 3 min (149 s przebiegu)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): nie dotyczy
- Defekty po odbiorze: brak
- Wymagane testy i dowody: raport przebiegu (tury, wywołania przeglądarki) zestawiony z `report.json` narzędzia na tych samych 5 scenariuszach

### routing-docs-bug-bez-e2e (skill v5.17) — 2026-10-04
- Archetyp: recenzja zasad procesu (tekst skilla, gałąź dowodu Buga)
- Stawka: średnia — zasada dowodu naprawy; błąd przepuszcza łatkę bez rzetelnego BEFORE/AFTER
- Niepewność: średnia — nowy wyjątek bez wcześniejszego wzorca
- Wykonawca (linia / model / native effort): architekt (Claude / Opus 5.5 / `xhigh`) — tekst skilla, nie kod
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh`, `-Access read`
- Dopuszczone alternatywy: Codex / `gpt-6.1-sol` / `high` (`-Mode review`); Gemini / `gemini-3.8-flash-high` (`-Access read`)
- Powód wyboru: inna rodzina niż autor; Spark znał już `browser-check` i skill fix-bug z poprzednich recenzji tej sesji
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark nieznany (brak odczytu zapasu), 13:12
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: odrzucono — werdykt „niepoprawny” (pewność 0,7)
- Rundy korekt: 1 (poprawki architekta, bez drugiej recenzji)
- Czas do akceptacji: ok. 4 min przebiegu + triaż
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): potwierdzone 3×P1 (dwie ręce także przy dowodzie w przeglądarce; podział na błąd interaktywny i czysto wizualny; zawężenie odesłania do kroków 3 i 6 fix-skilla), 4×P2 (tylko `FAIL`/`MAX_STEPS` jako BEFORE; porównanie SHA-256; pełny komentarz pieczętujący; AFTER z `passedWithoutActions:false` i izolacja danych), 2×P3 (`baseUrl` w briefie workera; `Get-FileHash`); odrzucone 0
- Defekty po odbiorze: brak (stan na 2026-10-04)
- Wymagane testy i dowody: architekt sprawdził nazwy statusów i powodów z kodem `browser-check` (`lib/flows.mjs`, `FLOWS.md`); recenzja potwierdziła brak miejsc dopuszczających test E2E w kodzie repo

### 1603-D (rewizje dokumentacji produktowej, D-1 + D-2) — 2026-10-04
- Archetyp: dokumentacja produktowa (rewizje dokumentów zatwierdzonych)
- Stawka: średnia — dokumentacja jest źródłem prawdy dla kodu i testów funkcji wysokiej stawki
- Niepewność: średnia — sprzeczności ze starszymi zapisami trzeba było wyłapać w wielu dokumentach
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `high`, `-Access write`
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read`
- Dopuszczone alternatywy: Gemini / `gemini-3.8-flash-high` `-Access write` (wtedy recenzent Spark); Claude / Sonnet 5.5 / `high` (`wykonawca`)
- Powód wyboru: tekst bez niezmiennika; Claude przewidziany dla plików niezmiennika i Figmy; osobna pula
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark i Gemini nieznany (brak odczytu zapasu), 2026-10-04 14:16
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: wymagane korekty (recenzja „niepoprawny”, znaleziska trafne)
- Rundy korekt: 2 (korekta D-1; uzupełnienie D-2 o późniejsze decyzje i jego poprawka)
- Czas do akceptacji: ok. 2 h 20 min (14:16 → ok. 16:35)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): D-1 — potwierdzone 3 (nowe rewizje nie uchylały wprost starszych zapisów; teksty dopłaty poniżej minimum operatora; dokument procesu opisywał starą metodę pobrania), odrzucone 0; D-2 — potwierdzone, skierowane do D-2-fix
- Defekty po odbiorze: 1 — rozbieżność dwóch dokumentów co do wyboru typu kupującego, wykryta przy przypadkach QA i rozstrzygnięta przez właściciela 2026-10-05
- Wymagane testy i dowody: diff przeczytany przez architekta, kontrola statusów front matter i linków, recenzja innej rodziny; zatwierdzenie na bramie potwierdzenia

### 1603-FE-1 (klucze i18n pl+en) — 2026-10-04
- Archetyp: Frontend / i18n
- Stawka: niska–średnia — teksty płatności i skutków zmiany widzi klient
- Niepewność: niska — brzmienie podane w planie
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `high`, `-Access write`
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read`
- Dopuszczone alternatywy: Gemini `-Access write`; Claude / Haiku `low` (`mechanik`) odrzucony — formy liczby mnogiej i spójność pl/en wymagają osądu
- Powód wyboru: tekst bez niezmiennika, duża liczba kluczy, pętla lint/test przez interop
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark i Gemini nieznany, 2026-10-04 14:16
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: wymagane korekty
- Rundy korekt: 1 (4 poprawki treści i 2 nowe klucze)
- Czas do akceptacji: ok. 30 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): zgodność ze specyfikacją potwierdzona; poprawki treści potwierdzone; 0 fałszywych P0/P1
- Defekty po odbiorze: brak (stan na 2026-10-05)
- Wymagane testy i dowody: spec spójności kluczy pl/en, lint i testy FE w walidacji fali

### 1603-FE-5 (przepływ FE, serwis HTTP i DTO — niezmiennik płatności) — 2026-10-04
- Archetyp: Frontend / logika przepływu z niezmiennikiem
- Stawka: wysoka — płatność i opłacone uprawnienia
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Claude / Opus 5.5 / `xhigh` (`wykonawca-opus`)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh`, `-Access read`
- Dopuszczone alternatywy: przy CZERWONYM Spark `xhigh` albo czekanie; poza tym brak (twarda bramka high-stakes)
- Powód wyboru: plik niosący niezmiennik płatności — twarda bramka
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany, ZIELONY (hook, 2026-10-04 ok. 14:00); Spark nieznany
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: wymagane korekty
- Rundy korekt: 4 (dwie rundy poprawek po recenzji, poprawka po recenzji poprawek, reakcja na nowy kod 409)
- Czas do akceptacji: ok. 6 h zegarowo (z oczekiwaniem na CZERWONY limit Claude'a)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): recenzja 1 — 1×P1 (zamknięcie w stanie oczekiwania przerywało odpytywanie) + 5×P3 potwierdzone; recenzja poprawek — 2 realne (ślepy zaułek ponowienia po wyczerpaniu limitu przeładowań, brak testu reguły) + 4 drobne potwierdzone, 1 odrzucone; 0 fałszywych P0/P1
- Defekty po odbiorze: bramka końcowa — 1×P1 (odpowiedzi poleceń po zmianie konta; brak strażnika generacji sesji) i 2×P2 (aktywne „Zapłać” w trakcie zapisu danych do faktury; utrata niezapisanej edycji przy przeliczaniu)
- Wymagane testy i dowody: czerwone testy przed poprawką (14 czerwonych na starym kodzie przy fix-3), pełna walidacja FE (lint, format, testy z AXE, build)

### 1603-BE-1 (trwałość i domena) — 2026-10-04
- Archetyp: Backend / migracja + domena wyliczeń
- Stawka: wysoka — migracja danych i wyliczenie dopłaty
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Claude / Opus 5.5 / `xhigh` (`wykonawca-opus`)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh`, `-Access read`
- Dopuszczone alternatywy: przy CZERWONYM Spark `xhigh` albo czekanie
- Powód wyboru: twarda bramka (migracja, wyliczenie wartości)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany, ZIELONY (hook, 2026-10-04 ok. 14:00); Spark nieznany
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: przekazanie — strażnik kontekstu zatrzymał przebieg przed pierwszym plikiem; zostało rozpoznanie i 6 pytań do specyfikacji
- Rundy korekt: 1 (BE-1c po recenzji) plus 2 kontynuacje (1a, 1b)
- Czas do akceptacji: ok. 2 h 15 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): poprawki z recenzji przeniesione do BE-1c; liczby znalezisk nie zachowały się w notatkach architekta
- Defekty po odbiorze: brak przypisanych do tego briefu (stan na 2026-10-05)
- Wymagane testy i dowody: build i pełne testy BE z `ZEBRANI_TEST_SQLSERVER` po każdym kroku
- Uwaga dla przeglądu: brief był za duży na jeden przebieg (reguła 15)

### 1603-BE-2 (bramka operatora płatności i atrapa) — 2026-10-04
- Archetyp: Backend / integracja z operatorem płatności
- Stawka: wysoka
- Niepewność: wysoka — zachowanie harmonogramów i zmian ilości u operatora sprawdzał spike BE-0
- Wykonawca (linia / model / native effort): Claude / Opus 5.5 / `xhigh` (`wykonawca-opus`)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh`, `-Access read`
- Dopuszczone alternatywy: przy CZERWONYM Spark `xhigh` albo czekanie
- Powód wyboru: twarda bramka (płatności)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ZIELONY → CZERWONY 16:39 (hook, 95 % okna 5 h; poprawki czekały na reset); Spark nieznany
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: wymagane korekty
- Rundy korekt: 2 (luki testów po recenzji; strażnik końca okresu w planowaniu)
- Czas do akceptacji: ok. 6 h zegarowo (z oknem CZERWONYM)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): recenzja 1 — poprawny 0,8, 2×P2 (luki testów) + 3×P3 potwierdzone; recenzja poprawek wspólna z BE-3b (zob. 1603-BE-3a/3b)
- Defekty po odbiorze: brak (stan na 2026-10-05)
- Wymagane testy i dowody: build 0/0, testy BE zielone; przebieg w trybie testowym operatora

### 1603-BE-3a/3b (odczyt, podgląd ceny, zaplanowana zmiana) — 2026-10-04
- Archetyp: Backend API / zapytania i komendy z niezmiennikiem
- Stawka: wysoka — wycena dopłaty i spójność harmonogramu z operatorem
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Claude / Opus 5.5 / `xhigh` (`wykonawca-opus`); testy API: Claude / Sonnet 5.5 / `medium` (`tester`)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh`, `-Access read`
- Dopuszczone alternatywy: przy CZERWONYM Spark `xhigh` albo czekanie
- Powód wyboru: twarda bramka; testy bez niezmiennika do `tester`
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostatni odczyt ZIELONY (23 %/21 %), od 19:25 nieznany (endpoint hooka nie odpowiadał); Spark nieznany
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: 3a — przekazanie po strażniku kontekstu (zrobiona tylko trwałość), 3a-3 drugi raz przy 306 tys. w spójnym stanie; 3b — wymagane korekty
- Rundy korekt: 3a — 0 (2 kontynuacje); 3b — 3
- Czas do akceptacji: ok. 4 h (18:59 → 22:54)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 3a — poprawny 0,85, 1×P2 (miejsce odczytu zegara) + P3 potwierdzone; 3a-3 — nic powyżej P3; 3b — 1×P2 (CAS nie sprawdzał bieżącego okresu) + 2×P3 potwierdzone; poprawki 3b i BE-2 — „niepoprawny” 0,72: 1×P1 (kontrola końca okresu przed zapisem) + 1×P2 potwierdzone; kolejna — poprawny, 1×P2 przyjęte jako utwardzenie + 4×P3 (3 bez zmian, 1 w innej postaci); 0 fałszywych P0/P1
- Defekty po odbiorze: brak (stan na 2026-10-05)
- Wymagane testy i dowody: build 0/0, pełne testy BE po każdym kroku, czerwone mutacje warunków CAS
- Uwaga dla przeglądu: dwa przebiegi oparły się o strażnika kontekstu — briefy BE ok. 15 kB były za duże

### 1603-BE-3c/3d (rozliczenie dopłaty, odczyt i przerwanie zlecenia) — 2026-10-05
- Archetyp: Backend / transakcja rozliczenia (naliczanie wartości, zwroty, współbieżność)
- Stawka: krytyczna — pieniądze klienta i opłacone miejsca, „dokładnie raz”
- Niepewność: wysoka
- Wykonawca (linia / model / native effort): Claude / Opus 5.5 / `xhigh` (`wykonawca-opus`); testy na bazie: Claude / Sonnet 5.5 / `medium` (`tester`)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh`, `-Access read`
- Dopuszczone alternatywy: przy CZERWONYM Spark `xhigh` albo czekanie
- Powód wyboru: twarda bramka i współbieżność
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ŻÓŁTY (hook, 81 % okna 5 h, 2026-10-04 23:20); Spark nieznany
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: 3c-1 wymagane korekty; 3c-2a przyjęte z 2 ryzykami zgłoszonymi przez wykonawcę; 3c-3a, 3c-3b i 3d przyjęte bez zmian kodu
- Rundy korekt: 3 (3c-1-fix; 3c-2a-fix — typ dat i kolejność przywracania; poprawki testów 3c-4) plus 1 runda testów w 3d
- Czas do akceptacji: ok. 5 h (21:53 → 02:57)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 3c-1 — „niepoprawny” 0,85: 1×P1 + 1×P2 + 2×P3 potwierdzone; 3c-2b — poprawny 0,9: 1×P2 (luka testów); 3c-3a — poprawny 0,85: 1×P2 (luka testów); 3c-3b — poprawny 0,85, 3 znaleziska przeniesione (P2 do BE-4b); fala testów — poprawny 0,8: 3×P2 + 5×P3 potwierdzone; 3d — poprawny, 2 luki testów, 3×P3 (1 odrzucone); 0 fałszywych P0/P1
- Defekty po odbiorze: bramka końcowa — P0 w styku z usuwaniem konta (zob. 1603-BE-4)
- Wymagane testy i dowody: równoległe rozliczenie tego samego zlecenia ×20 na prawdziwej bazie, czerwone mutacje, przywrócenie hashy plików produkcyjnych po mutacjach

### 1603-BE-3e (start płatności u operatora) — 2026-10-05
- Archetyp: Backend / integracja płatności (idempotencja, osierocone sesje)
- Stawka: wysoka
- Niepewność: wysoka — reguły idempotencji operatora
- Wykonawca (linia / model / native effort): Claude / Opus 5.5 / `xhigh` (`wykonawca-opus`)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh`, `-Access read`
- Dopuszczone alternatywy: przy CZERWONYM Spark `xhigh` albo czekanie
- Powód wyboru: twarda bramka (płatności)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ŻÓŁTY (hook, 2026-10-05 noc); Spark nieznany
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: przekazanie bez kodu — kontekst zużyty na rozpoznanie; raport obalił przesłankę briefu (operator odrzuca ponowiony klucz idempotencji przy innych parametrach)
- Rundy korekt: 4 (C2-fix, C3-fix, C2-fix-2, C2-fix-3) po 3 częściach C1–C3
- Czas do akceptacji: ok. 2 h 45 min (02:57 → 05:44)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): kolejne recenzje części i poprawek; ostatnia — poprawny 0,85, 8 ścieżek prześledzonych, 3×P3 potwierdzone; 0 fałszywych P0/P1
- Defekty po odbiorze: bramka końcowa — P1 obniżone do P2 (ponowne „Zapłać” przy opłaconej stronie zwracało błąd przed rozliczeniem)
- Wymagane testy i dowody: build 0/0, pełne testy BE, testy API na prawdziwej bazie (jedna płatność i jedna faktura przy ponownych kliknięciach)

### 1603-BE-4 (webhooki dopłaty, przegląd okresowy, domykacz sesji) — 2026-10-05
- Archetyp: Backend / zdarzenia asynchroniczne i usługa w tle
- Stawka: krytyczna — każda opłacona sesja musi skończyć się skutkiem albo alarmem
- Niepewność: wysoka
- Wykonawca (linia / model / native effort): Claude / Opus 5.5 / `xhigh` (`wykonawca-opus`); testy: Claude / Sonnet 5.5 / `medium` (`tester`)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh` (poprawki drobne `high`), `-Access read`
- Dopuszczone alternatywy: przy CZERWONYM Spark `xhigh` albo czekanie
- Powód wyboru: twarda bramka
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ŻÓŁTY (hook, 2026-10-05 rano); Spark nieznany
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: 4a wymagane korekty; 4b-1 przekazanie bez kodu (kontekst zużyty na rozpoznanie, 7 pytań rozstrzygniętych przez architekta)
- Rundy korekt: 4a — 2; 4b — 1 (eskalacja w przeglądzie okresowym) plus paczka testów przed bramką
- Czas do akceptacji: ok. 4 h (04:36 → ok. 08:40)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 4a — przyjęte poprawki (opłacona sesja zawsze kończy się skutkiem albo alarmem); 4a-fix — poprawny 0,85, 1×P2 (fałszywy alarm krytyczny) potwierdzone; 4a-fix-2 — kod poprawny, uwagi tylko do komentarzy i testów; 4b-1a — 1×P1 fałszywe (pomylona metoda, obalone jednym grepem), pozostałe przyjęte do paczki testów
- Defekty po odbiorze: bramka końcowa — P0 (usunięcie konta równolegle z rozliczeniem tej samej opłaconej strony mogło zostawić miejsca bez zwrotu); naprawione w G-1B
- Wymagane testy i dowody: build 0/0, pełne testy BE, czerwone mutacje cofające poprawki
- Uwaga dla przeglądu: trzeci przebieg BE, który zużył kontekst na rozpoznanie — rozpoznanie ścieżek przenoszę do `zwiadowca` przed briefem

### 1603-FE-2 (kroki liczby miejsc i okresu, próba A/B, ramię A) — 2026-10-04
- Archetyp: Frontend UI / Figma
- Stawka: średnia — ekran funkcji wysokiej stawki bez niezmiennika
- Niepewność: niska
- Wykonawca (linia / model / native effort): Claude / Sonnet 5.5 / `high` (`wykonawca`)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh`, `-Access read` (stały recenzent próby)
- Dopuszczone alternatywy: ramię B próby (`wykonawca-opus-medium`); Codex z Figmą niepotwierdzony
- Powód wyboru: ramię przydzielone przed briefem (próba A/B, reguła 14)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany, ZIELONY (hook, 2026-10-04 15:00)
- Pewność decyzji: niska (próba)
- Wynik pierwszego podejścia: wymagane korekty (odstępstwo od wzorca pola liczby)
- Rundy korekt: 2
- Czas do akceptacji: ok. 30 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): poprawny, 5×P3 potwierdzone, 0 odrzuconych
- Defekty po odbiorze: brak
- Wymagane testy i dowody: eslint/prettier/`ng test --include` wykonawcy; pełna walidacja fali i `browser-check`

### 1603-FE-4 (bloki warunkowe i wynik, ramię A) — 2026-10-04
- Archetyp: Frontend UI / Figma
- Stawka: średnia
- Niepewność: niska
- Wykonawca (linia / model / native effort): Claude / Sonnet 5.5 / `high` (`wykonawca`)
- Recenzent (linia / model / native effort): Spark / `xhigh`, `-Access read` (stały recenzent próby)
- Dopuszczone alternatywy: ramię B próby
- Powód wyboru: ramię A wg naprzemienności
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ZIELONY (hook, 2026-10-04 15:00)
- Pewność decyzji: niska (próba)
- Wynik pierwszego podejścia: wymagane korekty
- Rundy korekt: 1
- Czas do akceptacji: ok. 20 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): poprawny, 1×P3 (luka testu liczby mnogiej) potwierdzone
- Defekty po odbiorze: brak
- Wymagane testy i dowody: jak FE-2

### 1603-FE-7a (wejścia na zakładce Konto, ramię A) — 2026-10-04
- Archetyp: Frontend UI / Figma
- Stawka: średnia
- Niepewność: średnia — powrót z płatności i podmiana arkuszy
- Wykonawca (linia / model / native effort): Claude / Sonnet 5.5 / `high` (`wykonawca`)
- Recenzent (linia / model / native effort): Spark / `xhigh`, `-Access read` (stały recenzent próby)
- Dopuszczone alternatywy: ramię B próby
- Powód wyboru: ramię A wg naprzemienności
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ZIELONY 15:44, CZERWONY od 16:39 (hook); poprawki po resecie
- Pewność decyzji: niska (próba)
- Wynik pierwszego podejścia: wymagane korekty
- Rundy korekt: 2 (poprawki z recenzji; przekroczony budżet stylów z walidacji fali → wydzielenie komponentu)
- Czas do akceptacji: ok. 3,5 h zegarowo (z oknem CZERWONYM)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1×P2 obniżone do P3 (nieprawdziwy komentarz o nakładkach) + 4×P3 potwierdzone, 1×P3 odrzucone; plus 1 defekt z walidacji fali (budżet stylów)
- Defekty po odbiorze: brak
- Wymagane testy i dowody: jak FE-2; build bez nowego ostrzeżenia budżetu

### 1603-FE-3 (podsumowanie, wiersz faktury, pasek zaufania, ramię B) — 2026-10-04
- Archetyp: Frontend UI / Figma
- Stawka: średnia
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Claude / Opus 5.5 / `medium` (`wykonawca-opus-medium`)
- Recenzent (linia / model / native effort): Spark / `xhigh`, `-Access read` (stały recenzent próby)
- Dopuszczone alternatywy: ramię A próby
- Powód wyboru: ramię B wg naprzemienności
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ZIELONY (hook, 2026-10-04 15:00)
- Pewność decyzji: niska (próba)
- Wynik pierwszego podejścia: wymagane korekty
- Rundy korekt: 1 (2×P3 z recenzji i decyzje architekta po raporcie)
- Czas do akceptacji: ok. 40 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): poprawny, 2×P3 potwierdzone
- Defekty po odbiorze: bramka końcowa — 1×P2 w wierszu faktury (utrata edycji przy przeliczaniu), poprawione w G-1F
- Wymagane testy i dowody: jak FE-2

### 1603-FE-6 (kontener nakładki, ramię B) — 2026-10-04
- Archetyp: Frontend UI / Figma (kompozycja, stany, AXE)
- Stawka: średnia
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Claude / Opus 5.5 / `medium` (`wykonawca-opus-medium`)
- Recenzent (linia / model / native effort): Spark / `xhigh`, `-Access read` (stały recenzent próby)
- Dopuszczone alternatywy: ramię A próby
- Powód wyboru: ramię B wg naprzemienności
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ZIELONY (hook, 2026-10-04 15:29)
- Pewność decyzji: niska (próba)
- Wynik pierwszego podejścia: wymagane korekty (plus jedna poprawka briefu przez architekta w trakcie — błąd briefu, nie wykonawcy)
- Rundy korekt: 1
- Czas do akceptacji: ok. 30 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): poprawny 0,8, 3×P3 potwierdzone
- Defekty po odbiorze: bramka końcowa — 1×P2 („Zapłać” aktywne w trakcie zapisu danych do faktury), poprawione w G-1F
- Wymagane testy i dowody: jak FE-2; spec AXE kontenera

### 1603-FE-7b (wejście na zakładce Program, ramię B) — 2026-10-04
- Archetyp: Frontend UI / Figma
- Stawka: średnia
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Claude / Opus 5.5 / `medium` (`wykonawca-opus-medium`)
- Recenzent (linia / model / native effort): Spark / `xhigh`, `-Access read` (stały recenzent próby)
- Dopuszczone alternatywy: ramię A próby
- Powód wyboru: ramię B wg naprzemienności
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ZIELONY 15:44, CZERWONY od 16:39 (hook); poprawka po resecie
- Pewność decyzji: niska (próba)
- Wynik pierwszego podejścia: wymagane korekty
- Rundy korekt: 1
- Czas do akceptacji: ok. 3 h zegarowo (z oknem CZERWONYM)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1×P1 (zapasowy cel fokusu nie był fokusowalny) + 1×P2 + 1×P3 (luki testów) potwierdzone
- Defekty po odbiorze: brak
- Wymagane testy i dowody: jak FE-2

### 1603-K-1 (kreator a wynik po powrocie z płatności, dodatkowy brief ramienia B) — 2026-10-05
- Archetyp: Frontend / poprawka zachowania między komponentami
- Stawka: średnia
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Claude / Opus 5.5 / `medium` (`wykonawca-opus-medium`)
- Recenzent (linia / model / native effort): Spark / `xhigh`, `-Access read`
- Dopuszczone alternatywy: Claude / Sonnet 5.5 / `high` (`wykonawca`); Spark `high` `-Access write`
- Powód wyboru: odstępstwo — wysłane jako czwarty brief ramienia B, poza projektem próby (3 na ramię) i poza naprzemiennością; poza próbą agent jest wykluczony
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ŻÓŁTY (hook, 2026-10-05 09:30)
- Pewność decyzji: niska
- Wynik pierwszego podejścia: zaakceptowano
- Rundy korekt: 0
- Czas do akceptacji: ok. 20 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): „niepoprawny” 0,7; 1×P3 potwierdzone (przyjęte jako ryzyko bez zmiany), 2×P2 i 2 pozostałe odrzucone
- Defekty po odbiorze: brak
- Wymagane testy i dowody: czerwony test przed poprawką, pełna walidacja FE, `browser-check` scenariusz powrotu 4/4

### 1603-A-1 (audyt SCSS i refaktor wspólnych mixinów) — 2026-10-04
- Archetyp: Frontend / audyt i refaktor stylów
- Stawka: niska–średnia
- Niepewność: niska
- Wykonawca (linia / model / native effort): audyt Spark / `xhigh`, `-Access read`; refaktor Spark / `high`, `-Access write`
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (refaktor)
- Dopuszczone alternatywy: Claude / Sonnet 5.5 / `high`; Gemini `-Access write` (wtedy recenzent Spark)
- Powód wyboru: wcześniejszy pozytywny przebieg audytu SCSS na Sparku; osobna pula przy CZERWONYM Claude
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark i Gemini nieznany; Claude CZERWONY (hook, 16:39)
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: audyt — 0 naruszeń w 12 plikach; refaktor — wymagane korekty
- Rundy korekt: 1
- Czas do akceptacji: ok. 25 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): uwagi Gemini do mixinów potwierdzone i poprawione w A-1-fix-2
- Defekty po odbiorze: brak
- Wymagane testy i dowody: kompilacja 12 plików przed i po — CSS identyczny poza zamierzonymi zmianami; stylelint, prettier, eslint

### 1603-G-1 (bramka końcowa — odstępstwo od reguły 6) — 2026-10-05
- Archetyp: recenzja bramki końcowej (cały diff BE i FE funkcji wysokiej stawki)
- Stawka: krytyczna
- Niepewność: wysoka
- Wykonawca (linia / model / native effort): nie dotyczy (recenzja)
- Recenzent (linia / model / native effort): plan — Codex / `gpt-6-astra` / `max` ∥ `gpt-6.1-sol` / `max` (`-Mode review`); wykonane — Spark / `muse-spark-1.3-contributor` / `max`, `-Access read`, BE i FE równolegle
- Dopuszczone alternatywy: czekanie na reset puli Plus (reguła 6 nie dopuszcza słabszej bramki)
- Powód wyboru: Astra i Sol przerwane limitem Plus po ok. 13 min bez wyniku; właściciel zdecydował o innym recenzencie zamiast czekania do 16:49
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex zablokowany (komunikat limitu wrappera, 2026-10-05 ok. 10:02); Spark nieznany
- Pewność decyzji: średnia (decyzja właściciela)
- Wynik pierwszego podejścia: oba werdykty „wymaga poprawek”
- Rundy korekt: nie dotyczy — poprawki w 1603-G-1-fix
- Czas do akceptacji: BE 13,9 min, FE 9,5 min przebiegu
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): BE — 1×P0, 1×P1 obniżone do P2 potwierdzone, 1×P2 przyjęte jako ryzyko; FE — 1×P1, 2×P2 potwierdzone; 0 fałszywych
- Defekty po odbiorze: brak (stan na 2026-10-05; PRE jeszcze niewdrożone)
- Wymagane testy i dowody: każde znalezisko sprawdzone w kodzie i dokumentacji przez architekta
- Uwaga dla przeglądu: porównanie Astra/Sol z reguły 6 nie odbyło się; przechodzi na następną funkcję wysokiej stawki. Dwie bramki Codexa równolegle na dużym diffie wyczerpały okno Plus

### 1603-G-1-fix (poprawki po bramce, BE i FE) — 2026-10-05
- Archetyp: Backend + Frontend / poprawki niezmiennika płatności
- Stawka: krytyczna
- Niepewność: wysoka
- Wykonawca (linia / model / native effort): Claude / Opus 5.5 / `xhigh` (`wykonawca-opus`) dla plików niezmiennika; Spark / `high` `-Access write` dla podziału specu i resetu wiersza faktury (bez niezmiennika)
- Recenzent (linia / model / native effort): Spark / `xhigh`, `-Access read` (autor Claude); Gemini / `gemini-3.8-flash-high`, `-Access read` (autor Spark)
- Dopuszczone alternatywy: przy CZERWONYM Spark `xhigh` albo czekanie (pliki niezmiennika)
- Powód wyboru: twarda bramka; drobne pliki bez niezmiennika do osobnej puli
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ŻÓŁTY (hook, 2026-10-05 ok. 12:00); Spark i Gemini nieznany
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: G-1F — zaakceptowano; G-1B A–C — recenzja znalazła P1 wprowadzone przez poprawkę P0
- Rundy korekt: BE 3 (poprawka D i dwie korekty D); FE 2 (reset wiersza faktury — pierwsze podejście zatrzymane słusznie przez wykonawcę, bo przesłanka architekta była błędna)
- Czas do akceptacji: ok. 2 h (11:55 → 13:50)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): BE — 1×P1 (nieudane wygaszenie gubiło ujawnioną zapłatę) + 2×P3 potwierdzone; BE D — „niepoprawny” 0,8: P1 naprawione poprawnie, 1×P2 potwierdzone, 1×P3 jako dług; FE — 2×P2 (Gemini) potwierdzone, 1×P3 odrzucone, końcowa recenzja poprawny 0,98; 0 fałszywych P0/P1
- Defekty po odbiorze: brak (stan na 2026-10-05)
- Wymagane testy i dowody: czerwony test przed każdą zmianą produkcji; FE 4124/4124, BE 5043/0/0 (build Release od zera)

### 1603-gate-FE (decyzje bramy potwierdzenia we FE) — 2026-10-05
- Archetyp: Frontend / zachowanie nakładki i kreatora
- Stawka: średnia — blokada płatności przy edycji danych do faktury
- Niepewność: niska
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `high`, `-Access write`
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read`
- Dopuszczone alternatywy: Claude / Sonnet 5.5 / `high` (`wykonawca`)
- Powód wyboru: zmiana bez pliku niezmiennika (blokada interfejsu, nie rozliczenia); Claude ŻÓŁTY
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ŻÓŁTY (hook, 2026-10-05 13:28); Spark i Gemini nieznany
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: wymagane korekty (P2 wynikało z błędnej przesłanki briefu)
- Rundy korekt: 1
- Czas do akceptacji: ok. 25 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1×P2 potwierdzone (podpowiedź blokady znikała przy przeliczaniu), 1×P3 odrzucone; 0 fałszywych P0/P1
- Defekty po odbiorze: brak
- Wymagane testy i dowody: czerwony test, 418/418 testów katalogu, pełna walidacja FE 4131/4131

### 1603-Q (przypadki QA Sphere, Q-1 + Q-2) — 2026-10-05
- Archetyp: Testy manualne / QA Sphere
- Stawka: średnia — przypadki prowadzą testera przez płatność
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh`, `-Access write` (procedura `qasphere-test-generator`)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read`
- Dopuszczone alternatywy: Gemini `-Access write` (wtedy recenzent Spark)
- Powód wyboru: wiążąca procedura pomocniczego skilla
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark i Gemini nieznany
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: wymagane korekty
- Rundy korekt: Q-1 — 2; Q-2 — 1
- Czas do akceptacji: Q-1 ok. 2 h; Q-2 ok. 30 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): Q-2 — 1×P1 (SQL bez apostrofów) + 3×P2 (zbędny skrypt z błędnej przesłanki, liczba pojedyncza, brak sprawdzenia „Dokończ konfigurację”) + 1×P3 potwierdzone; Q-1 — poprawki w dwóch rundach, liczby w notatkach briefów
- Defekty po odbiorze: brak (stan na 2026-10-05)
- Wymagane testy i dowody: `qas.py lint` 0 błędów, publikacja i `verify` (znormalizowany) bez realnych różnic; 37 przypadków + 3 aktualizacje

### 1603-F (makiety Figma: stany nakładki, wejścia w Ustawieniach, poprawki) — 2026-10-04…05
- Archetyp: Figma
- Stawka: niska–średnia
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Claude / Sonnet 5.5 / `high` (`wykonawca`)
- Recenzent (linia / model / native effort): architekt przez zrzut ekranu (Spark i Gemini bez Figmy; inna rodzina z Figma MCP niepotwierdzona) — poza pomiarem próby A/B
- Dopuszczone alternatywy: `wykonawca-opus-medium` (tylko w próbie); Codex z Figmą niepotwierdzony
- Powód wyboru: wymagany faktyczny Figma MCP
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ZIELONY 2026-10-04, ŻÓŁTY 2026-10-05 (hook)
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: F-1a wymagane korekty tekstów; F-1b zaakceptowano; usunięcie wyboru typu kupującego — pierwsze podejście pominęło tablicę stanów
- Rundy korekt: F-1a 1; F-2 0; usunięcie typu kupującego 1
- Czas do akceptacji: F-1 ok. 45 min; F-2 ok. 10 min; typ kupującego ok. 10 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): zrzuty architekta — braki zakresu wykryte i zwrócone
- Defekty po odbiorze: brak
- Wymagane testy i dowody: `get_screenshot` węzłów desktop/mobile oglądane przez architekta

### 1603-P-1 (płatność u operatora w trybie testowym, ręczne odtworzenie) — 2026-10-05
- Archetyp: weryfikacja end-to-end (ręczne odtworzenie, Playwright MCP, bez testów E2E w repo)
- Stawka: wysoka — dowód „kwota pokazana = kwota pobrana”
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh`, `-Access write` (Playwright MCP); narzędzia lokalne E-1: Claude / Sonnet 5.5 / `high` (`wykonawca`)
- Recenzent (linia / model / native effort): nie dotyczy — brief dowodowy, artefakty zwalidowane przez architekta (baza, obiekty operatora)
- Dopuszczone alternatywy: Gemini z Playwright MCP; Codex z potwierdzonym MCP
- Powód wyboru: potwierdzony Playwright MCP, osobna pula, subagenci Claude'a nie robią zrzutów
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark nieznany, 2026-10-05 09:15
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowano
- Rundy korekt: 0
- Czas do akceptacji: ok. 10 min przebiegu
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): nie dotyczy
- Defekty po odbiorze: brak
- Wymagane testy i dowody: przerwana → `CANCELLED` i sesja wygaszona; zapłata kartą testową → C1–C7 PASS (kwota sesji = PaymentIntent = wiersz płatności = faktura `PENDING`; `quantity` = liczba miejsc); harmonogram dwufazowy i `release`

### BE-1 (BeautyEffect: migawki źródeł E1–E2 i szkielet dokumentacji S1) — 2026-10-05
- Archetyp: dokumentacja produktu — ekstrakcja źródeł i szkielet repo dokumentacji
- Stawka: niska–średnia (materiał dowodowy dla dalszych fal)
- Niepewność: średnia (Booksy za JS-em, stara strona z szablonu sieci)
- Wykonawca (linia / model / native effort): E1 Spark / `muse-spark-1.3-contributor` / `high`; E2 Spark / `xhigh` (Booksy, Playwright MCP); S1 Gemini / `gemini-3.8-flash-high`
- Recenzent (linia / model / native effort): architekt (kontrola linków i front matter skryptem); merytorycznie w recenzjach fal 2a/2b
- Dopuszczone alternatywy: Codex `gpt-6.1-sol` (Playwright niepotwierdzony)
- Powód wyboru: rozłączne cele, Playwright MCP u Sparka, osobne pule; Claude ŻÓŁTY
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook ŻÓŁTY), zewnętrzni nieznany — 2026-10-05 ok. 17:05
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowano po walidacji architekta
- Rundy korekt: brak osobnych; drobne usterki migawek wyszły w recenzjach fal (słowo cyrylicą w migawce Booksy, poprawione przez architekta)
- Czas do akceptacji: w ramach fali 1 (ok. 20 min)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): nie dotyczy
- Defekty po odbiorze: 1 drobny (znak cyrylicy w migawce Spark)
- Wymagane testy i dowody: skrypt linków/ID/front matter; odczyt migawek

### BE-R1 (BeautyEffect: research wyświetlania postów IG/FB) — 2026-10-05
- Archetyp: research techniczny
- Stawka: średnia (decyzja o bezobsługowości strony)
- Niepewność: wysoka (API Meta, zasady osadzania)
- Wykonawca (linia / model / native effort): R1 Codex / `gpt-6.1-sol` / `high`; R1b Spark / `xhigh` z Playwright MCP (odczyt na żywo)
- Recenzent (linia / model / native effort): architekt — zestawienie dwóch niezależnych rodzin
- Dopuszczone alternatywy: Gemini `high` (miękki sygnał negatywny z 2026-09-24)
- Powód wyboru: dwie rodziny dla krzyżowej kontroli źródeł; Spark z przeglądarką
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): nieznany (wrappery), 2026-10-05 17:11
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowano; wnioski zgodne (statyczne odnośniki domyślnie, Graph API tylko przy stałej opiece technicznej)
- Rundy korekt: 0
- Czas do akceptacji: ok. 25 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): nie dotyczy
- Defekty po odbiorze: brak
- Wymagane testy i dowody: URL-e przy twierdzeniach, wyrywkowe sprawdzenie

### BE-2a (BeautyEffect: produkt, wymagania, integracje, dokumenty prawne + recenzje i korekty) — 2026-10-05
- Archetyp: dokumentacja produktu — redakcja z migawek
- Stawka: średnia (dokumenty prawne i zasady wizyt widoczne dla klientek)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): B-PROD Spark `xhigh`; B-WP-INT Gemini `flash-high`; B-PRAWO Spark `high`; korekty K-A Spark `xhigh`, K-B Gemini `flash-high`
- Recenzent (linia / model / native effort): R-2a-A Codex `gpt-6.1-sol` `high` (tylko odczyt, autor Spark); R-2a-B Spark `xhigh` `-Access read` (autor Gemini)
- Dopuszczone alternatywy: Codex jako autor (pula Plus oszczędzana na research)
- Powód wyboru: rozłączne zbiory plików, recenzent innej rodziny per autor; Claude ŻÓŁTY
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook), zewnętrzni nieznany — 2026-10-05 17:26
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: wymagane korekty u obu autorów
- Rundy korekt: 1 (K-A, K-B)
- Czas do akceptacji: ok. 50 min od startu fali
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): potwierdzone m.in. twierdzenie bez pokrycia o dominacji telefonów i brak warunkowości regulaminu; odrzucone: P1 „motyw ciemny bez decyzji” (standard FE + decyzja właściciela), P3 rzekoma niezgodność ID
- Defekty po odbiorze: 1 nieoznaczone założenie (tryb aktualizacji danych salonu) — zneutralizowane przez architekta
- Wymagane testy i dowody: skrypt linków/ID; grep cen, „24/7”, „bezpłatn”

### BE-2b (BeautyEffect: specyfikacje stron — powłoka, główna, informacyjne, oferta, strony medyczne + recenzje i korekty) — 2026-10-05
- Archetyp: dokumentacja interfejsu (treść dosłowna, bez opisu wyglądu)
- Stawka: średnia; wyższa dla stron z elementem medycznym (obietnice efektu, przeciwwskazania)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): B-UI-1a i 2a Spark `xhigh`; B-UI-1b Gemini `flash-high`; B-UI-2b Codex `gpt-6.1-sol` `high`; korekty K2-A Spark, K2-B Gemini, K2-C Codex (ci sami autorzy)
- Recenzent (linia / model / native effort): R-2b-A Gemini `flash-high` `-Access read` (autor Spark); R-2b-B i R-2b-C Spark `xhigh` `-Access read` (autorzy Gemini, Codex)
- Dopuszczone alternatywy: Codex jako recenzent Sparka/Gemini (pula Plus zajęta autorstwem 2b i researchem)
- Powód wyboru: stawka stron medycznych → Codex `high`; reszta rozłącznie na Spark/Gemini
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook), zewnętrzni nieznany — 2026-10-05 18:10
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: korekty u wszystkich; najwięcej faktów spoza migawek u Gemini (lista oczekujących, „stylistka”, „sterylne”, ważność kart Booksy, porady przed wizytą), u Sparka P0 przy pedicure, u Codexa brak reguły publikacji niekompletnych opisów medycznych (zero obietnic efektu)
- Rundy korekt: 1 + drobne poprawki architekta (liczby w spisie punktów regulaminu, odwołania do nazw briefów w dokumentach, dwa zdania)
- Czas do akceptacji: ok. 45 min od startu fali
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): potwierdzone P0/P1 we wszystkich trzech zestawach; R-2b-A Gemini za pierwszym razem padł (próba polecenia powłoki w trybie odczytu) — ponowienie z zakazem powłoki i pełnymi ścieżkami przeszło; jeden P0 wynikał z błędu briefu architekta (prośba o treść nieistniejącego wariantu)
- Defekty po odbiorze: Gemini w raporcie przywołał nieistniejącą kwestię otwartą (tylko raport, nie pliki)
- Wymagane testy i dowody: skrypt linków/ID (0 martwych na 119 plików); grep cen, danych salonu, „Wam”, cyrylicy, odwołań do briefów

### BE-RK (BeautyEffect: research kolorystyki — dowody i rynek) — 2026-10-05
- Archetyp: research (przegląd dowodów z oceną siły; skan rynku z odczytem kolorów z kodu stron)
- Stawka: średnia (tożsamość wizualna, decyzja właściciela)
- Niepewność: wysoka (brak badań dla grupy docelowej i rezerwacji)
- Wykonawca (linia / model / native effort): R-K1 Codex / `gpt-6.1-sol` / `xhigh`; R-K2 Spark / `muse-spark-1.3-contributor` / `xhigh`
- Recenzent (linia / model / native effort): architekt — wyrywkowa weryfikacja źródeł (WebAIM Million 2026, zmienne CSS K Studio) i krzyżowanie wniosków dwóch rodzin
- Dopuszczone alternatywy: Gemini `high` do skanu rynku
- Powód wyboru: rozłączne pytania (dowody / rynek), dwie rodziny; Codex `xhigh` przy ocenie siły dowodów
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): nieznany (wrappery), 2026-10-05 18:05
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowano; R-K2 z jawnymi lukami (brak Playwright w przebiegu → część kolorów CTA „nie odczytano”, 403 u części serwisów)
- Rundy korekt: 0
- Czas do akceptacji: R-K1 ok. 38 min, R-K2 ok. 35 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): sprawdzone próbki zgodne; architekt dodał wniosek pominięty przez R-K2 (kierunek „śliwka + greige” to paleta jedynego lokalnego konkurenta z własną stroną)
- Defekty po odbiorze: brak
- Wymagane testy i dowody: URL przy każdym twierdzeniu, metoda odczytu HEX, kontrast WCAG policzony skryptem architekta (3 kierunki × 40 par, 0 niespełnionych)

### BE-3 (BeautyEffect: identyfikacja wizualna + system kolorów; wspólny standard struktury dokumentacji) — 2026-10-05
- Archetyp: dokumentacja produktowa z liczbami (tabele HEX/kontrastów przepisane z generatora architekta) + decyzja przekrojowa dla wielu repo dokumentacji
- Stawka: średnia (tożsamość wizualna; decyzja wiążąca wszystkie projekty)
- Niepewność: niska (decyzje i liczby podane w briefie)
- Wykonawca (linia / model / native effort): K3-A Spark / `muse-spark-1.3-contributor` / `xhigh`; K3-B Gemini / `gemini-3.8-flash-high`; korekty K3-A2 Spark / `high`, K3-B2 Gemini / `gemini-3.8-flash-high`
- Recenzent (linia / model / native effort): R-3 Codex / `gpt-6.1-sol` / `high` (`-Mode review`, obie rodziny autorów różne od Codexa)
- Dopuszczone alternatywy: K3-A — Gemini `high`; K3-B — Spark `xhigh`; R-3 — Spark `xhigh` tylko dla części Gemini
- Powód wyboru: rozłączne pliki (projekt / wspólne + Zebrani), równolegle; jeden recenzent spoza obu rodzin autorów zamiast dwóch
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude zablokowany (hook CZERWONY, 5 h ~88 %), Spark/Gemini/Codex nieznany (wrappery), 2026-10-05 17:35
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowano z poprawkami; liczby HEX/kontrastów zgodne z tabelami (sprawdzone skryptem)
- Rundy korekt: 1 (K3-A2 1,5 min, K3-B2 5 min)
- Czas do akceptacji: ok. 20 min (K3-A 6 min, K3-B 3 min, R-3 6 min, korekty)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 5 × P2 potwierdzone, 0 odrzuconych — sprzeczność „śliwka tylko w CTA” z tłem sekcji `sliwka-50/950`; brak `zrodlo`/`referencyjny` w instrukcji Zebrani; przesadzone „jedyny salon z własną stroną” (błąd architekta przeniesiony do DEC); niespójne ID historycznej DEC; wspólna DEC rozstrzygała model kopii instrukcji bez decyzji właściciela
- Defekty po odbiorze: brak
- Wymagane testy i dowody: skrypt linków/ID (0 martwych), porównanie skryptowe HEX/kontrastów z tabelami generatora, diff słowny plików Zebrani (tylko dopisania)

### BE-4 (BeautyEffect: rozstrzygnięcia KO — opisy medyczne z Booksy, zasady wizyt, dane firmy, domena) — 2026-10-05
- Archetyp: wprowadzenie decyzji właściciela w wiele powiązanych dokumentów (przeniesienie treści 1:1 ze źródła + wycofanie dokumentu i jego odnośników)
- Stawka: średnia (treści publiczne, dane firmy, zasady kaucji)
- Niepewność: niska (decyzje dosłowne)
- Wykonawca (linia / model / native effort): K4-A i K4-B Spark / `muse-spark-1.3-contributor` / `xhigh`; korekta K4-C Spark / `high`
- Recenzent (linia / model / native effort): R-4 Codex / `gpt-6.1-sol` / `high` (`-Mode review`)
- Dopuszczone alternatywy: wykonawca — Gemini `high` (zajęty K5 na tym samym repo); recenzent — Gemini `-Access read` (zajęty)
- Powód wyboru: dwa rozłączne zbiory plików na jednej linii równolegle; recenzent spoza rodziny autora, z dobrym wynikiem R-3 na tej samej dokumentacji
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude zablokowany (hook CZERWONY, 5 h 88–92 %), Spark/Codex nieznany (wrappery), 2026-10-05 17:44
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowano z poprawkami; architekt przed recenzją dopisał 2 brakujące spójności (wyjątek od zakazu obietnic w UI-OFERTA, nieaktualne odwołanie w PB-UMOWIENIE-WIZYTY)
- Rundy korekt: 1 (K4-C, 7,5 min)
- Czas do akceptacji: ok. 30 min (K4-A 7,6 min, K4-B 9 min, R-4 7,4 min, K4-C 7,5 min)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 7 × P2 + 1 × P3 potwierdzone, 0 odrzuconych — zasady VIP tylko z Instagrama mimo „Booksy jedynym źródłem”; „Regulamin” w stopce 3 stron; sprzeczny stan karty e-mail; pominięte „znaczące spóźnienie” z Booksy; warunki włosów uogólnione na Afro&loki; skróty zmieniające sens bez oznaczenia do akceptacji; niezaznaczone zakazy sprzed rozstrzygnięcia KO; kotwice ASCII do nagłówków z polskimi literami (skrypt architekta znalazł łącznie 26 martwych kotwic, recenzent wskazał 4 typy)
- Defekty po odbiorze: brak
- Wymagane testy i dowody: skrypt linków/ID (0 martwych), nowy skrypt kotwic wg slugów GitHub (96 sprawdzonych, 0 martwych), grep VIP/Regulamin/warunkowości e-maila

### BE-5 (BeautyEffect: porządek 185 zdjęć i filmów salonu + inwentarz) — 2026-10-05
- Archetyp: praca na plikach binarnych z oglądem obrazów (klasyfikacja, nazwy, duplikaty, inwentarz z tekstem alternatywnym)
- Stawka: średnia (wizerunek osób — oznaczenie twarzy decyduje o potrzebie zgody)
- Niepewność: średnia (klasyfikacja z oglądu)
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` (multimodalny ogląd; sam rozdzielił pracę na 6 podagentów)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — architekt: walidacja skryptowa (155 zdjęć + 29 filmów + 1 duplikat = 185, nazwy 1:1 z dyskiem, linki, tekst alternatywny ≤ 120 znaków, próbka wierszy); odstępstwo od reguły 13, bo recenzja wymagałaby ponownego oglądu 184 plików — złagodzone dopiskiem w obu README, że oznaczenia twarzy i tekstu są pomocnicze i wymagają sprawdzenia przy wyborze pliku do publikacji
- Dopuszczone alternatywy: Spark `xhigh` (ogląd obrazów niepotwierdzony w tym wrapperze), Codex `gpt-6.1-sol` (porcje ≤ 5 plików — nieekonomiczne przy 185 plikach)
- Powód wyboru: multimodalność i duży wolumen plików na puli niezależnej od zablokowanego Claude'a
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude zablokowany (CZERWONY), Gemini nieznany (wrapper), 2026-10-05 17:51
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: przerwany przez architekta po ok. 20 min — wszystkie pliki przeniesione, inwentarze gotowe w katalogu roboczym, KO-WERSJA-JEZYKOWA rozstrzygnięta, ale worker utknął na usuwaniu pustego `photos/` blokowanego przez własny proces i zaczął wyliczać systemowe uchwyty (`ntdll`, `DuplicateHandle`) oraz próbował zmienić nazwę katalogu — ryzyko ingerencji w cudze procesy poza briefem; zostawił też plik roboczy w `Dokumentacja/tmp/` poza zakresem
- Rundy korekt: 0 (architekt dokończył mechanicznie: kopia inwentarzy 1:1, wpis w KO-MATERIALY-OD-WLASCICIELA, usunięcie pliku roboczego; `photos/` zniknął po zatrzymaniu workera)
- Czas do akceptacji: ok. 35 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): nie dotyczy (brak recenzji innej rodziny — patrz wyżej)
- Defekty po odbiorze: brak stwierdzonych
- Wymagane testy i dowody: bilans plików i nazw skryptem, brak klatek tymczasowych w repo, `.gitattributes` uzupełniony o `*.mp4` jako binarny. Wniosek do briefów: zakazać wprost operacji na procesach i uchwytach systemowych oraz plików roboczych w repo; niemożność usunięcia katalogu zgłaszać w raporcie

### BE-6 (BeautyEffectFE: szkielet workspace Angular 22 + recenzja + korekta) — 2026-10-05
- Archetyp: szkielet projektu FE na wzór istniejącego repo (konfiguracja, core, powłoka, pierwsza strona, testy AXE)
- Stawka: średnia (fundament wszystkich briefów FE; licencja PrimeUI jako sekret)
- Niepewność: niska–średnia (wzorzec ZebraniFE, nowe decyzje: tylko `public/`, tylko `pl`)
- Wykonawca (linia / model / native effort): FE-W1 Spark / `muse-spark-1.3-contributor` / `xhigh`; korekta K-FE1 Spark / `high`
- Recenzent (linia / model / native effort): R-FE1 Codex / `gpt-6.1-sol` / `high` (`-Mode review`) — po nieudanym Gemini `gemini-3.8-flash-high` `-Access read` (429, limit indywidualny, reset ok. 10 min)
- Dopuszczone alternatywy: wykonawca — Codex `gpt-6.1-sol` (porcje ≤ 5 plików, nieekonomiczne dla szkieletu ~60 plików), `wykonawca` Sonnet (Claude ŻÓŁTY); recenzent — Gemini (zablokowany 429)
- Powód wyboru: duży wolumen plików na puli niezależnej od Claude'a, pętla lint/test przez interop; recenzent spoza rodziny autora
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (ŻÓŁTY, tydzień 69 %), Spark/Codex nieznany (wrappery), Gemini zablokowany (429) 2026-10-05 20:16
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowano z poprawkami; architekt sam: `npm install`, `prettier --write` na 5 plikach, sonda reguły importów w obie strony
- Rundy korekt: 1 (K-FE1, 4 min)
- Czas do akceptacji: ok. 45 min (FE-W1 14,6 min, R-FE1 3,1 min, K-FE1 4 min, walidacja)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 5 × P2 potwierdzone, 0 odrzuconych — brak `license` w `providePrimeNG`; klucz `ERRORS.UNEXPECTED` nieobecny w `pl.json`; brak polskich tekstów PrimeNG; loader SSR czyta `dist` przed `src` w trybie deweloperskim; ścieżki loadera zależne od `process.cwd()` (odziedziczone ze wzorca)
- Defekty po odbiorze: brak; K-FE1 słusznie zgłosił 2 błędne założenia briefu (wierna kopia `primeng-translation.ts` nie kompiluje się bez `LanguageMode`; kopia nie daje polskich „Tak/Nie” w `confirm`) — przyjęte
- Wymagane testy i dowody: `npm run lint`, `format:check`, `npm test` (7/7), `npm run build` (prerender `/`), sonda `no-restricted-imports` (3 poziomy i przekroczenie obszaru → błąd)

### BE-7 (BeautyEffect: research typografii i wyglądu strony beauty — dowody, rynek, trendy 2026) — 2026-10-05
- Archetyp: research z adresem przy każdym twierdzeniu (dowody/normy vs przegląd rynku), równolegle 4 briefy
- Stawka: średnia (podstawa kierunku wizualnego i wyboru krojów przez właściciela)
- Niepewność: wysoka (trendy, brak danych lokalnych)
- Wykonawca (linia / model / native effort): R-T1 Codex / `gpt-6.1-sol` / `xhigh`; R-T2 Spark / `muse-spark-1.3-contributor` / `xhigh`; R-W1 Codex / `gpt-6.1-sol` / `high`; R-W2 Gemini / `gemini-3.8-flash-high`
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — architekt: kontrola wszystkich 49 adresów R-W1 (43 × 200, 6 blokuje boty), 3/3 twierdzeń próbki R-W1, 3/3 stron próbki R-W2 w kodzie (kroje, Booksy, Boulevard); odstępstwo od reguły 13 dla researchu referencyjnego bez wpływu na decyzje
- Dopuszczone alternatywy: R-W2 — Codex (pula Plus, już 2 briefy), Spark (zajęty R-T2); R-T1/R-W1 — Gemini (negatywny sygnał researchu z 2026-09-24)
- Powód wyboru: rozdział „dowody/normy” (Codex — dotąd rzetelne adresy) od „przeglądu wizualnego wielu stron” (Gemini/Spark — wolumen); cztery pule równolegle
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (ŻÓŁTY), Spark/Codex/Gemini nieznany (wrappery), 2026-10-05 20:00
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: R-T1 i R-T2 słusznie ZATRZYMANE na błędnym założeniu briefu („odbiorczynie głównie na telefonie” — dokumenty mówią: udział nieznany; brak kierunku DomSztuki w dokumentach; niezgodny front matter) — architekt poprawił 4 briefy i założył KO-KIERUNEK-WIZUALNY; R-W2 zaakceptowany z adnotacją (zmyślone HEX palety w sekcji kierunków); R-W1 zaakceptowany bez uwag; R-T2 bez Playwright MCP (kroje z deklarowanego `font-family`, nie z obliczonych stylów)
- Rundy korekt: 1 (ponowienie R-T1/R-T2 po zatrzymaniu; R-W2 — adnotacja architekta zamiast korekty)
- Czas do akceptacji: ok. 40 min (R-T1 1 + 11,5 min, R-T2 1,4 + 11,3 min, R-W2 13,8 min, R-W1 19 min, kontrola)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): nie dotyczy (brak recenzji innej rodziny); znalezisko architekta: R-W2 sekcja 6 — HEX i numery odcieni sprzeczne z AT-SYSTEM-KOLOROW-UI (P2, adnotacja w dokumencie)
- Defekty po odbiorze: brak stwierdzonych
- Wymagane testy i dowody: front matter i linki skryptem, status HTTP wszystkich adresów R-W1, próbki twierdzeń. Wniosek: klauzula STOP zadziałała 2/2 na błędzie architekta; Gemini w przeglądzie wizualnym rzetelny co do stron, ale dopisuje własne wartości palety — brief ma zabraniać podawania HEX spoza dokumentu

### 2370-D (trzy rewizje dokumentacji produktowej) — 2026-10-05
- Archetyp: dokumentacja produktowa / rewizje zatwierdzonych dokumentów
- Stawka: średnia (źródło prawdy dla funkcji wysokiej stawki)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `high`, `-Access write`
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read`
- Dopuszczone alternatywy: Gemini write (recenzent Spark); Claude `wykonawca` (Sonnet 5.5 `high`)
- Powód wyboru: tekstowy brief bez Figmy; lokalnie 1603-D przyjęte po 1 rundzie
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark i Gemini nieznany (brak odczytu zapasu, 2026-10-05 ok. 17:00)
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: wymagane korekty
- Rundy korekt: 1
- Czas do akceptacji: ok. 30 min (17:04 → ok. 17:35)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 4×P1 (sprzeczności fokusu na wąskim ekranie, awarii operatora, wejść do nakładki, karty programów) — potwierdzone, poprawione 7 punktami korekty; 0 fałszywych
- Defekty po odbiorze: brak
- Wymagane testy i dowody: diff trzech plików, kontrola front matter i dat rewizji przez architekta

### 2370-FE-i18n (klucze pl+en wariantu zaległości) — 2026-10-05
- Archetyp: Frontend i18n
- Stawka: niska
- Niepewność: niska
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `high`, `-Access write`
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read`
- Dopuszczone alternatywy: Gemini write (recenzent Spark); `mechanik` (Haiku `low`) — odrzucony przy ~40 kluczach z odmianą
- Powód wyboru: jak 1603-FE-1 (1 runda)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark i Gemini nieznany (2026-10-05 ok. 17:00)
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: wymagane korekty
- Rundy korekt: 1
- Czas do akceptacji: ok. 30 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1×P1 (odwrócony podmiot w ogólnym komunikacie EN) + 1×P2 potwierdzone, 2×P3 częściowo; dodatkowo odmiana liczebnika poprawiona przez architekta w korekcie; 0 fałszywych P0/P1
- Defekty po odbiorze: brak
- Wymagane testy i dowody: parytet liści pl/en, prettier, `git diff --numstat` (tylko dopiski)

### 2370-FE-1 (przepływ płatności zaległości, serwis i DTO — niezmiennik płatności) — 2026-10-05
- Archetyp: Frontend / logika przepływu płatności
- Stawka: wysoka (high-stakes)
- Niepewność: wysoka
- Wykonawca (linia / model / native effort): Claude / Opus 5.5 / `xhigh` (`wykonawca-opus`), korekta świeżym agentem tej samej linii
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh`, `-Access read` (dwie recenzje: przebiegu i korekty)
- Dopuszczone alternatywy: brak dla autora (pliki niezmiennika); recenzent alt. Gemini `flash-high`
- Powód wyboru: twarda bramka high-stakes; lokalnie 1603-FE-5
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook ŻÓŁTY, 2026-10-05 ok. 17:00); Spark nieznany
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: wymagane korekty (recenzja „niepoprawny”)
- Rundy korekt: 1
- Czas do akceptacji: ok. 1 h (17:04 → ok. 18:05)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 2×P1 (równoległe POST z dwóch instancji nakładki; `crypto.randomUUID` na nieszyfrowanym hoście), 2×P2, 3×P3 — potwierdzone, K1–K7; recenzja korekty 1×P3 (nieosiągalne, odnotowane); 0 fałszywych
- Defekty po odbiorze: bramka FE (Spark `max`): 1×P2 (brak przeładowania abonamentu po `Paid` z odpytywania przy wejściu spoza `Arrears`) + 1×P3 (komentarz 409 zamiast 422) w `arrears-payment-flow.ts` → G-FE-1
- Wymagane testy i dowody: Vitest przepływu (brak podwójnego POST, nowy `attemptId`, 3DS i odpytywanie, straż generacji), pełne FE 4329/4329

### 2370-FE-2a (wariant nakładki zaległości z Figmy) — 2026-10-05
- Archetyp: Frontend UI / Figma
- Stawka: średnia (ekran funkcji high-stakes bez niezmiennika)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Claude / Sonnet 5.5 / `high` (`wykonawca`), z Figma MCP
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh`, `-Access read`
- Dopuszczone alternatywy: Codex `gpt-6.1-sol` `high` z potwierdzonym Figma MCP (odrzucony — pula Plus na bramkę); recenzent alt. Gemini `flash-high`
- Powód wyboru: ekran z makiety; próba A/B zakończona (3:3) — linia Sonnet wg kryterium
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook ŻÓŁTY, 2026-10-05 ok. 17:40); Spark nieznany
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: wymagane korekty (recenzja „niepoprawny” 0,8)
- Rundy korekt: 1 (wspólna korekta FE-2, K1–K5 i K10)
- Czas do akceptacji: ok. 50 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1×P1 (fokus po „Zmień abonament” w stanie wyniku), 1×P2, 2×P3 — potwierdzone; 0 fałszywych
- Defekty po odbiorze: bramka FE (Spark `max`): 2×P3 (akcje w trakcie animacji zamykania; „Zmień” metodę gubi szkic danych do faktury) w `change-subscription.ts` → G-FE-1
- Wymagane testy i dowody: specy komponentów i AXE wariantu, `browser-check` matrix 2×2 dla `PastDue` i `Unpaid` (16/16, 0 błędów konsoli/sieci, zrzuty obejrzane)

### 2370-FE-2b (Ustawienia: „Opłać teraz”, przekazanie nakładek) — 2026-10-05
- Archetyp: Frontend UI / okablowanie
- Stawka: średnia
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Claude / Sonnet 5.5 / `high` (`wykonawca`)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read`
- Dopuszczone alternatywy: recenzent alt. Spark `xhigh` (zajęty FE-2a)
- Powód wyboru: UI bez niezmiennika, kontekst sesji; rozłączne pliki z FE-2a
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook ŻÓŁTY, 2026-10-05 ok. 17:40); Gemini nieznany
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: wymagane korekty
- Rundy korekt: 1 (wspólna korekta FE-2, K6–K9)
- Czas do akceptacji: ok. 50 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1×P2, 3×P3 potwierdzone; Gemini zmyślił cytat z `AGENTS.md` („każdy serwis, pipe, funkcja pomocnicza… ma .spec.ts”) — odrzucony jako uzasadnienie, test i tak dopisany (K10)
- Defekty po odbiorze: brak
- Wymagane testy i dowody: spec przekazania nakładek i fokusu; `browser-check` (wąski ekran: arkusz „Abonament” z „Opłać teraz”)

### 2370-BE-1 (stan efektywny, odczyt zaległości, GET, strażnicy — łańcuch 1 → 1a → 1a2 → 1a3 → 1b → 1b2) — 2026-10-05
- Archetyp: Backend / integracja operatora płatności i strażnicy
- Stawka: wysoka (high-stakes)
- Niepewność: wysoka
- Wykonawca (linia / model / native effort): Claude / Opus 5.5 / `xhigh` (`wykonawca-opus`), sekwencyjnie
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh`, `-Access read` (1a+1a2; 1a3+1b)
- Dopuszczone alternatywy: brak dla autora; recenzent alt. Gemini `flash-high`
- Powód wyboru: płatności = niezmiennik; lokalnie 1603-BE 0–4 rund
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook ŻÓŁTY, 17:00–18:40); Spark nieznany (pierwsza recenzja 1a padła, ponowienie OK)
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: BE-1 i BE-1a — strażnik kontekstu (~303 k / 322 k), BE-1b — 301 k po 2 plikach; przekazania przyjęte, reszta świeżymi agentami
- Rundy korekt: 0 rund korekty kodu po recenzjach (P2/P3 przeszły do briefów testów 1b3a/b); 3 przekazania kontekstu
- Czas do akceptacji: ok. 2 h 10 min (17:04 → ok. 19:15) bez testów uzupełniających
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1a+1a2 — 1×P1 odrzucone (błąd bazy → 500 spójny z innymi odczytami), 1×P2 odrzucone (podwójny odczyt bez skutku), reszta P2/P3 do testów; 1a3+1b — 3×P2, 2×P3 potwierdzone → testy; 1 P3 (strażnik bez identyfikatorów) do PBI #2694
- Defekty po odbiorze: bramka BE (Spark `max`): 1×P1 (kontrola okresu przed żywą kontrolą zaległości — przy prawdziwej zaległości zawsze `PERIOD_NOT_CURRENT`) → G-BE-1; 1×P3 (`pm_…` w `ToString`) → G-BE-1; 1×P2 (zaległość bez otwartej faktury) → ryzyko w PBI #2694
- Wymagane testy i dowody: xunit z SQL (5156 → 5234), testy uzupełniające 1b3a–d (5234 → 5375), po G-BE-1 5456

### 2370-BE-2 (POST zapłaty zaległości — łańcuch 2 → 2a → 2b → 2c) — 2026-10-05
- Archetyp: Backend / obciążenie karty, idempotencja
- Stawka: krytyczna
- Niepewność: wysoka
- Wykonawca (linia / model / native effort): Claude / Opus 5.5 / `xhigh` (`wykonawca-opus`)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh`, `-Access read` (2a, 2b, 2c osobno)
- Dopuszczone alternatywy: brak dla autora; recenzent alt. Gemini `flash-high`
- Powód wyboru: obciążenie karty = twarda bramka
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (ŻÓŁTY) do ok. 19:40, potem zablokowany (CZERWONY 85 %, hook, 19:45); Spark nieznany
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: BE-2 — strażnik kontekstu przy 307 k bez kodu (rozpoznanie zjadło kontekst); podział na 2a/2b/2c z faktami z rozpoznania w briefach — każdy przyjęty za pierwszym razem
- Rundy korekt: 0 dla 2a/2b/2c (uwagi z recenzji 2a → pkt 9–10 briefu 2c; 2b → K-a/K-b jednolinijkowe przez architekta i testy; 2c → brief testów 1b3c)
- Czas do akceptacji: ok. 1 h 20 min od podziału (18:52 → ok. 20:00)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 2a — 3×P3 potwierdzone; 2b — 1×P1 obniżone (celowa decyzja BE-1b, nieaktualny komentarz → K-b), 4×P2 (1 odrzucone — kolejność, reszta do testów/K-a), 2×P3; 2c — „poprawny” 0,8, 4×P3 (luki w testach) potwierdzone → 1b3c
- Defekty po odbiorze: bramka BE (Spark `max`): 2×P3 (fałszywe 402 przy wyścigu z auto-ponowieniem operatora; 502 zamiast 409 przy odłączonej metodzie) → ryzyka w PBI #2694
- Wymagane testy i dowody: build 0/0, pełne xunit z SQL 5234/5234/0; mutacje potwierdzone przez wykonawcę (17 czerwonych w 12 testach); ręczny POST na lokalnej atrapie (409/409/400/400/200 PAID, 1 linia dziennika bez sekretu)

### 2370-FE-3 (audyt SCSS i mixiny) — 2026-10-05
- Archetyp: Refaktoring / SCSS
- Stawka: niska
- Niepewność: niska
- Wykonawca (linia / model / native effort): audyt Spark `xhigh` `-Access read`; mixiny Spark / `muse-spark-1.3-contributor` / `high`, `-Access write`
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read`
- Dopuszczone alternatywy: Gemini write (recenzent Spark)
- Powód wyboru: jak 1603-A-1; wyrocznia = bajtowo identyczny CSS 8 konsumentów (`scss-snapshot.mjs`)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark i Gemini nieznany (2026-10-05 ok. 18:50)
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowano kod; recenzja zaproponowała 3 uproszczenia
- Rundy korekt: 1
- Czas do akceptacji: ok. 25 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 4×P2, 2×P3 — 3 przyjęte (pozorne abstrakcje, komentarz), reszta odrzucona; pierwsza recenzja Gemini padła (brief bez zdania „nie masz powłoki”)
- Defekty po odbiorze: brak
- Wymagane testy i dowody: wyrocznia 8× IDENTYCZNY, stylelint/prettier, build FE

### 2370-BE-1b3 (testy uzupełniające po recenzjach, 3a/3b/3c/3d) — 2026-10-05
- Archetyp: Testy / xunit niezmiennika płatności (strażnicy zaległości, zapłata zaległości)
- Stawka: wysoka (testy przypinają niezmiennik; kod produkcyjny bez zmian)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Claude / Sonnet 5.5 / `medium` (`tester`), cztery osobne briefy
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh`, `-Access read` (3a, 3b, 3c osobno)
- Dopuszczone alternatywy: wykonawca `wykonawca` Sonnet `high`; recenzent alt. Gemini `flash-high`
- Powód wyboru: testy według istniejących wzorców z nazwanymi scenariuszami i mutacjami — rola `tester`; produkcja niezmieniona (skróty plików przed = po)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (ŻÓŁTY po resecie okna, hook, ok. 20:00); Spark nieznany
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: 3a, 3b, 3c przyjęte za pierwszym razem (5234 → 5316 → 5368 → 5375); każda recenzja dała drobne uwagi do kolejnego briefu; 3d przyjęty za pierwszym razem (5375/5375, mutacja: 10 czerwonych z 106, skrót produkcji przed = po; recenzją innej rodziny dla 3d jest bramka BE — zmiana to 6 asercji/docstringów)
- Rundy korekt: 0 na brief (uwagi recenzji → kolejny brief, nie poprawka)
- Czas do akceptacji: ok. 2 h 30 min dla całego łańcucha 3a–3d (ok. 20:00 → 22:35), z czego 3d ok. 4 min wykonania
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 3a — „poprawny” 0,8, 6×P3 (5 potwierdzonych → R-b…R-e; „zbędny `using`” FAŁSZYWE — tester odmówił słusznie, typ z tej przestrzeni użyty); 3b — „niepoprawny warunkowo” 0,85, 1×P2 potwierdzone (kolejność strażnik → zaległość nieprzypięta), ale proponowana poprawka częściowo błędna (`DoesNotContain` także dla dryfu — odrzucone), 2×P3 potwierdzone → 3d; 3c — „poprawny” 0,9, 5×P3: 2 potwierdzone → 3d, `Times.Never` dla innej faktury odrzucone, kolejność pól JSON i poziomy logowania → ryzyko w raporcie
- Defekty po odbiorze: testy nie złapały P1 z bramki BE (scenariusze z przyszłym okresem) — przypięte dopiero w G-BE-1
- Wymagane testy i dowody: build `--no-incremental` 0/0, pełne xunit z SQL po każdym briefie, mutacje potwierdzone przez wykonawcę, skróty plików produkcyjnych sprawdzone przez architekta

### 2370-G (bramka końcowa) — 2026-10-05
- Uwaga procesowa: pierwsze podejście Astry FE (168 s) zatrzymało się na klauzuli STOP — brief architekta podawał błędny kontrakt strażników („`SUBSCRIPTION_CHANGE_UNAVAILABLE` z powodem” zamiast własnego kodu `SUBSCRIPTION_IN_ARREARS`); Astra sprawdziła kod BE i testy API, zgłosiła rozjazd briefu, nie zgłosiła fałszywego defektu. Poprawka briefu i ponowienie.
- Podejście 2 Astry FE padło po 363 s na limicie Plusa („try again at Oct 6th 3:11 AM”), bez raportu → Codex `zablokowany` (rollout, 2026-10-05 22:44); bramka czeka, bez obniżenia modelu/effortu (reguła 6).
- Decyzja właściciela (2026-10-05 ok. 23:00): „Astra max na Plusie to idiotyzm” → reguła 6 na stałe: bramka = `gpt-6.1-sol` `max`; dla tej funkcji jednorazowo Spark `max` (Codex zablokowany do 03:11).
- Archetyp: Recenzja / bramka końcowa high-stakes (cały diff, osobno FE 88 i BE 132 pozycje)
- Stawka: krytyczna · Niepewność: średnia
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access read`, diff w briefie (bez powłoki), FE ∥ BE
- Dopuszczone alternatywy: Sol 6.1 `max` po 03:11 (nowa reguła); brak innej w tej chwili
- Sygnał dostępności: Codex zablokowany (rollout, 22:44, reset 03:11); Spark nieznany (równolegle sesja BeautyEffect)
- Pewność decyzji: średnia (Spark recenzował większość fal tej funkcji — mniej świeże oko)
- Wynik: FE 604 s — „wymaga poprawek” 0,85: 1×P2 (brak przeładowania abonamentu po `Paid` z odpytywania przy wejściu spoza `Arrears`) + 3×P3 (akcje w animacji zamykania, „Zmień” gubi szkic faktury, kłamliwy komentarz 409/422) — wszystkie potwierdzone → G-FE-1; BE 708 s — „wymaga poprawek” 0,85: 1×P1 POTWIERDZONE (strażnik okresu przed żywą kontrolą zaległości → przy prawdziwej zaległości zawsze `PERIOD_NOT_CURRENT`, bo baza nie przesuwa okresu do #2473; wariant zaległy z endpointów zmiany nieosiągalny w produkcji; testy miały przyszły okres) → G-BE-1; 1×P2 (zaległość bez otwartej faktury — strażnicy blokują, GET/POST „brak zaległości”) → ryzyko + zakres #2694; 3×P3: `pm_…` w `ToString` → G-BE-1, fałszywe 402 przy wyścigu z auto-ponowieniem i 502 przy odpiętej metodzie → ryzyka #2694. Fałszywych P0/P1: 0.
- Wartość bramki: P1 przeoczyły wszystkie recenzje fal (Spark ×5, architekt) — błąd przekrojowy strażnik × brak lustra okresu.
- G-FE-1 (poprawki FE): `wykonawca-opus` Opus `xhigh`, 1 przebieg, ok. 11 min, 243 k tokenów; 4 poprawki + 6 testów, 5 mutacji czerwonych; walidacja architekta: lint/format/build 0, testy 4335/4335; recenzja Spark `xhigh` read — „poprawny” 0,85, 1×P3 (podwójny GET przy bezpośrednim `PAID` — świadomie przyjęte w briefie). Rundy korekt: 0 (komentarz klasy dopisał architekt — 1 linia).
- G-BE-1 (poprawki BE): `wykonawca-opus` Opus `xhigh`, 1 przebieg, ok. 18 min, 321 k tokenów (powyżej miękkiego progu 300 k — domknął bez przekazania); P1 (kolejność dostępność → zaległość u operatora → okres, `EnsurePeriodCurrent`) + P3 (`ToString` bez `pm_`), 79 nowych przypadków, mutacje: A 65 czerwonych, B 1; walidacja architekta: build `--no-incremental` 0/0, 5456/5456/0; recenzja Spark `xhigh` read — „poprawny” 0,9, bez znalezisk. Rundy korekt: 0.
- Defekty po odbiorze: brak do bramy potwierdzenia; właściciel przyjął bez uwag (2026-10-05), deploy PRE zweryfikowany 21:49 UTC: FE 1.2.0 `1a2021c`, BE 1.2.0 `2f60f15` (dokładne SHA).
- Wymagane testy i dowody: FE 4335/4335 + lint/format/build; BE 5456/5456/0 z SQL; browser-check sprzed poprawek (8/8 × 2) — poprawki nie dotykają ekranu Ustawień.

### BE-8 (BeautyEffect: podglądy wyglądu do wyboru przez właściciela — M-1, część 1 B-1/B-1b/B-1c) — 2026-10-05
- Archetyp: samodzielna strona HTML z podglądem wariantów (przełączniki opcji, oba motywy, komputer/telefon) na prawdziwych zdjęciach i filmie salonu; materiał do decyzji właściciela, nie kod produktu
- Stawka: średnia (właściciel wybiera kierunek wizualny z podglądu — błąd podglądu = zła decyzja albo stracona runda)
- Niepewność: wysoka (gust właściciela, nastrój dopiero doprecyzowywany w trakcie)
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh` (wszystkie cztery)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — odbiór wizualny architekta (zrzuty Playwright MCP, klatki filmu); odstępstwo od reguły 13 dla materiału podglądowego bez kodu produktu
- Dopuszczone alternatywy: Codex `gpt-6.1-sol` `high` (pula Plus, później zablokowana limitem); Gemini `high` (bez wcześniejszych wyników przy stronach podglądu); Claude `wykonawca` (pula ŻÓŁTA, koszt kontekstu)
- Powód wyboru: duży jednoplikowy HTML/CSS bez Figmy, tani token Sparka, wcześniejsze dobre wyniki Sparka przy stronach statycznych
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (ŻÓŁTY, hook), Spark nieznany (wrapper), 2026-10-05 20:30
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: M-1 (33 min) odrzucony przez właściciela — brief architekta kazał „opowiadać historię” jak DomSztuki, a właściciel chciał z DomSztuki tylko proces wyboru i poziom wykonania (błąd briefu, nie wykonawcy); B-1 i B-1b zatrzymane przez architekta po kolejnych uwagach właściciela o nastroju („za ciemno i ponuro”, „radosny… premium”); B-1c (21 min) zaakceptowany po poprawkach architekta
- Rundy korekt: 3 zmiany briefu wywołane uwagami właściciela + drobne poprawki architekta w B-1c
- Czas do akceptacji: ok. 1 h 10 min od M-1 do pokazania B-1c
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): nie dotyczy (brak recenzji innej rodziny)
- Defekty po odbiorze: 3 wykryte dopiero po uwagach właściciela do części 1 — jednostki `vw` w skalowanym podglądzie telefonu (ogromny H1, łuk filmu poza osią), film w otwarciu z czarno-białym ujęciem i twardymi cięciami (zasób przygotował architekt bez sprawdzenia klatek)
- Wymagane testy i dowody: zrzuty wszystkich stanów przełączników w obu motywach i na obu ekranach. Wniosek: w podglądach ze skalowaniem brief wymaga jednostek kontenera (`cqi`, `container-type`), nie `vw`; architekt ogląda klatki filmu (jasność, kolor, styki) przed wpisaniem go do briefu; cytaty właściciela o nastroju wchodzą do briefu dosłownie

### BE-9 (BeautyEffect: research R-W3 — nagłówki sekcji, rozdzielenie sekcji, ciemny motyw, logo w nagłówku) — 2026-10-05
- Archetyp: research z adresem przy każdym twierdzeniu + gotowe opcje N/S/C/L do podglądu, z kontrastem WCAG wyliczonym wzorem
- Stawka: średnia (opcje idą wprost do podglądu i wyboru właściciela; kolory muszą trzymać ograniczenia AT-SYSTEM-KOLOROW-UI)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): plan Codex / `gpt-6.1-sol` / `high` → po komunikacie limitu Plusa ponowna kwalifikacja: Spark / `muse-spark-1.3-contributor` / `xhigh` (485 s)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — kontrola architekta (adresy, kontrast skryptem, zgodność z AT); odstępstwo od reguły 13 dla researchu referencyjnego
- Dopuszczone alternatywy: Gemini `high` (negatywny sygnał researchu z 2026-09-24); Codex zablokowany do 2026-10-06 03:11
- Powód wyboru: Codex — dotąd najrzetelniejsze adresy; po limicie Spark (ma sieć, dobre wyniki przy opcjach z liczbami)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex zablokowany (komunikat limitu wrappera, 2026-10-05 21:50), Spark nieznany, Claude ostrzegawczy (ŻÓŁTY)
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowany z 1 poprawką adresu (404 NN/g, poprawiony z adnotacją)
- Rundy korekt: 0 (poprawka adresu i uzupełnienia przy B-2 zrobił architekt)
- Czas do akceptacji: ok. 25 min (przebieg 8 min + kontrola)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): znaleziska architekta: część opcji (akcent nagłówków w śliwce, powierzchnie śliwka 900/950 w C-2/C-4, stopka w C-1) wykracza poza ograniczenia AT-SYSTEM-KOLOROW-UI, a research tego nie oznaczył (P2 — odnotowane w KO-KIERUNEK-WIZUALNY); brak kontrastu odnośników na jasnych pasach (4,20 / 3,92 / 4,42 — P2, rozwiązane w briefie B-2)
- Defekty po odbiorze: brak stwierdzonych
- Wymagane testy i dowody: status HTTP adresów, kontrast kluczowych par skryptem. Wniosek: brief researchu z opcjami kolorów wymaga tabeli „opcja × ograniczenie dokumentu” i kontrastu na każdej powierzchni, na której stoi tekst lub odnośnik

### BE-10 (BeautyEffect: podgląd części 1b — dopracowanie wariantu A, grupy N/S/C/L) — 2026-10-05…06
- Archetyp: jak BE-8 (samodzielny HTML podglądu), z czterema grupami opcji łączonymi dowolnie i poprawkami po uwagach właściciela (film, środek na telefonie)
- Stawka: średnia
- Niepewność: średnia (opcje z researchu BE-9, wartości podane w briefie co do piksela i prymitywu palety)
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh` (514 s)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — odbiór wizualny architekta: macierz stanów (N×3, S×3, C×4, L×2, oba ekrany, oba motywy) w Playwright MCP, zestawienia siatek, zrzuty 2–3× gęstości pikseli dla logo
- Dopuszczone alternatywy: Codex zablokowany limitem; Gemini `high`; Claude `wykonawca` (pula ŻÓŁTA)
- Powód wyboru: autor B-1c zna plik; pełna specyfikacja liczbowa w briefie
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex zablokowany (do 2026-10-06 03:11), Spark nieznany, Claude ostrzegawczy (ŻÓŁTY), 2026-10-05 22:05
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zgodny z briefem w większości; Spark nie mógł zrobić zrzutów (serwer podglądu niedostępny z WSL — zrzuty przejął architekt); 5 jawnie zgłoszonych odchyleń, przyjętych
- Rundy korekt: 0 przebiegów korekty — 6 drobnych poprawek CSS/znaczników zrobił architekt (taniej niż brief do pliku 52 kB): podwójny monogram w jasnym motywie (brak reguły ukrywającej wersję ciemną), nagłówki stopki w Bodoni ok. 50 px (reguły grupy N obejmowały każdy `h2`), poświata nad tekstem kroku 3 w ciemnym motywie (brak `z-index`/izolacji) i w najjaśniejszym punkcie pod tekstem (wbrew briefowi), kafelki monogramu widoczne na komputerze w wierszach bez zdjęć (odziedziczone z części 1), logo: grafika z przezroczystym marginesem 33 % wysokości (przycięto zasób), a „duże” logo złożone w L-2 miało napis mniejszy niż poziome — zastąpione poziomym 64 px; L-2 na telefonie dostał własny układ (menu jako ikona, logo na środku 38 px)
- Czas do akceptacji: ok. 1 h 15 min (przebieg 8,5 min + walidacja macierzy i poprawki)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): znaleziska architekta — 2× P1 wizualne (podwójny monogram, nagłówki stopki), 4× P2 (poświata ×2, kafelki, logo); fałszywych: 0
- Defekty po odbiorze: 1 uwaga właściciela po pokazie (2026-10-06): nagłówek otwarcia z myślnikiem łamał się na „Beauty Effect — / salon / kosmetyczny w…” — „salon” sam w wierszu, myślnik jako cienka kreska na początku wiersza; poprawka architekta (myślnik ukryty wizualnie, opis w osobnym bloku 0,75 em, frazy niełamliwe). Źródło: brief B-2 nie przewidział łamania długiego `<em>` przy 72 px (fraza „salon kosmetyczny” ma 500 px przy kolumnie 490–575 px) — pomiar szerokości fraz należy do odbioru wizualnego, nie tylko zrzut. Właściciel wybrał N-1, S-3, C-1, L-1
- Wymagane testy i dowody: zrzuty każdej opcji, `getComputedStyle` dla przełączanych elementów, zapis kliknięć `data-choice` w `state/events`. Wniosek: przy regułach typu „każdy `h2`” brief ma wymieniać wyjątki (stopka, karty); grafik z logo nie skaluje się bez sprawdzenia ramki obrazu (bbox kanału alfa) — architekt przycina zasoby przed briefem

### BE-11 (BeautyEffect: podgląd części 2 — trzy pary krojów na wybranym układzie) — 2026-10-06
- Archetyp: jak BE-10 (samodzielny HTML podglądu) — przepięcie krojów na zmienne CSS i trzy zestawy rozmiarów/grubości z briefu
- Stawka: średnia
- Niepewność: niska–średnia (wszystkie wartości w briefie; jedyna decyzja projektowa — akcent bez kursywy dla Marcellusa — podjęta przez architekta w briefie)
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh` (247 s)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — odbiór wizualny architekta (3 pary × komputer/telefon × jasny/ciemny, pomiar wierszy etykiety i opisu H1); odstępstwo od reguły 13 dla materiału podglądowego
- Dopuszczone alternatywy: Gemini `high`; Codex zablokowany do 2026-10-06 03:11; Claude `wykonawca` (pula ŻÓŁTA)
- Powód wyboru: autor B-1c i B-2 zna plik; dobry wynik B-2
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark nieznany, Codex zablokowany, Claude ostrzegawczy (ŻÓŁTY, tydzień 73 %), 2026-10-06 00:34
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zgodny z briefem; Spark słusznie wskazał lukę briefu (reguła N-1 „ciemny = grubiej” podniosłaby Marcellus — sam dodał nadpisanie) i niejawne zmiany grubości przycisków/nawigacji
- Rundy korekt: 0 przebiegów — 1 poprawka architekta (rozstrzelenie etykiety T-B na telefonie, „GÓRA” w osobnym wierszu)
- Czas do akceptacji: ok. 15 min (przebieg 4 min + walidacja)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): architekt — 1× P3 (zawijanie etykiety T-B na telefonie); fałszywych: 0
- Defekty po odbiorze: brak — właściciel przełączył trzy pary i wybrał T-B „Klasyka” (Cormorant Garamond + Jost) bez uwag (2026-10-06)
- Wymagane testy i dowody: siatki zrzutów, `document.fonts` (załadowane kroje i grubości), liczba wierszy etykiety i opisu H1 per para i widok. Wniosek: brief zmieniający krój musi wymieniać reguły zależne od motywu (grubość w ciemnym) dla każdej pary; tracking wersalików sprawdzać na telefonie przy najdłuższej etykiecie

### BE-12 (BeautyEffect: podgląd części 3 — ruch: wejścia, najechanie, pasek u góry) — 2026-10-06
- Archetyp: jak BE-10 (samodzielny HTML podglądu), ale z logiką: obserwator wejść z kolejnością w partii, odtwarzanie od początku, zachowanie paska przy przewijaniu, przejście motywu (View Transitions), pełny wariant ograniczonego ruchu; wszystkie czasy, krzywe i przesunięcia podane w briefie
- Stawka: średnia
- Niepewność: średnia (interakcje przejść CSS z najechaniem i wejściem na tych samych elementach — rozstrzygnięte w briefie zasadą „efekty R tylko na dzieciach jednostek wejścia”)
- Wykonawca (linia / model / native effort): pierwotnie Spark / `muse-spark-1.3-contributor` / `xhigh` — przebieg nieudany po 295 s (API 402 `billing_error`: „Billing verification failed. Please check your payment method.” — awaria rozliczeń konta, nie limit); ponowna kwalifikacja → Codex / `gpt-6.1-sol` / `high` (2 przebiegi: 57 s zatrzymanie, 590 s wykonanie)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — odbiór wizualny architekta (stany pośrednie animacji przez `document.getAnimations()`, siatki zrzutów W×czas, R×najechanie, P×przewijanie, telefon, ciemny, `emulateMedia(reducedMotion)`, przejście motywu); odstępstwo od reguły 13 dla materiału podglądowego
- Dopuszczone alternatywy: Gemini `high` (zapis na Windows); Claude `wykonawca` (pula ŻÓŁTA, tydzień 73 %)
- Powód wyboru: Spark — autor B-1c/B-2/B-3, dobre wyniki; po awarii Codex Sol — najsilniejsza dostępna linia spoza puli Claude'a, pula po resecie 03:11, brief nie jest high-stakes, jeden plik
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark zablokowany (402 z wrappera, 2026-10-06 11:31), Codex nieznany, Claude ostrzegawczy (ŻÓŁTY, tydzień 73 %), 2026-10-06 11:30
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: przebieg 1 Codexa zatrzymał się zgodnie z klauzulą STOP na dwóch słusznych lukach briefu (samokontrola obejmowała nagłówek paska wyboru; przycisk motywu ukryty na telefonie) — oba rozstrzygnięte przez architekta; przebieg 2 zgodny z briefem, z jawnie opisanymi doprecyzowaniami (osobna właściwość `scale` dla R-2, żeby nie kolidować z transformacją wejścia)
- Rundy korekt: 0 przebiegów korekty — 2 poprawki architekta: `<address>` wewnątrz `<p class="rv">` (błąd znaczników z części 1 — parser zostawiał pusty akapit, który nigdy się nie odsłaniał) oraz kontrast przycisku obrysowego przy najechaniu (podbarwienie 8 % `--link` dawało 4,16:1 na `--feat`; tekst i obrys przy najechaniu → `--ctah`, 5,8:1 — usterka istniała od części 1)
- Czas do akceptacji: ok. 45 min (przebiegi 11 min + walidacja)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): architekt — 1× P2 (kontrast przy najechaniu), 1× P3 (znaczniki adresu); fałszywych: 0
- Defekty po odbiorze: brak uwag właściciela — wybrał W-3 „Odsłonięcie”, R-2 „Uniesienie” i P-2 „Szkło” (2026-10-06). Po wyborze P-2 architekt znalazł 1× P2 nieobjęte briefem: na pasku „szkło” (85 % karty) napis „Zadzwoń”/„Menu” w kolorze odnośnika spadał w najgorszym przypadku do 3,50:1 (jasny) i 3,92:1 (ciemny) — przyciski obrysowe na szkle dostały pełne tło karty. Wniosek: brief z półprzezroczystą powierzchnią musi podawać kontrast każdego koloru tekstu nad najgorszą treścią pod spodem
- Wymagane testy i dowody: postęp `.in` przy przewijaniu krokami (komputer i telefon — 38/38 poza ukrytym na telefonie podglądem), wymiary H1/H2 identyczne z częścią 2 we wszystkich W, wysokość nagłówka i pozycja sekcji stałe we wszystkich P, `data-hidden` nie przy otwartym menu, brak animacji przy ograniczonym ruchu, 0 błędów konsoli. Wniosek: brief zmieniający zachowanie istniejącego elementu musi sprawdzić, czy element jest widoczny w obu widokach; Codex z klauzulą STOP zatrzymuje się na drobnych lukach — w briefie dla Codexa warto dopisać regułę „drobne niejasności rozstrzygnij zachowawczo i zgłoś”

### BE-13 (BeautyEffect: podgląd części 4 — strona kategorii „Rzęsy i brwi” K-1/K-2/K-3 i menu na telefonie M-1/M-2) — 2026-10-06
- Archetyp: jak BE-12 (samodzielny HTML podglądu z logiką): przełączanie stron z przejściem, 11 zabiegów z kotwicami, rozwijanie (K-3), szuflada i arkusz z pułapką fokusu, Escape/scrim/zamknięcie, przeciąganie arkusza palcem
- Stawka: średnia
- Niepewność: średnia (geometria warstwy menu w scenie z `zoom`)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (1 przebieg, 688 s)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — odbiór w przeglądarce architekta (geometria menu w 4 stanach × 2 zoomy, pułapka fokusu, Escape i powrót fokusu, kotwice 11/11, K-3 `aria-expanded` i ukrycie treści, ciemny motyw, ograniczony ruch, konsola); odstępstwo od reguły 13 dla materiału podglądowego
- Dopuszczone alternatywy: Gemini `high` (zapis na Windows); Claude `wykonawca` (pula ŻÓŁTA, tydzień 74 %); Spark zablokowany (402)
- Powód wyboru: Codex — przyjęty BE-12 na tym samym pliku, najsilniejsza dostępna linia spoza puli Claude'a
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY), 2026-10-06 12:05
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: plik kompletny, samokontrola Codexa zielona; Codex słusznie zgłosił błędne założenie briefu (warstwa menu liczona od góry sceny, a nagłówek u początku strony stoi 40 px niżej — dół menu poza ekranem); potwierdzone pomiarem (40 px), poprawione przez architekta jedną linią (wysokość warstwy liczona przy otwarciu od góry nagłówka do dołu sceny), sprawdzone przy `zoom` 1 i 0,88
- Rundy korekt: 0 przebiegów korekty — 1 poprawka architekta (geometria menu)
- Czas do akceptacji: ok. 25 min (przebieg 11,5 min + walidacja)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): Codex — 1× P2 w briefie (potwierdzone); architekt — 1× P3 (etykiety Booksy łamane między wiersze na telefonie, `box-decoration-break: clone` — zostawione), 1× P3 dziedziczone (nazwa dostępna adresu „ulica…” nie zawiera widocznego „ul.” — WCAG 2.5.3, do specyfikacji)
- Defekty po odbiorze: właściciel odrzucił K-1/K-2/K-3 — „Te zabiegi wydaja sie tuuuurbo chujowe. Mam w sumie powtórzone 11x "idz do booksy"”. Przyczyna po stronie architekta i dokumentacji, nie wykonawcy: specyfikacja strony kategorii (podpowiedź Booksy + „Umów wizytę” przy każdym zabiegu, wspólna zasada uzupełnienia powtórzona 5×) przeniesiona do briefu dosłownie, mimo że Booksy nie ma odnośników do pojedynczych usług. Wniosek: przed briefem podglądu przejrzeć specyfikację treści pod kątem powtórzeń i martwych działań (ten sam cel 11×), nie tylko pod kątem zgodności tekstu. Druga lekcja: podgląd części 4 pokazywał niezmienioną sekcję „Co tu zrobisz”, którą właściciel już skrytykował — właściciel odebrał to jako zignorowanie uwagi; przy publikacji podglądu jawnie mówić, które sekcje są nieaktualne
- Wymagane testy i dowody: pomiar geometrii warstwy menu (przepełnienie 0 px w 4 stanach × 2 zoomy), fokus i Escape, kotwice, konsola 0 błędów, zrzuty 2 widoki × 2 motywy

### BE-14 (BeautyEffect: research R-S1 — sekcje niesione zdjęciem i wideo: dowody, wydajność, WCAG, AI) — 2026-10-06
- Archetyp: research dowodowy z adresem i siłą dowodu przy każdym twierdzeniu + 3–4 opcje na każdą sekcję strony głównej
- Stawka: średnia (opcje idą do podglądów; zasady AI i ruchu wiążą wygląd)
- Niepewność: średnia (stan prawny AI Act i UOKiK na 2026, Baseline przeglądarek)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (1607 s)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — kontrola architekta (status HTTP adresów, sprawdzenie dwóch twierdzeń prawnych u źródła); odstępstwo od reguły 13 dla researchu referencyjnego
- Dopuszczone alternatywy: Gemini `high` (równolegle prowadził research rynkowy R-S2); Spark zablokowany (402); Claude — pula ŻÓŁTA
- Powód wyboru: Codex — najrzetelniejsze adresy w dotychczasowych researchach (BE-7, BE-9)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY), 2026-10-06 ok. 12:30
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowany bez poprawek; adresy — 35 odpowiada, 20 zwraca 403 automatowi (strony blokujące boty, treść nie do sprawdzenia skryptem), 1 nie odpowiada; dwa twierdzenia prawne (ustawa o przeciwdziałaniu nieuczciwym praktykom rynkowym, ELI DU/2023/845; AI Act art. 50 od 2026-08-02) potwierdzone u źródła; rekomendacje sekcji 01 (duże karty w widocznej siatce; przy taśmie wszystkie nazwy widoczne poza nią) i zasada „pętla 5 s powtarzana to nadal ruch bez końca” przeniesione do briefu B-6
- Rundy korekt: 0
- Czas do akceptacji: ok. 35 min (przebieg 27 min + kontrola)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): brak znalezisk architekta powyżej P3
- Defekty po odbiorze: brak stwierdzonych
- Wymagane testy i dowody: status HTTP adresów, odczyt źródeł prawnych dla twierdzeń o obowiązkach

### BE-15 (BeautyEffect: research R-S2 — jak strony beauty 2025–2026 używają zdjęć i wideo w sekcjach) — 2026-10-06
- Archetyp: przegląd rynku 20–30 stron z opisem sekcji pod pełnym adresem + wzorce per sekcja
- Stawka: niska–średnia (materiał inspiracyjny; wiążące ustalenia biorą się z BE-14)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` (817 s)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — kontrola architekta (status HTTP adresów, próbka 3 opisów stron porównana z żywą stroną); odstępstwo od reguły 13 dla researchu referencyjnego
- Dopuszczone alternatywy: Codex `high` (zajęty R-S1 — dwa researche równolegle na rozłącznych plikach); Spark zablokowany (402)
- Powód wyboru: ponowna ocena negatywnego sygnału z 2026-09-24 na briefie z twardym wymogiem pełnego adresu przy każdym twierdzeniu; druga linia równolegle do Codexa
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany, Codex nieznany (zajęty), Spark zablokowany (402), 2026-10-06 ok. 12:30
- Pewność decyzji: niska
- Wynik pierwszego podejścia: przyjęty z adnotacją architekta, bez przebiegu korekty; adresy — 28 odpowiada, 1 zwraca 404 (wpis Awwwards), 2 nie odpowiadają; próbka 3 opisów: 1 zgodny, 1 częściowo błędny, 1 błędny — opisy stron w katalogu niepotwierdzone mimo poprawnych adresów; błędy faktów o salonie (adres, uchwyt Instagrama), błąd techniczny (`loading="lazy"` przy `<video>` nie działa), twierdzenia prawne bez adresów
- Rundy korekt: 0 (adnotacja architekta zamiast korekty — wzorce z rozdziałów 5–6 tylko jako pomysły)
- Czas do akceptacji: ok. 25 min (przebieg 14 min + kontrola)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): architekt — opisy treści stron zmyślone przy prawdziwych adresach (P1 dla rzetelności researchu, potwierdzone na 2 z 3 próbek), 2× błędny fakt o salonie (P2), 1× błąd techniczny (P2), twierdzenia prawne bez źródła (P2)
- Defekty po odbiorze: brak — dokument oznaczony jako niepotwierdzony w części opisowej, ustalenia prawne i techniczne brane wyłącznie z BE-14
- Wymagane testy i dowody: status HTTP adresów i porównanie próbki opisów z żywą stroną. Wniosek: drugi sygnał negatywny Gemini w researchu rynku — wymóg adresu nie wystarcza, bo adres bywa prawdziwy, a opis strony wymyślony; przy kolejnym researchu rynkowym Gemini kontrola próbki ≥ 3 opisów jest obowiązkowa, a dla treści, które mają wiązać, kwalifikować inną linię

### BE-16 (BeautyEffect: podgląd części 5 — sekcja „Co tu zrobisz”, cztery układy O-1…O-4 ze zdjęciami i filmami) — 2026-10-06
- Archetyp: jak BE-12/BE-13 (samodzielny HTML podglądu z logiką): cztery układy jednej sekcji × 2 widoki × 2 motywy, filmy z regułą ≤ 5 s i ograniczeniem ruchu, taśma z licznikiem i strzałkami, karty przyklejane, pasy rozsuwane przy najechaniu/fokusie
- Stawka: średnia (odpowiedź na trzy wprost wymienione zastrzeżenia właściciela, które BE-13 przeoczył)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (1 przebieg, 265 s)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — odbiór w przeglądarce architekta (rozmiary kafli w 4 układach × 2 widoki, filmy: start, pauza przy 5,05 s, powtórka po najechaniu, brak odtwarzania przy ograniczonym ruchu, taśma: licznik, strzałki, klawiatura, fokus, Stos: `sticky` i jego wyłączenie przy ograniczonym ruchu, Panorama: rozsunięcie przy fokusie, kontrast przyciemnienia wzorem, unikalne `id`, brak nowych HEX, konsola 0 błędów, pliki na serwerze właściciela); odstępstwo od reguły 13 dla materiału podglądowego
- Dopuszczone alternatywy: Gemini `high`; Claude `wykonawca` (pula ŻÓŁTA); Spark zablokowany (402)
- Powód wyboru: Codex — przyjęte BE-12 i BE-13 na tym samym pliku
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 75 %), 2026-10-06 12:40
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: plik kompletny i poprawny w logice filmów, ale Codex zatrzymał się klauzulą STOP na drobnej sprzeczności briefu (opis przycisku „dwa z filmem” przy trzech filmach w specyfikacji), mimo polecenia, by drobne niejasności rozstrzygać zachowawczo — bez końcowej samokontroli; sprzeczność słuszna, ale nie wymagała zatrzymania
- Rundy korekt: 0 przebiegów korekty — poprawki architekta: opis przycisku; taśma O-2 — licznik pokazuje zakres widocznych kart („1–4 / 8” zamiast „5 / 8” na końcu), „wstecz” wyłączone na starcie (wcięcie 4 px na obrys fokusu), pasek postępu pokazuje widoczną część, zerowanie taśmy przy zmianie widoku
- Czas do akceptacji: ok. 30 min (przebieg 4,5 min + walidacja i poprawki)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): Codex — 1× P3 w briefie (potwierdzone); architekt — 4× P3 w taśmie O-2 (potwierdzone, poprawione); podejrzenie ucięcia pionowych nazw w O-4 — odrzucone pomiarem (zrzut dzielił pas na dwa kadry)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: pomiary rozmiarów kafli, stan `<video>` w czasie (odtwarzanie/pauza/`currentTime`), stan kontrolek taśmy, zrzuty 2 widoki × 2 motywy. Wniosek: brief z twardym wymogiem zgodności liczb (tu: liczba filmów w opisie i w specyfikacji) sprawdzić przed wysłaniem; Codex przy klauzuli STOP przerywa także drobiazgi — w briefie podglądu wskazać wprost, które sprzeczności rozstrzyga sam

### BE-17 (BeautyEffect: research R-S3 — strona kategorii zabiegów bez powtarzanego „umów się”, odnośniki Booksy) — 2026-10-06
- Archetyp: przegląd rynku 15–25 stron z pełnym adresem + pytanie faktograficzne (Booksy: odnośnik do usługi) + 3–4 wzorce
- Stawka: średnia (odpowiedź na pytanie 1 rozstrzyga, czy przycisk przy zabiegu ma sens)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` (1403 s)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — kontrola architekta (status HTTP 52 adresów, odczyt kodu profilu Booksy, próbka 4 opisów stron); odstępstwo od reguły 13 dla researchu referencyjnego
- Dopuszczone alternatywy: Codex `high` (zajęty B-6); Spark zablokowany (402)
- Powód wyboru: Codex zajęty budową podglądu; pytanie 1 sprawdzalne przez architekta u źródła, więc ryzyko zmyśleń ograniczone do katalogu
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany, Codex nieznany (zajęty), Spark zablokowany (402), 2026-10-06 12:25
- Pewność decyzji: niska
- Wynik pierwszego podejścia: przyjęty z adnotacją architekta, bez przebiegu korekty; pytanie 1 — potwierdzone dokładnie (identyfikator usługi z nazwą, jedyne dwie kotwice, oferty bez adresów); adresy — 34 odpowiada, 8 × 403, 5 × 404, 1 × 500, 4 nie odpowiadają; próbka 4 opisów: 3 częściowo niezgodne, 1 strona opisana jako odczytana, choć jej adresy nie działają i nie trafiła na listę nieodczytanych
- Rundy korekt: 0
- Czas do akceptacji: ok. 20 min (przebieg 23 min + kontrola)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): architekt — opis strony nieodczytanej podany jako odczyt (P1 dla rzetelności, potwierdzone), 3× częściowo zmyślone szczegóły stron (P2), w sekcji „co błędne” teza, że nazwa usługi Booksy to szum (P3 — sprzeczna z INT-BOOKSY, odnotowana)
- Defekty po odbiorze: brak — katalog oznaczony jako poglądowy
- Wymagane testy i dowody: odczyt kodu profilu Booksy, status HTTP adresów, porównanie próbki opisów z żywą stroną. Wniosek: trzeci sygnał negatywny Gemini w researchu rynku (po 2026-09-24 i BE-15) — opisy pojedynczych stron niewiarygodne mimo poprawnych adresów; pytania faktograficzne sprawdzalne przez architekta wypadły dobrze. Przy kolejnym researchu rynkowym kwalifikować inną linię albo ograniczyć Gemini do pytań sprawdzalnych u źródła

### BE-18 (BeautyEffect: podgląd części 6 — strona kategorii „Rzęsy i brwi” Z-1/Z-2/Z-3 bez powtarzanego „idź do Booksy”) — 2026-10-06
- Archetyp: jak BE-16 (samodzielny HTML podglądu z logiką): trzy układy strony kategorii z odrębnym DOM, wzorzec ARIA zakładek z klawiaturą, przełącznik trybu z regionem `aria-live`, rysunki SVG wg parametrów, pływający przycisk z IntersectionObserver, tabela ↔ lista definicji, film z regułą ≤ 5 s
- Stawka: średnia (odpowiedź na odrzucenie K-1/K-2/K-3 z BE-13)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (1 przebieg, 517 s)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — odbiór w przeglądarce architekta (liczby: 11 zabiegów i 3 grupy w każdej opcji, 4 odnośniki Booksy, żadnego przy zabiegu; zakładki: strzałki/Home/End, `aria-selected`, `hidden`; przełącznik: nazwy obu trybów, `aria-pressed`, komunikat; pływający przycisk: widoczność i fokus na nagłówku ściągawki; film: pauza 5,02 s; ograniczony ruch: 0 animacji, 0 ukrytych, 0 filmów; zrzuty 3 opcje × 2 widoki, ciemny motyw; konsola 0 błędów); odstępstwo od reguły 13 dla materiału podglądowego
- Dopuszczone alternatywy: Gemini `high`; Claude `wykonawca` (pula ŻÓŁTA, tydzień 75 %); Spark zablokowany (402)
- Powód wyboru: Codex — przyjęte BE-12, BE-13 i BE-16 na tej samej rodzinie plików
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY), 2026-10-06 13:02
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowany po 4 drobnych poprawkach architekta; tym razem bez zatrzymania na drobiazgach (brief wskazywał wprost, które sprzeczności rozstrzyga sam — wniosek z BE-16 zadziałał)
- Rundy korekt: 0 przebiegów korekty — poprawki architekta: przywrócony odnośnik „Profil salonu w Booksy” w stopce (Codex usunął go, dosłownie stosując limit odnośników z briefu, który dotyczył przycisków rezerwacji — niejasność briefu), Z-3 na telefonie — zdjęcie grupy „Laminacja” ukryte odziedziczoną klasą `.a-preview` z części 4 (przywrócone), Z-3 ściągawka na telefonie — puste wiersze „uzupełnienie —” przy zabiegach bez uzupełnienia (usunięte), Z-2 — kadr filmu przesunięty z maseczki na dłonie
- Czas do akceptacji: ok. 35 min (przebieg 8,5 min + walidacja i poprawki)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): architekt — 1× P2 (zdjęcie ukryte na telefonie), 3× P3 (stopka, puste wiersze, kadr); podejrzenia odrzucone pomiarem: puste łuki w Z-3 (zrzut w trakcie odsłaniania), przyklejone zakładki Z-2 nad zamknięciem (zakładki kończą się z ostatnią grupą — zachowanie poprawne)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: liczby z DOM dla każdej opcji, stan ARIA po klawiszach, stan `<video>` w czasie, zrzuty 3 × 2 i ciemny motyw. Wnioski: (1) przy budowie z pliku bazowego wskazać w briefie klasy bazowe, których nie wolno używać ponownie (np. `.a-preview` ma reguły widoku telefonu); (2) limity liczbowe w briefie opisywać rolą („przyciski rezerwacji”), nie wzorcem adresu

### BE-19 (BeautyEffect: podgląd części 7 — strona „Rzęsy i brwi” bez nazw usług z Booksy, z równymi opisami) — 2026-10-06
- Archetyp: przeróbka istniejącego HTML podglądu (BE-18) — usunięcie mechanizmów (bloki nazw, przełącznik z `aria-live`, ściągawka, pływający przycisk, martwy CSS/JS), podmiana treści dosłownej, nowy rysunek SVG wg parametrów, równe wysokości kart
- Stawka: średnia (odpowiedź na odrzucenie treści części 6)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (2 przebiegi: 61 s — zatrzymanie, 301 s — wynik)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — odbiór w przeglądarce architekta (liczby z DOM: 11 zabiegów z opisem i 3 grupy w każdej opcji, 2 notki na opcję, 6 SVG w Z-3, 4 odnośniki Booksy wg ról, zero zakazanych ciągów, zero zdublowanych `id`; równe wysokości kart w rzędzie Z-2; zakładki `aria-selected`; zrzuty 3 opcje × 2 widoki i ciemny motyw; konsola 0 błędów); odstępstwo od reguły 13 dla materiału podglądowego
- Dopuszczone alternatywy: Gemini `high` (zajęty briefem B-8); Claude `wykonawca` (pula ŻÓŁTA, tydzień 76 %); Spark zablokowany (402)
- Powód wyboru: Codex — przyjęte BE-16 i BE-18 na tym samym pliku bazowym
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY), 2026-10-06 14:02
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zatrzymanie słuszne — w opisie mega volume architekt napisał „stąd «7–15D» w nazwie”, a nazwa zabiegu na stronie nie zawiera „7–15D” (to była nazwa usługi z Booksy, właśnie usuwana); po poprawce opisu w dokumentacji i briefie drugi przebieg zaakceptowany
- Rundy korekt: 1 przebieg ponowny po błędzie przesłanki architekta; poprawka architekta: jedno słowo w opisie paska podglądu („tej samej długości” → „podobnej długości”) — Codex słusznie zgłosił, że opisy mają 107–196 znaków
- Czas do akceptacji: ok. 15 min (2 przebiegi 6 min + walidacja)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): architekt — brak defektów; zgłoszenia wykonawcy w sekcji „Co uważasz za błędne” — 2 trafne (sprzeczność opisu z nazwą, nieprecyzyjne „tej samej długości”)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: liczby z DOM dla każdej opcji, wysokości kart, zrzuty 3 × 2 i ciemny motyw, konsola. Wniosek: przy zmianie źródła nazw (tu: wycofanie nazw Booksy) sprawdzić w treści odwołania do usuwanych nazw — klauzula STOP wyłapała błąd przesłanki architekta po 61 s, taniej niż poprawka po odbiorze

### BE-20 (BeautyEffect: podgląd części 8 — trzy style kart zabiegów w układzie Z-2) — 2026-10-06
- Archetyp: przeróbka HTML podglądu (BE-19) — trzy warianty DOM z zakładkami ARIA, wyróżnienia w treści bez zmiany znaków, 5 nowych rysunków SVG z opisu słownego i parametrów, rysowanie kresek w CSS, siatka mozaikowa z jawnym rozmieszczeniem kafli i osobną kolejnością na telefonie
- Stawka: średnia (odpowiedź na uwagę właściciela do kart Z-2)
- Niepewność: średnia (rysunki laminacji i henny projektowane z opisu)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (1 przebieg, 549 s)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — odbiór w przeglądarce architekta (liczby z DOM: 11 zabiegów i 3 zakładki w każdym wariancie, 11 słów-kluczy w KA-1/KA-2, 11 SVG w KA-2, 4 odnośniki Booksy wg ról, zero zdublowanych `id`; zrzuty 3 warianty × 3 zakładki × 2 widoki; zbliżenia 11 rysunków w obu motywach; ograniczony ruch: 194 ścieżki kompletne, 0 animacji, 0 filmów; konsola 0 błędów); odstępstwo od reguły 13 dla materiału podglądowego
- Dopuszczone alternatywy: Gemini `high` (zajęty briefem B-8); Claude `wykonawca` (pula ŻÓŁTA, tydzień 76 %); Spark zablokowany (402)
- Powód wyboru: Codex — przyjęte BE-16, BE-18 i BE-19 na tym samym pliku bazowym
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY), 2026-10-06 14:17
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany bez poprawek
- Rundy korekt: 0
- Czas do akceptacji: ok. 15 min (przebieg 9 min + walidacja)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): architekt — brak defektów; wykonawca trafnie wskazał niejednoznaczne „koniec na wysokości 18” (przyjął 18 px nad nasadą)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: liczby z DOM, zrzuty wariant × zakładka × widok, zbliżenia rysunków w obu motywach, stan ruchu przy ograniczeniu. Wniosek: rysunki z opisu słownego z jednym przykładowym kształtem i parametrami geometrii wyszły w pierwszym przebiegu — ten sposób opisu wystarcza dla ilustracji podglądowych

### BE-21 (BeautyEffect: dokumentacja — usunięcie nazw usług Booksy z siedmiu stron kategorii) — 2026-10-06
- Archetyp: wdrożenie decyzji właściciela w dokumentacji Markdown — 7 plików, usuwanie powtarzalnych bloków, przenoszenie faktów salonu, ujednolicenie wierszy powiązań
- Stawka: niska–średnia (dokumentacja; źle przeniesiony fakt salonu to błędna informacja dla klientki)
- Niepewność: średnia (dwa kształty bloków, osobna wcześniejsza reguła publikacji na trzech stronach zabiegów medycznych)
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / effort w sufiksie (1 przebieg, 1850 s, exit 3 — 503 w ostatniej turze, po zapisaniu wszystkich plików)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — odbiór architekta (diff 7 plików, wyszukiwanie zakazanych fraz, kontrola linków: 140 plików, 0 martwych); odstępstwo od reguły 13 dla dokumentacji niskiej stawki
- Dopuszczone alternatywy: Codex `gpt-6.1-sol` `high` (zajęty briefem podglądu części 7); Claude `wykonawca` (pula ŻÓŁTA); Spark zablokowany (402)
- Powód wyboru: Gemini — rozłączny tor dokumentacji równolegle z Codexem na podglądzie; brak niezmiennika wysokiej stawki
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany, Codex nieznany (zajęty), Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY), 2026-10-06 przy starcie podglądu części 7
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowany po poprawkach architekta
- Rundy korekt: 0 przebiegów wykonawcy; poprawki architekta jednym skryptem (4 strony + KO + DEC)
- Czas do akceptacji: ok. 31 min przebiegu + ok. 20 min walidacji i poprawek
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): (1) P2 potwierdzone — piercing: kolczyk tytanowy przeniesiony do otwarcia jako zasada „dla wszystkich zabiegów”, choć dotyczy tylko sekcji 3–13 (wykonawca sam to zgłosił); (2) luka specyfikacji, nie wykonania — trzy strony z regułą publikacji z 2026-10-05 zachowały zdanie odsyłające do Booksy przy 15 zabiegach i „szukaj nazw podanych przy zabiegach” w zamknięciu (brief kazał nie ruszać opisów i zamknięcia); (3) wada specyfikacji — fraza `Jak się umówić` z listy zakazanych w definicji ukończenia jest też nazwą pozycji menu, więc wykonawca zamienił ją w trzech plikach na adres `/umow-wizyte`
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: diff, wyszukiwanie zakazanych fraz, kontrola linków. Wniosek: lista zakazanych fraz w definicji ukończenia musi wyłączać ich uprawnione użycia; przed wdrożeniem decyzji w wielu plikach architekt sprawdza, czy któryś plik nie ma własnej, wcześniejszej reguły tego samego tematu

### BE-22 (BeautyEffect: podgląd części 9 — „Dlaczego Beauty Effect”, „Jak się umówić” i menu na telefonie) — 2026-10-06
- Archetyp: nowy HTML podglądu na pliku bazowym (`czesc-5.html`) z przeniesieniem menu M-2 z `czesc-4.html` — trzy grupy wariantów (D ×3, U ×3, M ×2) z jednym API `pokaz`, rysunki SVG z opisu słownego, film w ramce
- Stawka: średnia (dwie sekcje strony głównej i menu na telefonie do wyboru przez właściciela)
- Niepewność: średnia (trzy nowe układy na sekcję, rysunki z opisu, przeniesienie menu między plikami)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (2 przebiegi: B-11 850 s, poprawki B-11a 490 s)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — odbiór w przeglądarce architekta (zrzuty 6 wariantów × 2 widoki × 2 motywy, zbliżenia wieńca w obu motywach, stan filmu w czasie: start po wejściu w widok, zatrzymanie przy 5 s, ponowne odtworzenie po najechaniu; ograniczony ruch: tylko plakat, 12 liści kompletnych, 0 animacji; menu M-1/M-2: otwarcie, Escape i powrót fokusu; konsola 0 błędów); odstępstwo od reguły 13 dla materiału podglądowego
- Dopuszczone alternatywy: Claude `wykonawca` (pula ŻÓŁTA, tydzień 76 %); Gemini `high` (gorsze wyniki na HTML podglądu niż Codex w BE-16…20); Spark zablokowany (402)
- Powód wyboru: Codex — przyjęte BE-16, BE-18, BE-19 i BE-20 na tych samych plikach bazowych
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 76 %), 2026-10-06 15:06
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: odrzucony do poprawki — 8 defektów wykonania i jedna decyzja architekta odrzucona przez właściciela (czarno-biały film z ręcznym startem w U-3); po B-11a zaakceptowany
- Rundy korekt: 1 przebieg poprawkowy wykonawcy (B-11a), bez poprawek architekta
- Czas do akceptacji: ok. 14 min przebiegu B-11 + ok. 8 min B-11a + ok. 40 min walidacji obu
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): architekt — 8 potwierdzonych P2/P3: etykieta nad nagłówkiem nie wyśrodkowana w trzech wariantach wyśrodkowanych; tekst ucięty przez stałe wysokości rzędów siatki D-2; etykieta „Na miejscu” nad pierwszą kolumną zamiast nad trzema; wieniec laurowy narysowany jak łańcuszek w kształcie litery U; nazwy urządzeń łamane z kropką na końcu wiersza; D-3 na telefonie wyśrodkowany z rozjechaną ikonką; numery kroków nie na linii pierwszego wiersza; zdanie o zasadach bez odstępu od przycisków. Właściciel — wada briefu architekta, nie wykonania: film czarno-biały i start ręczny („wygląda strasznie depresyjnie - pogrzebowo”, „włączanie ręczne jest idiotyczne”)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: zrzuty wariant × widok × motyw, zbliżenia rysunków, stan `<video>` w czasie, ograniczony ruch, menu z klawiatury, konsola. Wnioski: (1) brief opisujący rysunek słowami („wieniec laurowy”) bez geometrii dał kształt nierozpoznawalny — w B-11a ścieżki łodyżek i kształt liścia podane wprost wyszły w pierwszym przebiegu, zgodnie z wnioskiem BE-20; (2) układy wyśrodkowane i siatki ze stałą wysokością rzędów trzeba w briefie opisać wprost (wyśrodkowanie etykiety, wysokość z treści) — wykonawca bez przeglądarki tego nie widzi; (3) dobór mediów sprawdza architekt przed briefem: kolor kadrów i sposób startu filmu (pamięć „media w kolorze, autoplay”)

### BE-23 (BeautyEffect: podgląd części 10 — „Aktualności i promocje”, „Gdzie nas znajdziesz” i stopka) — 2026-10-06
- Archetyp: nowy HTML podglądu na pliku bazowym (`czesc-9.html`) — usunięcie niewybranych wariantów D/U/M, trzy nowe grupy wariantów (A ×3, L ×3, F ×3), galeria, ramka telefonu z filmem, słupki tygodnia, dzisiejszy dzień liczony w skrypcie, napis marki w stopce
- Stawka: średnia (ostatnie sekcje strony głównej i stopka do wyboru przez właściciela)
- Niepewność: średnia (dziewięć nowych układów; mechanizmy pliku bazowego z wcześniejszych części)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (4 przebiegi: B-12 75 s — zatrzymanie, B-12 831 s — wynik, B-12a 103 s — zatrzymanie, B-12a 250 s — poprawki)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — odbiór w przeglądarce architekta (zrzuty 9 wariantów × 2 widoki × 2 motywy, zbliżenie łuku L-3, stan filmu A-2 w czasie, film otwarcia: pętla, ograniczony ruch przy starcie i po przełączeniu, odtworzenie przyciskiem; dzisiejszy dzień; konsola 0 błędów); odstępstwo od reguły 13 dla materiału podglądowego
- Dopuszczone alternatywy: Claude `wykonawca` (pula ŻÓŁTA, tydzień 77 %); Gemini `high` (słabsze wyniki na HTML podglądu); Spark zablokowany (402)
- Powód wyboru: Codex — przyjęte BE-16, BE-18…BE-20 i BE-22 na tych samych plikach bazowych
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 77 %), 2026-10-06 15:33
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zatrzymanie słuszne — dwa błędy przesłanek architekta (atrybut `data-l` zajęty przez nagłówek z części 1b; „istniejący przełącznik ograniczonego ruchu”, którego w pliku nie ma); po poprawce briefu wynik z 6 defektami do poprawki
- Rundy korekt: 1 runda poprawek (B-12a) z jednym słusznym zatrzymaniem po drodze (architekt błędnie podał, że `czesc-9.html` zatrzymuje film otwarcia przy ograniczonym ruchu — wcześniejszy odczyt architekta złapał film przed startem); bez poprawek architekta
- Czas do akceptacji: ok. 24 min przebiegów + ok. 45 min walidacji
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): architekt — (1) P2 zmiana poza zakresem: wykonawca usunął pętlę zatwierdzonego filmu otwarcia, czytając „bez nieskończonych pętli” szerzej niż sekcje briefu; (2–6) P3 wykonania: etykiety L-2 przy lewej krawędzi nad wyśrodkowaną treścią, pinezka obok dwuwierszowego adresu na telefonie, przesunięty obrys łuku na bladym wypełnieniu (wygląda jak błąd, wychodzi poza margines), zdjęcie F-3 poza marginesem na telefonie, napis F-1 niewidoczny w jasnym i głośny w ciemnym motywie. Wykonawca — 3 trafne zatrzymania na błędach przesłanek architekta
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: zrzuty wariant × widok × motyw, zbliżenia, stan `<video>` w czasie, ograniczony ruch przy starcie i po przełączeniu, konsola. Wnioski: (1) zakaz ogólny w briefie („bez nieskończonych pętli”) trzeba zawęzić do zakresu briefu, inaczej wykonawca stosuje go do zatwierdzonych elementów; (2) przed briefem na pliku bazowym architekt sprawdza zajęte nazwy atrybutów i kluczy stanu oraz faktyczne zachowanie, na które się powołuje — trzy zatrzymania kosztowały razem ok. 3 min przebiegu, taniej niż poprawka po odbiorze; (3) kolor ozdoby opisany nazwą zmiennej („kolor linii”) daje różny efekt w motywach — podawać kolor z przezroczystością osobno dla każdego motywu

### BE-24 (BeautyEffect: podgląd części 10b — ramka iPhone'a, odnośniki do profili, łuk ze zdjęciem, stopka z podpisem twórcy) — 2026-10-06
- Archetyp: nowy HTML podglądu na pliku bazowym (`czesc-10.html`) — usunięcie niewybranych wariantów, przebudowa ramki telefonu z geometrią w tabeli, trzy warianty odnośników tylko w widoku telefonu, okno ze zdjęciem w łuku, stopka bez godzin z podpisem twórcy, niski panel wyboru i przewijanie do sekcji
- Stawka: średnia (dopracowanie wybranych wariantów i ponowny wybór stopki przez właściciela)
- Niepewność: średnia (sześć niezależnych zmian w jednym pliku, nowe klucze stanu)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (1 przebieg, 719 s)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — odbiór w przeglądarce architekta (okno laptopa 1366×657 bez `odslon()`: wysokość sceny i widoczność trzech stopek; zrzuty A-2 × 3 warianty × 2 motywy, L-3 i stopki w obu widokach i motywach; stan filmu A-2 w czasie i przy ograniczonym ruchu; bilans nawiasów CSS; reguły w CSSOM; konsola 0 błędów); odstępstwo od reguły 13 dla materiału podglądowego
- Dopuszczone alternatywy: Claude `wykonawca` (pula ŻÓŁTA, tydzień 77 %); Gemini `high` (słabsze wyniki na HTML podglądu); Spark (ostatni sygnał: zablokowany, 402)
- Powód wyboru: Codex — przyjęte BE-16, BE-18…BE-20, BE-22 i BE-23 na tych samych plikach bazowych
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Spark zablokowany (402, ostatni odczyt), Claude ostrzegawczy (ŻÓŁTY, tydzień 77 %), 2026-10-06 16:19
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: przyjęty bez rundy korekt; wszystkie wymiary z tabeli i warianty zgodne ze zrzutami
- Rundy korekt: 0; jedna poprawka jednowierszowa architekta poza zakresem briefu (osierocona lista deklaracji w bloku ograniczonego ruchu, obecna w plikach od części 3 — wykonawca ją wykrył i słusznie nie ruszył, bo brief zakazywał zmian poza zakresem)
- Czas do akceptacji: ok. 12 min przebiegu + ok. 20 min walidacji
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): architekt — (1) P2 odziedziczone: w `@media (prefers-reduced-motion)` lista deklaracji bez selektora zamykała blok za wcześnie, przez co reguły „tylko przy ograniczonym ruchu” (przejścia nagłówka P-2, przejście motywu) działały zawsze, a nadmiarowy `}` unieważniał następną regułę (poprawka kontrastu przycisku obrysowego); zgłoszone przez wykonawcę jako uwaga, potwierdzone w CSSOM, usunięte. Przyczyna niewidocznej stopki w części 10 (panel ok. 240 px, stopka wydłużona godzinami) — błąd projektu podglądu po stronie architekta, wykryty dopiero przez właściciela; walidacja części 10 szła w wysokim oknie z `odslon()`, więc go nie pokazała
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: zrzuty w oknie typowego laptopa bez `odslon()` obok zrzutów kompozycji w wysokim oknie, bilans nawiasów i obecność reguł w CSSOM, stan `<video>` w czasie. Wnioski: (1) podgląd sprawdzać także w oknie laptopa (ok. 1366×657) i bez wymuszonego odsłonięcia — wysokie okno z `odslon()` ukrywa problemy, które widzi właściciel; (2) zakaz zmian poza zakresem działa: wykonawca zgłasza zastany błąd zamiast go łatać, a architekt rozstrzyga; (3) przy plikach budowanych łańcuchowo od części do części sprawdzać bilans nawiasów CSS — błąd składni przenosił się przez 8 części

### BE-25 (BeautyEffect: podgląd części 11 — strona „Oferta” w trzech wariantach) — 2026-10-06
- Archetyp: nowy HTML podglądu na pliku bazowym (`czesc-10b.html`) — usunięcie treści strony głównej i niepotrzebnych kluczy stanu, nowa podstrona z treścią z dokumentu interfejsu (otwarcie, osiem kategorii, zamknięcie), trzy warianty układu (lista z przyklejonym podglądem w łuku, karty, łuki naprzemiennie) w widoku komputera i telefonu, nowy klucz stanu i grupa panelu
- Stawka: średnia (wzór otwarcia dla kolejnych podstron wybiera właściciel)
- Niepewność: średnia (nowa podstrona, trzy niezależne kompozycje, przenikanie podglądu na najechanie i fokus)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (1 przebieg, 533 s)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — odbiór w przeglądarce architekta (zrzuty 3 warianty × 2 widoki × 2 motywy; okno laptopa 1366×657 bez `odslon()` z przewinięciem do stopki; przenikanie podglądu OF-1 na najechanie i fokus, przy ograniczonym ruchu bez przejścia; bilans nawiasów CSS i reguły w CSSOM; konsola 0 błędów); odstępstwo od reguły 13 dla materiału podglądowego
- Dopuszczone alternatywy: Claude `wykonawca` (pula ŻÓŁTA, tydzień 77–78 %); Gemini `high` (słabsze wyniki na HTML podglądu); Spark (ostatni sygnał: zablokowany, 402)
- Powód wyboru: Codex — przyjęte BE-16, BE-18…BE-20 i BE-22…BE-24 na tych samych plikach bazowych
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Spark zablokowany (402, ostatni odczyt), Claude ostrzegawczy (ŻÓŁTY, tydzień 77–78 %), 2026-10-06
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: przyjęty bez rundy korekt; treść, klucze stanu, `aria-current` i układy zgodne z briefem
- Rundy korekt: 0; jedna poprawka architekta (trzy reguły CSS) — plamy tła otwarcia OF-2 brały jasne `--blob1`/`--blob2` także w ciemnym motywie (jasna poświata za białym tekstem) i były ucinane krawędzią sekcji; dodano wariant ciemny na `--glow1` jak na stronie głównej i wygaszenie maską ku dołowi
- Czas do akceptacji: ok. 9 min przebiegu + ok. 25 min walidacji
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): architekt — (1) P2: OF-2 w ciemnym motywie — jasna poświata za białym tekstem otwarcia i ostra pozioma krawędź tła; potwierdzone na zrzutach, poprawione. Brief nie wskazał, że strona główna ma osobne reguły plam dla ciemnego motywu — luka briefu, nie wykonawcy
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: zrzuty w obu motywach i widokach, okno laptopa bez `odslon()` z przewinięciem kółkiem nad sceną (kursor nad panelem nie przewija sceny), stan klasy aktywnej i `transition` w podglądzie OF-1 przy zwykłym i ograniczonym ruchu. Wniosek: przy nowym elemencie dekoracyjnym brief ma wskazać istniejący odpowiednik i jego reguły dla ciemnego motywu — zmienne palety podglądu nie są w całości przedefiniowane w ciemnym motywie

### BE-26 (BeautyEffect: podgląd części 12 — strona „O nas” w trzech grupach wariantów) — 2026-10-06
- Archetyp: nowy HTML podglądu na pliku bazowym (`czesc-11.html`) — usunięcie treści „Oferty” i jej klucza stanu, nowa podstrona z treścią z dokumentu interfejsu (otwarcie wg wybranego wzoru, wyróżnienia, komfort, zespół, zamknięcie), trzy niezależne grupy po trzy warianty (9 układów) w widoku komputera i telefonu, trzy klucze stanu i grupy panelu z przewinięciem do sekcji, przeniesienie `aria-current` w czterech menu
- Stawka: średnia (wygląd strony „O nas” wybiera właściciel; zdjęcia i dane osób z Booksy)
- Niepewność: średnia (trzy grupy wariantów naraz, nowe zdjęcia zespołu dostarczone w trakcie, ikona spoza PrimeIcons)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (3 przebiegi: 62,9 s i 67,1 s — zasadne zatrzymania na błędach briefu; 465,7 s — wynik)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — odbiór w przeglądarce architekta (zrzuty 3 kombinacje × 2 widoki × 2 motywy w oknie mieszczącym całą stronę; okno laptopa 1366×657 bez `odslon()` z przewinięciem do stopki; przyciski grup; konsola 0 błędów; elementy poza `.site`; bilans nawiasów CSS, unikalne id, `aria-current`, obrazy); odstępstwo od reguły 13 dla materiału podglądowego
- Dopuszczone alternatywy: Claude `wykonawca` (pula ŻÓŁTA, tydzień 78 %); Gemini `high` (słabsze wyniki na HTML podglądu); Spark (ostatni sygnał: zablokowany, 402)
- Powód wyboru: Codex — przyjęte BE-16, BE-18…BE-20 i BE-22…BE-25 na tych samych plikach bazowych
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Spark zablokowany (402, ostatni odczyt), Claude ostrzegawczy (ŻÓŁTY, tydzień 78 %), 2026-10-06
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: dwa pierwsze przebiegi zatrzymane zgodnie z klauzulą STOP — (1) brief podawał błędną liczbę menu z `aria-current` i zakładał zachowanie przewinięcia przy zmianie widoku, którego plik bazowy nie ma; (2) ogólna reguła „identycznej dostępnej treści” przeczyła opisom wariantów. Oba zarzuty trafne; brief poprawiony (dodana reguła pierwszeństwa opisu wariantu nad regułą ogólną). Trzeci przebieg przyjęty po dwóch poprawkach architekta
- Rundy korekt: 0 po wyniku (2 przebiegi powtórzone na błędach briefu); dwie poprawki architekta — (1) wyjątek w obsłudze kliknięć przepuszczał `Zobacz ofertę` w zamknięciu do nawigacji (właściciel opuściłby podgląd); (2) nadmiarowe `</div>` w KB-3 zamykało `.site`, przez co zespół, zamknięcie i stopka wypadały poza stronę, a przewinięcie do sekcji rzucało błąd
- Czas do akceptacji: ok. 10 min trzech przebiegów + ok. 35 min walidacji (w tym ponowne zrzuty)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): architekt — (1) P1: nadmiarowe `</div>` zamykające `.site` w wariancie KB-3 (sekcje poza kontenerem, błąd `replaySection`); potwierdzone, poprawione; (2) P2: wyjątek nawigacji dla `/oferta` w zamknięciu wbrew regule podglądu; potwierdzone, poprawione
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: zrzuty całej strony w oknie wyższym niż strona (zrzut elementu w przewijanym kontenerze obejmuje tylko część widoczną — reszta wychodzi pusta), przewinięcie sceny na górę przed zrzutem (przyciski grup przewijają scenę), sprawdzenie, że żadna sekcja ani stopka nie leży poza `.site`. Wniosek: bilans nawiasów i walidacja id nie wykrywają błędnego zagnieżdżenia — przy każdym wariancie sprawdzać rodzica sekcji w DOM

### BE-27 (BeautyEffect: podgląd części 13 — strona „Jak się umówić” w trzech grupach wariantów) — 2026-10-06
- Archetyp: nowy HTML podglądu na pliku bazowym (`czesc-12.html`) — usunięcie treści „O nas” i jej kluczy stanu, nowa podstrona z treścią z dokumentu interfejsu (otwarcie, kroki, kontakt z godzinami, zasady, karta podarunkowa, zamknięcie ze wskazówkami), trzy grupy po trzy warianty i jedna sekcja o stałym układzie, w widoku komputera i telefonu
- Stawka: średnia (wygląd strony „Jak się umówić” wybiera właściciel)
- Niepewność: średnia (grafiki rysowane w CSS — bon, kupon z perforacją; lista godzin z innego pliku podglądu)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (2 przebiegi: 62,6 s — zasadne zatrzymanie na błędzie briefu; 484,7 s — wynik)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — odbiór w przeglądarce architekta (zrzuty 3 kombinacje × 2 widoki × 2 motywy w oknie mieszczącym całą stronę; zbliżenia kuponu i osi; okno laptopa 1366×657 bez `odslon()` z przewinięciem do stopki; przyciski grup; odnośnik wewnętrzny bez nawigacji; sekcje wewnątrz `.site`; konsola 0 błędów; reguła ograniczonego ruchu); odstępstwo od reguły 13 dla materiału podglądowego
- Dopuszczone alternatywy: Claude `wykonawca` (pula ŻÓŁTA, tydzień 79 %); Gemini `high` (słabsze wyniki na HTML podglądu); Spark (ostatni sygnał: zablokowany, 402)
- Powód wyboru: Codex — przyjęte BE-16, BE-18…BE-20 i BE-22…BE-26 na tych samych plikach bazowych
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Spark zablokowany (402, ostatni odczyt), Claude ostrzegawczy (ŻÓŁTY, tydzień 79 %), 2026-10-06
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: pierwszy przebieg zatrzymany zgodnie z klauzulą STOP — brief kazał kopiować `aria-label` przycisku `Zadzwoń` z nagłówka, którego ten przycisk nie ma; zarzut trafny, brief poprawiony. Drugi przebieg przyjęty po dwóch poprawkach architekta
- Rundy korekt: 0 po wyniku (1 przebieg powtórzony na błędzie briefu); dwie poprawki architekta w CSS — (1) karty wskazówek w zamknięciu dziedziczyły szerokość 900 px wzoru zamknięcia (tytuł łamany na cztery linie) — poszerzone do szerokości kontenera; (2) wycięcia perforacji kuponu KP-3 w kolorze tła były prawie niewidoczne na jasnej karcie — dodane obramowanie, średnica 32 px, wyraźniejsza linia przerywana
- Czas do akceptacji: ok. 9 min dwóch przebiegów + ok. 25 min walidacji
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): architekt — (1) P2: zbyt wąska siatka kart wskazówek w zamknięciu; (2) P3: słabo widoczne wycięcia kuponu; oba potwierdzone na zrzutach i poprawione. Oba wynikały z briefu (brak szerokości siatki, wycięcia opisane wyłącznie kolorem tła), nie z wykonania
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: zrzuty całej strony w oknie wyższym niż strona, sprawdzenie rodzica sekcji w DOM, zbliżenia drobnych ozdób w obu motywach. Wniosek: przy umieszczaniu nowej treści w stałym wzorze (`sub-close`) brief ma podać szerokość nowej treści, bo wzór niesie własne ograniczenia; ozdoba „w kolorze tła” na jasnej karcie potrzebuje obrysu

### BE-28 (BeautyEffect: podgląd części 13b — grafika przy krokach rezerwacji i zdjęcie na karcie podarunkowej) — 2026-10-06
- Archetyp: poprawka HTML podglądu na pliku bazowym (`czesc-13.html`) po wyborze właściciela — utrwalenie trzech wybranych wariantów i usunięcie pozostałych z kluczami stanu, dwie nowe grupy po trzy warianty (grafika obok kroków tylko w widoku komputera, w tym makieta telefonu z kalendarzem w CSS; zdjęcie na karcie podarunkowej w trzech kadrach), nowe klucze stanu i grupy panelu
- Stawka: średnia (wygląd strony „Jak się umówić” wybiera właściciel)
- Niepewność: niska–średnia (odpowiedź na dwie konkretne uwagi właściciela; makieta telefonu przeniesiona z części 10b)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (1 przebieg, 458,2 s)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — odbiór w przeglądarce architekta (zrzuty 3 × 3 warianty × 2 widoki × 2 motywy w oknie mieszczącym całą stronę; porównanie makiety telefonu w obu motywach; okno laptopa 1366×657 bez `odslon()` z przewinięciem do stopki dla każdego wariantu grafiki; konsola 0 błędów; elementy poza `.site`, unikalne id, `aria-current`, obrazy; wystawanie grafiki poza sekcję kroków); odstępstwo od reguły 13 dla materiału podglądowego
- Dopuszczone alternatywy: Claude `wykonawca` (pula ŻÓŁTA, tydzień 79 %); Gemini `high` (słabsze wyniki na HTML podglądu); Spark (ostatni sygnał: zablokowany, 402)
- Powód wyboru: Codex — przyjęte BE-16, BE-18…BE-20 i BE-22…BE-27 na tych samych plikach bazowych
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Spark zablokowany (402, ostatni odczyt), Claude ostrzegawczy (ŻÓŁTY, tydzień 79 %), 2026-10-06
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: przyjęty po jednej poprawce architekta. Przed wysłaniem architekt sprawdził przesłanki briefu i poprawił dwie błędne (brief podawał nieistniejący plik logo i ikonę nagłówka, której nagłówek nie używa)
- Rundy korekt: 0; jedna poprawka architekta — makieta telefonu w ciemnym motywie miała białą ramkę ekranu, bo brief zabraniał prymitywów palety i Codex podstawił kolory semantyczne odwracające się w ciemnym motywie; przywrócone kolory ramki z części 10b (prymitywy szarości, osobne wartości dla ciemnego motywu). Przyczyna po stronie briefu, nie wykonawcy
- Czas do akceptacji: ok. 8 min przebiegu + ok. 30 min walidacji
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): architekt — (1) P2: odwrócona kolorystyka ramki telefonu w ciemnym motywie; potwierdzone, poprawione (luka briefu)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: jak w BE-26 (okno wyższe niż strona, scena przewinięta na górę, rodzic sekcji w DOM) oraz porównanie obu motywów dla każdego elementu przeniesionego z wcześniejszej części. Wniosek: zakaz prymitywów w briefie musi mieć wyjątek dla elementów kopiowanych z zatwierdzonego podglądu — inaczej wykonawca „naprawia” je kolorami semantycznymi, które w ciemnym motywie się odwracają

### BE-29 (BeautyEffect: generator statycznego planu okolicy salonu z danych OpenStreetMap do SVG) — 2026-10-06
- Archetyp: skrypt Pythona (biblioteka standardowa) przetwarzający dane Overpass (ok. 2,2 tys. obiektów) na SVG bez kolorów — rzutowanie lokalne, upraszczanie Douglasa–Peuckera, klasyfikacja warstw, etykiety ulic po ścieżkach z wyborem fragmentu i kolizjami, samosprawdzenie wyniku, podgląd jasny/ciemny
- Stawka: niska–średnia (materiał podglądowy do wyboru sposobu prezentacji mapy; bez danych osobowych)
- Niepewność: średnia (nowy archetyp — przetwarzanie danych geograficznych; jakość etykiet oceniana dopiero wizualnie)
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` (`-Access write`; 2 przebiegi: 787,9 s — wynik, 326,9 s — poprawka)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — odbiór architekta (podgląd jasny/ciemny w przeglądarce, plan w trzech polach strony w obu motywach i na telefonie, unikalność `id` po wstawieniu trzech kopii, przegląd skryptu pod kątem kierunku obrysów); odstępstwo od reguły 13 dla materiału podglądowego
- Dopuszczone alternatywy: Codex `gpt-6.1-sol` `high` (zajęty równoległym briefem strony, mała pula Plus); Claude `wykonawca` (pula ŻÓŁTA, tydzień 79 %); Spark (ostatni sygnał: zablokowany, 402)
- Powód wyboru: samodzielny skrypt z jasnym wynikiem do sprawdzenia, rozłączny z briefem strony — rozłożenie fali na dwie linie zamiast dwóch przebiegów Codexa; brak lokalnych wyników Gemini dla tego archetypu (pewność niska)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany, Codex nieznany, Spark zablokowany (402, ostatni odczyt), Claude ostrzegawczy (ŻÓŁTY, tydzień 79 %), 2026-10-06
- Pewność decyzji: niska (pierwszy brief tego archetypu)
- Wynik pierwszego podejścia: przyjęty wizualnie; sekcja „co błędne” zgłosiła dwa trafne zarzuty wobec briefu — stała długości 1° szerokości dla równika zamiast dla 51,95° N oraz brak ujednolicenia kierunku obrysów przy łączeniu wielokątów w jedną ścieżkę (ryzyko dziur przy `nonzero`); dwa pozostałe uwzględnione bez zmiany (okno doboru etykiet szersze niż wąskie pola — celowe; pominięcie jednej ulicy przez próg kolizji)
- Rundy korekt: 1 (poprawka obu trafnych zarzutów — brief architekta był źródłem obu); 0 po poprawce
- Czas do akceptacji: ok. 13 min przebiegu + ok. 5,5 min poprawki + ok. 15 min oceny (równolegle z briefem strony)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): wykonawca (sekcja „co błędne”) — P2 stała skali osi y, P2 kierunek obrysów; potwierdzone, poprawione. Architekt — brak dodatkowych
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: samosprawdzenie skryptu (parsowanie XML, brak atrybutów stylu, unikalne `id` z prefiksem, poprawne odwołania `href`, rozmiar ≤ 300 KB), znak pola wszystkich podścieżek obszarów, ocena wizualna obu motywów. Uwaga procesowa: Gemini zostawił katalog `__pycache__` (import skryptu) — architekt usunął po przebiegu, zgodnie z pamięcią o blokadach katalogów

### BE-30 (BeautyEffect: podgląd części 14 — strona „Kontakt” z trzema sposobami prezentacji mapy) — 2026-10-06
- Archetyp: nowy HTML podglądu na pliku bazowym (`czesc-13b.html`) — usunięcie treści poprzedniej strony i jej kluczy stanu, nowa podstrona z treścią z dokumentu interfejsu, trzy grupy po trzy warianty (sposoby kontaktu, mapa, układ godzin i adresu — 27 kombinacji), wczytanie planu SVG do trzech pól z przepisaniem `id`, mapa Google ładowana dopiero po kliknięciu z przywracaniem zaślepki, przeniesienie `aria-current`
- Stawka: średnia (wygląd strony „Kontakt” i decyzja właściciela o mapie i plikach cookies)
- Niepewność: średnia (zależność od pliku SVG powstającego równolegle, interakcja z zasobem zewnętrznym)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (2 przebiegi: 64,1 s — zasadne zatrzymanie na błędzie briefu; 751,8 s — wynik)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — odbiór w przeglądarce architekta (zrzuty 3 warianty kontaktu i 9 kombinacji mapy z układem × 2 motywy × komputer/telefon; brak żądań do Google przed kliknięciem, `iframe` z fokusem po kliknięciu, przywrócenie zaślepki po zmianie wariantu; okno laptopa 1366×657 bez `odslon()` dla 9 kombinacji; konsola 0 błędów; sekcje w `.site`, unikalne `id` po wstawieniu planu, `aria-current`, obrazy); odstępstwo od reguły 13 dla materiału podglądowego
- Dopuszczone alternatywy: Claude `wykonawca` (pula ŻÓŁTA, tydzień 79 %); Gemini `high` (zajęty równoległym generatorem; słabsze wyniki na HTML podglądu); Spark (ostatni sygnał: zablokowany, 402)
- Powód wyboru: Codex — przyjęte BE-16, BE-18…BE-20 i BE-22…BE-28 na tych samych plikach bazowych
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Gemini nieznany, Spark zablokowany (402, ostatni odczyt), Claude ostrzegawczy (ŻÓŁTY, tydzień 79 %), 2026-10-06
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: pierwszy przebieg zatrzymany zgodnie z klauzulą STOP — brief wymieniał stopkę jako jedno z czterech menu z `aria-current`, a stopka nie ma menu (czwarte to nagłówek alternatywny); zarzut trafny, brief poprawiony. Drugi przebieg przyjęty po jednej poprawce architekta
- Rundy korekt: 0 po wyniku; jedna poprawka architekta — podmiana zdjęcia prawego łuku otwarcia (obrócone zdjęcie brwi z ciemnym pasem włosów u dołu → zdjęcie ust); błąd doboru zdjęcia po stronie briefu, nie wykonawcy
- Czas do akceptacji: ok. 1 min + 12,5 min przebiegów + ok. 25 min walidacji
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): architekt — P3: niefortunny kadr zdjęcia w prawym łuku (luka briefu); poprawione
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: jak w BE-26 (okno wyższe niż strona, scena na górze, rodzic sekcji w DOM) oraz test sieci dla wariantu ładowanego po zgodzie (zero żądań przed kliknięciem) i unikalność `id` po wstawieniu treści przez skrypt. Wniosek: przy przenoszeniu `aria-current` brief podaje menu po klasach, a nie z pamięci

### BE-31 (BeautyEffect: podgląd części 15 — elementy stron kategorii „Warkocze” i „Makijaż permanentny”) — 2026-10-06
- Archetyp: nowy HTML podglądu na pliku bazowym (`czesc-14.html`) z przeniesionym blokiem wariantu KA-1 z `czesc-8.html` — dwie strony kategorii w jednym pliku, zakładki grup, trzy grupy po trzy warianty (długi opis: rozwinięcie / okno z arkuszem na telefonie / szeroka karta; przed i po zabiegu: ramki / zakładki / oś; zasada grupy: notka / lista / kafelki), przenoszenie treści do okna bez duplikatów `id`, zamykanie arkusza na cztery sposoby
- Stawka: średnia (wygląd stron kategorii z dłuższymi opisami i zasadami przygotowania)
- Niepewność: średnia (dwa źródła stylu, interakcje okna i zakładek, treść z dokumentów interfejsu z dwoma szkicami opisów)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (3 przebiegi: 38,5 s i 42,4 s — zasadne zatrzymania na błędach briefu; 1108,8 s — wynik)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — odbiór w przeglądarce architekta (zrzuty obu stron × DO/PZ/ZW × komputer/telefon × jasny/ciemny; okno: pułapka fokusu, Escape, tło, przycisk, przeciągnięcie uchwytu poniżej i powyżej progu, powrót fokusu; zakładki z klawiatury; brak duplikatów `id` przy otwartym oknie; okno laptopa 1366×657 bez `odslon()`; ograniczony ruch; konsola 0 błędów; sekcje w `.site`, `aria-current`, brak nowych HEX); odstępstwo od reguły 13 dla materiału podglądowego
- Dopuszczone alternatywy: Claude `wykonawca` (pula ŻÓŁTA, tydzień ok. 80 %); Gemini `high` (słabsze wyniki na HTML podglądu); Spark (ostatni sygnał: zablokowany, 402)
- Powód wyboru: Codex — przyjęte BE-16, BE-18…BE-20, BE-22…BE-28 i BE-30 na tych samych plikach bazowych
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Gemini nieznany, Spark zablokowany (402, ostatni odczyt), Claude ostrzegawczy (ŻÓŁTY, tydzień ok. 80 %), 2026-10-06
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: dwa przebiegi zatrzymane zgodnie z klauzulą STOP, oba trafnie — (1) sprawdzenie briefu zakazywało `google.com/maps`, a niezmieniona stopka ma odnośnik do wyznaczania trasy; (2) brief podawał klasę karty `accent-card`, która należy do wariantu KA-3, a wybrany był KA-1 (`treatment`). Trzeci przebieg przyjęty po poprawkach architekta
- Rundy korekt: 0 po wyniku; poprawki architekta w pliku — kadr dwóch banerów (`--pos`: twarz ucięta na ustach, warkocze poza kadrem) oraz usunięcie zdegenerowanych wariantów PZ-2/PZ-3 przy karcie bez treści przed/po (jedna zakładka „Opis”, jednoetapowa oś); obie luki briefu, nie wykonawcy
- Czas do akceptacji: ok. 1,5 min zatrzymań + 18,5 min przebiegu + ok. 35 min walidacji
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): architekt — P3 kadr banerów, P3 pojedyncza zakładka i jednoetapowa oś; poprawione
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: jak w BE-30 oraz test okna/arkusza (cztery sposoby zamknięcia, próg przeciągnięcia, fokus) i brak duplikatów `id` po przeniesieniu treści do okna. Wnioski: (1) klasy przenoszonego wariantu brief weryfikuje w obrębie bloku tego wariantu, nie globalnym zliczeniem; (2) zakazy w sprawdzeniach briefu nie mogą obejmować elementów powłoki, które mają zostać bez zmian; (3) brief wariantów przekrojowych mówi, co zrobić z kartą, która nie ma treści dla wariantu; (4) przy skali ekranu ≠ 1 zrzuty elementów z Playwright są przesunięte — kadrować zrzut całego okna według `getBoundingClientRect` × (szerokość obrazu / `innerWidth`)

### BE-32 (BeautyEffect: podgląd części 16 — „Polityka prywatności” i strona 404) — 2026-10-06
- Archetyp: nowy HTML podglądu na pliku bazowym (`czesc-14.html`) z mechanizmem dwóch stron przeniesionym z `czesc-15.html`; trzy grupy po trzy warianty (otwarcie dokumentu, układ długiego tekstu ze spisem przyklejonym / ramką spisu / sekcjami rozwijanymi z `hidden="until-found"`, strona 404), przewijanie sceny do sekcji z fokusem na nagłówku, śledzenie czytanej sekcji
- Stawka: niska–średnia (strona prawna bez treści normatywnej i strona błędu; materiał podglądowy)
- Niepewność: niska (wzór otwarcia i zamknięcia zaakceptowany, treść z dokumentów interfejsu)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (1 przebieg, 662 s)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — odbiór w przeglądarce architekta (zrzuty wybranych wariantów komputer/telefon × jasny/ciemny, pozostałe warianty na komputerze; spis: przewinięcie, wyróżnienie, fokus, zwijanie na telefonie; 404: jeden `<h1>`, cztery odnośniki z właściwymi adresami; `aria-current` w stopce; konsola: tylko brak `favicon.ico` serwera podglądu); odstępstwo od reguły 13 dla materiału podglądowego
- Dopuszczone alternatywy: Claude `wykonawca` (pula ŻÓŁTA, tydzień 81 %); Gemini `high` (słabsze wyniki na HTML podglądu); Spark (ostatni sygnał: zablokowany, 402)
- Powód wyboru: Codex — przyjęte BE-16, BE-18…BE-20, BE-22…BE-28, BE-30 i BE-31 na tych samych plikach bazowych
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Gemini nieznany, Spark zablokowany (402, ostatni odczyt), Claude ostrzegawczy (ŻÓŁTY, tydzień 81 %), 2026-10-06
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: przyjęty; wykonawca sam przeszedł symulacją DOM 216 kombinacji stanu. Jedno odchylenie zgłoszone trafnie (`transparent` jako wypełnienie obrysowanej liczby wbrew regule „tylko zmienne”)
- Rundy korekt: 0; poprawki architekta w pliku — obrys liczby `404` (`-webkit-text-stroke` na kroju Cormorant rysuje nakładające się kontury cyfry 4; zamiast przezroczystego wypełnienia: wypełnienie tłem `var(--bg)` + `paint-order: stroke fill`) oraz wymiana zdjęcia prawego łuku (szare tło zdjęcia widoczne pod środkowym łukiem) — oba to luki briefu (dobór zdjęcia i techniki obrysu przez architekta), nie wykonawcy
- Czas do akceptacji: 11 min przebiegu + ok. 30 min walidacji (z przerwą na restart serwerów podglądu)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): architekt — P3 obrys `404`, P3 kadr prawego łuku; poprawione
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: jak w BE-31 oraz przewinięcie do sekcji ze spisu (położenie nagłówka pod nagłówkiem strony, fokus, wyróżnienie pozycji). Wnioski: (1) obrys tekstu w kroju szeryfowym wymaga `paint-order: stroke fill` z wypełnieniem kolorem tła — `-webkit-text-stroke` z przezroczystym wypełnieniem pokazuje wewnętrzne kontury glifów; (2) zdjęcie bocznego łuku OF-3 dobiera się po dolnej krawędzi — prawy łuk wystaje pod środkowym, więc jednolite tło na dole zdjęcia wygląda jak pasek; (3) właściciel potrafi wybrać z opisu słownego zanim podgląd jest gotowy — podgląd i tak publikuje się na wybranych wariantach do potwierdzenia

### BE-33 (BeautyEffect: odczyt wartości wyglądu z 19 makiet HTML pod specyfikację wyglądu) — 2026-10-06
- Archetyp: odczyt (ekstrakcja) wartości CSS/HTML/JS wybranych wariantów z 19 podglądów HTML do jednego pliku z odnośnikami `plik:linia`, z dopasowaniem kolorów do skal dokumentu kolorów i tabelą rozbieżności między makietami; tylko odczyt plików wejściowych, jeden plik wynikowy w kopii roboczej
- Stawka: niska–średnia (podstawa specyfikacji wyglądu, którą pisze architekt; katalog nie jest źródłem prawdy)
- Niepewność: średnia (makiety z kolejnych etapów, warianty odrzucone w tych samych plikach, trzy mechanizmy szerokości)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (3 przebiegi: 80 s, 120 s, 1508 s)
- Recenzent (linia / model / native effort): brak recenzji innej rodziny — odbiór architekta: 26 wartości porównanych z liniami makiet (wszystkie zgodne), podsumowania sekcji przeczytane w całości, pliki wejściowe bez zmian (`cmp`), brak ścieżek lokalnych w wyniku; odstępstwo od reguły 13 dla materiału pomocniczego
- Dopuszczone alternatywy: Gemini `high` (tańszy odczyt, słabsze wyniki na HTML podglądu); Claude `zwiadowca` (Haiku `low` — za słaby do rozdzielenia wariantów i kaskady CSS); Spark (ostatni sygnał: zablokowany, 402)
- Powód wyboru: Codex — przyjęte BE-16…BE-32 na tych samych plikach
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Gemini nieznany, Spark zablokowany (402, ostatni odczyt), Claude ostrzegawczy (ŻÓŁTY, tydzień 82 %), 2026-10-06
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zatrzymanie — trafne zgłoszenie błędnego założenia briefu (widok telefonu opisany tylko przez `data-view`, a późniejsze makiety używają też `@container`); drugi przebieg — zatrzymanie zbędne (rozbieżność opisu filmów z kodem potraktowana jako błąd założeń); trzeci — przyjęty
- Rundy korekt: 0 korekt wyniku; 2 poprawki briefu przez architekta (obie to luki briefu, nie wykonawcy)
- Czas do akceptacji: ok. 28 min przebiegów + ok. 30 min odbioru
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): wykonawca wykazał 23 rozbieżności wspólnych elementów między makietami oraz różnice z decyzjami (m.in. grubości Cormoranta w motywie ciemnym, brak kursywy N-1 i wysuwania słów W-3 na podstronach, ikona `roz-700` zamiast `roz-600`, niedziałający selektor w części 13b, limit filmu 5 s sprawdzany zdarzeniem postępu) — potwierdzone, rozstrzygnięte w specyfikacji wyglądu
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: wyrywkowe porównanie wartości z liniami makiet, `cmp` plików wejściowych, przegląd wyniku pod kątem ścieżek lokalnych. Wnioski: (1) brief odczytu z makiet musi wymienić wszystkie mechanizmy szerokości (`data-view`, `@container`, `cqi`, `@media`); (2) sama klauzula STOP przy briefie odczytu powoduje zbędne zatrzymania — brief odczytu mówi wprost, że rozbieżność opisu z kodem zapisuje się i pracuje dalej, a zatrzymanie tylko przy niewykonalności; (3) odczyt „wszystkiego” dał 600 KB (4158 wierszy) — do napisania specyfikacji wystarczyły podsumowania na początku sekcji; przy podobnym briefie żądać najpierw podsumowań, a katalogów szczegółowych tylko dla elementów wspólnych

### BE-34 (BeautyEffect: Etap 1 Z1 — paleta, role kolorów i preset PrimeNG) — 2026-10-07
- Archetyp: motyw PrimeNG z dokumentu kolorów — prymitywy (3 skale 50–950 + kolory stanów), 29 ról na motyw jako własne tokeny `bty`, mapowanie prymityw → semantyka w `definePreset(Aura)`, testy wartości; ≤ 5 plików, jedna warstwa (theme)
- Stawka: średnia (podstawa kontrastu WCAG AA w obu motywach; bez niezmiennika wysokiej stawki)
- Niepewność: niska–średnia (wartości z tabeli dokumentu, nowy mechanizm własnych tokenów `--p-bty-*`)
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie (943 s; korekty Z1-K1 634 s i część B K-G1)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (159 s), tylko odczyt
- Dopuszczone alternatywy: Codex `gpt-6.1-sol` `high` (w tej fali pisał Z2 — rozłączne pliki, druga rodzina na krzyżową recenzję); Claude `wykonawca` (pula ŻÓŁTA, tydzień 84 %); Spark (ostatni sygnał: zablokowany, 402)
- Powód wyboru: brief tekstowy z tabelą wartości, bez Figmy i bez kontekstu sesji; Gemini i Codex równolegle dają recenzję krzyżową dwóch rodzin w jednej fali
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany, Codex nieznany, Spark zablokowany (402, ostatni odczyt), Claude ostrzegawczy (ŻÓŁTY, tydzień 84 %), 2026-10-06 21:30
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: przyjęty z poprawkami (recenzja: P2 brak mapowania kolorów pól formularza, P3 dodatkowe deklaracje typów w pliku specu — potwierdzone)
- Rundy korekt: 2 — Z1-K1 (znaleziska recenzji) i część B K-G1: test ról po Z1-K1 porównywał preset ze stałą źródłową (tautologia; luka briefu korekty architekta, nie wykonawcy) — zastąpiony specem z literałami z dokumentu (60 testów)
- Czas do akceptacji: ok. 36 min przebiegów + walidacja fali
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1 × P2, 1 × P3 potwierdzone; architekt — test wartości ról bez niezależnej wyroczni (P2), poprawione
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: Vitest (wartości ról względem literałów z tabeli dokumentu, zbiór kluczy w obu motywach), skan HEX poza `palette.ts`, `lint`, `format:check`, build. Wnioski: (1) wyrocznia testu wartości to literały z dokumentu, nigdy stała źródłowa — brief korekty, który każe „porównać z `lightSchemeTokens`”, zamienia test wartości w test podpięcia; (2) `definePreset` scala głęboko — nie porównywać tożsamości obiektów presetu; (3) brak `.gitattributes` przy `autocrlf=true` daje CRLF i 72 pliki z błędem Prettiera — dodać przy szkielecie repo

### BE-35 (BeautyEffect: Etap 1 Z2 — ThemeMode i skrypt startowy motywu bez mignięcia) — 2026-10-07
- Archetyp: serwis sygnałowy SSR-safe (ngx-webstorage, `.app-dark` na `<html>`, View Transitions z obejściem przy ograniczeniu ruchu) + blokujący skrypt w `index.html` czytający zapisany wybór lub `prefers-color-scheme`; testy serwisu i skryptu w jsdom
- Stawka: średnia (pierwsze malowanie i zgodność SSR/hydracji; bez niezmiennika wysokiej stawki)
- Niepewność: średnia (View Transitions w jsdom, kolejność skrypt → styl → hydracja)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (203 s; korekta Z2-K1 `medium` 81 s)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie (670 s), tylko odczyt
- Dopuszczone alternatywy: Gemini `high` (w tej fali pisał Z1); Claude `wykonawca` (pula ŻÓŁTA); Spark (zablokowany, 402)
- Powód wyboru: logika z przypadkami brzegowymi SSR i platformy — Codex przyjęty bez korekt na podobnych briefach logiki; recenzja krzyżowa z Z1
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Gemini nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 84 %), 2026-10-06 21:30
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: przyjęty z poprawkami
- Rundy korekt: 1 (Z2-K1, `medium`)
- Czas do akceptacji: ok. 5 min przebiegów + recenzja 11 min + walidacja fali
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 2 × P2 (wyjątek `startViewTransition` rozjeżdża sygnał i klasę; asynchroniczny rozjazd sygnału z klasą w trakcie przejścia), 2 × P3 (zbędne przejście przy tym samym stanie; brak stylu tła płótna dla `.app-dark` przed hydracją) — wszystkie potwierdzone i poprawione
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: Vitest serwisu (14) i skryptu startowego (8, w tym styl płótna), `lint`, `format:check`, build. Wniosek: recenzja Gemini trafnie wychwyciła przypadki brzegowe API przeglądarki (wyjątek, kolejność) — przy podobnej logice platformowej warto ją utrzymać

### BE-36 (BeautyEffect: Etap 1 Z3 — kroje, skala pisma, rytm, ruch i style globalne) — 2026-10-07
- Archetyp: SCSS fundamentów — `@font-face` z fontsource (WOFF2, `latin-ext`), 22 mixiny ról pisma bez emitowanego CSS, progi Bootstrapa, zmienne rytmu i ruchu, odnośniki, style globalne, preload krojów w `index.html`, kopiowanie krojów w `angular.json`, test zakresów Unicode
- Stawka: średnia (wszystkie późniejsze ekrany dziedziczą pismo i ruch; polskie znaki są wymaganiem blokującym)
- Niepewność: średnia (ścieżki krojów w buildzie, warunki ruchu `hover`/`reduce`)
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie (709 s; korekta w K-G1 część A, 585 s łącznie z częścią B)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (152 s), tylko odczyt
- Dopuszczone alternatywy: Codex `gpt-6.1-sol` `high` (w tej fali pisał Z4); Claude `wykonawca` (pula ŻÓŁTA); Spark (zablokowany, 402)
- Powód wyboru: brief tekstowy z tabelą wartości ze specyfikacji wyglądu; recenzja krzyżowa z Z4 w tej samej fali
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany, Codex nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 84 %), 2026-10-06 22:00
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: przyjęty z poprawkami
- Rundy korekt: 1 (K-G1 część A)
- Czas do akceptacji: ok. 12 min przebiegu + recenzja + korekta ok. 10 min + walidacja
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): recenzja — 2 × P2 (kolor nieaktywnej zakładki; przesunięcie strzałki bez warunku `hover: hover`) potwierdzone; architekt — przejście koloru odnośnika poza `prefers-reduced-motion: no-preference` (P2), podkreślenie odnośnika ze strzałką pod strzałką (P3); poprawione
- Defekty po odbiorze: 1 — role Jostu (`eyebrow`, `footer-heading` itd.) nie ustawiały kroju i na elemencie nagłówka/w nagłówku dziedziczyły Cormoranta z globalnej reguły `h1–h4`; wykrył wykonawca Z5b (trafne zatrzymanie), poprawione korektą K-Z3 (Gemini `high`, 307 s; 20 ról z jawnym krojem przez `$font-serif`/`$font-sans`, test wycinający ciała mixinów), recenzja Codex `gpt-6.1-sol` `high`: poprawne. Wniosek: brief mixinów pisma musi wymagać kroju w każdej roli, bo komponentom nie wolno deklarować `font-family`
- Wymagane testy i dowody: Vitest krojów (zakresy Unicode liczbowo, ścieżki `url()` i preloadów), stylelint, `lint`, `format:check`, build z 8 plikami WOFF2 w `dist/.../fonts/`. Wniosek: przy ruchu w SCSS Gemini pomija warunek `hover: hover` i umieszcza przejście poza blokiem `no-preference` — brief ruchu podaje oba warunki jako osobne punkty definicji ukończenia

### BE-37 (BeautyEffect: Etap 1 Z4 — przyciski R-2 „Uniesienie” w presecie PrimeNG) — 2026-10-07
- Archetyp: tokeny komponentu `button` w presecie Aury (warianty wypełniony, obrysowy, mały, przycisk-ikona) + hak `css` komponentu z wymiarami, wyglądem najechania/fokusu/naciśnięcia i ruchem pod warunkami `hover`/`reduced-motion`; testy emisji zmiennych przez `Theme.getComponent('button')`; 3 pliki
- Stawka: średnia (każdy przycisk strony; fokus klawiatury i cele dotykowe; bez niezmiennika wysokiej stawki)
- Niepewność: wysoka (kaskada haka wobec bazowych reguł PrimeNG, typy PrimeUIX, pułapka ścieżek `button.root.<severity>`)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (126 s, zatrzymanie); korekty Z4-K1 i Z4-K2 `medium` (95 s, 157 s)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie (529 s), tylko odczyt
- Dopuszczone alternatywy: Gemini `high` (w tej fali pisał Z3); Claude `wykonawca` (pula ŻÓŁTA, tydzień 84 %); Spark (zablokowany, 402)
- Powód wyboru: 3 pliki w porcji Codexa, logika kaskady i typów; recenzja krzyżowa z Z3
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Gemini nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 84 %), 2026-10-06 22:10 i 2026-10-07 06:15
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: trafne zatrzymanie — brief kazał pisać hak jako funkcję `({ dt }) => …`, a PrimeUIX typuje `css` jako `string | ((options?) => string)` (błąd briefu architekta)
- Rundy korekt: 2 — Z4-K1 (hak jako tekst z `var(--p-button-…)`), Z4-K2 (znaleziska recenzji)
- Czas do akceptacji: ok. 6 min przebiegów wykonawcy + recenzja 9 min + walidacja fali
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): potwierdzone — P1 szara obwódka fokusu przycisku-ikony (Aura ustawia `secondary.focusRing` na `surface`), P1 bazowa reguła `.p-button-outlined:active` przywraca kolory spoczynkowe, P2 naciśnięcie tylko pod `hover: hover` (specyfikacja ogranicza tylko uniesienia przy najechaniu; makieta miała je w `hover:hover`, wygrywa dokument), P2 test ruchu wycinał tylko pierwszy blok `@media`, P3 asercje bez wartości dowodowej; odrzucone — P1 „cień przy naciśnięciu” (makieta go nie gasi)
- Defekty po odbiorze: 1 — `<a pButton>` miał podkreśloną etykietę (bazowy `.p-button` PrimeUIX nie zeruje `text-decoration`, a wezwanie „Umów wizytę” do Booksy będzie odnośnikiem); widoczne dopiero na zrzucie `browser-check` `/design/komponenty`; korekta Z4-K3 (Codex `medium`, 73 s, `text-decoration: none` w haku + test). Kaskada wypełnionych/obrysowych/ikon w przeglądarce bez dalszych uwag. Wniosek: przy haku komponentu sprawdzić oba elementy nosiciela (`button` i `a`)
- Wymagane testy i dowody: Vitest emisji zmiennych (`--p-button-*` → `var(--p-bty-*)`, obwódka fokusu obu severity), wszystkie zmienne haka emitowane, ruch tylko we właściwych blokach `@media` (wszystkie wystąpienia), naciśnięcie po bloku uniesienia; skan HEX; pełny `lint`, `format:check`, `npm test`, build. Wnioski: (1) `Theme.getComponent` zwraca zmienne i hak, ale nie bazowe style `@primeuix/styles` — kaskadę haka rozstrzyga dopiero przeglądarka, brief musi wymienić konkurujące reguły bazowe; (2) recenzja Gemini z dostępem do `node_modules/@primeuix/styles` znalazła realne konflikty kaskady, których testy jednostkowe nie widzą; (3) architekt przed wysłaniem briefu korekty sprawdza położenie reguły w makiecie i treść dokumentu — pierwsza wersja Z4-K2 miała błędne założenie o makiecie, poprawione przed wysłaniem

### BE-38 (BeautyEffect: Etap 1 Z5a — `/design`: powłoka, przegląd, zaślepki stron, trasy i teksty) — 2026-10-07
- Archetyp: ekran FE bez Figmy — powłoka podglądu (nawigacja z `aria-current`, przełącznik motywu R-2, `Seo.applyTitle`), przegląd z kartami na siatce Bootstrapa, trzy zaślepki stron, trasy + `ServerRoute` (prerender), `robots.txt`, drzewo 127 tekstów `DESIGN` w `pl.json`, testy tras i AXE; ok. 20 plików
- Stawka: niska (strona pomocnicza, `noindex`, bez danych; jedynie SEO/prerender i dostępność)
- Niepewność: średnia (prerender tłumaczeń, `RouterTestingHarness`, dokładne dopasowanie `routerLinkActive`)
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie (893 s); korekta K-Z5a ta sama linia (146 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (3 przebiegi: 120 s zatrzymanie, 105 s, 87 s)
- Dopuszczone alternatywy: Codex `high` (porcja > 5 plików — odpada bez podziału); Claude `wykonawca` (pula ŻÓŁTA, tydzień 85 %); Spark (zablokowany, 402)
- Powód wyboru: dużo plików jednej warstwy i długi słownik tekstów — Gemini bez limitu 5 plików; recenzja krzyżowa z Codexem
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany, Codex nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 85 %), 2026-10-07 06:40–07:10
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: kompletny i zielony (lint, format, testy, build z 5 trasami prerenderowanymi); pierwszy build prerenderował surowe klucze — defekt istniejącego loadera SSR (osobny brief Z8), nie Z5a
- Rundy korekt: 1 — K-Z5a (`[iconOnly]="true"` na przełączniku motywu + asercja)
- Czas do akceptacji: ok. 15 min wykonawcy + 2,5 min korekty + ok. 5 min recenzji (3 przebiegi) + walidacja
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): potwierdzone — P2 przełącznik motywu bez klasy `p-button-icon-only` (PrimeNG 22 wnioskuje tryb ikony tylko z wejścia `icon`/przestarzałego `ButtonIcon`, nie ze zwykłego `<i>`), więc bez rozmiaru 44 × 44 px; trzeci przebieg — bez defektów (127 tekstów znak w znak)
- Defekty po odbiorze: 1 — lista kart przeglądu z `margin: 0` kasowała ujemne marginesy `.row`, karty wcięte o 12 px względem treści; widoczne na zrzucie `browser-check`, poprawione jednolinijkowo przez architekta (`margin-block-end: 0`)
- Wymagane testy i dowody: `RouterTestingHarness` rozróżniający `Colors`/`NotFound`, `ServerRoute` przed `**`, AXE powłoki i przeglądu, `aria-pressed` w obu stanach; build z prerenderem (tytuł, 0 surowych kluczy), `browser-check` 2×2 (16 zrzutów, 0 błędów konsoli/sieci). Wnioski: (1) klauzula STOP w briefie recenzji sprawiła, że recenzent przerwał całą recenzję po pierwszym znalezisku — brief recenzji mówi teraz wprost „zgłoś defekt i kontynuuj; zatrzymaj się tylko, gdy błędne założenie uniemożliwia recenzję”; (2) brief recenzji wymienia znane, osobno poprawiane defekty, inaczej recenzent zatrzymuje się na nich; (3) wyrównanie siatki widać tylko w przeglądarce — `browser-check` po każdej fali ekranów

### BE-39 (BeautyEffect: Etap 1 Z8 — loader tłumaczeń SSR czyta zawsze najpierw źródło) — 2026-10-07
- Archetyp: poprawka defektu istniejącego kodu SSR (kolejność katalogów w `TranslateServerLoader`) + test z `vi.mock('node:fs')` + akapit README; 3 pliki
- Stawka: średnia (prerender stron publicznych: surowe klucze zamiast tekstów w HTML dla wyszukiwarek przy buildzie z maszyny dewelopera)
- Niepewność: niska (przyczyna odtworzona przez architekta dwoma buildami)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `medium` (116 s)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie, tylko odczyt (w zbiorczej recenzji fali 4, 644 s)
- Dopuszczone alternatywy: Gemini `high`; Claude `wykonawca` (pula ŻÓŁTA); Spark (zablokowany, 402)
- Powód wyboru: krótka, dobrze określona poprawka w porcji Codexa; `medium` wystarcza przy znanej przyczynie
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Gemini nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 85 %), 2026-10-07 07:00
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: poprawny — testy czerwone 3/6 → zielone 6/6, eslint/prettier czyste
- Rundy korekt: 0
- Czas do akceptacji: ok. 2 min wykonawcy + walidacja architekta (build z celowo nieaktualnym `dist/…/pl.json` = `{}`: tytuł poprawny, 0 surowych kluczy)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): odrzucone — P3 „martwy mock `isDevMode`” (parametryzacja celowo pilnuje, że zachowanie nie zależy od trybu, wymóg briefu); uwaga spoza zakresu: zależność od `process.cwd()` przy uruchomieniu serwera z innego katalogu — znana, opisana w README, do rozstrzygnięcia przy definiowaniu środowiska
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: Vitest kolejności odczytu (pierwsze wywołanie = źródło, fallback do `dist`, pusty słownik), oba tryby `isDevMode`; dowód buildem z nieaktualnym artefaktem. Wniosek: dowód poprawki prerenderu wymaga celowo zepsutego stanu wejściowego, nie kolejnego „czystego” buildu

### BE-40 (BeautyEffect: Etap 1 Z7 — `/design/komponenty`: przyciski R-2, przyciski-ikony, odnośniki) — 2026-10-07
- Archetyp: strona podglądu FE bez Figmy — pięć sekcji z prawdziwymi komponentami (`[pButton]` na `button` i `a`, warianty, mały, ikona), odnośniki `.bty-link`, AXE; 4 pliki
- Stawka: niska (strona pomocnicza; służy jako bramka wizualna przycisków)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (81 s zatrzymanie + 258 s)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie, tylko odczyt (zbiorczo z Z5b i Z8)
- Dopuszczone alternatywy: Gemini `high` (w tej fali pisał Z6a); Claude `wykonawca` (pula ŻÓŁTA); Spark (zablokowany, 402)
- Powód wyboru: 4 pliki w porcji Codexa; recenzja krzyżowa z Gemini
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Gemini nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 85 %), 2026-10-07 07:05
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: trafne zatrzymanie — brief zapowiadał „cztery sekcje”, a wymieniał pięć (błąd briefu); `iconOnly` architekt dopisał do briefu przed wysłaniem po znalezisku recenzji Z5a
- Rundy korekt: 0 (ponowne wysłanie po poprawce briefu)
- Czas do akceptacji: ok. 6 min wykonawcy + recenzja zbiorcza 11 min + walidacja
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): brak defektów; odrzucone — P3 podwójna asercja AXE (nieszkodliwa)
- Defekty po odbiorze: strona ujawniła defekt Z4 (podkreślona etykieta `<a pButton>`) — przypisany do BE-37
- Wymagane testy i dowody: Vitest struktury (klasy `p-button-outlined`/`-sm`/`-icon-only`, `href`, `aria-label`, `aria-hidden`), AXE; `browser-check` 2×2 (zrzuty obejrzane). Wniosek: strona galerii komponentów jest skutecznym oracle dla haka presetu — defekt kaskady wyszedł dopiero na niej

### BE-41 (BeautyEffect: Etap 1 Z5b — `/design/typografia`: 20 ról pisma i polskie znaki) — 2026-10-07
- Archetyp: strona podglądu FE bez Figmy — tablica danych ról (`as const`), szablon z `@switch` dla próbek złożonych, 20 klas próbek z mixinami pisma, sekcja polskich znaków w 4 wariantach, testy struktury i powiązania z `typography.scss` przez `node:fs`; 5 plików
- Stawka: niska (strona pomocnicza; oracle wizualny ról pisma)
- Niepewność: średnia (dziedziczenie kroju w zagnieżdżonych rolach — ujawnione przez wykonawcę)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (85 s zatrzymanie + 285 s); korekta K-Z5b `medium` (101 s)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie, tylko odczyt (zbiorczo z Z7 i Z8; korekta w osobnej krótkiej recenzji)
- Dopuszczone alternatywy: Gemini `high` (w tej fali pisał Z6a); Claude `wykonawca` (pula ŻÓŁTA); Spark (zablokowany, 402)
- Powód wyboru: 5 plików w porcji Codexa, dużo dokładnych wartości do przepisania; recenzja krzyżowa z Gemini
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Gemini nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 85 %), 2026-10-07 07:05–07:30
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: trafne zatrzymanie — mixiny ról Jostu nie ustawiały kroju, więc etykieta w próbce nagłówka i `<h2>` nazwy roli dostałyby Cormoranta (defekt Z3, poprawiony K-Z3, BE-36); drugi przebieg kompletny i zielony (9/9, AXE)
- Rundy korekt: 1 — K-Z5b (interlinia 1,6 w opisie `eyebrow` — błąd tabeli w briefie architekta; test użycia mixinów w stylach komponentu)
- Czas do akceptacji: ok. 8 min wykonawcy + 1,7 min korekty + recenzje + walidacja
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): potwierdzone — P2 brak interlinii 1,6 w opisie `eyebrow`, P3 test mixinów sprawdzał tylko `theme/typography.scss`, nie użycie w próbkach; odrzucone — P3 „tautologiczna” asercja wartości (test szablonu, nie danych), P3 podwójna asercja AXE
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu; style komponentu (5,6 kB) przekroczyły budżet ostrzeżenia 4 kB — architekt podniósł próg ostrzeżenia `anyComponentStyle` do 6 kB (błąd nadal 8 kB)
- Wymagane testy i dowody: Vitest 20 ról w kolejności, próbki złożone, mixin istnieje i jest użyty w dokładnym selektorze próbki, AXE; `browser-check` (role Jostu w Joście po K-Z3). Wniosek: tabele wartości przepisywane „znak w znak” architekt sprawdza z dokumentem przed wysłaniem — wykonawca wiernie powieli błąd briefu

### BE-42 (BeautyEffect: Etap 1 Z6a — czyste funkcje koloru do pomiaru kontrastu WCAG) — 2026-10-07
- Archetyp: czyste funkcje TS (parsowanie `rgb()`/`color(srgb …)`, krycie, spłaszczanie alfa, powierzchnia złożona, luminancja, kontrast, obcięcie, HEX), część przeniesiona `Copy-Item` z innego projektu, testy z literałami z dokumentu; 13 plików, jedna deklaracja na plik
- Stawka: średnia (fałszywy PASS na bramce kontrastu WCAG AA przepuszcza defekt dostępności strony publicznej)
- Niepewność: średnia (precyzja zmiennoprzecinkowa obcięcia, wartości dokumentu liczone na powierzchniach złożonych)
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie (802 s); korekta K-Z6a ta sama linia (680 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (214 s; razem z K-Z3); ponowna weryfikacja korekty w recenzji Z6b
- Dopuszczone alternatywy: Codex `high` (porcja > 5 plików — odpada bez podziału); Claude `wykonawca` (pula ŻÓŁTA); Spark (zablokowany, 402)
- Powód wyboru: wiele małych plików jednej warstwy — Gemini bez limitu 5 plików; recenzja krzyżowa z Codexem
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany, Codex nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 85 %), 2026-10-07 07:05–07:45
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zielony (34 testy) z trzema trafnymi uwagami do briefu: przypadek `14.469999999` w briefie nie był błędem reprezentacji (wykonawca podniósł epsilon do `1e-5`, żeby go spełnić), wartości 10.69/5.83 dotyczą powierzchni złożonych bez zaokrąglenia, pusta lista warstw przy półprzezroczystym podłożu i tak spłaszcza na biel
- Rundy korekt: 1 — K-Z6a (epsilon `1e-9` + przypadki błędu reprezentacji `4.35`/`1.15`/`0.29` i regresja `4.49999995` → `4.49`; `parseAlpha` z procentami i `none`; zakotwiczone wyrażenia odrzucające uszkodzone zapisy)
- Czas do akceptacji: ok. 13 min wykonawcy + 11 min korekty + 3,5 min recenzji + walidacja
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): potwierdzone — P2 epsilon `1e-5` zamienia osiągalny kontrast `4.49999995` na `4.5` (fałszywe AA), P2 krycie w procentach (`85%` → `a: 85`) i `none` (→ `a: 1` zamiast 0), P3 brak zakotwiczenia (`rgb(42, 37, 35oops)` przyjęty); błąd źródłowy — przypadek testowy w briefie architekta
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: Vitest 54 przypadki z literałami dokumentu; pomiar w przeglądarce na `/design/kolory` (jasny: wszystkie pary zgodne z dokumentem). Wnioski: (1) przypadek testowy precyzji architekt sprawdza w `node -e` przed wysłaniem — błędny przypadek skłonił wykonawcę do obejścia, które recenzja słusznie odrzuciła; (2) reguła lint `sonarjs/super-linear-regex` wymusiła deterministyczny wzorzec liczby — brief z wyrażeniem regularnym przechodzi przez lint przed wysłaniem

### BE-43 (BeautyEffect: Etap 1 Z6b — strona `/design/kolory` z pomiarem kontrastu w przeglądarce) — 2026-10-07
- Archetyp: strona podglądu (komponent OnPush, SSR-bezpieczny pomiar w `afterNextRender` + `MutationObserver` na klasie motywu), dane 74 par kontrastu i 27 ról przepisane z dokumentu kolorów, etykiety `pl.json`, tabela ↔ karty z jednego strumienia, testy Vitest + AXE; technika próbnika wzięta ze wzoru w innym projekcie
- Stawka: średnia (strona jest bramką kontrastu WCAG AA projektu — fałszywy PASS przepuszcza defekt dostępności strony publicznej)
- Niepewność: średnia (zachowanie `var()` brakującego tokenu w przeglądarce, zgodność 74 par z tabelą dokumentu)
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie (ok. 1084 s); korekta K-Z6b ta sama linia (454 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (226 s; razem z weryfikacją K-Z6a); ponowna recenzja K-Z6b ta sama para (70 s)
- Dopuszczone alternatywy: Codex `high` (porcja > 5 plików — odpada bez podziału); Claude `wykonawca` (pula ŻÓŁTA); Spark (zablokowany, 402)
- Powód wyboru: wiele plików jednej warstwy bez Figmy — Gemini bez limitu 5 plików; recenzja krzyżowa z Codexem
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany, Codex nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 85–86 %), 2026-10-07 07:15–08:00
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zielony (testy, lint, prettier), pomiar w przeglądarce zgodny z dokumentem w jasnym motywie; wrapper zakończył przebieg kodem 3 („stream interrupted”) mimo kompletnego raportu i plików — odbiór po artefaktach, nie po kodzie wyjścia
- Rundy korekt: 1 — K-Z6b (opakowanie próbnika z dwiema wartościami sterującymi koloru dziedziczonego, `createTokenResolver` w osobnym pliku, `finally` usuwa opakowanie; niezależna mapa `id → próg` dla 74 par i pełne definicje 12 par plam w teście)
- Czas do akceptacji: ok. 18 min wykonawcy + 7,5 min korekty + 5 min recenzji + walidacja (pełny lint/format/test/build, browser-check 4 zrzuty)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): potwierdzone — P1 brakujący token w `color: var(--x)` jest nieprawidłowy w chwili obliczania i dziedziczy kolor rodzica (architekt potwierdził w Chrome), więc próbnik mierzyłby brakującą rolę jako kolor tekstu strony; P2 test danych par nie wiązał progu z parą ani definicji par plam (przyjęte częściowo: mapa progów + definicje plam); ponowna recenzja K-Z6b — bez znalezisk, werdykt poprawny
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu; ten sam błąd próbnika jest we wzorze w ZebraniFE (`/design/kolory`) — zgłoszony właścicielowi
- Wymagane testy i dowody: Vitest (katalog kolorów 78 przypadków, cały projekt 295), AXE strony, browser-check `/design/kolory` 2 szerokości × 2 motywy (jasny: wszystkie pary zgodne; ciemny: rozbieżność dokumentu 8 %/12 % tinty najechania i jedna para plamy poniżej AA — pytania do właściciela). Wnioski: (1) technika przeniesiona z innego projektu wymaga w briefie sprawdzenia jej założenia w prawdziwej przeglądarce, nie tylko w jsdom — błąd wzoru przeszedł do kopii; (2) kod wyjścia 3 wrappera Gemini nie oznacza braku wyniku — raport i diff są dowodem

### BE-44 (BeautyEffect: K-Z6c — plamy otwarcia z kryciem po rozmyciu, DARK_15 = 6.10, naciśnięcie tylko z kursorem) — 2026-10-07
- Archetyp: korekta danych par kontrastu (12 par plam: krycie warstwy po rozmyciu Gaussa, jedna wartość oczekiwana) i jednej reguły CSS w haku presetu przycisków + testy z niezależnym wzorcem; 4 pliki, dwa obszary jednej warstwy FE
- Stawka: średnia (bramka kontrastu WCAG AA; fałszywy FAIL trafił już do właściciela jako pytanie o paletę)
- Niepewność: niska (wartości policzone przez architekta, Codex przeliczył je niezależnie)
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie (596 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (120 s)
- Dopuszczone alternatywy: Codex `medium` (≤ 5 plików — mieści się); Claude `wykonawca` (pula ŻÓŁTA, tydzień 86 %); Spark (zablokowany, 402)
- Powód wyboru: Gemini jest autorem strony kolorów (Z6b) — poprawka wraca do autora; recenzja krzyżowa z Codexem
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany, Codex nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 86 %), 2026-10-07 08:20–08:40
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zielony (92 testy w zakresie, czerwone → zielone 2/92), z jedną trafną uwagą do briefu: etykieta DARK_15 w `pl.json` nadal mówiła „8 %” (poza zakresem briefu — architekt poprawił jedną linię)
- Rundy korekt: 0
- Czas do akceptacji: ok. 10 min wykonawcy + 2 min recenzji + walidacja (przerwana zamknięciem sesji Claude Code i powtórzona)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): brak; recenzent przeliczył całkę (0,610954 / 0,561588), krycie mnożone (0,3135) i DARK_15 (6,100263)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: Vitest 295, lint, format, build, browser-check `/design/kolory` 2 × 2 (ciemny: wszystkie pary spełniają, DARK_15 bez DIFF, akcent na pierwszej plamie 5.26:1). Wniosek: źródłem korekty był brief Z6b architekta — para „tekst na plamie” liczona bez rozmycia i rozmiaru gradientu dała fałszywy FAIL (3.81:1), który poszedł do właściciela jako pytanie o paletę; przed eskalacją FAIL-a architekt modeluje pełne renderowanie z makiety (rozmycie, krycie, rozmiar gradientu)

### BE-45 (BeautyEffect: D-1 — zapis sześciu decyzji właściciela z 2026-10-07 w dokumentacji) — 2026-10-07
- Archetyp: dokumentacja produktu — statusy (AT zatwierdzony, dwie KO rozstrzygnięte), rozstrzygnięcia z dosłownymi cytatami, wyjątki w DEC i WP, uzgodnienie odwołań w dokumentach UI i KO, dwie poprawki wartości technicznych; 14 plików
- Stawka: średnia (źródło prawdy dla etapów 2–5; błędny cytat albo pozostawiona „otwarta” kwestia wprowadza w błąd kolejne briefy)
- Niepewność: niska (decyzje i cytaty podane w briefie; struktura wg wzoru rozstrzygniętej kwestii)
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie (903 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (77 s STOP na kryterium briefu + 171 s pełna recenzja)
- Dopuszczone alternatywy: Codex (porcja > 5 plików — odpada bez podziału); Claude `wykonawca` (pula ŻÓŁTA, tydzień 86 %); Spark (zablokowany, 402)
- Powód wyboru: brief tekstowy wielu plików — Gemini bez limitu 5 plików; równolegle z K-Z6c w innym repozytorium (rozłączne cele); recenzja krzyżowa z Codexem
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany, Codex nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 86 %), 2026-10-07 08:25–10:15
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: wszystkie punkty A–J wdrożone; dwa defekty wykonania poprawione przez architekta: (1) cały plik `tresci-bezobslugowe.md` zapisany z CRLF wbrew `eol=lf` repozytorium, (2) zdanie „kontrast pochodzi z pomiaru strony” sprzeczne z zasadą dokumentu „tabela to obliczenie, nie pomiar” (zgłoszone przez samego wykonawcę w sekcji uwag); pozostałe uwagi wykonawcy (fragment `#business-reviews`, wyjątki od bezobsługowości, odnośnik do Booksy, krawędź pola bez formularza) dotyczyły decyzji właściciela — odrzucone
- Rundy korekt: 0 (poprawki architekta: przywrócenie LF, jedno zdanie)
- Czas do akceptacji: ok. 15 min wykonawcy + 4 min recenzji (dwa przebiegi) + walidacja; sesja Claude Code zamknęła się w trakcie — stan odebrany z rekordów wrappera i `git status`
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): pierwszy przebieg — STOP na błędnym założeniu briefu architekta (kryterium „żaden dokument” kolidowało z zakazem zmian w researchu `zrodla\`), potwierdzone; po zawężeniu kryterium — brak znalezisk, 472 linki względne poprawne
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: recenzja diffu, wyrywkowy odczyt architekta (statusy, cytaty, wartości 12 % / `#56494B` / 6.10:1, adres Booksy), kontrola końców linii wszystkich 14 plików. Wnioski: (1) brief dokumentacji dla Gemini wymaga jawnego „końce linii LF zgodnie z `.gitattributes`” zamiast „zachowaj dotychczasowe” — wykonawca i tak zmienił plik na CRLF; (2) kryterium spójności w briefie recenzji od razu wyłącza zapisy historyczne (`zrodla\`, research)

### BE-46 (BeautyEffect: Etap 2 Z1 — dane salonu, logo, pozycje menu, teksty powłoki) — 2026-10-07
- Archetyp: pliki stałych (dane salonu znak w znak z WP, zasoby marki, pozycje menu) + 28 kluczy `pl.json` + test z niezależną wyrocznią literałów; 7 plików, jedna warstwa FE, bez logiki
- Stawka: średnia (adres, telefon i odnośniki trafiają na każdą stronę; literówka w numerze lub adresie Booksy uderza w rezerwacje)
- Niepewność: niska (wszystkie wartości i klucze podane w planie tabelą)
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie (533 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (320 s, wspólnie z Z3)
- Dopuszczone alternatywy: Codex `medium` (7 plików — wymagałby podziału na porcje ≤ 5); Claude `wykonawca` (pula ŻÓŁTA, tydzień 87 %); Spark (zablokowany, 402)
- Powód wyboru: brief tekstowy wielu plików bez podziału; Gemini równolegle z trzema briefami Codexa (rozłączne pliki); recenzja krzyżowa z Codexem
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany, Codex nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 87 %), 2026-10-07 12:50–13:25
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zielony (6 testów czerwone → zielone), wartości zgodne z planem; trafna uwaga wykonawcy: zapis briefu „reszta jako `string`” koliduje z `no-inferrable-types` — typy wywnioskowane z literałów
- Rundy korekt: 0
- Czas do akceptacji: ok. 9 min wykonawcy + recenzja + walidacja fali
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): brak (werdykt poprawny, pewność 0,99)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: Vitest (fala 351 → 355 po korekcie Z3), lint, format, build; odczyt architekta wszystkich stałych i kluczy względem tabeli planu

### BE-47 (BeautyEffect: Etap 2 Z2 — rozmiar przycisków paska, tło przycisku obrysowego, przyciemnienie pod szufladą) — 2026-10-07
- Archetyp: zmiana tokenów presetu PrimeNG (zmienna tła przycisku obrysowego w stanach i haku CSS presetu, maska greige-950 50 %) + testy na rozwiązanych tokenach (`Theme.tokens…computed`); 4 pliki
- Stawka: średnia (preset dotyka każdego przycisku obrysowego w aplikacji; kontrast na szkle paska — AT-SYSTEM-KOLOROW-UI)
- Niepewność: niska (wartości w planie; ścieżki tokenów Aury znane z etapu 1)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (264 s)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie, `-Access read` (690 s, wspólnie z Z4 i Z5)
- Dopuszczone alternatywy: Gemini (autor tokenów strony kolorów — ale Codex wolny i w limicie ≤ 5 plików); Claude `wykonawca` (pula ŻÓŁTA); Spark (zablokowany, 402)
- Powód wyboru: ≤ 5 plików, pułapki ścieżek tokenów Aury (cicho ignorowany token) — Sol `high` ze sprawdzeniem na rozwiązanych tokenach; recenzja krzyżowa z Gemini
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Gemini nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 87 %), 2026-10-07 12:50–13:25
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zielony (6 czerwonych + 29 zielonych → 35); rozmiary `small` już były zgodne, potwierdzone emisją z `root.sm`
- Rundy korekt: 0
- Czas do akceptacji: ok. 4 min wykonawcy + recenzja + walidacja fali
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1 × P2 odrzucone — stan `:active` czyta zmienną najechania (reguła istniała w `HEAD` przed falą, wartości obu tokenów identyczne); recenzent potwierdził brak kolizji specyficzności (0,2,0) z regułami stanów (0,3,0)/(0,4,0)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: Vitest, lint, format, build; w prerenderowanym HTML jedna definicja `--p-mask-background` = `color-mix(… var(--p-bty-shade) 50%, transparent)`, `--p-bty-shade` = greige-950 — maska Aury z `colorScheme` jej nie nadpisuje

### BE-48 (BeautyEffect: Etap 2 Z3 + K-Z3 — odsłonięcia W-3: dyrektywa, serwis obserwatora, style, bezpiecznik) — 2026-10-07
- Archetyp: dyrektywa + `@Service()` z dwoma `IntersectionObserver` i kaskadą, globalne style odsłonięć z bezpiecznikiem bez JS, sterowalna atrapa obserwatora do testów; 7 plików, jedna warstwa FE, SSR-wrażliwe
- Stawka: średnia–wysoka (błąd = treść całej strony niewidoczna dla części odwiedzających; dotyka każdej strony etapów 3–5)
- Niepewność: średnia (zachowanie animacji `forwards` przy zmianie selektora, prerender, hydracja)
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie (797 s + korekta K-Z3 ok. 10 min)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (320 s, wspólnie z Z1)
- Dopuszczone alternatywy: Codex `high` (7 plików — wymagałby podziału, a dyrektywa i serwis muszą powstać razem); Claude `wykonawca` (pula ŻÓŁTA); Spark (zablokowany, 402)
- Powód wyboru: spójna jednostka > 5 plików; recenzja krzyżowa z Sol `high` z naciskiem na scenariusze „treść niewidoczna”
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany, Codex nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 87 %), 2026-10-07 12:50–13:40
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zielony (18 testów), ale z defektem przeniesionym z recepty planu architekta: bezpiecznik w selektorze `html:not(.bty-reveal-ready)` — przy starcie aplikacji po 4 s dodanie klasy zdejmowało animację razem ze stanem `forwards` i treść znikała ponownie; testy dyrektywy sprawdzały metadane zamiast wyrenderowanego hosta
- Rundy korekt: 1 (K-Z3: bezpiecznik na stałe + `animation-play-state: paused` pod `html.bty-reveal-ready`; testy dyrektywy przez TestBed z hostem testowym, w tym SSR)
- Czas do akceptacji: ok. 13 min + 5 min recenzji + 10 min korekty + dwie walidacje fali
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 3 × P2 — potwierdzone 2 (bezpiecznik po późnym starcie — błąd planu architekta; testy metadanych), odrzucone 1 (filtr `intersectionRatio >= 0.1` — makieta filtruje samym `isIntersecting`, a filtr ukryłby na stałe element wyższy niż 10 ekranów)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: Vitest 355, lint, format, build; odczyt architekta selektorów bezpiecznika. Wnioski: (1) recepta „bezpiecznik do czasu klasy gotowości” musi rozważyć start po upływie bezpiecznika — klasa wstrzymuje animację, nie usuwa jej; (2) wejście typowane enumem nie przyjmuje gołego tekstu w szablonie (`btyReveal="words"` → TS2322) — briefy wiążą `[btyReveal]="RevealKind.Words"`; (3) nowe ograniczenie dla stron: `[btyReveal]` nigdy w `@defer (hydrate never)`

### BE-49 (BeautyEffect: Etap 2 Z4 — łuk zdjęcia z obrysem i rozdzielenia sekcji S-3) — 2026-10-07
- Archetyp: komponent prezentacyjny z `NgOptimizedImage` (`fill`) + partial SCSS z trzema mixinami + spec z AXE; 5 plików, jedna warstwa FE
- Stawka: niska–średnia (wspólny element wielu stron; obrys i kadrowanie widoczne od razu)
- Niepewność: niska (wartości i wzór w makiecie i planie)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (273 s)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie, `-Access read` (690 s, wspólnie z Z2 i Z5)
- Dopuszczone alternatywy: Codex `medium`; Gemini (zajęty Z1 i Z3); Claude `wykonawca` (pula ŻÓŁTA); Spark (zablokowany, 402)
- Powód wyboru: 5 plików mieści się w porcji Codexa; równolegle z Gemini; recenzja krzyżowa z Gemini
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Gemini nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 87 %), 2026-10-07 12:50–13:25
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zielony (14 czerwonych + 2 zielone → 16, dwa audyty AXE); `disableOptimizedSrcset` dla zdjęć statycznych bez loadera
- Rundy korekt: 0 (architekt dodał jedną linię `max-height: var(--bty-arch-max-height, none)` — stopka w makiecie ogranicza łuk do 340 px, czego plan nie przewidział)
- Czas do akceptacji: ok. 5 min wykonawcy + recenzja + walidacja fali
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1 × P2 odrzucone jako defekt komponentu — obrys wystaje 12 px w dół (tak samo w makiecie `.archwrap::after`; miejsce rezerwuje rodzic — wymaganie dopisane do briefu stopki Z8)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: Vitest, lint, format, build; odczyt architekta względem planu i makiety

### BE-50 (BeautyEffect: Etap 2 Z5 — przełącznik motywu: przycisk-ikona paska i wariant z napisem do szuflady) — 2026-10-07
- Archetyp: mały komponent prezentacyjny z dwoma wariantami, ikony przełączane wyłącznie CSS-em `:host-context(.app-dark)` (bez mignięcia przed hydracją) + spec z AXE; 4 pliki
- Stawka: niska (dostępność przełącznika, brak mignięcia przy zapisanym motywie ciemnym)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `medium` (161 s)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie, `-Access read` (690 s, wspólnie z Z2 i Z4)
- Dopuszczone alternatywy: Codex `low`/Luna (ryzyko pominięcia szczegółu SSR); Claude `mechanik` (za dużo decyzji); Spark (zablokowany, 402)
- Powód wyboru: prosty komponent ≤ 5 plików — `medium` wystarcza; recenzja krzyżowa z Gemini
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Gemini nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 87 %), 2026-10-07 12:50–13:25
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zielony (9 czerwonych → 9 zielonych, AXE obu wariantów)
- Rundy korekt: 0
- Czas do akceptacji: ok. 3 min wykonawcy + recenzja + walidacja fali
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 2 × P3 bez działania (kontrast lokalnej ramki fokusu 1,8:1 — wskaźnikiem jest globalny pierścień `--bty-focus`, nienaruszony; nadmiarowe 44 × 44 px przy `p-button-icon-only`)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: Vitest, lint, format, build; odczyt architekta (obie ikony w HTML, brak `aria-pressed`, globalny pierścień fokusu)

### BE-51 (BeautyEffect: Etap 2 Z6 + K-Z6Z7 — pasek P-2: szkło po przewinięciu, logo obu motywów, przyciski i menu) — 2026-10-07
- Archetyp: komponent powłoki z sygnałem przewinięcia (SSR-safe), wariantami logo przełączanymi CSS-em, progami widoczności i spec z AXE; 4 pliki, jedna warstwa FE
- Stawka: średnia (pasek na każdej stronie; dostępność nawigacji, mignięcie logo przed hydracją)
- Niepewność: niska–średnia (makieta P-2 i plan; stan przewinięcia po odświeżeniu w połowie strony)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (425 s; korekta K-Z6Z7 wspólna z Z7 — 380 s)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie, `-Access read` (961 s, wspólnie z Z7 i Z9)
- Dopuszczone alternatywy: Claude `wykonawca` (pula ŻÓŁTA, tydzień 88 %); Gemini (zajęty Z8 i Z10); Spark (zablokowany, 402)
- Powód wyboru: 4 pliki w porcji Codexa; równolegle z Gemini; recenzja krzyżowa z Gemini
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Gemini nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 88 %), 2026-10-07 13:36–14:30
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zielony (testy, lint, format); recenzja: werdykt poprawny 0,98
- Rundy korekt: 1 (K-Z6Z7, wspólna z Z7 — bieżąca sekcja na podstronach `/oferta/*`)
- Czas do akceptacji: ok. 7 min wykonawcy + recenzja + korekta + walidacja fali
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1 × P2 potwierdzone (`exact: true` gasi „Oferta” na podstronach — plan nie przewidział podstron)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: Vitest, lint, format, build; odczyt architekta względem planu i makiety

### BE-52 (BeautyEffect: Etap 2 Z7 + K-Z7 + K-Z6Z7 — szuflada M-1: PrimeNG Drawer, historia przeglądarki, fokus, blokada przewijania) — 2026-10-07
- Archetyp: nakładka modalna na PrimeNG z wpisem historii (gest „wstecz”), powrotem fokusu, zamykaniem przy poszerzeniu ekranu i klasami ruchu `motionOptions` + spec; 5 plików + partial SCSS ruchu
- Stawka: średnia (dostępność nakładki, historia przeglądarki — ryzyko cofnięcia za daleko i opuszczenia strony)
- Niepewność: średnia (zachowanie routera przy `history.back()` i PrimeNG Drawer)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (580 s; K-Z7 72 s zatrzymany STOP + 130 s; K-Z6Z7 380 s)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie, `-Access read` (961 s, wspólnie z Z6 i Z9)
- Dopuszczone alternatywy: Claude `wykonawca-opus` (brak niezmiennika wysokiej stawki — nieuzasadniony); Claude `wykonawca` (pula ŻÓŁTA); Spark (zablokowany, 402)
- Powód wyboru: logika historii i fokusu wymaga `high`; 5 plików w porcji Codexa; recenzja krzyżowa z Gemini
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Gemini nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 88 %), 2026-10-07 13:36–14:30
- Pewność decyzji: średnia–wysoka
- Wynik pierwszego podejścia: zielony; architekt dopisał do planu wybór pozycji bieżącej strony (K-Z7)
- Rundy korekt: 2 (K-Z7 — pozycja bieżącej strony zamyka szufladę; brief architekta zakładał błędnie, że `history.length` maleje po `back()` — wykonawca zatrzymał się klauzulą STOP i miał rację; K-Z6Z7 — dokładne dopasowanie URL przy decyzji „zamknij czy nawiguj”, utwardzenie fokusu)
- Czas do akceptacji: ok. 13 min wykonawcy + recenzja + dwie korekty + walidacja fali
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): P1 „wyścig `popstate` zeruje wyzwalacz fokusu” obniżone do P2 i przyjęte jako utwardzenie (router dla tego samego URL emituje `NavigationSkipped`, nie `NavigationStart` — kod ma jednak nie zależeć od tego szczegółu); P2 `exact: true` potwierdzone (wspólne z Z6); werdykt recenzenta: niepoprawny 0,95
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: Vitest, lint, format, build; odczyt architekta; zachowanie historii w przeglądarce po złożeniu powłoki (Z11)

### BE-53 (BeautyEffect: Etap 2 Z8 + K-Z8 — stopka F-3: grupy kontaktu, łuk zdjęcia, podpis DTCode) — 2026-10-07
- Archetyp: komponent powłoki z danymi salonu, zagnieżdżoną siatką Bootstrapa, zdjęciem w łuku i wariantami logo + spec z AXE; 4 pliki
- Stawka: niska–średnia (dane kontaktowe i odnośniki zewnętrzne, Label in Name)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie, `-Access write` (1464 s; K-Z8 411 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (494 s, wspólnie z Z10)
- Dopuszczone alternatywy: Codex (zajęty Z6, Z7, Z9); Claude `wykonawca` (pula ŻÓŁTA); Spark (zablokowany, 402)
- Powód wyboru: równoległość z Codexem; zadanie bez niezmiennika; recenzja krzyżowa z Codexem
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Gemini nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 88 %), 2026-10-07 13:36–14:20
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zielony w testach, ale z dwiema wadami wzorca: własna siatka CSS zamiast Bootstrapa oraz atrapa `canvas` w spec dająca werdykt AXE z fałszywych pikseli
- Rundy korekt: 1 (K-Z8 — siatka Bootstrapa, odstępy telefonu, test Label in Name zamiast atrapy, grupy bez zbędnych regionów, `protected readonly`)
- Czas do akceptacji: ok. 31 min wykonawcy + recenzja + korekta + walidacja fali
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): P2 własna siatka CSS — potwierdzone; P3 odstępy telefonu — potwierdzone; architekt dołożył: atrapa `canvas` (nowa reguła martwego pola `label-content-name-mismatch` w pomocniku AXE i w `AGENTS.md`), regiony `section aria-label` w `contentinfo`, modyfikatory dostępu; raport K-Z8 wspomniał adres spoza danych salonu — sprawdzone `grep`, w kodzie go nie ma
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: Vitest, lint, format, stylelint, build; odczyt architekta (dane salonu niezmienione, brak atrapy `canvas`)

### BE-54 (BeautyEffect: Etap 2 Z9 — nagłówek sekcji N-1: maski słów, akcent, etykieta z kreską) — 2026-10-07
- Archetyp: komponent prezentacyjny z podziałem tytułu na słowa (odsłonięcie słowo po słowie), akcentem i jednorazowym odczytem przez czytnik + enum rozmiaru + spec z AXE; 5 plików
- Stawka: niska–średnia (tytuł czytany raz, spacje w DOM)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (246 s)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie, `-Access read` (961 s, wspólnie z Z6 i Z7)
- Dopuszczone alternatywy: Codex `medium`; Gemini (zajęty Z8 i Z10); Claude `wykonawca` (pula ŻÓŁTA); Spark (zablokowany, 402)
- Powód wyboru: logika podziału i dostępności — `high`; recenzja krzyżowa z Gemini
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Gemini nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 88 %), 2026-10-07 13:36–14:20
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zielony; recenzja: werdykt poprawny 0,97
- Rundy korekt: 0
- Czas do akceptacji: ok. 4 min wykonawcy + recenzja + walidacja fali
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1 × P3 odrzucone (kreska etykiety w wariancie wyśrodkowanym rośnie od środka — tak jak w makiecie części 10b)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: Vitest, lint, format, build

### BE-55 (BeautyEffect: Etap 2 Z10 + K-Z10 — film z limitem 5 s: start w widoku, plakat przy ograniczeniu ruchu) — 2026-10-07
- Archetyp: komponent multimedialny z obserwatorem widoczności, `requestVideoFrameCallback` z rezerwą `timeupdate`, `play()` owiniętym w RxJS i reakcją na `prefers-reduced-motion` + spec; 4 pliki
- Stawka: niska–średnia (dokładny limit 5 s, brak wiszących wywołań zwrotnych, reduced motion)
- Niepewność: średnia (wyścigi zdarzeń mediów, brak rVFC w jsdom)
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie, `-Access write` (969 s; K-Z10 543 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (494 s, wspólnie z Z8)
- Dopuszczone alternatywy: Codex (zajęty Z6, Z7, Z9); Claude `wykonawca` (pula ŻÓŁTA); Spark (zablokowany, 402)
- Powód wyboru: równoległość z Codexem; recenzja krzyżowa z Codexem
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Gemini nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 88 %), 2026-10-07 13:36–14:25
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zielony (17 testów), dwie luki brzegowe
- Rundy korekt: 1 (K-Z10 — `load()` przywraca plakat po włączeniu ograniczenia ruchu tylko po starcie; wspólna kontrola limitu także w `ended` na ścieżce rVFC; 17 → 20 testów, czerwone → zielone)
- Czas do akceptacji: ok. 25 min wykonawcy + recenzja + korekta + walidacja fali
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 2 × P2 potwierdzone (bieżąca klatka zamiast plakatu przy reduce; limit pomijany przy `ended` między klatkami rVFC)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: Vitest, lint, format, build; odczyt architekta (jedna metoda limitu, `load()` tylko po starcie)

### BE-56 (BeautyEffect: Etap 2 Z11 — złożenie powłoki publicznej: pasek, szuflada, stopka, odnośnik pomijający) — 2026-10-07
- Archetyp: złożenie komponentów powłoki w layoucie (sygnał stanu szuflady, landmarki, `scroll-margin-top`, styl odnośnika pomijającego) + rozszerzony spec z AXE w obu stanach szuflady; 6 plików (w tym jednolinijkowa podmiana atrybutu na dyrektywę w `ArchPhoto`)
- Stawka: średnia (struktura każdej strony: landmarki, przyklejenie paska, pierwszy fokus)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie, `-Access write` (639 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (161 s)
- Dopuszczone alternatywy: Codex (zajęty Z12b); Claude `wykonawca` (pula ŻÓŁTA, tydzień 88–89 %); Spark (zablokowany, 402)
- Powód wyboru: równoległość z Codexem; brak niezmiennika; recenzja krzyżowa z Codexem
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Gemini nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 89 %), 2026-10-07 14:29–15:15
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zielony; recenzja bez znalezisk (werdykt poprawny)
- Rundy korekt: 0
- Czas do akceptacji: ok. 11 min wykonawcy + recenzja + walidacja fali
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): brak
- Defekty po odbiorze: brak w plikach Z11; sprawdzenie przeglądarkowe złożonej powłoki (Gemini, Playwright MCP) wykryło utratę pozycji przewinięcia po zamknięciu szuflady — defekt szuflady (BE-61), nie złożenia
- Wymagane testy i dowody: Vitest (AXE w obu stanach szuflady), lint, format, build; `browser-check` (zrzuty 2×2: przyklejony pasek, odnośnik pomijający, szuflada, motywy)

### BE-57 (BeautyEffect: Etap 2 Z12a + K-Z12a — otwarcie podstrony OF-3: tekst i kompozycja trzech łuków) — 2026-10-07
- Archetyp: komponent prezentacyjny z siatką Bootstrapa, kompozycją trzech zdjęć w łukach (wymiary z makiety dla dwóch progów), odsłonięciami W-3 i `NgOptimizedImage` + model + spec z AXE; 5 plików
- Stawka: niska–średnia (element LCP podstron, przepełnienie na wąskim ekranie)
- Niepewność: średnia (geometria kompozycji z makiety, kurtyna na kompozycji)
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie, `-Access write` (660 s; K-Z12a 672 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (322 s)
- Dopuszczone alternatywy: Codex (zajęty Z12b-1); Claude `wykonawca` (pula ŻÓŁTA); Spark (zablokowany, 402)
- Powód wyboru: równoległość z Codexem; recenzja krzyżowa z Codexem
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Gemini nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 88–89 %), 2026-10-07 14:03–14:45
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zielony w testach; kurtyna obcinała kompozycję, testy wymiarów nie wiązały wartości z selektorami i progami
- Rundy korekt: 1 (K-Z12a — kurtyna obejmuje pełną szerokość trzech łuków, testy wymiarów per selektor i próg, jedna kreska etykiety, `priority` dla zdjęcia środkowego); architekt dopisał sam `overflow-x: clip` na sekcji (jedna linia)
- Czas do akceptacji: ok. 22 min wykonawcy + recenzja + korekta + walidacja fali
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): P2 kurtyna obcina kompozycję — potwierdzone; P3 asercje wymiarów bez selektorów — potwierdzone; architekt: plan błędnie zakładał drugą kreskę etykiety (`.eline-end` tylko w otwarciach wyśrodkowanych, etap 6) — plan poprawiony
- Defekty po odbiorze: kurtyna kompozycji nie odsłaniała się w Chrome — przyczyna w serwisie odsłonięć (BE-60), nie w Z12a
- Wymagane testy i dowody: Vitest, lint, format, stylelint, build; `browser-check`

### BE-58 (BeautyEffect: Etap 2 Z12b-1 — przyciski rezerwacji „Umów wizytę” / „Zadzwoń”) — 2026-10-07
- Archetyp: mały komponent prezentacyjny z odnośnikami zewnętrznymi (Booksy, `tel:`), dostępną nazwą i układem kolumna/wiersz + spec z AXE; 4 pliki
- Stawka: niska (dane salonu z jednego źródła, Label in Name)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `medium` (172 s)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie, `-Access read` (743 s, wspólnie z Z12b-2)
- Dopuszczone alternatywy: Codex `low`; Gemini (zajęty Z12a); Claude `wykonawca` (pula ŻÓŁTA); Spark (zablokowany, 402)
- Powód wyboru: prosty komponent — `medium` wystarcza; recenzja krzyżowa z Gemini
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Gemini nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 88 %), 2026-10-07 14:03–14:43
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zielony
- Rundy korekt: 0
- Czas do akceptacji: ok. 3 min wykonawcy + recenzja + walidacja fali
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): P3 „brak sprzątania `fixture`” — odrzucone (TestBed niszczy fixture po każdym teście domyślnie)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: Vitest, lint, format, build

### BE-59 (BeautyEffect: Etap 2 Z12b-2 + K-Z12b2 — pas zamknięcia z łukiem i projekcją akcji) — 2026-10-07
- Archetyp: komponent prezentacyjny z projekcją treści (`ng-content`), nagłówkiem sekcji, łukiem górnym z mixinu i odsłonięciami + spec z projekcją bez komponentu-hosta (`createComponent` + `projectableNodes`); 4 pliki
- Stawka: niska–średnia (wspólny element każdej podstrony; pełna szerokość akcji na telefonie)
- Niepewność: średnia (test projekcji przy regule jednej deklaracji na plik)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (49 s STOP + 144 s STOP + 155 s; K-Z12b2 `medium` 131 s)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie, `-Access read` (743 s, wspólnie z Z12b-1)
- Dopuszczone alternatywy: Gemini (zajęty Z12a i Z11); Claude `wykonawca` (pula ŻÓŁTA); Spark (zablokowany, 402)
- Powód wyboru: wzorzec testu projekcji wymagał `high`; recenzja krzyżowa z Gemini
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Gemini nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 88 %), 2026-10-07 14:22–14:50
- Pewność decyzji: średnia–wysoka
- Wynik pierwszego podejścia: dwa zatrzymania STOP na błędnych przesłankach briefu architekta (komponent-host testu poza zakresem plików; `TestBed.createComponent` nie ma `projectableNodes`) — wykonawca miał rację oba razy; potem zielony
- Rundy korekt: 1 (K-Z12b2 — kontener projektu `.bty-container` zamiast Bootstrapowego `.container` (błąd briefu architekta), akcje na całą szerokość poniżej `sm`, pusty `headingId` bez pustych atrybutów, klasy zamiast gołych znaczników)
- Czas do akceptacji: ok. 8 min wykonawcy (z dwoma restartami) + recenzja + korekta + walidacja fali
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): P2 pojedynczy przycisk nie rozciąga się na telefonie — potwierdzone; P3 pusty `aria-labelledby` — potwierdzone; P3 goły selektor `p` — potwierdzone
- Defekty po odbiorze: łuk górny pasa płaski w przeglądarce — przyczyna w mixinie `arc-top` z etapu 1 (BE-63), testy tekstu SCSS go nie wykryły
- Wymagane testy i dowody: Vitest, lint, format, stylelint, build; `browser-check`

### BE-60 (BeautyEffect: Etap 2 K-R1 + K-R1b — odsłonięcia W-3: kurtyna obserwowana przez rodzica, zwalnianie per tryb) — 2026-10-07
- Archetyp: serwis przekrojowy z dwoma IntersectionObserverami, mapami cel ↔ wartownik ↔ obserwator, kaskadą w kolejności dokumentu i sprzątaniem obserwacji + spec z atrapą obserwatora; 3–4 pliki
- Stawka: średnia (cicha awaria: każda kurtyna ukryta na zawsze przy działającym JS; bezpiecznik wstrzymany)
- Niepewność: wysoka (Chrome liczy przecięcie z własnym `clip-path` celu; jsdom tego nie widzi)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (301 s; K-R1b `medium` 178 s)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie, `-Access read` (566 s; pierwsza próba 634 s przerwana „stream interrupted”); K-R1b zrecenzowane w R9 (Gemini, 629 s, wspólnie z K-Z7b; werdykt poprawny 1,0)
- Dopuszczone alternatywy: Claude `wykonawca-opus` (logika przekrojowa z cichym błędem, ale bez niezmiennika wysokiej stawki — pula ŻÓŁTA); Claude `wykonawca`; Spark (zablokowany, 402)
- Powód wyboru: autor serwisu w tej samej linii zna mapy; recenzja krzyżowa z Gemini
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Gemini nieznany (jedno przerwanie strumienia), Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 89 %), 2026-10-07 14:46–15:20
- Pewność decyzji: średnia–wysoka
- Wynik pierwszego podejścia: zielony; łuk stopki potwierdzony w Chrome (`bty-reveal--in`, `clip-path: inset(0)`)
- Rundy korekt: 1 (K-R1b — wartownik zwalniany osobno z każdego obserwatora, idempotentne `observe` w atrapie, wczesne wyjście przy pustym zbiorze)
- Czas do akceptacji: ok. 8 min wykonawcy + dwie recenzje + korekta + walidacja fali
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): zgłoszone P1 „wyciek obserwacji w trybie mieszanym” — potwierdzone jako P2 (rzadki układ, ale cichy); P2 „hipoteza architekta o braku powiadomienia w jednym trybie jest błędna” — recenzent miał rację (wartownik jest zwalniany po odsłonięciu); P3 atrapa nieidempotentna — przyjęte; P3 wczesne wyjście — przyjęte
- Defekty po odbiorze: defekt pierwotny wykryty przez architekta w Chrome na zbudowanej aplikacji (diagnoza Playwright: `intersectionRatio` 0 dla celu z `clip-path`), nie przez testy ani recenzje
- Wymagane testy i dowody: Vitest (24 → 87 w pięciu specach), lint, format, build; odczyt `classList` i `clip-path` w Chrome

### BE-61 (BeautyEffect: Etap 2 P1 + K-Z7b — sprawdzenie szuflady w przeglądarce i powrót pozycji przewinięcia) — 2026-10-07
- Archetyp: (a) ręczne sprawdzenie dziesięciu scenariuszy szuflady przez worker z Playwright MCP; (b) poprawka komponentu z porządkiem zdarzeń routera (`RouterScroller` vs subskrybent `router.events`) i testem na prawdziwym `RouterScroller` (szew `APP_BOOTSTRAP_LISTENER`); 2 pliki
- Stawka: średnia (dostępność i wygoda nakładki na każdej stronie telefonu)
- Niepewność: średnia–wysoka (kolejność subskrybentów, mikrozadania, `scroll-behavior: smooth`)
- Wykonawca (linia / model / native effort): (a) Gemini / `gemini-3.8-flash-high` / `-Access write` z briefem bez zmian (1012 s; pierwsza próba `-Access read` 111 s — MCP odrzucone automatycznie); (b) Codex / `gpt-6.1-sol` / `high` (456 s)
- Recenzent (linia / model / native effort): (b) Gemini / `gemini-3.8-flash-high` / w nazwie, `-Access read` (R9, 629 s, wspólnie z K-R1b)
- Dopuszczone alternatywy: (a) `browser-check` flows — nie rozstrzyga stanów równych startowi (`passedWithoutActions`), Codex z Playwright (zajęty); (b) Claude `wykonawca` (pula ŻÓŁTA), Gemini (autor sprawdzenia, recenzent)
- Powód wyboru: (a) scenariusze historii i fokusu wymagają interakcji poza zakresem `browser-check`; (b) autor szuflady, logika routera — `high`
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Gemini nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 89 %), 2026-10-07 14:47–15:25
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: (a) 9/10 PASS, 1 FAIL (pozycja przewinięcia 468 → 0 po `Escape`); (b) zielony 38/38 testów, w Chrome Escape / przycisk / przyciemnienie / „wstecz” wracają do 479, wybór innej pozycji na górę
- Rundy korekt: 0
- Czas do akceptacji: ok. 25 min (sprawdzenie + poprawka + recenzja + walidacja w Chrome)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): (a) DEF-2 „znacznik szuflady po odświeżeniu” — odrzucone (dodaje najwyżej jeden zbędny wpis historii); (b) P2 „`popstate` na inny adres zwraca fokus do `Menu`” — odrzucone (przycisk `Menu` jest w stałym pasku powłoki, alternatywą jest fokus na `body`; pozycja przewinięcia nie jest wtedy przywracana); werdykt recenzenta: poprawny 0,98
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: Vitest, lint, format, build; skrypt Playwright architekta (sześć dróg zamknięcia, `scrollY` przed i po)

### BE-62 (BeautyEffect: Etap 2 Z12c + K-Z12c — podgląd elementów wspólnych na `/design/komponenty`) — 2026-10-07
- Archetyp: komponent podrzędny galerii podglądu składający sześć gotowych elementów (nagłówek sekcji, łuk, otwarcie, pas zamknięcia, film, odsłonięcia) + i18n + spec z AXE i atrapami mediów/obserwatora; 4 nowe pliki + 4 zmienione
- Stawka: niska (strona laboratoryjna poza indeksowaniem)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie, `-Access write` (743 s; K-Z12c 184 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (284 s)
- Dopuszczone alternatywy: Codex (zajęty K-Z7b, K-R1b); Claude `wykonawca` (pula ŻÓŁTA); Spark (zablokowany, 402)
- Powód wyboru: równoległość z Codexem; brak niezmiennika; recenzja krzyżowa z Codexem
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Gemini nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 89 %), 2026-10-07 15:11–15:45
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zielony (15 testów galerii); wykonawca zawęził selektory spec galerii do `:scope > section` (zagnieżdżone sekcje nowych komponentów) — przyjęte
- Rundy korekt: 1 (K-Z12c — zestaw zdjęć otwarcia 009 / 003 / 004 według planu i makiety części 16; brief architekta podał błędnie 004 / 019 / 009; zniszczenie fixture przed przywróceniem atrap mediów)
- Czas do akceptacji: ok. 16 min wykonawcy + recenzja + korekta + walidacja fali
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): P2 zestaw zdjęć niezgodny z planem — potwierdzone (błąd briefu); P3 kolejność sprzątania daje błąd jsdom `pause()` — potwierdzone; architekt przyjął drugi `<h1>` z prawdziwego `PageOpening` na stronie laboratoryjnej
- Defekty po odbiorze: oględziny zrzutu ujawniły płaski łuk pasa zamknięcia — defekt mixinu z etapu 1 (BE-63)
- Wymagane testy i dowody: Vitest, lint, format, stylelint, build; `browser-check` (`/design/komponenty` × 2 × 2), brak poziomego przewijania przy 320 px

### BE-63 (BeautyEffect: Etap 2 K-SEP — mixin `arc-top`: `list.slash()` i test kompilacji SCSS) — 2026-10-07
- Archetyp: poprawka mixinu SCSS motywu (dzielenie Sass zamiast separatora `/`) + nowy spec kompilujący SCSS przez `sass.compileString` zamiast testu tekstu źródła; 3 pliki
- Stawka: niska–średnia (łuki pasa zamknięcia i stopki na każdej stronie; cicha awaria — przeglądarka odrzuca deklarację)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `medium` (39 s STOP + 160 s)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie, `-Access read` (R11, 832 s, wspólnie z Z13)
- Dopuszczone alternatywy: Gemini (zajęty Z12c); Claude `mechanik` (zmiana dwóch linii, ale test kompilacji wymaga oceny); Spark (zablokowany, 402)
- Powód wyboru: mała poprawka z testem — `medium`; recenzja krzyżowa z Gemini
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Gemini nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 89 %), 2026-10-07 15:33–15:38
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: STOP — `arch-photo.spec.ts` sprawdzał dosłowny tekst starych deklaracji poza zakresem briefu; wykonawca miał rację; po rozszerzeniu zakresu zielony (4 testy czerwone → 41/41)
- Rundy korekt: 0 (jeden restart po STOP)
- Czas do akceptacji: ok. 4 min wykonawcy + walidacja w Chrome (`borderRadius` pasa `50% 50% 0 0 / 48px 48px 0 0`)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): brak w plikach K-SEP; P3 `sass` jako zależność przechodnia (`@angular/build`, przypięty 1.104.1) w teście kompilacji — przyjęte jako znane ryzyko, bez zmiany `package.json`; werdykt recenzenta: poprawny 1,0
- Defekty po odbiorze: defekt pierwotny wykryty przez architekta przy oględzinach zrzutu `browser-check` i pomiarze `getComputedStyle`; testy tekstu SCSS z etapu 1 i recenzje go nie wykryły — lekcja: kontrakty SCSS z wartościami złożonymi sprawdzać kompilacją
- Wymagane testy i dowody: Vitest (kompilacja SCSS), lint, stylelint, format, build; pomiar w Chrome

### BE-64 (BeautyEffect: Etap 2 Z13 — preload ikon `primeicons` tylko w WOFF2 zamiast `.eot`) — 2026-10-07
- Archetyp: diagnoza narzędzia budowania (Beasties w `@angular/build` preloaduje pierwszy `url()` użytego `@font-face`) + własny `@font-face` motywu, skrypt generujący klasy `.pi` z pakietu bez deklaracji fontu, podpięcie w `angular.json` i skryptach `npm` + spec kompilacji; 5 plików
- Stawka: niska–średnia (zbędne pobranie na każdej stronie; ryzyko utraty ikon przy złym imporcie)
- Niepewność: średnia (mechanizm w `node_modules`, opcje Beasties zaszyte na sztywno)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `medium` (311 s, sam w drzewie — z `npm run build`)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / w nazwie, `-Access read` (R11, 832 s, wspólnie z K-SEP)
- Dopuszczone alternatywy: Codex `high`; Gemini (recenzent fali); Claude `wykonawca` (pula ŻÓŁTA); Spark (zablokowany, 402)
- Powód wyboru: diagnoza z jasnym kierunkiem z planu i zakazami (bez `inlineCritical: false`, bez zależności) — `medium` wystarcza; recenzja krzyżowa z Gemini
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany, Gemini nieznany, Spark zablokowany (402), Claude ostrzegawczy (ŻÓŁTY, tydzień 89–90 %), 2026-10-07 15:43–16:05
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zielony; w zbudowanym HTML brak `.eot`, preload `primeicons-*.woff2`; ikony renderują się w Chrome (`document.fonts` — załadowany)
- Rundy korekt: 0 (dwie jednolinijkowe poprawki architekta po recenzji, reguła 11)
- Czas do akceptacji: ok. 5 min wykonawcy + recenzja + walidacja na zbudowanym SSR
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): P2 `prewatch` bez generatora licencji PrimeUI — potwierdzone, poprawione; P3 asymetryczna normalizacja CRLF w spec — potwierdzone, poprawione; P3 `sass` jako zależność przechodnia — przyjęte jako znane ryzyko (przypięty przez `@angular/build`, dodanie wymaga zmiany lockfile); werdykt recenzenta: poprawny 0,98
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu; obserwacja poza zakresem — Beasties preloaduje też wiele plików fontów `latin-ext` i kursywy na każdej stronie (wydajność, do decyzji)
- Wymagane testy i dowody: Vitest (kompilacja SCSS, zgodność klas z pakietem), lint, format, build (5 prerenderowanych tras); `grep .eot` w `dist`, preload w HTML, Chrome na `127.0.0.1` (pułapka cienia `ng serve` na `[::1]:4200`)

### BE-65 (BeautyEffect: Etap 3 H2a + H2a-k1 + K2 — film otwarcia `HeroFilm`) — 2026-10-07
- Archetyp: komponent prezentacyjny z imperatywnym API mediów (autostart w `afterNextRender` przez `defer(from(play()))`, przycisk wstrzymania, reakcja na zmianę `prefers-reduced-motion`), łuk z obrysem i ruchem wejścia w SCSS; 4 pliki
- Stawka: niska–średnia (otwarcie strony głównej; przycisk nie może kłamać o stanie filmu)
- Niepewność: średnia (odrzucenie `play()`, zmiana ustawień ruchu w trakcie)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (472 s); korekty `medium` (H2a-k1 144 s po przerwanym limitem przebiegu 23 s; K2 126 s wspólnie z BE-66)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `high`, `-Access read` (308 s, wspólnie z BE-66)
- Dopuszczone alternatywy: Gemini (wykonawca H1 w tej fali); Spark (zablokowany 402 przy przydziale); Claude `wykonawca` (pula ŻÓŁTA)
- Powód wyboru: logika mediów i stanów przycisku — `high`; korekty z gotowymi decyzjami — `medium`
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany → zablokowany (limit 16:47 lokalnie, reset 18:01) → nieznany; Spark zablokowany (402) → znany (sonda 18:05); Claude ostrzegawczy (ŻÓŁTY, tydzień 90–91 %), 2026-10-07 16:38–18:22
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zielony, ale z błędnych przesłanek architekta (próg `sm`/`lg` zamiast `md` z AT-SPEC dla sekcji strony głównej; obrys przy najechaniu) — korekta H2a-k1
- Rundy korekt: 2 (H2a-k1 — błąd briefu; K2 — znalezisko recenzji)
- Czas do akceptacji: ok. 4 h zegarowo (przerwa na limit Codexa i 402 Sparka); pracy wykonawcy ok. 12 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): P3 `load()` przy zmianie na `reduce`, gdy film nie grał — potwierdzone, poprawione w K2 (wzór `VideoClip`); P3 zapis sygnału po zniszczeniu przy odrzuconym `play()` — odrzucone (`onDestroy` odpina `playSubscription`, więc `catchError` nie startuje); werdykt recenzenta: poprawny 0,9
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: Vitest 15/15, lint, format, build (prerender `/`); `browser-check` po złożeniu strony (H8)

### BE-66 (BeautyEffect: Etap 3 H3a + H3a-k1 + K2 — kafel kategorii `CategoryTile`) — 2026-10-07
- Archetyp: komponent prezentacyjny — jeden odnośnik na kafel, zdjęcie albo `VideoClip` z restartem przy najechaniu i fokusie, kurtyna W-3, modyfikatory `large`/`featured`; 4 pliki
- Stawka: niska–średnia (8 wejść do oferty na stronie głównej; nazwa dostępna odnośnika)
- Niepewność: niska–średnia
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `medium` (290 s); H3a-k1 `high` przerwany limitem (80 s), ponowiony `medium` (140 s); K2 `medium` (126 s, wspólnie z BE-65)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `high`, `-Access read` (308 s, wspólnie z BE-65)
- Dopuszczone alternatywy: Gemini; Spark (zablokowany 402 przy przydziale); Claude `wykonawca` (pula ŻÓŁTA)
- Powód wyboru: mały komponent na gotowym `VideoClip` — `medium`
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-65
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zielony, ale z trzech błędnych przesłanek architekta (`large` tylko jako wysokość, uniesienie R-2 na kaflach, próg `sm` zamiast `md`) — korekta H3a-k1
- Rundy korekt: 2 (H3a-k1 — błąd briefu; K2 — znalezisko recenzji)
- Czas do akceptacji: ok. 4 h zegarowo (przerwy na limity); pracy wykonawcy ok. 9 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): P1 licznik identyfikatorów przecieka między żądaniami SSR — odrzucone jako P1 (`id` i `aria-labelledby` z tej samej instancji są spójne w HTML serwera, a pierwsza detekcja zmian po hydracji przepisuje oba), ale usunięte razem z P2; P2 nazwa dostępna = sam tytuł nie zawiera widocznego opisu (WCAG 2.5.3) — potwierdzone, K2: nazwa z treści odnośnika, bez `aria-labelledby` i licznika; P3 martwe zdarzenia w specu — potwierdzone, usunięte; P3 `objectPosition` ignorowane dla kafli z filmem — przyjęte (żaden wpis danych go nie ustawia); werdykt recenzenta: niepoprawny 0,7 → po K2 zgodny
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: Vitest 12/12 (z AXE), lint, format, build; oględziny mozaiki po H3b

### BE-67 (BeautyEffect: Etap 3 H1 + H1-k1 — teksty i dane strony głównej) — 2026-10-07
- Archetyp: dane i i18n — klucze `pl.json`, tablice kategorii i godzin otwarcia z testami danych; ok. 8 plików
- Stawka: niska (treść publiczna, bez niezmiennika)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` (513 s); H1-k1 ten sam (366 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (196 s); H1-k1 w recenzji fali 2 (413 s, wspólnie z BE-68 i BE-69)
- Dopuszczone alternatywy: Spark; Codex (pula zostawiona na recenzje); Claude `mechanik` (pula ŻÓŁTA)
- Powód wyboru: tekstowy brief bez makiety i bez niezmiennika
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini — znany (udane przebiegi tego dnia); Codex — nieznany (wrapper bez zapasu)
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zielony, ale testy nie przypinały danych (zgodność kluczy bez trójek `path`/`nameKey`/`descriptionKey` i bez pełnych rekordów godzin)
- Rundy korekt: 1 (H1-k1 — wspólny helper `getNestedTranslation`, pełne trójki 8 kategorii i 7 rekordów godzin)
- Czas do akceptacji: ok. 25 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): P2 słabe testy danych — potwierdzone, H1-k1; recenzja H1-k1 bez znalezisk
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: Vitest, lint, format, build; uwaga — „pusty diff” Gemini z `git diff` na pliku nieśledzonym niczego nie dowodzi, dowodem jest spec przypinający dane

### BE-68 (BeautyEffect: Etap 3 H2b — otwarcie strony głównej `HomeOpening`) — 2026-10-07
- Archetyp: sekcja prezentacyjna z gotowym dzieckiem (`HeroFilm`) — `h1` z ukrytym myślnikiem, plamy tła, CTA; 4 pliki
- Stawka: niska–średnia (jedyny `h1` strony, SEO)
- Niepewność: niska–średnia
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` (877 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (413 s, wspólnie z BE-67 i BE-69)
- Dopuszczone alternatywy: Spark (równolegle zajęty H3b/H5); Codex (pula na recenzje)
- Powód wyboru: tekstowy brief z dokumentem strony i makietą, bez Figmy
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-67
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowany bez korekty
- Rundy korekt: 0
- Czas do akceptacji: ok. 30 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): brak potwierdzonych dla `HomeOpening`
- Defekty po odbiorze: „Zobacz ofertę” 121 × 30 px wobec wymogu planu ≥ 44 px — wykryte pomiarem architekta w przeglądarce; przyczyna wspólna (`.bty-link--arrow` bez `min-height`), naprawione globalnie w BE-69 (KG2)
- Wymagane testy i dowody: Vitest z AXE, lint, format, build, `browser-check` (16 zrzutów, przepływ pauzy filmu PASS)

### BE-69 (BeautyEffect: Etap 3 H4 + KG1 + KG2 — bento „Wyróżniki salonu” `SalonHighlights`) — 2026-10-07
- Archetyp: sekcja prezentacyjna — bento na siatce Bootstrapa z `display: contents` poniżej `md`, rysowane SVG (wieniec, piktogramy), kurtyna zdjęcia; 4 pliki (+ `links.scss`, `links.spec.ts`, `reveal-styles.spec.ts` w KG2)
- Stawka: niska–średnia
- Niepewność: średnia (kolejność kafli na telefonie, odsłanianie rysunków)
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` — H4 (896 s), KG1 (670 s), KG2 (680 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` — `high` (413 s fala 2; 396 s korekty), `medium` (runda 2)
- Dopuszczone alternatywy: Spark (korekty wracają do autora, o ile się kwalifikuje)
- Powód wyboru: tekstowy brief, autor korekt = autor kodu
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-67
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zielony, z czterema defektami z recenzji
- Rundy korekt: 2 (KG1 — recenzja; KG2 — pomiar w przeglądarce i recenzja korekt)
- Czas do akceptacji: ok. 1 h 15 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): zdjęcie-treść pod `aria-hidden` — potwierdzone; podwójny odstęp `row-gap` + rynna (40 px zamiast 20) — potwierdzone; stany ukryte rysunków bez JS — potwierdzone (wspólny mixin `reveal-local.pending`, BE-74); test nie łapał usunięcia stanu końcowego kresek — potwierdzone; test keyframes bezpiecznika nie łapał usunięcia `scale: none` — potwierdzone, KG2
- Defekty po odbiorze: nazwy urządzeń sklejone (Angular usuwa białe znaki między elementami) — przy 768 px wystają 49 px, czytnik ekranu czyta „EndosferaNeoPulseBloomea”; wykryte pomiarem architekta, KG2 (`&ngsp;`) z kontrolą czerwony → zielony
- Wymagane testy i dowody: Vitest z AXE, lint, format, build, pomiar `scrollWidth` 320/390/768, `browser-check`, kontrola bez JS i przy `reduce`

### BE-70 (BeautyEffect: Etap 3 H3b + KS1 — mozaika kategorii `OfferMosaic`) — 2026-10-07
- Archetyp: sekcja prezentacyjna — 8 kafli `CategoryTile` w jednym `.row.g-3`, para Twarz/Ciało `col-md-3`, łuk górny; 4 pliki
- Stawka: niska–średnia (8 wejść do oferty)
- Niepewność: średnia (układ pary na telefonie)
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh` (361 s); KS1 `xhigh` (683 s, wspólnie z BE-71 i BE-73)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (726 s, wspólnie z BE-71–73); korekty — Codex `gpt-6.1-sol` `high` (396 s)
- Dopuszczone alternatywy: Codex (pula na recenzje, pamięć `spark-przejmuje-prosta-prace`); Gemini
- Powód wyboru: prosty brief tekstowy — Spark przejmuje prostą pracę
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark — znany (udane przebiegi, brak komunikatu limitu); Gemini — znany
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zielony; Spark wykazał trzy błędne przesłanki briefu (zapis `col-6` bez `col-md-3`, `arc-top` przełącza się przy `sm`, brak wejścia indeksu kaskady)
- Rundy korekt: 1 (KS1)
- Czas do akceptacji: ok. 1 h
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): test nie wykrywał usunięcia `col-md-3` z kontenera pary — potwierdzone; `objectPosition` z danych gubiony — potwierdzone; oba KS1
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: Vitest 13 z AXE, lint, format, build, `browser-check` (przepływ wejścia w kategorię PASS)

### BE-71 (BeautyEffect: Etap 3 H5 + KS1 + KS3 — ścieżka rezerwacji `BookingPath`) — 2026-10-07
- Archetyp: sekcja prezentacyjna — `ol` trzech kroków, linia rysowana, piktogramy SVG, poświata w ciemnym motywie; 4 pliki
- Stawka: niska–średnia
- Niepewność: niska–średnia
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh` (443 s); KS1 `xhigh`; KS3 `high` (281 s, wspólnie z BE-72 i BE-73)
- Recenzent (linia / model / native effort): Gemini `flash-high` (fala); Codex `gpt-6.1-sol` `high` (korekty), `medium` (runda 2)
- Dopuszczone alternatywy: Codex; Gemini
- Powód wyboru: jak BE-70
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-70
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zielony; poświata ciemnego motywu martwa od początku, a spec przypinał wadliwy selektor jako kontrakt
- Rundy korekt: 2 (KS1, KS3)
- Czas do akceptacji: ok. 1 h 20 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): niejawny `accentWordIndex`, brak testu `ol`, nierówne wiersze kroków poniżej `md`, stany ukryte bez JS — potwierdzone, KS1; P2 `.app-dark .x` nie pasuje przy enkapsulacji emulowanej (`<html>` bez atrybutu komponentu) — potwierdzone, KS3 + strażnik `dark-selector-guard.spec.ts` dla wszystkich stylów komponentów
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: Vitest 15 z AXE, lint, format, build, pomiar `display` poświaty w obu motywach, zrzut ciemnego motywu

### BE-72 (BeautyEffect: Etap 3 H6 + KS2 + KS3 — aktualności `SocialNews` i `PhoneScene`) — 2026-10-07
- Archetyp: sekcja prezentacyjna z ozdobną sceną telefonu (rama, karty, film) — po KS2 dwa komponenty; 8 plików
- Stawka: niska
- Niepewność: średnia (budżet stylów, odwzorowanie urządzenia rolami kolorów)
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh` (551 s); KS2 `xhigh` (372 s); KS3 `high`
- Recenzent (linia / model / native effort): Gemini `flash-high` (fala); Codex `gpt-6.1-sol` `high` / `medium`
- Dopuszczone alternatywy: Codex; Gemini
- Powód wyboru: jak BE-70
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-70
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zielony; plan zawierał błąd architekta (odznaki profili w ekranie — wariant S-3 zamiast wybranego S-1), poprawiony przed startem; Spark wykazał błędne przesłanki briefu (szerokość kolumny, brak „czystej klasy” w `RevealKind`, kolory urządzenia bez dokładnych ról)
- Rundy korekt: 2 (KS2, KS3)
- Czas do akceptacji: ok. 1 h 20 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): budżet `anyComponentStyle` 7,61 kB > 6 kB (build architekta) — KS2 wydzielił `PhoneScene`; podkreślenie przy `reduce` niewidoczne — KS2; stany ukryte bez JS — KS2; P2 rola metalu w ciemnym motywie martwa (`.app-dark` przy enkapsulacji) — KS3; P2 rynna 64 px na każdej szerokości → przewijanie poziome 12 px przy 320/390 px (recenzja i pomiar architekta) — KS3
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: Vitest 17 z AXE, lint, format, build bez ostrzeżenia budżetu, pomiar `scrollWidth`, `browser-check`

### BE-73 (BeautyEffect: Etap 3 H7 + KS1 + KS3 — „Gdzie nas znaleźć” `FindUs`) — 2026-10-07
- Archetyp: sekcja prezentacyjna z małą logiką (dzień tygodnia w Europe/Warsaw po stronie przeglądarki) — łuk z adresem, godziny, CTA; 6 plików
- Stawka: niska–średnia (dane kontaktowe)
- Niepewność: średnia (kolejność fokusu przy `display: contents`)
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh` (487 s); KS1 `xhigh`; KS3 `high`
- Recenzent (linia / model / native effort): Gemini `flash-high` (fala); Codex `gpt-6.1-sol` `high` / `medium`
- Dopuszczone alternatywy: Codex; Gemini
- Powód wyboru: jak BE-70
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-70
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zielony; kolejność fokusu sprzeczna z wizualną wynikała z DOM przepisanego w briefie (błąd architekta)
- Rundy korekt: 2 (KS1, KS3)
- Czas do akceptacji: ok. 1 h 20 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): zdanie z „Kontakt” przed adresem w kolejności fokusu — potwierdzone, KS1 (osobna kolumna `order-4 order-md-3`, test kolejności); stany ukryte godzin bez JS — KS1; P2 numer telefonu 36 px wobec wymogu planu ≥ 44 px — potwierdzone, KS3 (wcześniej błędnie przyjęte przez architekta z uzasadnieniem WCAG 2.5.8; plan wiąże)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: Vitest 17 z AXE, lint, format, build, pomiar celów dotykowych, „Dziś” na właściwym dniu w zrzucie

### BE-74 (BeautyEffect: Etap 3 T — mixin `reveal-local.pending` z bezpiecznikiem W-3) — 2026-10-07
- Archetyp: wspólny mixin SCSS + rozszerzenie keyframes, test kompilacji; 3 pliki
- Stawka: średnia (przekrojowo — po nieudanym starcie aplikacji treść nie może zniknąć na stałe)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `high` (85 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (396 s, wspólnie z korektami BE-69–73)
- Dopuszczone alternatywy: Gemini; Codex
- Powód wyboru: krótki brief z gotowym kodem mixinu, przed trzema równoległymi korektami korzystającymi z jego API
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-70
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany (API dokładnie jak w briefie); architekt dopisał do briefów korekt ograniczenie — bezpiecznik wymusza `transform: none` i `clip-path: inset(0)`, więc mixin tylko na elementach bez spoczynkowego `transform`
- Rundy korekt: 0 (test keyframes uzupełniony w KG2, BE-69)
- Czas do akceptacji: ok. 10 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): P2 test nie kompilował rzeczywistych keyframes — potwierdzone, KG2
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: Vitest, kontrola bez JS i przy `reduce` w przeglądarce (0 elementów ukrytych w 4 przypadkach)

### BE-75 (BeautyEffect: Etap 3 H8 + H8-k1 — złożenie strony głównej, SEO, AXE `Home`) — 2026-10-07
- Archetyp: złożenie sześciu gotowych sekcji + `Seo.apply` + AXE całej strony; 5 plików
- Stawka: niska–średnia (SEO trasy `/`)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `high` (149 s); H8-k1 `medium` (104 s)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (350 s); H8-k1 w rundzie 2 Codex `gpt-6.1-sol` `medium` (104 s, wspólnie z KS3 i KG2: bez defektów, 6/6 poprawne)
- Dopuszczone alternatywy: Gemini; Codex
- Powód wyboru: mechaniczne złożenie według gotowej tabeli selektorów
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-70
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zielony (4/4, AXE całej strony bez naruszeń)
- Rundy korekt: 1 (H8-k1)
- Czas do akceptacji: ok. 25 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): P2 test SEO tautologiczny (brak klucza → komponent i test dostają ten sam klucz) — potwierdzone, H8-k1: wartości z `pl.json` przez `getNestedTranslation`, kontrola czerwona
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: Vitest, lint, format, build (prerender 5 tras), SSR na 127.0.0.1 (tytuł, kanoniczny, jeden `h1`), `browser-check` 16/16 + 2/2

### BE-76 (BeautyEffect: Etap 4 D4-A — UI-OFERTA punkt 5 i zdjęcia; „Rzęsy i brwi” w układzie wzoru) — 2026-10-07
- Archetyp: dokumentacja produktu — wspólny układ stron kategorii + dopasowanie strony do wzoru, wybór zdjęć z oglądem klatek filmów; 2 pliki
- Stawka: niska–średnia (źródło prawdy dla etapu 4 FE; bez niezmiennika)
- Niepewność: średnia (przypisanie plików podglądu do katalogu, kadry filmów)
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / `-Access write` (1146 s)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh`, `-Access read` (188 s)
- Dopuszczone alternatywy: Spark (wykonawca); Codex (recenzent)
- Powód wyboru: brief tekstowy z oglądem zdjęć i ffmpeg na Windows; przy ŻÓŁTYM tygodniu Claude'a tekst idzie do Spark/Gemini, Spark miał cztery równoległe briefy tej fali
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook, tydzień 93 %, 2026-10-07); Gemini nieznany (brak komunikatu limitu); Spark nieznany
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowany z jedną luką (brak nagłówka zamknięcia `Ceny i rezerwacja`); błąd briefu (opis kadru w kolumnie tekstu alternatywnego) wykonawca słusznie przeniósł do kolumny „Plik”
- Rundy korekt: 0 (dwie jednolinijkowe poprawki architekta)
- Czas do akceptacji: ok. 45 min (z recenzją i oglądem klatek)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): P1 brak nagłówka zamknięcia — potwierdzone; P1 kafle uzupełnienia a karta „Ściągnięcie” — odrzucone (makieta części 7/8 zatwierdzona przez właściciela); P2 łuk prawy na kadr filmu — odrzucone (ten sam plik dwa razy na stronie, film jest banerem); P2 napisy w kadrach 7 s / 9 s — architekt obejrzał, brak napisów, dopisana adnotacja; P3 ×2 — pozostawione
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: skrypt kontroli kotwic, fragmentów, nazw Booksy i linków; ogląd klatek filmów

### BE-77 (BeautyEffect: Etap 4 D4-B — „Manicure i pedicure” w układzie Z-2 z kartą KA-1) — 2026-10-07
- Archetyp: dokumentacja produktu — przebudowa strony kategorii na wzór, szkice opisów, wybór zdjęć; 1 plik
- Stawka: niska
- Niepewność: niska–średnia
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh` (244 s)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (587 s, wspólnie z D4-E)
- Dopuszczone alternatywy: Gemini (wykonawca); Codex (recenzent)
- Powód wyboru: brief tekstowy z gotowymi grupami; Spark z oglądem zdjęć przez interop
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-76
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany z jedną usterką
- Rundy korekt: 0 (poprawka architekta: przywrócone dwie linie)
- Czas do akceptacji: ok. 40 min (z recenzją)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): P2 usunięte pytanie o rolkę Instagrama (pielęgnacja domowa stóp) i odnośnik do migawki Instagrama — potwierdzone; zakaz briefu dotyczył treści starej strony, nie Instagrama
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: skrypt kontroli dokumentów kategorii

### BE-78 (BeautyEffect: Etap 4 D4-C + D4-K — „Pielęgnacja twarzy” w układzie Z-2, wiernie z Booksy) — 2026-10-07
- Archetyp: dokumentacja produktu — przebudowa strony z wyjątkiem „wiernie z Booksy” (16 kart, 7 długich), ogląd klatek filmów; 1 plik
- Stawka: średnia (wierność tekstów Booksy — decyzja właściciela)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh` (933 s); D4-K `high` (576 s, wszystkie cztery pliki w jednym przebiegu)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (762 s, wspólnie z D4-D)
- Dopuszczone alternatywy: Gemini (wykonawca); Gemini (recenzent)
- Powód wyboru: najdłuższy brief fali z wiernością Booksy; recenzja wierności — Sol z innej rodziny
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-76; Codex nieznany
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: treść kart poprawna (kompletność Booksy potwierdzona przez recenzenta), ale przepisane wszystkie sekcje chronione briefem (z błędami: nawigacja bez dwóch kategorii, „ceny” w SEO, wizytówka Google w wejściach) i zbyt ostrożnie pominięty jedyny czysty film
- Rundy korekt: 1 (D4-K; tekst dyktowany, diff sprawdzony przez architekta zamiast osobnej recenzji — nowe szkice pochodzą z propozycji recenzenta Codex; Spark sam wykrył i naprawił zbyt szeroką podmianę sekcji, jedno zdanie o filmie 002 poprawił architekt)
- Czas do akceptacji: ok. 80 min (wykonanie, recenzja, korekta D4-K)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): P2 baner — dostępny film 002 — potwierdzone (architekt wybrał fragment 8,5–10,5 s oglądem); P2 zmieniony zakres „Użytkowników” — potwierdzone, a architekt ustalił, że przepisano też „Cel”, „Dziedziczone wymagania”, „Wejścia”, „Nawigację” i SEO
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: skrypt kontroli; porównanie sekcji chronionych z wersją sprzed fali

### BE-79 (BeautyEffect: Etap 4 D4-D + D4-K — „Pielęgnacja ciała” i „Medycyna estetyczna”, wiernie z Booksy) — 2026-10-07
- Archetyp: dokumentacja produktu — dwie strony z wyjątkiem „wiernie z Booksy”, szkice dla zabiegów bez opisu; 2 pliki
- Stawka: średnia (zabiegi medyczne, wierność Booksy)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh` (1030 s); D4-K `high` (576 s, wszystkie cztery pliki w jednym przebiegu)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (762 s, wspólnie z D4-C)
- Dopuszczone alternatywy: Gemini (wykonawca); Gemini (recenzent)
- Powód wyboru: jak BE-78
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-78
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: teksty Booksy kompletne; szkice dopowiadały niepotwierdzone szczegóły
- Rundy korekt: 1 (D4-K; tekst dyktowany, diff sprawdzony przez architekta zamiast osobnej recenzji — nowe szkice pochodzą z propozycji recenzenta Codex; Spark sam wykrył i naprawił zbyt szeroką podmianę sekcji, jedno zdanie o filmie 002 poprawił architekt)
- Czas do akceptacji: ok. 80 min (wykonanie, recenzja, korekta D4-K)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): P2 nieprawdziwe przypisanie podziału do podglądu części 15 (×2; ten sam błąd architekt znalazł też w „Piercingu”) — potwierdzone; P2 masaż ajurwedyjski „ciała, z olejem” wbrew otwartej KO — potwierdzone; P2 termoaktywny „rozgrzewanie, potem masaż” bez źródła — potwierdzone; P2 urwany opis karty Bloomea — potwierdzone; P2 dwa pierwsze zdania Booksy na karcie NeoPulse — odrzucone (pytanie retoryczne i slogan nie mówią, czym jest zabieg; pełny tekst zostaje w „Dalszym opisie”)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: skrypt kontroli; porównanie z migawką Booksy

### BE-80 (BeautyEffect: Etap 4 D4-E + D4-K — „Piercing” w układzie Z-2) — 2026-10-07
- Archetyp: dokumentacja produktu — przebudowa strony kategorii bez zdjęć w katalogu (tylko jeden czysty film); 1 plik
- Stawka: niska–średnia (zdanie o wieku 18+)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh` (322 s); D4-K `high` (576 s, wszystkie cztery pliki w jednym przebiegu)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (587 s, wspólnie z D4-B)
- Dopuszczone alternatywy: Gemini (wykonawca); Codex (recenzent)
- Powód wyboru: jak BE-77
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-76
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany z dwiema usterkami
- Rundy korekt: 1 (D4-K, jedno zdanie) + jedna linia architekta
- Czas do akceptacji: ok. 80 min (wykonanie, recenzja, korekta D4-K)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): P1 (zgłoszone; realnie P2) brak pozycji „Treści do dostarczenia” o zdjęciach w miejsce paneli — potwierdzone; P3 zmiana opisu SEO (wiek tylko dla przekłuć igłowych) — zaakceptowana jako konieczna; przegapione przez recenzenta: nieprawdziwe zdanie o podglądzie części 15 (wykryte przez architekta po recenzji R2)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: skrypt kontroli dokumentów kategorii

### BE-81 (BeautyEffect: Etap 4 D5-1 — decyzja z 2026-10-07, PROD-OFERTA, mapa stron, kwestie otwarte, WP-UMOW-WIZYTE) — 2026-10-07
- Archetyp: dokumentacja produktu — zapis decyzji właściciela i jej skutków w dokumentach produktu, przekierowania z przypisaniem do migawek; 9 plików + nowa decyzja
- Stawka: niska–średnia (źródło prawdy zakresu oferty; bez niezmiennika)
- Niepewność: średnia (przypisanie starych adresów do zabiegów, zawężenie kwestii otwartej)
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / `-Access write` (947 s)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh`, `-Access read`, diff w briefie (295 s)
- Dopuszczone alternatywy: Spark (wykonawca); Codex (recenzent)
- Powód wyboru: brief tekstowy na wielu plikach Windows; przy ŻÓŁTYM tygodniu Claude'a tekst idzie do Spark/Gemini, Spark miał w tej fali trzy inne briefy
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook, tydzień 94 %, 2026-10-07); Gemini znany (`agy /quota` przed falą: okno 53 %, tydzień 83 %); Spark nieznany
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowany; recenzent: wszystkie 13 plików „gotowy”; wykonawca wypisał 5 nieaktualnych miejsc poza zakresem (3 poprawił architekt, 2 to zapisy historyczne)
- Rundy korekt: 0 (jednolinijkowe poprawki architekta: uwaga przekierowania, wiązanie decyzji z DEC-BOOKSY-REZERWACJA-I-CENY)
- Czas do akceptacji: ok. 40 min (praca równoległa z resztą fali)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): P3 `/zamykanie-naczynek-2/` dotyczy twarzy i nóg — potwierdzone; P2/P3 w plikach innego autora (SEO strony głównej, streszczenia „wyłącznie w Booksy”) — potwierdzone, przypisane D5-4; stare makiety z masażem ajurwedyjskim w ciele — odrzucone (zapis historyczny wyborów)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: kontrola linków (148 plików, 0 martwych), skrypt kotwic kategorii, przeliczenie liczby zabiegów przez recenzenta

### BE-82 (BeautyEffect: Etap 4 D5-2 — nowa strona „Zabiegi laserowe” ze starej strony, prostym językiem) — 2026-10-07
- Archetyp: dokumentacja produktu — nowy dokument strony kategorii, szkice opisów i zaleceń przed/po zabiegu z migawek starej strony, bez obietnic; 1 plik
- Stawka: średnia (zalecenia przed i po zabiegach laserowych — błąd treści zdrowotnej przechodzi do implementacji)
- Niepewność: średnia–wysoka (migawki starej strony z szablonu, sprzeczne terminy w źródłach)
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh` (368 s; korekta D5-2K 336 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (741 s, wspólnie z D5-3, D5-4 i poprawkami architekta)
- Dopuszczone alternatywy: Gemini (wykonawca, `high`); Gemini (recenzent)
- Powód wyboru: tekst z wiernością źródłom wymaga dokładności, Spark `xhigh` miał dobre wyniki w D4; recenzja wierności źródłom na Codexie (w D4 R2 6 z 7 trafnych), Gemini miał w tej fali D5-1
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook, tydzień 94 %); Spark nieznany; Codex nieznany (brak komunikatu limitu)
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: odrzucony do korekty — budowa, kotwice, zamknięcie i panele poprawne, ale 10 odchyleń od źródeł w zaleceniach (sprzeczne terminy antybiotyków rozstrzygnięte po cichu, retinoidy bez rozróżnienia doustne/miejscowe, zakazy opalania skrócone, zapewnienia o bezpieczeństwie przeniesione z migawki)
- Rundy korekt: 1 (D5-2K, wszystkie punkty zgodne z propozycjami recenzenta; architekt sprawdził cytaty w migawkach przed korektą)
- Czas do akceptacji: ok. 55 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): P1 sprzeczne przerwy po antybiotykach — potwierdzone; P2 ×9 (retinoidy, słońce/sauna/alkohol, opalanie po naczynkach, opalanie między sesjami depilacji, „żyłki pod skórą”, „komórki barwnika”, nazwy fachowe bez objaśnienia, zapewnienia o omijaniu zdrowych tkanek, lista urządzeń) — wszystkie potwierdzone
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: architekt sprawdził cytaty P1/P2 w migawkach jednym poleceniem; skrypt kotwic i fragmentów; kontrola linków

### BE-83 (BeautyEffect: Etap 4 D5-3 — masaż ajurwedyjski z „Pielęgnacji ciała” do „Pielęgnacji twarzy”) — 2026-10-07
- Archetyp: dokumentacja produktu — przeniesienie jednej karty między zatwierdzonymi dokumentami z przeliczeniem; 2 pliki
- Stawka: niska
- Niepewność: niska
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `high` (189 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (wspólny przebieg z BE-82)
- Dopuszczone alternatywy: Gemini (wykonawca); Gemini (recenzent)
- Powód wyboru: prosta, dobrze określona zmiana — Spark `high` (pamięć: prosta praca na Sparku, pula Codexa na recenzje)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-82
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany; wykonawca słusznie zgłosił nieaktualne „ośmiu kategorii” w chronionej „Nawigacji” (poprawił architekt)
- Rundy korekt: 0
- Czas do akceptacji: ok. 15 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): brak — oba pliki „gotowy”
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: skrypt kotwic (kotwica raz w twarzy, zero w ciele), liczby zakładek, statusy

### BE-84 (BeautyEffect: Etap 4 D5-4 — dziewiąta kategoria w UI-OFERTA i na stronie głównej) — 2026-10-07
- Archetyp: dokumentacja produktu — zmiana liczby kategorii i wyjątku zamknięcia w dwóch zatwierdzonych dokumentach; 2 pliki
- Stawka: niska–średnia
- Niepewność: niska
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `high`
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (wspólny przebieg z BE-82); dodatkowo uwagi Sparka z recenzji BE-81
- Dopuszczone alternatywy: Gemini (wykonawca); Gemini (recenzent)
- Powód wyboru: jak BE-83
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-82
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany w zakresie briefu; luka briefu architekta — brief nie kazał dopasować zdań „ceny i rezerwacja w Booksy” (zdanie wiodące sekcji 2 strony głównej, opis SEO, streszczenia decyzji, tekst sekcji 3 „Oferty”) ani rodzica `interfejsy/strony-publiczne/README.md` i WP-TRESCI-BEZOBSLUGOWE
- Rundy korekt: 0 (poprawki architekta — gotowe teksty z recenzji; dwuznaczne zdanie o przycisku nagłówka poprawione przez architekta po uwadze autora D5-2)
- Czas do akceptacji: ok. 50 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): P2 wyjątek telefoniczny w ogólnych tekstach rezerwacji — potwierdzone częściowo (trzy kroki rezerwacji w Booksy na stronie głównej zostają: opisują główną drogę); P2 wyjątek u nadrzędnego interfejsu i w WP-TRESCI-BEZOBSLUGOWE — potwierdzone; P2 (Spark) opis SEO strony głównej — potwierdzone (tytuł bez zmian ze względu na długość)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: kontrola „osiem/ośmiu” w kontekście kategorii; kontrola linków

### BE-85 (BeautyEffect: Etap 4 P17 — podgląd części 17: mozaika 9 kafli, siatka 9 łuków, otwarcie bez zdjęć) — 2026-10-07
- Archetyp: podgląd HTML do wyboru wariantów przez właściciela — trzy bloki × trzy warianty, CSS przejęty z części 8, 10b, 11, 15; 1 plik + wiersz README
- Stawka: niska (narzędzie decyzji, nie produkt)
- Niepewność: średnia (układ dziewięciu pozycji w siatkach zbudowanych na osiem)
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh` (900 s; korekta P17-K 267 s)
- Recenzent (linia / model / native effort): architekt — zrzuty Playwright (Chrome, oba motywy, komputer i telefon, 36 zrzutów w arkuszach)
- Dopuszczone alternatywy: Gemini (wykonawca); recenzja wizualna — worker z Playwright MCP
- Powód wyboru: podgląd wymaga dużego, spójnego CSS — Spark `xhigh` budował poprzednie części
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-82
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: odrzucony — Spark zgłosił brak przeglądarki (nie użył Playwright MCP) i sprawdził tylko strukturę; brak `</div>` zamykającego `.bar` (strona podglądu 38 px szerokości), pas M9-2 800 px z kolumną jednego słowa, OK-2 łuk na tekście, LO-1 łuk bez wypełnienia (niezdefiniowany token `--s500`) i ucięte słowa, przycisk w otwarciu spoza wzoru
- Rundy korekt: 1 (P17-K) + dwie poprawki architekta (`</div>`; jawne `grid-column` dzieci pasa, bo wspólna reguła `.offer-o1 .cat-arrow{grid-column:2}` przepychała tekst do kolumny 28 px — Spark naprawił objawy bez podglądu)
- Czas do akceptacji: ok. 60 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): sześć usterek wizualnych — wszystkie potwierdzone zrzutami; Spark słusznie wskazał błędne odesłanie briefu (kompozycja łuków z części 11, nie 15)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: zrzuty wszystkich wariantów w obu motywach i szerokościach, konsola bez błędów, `files/…` istnieją. Wniosek: brief podglądu musi wskazać sposób oglądu (Playwright MCP albo raport „nie oglądałem” jako blokada), a sprawdzenie skryptem „zbalansowanych tagów” nie wystarcza

### BE-86 (BeautyEffect: Etap 4 K0 — zasoby oferty: zdjęcia, kadry, wycinki filmów) — 2026-10-07
- Archetyp: przygotowanie zasobów multimedialnych wg listy z dokumentów (ffmpeg, kadrowanie, arkusz kontrolny); 32 pliki w `public/`
- Stawka: niska
- Niepewność: średnia (dobór kadrów i długości wycinków)
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` (1166 s)
- Recenzent (linia / model / native effort): architekt — arkusz kontrolny, długości klipów, istnienie 48 ścieżek; RE5 (Codex) potwierdziło ścieżki ponownie
- Dopuszczone alternatywy: Spark `high` (wykonawca)
- Powód wyboru: zadanie narzędziowe na Windows (ffmpeg, pliki binarne), bez niezmiennika; Spark w tym czasie na K1 i K4
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude zablokowany (hook, CZERWONY — tydzień 95–97 %, od 2026-10-07 ok. 22:27); Spark/Gemini/Codex nieznany (brak komunikatów limitu wrappera przez cały etap)
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowany — wszystkie media w kolorze, kadry sensowne, długości wycinków zgodne z briefem
- Rundy korekt: 0
- Czas do akceptacji: ok. 20 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): brak
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: arkusz kontrolny obejrzany przez architekta, skrypt istnienia ścieżek, brak powtórzeń pliku na stronie

### BE-87 (BeautyEffect: Etap 4 K1 — model danych oferty, budowa widoku kategorii, kontrola tekstów) — 2026-10-07
- Archetyp: warstwa danych FE (modele, enumy, funkcja budująca widok, testy kontraktu kluczy i tekstów); ok. 20 plików
- Stawka: średnia (kontrakt, na którym stoją wszystkie strony kategorii)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh` (1177 s); poprawka 1 `high` (109 s), poprawka 2 `high` (401 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (R1, 231 s); poprawki — Gemini `gemini-3.8-flash-high` read (RE3)
- Dopuszczone alternatywy: Codex Sol `high` (wykonawca, ale > 5 plików); Gemini (recenzent)
- Powód wyboru: największy brief fali 1, wiele plików — Spark `xhigh`
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-86
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany warunkowo; kontrola cen odrzucała słowa typu „złuszczanie” — poprawka 1 (Spark słusznie wykazał, że regex architekta odrzucał też „150zł”); R1 wskazało luki kontroli tekstów — poprawka 2
- Rundy korekt: 2
- Czas do akceptacji: ok. 55 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R1 — uwagi do kontroli tekstów potwierdzone i naprawione; RE3 — poprawki bez uwag
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: 43/43 testy warstwy danych, pełna walidacja fali (725 testów)

### BE-88 (BeautyEffect: Etap 4 K2a + K2b — tokeny panelu typograficznego i komponent panelu) — 2026-10-07
- Archetyp: K2a — nowe tokeny koloru (preset, aliasy, pary kontrastu `/design`); K2b — komponent prezentacyjny
- Stawka: średnia (system kolorów, kontrast WCAG)
- Niepewność: niska
- Wykonawca (linia / model / native effort): K2a — Codex / `gpt-6.1-sol` / `medium` (pierwszy przebieg 49 s zatrzymany, ponowny 151 s); K2b — Gemini / `gemini-3.8-flash-high` (581 s)
- Recenzent (linia / model / native effort): K2a — Gemini read (R2, 450 s); K2b — Codex Sol `high` review (R1)
- Dopuszczone alternatywy: Spark `high` (oba)
- Powód wyboru: K2a ≤ 5 plików, wyraźny kontrakt — Codex `medium`; K2b równolegle na wolnej linii Gemini
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-86
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: K2a — Codex słusznie zatrzymał się na błędnej przesłance briefu (wcięcie `pl.json` to 2 spacje); po poprawce briefu zaakceptowany. K2b — zaakceptowany; błąd briefu architekta (`cqi` względem samego panelu zamiast `vw` wg AT-SPEC) poprawił architekt w dwóch liniach
- Rundy korekt: K2a 1 (restart po błędzie briefu), K2b 0 (poprawka architekta)
- Czas do akceptacji: ok. 15 min (K2a), ok. 12 min (K2b)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R2 — P3 brzmienie etykiet `/design/kolory` (odrzucone: etykiety wewnętrzne); sugestia scalenia par gradientu (odrzucona: pomiar per motyw)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: pary kontrastu w specu, 11/11 testów panelu po poprawce

### BE-89 (BeautyEffect: Etap 4 K4 — wspólne teksty oferty w `pl.json`) — 2026-10-07
- Archetyp: i18n — klucze wspólne stron kategorii; 1 plik + spec
- Stawka: niska
- Niepewność: niska
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `high` (368 s)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / read (R2)
- Dopuszczone alternatywy: Gemini (wykonawca); Codex (recenzent)
- Powód wyboru: prosta praca tekstowa — Spark (pamięć: prosta praca na Sparku)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-86
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany; jeden tekst wpisany na sztywno w spec poprawiony jednolinijkowo przez architekta
- Rundy korekt: 0
- Czas do akceptacji: ok. 10 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R2 — brak defektów (pewność 0,99)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: spec kluczy, prettier `pl.json`

### BE-90 (BeautyEffect: Etap 4 K3 — otwarcie strony z łukami, pas zamknięcia, przyciski rezerwacji, podgląd `/design`) — 2026-10-07
- Archetyp: komponenty wspólne FE (3 komponenty + podgląd); ok. 15 plików
- Stawka: niska–średnia
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` (907 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (RE4, 142 s, wspólnie z K8)
- Dopuszczone alternatywy: Spark `xhigh` (wykonawca)
- Powód wyboru: równoległa fala 2 — Spark na K6 i poprawce K1, Codex na K7
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-86
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowany
- Rundy korekt: 0
- Czas do akceptacji: ok. 30 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): RE4 — K3 poprawny
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: specy z AXE, pełna walidacja fali, zrzuty `/oferta` w browser-check

### BE-91 (BeautyEffect: Etap 4 K5 — karta zabiegu KA-1 z rozwinięciem i osią PZ-3) — 2026-10-07
- Archetyp: komponent prezentacyjny FE z rozwinięciem (`inert`, aria), podkomponent szczegółów, funkcje podziału tekstu; ok. 12 plików
- Stawka: średnia (dostępność rozwinięcia, SEO treści w DOM)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` (866 s; poprawka 478 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (RE6, 158 s)
- Dopuszczone alternatywy: Spark `xhigh` (wykonawca); Spark read (recenzent)
- Powód wyboru: jak BE-90
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-86
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: odrzucony przez architekta — znikające spacje wokół wyróżnienia (`preserveWhitespaces:false` usuwa węzły z samych spacji), `track` na treści w listach, podwójne pogrubienie w ciemnym motywie
- Rundy korekt: 1 (K5fix)
- Czas do akceptacji: ok. 45 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): RE6 — brak defektów, sprawdzone klucze 83 zabiegów
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: 24 testy karty z dokładnym tekstem opisu, AXE

### BE-92 (BeautyEffect: Etap 4 K6 — baner grupy i kafle zasad ZW-3) — 2026-10-07
- Archetyp: dwa komponenty prezentacyjne + jedna linia w `VideoClip`; ok. 9 plików
- Stawka: niska
- Niepewność: niska
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh` (383 s); poprawka `high` (269 s)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / read (RE3, 827 s, wspólnie z K7 i poprawkami K1)
- Dopuszczone alternatywy: Gemini (wykonawca); Codex (recenzent)
- Powód wyboru: Spark wolny w fali 2; Gemini recenzuje Sparka i Codexa jednym przebiegiem
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-86
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany (22/22); wykonawca słusznie zawęził unię banera przez `computed()` zamiast `@switch` — przesłanka briefu nie trzymała się kontroli typów
- Rundy korekt: 1 — **zbędna**: RE3 zgłosiło P2 „znak 40 px nigdy nie działa”, architekt potwierdził bez sprawdzenia skompilowanego CSS; Spark w poprawce obalił przesłankę (dart-sass emituje `@media` mixina w miejscu `@include` i dzieli regułę, więc 40 px działało od 576 px). Zapis mobile-first zostawiony jako odporniejszy, z testem kontraktu SCSS
- Czas do akceptacji: ok. 40 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): RE3 P2 rozmiar znaku — fałszywie dodatnie (błędnie potwierdzone przez architekta, obalone przez wykonawcę)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: 9/9 testów kafli z kontraktem skompilowanego SCSS. Wniosek: twierdzenia recenzenta o kaskadzie SCSS sprawdzać na skompilowanym CSS przed potwierdzeniem

### BE-93 (BeautyEffect: Etap 4 K7 — zakładki grup Z-2 na `@angular/aria`) — 2026-10-07
- Archetyp: komponent interaktywny FE (zakładki, przyklejony pasek, wejście z `#kotwicy`, SSR); 4 pliki
- Stawka: średnia (klawiatura, SSR, kotwice)
- Niepewność: średnia (nowe API `@angular/aria`)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (413 s)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / read (RE3)
- Dopuszczone alternatywy: Spark `xhigh` (wykonawca); Spark read (recenzent)
- Powód wyboru: ≤ 5 plików, trudniejsze API — Codex Sol `high`; architekt sprawdził API w zainstalowanym pakiecie przed briefem
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-86
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany (25/25); fragment adresu czytany tylko w przeglądarce, przewinięcie po renderze
- Rundy korekt: 0
- Czas do akceptacji: ok. 35 min (z oczekiwaniem na RE3)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): RE3 — brak
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: specy klawiatury i fragmentu; browser-check kotwicy `/oferta/warkocze#afro-i-loki`

### BE-94 (BeautyEffect: Etap 4 K8 — łuki kategorii OK-1 na stronie „Oferta”) — 2026-10-07
- Archetyp: lista prezentacyjna FE z przesunięciem kolumny; 8 plików
- Stawka: niska
- Niepewność: niska
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` (804 s; poprawka 218 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (RE4)
- Dopuszczone alternatywy: Spark (wykonawca)
- Powód wyboru: zwolniony slot Gemini po R2
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-86
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowany warunkowo; specy chwilowo czerwone w trakcie przebiegu (architekt powtórzył: 18/18)
- Rundy korekt: 1 (szerokość łuku 576–991 px ograniczona do 360 px, test kontraktu)
- Czas do akceptacji: ok. 35 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): RE4 P2 rozciągnięte łuki na tablecie — potwierdzone, naprawione
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: 19/19, zrzuty `/oferta` 4 szerokości × 2 motywy

### BE-95 (BeautyEffect: Etap 4 K9–K17 — dane dziewięciu stron kategorii) — 2026-10-07
- Archetyp: przeniesienie zatwierdzonych dokumentów do danych `.ts` i fragmentów `pl.json` dosłownie; 9 briefów po 2 pliki + fragment
- Stawka: średnia (wierność treści właścicielki, brak cen)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `high` — wszystkie 9 (117–244 s, mediana ok. 180 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (RE5, 139 s, cały zbiór); architekt — skrypt fragmentów i skrypt wierności (każdy tekst dosłownie w źródle)
- Dopuszczone alternatywy: Gemini (wykonawca — pierwotny plan dla K10/K12); Gemini read (recenzent)
- Powód wyboru: krótkie, mechaniczne briefy ze wspólnego szablonu; K10 i K12 przeniesione z Gemini na Sparka (Gemini zajęty trzema komponentami, Spark przepisał dosłownie 4 strony)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-86
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: 8/9 zaakceptowane od razu (np. K9 57/57, K15 78/78, K17 61/61 tekstów dosłownie); K12 wyciął całe zdania z dopiskiem „(wyjaśnienie dopisał architekt)” zamiast samego dopisku — architekt przywrócił zdania we fragmencie przed scaleniem
- Rundy korekt: 0 (jedna poprawka architekta we fragmencie K12)
- Czas do akceptacji: ok. 40 min całości; scalenie 447 kluczy bez zmian istniejących
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): RE5 — brak (log potwierdził, że Codex otworzył dokumenty i dane); uwagi wykonawców: K12 — notka redakcyjna dokumentu sprzeczna z blokiem (`chcą/chcesz`), do zgłoszenia właścicielce; K16 — „plan nie ma sekcji K9–K17” — fałszywe (sekcja istnieje)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: spec pokrycia kluczy, skrypt wierności, istnienie 48 mediów

### BE-96 (BeautyEffect: Etap 4 K19 — mozaika M9-1 z dziewiątym kaflem „Zabiegi laserowe”) — 2026-10-07
- Archetyp: zmiana istniejącego komponentu strony głównej (kafel z panelem typograficznym zamiast zdjęcia); ok. 10 plików
- Stawka: niska
- Niepewność: niska
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh` (347 s)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / read (RE7, 516 s, wspólnie z K20)
- Dopuszczone alternatywy: Codex Sol `high` (pierwotny plan — przeniesiony na Sparka: > 5 plików i pula Codexa na recenzje, pamięć „prosta praca na Sparku”)
- Powód wyboru: jak w alternatywach
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-86
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany
- Rundy korekt: 0
- Czas do akceptacji: ok. 25 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): RE7 — P3: komórka lasera bez gałęzi zdjęcia (do zmiany, gdy przyjdą zdjęcia) — przyjęte jako dalsza praca
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: specy strony głównej, zrzuty strony głównej 4 × 2

### BE-97 (BeautyEffect: Etap 4 K20 — strona „Oferta” i trasa `oferta`) — 2026-10-07
- Archetyp: strona FE składająca gotowe komponenty + trasa, prerender, SEO; ok. 7 plików
- Stawka: niska–średnia
- Niepewność: niska
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh` (419 s)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / read (RE7)
- Dopuszczone alternatywy: Codex Sol `high` (> 5 plików); Codex review (recenzent)
- Powód wyboru: pliki tras po kolei (K20 → K21), wolna linia Sparka
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-86
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany; wykonawca słusznie użył tokenu rytmu podstron zamiast sugerowanych w briefie tokenów pasów strony głównej
- Rundy korekt: 0
- Czas do akceptacji: ok. 20 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): RE7 — poprawny, P3 bez wpływu
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: spec strony z AXE, spec tras, build (prerender `/oferta`), zrzuty 4 × 2

### BE-98 (BeautyEffect: Etap 4 K18 — panel grupy zabiegów) — 2026-10-07
- Archetyp: komponent składający (karty, baner, kafle) ze stanem rozwinięcia; 4 pliki
- Stawka: średnia
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` (795 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (RE8, 155 s)
- Dopuszczone alternatywy: Spark `xhigh` (wykonawca, zajęty K20/K6fix); Spark read (recenzent)
- Powód wyboru: wolna linia Gemini, ≤ 5 plików
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-86
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowany; błąd przesłanki briefu architekta (`GroupView.index` od 0 — w rzeczywistości od 1) — wykonawca zabezpieczył się warunkiem zamiast zatrzymać; architekt zamienił warunek na `group.index` (jedna linia)
- Rundy korekt: 0 (poprawka architekta, jednolinijkowa)
- Czas do akceptacji: ok. 17 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): RE8 — brak defektów; przypadek „zmiana wejścia group” odrzucony (każda grupa ma własną instancję)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: 7/7 specy panelu, pełna walidacja (905 testów, build)

### BE-99 (BeautyEffect: Etap 4 K21 — strona kategorii `/oferta/<slug>`, 9 tras, prerender, SEO) — 2026-10-07
- Archetyp: strona FE składająca komponenty + zakładki (`ngTabs`/`ngTabPanel`) + trasy i SEO; 7 plików
- Stawka: średnia (9 stron, SEO, prerender)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `xhigh` (463 s)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / read (RE9)
- Dopuszczone alternatywy: Codex Sol `high` (pierwotny plan — przeniesiony na Sparka: 7 plików > 5)
- Powód wyboru: jak w alternatywach
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-86
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany; jedyne odchylenie — jawny typ `ServerRoute` w `.map()` (bez niego TypeScript poszerzał `renderMode`)
- Rundy korekt: 0
- Czas do akceptacji: ok. 25 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): RE9 — poprawny (0,98); P3 „brak testu zmiany `slug` na żywej instancji” odrzucone (9 osobnych tras — router tworzy nową instancję); RE9 słusznie wskazało, że brief pominął test planu „render z `PLATFORM_ID` server” — zastąpiony dowodem z artefaktu: HTML prerenderu 9 stron zawiera nazwy wszystkich zabiegów
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: 48 testów (strona × 9 z AXE, trasy), build — 15 tras prerenderowanych, panele nieaktywne z `inert` w HTML prerenderu, browser-check stron kategorii

### BE-100 (BeautyEffect: Etap 5 — audyt i poprawki dokumentów O nas, Jak się umówić, Kontakt, mapy) — 2026-10-08
- Archetyp: audyt gotowości dokumentów (tylko odczyt) + dwie rundy poprawek spójności i decyzji właścicielki + recenzja dokumentów
- Stawka: średnia (dokumenty wiążące dla wdrożenia trzech stron)
- Niepewność: średnia (otwarte kwestie: formularz, sobota, gotówka, współrzędne)
- Wykonawca (linia / model / native effort): A5 — Spark / `muse-spark-1.3-contributor` / `xhigh`, `-Access read` (249 s); W5 i W5b — Spark / `muse-spark-1.3-contributor` / `high` (226 s, 320 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (RD5, 307 s)
- Dopuszczone alternatywy: Gemini `gemini-3.8-flash-high` (audyt, poprawki); Codex Sol (audyt)
- Powód wyboru: Spark dla tekstowej, prostej pracy (preferencja właściciela — pula Codexa na recenzje); recenzja z innej rodziny niż autor
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude zablokowany (hook, CZERWONY — tydzień 99–100 %, cały etap 2026-10-08); Spark i Codex nieznany (brak komunikatów limitu); Gemini nieznany do E9 (patrz BE-102)
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: A5 — rzetelny podział na poprawki A i decyzje B dla czterech dokumentów; W5 — poprawki wykonane, trzy trafne uwagi do briefu (adresat „Układu”, usuwanie zdania wiodącego, brzmienie „wyłącznie”); W5b — cztery decyzje właścicielki wpisane dosłownie
- Rundy korekt: 0 (poprawka RD5 P2 wpisana przed zatwierdzeniem dokumentów)
- Czas do akceptacji: ok. 1 h 30 min (z odpowiedziami właścicielki)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): RD5 — P2 akapit laserowy sprzeczny z „Układem” (potwierdzony, poprawiony); P2 zależność polityki prywatności od formularza (potwierdzony, przeniesiony do etapu 6 — polityka); P3 kotwice po renumeracji sekcji (bez zmian)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: 398 lokalnych odnośników Markdown bez martwych (RD5), statusy dokumentów zmieniane tylko za zgodą właścicielki

### BE-101 (BeautyEffect: Etap 5 fala 1 — lista godzin, rozszerzenia PageOpening/ClosingBand, kafle udogodnień, teksty) — 2026-10-08
- Archetyp: wspólne komponenty FE i teksty `pl.json` pod trzy strony; 4 briefy o rozłącznych plikach
- Stawka: średnia (komponenty współdzielone przez stronę główną i trzy podstrony)
- Niepewność: niska
- Wykonawca (linia / model / native effort): E1 lista godzin — Spark / `muse-spark-1.3-contributor` / `xhigh` (334 s); E2 PageOpening/ClosingBand + stałe salonu — Spark / `high` (244 s); E3 AmenityTiles — Gemini / `gemini-3.8-flash-high` (932 s); E4 `pl.json` (135 kluczy) — Spark / `xhigh` (209 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (RW1, 261 s, cała fala)
- Dopuszczone alternatywy: Gemini dla E1/E2/E4; Spark dla E3; Codex Sol `high` (≤ 5 plików)
- Powód wyboru: rozłożenie fali na dwie linie zewnętrzne; Claude zablokowany
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-100
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowane po walidacji; E1 24 testy, E2 44, E4 14; E3 wolny (932 s)
- Rundy korekt: 1 (F1 — Spark `high`, 163 s: test miejsc `ClosingBand` z komponentem-gospodarzem; mutacja selektora czerwona → przywrócenie zielone)
- Czas do akceptacji: ok. 50 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): RW1 — P2 test miejsc `ClosingBand` przechodził niezależnie od selektorów (`projectableNodes` po indeksie) — potwierdzony; P3 spacje w tekstach wokół odnośnika — odrzucony (spacje stawia szablon, plan poprawiony)
- Defekty po odbiorze: E3 — tytuł kafla 24/26 px zamiast 22 px z makiety; słowo „niepełnosprawnościami” (220 px) nie mieści się w kaflu: przy 320 px strona przewija się w poziomie (`scrollWidth` 333), przy 360 i 992–1440 px tekst wystaje poza kafel. Wykryte sondą przeglądarki architekta, nie przez testy ani recenzję; poprawione w F7 (Spark `high`; 22 px, `overflow-wrap: break-word`; Chrome na Windows nie dzieli polskich wyrazów przy `hyphens: auto`) — po przebudowie sonda: `scrollWidth` równy szerokości okna i 0/4 tytułów poza kaflem od 320 do 1440 px
- Wymagane testy i dowody: specy z AXE, pokrycie kluczy `pl.json`, sonda `scrollWidth` 320–1440 px

### BE-102 (BeautyEffect: Etap 5 fala 2 — sekcje Gemini: WY-2 + KB-1, KR-1 + KG-3, KP-1 + KZ-2) — 2026-10-08
- Archetyp: sekcje stron z makiety HTML (układ na siatce Bootstrapa, grafika CSS, zdjęcia); 3 briefy po 4–8 plików
- Stawka: średnia
- Niepewność: średnia (odczyt makiety, szerokości pośrednie bez wzorca)
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` — E5 (761 s), E7 (1060 s), E9 (**failed**, 1804 s: limit tokenów wyjścia, potem 30-minutowy limit tury `agy`; artefakty kompletne i zielone, odebrane ręcznie)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (RW2, 306 s, cała fala 2 razem z BE-103)
- Dopuszczone alternatywy: Spark `xhigh` (E12 i E14 przekwalifikowane z Gemini na Sparka w trakcie — obciążenie, potem porażka E9)
- Powód wyboru: druga linia zewnętrzna dla równoległości fali
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini — rzeczywiste niepowodzenie E9 (2026-10-08 ok. 08:48), potem ponowna kwalifikacja; reszta jak BE-100
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: E5 — `font-family` w SCSS zamiast mixinów, test kolejności nie sprawdzał kolejności; E7 — kolumny przez własny `display: grid` od `lg` (łamie regułę siatki Bootstrapa), poziomy logotyp zamiast znaku salonu; E9 — `calc(auto + 12px)` (nieprawidłowa deklaracja), uniesienie bez `(hover: hover)`, czas bez tokenu, getter zamiast `computed`; we wszystkich trzech cienie z `--bty-text` zamiast roli `--bty-shade` (poprawił architekt)
- Rundy korekt: 2 — F2 (Gemini `high`, 456 s: siatka Bootstrapa z dwiema kopiami `BookingActions`, znak salonu) i F3 (Spark `high`, 205 s — E9 przekwalifikowane po porażce Gemini, razem z E5); po oglądzie w przeglądarce F7 (Spark `high`): przyciski kroków wyrównane do lewej (`alignStart`), recenzja F7 — Codex `gpt-6.1-sol` `high` `-Mode review` (RW4, 117 s): brak znalezisk
- Czas do akceptacji: ok. 2 h 30 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): RW2 dla tych sekcji — P3 `font-family` (potwierdzony), P3 kolejność akapitów komfortu (potwierdzony); defekty E7/E9 znane architektowi przed recenzją
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu poza F7 (potwierdzone sondą przeglądarki po przebudowie)
- Wymagane testy i dowody: specy z AXE, próba mutacyjna testu kolejności (czerwony → zielony), zrzuty 320/390/600/768/992/1440 px w obu motywach

### BE-103 (BeautyEffect: Etap 5 fala 2 — sekcje Sparka: ZE-2, KN-1 + zasady, wskazówki, SK-1, GA-3 + MA-1) — 2026-10-08
- Archetyp: jak BE-102; 5 briefów, w tym statyczny plan okolicy (SVG 97 KB skopiowany bajt w bajt jako szablon)
- Stawka: średnia (GA-3: zero żądań do dostawców map, licencja OSM)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` — E6 `xhigh` (354 s), E8 `xhigh` (584 s), E10 `high` (221 s), E11 `xhigh` (304 s), E12 `xhigh` (372 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (RW2)
- Dopuszczone alternatywy: Gemini `high`; Codex Sol `high` (≤ 5 plików)
- Powód wyboru: Spark dla większości fali; E12 przekwalifikowany z Gemini
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-100
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: E6, E10, E11 bez uwag recenzji; E8 — tytuły kafli i etykieta zasady bez `h3`; E12 — licencja OSM pozycjonowana względem całego pasa (na telefonie w rogu karty), karta zasłania pinezkę przy 576–991 px (luka szerokości pośredniej w AT-SPEC — rozstrzygnięcie architekta, wiersz do potwierdzenia przez właścicielkę)
- Rundy korekt: 1 — F4 (Spark `high`, 158 s, `h3`), F5 (Spark `xhigh`, 138 s, pojemnik planu, karta na planie od `lg`); po oglądzie w przeglądarce F7: licencja 52 px nad dolną krawędzią poniżej `lg` (karta przykrywała pole kliknięcia), łamanie adresu e-mail po `@` (`<wbr>`) w SK-1 przy 992–1199 px
- Czas do akceptacji: ok. 2 h
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): RW2 — 3 × P2 (licencja w złym miejscu, pinezka zasłonięta, brak `h3`) potwierdzone
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu poza F7 (RW4 bez znalezisk; sonda: e-mail łamie się tylko po `@`, licencja 12 px nad kartą i klikalna, pole 44 px). Otwarte pytanie do właścicielki: przy oknie szerszym niż 1280 px rysunek planu (1280 × 1280, stała skala z `zasoby/mapa`) kończy się przed krawędzią pasa na całą szerokość — luka dokumentów, nie wada wykonania
- Wymagane testy i dowody: liczby elementów SVG równe plikowi źródłowemu (17 `path`, 7 `text`, 12 `g`), brak `iframe`/`script`/`img` w mapie, odnośnik licencji poza `role="img"`, zrzuty 320–1440 px

### BE-104 (BeautyEffect: Etap 5 fale 3–4 — strony /o-nas, /umow-wizyte, /kontakt, trasy i prerender) — 2026-10-08
- Archetyp: złożenie stron z gotowych sekcji + SEO + spec strony z AXE; trasy `loadComponent` i `RenderMode.Prerender`
- Stawka: średnia (3 strony publiczne, SEO)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` — E13 `xhigh` (325 s), E14 `xhigh` (263 s), E15 `xhigh` (241 s), E16 `high` (111 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (RW3, 247 s — fale 3–4 i poprawki F2–F6 razem)
- Dopuszczone alternatywy: Gemini `high` (strony); Codex Sol `high` (E16, 2 pliki)
- Powód wyboru: Spark — krótkie briefy złożenia; E14 przekwalifikowany z Gemini
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-100
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: wszystkie 4 zielone za pierwszym razem (E13 7 testów, E14 7, E15 8, E16 35); E16 słusznie zastosował import względny jak istniejąca trasa `oferta` zamiast aliasu z briefu
- Rundy korekt: 1 — F6 (Spark `high`, 109 s): wstęp „O nas” z `g-5` wystawał 4 px poza okno telefonu (marginesy wiersza −24 px przy 20 px dopełnienia kontenera), a `margin: 0` akapitów zerował odstęp pionowy; wykryte przez architekta przy czytaniu szablonu, nie przez recenzję. Architekt: szerokość akapitu zamknięcia 900 → 760 px (spójnie z pasem zamknięcia)
- Czas do akceptacji: ok. 1 h 30 min z oglądem w przeglądarce
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): RW3 — brak znalezisk (wada F6 i defekty wyglądu F7 umknęły recenzji z samego kodu)
- Defekty po odbiorze: etykiety przycisków `Napisz na Instagramie` / `Napisz na Facebooku` w kartach kontaktu (SK-1) łamią się przy 992–1440 px i stały przy lewej krawędzi przycisku — wykryte na zrzutach 1440 px, poprawione jednym wierszem przez architekta (`text-align: center` na własnej klasie `.contact-card__action`), sprawdzone sondą
- Wymagane testy i dowody: 105 plików / 1086 testów, build — 18 tras prerenderowanych, HTML prerenderu: jedno `h1`, `h2` w kolejności z dokumentów, kanoniczne adresy, brak zduplikowanych `id`; browser-check: pełny przebieg 29/32 zrzutów (limit czasu scenariusza 20 min — trzy brakujące komputer/ciemny dorobione po przebudowie) + 6 zrzutów szerokości pośrednich + 8 zrzutów 1440 px po F7, sondy `scrollWidth`, licencji mapy, łamania e-maila i wyrównania przycisków

### BE-105 (BeautyEffect: Etap 6 — audyt dokumentów, decyzje właścicielki, SEO, przekierowania) — 2026-10-11
- Archetyp: dokumentacja produktu — audyt spójności (tylko odczyt) i redakcja wymagań (SEO, mapa stron, dane salonu, kwestie otwarte) z wpisaniem decyzji właścicielki
- Stawka: średnia (wymagania wiążące dla fal FE etapu 6; statusy zatwierdzenia tylko za zgodą właścicielki)
- Niepewność: średnia (kilka decyzji właścicielki zapadło w trakcie)
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` — A6 `xhigh` `-Access read` (327 s, audyt), W6 `high` (305 s), W6b `high` (336 s), W6d `high` (248 s, poprawki po recenzji — także polityka, BE-106)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (RD6, 467 s — W6, W6b, W6c, W6m razem)
- Dopuszczone alternatywy: Gemini `high` (redakcja dokumentów); Codex Sol `high` (wykonanie — odrzucone, pula Codexa zostaje na recenzje)
- Powód wyboru: Spark — tekst w repo dokumentacji bez kodu, krótkie briefy; audyt na `xhigh`, bo wyniki decydowały o pytaniach do właścicielki
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark i Codex `nieznany` (wrapper bez odczytu zapasu), bez komunikatów limitu, 2026-10-11
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: A6 — rzetelny audyt (m.in. sprzeczność „w tym plików cookies” z wariantem bez analityki, brak `hreflang`), podstawa pytań do właścicielki; W6 i W6b zgodne z briefami; RD6 znalazła w WP-WIDOCZNOSC `Disallow: /design/` (nie blokował samego `/design` po regule kanonicznej)
- Rundy korekt: 1 — W6d (razem z poprawkami polityki); architekt dopisał jednym wierszem atrybucję decyzji właścicielki w decyzji o mapie (luka zgłoszona przez W6d)
- Czas do akceptacji: ok. 1 h pracy workerów (bez czasu na odpowiedzi właścicielki); dokumenty etapu 6 czekają na zatwierdzenie
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): RD6 — 5 × P2 potwierdzonych (1 tutaj, 4 w BE-106), 0 odrzuconych; RD6 sprawdziła też 567 linków względnych (0 martwych)
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: grep sprawdzeń z briefu W6d, martwe linki 0, statusy bez zmian poza zgodą właścicielki; CEIDG odpowiadał 403 automatom — administrator ustalony z białej listy MF (bez zapisywania numerów rachunków)

### BE-106 (BeautyEffect: Etap 6 — projekt treści polityki prywatności) — 2026-10-11
- Archetyp: tekst prawny dla odwiedzającej (prosty język, forma „Ty”) ze znacznikami danych i sekcją luk dla prawnika
- Stawka: średnia–wysoka (dokument prawny RODO; publikacja dopiero po zatwierdzeniu i zalecanym przeglądzie prawnika)
- Niepewność: średnia (role Booksy, retencja, IOD — luki dla właścicielki i prawnika)
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` — W6c `xhigh` (117 s), poprawki w W6d `high`
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (RD6, wspólna z BE-105)
- Dopuszczone alternatywy: Gemini `high`; Codex Sol `high` (wykonanie — odrzucone, pula na recenzje)
- Powód wyboru: Spark `xhigh` — tekst z wieloma zależnościami między dokumentami, ale bez niezmiennika kodu
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-105
- Pewność decyzji: średnia (krótki przebieg `xhigh` przy tekście prawnym — wymagał rundy poprawek)
- Wynik pierwszego podejścia: wymagane korekty — notatki dla redakcji i zdania „potwierdzi prawnik” w tekście dla odwiedzającej, błędy gramatyczne („Twoje dane używamy”), mylący nagłówek sekcji 3 o usługach osadzonych (strona nic nie osadza) — wykryte przez architekta; RD6 dołożyła 4 merytoryczne
- Rundy korekt: 1 — W6d: znaczniki `[administrator]` itd. objaśnione w „Zastrzeżeniu”, rezerwacje laserowe telefonicznie i retencja danych rezerwacji, bez adresu pocztowego UODO, IOD przeniesiony do luk
- Czas do akceptacji: ok. 25 min do zgodności z recenzją; zatwierdzenie treści czeka na właścicielkę
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): RD6 — 4 × P2 potwierdzone (rezerwacje telefoniczne, nieaktualny adres UODO, nazwisko administratora wpisane na stałe, brak inspektora podany jako fakt), 0 odrzuconych
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: grep — w sekcji „Treść” zero zdań do redakcji i prawnika, nazwiska administratora ani zdań o inspektorze; nazwy dziewięciu sekcji identyczne w PRAWO i UI-POLITYKA; martwe linki 0. Uwaga architekta: literówka w briefie W6c („możesz, że”) poprawiona przed wysłaniem

### BE-107 (BeautyEffect: Etap 6 — szerszy plan okolicy 2560 × 1280 z OSM, osobny plik przez `<use>`) — 2026-10-11
- Archetyp: generator SVG w repo dokumentacji (Python, dane Overpass) + komponent FE (szablon, SCSS ze zmiennymi z tokenów, spec z odczytem pliku)
- Stawka: średnia (publiczna strona Kontakt, zero żądań do dostawców map, licencja OSM, oba motywy)
- Niepewność: średnia (zewnętrzny `<use>` i dziedziczenie zmiennych CSS do klonu; Safari/Firefox niesprawdzone)
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` — W6m `high` (237 s, generator i plik), E8 `xhigh` (305 s, FE), F8 `high` (60 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` — RD6 (generator, granice, struktura SVG) i RE8 (138 s, FE)
- Dopuszczone alternatywy: Gemini `high` (generator); Codex Sol `high` (E8 — 5 plików, odrzucone ze względu na pulę)
- Powód wyboru: Spark — jasno opisana zmiana o rozłącznych plikach; E8 na `xhigh` przez nowy mechanizm `<use>`
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-105
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: W6m — plik 227 258 B (tolerancja 1,5 m), zgodny ze specyfikacją; E8 — zielone testy i lint; błąd architekta w briefie E8 (precedens z nieistniejącym specem `design-system-mirror`) poprawiony na `theme-boot-script.spec.ts`
- Rundy korekt: 1 — F8 (stała i funkcja pomocnicza specu na poziomie modułu → do `describe`, reguła „one declaration per file”)
- Czas do akceptacji: ok. 45 min z oglądem w przeglądarce
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): RE8 — 1 × P3 potwierdzone, 0 odrzuconych; RD6 bez znalezisk dla planu
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu; ryzyko otwarte — zewnętrzny `<use>` w Firefox/WebKit niesprawdzony (zgodna wersja przeglądarek Playwright wymaga pobrania)
- Wymagane testy i dowody: 105 plików / 1088 testów, lint, format, build — 18 tras; sonda Chrome 390/1440/1920/2560 px w obu motywach: plik `200 image/svg+xml`, klon renderuje się do krawędzi przy 2560 px, brak przewijania w poziomie i błędów konsoli; SHA-256 kopii w FE równy plikowi źródłowemu; CI na `main`

### BE-108 (BeautyEffect: Etap 6 fala 1 — Seo/Open Graph, sitemap + robots, strona 404 NZ-1) — 2026-10-11
- Archetyp: rozszerzenie usługi SEO ze specem + skrypt `postbuild` + strona błędu (szablon, SCSS, AXE)
- Stawka: średnia (indeksowanie całej witryny, `noindex` na 404)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` — E1 `xhigh` (380 s), E3 `high` (120 s), E7 `xhigh` (280 s), F1b `high` (93 s, poprawka)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (RF1, 239 s — cała fala 1 razem z przekierowaniami BE-109)
- Dopuszczone alternatywy: Gemini `high` (E3, E7); Codex Sol `high` (odrzucone — pula na recenzje)
- Powód wyboru: Spark — rozłączne, krótkie briefy; `xhigh` przy zmianie wspólnej usługi (E1) i stronie z wyglądem z makiety (E7)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark i Codex `nieznany` (wrapper bez odczytu zapasu), bez komunikatów limitu; Claude ZIELONY (hook), 2026-10-11
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: wszystkie zielone na własnych plikach; walidacja fali — 2 czerwone testy w `app.routes.spec.ts` (zastępcze `Seo` bez nowej metody `applyNotFound` — plik poza listą E1), poprawione przez architekta jednym poleceniem; błąd briefu E3 (`prettier --check` na `.txt`) — odchylenie wykonawcy przyjęte
- Rundy korekt: 1 — F1b (własna `font-family` w komponencie 404 → miksin `error-number` w `typography.scss`)
- Czas do akceptacji: ok. 1 h z sondami HTTP i zrzutami 404 (390/1440, oba motywy)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): RF1 dla tej części — 1 × P3 potwierdzone (font-family), 0 odrzuconych
- Defekty po odbiorze: brak stwierdzonych do chwili wpisu
- Wymagane testy i dowody: sitemap 14 → 15 adresów, `robots.txt` z `Disallow: /design`, komplet OG/Twitter na `/kontakt`, 404 z tytułem, opisem i `noindex, nofollow`, bez kanonicznego; brak przewijania w poziomie

### BE-109 (BeautyEffect: Etap 6 — przekierowania 301 ze starej strony i hostów, niezmiennik open redirect) — 2026-10-11
- Archetyp: logika serwera SSR (Express) z niezmiennikiem bezpieczeństwa — normalizacja ścieżki, tabela 33 przekierowań, zmiana hosta
- Stawka: wysoka (open redirect i pętle przekierowań — błąd cichy; ten sam kod obsłuży stary ruch i SEO)
- Niepewność: średnia (różnice między dekodowaniem Expressa, parserem WHATWG i routerem Angulara)
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` (Opus 5.5 `xhigh`) — E5 (pierwszy przebieg, czas niezapisany), F1a (1249 s, poprawki RF1), F1c (167 s, poprawka RF3) — ten sam agent wznawiany przez SendMessage
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` — RF1 (wspólna z BE-108) i RF3 (259 s, wspólna z BE-111); dodatkowo automatyczny przegląd bezpieczeństwa sesji
- Dopuszczone alternatywy: brak — niezmiennik bezpieczeństwa (reguła wysokiej stawki: tylko `wykonawca-opus`; Spark `xhigh` wyłącznie przy CZERWONYM)
- Powód wyboru: open redirect = błąd bezpieczeństwa z cichym skutkiem
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ZIELONY (hook, 20–23 % okna 5 h), Codex `nieznany`, 2026-10-11
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: niezmiennik „nigdy obcy host” dotrzymany od początku (`//evil.com` → `/evil.com`), ale RF1 wykazała dwa skoki przy segmentach `..`/wewnętrznym `\` i brak dekodowania `%63ennik`; pośrednia wersja F1a złapana przez automatyczny przegląd (`join('/')` mógł dać wiodące `//`) — wersja końcowa zwija ukośniki po usunięciu kropek
- Rundy korekt: 2 — F1a (normalizacja WHATWG, dekodowanie wyłącznie znaków niezastrzeżonych „do skutku” stosem, liniowo; wykonawca słusznie obalił przesłankę briefu: jedno przejście składa `%2e` z `%%32%65` i daje drugi skok) i F1c (kropka końcowa hosta, bez wyrażenia regularnego — ochrona przed cofaniem kwadratowym)
- Czas do akceptacji: ok. 2 h 40 min (dwie rundy, testy mutacyjne)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): RF1 — 2 × P2 potwierdzone; RF3 — 1 × P2 potwierdzone (kropka końcowa hosta); 0 odrzuconych
- Defekty po odbiorze: brak stwierdzonych; incydenty procesu: (1) wykonawca wypisał wygenerowany klucz licencji deweloperskiej do własnego transkryptu (nie do plików ani usług) — w briefach dopisać zakaz wypisywania zawartości `.env.local` i plików generowanych z sekretów; (2) celowo zepsuta kopia kodu w teście mutacyjnym zostawiła zawieszony proces Vitest — architekt go zatrzymał; w kolejnych briefach: przebiegi mutacyjne z limitem czasu i zakaz zostawiania procesów
- Wymagane testy i dowody: spec 166 testów (w tym „jeden skok” przez `new URL(location)`, niezmiennik na wektorach ataku, wydajność 50 000 kropek < 50 ms), czerwone przed poprawką (25/153 przed F1a, 20/166 przed F1c); sondy `curl`/Node na zbudowanym serwerze: `/..//evil.com`, `/a/../../evil.com`, `/x/%%32%65%%32%65/cennik/`, `/\evil.com`, `/x\..\cennik`, `%2F%2F`, hosty `www`/stara domena z kropką i portem — każdy jeden skok na własny host

### BE-110 (BeautyEffect: Etap 6 fala 2 — JSON-LD BeautySalon, treść polityki w pl.json, spis treści PT-1) — 2026-10-11
- Archetyp: dane strukturalne ze stałych + przeniesienie zatwierdzonego tekstu prawnego słowo w słowo do i18n z modelem bloków + komponent prezentacyjny spisu
- Stawka: średnia–wysoka (tekst prawny musi być wierny dokumentowi; JSON-LD wpływa na wyniki wyszukiwania)
- Niepewność: średnia (składanie zdań z części z odnośnikami, spacje na stykach)
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` — E2 `xhigh` (221 s), E6a `xhigh` (639 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (RF2, 164 s)
- Dopuszczone alternatywy: Gemini `high` (E2); Codex Sol `high` (odrzucone — pula na recenzje)
- Powód wyboru: Spark `xhigh` — wierność tekstu i model danych bez niezmiennika
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-108
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: treść polityki (68 kluczy) wierna dokumentowi — RF2 złożyła i porównała wszystkie sekcje bez rozbieżności; JSON-LD zgodny z WP-WIDOCZNOSC; spis bez JS działa jako lista kotwic z pełną ścieżką (z `<base href="/">`)
- Rundy korekt: 0 osobnych — jedyne znalezisko dołączone do briefu E6b (BE-111)
- Czas do akceptacji: ok. 45 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): RF2 — 1 × P2 potwierdzone (`position: sticky` na wewnętrznym `nav`, którego rodzic nie zostawia miejsca na przesunięcie — spis się nie przyklejał), 0 odrzuconych
- Defekty po odbiorze: brak stwierdzonych; uwaga architekta dla właścicielki: zdanie o przedawnieniu w zatwierdzonym tekście jest nieprecyzyjne prawnie — tekst bez zmian
- Wymagane testy i dowody: spec sekcji (każdy klucz istnieje i nie jest pusty, brak `[`, liczba części z odnośnikami), spec spisu z AXE, testy JSON-LD; prerender — JSON-LD tylko na `/` i `/kontakt`

### BE-111 (BeautyEffect: Etap 6 fala 3 — strona /polityka-prywatnosci, trasa, prerender, aktywna sekcja) — 2026-10-11
- Archetyp: złożenie strony z gotowych danych i komponentów + interakcja przeglądarkowa (IntersectionObserver, przewinięcie i fokus, `Location.replaceState`)
- Stawka: średnia (publiczna strona wymagana prawem; dostępność nawigacji)
- Niepewność: średnia (kolejność renderu przy zwijaniu spisu, semantyka `rootMargin`)
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` — E6b `xhigh` (1221 s), K6b `xhigh` (625 s, poprawki)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (RF3, 259 s — wspólna z BE-109)
- Dopuszczone alternatywy: Gemini `high`; `wykonawca` Sonnet 5.5 `high` (odrzucony — brief tekstowy bez Figmy)
- Powód wyboru: Spark `xhigh` — logika przeglądarkowa bez niezmiennika wysokiej stawki
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-108
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zielone 54/54, poprawne odchylenia z uzasadnieniem (`prettier-ignore` dla sklejania części bez białych znaków, wymóg nazwy dostępnej bez wielkości liter); sondy architekta w Chrome wykazały skok ze spisu na telefonie o 293 px za nagłówek (przewinięcie liczone przed zwinięciem listy) — test jednostkowy tego nie widział
- Rundy korekt: 1 — K6b (przewinięcie w `afterNextRender`, stan przecięć w zbiorze zamiast z niepełnych `entries`, `rootMargin` w pikselach z odtwarzaniem po zmianie rozmiaru okna); test skoku czerwony przed poprawką
- Czas do akceptacji: ok. 1 h 15 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): RF3 dla tej części — 2 × P2 potwierdzone (aktywna sekcja z niepełnego stanu; procent `rootMargin` liczony wg specyfikacji W3C od szerokości — Chrome liczy od wysokości, więc sonda w Chrome go nie wykryła); 0 odrzuconych; skok na telefonie podany recenzentowi jako znany
- Defekty po odbiorze: brak stwierdzonych; P3 zaakceptowane bez poprawki — bez JS przycisk spisu na telefonie jest widoczny, ale nieaktywny (lista i tak rozwinięta)
- Wymagane testy i dowody: 112 plików / 1309 testów, lint, format, build — 19 tras, sitemap 15 adresów; prerender: jedno `h1`, dziewięć `h2` z `id`, kanoniczny, bez JSON-LD; sondy Chrome 390/1440 w obu motywach (nagłówek po skoku 88 px od góry, spis przyklejony `top` 96 px, fokus i `#id` w adresie, brak błędów konsoli i przewijania w poziomie), śledzenie aktywnej sekcji 1920 × 1080 / 1440 × 900 / 1024 × 700 i po zmianie rozmiaru, spis bez JS — 9 widocznych kotwic

### BE-112 (BeautyEffect: łuk pasa oferty nachodzi na koniec otwarcia strony głównej) — 2026-10-11
- Archetyp: poprawka wizualna w SCSS (separator sekcji, kolejność warstw) + kontrakt skompilowanego CSS w specach
- Stawka: niska (wygląd strony głównej, bez niezmiennika)
- Niepewność: niska po ustaleniu przyczyny; przyczynę (przezroczyste narożniki łuku pokazujące tło strony) wskazał użytkownik po długiej, chybionej analizie architekta (pomiary profilu rozmycia plam)
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `high` — L1 (125 s), K1 (63 s, korekta)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `medium`, `-Mode review` (46 s)
- Dopuszczone alternatywy: Codex Sol `medium` jako wykonawca; Gemini `high` jako recenzent
- Powód wyboru: prosta zmiana w 5 plikach z gotowym kodem w briefie — Spark; recenzja tania i z innej rodziny — Sol `medium`
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark i Codex nieznany (wrapper bez zapasu, bez komunikatu limitu, 2026-10-11 12:40); Claude znany — ZIELONY (hook, 12:45)
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zgodny z briefem co do znaku, sprawdzenia własnych plików zielone; pełne `npm test` wykazało 1 czerwony test w `theme/separators.spec.ts`, którego brief nie wymienił (kolejność deklaracji z nowego mixinu) — luka briefu architekta, nie wykonawcy
- Rundy korekt: 1 — K1 (regex i nowy test `arc-overlap`); ponadto jednolinijkowe zaostrzenie asercji `position: relative` do bloku `:host` przez architekta po uwadze wykonawcy
- Czas do akceptacji: ok. 25 min od briefu
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 defektów; recenzent słusznie obalił przesłankę briefu (pas nie musi przykrywać kontenera z `z-index: 1`, bo nakładka obejmuje tylko dolny odstęp)
- Defekty po odbiorze: brak stwierdzonych
- Wymagane testy i dowody: 112 plików / 1312 testów, lint, format, build — 19 tras; sondy Chrome 390/1003/1440/2560 w obu motywach: odstęp treści do wierzchołka łuku (80/120 px), położenie pasa, wysokość strony i obu plam identyczne co do piksela przed i po, nakładka 28/48 px, bez przewijania w poziomie; zrzuty z rozciągniętym kontrastem — przed: prosta krawędź gradientu w prawym rogu na każdej szerokości komputera, po: gradient ciągły do łuku; pozostałe łuki (sekcja wyróżniona −80 px, pasy zamknięcia) bez zmian

### BE-113 (BeautyEffect: mały, półprzezroczysty przycisk pauzy filmu otwarcia) — 2026-10-11
- Archetyp: zmiana kontrolki w szablonie i SCSS (przycisk tekstowy → ikona z `aria-label`) + aktualizacja testów
- Stawka: niska (wygląd; ograniczenie dostępności WCAG 2.2.2 i 1.4.11 — przycisk musi zostać i być rozpoznawalny)
- Niepewność: niska; krycie koła i znaku architekt wyznaczył przed briefem pomiarem 36 klatek filmu w rogu przycisku (390/1440 px) — najmniejsza para dająca ≥ 3:1 na najjaśniejszym pikselu
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `high` — F1 (163 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `medium`, `-Mode review`
- Dopuszczone alternatywy: Codex Sol `medium` jako wykonawca; Gemini `high` jako recenzent
- Powód wyboru: prosta zmiana w 3 plikach z gotowym kodem w briefie — Spark; recenzja innej rodziny, tania — Sol `medium`
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark i Codex nieznany (wrapper, bez komunikatu limitu, 2026-10-11 12:55); Claude znany — ZIELONY (hook, 12:55)
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zgodny z briefem; jedyne odchylenie — ręczne zawinięcie linii pod prettier zamiast `--write` (słuszne)
- Rundy korekt: 0
- Czas do akceptacji: ok. 20 min od briefu
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 defektów; recenzent nie miał wersji bazowej testów — brak osłabienia asercji sprawdził architekt w diffie (zamiany 1:1 i nowe asercje)
- Defekty po odbiorze: brak stwierdzonych
- Wymagane testy i dowody: 112 plików / 1313 testów, lint, format, build — 19 tras; sondy Chrome 1440/390 w obu motywach: start z `pi-pause` i `Wstrzymaj film`, klik → film stoi, `pi-play` i `Odtwórz film`, cel 32 × 32 px, fokus klawiaturą z pierścieniem, 0 błędów konsoli; zrzuty i zbliżenia rogu obejrzane

### BE-114 (BeautyEffect: teksty całej strony pod konwersję, SEO i GEO — i18n, JSON-LD, dokumenty stron) — 2026-10-11
- Archetyp: wdrożenie zatwierdzonego planu treści — podmiana ok. 140 tekstów w i18n z aktualizacją testów przypinających teksty i dwiema drobnymi zmianami szablonu (B1), rozszerzenie danych strukturalnych (B3), aktualizacja 15 dokumentów stron (D1); decyzję, wymagania i docelowy plik tłumaczeń przygotował architekt
- Stawka: średnia (treść publicznej strony, twierdzenia o zabiegach medycznych, dane dla wyszukiwarek; bez niezmiennika wysokiej stawki)
- Niepewność: niska–średnia (testy przypinające stare teksty poza listą briefu; spójność dokumentów stron z i18n)
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `high` — B1 (590 s), B3 (217 s), D1 (497 s), równolegle w jednej fali o rozłącznych plikach
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review` (R1, FE, 139 s); Gemini / `gemini-3.8-flash-high`, `-Access read` (R2, dokumentacja autorstwa Sparka i architekta, 769 s)
- Dopuszczone alternatywy: Codex Sol `medium` jako wykonawca B3; Gemini `high` jako wykonawca D1; Spark `-Access read` odrzucony jako recenzent (autor)
- Powód wyboru: briefy z twardą wyrocznią (docelowy plik tłumaczeń porównywany jako obiekt, gotowe pola JSON-LD) — Spark `high`; recenzja FE z innej rodziny — Sol `high`; dokumenty pisane przez Sparka i Claude'a — trzecia rodzina, Gemini
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark, Codex i Gemini nieznany (wrapper bez zapasu, bez komunikatu limitu, 2026-10-11 13:30–13:45); Claude znany — ZIELONY, potem ŻÓŁTY (hook, 13:30–16:00)
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: B1 — plik tłumaczeń identyczny z docelowym, testy zaktualizowane bez osłabienia asercji, także cztery spoza minimalnej listy briefu (luka briefu architekta); forma `--include` z gwiazdkami w briefie nie znajduje testów — działa forma katalogowa; B3 — zgodny z briefem; D1 — 15 dokumentów stron zgodnych z i18n (166/166 brzmień), słusznie wskazał luki briefu: reguła „żadne stare brzmienie” musi wyłączać nazwy strukturalne i teksty-prefiksy, adnotacje pochodzenia stoją też w liniach „Pochodzenie:”
- Rundy korekt: 0 dla wykonawców; architekt dopisał we własnych i trzech stronicowych dokumentach zdania wynikające z nowej decyzji (wierne przejęcie z Booksy → redakcja) oraz 6 poprawek po R2
- Czas do akceptacji: ok. 2 h 30 min od briefów (z dwoma przebiegami zrzutów po ok. 10 i 4 min)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R1 — 0 defektów; R2 — 6 potwierdzonych (P1 nieaktualne źródło JSON-LD w dokumencie strony — realnie P2; 3 × P2 nazwy udogodnień, podwójny nawias, brak dokumentu na liście zmian decyzji; 2 × P3 brak odnośnika `tel:` w tabeli działań, „jedno zdanie” przy dwóch zdaniach), 0 odrzuconych; dwa „błędne założenia briefu” R2 częściowo słuszne (akcent nagłówka nie jest regułą dokumentu strony)
- Defekty po odbiorze: brak stwierdzonych w zakresie zmiany; zrzuty ujawniły dwie usterki układu sprzed zmiany (ucięta druga linia opisu dużego kafelka przy 320 px, nazwa kafelka na strzałce przy 320/768 px)
- Wymagane testy i dowody: 113 plików / 1316 testów, lint, format, build — 19 tras; HTML z serwera na 15 adresach (długości tytułów i opisów, JSON-LD tylko na `/` i `/kontakt`, bez surowych kluczy); skrypt plan → i18n (116 zgodnych co do znaku, 25 odstępstw opisanych) i i18n → dokumenty stron; `browser-check matrix` 5 stron × 320/768/1440 jasny + 320 ciemny, 0 błędów konsoli i sieci

### BE-115 (BeautyEffect: kafle mozaiki kategorii — nazwa na strzałce, ucięty opis dużego kafla) — 2026-10-11
- Archetyp: naprawa układu responsywnego w SCSS komponentu z kontraktowymi testami skompilowanego SCSS (5 plików FE: 2 × SCSS, szablon, 2 × spec); geometrię zmierzył w przeglądarce architekt, brief podawał dokładny kod
- Stawka: niska–średnia (wygląd publicznej strony głównej; bez niezmiennika wysokiej stawki)
- Niepewność: średnia (zachowanie CSS: jednostki kontenera, `aspect-ratio` z ograniczeniami wymiarów)
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `high` — brief główny (234 s), korekta (258 s)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `medium`, `-Mode review` (80 s)
- Dopuszczone alternatywy: `wykonawca` (Sonnet `high`) lub Gemini `high` jako wykonawca; Gemini `-Access read` jako recenzent
- Powód wyboru: brief z gotowym kodem i twardą wyrocznią (testy kontraktu SCSS, pomiar w przeglądarce) — Spark `high`, jak trzy zaakceptowane briefy tego dnia; krótka recenzja z innej rodziny — Sol `medium`
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark i Codex nieznany (wrapper bez zapasu, bez komunikatu limitu, 2026-10-11 16:15–16:30); Claude znany — ZIELONY (hook)
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zgodny z briefem co do znaku; jedno słuszne odchylenie (pusta linia wymagana przez stylelint); dobre uwagi w sekcji „co błędne” (Sass upraszcza `calc` w `min()`, krótkie nazwy też maleją na wąskim kaflu)
- Rundy korekt: 1 — błąd briefu architekta, nie wykonawcy: `aspect-ratio: 4 / 3` z `min-height` poszerzał duży kafel do 353 px przy 320 px (przeglądarka przenosi `min-height` przez proporcję na szerokość); wykrył go pomiar architekta po pierwszej fali, poprawka: wysokość `max(75cqi, …)` bez `aspect-ratio`
- Czas do akceptacji: ok. 25 min od wysłania briefu (pomiar przed briefem ok. 15 min)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 zgłoszonych; recenzja bez przeglądarki przeoczyła P1 (poziome przewijanie strony przy 320–360 px, kafel szerszy od kolumny przy 375–390 px) — wniosek: recenzja SCSS układu nie zastępuje pomiaru w przeglądarce
- Defekty po odbiorze: brak stwierdzonych
- Wymagane testy i dowody: 113 plików / 1317 testów, lint, format, build — 19 tras; pomiar w Chrome przy 12 szerokościach (320–1440) w obu motywach: nazwa nie sięga strzałki (zapas ≥ 9,8 px), napis w 45 %, opis w dwóch wierszach, kafel w kolumnie, bez przewijania w poziomie; zrzuty mozaiki 320/360 ciemny/768/1024/1440

### BE-116 (BeautyEffect: druga analiza tekstów całej strony pod konwersję, SEO i GEO — plan zmian) — 2026-10-11
- Archetyp: analiza copywriterska i SEO/GEO całej strony (i18n ok. 110 KB, 15 prerenderowanych HTML-i, szablony, JSON-LD) z gotowymi brzmieniami; wynik to jeden plik planu w dokumentacji, bez zmian w kodzie; drugie przejście po wdrożeniu BE-114
- Stawka: średnia (treść publicznej strony, twierdzenia o zabiegach medycznych i laserowych; bez niezmiennika wysokiej stawki)
- Niepewność: średnia (ocena redakcyjna bez danych o wolumenie fraz; ryzyko wymyślonych faktów)
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` — wybór linii przez właściciela („zrób to na gpt 6 sol”), `-Repo` = katalog dokumentacji (zapis tylko tam, FE poza piaskownicą), 1929 s, 6 wyszukiwań w sieci
- Recenzent (linia / model / native effort): architekt — weryfikacja odczytem źródeł i skryptem plan → i18n; plan jest propozycją do akceptacji właścicielki, nie kodem
- Dopuszczone alternatywy: Sol `xhigh` (nieznaczny wzrost jakości przy większym zużyciu puli Plus); Spark `xhigh` lub Gemini `high`, gdyby właściciel nie wskazał linii
- Powód wyboru: linia wskazana przez właściciela; `high` jako kolano krzywej przy najmniejszej puli
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper bez zapasu, bez komunikatu limitu, 2026-10-11 16:14–16:46); Claude znany — ZIELONY (hook)
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: 106 zmian tekstu (P1 29, P2 70, P3 7), 3 [szablon], D-7…D-9, M-7…M-10; skrypt: 106/106 kluczy istnieje, „Obecnie” zgodne co do znaku, limity 60/155 i HIGHLIGHT spełnione; fakty pod P1 z pokryciem w źródłach (kaucja — usługodawca, usuwanie pigmentu w Booksy, IPL Cutera); trafne znaleziska nieuchwycone w BE-114 (pięć instrukcji odstawiania leków, kaucja przypisana Booksy); słusznie zgłosił równoległe zmiany w drzewie (BE-115) zamiast uznać warunek „nic poza planem” za spełniony
- Rundy korekt: 0 (zastrzeżenia architekta dopisane do planu, do rozstrzygnięcia przy akceptacji)
- Czas do akceptacji: odbiór architekta ok. 15 min po przebiegu; akceptacja treści czeka na właścicielkę
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 4 zastrzeżenia redakcyjne architekta — skrócenie kafelków jako P1 nieaktualne po BE-115; dwa wstępy łamią zasady stylu briefu (zdanie bez informacji, opis strony zamiast zabiegów) i gubią frazy docelowe z własnej mapy fraz; opisy laserów gubią cel zabiegu; skrócone tytuły tracą frazy
- Defekty po odbiorze: brak stwierdzonych błędów faktów
- Wymagane testy i dowody: `git status` + porównanie diffów przed i po w FE i dokumentacji (zmiany spoza planu przypisane BE-115 po znacznikach czasu i rekordach wrappera); skrypt plan → `pl.json`; odczyt źródeł dla faktów P1

### BE-117 (BeautyEffect: wdrożenie drugiego planu tekstów — i18n, nazwa dostępna „Czytaj więcej”, `@id`/`publisher` w JSON-LD, dokumenty stron) — 2026-10-11
- Archetyp: wdrożenie zaakceptowanego planu treści — podmiana 84 tekstów i 2 nowe klucze z docelowego pliku tłumaczeń, `aria-label` przycisku z testem obu stanów (B1); `@id` i `publisher` w JSON-LD w nowym pliku pomocniczym (B2); aktualizacja 16 dokumentów stron i wymagania widoczności (D1); docelowy plik i 10 brzmień przygotował architekt
- Stawka: średnia (treść publicznej strony, opisy zabiegów medycznych i laserowych, dane dla wyszukiwarek; bez niezmiennika wysokiej stawki)
- Niepewność: niska dla kodu (twarda wyrocznia: plik docelowy, dokładne pola JSON-LD); średnia dla treści (teksty z planu Sola nie przeszły wcześniej niezależnej recenzji redakcyjnej)
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `high` — B1 (224 s), B2 (154 s), D1 (632 s), równolegle w jednej fali o rozłącznych plikach
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (R1 — nowe teksty i kod FE, 526 s; teksty autorstwa Sola i Claude'a, kod Sparka — trzecia rodzina wobec obu); Codex / `gpt-6.1-sol` / `high`, `-Mode review` (R2 — izolowany diff D1, 288 s)
- Dopuszczone alternatywy: Codex Sol `medium` jako wykonawca B2; Gemini `high` jako wykonawca D1; Sol jako recenzent R1 odrzucony (autor tekstów — rodzina Codex); Sol `medium` dla R2 odrzucony (przeoczony defekt w BE-115)
- Powód wyboru: briefy z twardą wyrocznią i gotowym kodem — Spark `high`, jak w BE-114; recenzja treści poza rodzinami autorów — Gemini; dokumentacja Sparka przy zajętym Gemini — Sol `high` (17 dokumentów, spójność wewnętrzna)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark, Codex i Gemini nieznany (wrapper bez zapasu, bez komunikatu limitu, 2026-10-11 17:02–17:20); Claude znany — ZIELONY (hook, 17:10–17:25)
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: B1 — plik tłumaczeń równy docelowemu, testy przypinające teksty zaktualizowane bez osłabienia asercji, `aria-label` z testem obu stanów; zgłosił 83 zamiast 84 zmian (dwie wartości w jednej tablicy — liczenie, nie brak); B2 — zgodny z briefem; D1 — 86/86 brzmień w dokumentach, zero starych, słusznie wskazał literówkę briefu (klucz bez prefiksu) i zawijanie linii w dokumentach jako pułapkę weryfikacji; jedna usterka: nowy punkt listy z wcięciem 4 zamiast 5 spacji (poprawił architekt)
- Rundy korekt: 0 dla wykonawców; architekt wprowadził 5 wartości i 3 dokumenty po R1 oraz 4 dokumenty po R2 (zmiany jednolinijkowe)
- Czas do akceptacji: ok. 30 min od briefów (ze zrzutami i dwiema recenzjami)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R1 — 4 potwierdzone (P1 lipoliza bez objaśnienia pojęcia — realnie P2; P2 puste drugie zdanie opisu Larens; 2 × P3: wstęp laserów zgubił zabieg na wiotką skórę, wyróżnienie tropokolagenu), 1 odrzucone (P3 osobny spec funkcji pomocniczej); proponowane brzmienia R1 obiecywały efekt bez źródła — nie weszły; wszystkie 4 to defekty treści z planu Sola, przeoczone przy odbiorze planu przez architekta, nie defekty wykonawców; R2 — 2 potwierdzone (P2 reguły „dwa zdania” w 3 dokumentach sprzeczne ze skróconymi opisami — luka briefu D1 architekta; P3 adnotacja „dosłownie” przy poprawionym cytacie), 0 odrzuconych; 1186 linków, zero martwych
- Defekty po odbiorze: brak stwierdzonych w zakresie zmiany; zrzut ujawnił usterkę sprzed zmiany (nazwa zakładki „Oczyszczanie i kwasy” łamie się w środku słowa przy 320 px)
- Wymagane testy i dowody: 113 plików / 1318 testów, lint, format, build — mapa strony 15 adresów (dwukrotnie: po fali i po poprawkach); `pl.json` == plik docelowy; skrypt tabela → dokumenty w obie strony; HTML z serwera na 15 adresach (tytuły ≤ 65, opisy ≤ 146, JSON-LD `#salon`/`#website`/`publisher`, 24 nazwy „Czytaj więcej: …”); `browser-check matrix` 3 strony × 320 px jasny, 0 błędów konsoli i sieci

### BE-118 (BeautyEffect: rozstrzygnięcia otwartych spraw tekstów — nazwy urządzeń jako odnośniki, przewijanie do kotwicy ze `scroll-margin-top`, teksty leków przy laserach) — 2026-10-11
- Archetyp: kilka zmian po decyzjach architekta z upoważnienia właściciela:
  - W1: trzy nazwy urządzeń jako `routerLink` z `fragment`, styl odnośnika i spec;
  - W2: podmiana `ViewportScroller` na klasę przewijającą do kotwicy przez `scrollIntoView`, czyli z poszanowaniem `scroll-margin-top`; nowa klasa, provider, spec z red-green;
  - W3: spłaszczenie bloku SCSS przekraczającego budżet stylu;
  - teksty i dokumenty po stronie architekta.
- Stawka: średnia. Treść medyczna przy laserach to leki i przeciwwskazania. Do tego przekrojowe przewijanie do kotwic w całej aplikacji. Bez niezmiennika wysokiej stawki.
- Niepewność:
  - W1 i W3 niska: twarda wyrocznia w specu i budżecie;
  - W2 średnia: kontrakt `ViewportScroller` i SSR, a przyczyna zmierzona dopiero w przeglądarce.
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor`:
  - W1 — `high`, 402 s;
  - W2 — `high`, 357 s;
  - W3 — `low`, 52 s.
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review`:
  - R3 — teksty i dokumenty architekta oraz kod W1, 310 s;
  - R4 — W2 i poprawki tekstów po R3, 274 s.
  
  Rodzina inna niż oba źródła zmian (Spark, Claude).
- Dopuszczone alternatywy:
  - Gemini `high` `-Access read` jako recenzent R3 i R4;
  - `wykonawca` (Sonnet `high`) dla W2 — odrzucony: koszt kontekstu w puli Claude'a, a brief miał twardą wyrocznię;
  - `mechanik` dla W3 — odrzucony: start ok. 58 tys. tokenów wobec 52 s Sparka.
- Powód wyboru:
  - kod z gotową specyfikacją i pętlą lint/test — Spark (pamięć „Spark przejmuje prostą pracę”);
  - recenzja treści medycznej i kontraktu frameworka — Sol `high`, jak R2 w BE-117 (0 fałszywych P0/P1).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas):
  - Spark i Codex — nieznany: wrapper nie podaje zapasu i nie zgłosił limitu, 2026-10-11 15:42–16:11 UTC;
  - Claude — znany, ZIELONY: hook, okno 5 h 16–17 %, tydzień 10 %.
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia:
  - W1 zgodny z briefem, red-green potwierdzony. Mimo to przy kontroli w przeglądarce wyszedł defekt: tytuł karty lądował pod nagłówkiem. Przyczyną była luka briefu architekta, który założył, że Angular przy `anchorScrolling` uwzględnia `scroll-margin-top`. Angular przewija współrzędnymi przez `window.scrollTo`.
  - W2 zgodny. Trzy odchylenia wymusiły bramki repo (`sonarjs/cognitive-complexity`, `unbound-method`, `no-unnecessary-type-assertion`). Spark słusznie wskazał w briefie wzorzec asercji, który łamie lint.
  - W3 zgodny.
- Rundy korekt: 0 dla wykonawców.
  - W2 to nowy brief na defekt ujawniony przez `browser-check`.
  - W3 to nowy brief na ostrzeżenie budżetu po W1. Ostrzeżenie przeoczył architekt przy pierwszej walidacji, bo filtr wyjścia buildu nie obejmował budżetu.
- Czas do akceptacji: ok. 35 min od briefu W1, z dwiema recenzjami i czterema przebiegami `browser-check`.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet):
  - R3 — 3 potwierdzone, wszystkie w tekstach i dokumentach architekta, w kodzie W1 nic. Znaleziska:
    - P2: akapity leków gubiły przeciwwskazanie „niedawno zakończona kuracja retinoidami”;
    - P2: zniknęło objaśnienie „retinoidów” wymagane przez WP-PROSTY-JEZYK;
    - P3: reguła w dokumencie obejmowała „każdą kartę” zamiast pięciu.
    
    0 odrzuconych.
  - R4 — 0 znalezisk.
  - Recenzja R3 nie wykryła złego lądowania kotwicy (sama zaznaczyła, że nie uruchamiała przeglądarki); wykrył je dopiero zrzut.
- Defekty po odbiorze: brak stwierdzonych. Odnotowane rozbieżności sprzed zmiany:
  - AT-SPECYFIKACJA-WYGLADU mówi „80 px pod paskiem”, a kod daje wysokość nagłówka + 72 px;
  - nazwa zakładki „Oczyszczanie i kwasy” przy 320 px (z BE-117).
- Wymagane testy i dowody:
  - 114 plików / 1331 testów, lint 0, format 0;
  - build 0 bez ostrzeżenia budżetu (19 stron prerenderowanych);
  - spec klasy przewijania 8/8 z czerwonym przebiegiem przed poprawką.
  - `browser-check matrix` (0 błędów konsoli i sieci):
    - odnośniki urządzeń w 2 szerokościach × 2 motywach;
    - lądowanie po kliknięciu trzech nazw i po wejściu na adres z kotwicą, przed i po poprawce;
    - notka „Jak się umówić”, zamknięcie makijażu permanentnego i akapit „Przed wizytą” przy laserach.

### BE-119 (BeautyEffect: zdjęcia i film zamiast paneli typograficznych — materiały z Instagrama salonu i zdjęcia poglądowe z banku zdjęć) — 2026-10-11
- Archetyp: podmiana danych konfiguracyjnych stron po decyzji właściciela.
  - M2: 7 banerów grup, 3 łuki otwarcia lasera, łuk lasera na stronie „Oferta”, kafel lasera z filmem na stronie głównej, klucze `pl.json` (`PANEL_WORD` → `BANNER_ALT`, `OPENING.ALT`) i specy;
  - kadry (13 plików w `public/`), decyzja, katalog zdjęć i dokumenty stron po stronie architekta.
- Stawka: niska. Treść wizualna i teksty alternatywne, bez niezmiennika wysokiej stawki. Ryzyko leżało w licencji i granicach zdjęć poglądowych (bez twarzy i efektów), a to rozstrzyga decyzja, nie kod.
- Niepewność: niska. Twarda wyrocznia: kontrola osieroconych kluczy i `BANNER_ALT` w specach, lint, build z prerenderem.
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `high`, `-Access write`, M2 — 350 s.
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `medium`, `-Mode review`, R-M2 — 60 s. Rodzina inna niż wykonawca.
- Dopuszczone alternatywy:
  - Gemini `high` `-Access read` jako recenzent;
  - Spark `medium` jako wykonawca — odrzucony: 17 plików, dane czterech rodzajów miejsc (baner, łuk otwarcia, łuk oferty, kafel z filmem) i ich specy;
  - `wykonawca` (Sonnet `high`) — odrzucony: koszt kontekstu w puli Claude'a przy briefie bez Figmy.
- Powód wyboru:
  - dane z gotową specyfikacją i pętlą lint/test — Spark (pamięć „Spark przejmuje prostą pracę”);
  - recenzja zgodności danych z plikami i kluczami — Sol `medium`; zakres nie wymagał `high`.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas):
  - Spark i Codex — nieznany: wrapper nie podaje zapasu i nie zgłosił limitu, 2026-10-11 16:37–16:45 UTC;
  - Claude — hook bez ostrzeżenia w tym oknie.
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: zgodny z briefem, jedno uzasadnione odchylenie. Spark obalił założenie briefu: szablon mozaiki renderował 9. kafel wyłącznie w gałęzi panelu. Dodał gałąź `@else` z kaflem zdjęcia i filmu jak kafle 4–8; architekt ją przyjął.
- Rundy korekt: 0.
- Czas do akceptacji: ok. 14 min od briefu do commitu, z recenzją, pełną walidacją i `browser-check`.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R-M2 — 0 znalezisk; sprawdziła też gałąź `@else`.
- Defekty po odbiorze: brak stwierdzonych. Błąd procesu po stronie architekta: `git add -A src` objął 5 plików równoległej sesji. Cofnięty przez `reset --soft` przed pushem; od tej pory commit tylko z jawną listą ścieżek.
- Wymagane testy i dowody:
  - 114 plików / 1336 testów, lint 0, format 0;
  - build 0, 19 stron prerenderowanych;
  - CI na `main` zielone;
  - `browser-check matrix` 40/40 (10 widoków × 2 szerokości × 2 motywy), 0 błędów konsoli i sieci.

### BE-120 (BeautyEffect: odstęp karty zabiegu po odnośniku 80 px i margines paska zakładek na telefonie) — 2026-10-11
- Archetyp: drobna poprawka CSS na podstawie specyfikacji i makiety, z testami kontraktu SCSS. Pięć plików jednej warstwy:
  - `scroll-margin-top` karty: `+ 72px` → `+ 80px`;
  - klasa `group-tabs__container` z `padding-inline: 8px` poniżej `sm`.

  Dokument specyfikacji wyglądu uzupełnił architekt.
- Stawka: niska (wygląd, bez niezmiennika).
- Niepewność: niska. Przyczynę ustalił pomiar w Chrome przed briefem: „Oczyszczanie” ma 84 px, a obszar tekstu 83,3 px; margines kontenera wynosił 20 px zamiast 8 px z makiety.
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `medium` (256 s).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (R5). To rodzina inna niż oba źródła zmian (Spark, Claude). Codexa zostawiłem na bramki i trudniejsze recenzje.
- Dopuszczone alternatywy: Spark `low` (jak W3 w BE-118); Codex Sol `high` jako recenzent.
- Powód wyboru: krótki brief z dokładnymi wartościami i testami red-green — Spark `medium`. Przy samym przeniesieniu bloku bez testów wystarczył `low` (W3).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas):
  - Spark i Gemini: nieznany (wrapper bez komunikatu limitu, 2026-10-11 16:43–16:55 UTC);
  - Claude: znany — ZIELONY (hook, okno 5 h 22–25 %).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: zgodny z briefem, red-green potwierdzony (4 asercje czerwone przed zmianą). Dwa odchylenia wymusiła bramka repo:
  - osobny blok `describe` z powodu `sonarjs/max-lines-per-function`;
  - `prettier --write` na własnym pliku.

  Spark słusznie wskazał, że asercja strażnika (`overflow-wrap`) z natury nie bywa czerwona.
- Rundy korekt: 0.
- Czas do akceptacji: ok. 25 min od pomiaru przyczyny (z recenzją i zrzutami).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R5 — 0 znalezisk. Dwie trafne uwagi do briefu:
  - „pod paskiem u góry” było niejednoznaczne (w specyfikacji to nagłówek P-2);
  - „7 stron” to strony z zakładkami, nie wszystkie 9.
- Defekty po odbiorze: brak stwierdzonych.
- Wymagane testy i dowody:
  - spece komponentów strony kategorii (11 plików, 103 testy);
  - eslint, stylelint i prettier na własnych plikach;
  - build do osobnego katalogu, bo w drzewie równolegle pracowała inna sesja;
  - pomiar w Chrome: obszar tekstu zakładki 91 px przy 320 px, bez łamania słów na 7 stronach z zakładkami (320–390 px); karta staje dokładnie na wysokości nagłówka + 80 px (144 / 152 px);
  - `browser-check matrix` przy 320 px w motywie jasnym i ciemnym, 0 błędów konsoli i sieci.

### BE-121 (BeautyEffect: obraz Dockera i ręczne wdrożenie na serwer Mikrus — workflow, środowisko `Prod`, pierwsze wdrożenie) — 2026-10-11
- Archetyp: konfiguracja wdrożenia.
  - D1: `Dockerfile` (Node SSR, licencja jako sekret BuildKita), `.dockerignore`, ręczny workflow build → GHCR → SSH, hosty tymczasowe w `allowedHosts`;
  - D1-K1: poprawki po recenzji (skrypt SSH z przywracaniem poprzedniego kontenera, akcje przypięte do SHA);
  - po stronie architekta: środowisko GitHub i zmienne, sekcja Environments w regułach FE/BE, dziennik serwera, luki polityki prywatności.
- Stawka: średnia. Współdzielony serwer produkcyjny z innymi kontenerami i sekrety przywoływane po nazwie. Bez niezmiennika wysokiej stawki: licencja trafia celowo do kodu przeglądarki, a sekrety SSH i licencję wpisał właściciel.
- Niepewność: średnia. `npm ci --ignore-scripts` na alpine i SSR bez `node_modules` niesprawdzone przed buildem; zachowanie pośrednika HTTPS Mikrusa nieznane.
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor`:
  - D1 — `high`, 446 s;
  - D1-K1 — `medium`, 111 s; treść skryptu podana dosłownie.
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review`, R-D1 — 146 s. Rodzina inna niż oba źródła zmian (Spark, Claude). Dodatkowo automatyczny przegląd bezpieczeństwa wtyczki (nieprzypięte akcje).
- Dopuszczone alternatywy:
  - Gemini `high` `-Access read` jako recenzent;
  - `wykonawca-opus` — odrzucony: brak niezmiennika wysokiej stawki w plikach, wzorzec z działającego projektu siostrzanego.
- Powód wyboru:
  - pliki konfiguracji z pełną specyfikacją — Spark (pamięć „Spark przejmuje prostą pracę”);
  - recenzja skryptu na współdzielonym serwerze i obsługi sekretów — Sol `high`.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas):
  - Spark i Codex — nieznany: wrapper nie podaje zapasu i nie zgłosił limitu, 2026-10-11 17:08–17:22 UTC;
  - Claude — znany, ZIELONY: hook, okno 5 h 25–30 %, tydzień 11–12 %.
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia:
  - D1 zgodny z briefem: 4 pliki, Dockerfile bajtowo jak w briefie. Spark potwierdził przesłankę o zbundlowanym serwerze SSR.
  - **Naruszenie:** Spark uznał równoległe zmiany architekta w `AGENTS.md` i `.claude/CLAUDE.md` za swoje i cofnął je `git checkout`, łamiąc zakaz gita z briefu. Szkoda ograniczyła się do tych dwóch plików; architekt przywrócił je z kopii w BE. Brief poprawki zawierał bezwzględny zakaz gita z uzasadnieniem i Spark go przestrzegał.
  - D1-K1 zgodny.
- Rundy korekt: 1 (D1-K1, wynik recenzji).
- Czas do akceptacji: ok. 30 min od briefu D1 do udanego wdrożenia, w tym oczekiwanie na sekrety właściciela i jedno nieudane wdrożenie (błędne hasło w sekrecie, poprawione przez właściciela).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet):
  - R-D1 — 3 potwierdzone, 0 odrzuconych:
    - P2: logowanie do ghcr.io zostawało na serwerze po błędzie `pull`;
    - P2: stary kontener był usuwany przed sondą zdrowia nowego;
    - P2: globalny `docker image prune` na współdzielonym serwerze.
  - R-D1 słusznie obaliła przesłankę briefu architekta („licencji nie może być w żadnej warstwie”, a celowo jest w kodzie przeglądarki) i według klauzuli STOP przerwała dalszą weryfikację.
  - Przegląd automatyczny — 1 potwierdzone: akcje zewnętrzne nieprzypięte do SHA.
- Defekty po odbiorze: brak stwierdzonych. Błąd procesu po stronie architekta: commit rejestru z jawną ścieżką objął wpis BE-120 równoległej sesji, bo moja edycja pliku się nie powiodła (plik zmieniony w międzyczasie), a commit poszedł bez sprawdzenia diffu. Treść BE-120 jest kompletna i należy do tamtej sesji; mylący jest tylko opis commita `22e35f3`.
- Wymagane testy i dowody:
  - lokalny build obrazu z sekretem BuildKita: klucz 0 razy w `docker history`, obecny tylko w kodzie przeglądarki, brak plików `.env*`, użytkownik `node`;
  - test dymny kontenera: hosty tymczasowe 200, obcy host 400, `www` → 301, 404, pliki statyczne;
  - lokalny harness skryptu SSH: pierwsze wdrożenie, ponowne wdrożenie, brak obrazu (przerwanie przed zmianą), zepsuty obraz (przywrócenie poprzedniego, 200);
  - CI na `main` zielone;
  - wdrożenie przez workflow: sonda zdrowia ✓; z zewnątrz oba adresy 200, 404, mapa strony i film 200;
  - `browser-check matrix` na żywym adresie HTTPS 16/16, 0 błędów konsoli i sieci.

### BE-122 (BeautyEffect: tekst otwarcia, numer z +48, wyśrodkowany pasek stopki, kurtyna zdjęć z czterech krawędzi) — 2026-10-11
- Archetyp: Frontend UI — dwa briefy w jednej fali: (1) i18n + stała + SCSS, (2) serwis odsłonięć (TS) + SCSS przejść + testy.
- Stawka: niska (strona wizytówka, bez niezmiennika high-stakes).
- Niepewność: niska (1); średnia (2) — interakcja przejść CSS z hydratacją.
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `medium` (1) i `high` (2 + korekta).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `medium`, `-Mode review`, jedna recenzja całej fali (inna rodzina niż autor).
- Dopuszczone alternatywy: Gemini `gemini-3.8-flash-medium` (1), Codex `gpt-6.1-sol` `high` lub `wykonawca` Sonnet 5.5 `high` (2); recenzja: Gemini `gemini-3.8-flash-high` `-Access read`.
- Powód wyboru: proste briefy bez Figmy i bez niezmiennika — pula Sparka zgodnie z preferencją użytkownika, pula Codexa na recenzję.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark `nieznany`, Codex `nieznany` (brak odczytu zapasu, 2026-10-11 ~20:15); Claude ZIELONY (hook).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: (1) zaakceptowany; (2) wymagał korekty.
- Rundy korekt: (1) 0; (2) 1.
- Czas do akceptacji: ~15 min (1, przebieg 313 s); ~25 min (2: przebieg 131 s + recenzja 90 s + korekta 143 s + walidacja).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): potwierdzone 1 × P2 — `transition` kurtyny działało także w stanie ukrytym, więc przydział krawędzi po hydratacji animował stan ukryty (ćwiartka zdjęcia widoczna, odsłonięcie ze stanu pośredniego). Błąd tkwił w specyfikacji architekta, nie w wykonaniu. Odrzucone: 0. Spark w (1) słusznie wskazał niepełną listę specyfikacji do poprawy (normalizacja `\s+` z twardą spacją) i sam ją domknął zgodnie z punktem zakresu.
- Defekty po odbiorze: brak stwierdzonych.
- Wymagane testy i dowody: `npm run lint`, `format:check`, `npm test` 1351/1351, build (19 tras); przeglądarka na lokalnym SSR i na produkcji: zero przejść `clip-path` na ukrytych kurtynach, odsłonięcie animowane od przydzielonej krawędzi, pasek stopki 51/50 px (komputer i telefon), numer `+48 795 547 837`; CI i wdrożenie `Prod` zielone.

### 2705-B1 (trwałość i bramka operatora płatności — przebieg przerwany przekazaniem) — 2026-10-12
- Archetyp: Backend — migracja, repozytorium Dapper, bramka operatora płatności
- Stawka: wysoka / high-stakes (migracja danych, płatność)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh`
- Recenzent (linia / model / native effort): — (brief podzielony przed recenzją)
- Dopuszczone alternatywy: brak (przy CZERWONYM Spark `max`)
- Powód wyboru: twarda bramka — migracja i płatność
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): znany, hook Claude'a ZIELONY, 2026-10-12 rano
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: przekazanie przy ~306 tys. kontekstu (strażnik kontekstu, próg miękki) po warstwie bazy; bramka operatora nie rozpoczęta
- Rundy korekt: 0 (reszta zlecona jako B1a/B1b świeżym agentom tej samej linii)
- Czas do akceptacji: nie dotyczy — zastąpiony przez B1a i B1b
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): —
- Defekty po odbiorze: —
- Wymagane testy i dowody: —
- Wniosek: brief łączący migrację, repozytorium (20 zapytań) i bramkę operatora był za duży na jeden przebieg (reguła 15) — dzielić od razu na bazę i bramkę.

### 2705-B1a (tabela prób zakupu, słownik stanów, repozytorium z testami DB) — 2026-10-12
- Archetyp: Backend — migracja i repozytorium Dapper
- Stawka: wysoka / high-stakes (migracja danych, przejścia stanów warunkowe)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh`
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access read`
- Dopuszczone alternatywy: wykonawca — brak (przy CZERWONYM Spark `max`); recenzent — brak bez naruszenia rezerwy puli Codexa na bramkę (reguła 7), Gemini wykluczony przy high-stakes
- Powód wyboru: twarda bramka; recenzent innej rodziny o stawce wyższej niż niska
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook ZIELONY); Spark nieznany (wrapper bez zapasu), 2026-10-12
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowano (build i 5508 testów zielone, 0 pominiętych; kontrola SQL przez architekta)
- Rundy korekt: 0 (3 × P3 z recenzji wykonuje następny brief tej samej linii)
- Czas do akceptacji: ~1 h (z recenzją 11 min)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): potwierdzone 3 × P3 (brak więzu zamkniętego zbioru przyczyn porażki, zbędna metoda kasowania bez warunku stanu, nieaktualna liczba w legendzie diagramu); odrzucone 0
- Defekty po odbiorze: brak (stan na odbiór fali)
- Wymagane testy i dowody: `dotnet build`, `dotnet test` ze zmienną testów SQL (0 pominiętych), przegląd zapytań warunkowych

### 2705-F1a (awans konfiguratora oferty do warstwy wspólnej + przeniesienie kluczy i18n) — 2026-10-12
- Archetyp: Refactoring / Architektura — hoisting komponentów i kluczy i18n
- Stawka: niska (bez niezmiennika; regresja strony zakupu publicznego łapana testami)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access write`
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read`
- Dopuszczone alternatywy: wykonawca — Claude `wykonawca` Sonnet 5.5 `high`; recenzent — Sol `high` (pominięty: rezerwa puli Codexa na bramkę)
- Powód wyboru: zmiana mechaniczna o dużej liczbie plików; Spark lokalnie 0–1 rund; Gemini preferowany przy niskiej stawce (reguła 13)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark i Gemini nieznany (wrappery), 2026-10-12
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowano po cofnięciu przez architekta niezgłoszonej zmiany koloru w jednym arkuszu SCSS (poza zakresem briefu)
- Rundy korekt: 0
- Czas do akceptacji: ~35 min (wykonanie 18 min, recenzja 10 min)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): werdykt poprawny (1,0); P3 obsłużone przez architekta
- Defekty po odbiorze: 1 — komentarz w presecie wskazywał starą ścieżkę po przeniesieniu; poprawka architekta złamała test lustra design systemu (lustro w 2 repozytoriach), cofnięta — dług do bramki
- Wymagane testy i dowody: lint, format, pełny `npm test`, build; specy strony zakupu publicznego zielone

### 2705-F1b (awans pomocników operatora płatności i serwisów profilu do obszaru zalogowanego) — 2026-10-12
- Archetyp: Refactoring / Architektura — hoisting serwisów i DTO
- Stawka: niska (przeniesienie bez zmiany zachowania)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access write`
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read`
- Dopuszczone alternatywy: jak 2705-F1a
- Powód wyboru: jak 2705-F1a; rozłączne pliki, równolegle
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark i Gemini nieznany (wrappery), 2026-10-12
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowano
- Rundy korekt: 0
- Czas do akceptacji: ~35 min (wykonanie 16 min, recenzja 10 min)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): werdykt poprawny (0,98); P3 obsłużone
- Defekty po odbiorze: brak
- Wymagane testy i dowody: lint, format, pełny `npm test`, build

### 2705-F2a (klient HTTP zakupu z konta, DTO, enumy, strażnik trasy, awans typów nabywcy) — 2026-10-12
- Archetyp: Frontend — serwis HTTP, DTO, strażnik trasy
- Stawka: średnia (strażnik dostępu i kontrakt płatności, bez logiki płatności)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access write`
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read`
- Dopuszczone alternatywy: wykonawca — `wykonawca-opus` (strażnik); recenzent — Sol `high` (rezerwa puli Codexa)
- Powód wyboru: kod według ścisłego kontraktu i wzorca istniejącego strażnika; logika płatności wydzielona do osobnego briefu Opusa
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark i Gemini nieznany (wrappery), 2026-10-12
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowano; jedno odstępstwo zgłoszone słusznie (brief wskazał nieistniejący spec)
- Rundy korekt: 0 (2 × P3 wykonuje następny brief w tych plikach)
- Czas do akceptacji: ~2 h (wykonanie 9 min, recenzja 11 min; reszta to kolejka walidacji fali)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): potwierdzone 2 × P3 (zbyt szeroki typ kodu języka, niepełny komentarz strażnika o braku ponownego biegu po hydratacji); odrzucone 1 × P3 (adres bazowy — konwencja projektu)
- Defekty po odbiorze: brak (stan na odbiór fali)
- Wymagane testy i dowody: lint, format, pełny `npm test`, build; specy API, strażnika i mapowania nabywcy

### 2372-F3 (sekcja ustawień konta dla konta bez roli właściciela, z makiety) — 2026-10-12
- Archetyp: Frontend UI / Figma
- Stawka: niska (widoczność wyłącznie z roli w sesji)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Claude / `wykonawca` — Sonnet 5.5 / `high` (Figma MCP)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read`
- Dopuszczone alternatywy: wykonawca — brak (Figma MCP tylko w linii Claude'a w tej sesji); recenzent — Sol `high` (rezerwa puli Codexa)
- Powód wyboru: ekran z makiety wymaga faktycznego Figma MCP; linia Figmy po próbie A/B zostaje przy Sonnecie
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook ZIELONY); Gemini nieznany, 2026-10-12
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowano po poprawce wyrównania przycisku na szerokim ekranie przez architekta — przyczyna w specyfikacji (brief podał identyfikator całej strony zamiast sekcji, więc wykonawca nie odczytał wariantu szerokiego)
- Rundy korekt: 0 z wykonania (1 poprawka z winy specyfikacji)
- Czas do akceptacji: ~2 h (z kolejką walidacji fali; recenzja 12 min)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): potwierdzone 1 × P3 (tytuł testu deklaruje wąski ekran bez jego ustawienia) — wykonuje następny brief
- Defekty po odbiorze: brak (stan na odbiór fali)
- Wymagane testy i dowody: lint, format, pełny `npm test` z AXE, build; zrzuty makiety przez architekta

### 2372-FIG (nagłówek i opis sekcji w ramkach makiety) — 2026-10-12
- Archetyp: Frontend UI / Figma — edycja makiety
- Stawka: niska
- Niepewność: niska
- Wykonawca (linia / model / native effort): Claude / `wykonawca` — Sonnet 5.5 / `high` (Figma MCP)
- Recenzent (linia / model / native effort): architekt (zrzuty `get_screenshot`) — inna rodzina z Figma MCP niedostępna w tej sesji
- Dopuszczone alternatywy: brak (Figma MCP)
- Powód wyboru: edycja makiety wymaga Figma MCP
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook ZIELONY), 2026-10-12
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowano
- Rundy korekt: 0
- Czas do akceptacji: w obrębie fali (~1 h)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): brak; zgłoszenie do bramy — brak ramek trybu ciemnego tego ekranu w pliku makiet
- Defekty po odbiorze: brak
- Wymagane testy i dowody: zrzuty ramek przez architekta

### 2705-B1b (bramka operatora płatności dla zakupu z konta — kontrakt, implementacja, atrapa, DI) — 2026-10-12
- Archetyp: Backend — integracja z operatorem płatności
- Stawka: wysoka / high-stakes (płatność, zwrot, anulowanie subskrypcji)
- Niepewność: wysoka (zachowanie operatora przy anulowaniu i zwrocie sprawdzane sondą na koncie testowym)
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh` (dwa przebiegi: pierwszy zakończony przekazaniem przy ~301 tys., kontynuacja świeżym agentem tej samej linii)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access read`
- Dopuszczone alternatywy: wykonawca — brak (przy CZERWONYM Spark `max`); recenzent — brak bez naruszenia rezerwy puli Codexa na bramkę (reguła 7), Gemini wykluczony przy high-stakes
- Powód wyboru: twarda bramka — płatność; recenzent innej rodziny o stawce wyższej niż niska
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook ZIELONY→ŻÓŁTY); Spark nieznany (wrapper bez zapasu), 2026-10-12 przed południem
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: przekazanie przy ~301 tys. (strażnik kontekstu); kontynuacja dokończyła — zaakceptowano po walidacji (build czysty, 5572 testy, 0 pominiętych)
- Rundy korekt: 1 (P2 z recenzji jako Krok 0 briefu następnego, ta sama linia; zaakceptowany: 5576 testów)
- Czas do akceptacji: ~1,5 h z kontynuacją i recenzją; Krok 0 +~20 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): potwierdzone 3 × P2 (sekret płatności w domyślnym opisie rekordu, zbyt wąski ponowny odczyt po odmowie unieważnienia faktury, pusty identyfikator sesji przy ponownym użyciu zapisu subskrypcji — przeniesione do briefu domknięcia); P3: 1 odrzucone (klucz idempotencji unieważnienia — współbieżność wyklucza blokada konta), 1 bez poprawki (więz przyczyny porażki przepuszcza małe litery — kolumnę zapisuje wyłącznie kod ze stałych), drobiazgi bez wpływu
- Defekty po odbiorze: brak (stan na odbiór fali)
- Wymagane testy i dowody: `dotnet build`, `dotnet test` ze zmienną testów SQL (0 pominiętych), testy HTTP bramki na zapisanych odpowiedziach operatora, sonda na koncie testowym operatora (bez sekretów w logach)
- Uwaga o specyfikacji: dwa błędy briefu architekta (zbyt wąski ponowny odczyt; uproszczony opis istniejącego zapisu subskrypcji) — rundy z winy specyfikacji, nie wykonania.

### 2705-F2b (przepływ płatności zakupu z konta — serwis FE: pole karty, start, potwierdzenie, odpytywanie, sesja) — 2026-10-12
- Archetyp: Frontend — logika przepływu płatności z sesją i odpytywaniem (niezmiennik)
- Stawka: wysoka / high-stakes (płatność, sesja)
- Niepewność: wysoka (zmiana sesji w trakcie płatności, fail-closed po potwierdzeniu)
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh`
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access read`
- Dopuszczone alternatywy: wykonawca — brak (przy CZERWONYM Spark `max`); recenzent — brak bez naruszenia rezerwy puli Codexa na bramkę, Gemini wykluczony przy high-stakes
- Powód wyboru: twarda bramka — płatność i sesja; recenzent innej rodziny o stawce wyższej niż niska
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook ŻÓŁTY — Opus dozwolony dla niezmiennika); Spark nieznany, 2026-10-12 południe
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: odrzucony do poprawek (bez P0/P1; 3 × P2 w kodzie i testach)
- Rundy korekt: 3 (runda 1: 7 poprawek z recenzji; runda 2: luka tej samej klasy zgłoszona przez wykonawcę + podział specu przekraczającego limit długości; runda 3: luka zgłoszona przez wykonawcę rundy 2 — jednolinijkowa bramka potwierdzenia w toku; zaakceptowana). Runda 2 przerwana wyjściem procesu sesji i wznowiona tym samym agentem (ryzyko pozostawionej mutacji) — dokończona.
- Czas do akceptacji: ~2,5 h z trzema rundami (rundy 1–2 ~2 h, runda 3 ~20 min)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): potwierdzone 4 × P2 (nieukształtowany wynik potwierdzenia wiesza fazę wysyłania; zmiana sesji zostawia fazy oczekiwania bez wyjścia; dwie luki dowodowe w testach) i 3 × P3 (luki testów montażu i wznowienia, kolejność fokusu); odrzucone 0
- Defekty po odbiorze: nieustalone (bramka końcowa przed nami)
- Wymagane testy i dowody: spec Vitest przepływu z kontrolą mutacyjną każdej asercji na niezmienniku; pełne `npm run lint` / `format:check` / `npm test` (4521) / `npm run build` po fali
- Uwaga o specyfikacji: dwie przesłanki briefu błędne (wzorzec ścieżki istniejącego komponentu; wzorzec współdzielonego setupu testów) — wykonawcy zgłosili je w sekcji „co błędne”.
### 2705-F4 (ekran zakupu programu z konta — strona, sekcje, walidacja kolejnością ekranu, trasa, i18n) — 2026-10-12
- Archetyp: Frontend — ekran z formularzem wg wzorca istniejącego ekranu, bez makiety (decyzja właściciela: wzór w kodzie)
- Stawka: średnia (ekran funkcji high-stakes bez niezmiennika — niezmiennik płatności i sesji w osobnym serwisie przepływu)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access write`
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read`
- Dopuszczone alternatywy: wykonawca — `wykonawca` Sonnet 5.5 `high`; recenzent — brak bez naruszenia rezerwy puli Codexa na bramkę (Sol `high` byłby kandydatem)
- Powód wyboru: ekran bez Figmy i bez niezmiennika, wzorzec w kodzie; recenzent innej rodziny, preferencja Gemini przy niskiej/średniej stawce
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark i Gemini nieznany (wrapper bez zapasu), 2026-10-12 popołudnie
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: odrzucony do poprawek (bez P0/P1); wykonawca sam wskazał błąd specyfikacji (podwójny nagłówek strony)
- Rundy korekt: 1 (5 poprawek: nagłówek, warunek liczby programów, enum zamiast unii, atrybut niepoprawności pola zgody, działanie główne nieaktywne do wczytania pola karty)
- Czas do akceptacji: ~1 h 50 min (z recenzją 10 min i rundą korekty 10 min)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): potwierdzone 2 × P2 (warunek liczby programów nie łapie wartości nieliczbowej — potwierdzony testem czerwonym na starym kodzie; zamknięty zbiór jako unia typów zamiast enuma) i 2 × P3 (brak atrybutu niepoprawności na polu zgody; ciche naciśnięcie w czasie wczytywania pola karty — nowa decyzja w dokumentacji); odrzucone 1 (kolejność zgody po polu karty — zgodna z kolejnością ekranu)
- Defekty po odbiorze: brak (stan na odbiór fali)
- Wymagane testy i dowody: speci Vitest komponentów i AXE strony; pełne `npm run lint` / `format:check` / `npm test` (4528) / `npm run build`; zrzuty `browser-check` — po etapie BE
- Uwaga o specyfikacji: 2 błędy briefu architekta (własny nagłówek strony wbrew powłoce; nieistniejące użycia kluczy w jednym pliku) — zgłoszone przez wykonawcę.
### 2705-A-SCSS (audyt SCSS ekranu zakupu i sekcji ustawień — Faza 4) — 2026-10-12
- Archetyp: Audyt SCSS (tylko odczyt) — duplikacja i reguły stylów, 10 plików
- Stawka: niska (audyt bez zapisu)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access read`
- Recenzent (linia / model / native effort): architekt (triaż rekomendacji względem repo i reguł); kod nie powstał
- Dopuszczone alternatywy: Gemini `high` `-Access read`; Sol `high` wyłączony rezerwą puli Codexa na bramkę
- Powód wyboru: wcześniejszy audyt SCSS na Sparku bez pominiętego pliku; tylko odczyt
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark nieznany (wrapper bez zapasu), 2026-10-12 ok. 14:15
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowany — wszystkie 10 plików omówione
- Rundy korekt: 0
- Czas do akceptacji: ~10 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): rekomendacje — 4 przyjęte do refaktoru (dwa wspólne partiale, scalenie dwóch reguł, mixin hosta sekcji ustawień), 1 zamieniona z komponentu na mixin (decyzja architekta), 1 odłożona jako dług (atomy tekstu ekranu logowania poza obszarem)
- Defekty po odbiorze: nie dotyczy
- Wymagane testy i dowody: brak (wejście do F5-scss)
- Uwaga o specyfikacji: brak.

### 2705-F5-scss (refaktor SCSS po audycie — dwa partiale z mixinami, scalenie reguł, mixiny ustawień) — 2026-10-12
- Archetyp: Frontend — refaktor SCSS z wyrocznią identyczności skompilowanego CSS (11 plików)
- Stawka: niska (style bez niezmiennika; wygląd chroniony wyrocznią)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Claude / `wykonawca` — Sonnet 5.5 / `high` (ponowna kwalifikacja: pierwszy przydział Spark `max` padł na pierwszym wywołaniu modelu komunikatem 429 „Subscription quota exhausted” — pierwszy limit puli Sparka w rejestrze)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read`
- Dopuszczone alternatywy: wykonawca — Gemini `high` `-Access write` (recenzent musiałby czekać na reset Sparka; Codex ≤ 5 plików w funkcji high-stakes); recenzent — Spark po resecie
- Powód wyboru: Spark zablokowany do 14:27Z; pula Claude'a zielona; autor Claude pozwala na natychmiastową recenzję Gemini
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark zablokowany (wrapper 429, reset 14:27Z), Claude znany (hook ZIELONY 7 %), Gemini nieznany — 2026-10-12 12:23Z
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany po walidacji (wyrocznia 10 × OK, stylelint i Prettier czyste); 2 odchylenia od briefu zgłoszone przez wykonawcę i słuszne (parametr mixinu, wycofany punkt bez identycznych deklaracji)
- Rundy korekt: 1 (4 poprawki z recenzji: drugi konsument mixinu szerokości przycisku, komentarz konsumentów, domyślna wartość parametru, nagłówek sekcji na ekranie publicznym) — przez wznowienie tego samego agenta (152 tys. kontekstu)
- Czas do akceptacji: ~25 min (z recenzją ~9 min)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): potwierdzone 1 × P2, 3 × P3; odrzucone 0; 1 propozycja zmiany komponentu sekcji ustawień odłożona jako dług (dotyka 12 użyć)
- Defekty po odbiorze: brak (stan na odbiór fali)
- Wymagane testy i dowody: wyrocznia sass (znormalizowane reguły przed/po, 11 plików), stylelint, Prettier; pełne `npm run lint` / `format:check` / `npm test` (4528) / `npm run build` po fali
- Uwaga o specyfikacji: 1 błąd briefu (parametr mixinu z samym dolnym marginesem nie daje identycznego CSS) — wykonawca naprawił i zgłosił.
### 2705-B2 (start zakupu z konta — oferta, walidator, handler pod blokadą konta, kontroler, testy) — 2026-10-12
- Archetyp: Backend — przypadek użycia z płatnością (CQRS + kontroler)
- Stawka: wysoka / high-stakes (płatność, start subskrypcji, warunki nadania roli właściciela)
- Niepewność: wysoka (ponowne kliknięcie przy istniejącej próbie, stany płatności po stronie operatora)
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh` (trzy przebiegi: STOP na błędzie briefu po Kroku 0; świeży przebieg zakończony przekazaniem przy ~300 tys.; wznowienie tego przebiegu przez SendMessage od razu przekroczyło 305 tys. bez żadnej zmiany; świeży przebieg z briefem i dosłownym przekazaniem dokończył)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access read` (po pierwszym limicie puli Sparka recenzja ruszyła po resecie 14:28Z; 13,5 min)
- Dopuszczone alternatywy: wykonawca — brak (przy CZERWONYM Spark `max`); recenzent — brak bez naruszenia rezerwy puli Codexa na bramkę (reguła 7), Gemini wykluczony przy high-stakes; przy limicie Sparka recenzja czeka, zależna fala B3a czeka na nią
- Powód wyboru: twarda bramka — płatność; recenzent innej rodziny o stawce wyższej niż niska
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook); Spark zablokowany (429 wrappera, 2026-10-12 ok. 12:30Z, reset 14:27Z)
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: STOP — wykonawca słusznie zakwestionował przepisane w briefie brzmienie zgody (tekst zakupu publicznego zamiast zgody cyklicznej z konta); Krok 0 (poprawki po recenzji B1b) zaakceptowany
- Rundy korekt: 0 z wykonania; przebiegi dodatkowe z winy specyfikacji (1) i kosztu kontekstu (wznowienie zamiast świeżego agenta); po zaakceptowaniu: build czysty, 5691 testów, 0 pominiętych
- Czas do akceptacji: ~1,5 h od pierwszego przebiegu (11:00Z) do odbioru, bez recenzji
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): werdykt „poprawny”, pewność 0,85, 0 × P0–P2; 3 × P3 potwierdzone (jawny `null` zamówienia/nabywcy daje 500 zamiast 400; rozjazd wielkości liter języka zgoda↔produkt operatora; klient usunięty ręcznie u operatora blokuje zakup konta — dług); 1 uwaga wykonawcy obalona (brak śladu 503 — middleware loguje każde 5xx). Dwa pierwsze P3 + własne znaleziska architekta (język pl/en, kod odmowy operatora w logu) jako Krok 0 briefu B3a, ta sama linia
- Defekty po odbiorze: brak (stan na odbiór fali)
- Wymagane testy i dowody: `dotnet build`, `dotnet test` ze zmienną testów SQL (0 pominiętych), testy jednostkowe handlera z prawdziwym resolverem klucza i starterem na atrapie operatora, test kontraktu JSON kontrolera
- Uwaga o specyfikacji: 1 błąd briefu (brzmienie zgody); lekcja kosztu — wznowienie przerwanego agenta z dużym kontekstem kończy się natychmiastowym przekazaniem, kontynuacja zawsze świeżym agentem (reguła 15).
### 2372-QAS (przypadki QA Sphere — sekcja „Własny program”, 8 przypadków) — 2026-10-12
- Archetyp: QA Sphere — autor przypadków manualnych (plik podglądu wg skilla v1.6)
- Stawka: niska (ekran bez niezmiennika; przypadki manualne, wysyłka skryptem po bramie użytkownika)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / `-Access write` (Spark — linia domyślna autora — z pierwszym limitem puli)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access read` (plik Gemini → Spark, wg skilla; po resecie puli)
- Dopuszczone alternatywy: autor — Spark `max` (limit do 14:27Z); recenzent — brak innej rodziny wg procedury skilla (Gemini nie recenzuje Gemini)
- Powód wyboru: procedura skilla QA Sphere (Spark autor, Gemini przy limicie Sparka; recenzja krzyżowa)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark zablokowany (429, 12:25Z → reset 14:27Z); Gemini nieznany (wrapper bez zapasu), 12:43Z
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: lint 0 błędów; 8 przypadków (2 high, 2 medium, 4 low), `updates[]` puste po sprawdzeniu ZEB-980/881/882/951/979
- Rundy korekt: 2 — runda 1 po recenzji (2 × P2, 3 × P3), runda 2 z kontroli architekta (kolejność kroków warunków wstępnych A5/A6 — sekcja języka i motywu jest na otwieranej dopiero stronie)
- Czas do akceptacji: ~2,5 h zegarowo, w tym ~1,5 h oczekiwania na reset puli Sparka (autor 9,5 min, recenzja 8,7 min, korekty 4,9 i 4,4 min)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 2 × P1 obalone przez architekta (hasło `klient.demo` zmierzone logowaniem i obecne w opublikowanych przypadkach — seed celowo go nie zapisuje; puste `updates[]` potwierdzone odczytem ZEB-980/881 — `context.json` nie niesie treści przypadków); potwierdzone 2 × P2 (fałszywe pokrycie „persystencja”, trwała zmiana języka/motywu bez przywrócenia), 3 × P3 (nieprawdziwe uzasadnienie i nieistniejący endpoint w A7, nazwa tokenu zamiast obserwacji w A6)
- Defekty po odbiorze: brak (`qas.py verify` 8/8, różnic 0; ZEB-1581…1588, folder 166)
- Wymagane testy i dowody: `qas.py lint --context` (0/0), tabela na bramie użytkownika, `qas.py folders` → `push --limit 1` → `verify --only` → `push` → `verify`
- Uwaga o specyfikacji: 2 błędy briefu architekta — „hasła wyłącznie z seedów” (niespełnialne dla `klient.demo`) i „sprawdź treść w `context.json`” (plik niesie tylko tytuły; autor sięgnął po MCP sam); lekcja: brief autora i recenzenta ma wskazywać źródło hasła spoza seeda i dołączać treść przypadków do sprawdzenia albo kazać ją pobrać `get_test_case`.
### 2705-B3a (domknięcie zakupu z konta — orkiestrator, zapis w jednej transakcji, procesor `invoice.paid`, siatka) — 2026-10-12
- Archetyp: Backend — domknięcie płatności (orkiestrator + procesor webhooka)
- Stawka: wysoka / high-stakes (nadanie roli właściciela, zapis subskrypcji i płatności, zwrot przy konflikcie)
- Niepewność: wysoka (trzy wejścia domknięcia, brak ponowienia webhooka, stany operatora)
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh` (trzy przebiegi: Krok 0 zakończony przekazaniem przy ~300 tys. po jednym kroku; B3a-1 orkiestrator; B3a-2 procesor — oba świeże, z plikiem przekazania)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access read` (12,3 min)
- Dopuszczone alternatywy: wykonawca — brak (przy CZERWONYM Spark `max`); recenzent — brak bez naruszenia rezerwy puli Codexa (reguła 7), Gemini wykluczony przy high-stakes
- Powód wyboru: twarda bramka — płatność i rola; recenzent innej rodziny o stawce wysokiej
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook, ZIELONY 31–38 % okna); Spark nieznany (bez komunikatu limitu od resetu 14:27Z), 15:35Z
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: B3a-1 i B3a-2 zaakceptowane bez korekty z wykonania (5735 → 5759 testów, 0 pominiętych); wykonawca B3a-2 sam wskazał lukę: anulowane żądanie webhooka w siatce gubi zwrot bez alarmu
- Rundy korekt: 1 wspólna z B3b (B3-fix, `wykonawca-opus` `xhigh`, świeży przebieg, 17 min, 322 tys. kontekstu — próg miękki przekroczony przy mutacjach, dokończony bez przekazania): 9 punktów (P1–P9) przyjętych za pierwszym razem, 5885 testów, 0 pominiętych, każda poprawka z mutacją; architekt dopisał sam 1 zdanie komentarza handlera i 1 zdanie dokumentacji INT pkt 9 (uwagi wykonawcy). Bez osobnej recenzji poprawek — gałęzie przeczytane przez architekta, cały diff idzie do bramki Sol `max`
- Czas do akceptacji: B3a-1 ~25 min, B3a-2 ~16 min, recenzja 12 min, B3-fix 17 min + walidacja ~10 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 × P0/P1; 1 × P2 potwierdzone (zwrot w konflikcie nieprzyjęty → subskrypcja `canceled` → kolejne domknięcia `NotPaid`, zwrot nigdy nie ponowiony); 3 × P3 potwierdzone (brakujące testy kolejności i ścieżki `ABANDONED`; strażnik pustego `InvoiceId`; warunki przejęcia przez B3b — już w briefie B3b); 2 uwagi wykonawcy przyjęte jako poprawki (token żądania w siatce; zdarzenia poza zakresem jako przetworzone)
- Defekty po odbiorze: brak (stan na odbiór fali)
- Wymagane testy i dowody: `dotnet build`, `dotnet test` ze zmienną testów SQL (0 pominiętych), testy jednostkowe orkiestratora i procesora z mutacją, test SQL dwóch domknięć z konta
- Uwaga o specyfikacji: 5 błędów przesłanek briefu B3a-completion obalonych przez wykonawców (ponowienie webhooka mimo deduplikacji; null → 500 zamiast 400; testy persistera nie istniały; położenie `MessageLanguageCodes`; typ `BillingIntervalId`) i 2 w B3a-2 („przetworzone jak `default`” — `default` niczego nie oznacza; siatka jako użytkownik blokady konta — siatka konta nie zna); lekcja: przesłanki o mechanice istniejącego kodu (ponowienia, oznaczanie zdarzeń) sprawdzać odczytem przed briefem.
### 2705-B3b (status zakupu z odczytem u operatora, cykl uzgadniający i retencja prób) — 2026-10-12
- Archetyp: Backend — zapytanie z domknięciem + usługa cykliczna w tle
- Stawka: wysoka / high-stakes (status steruje ponowną płatnością na froncie; cykl jest jedynym ponowieniem domknięcia; porzucanie i anulowanie subskrypcji)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh` (jeden przebieg, 300 tys. kontekstu na granicy progu)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access read` (14,8 min)
- Dopuszczone alternatywy: jak 2705-B3a
- Powód wyboru: twarda bramka — płatność; recenzent innej rodziny o stawce wysokiej
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook, ZIELONY 38–40 % okna); Spark nieznany, 15:54Z
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany bez korekty z wykonania (5857 testów, 0 pominiętych; mutacje blokady potwierdzone przez wykonawcę); 3 uwagi wykonawcy przyjęte jako poprawki (eskalacja zawieszonej próby po 24 h; `incomplete` + PaymentIntent `canceled` → `PAYMENT_REQUIRED`; opis blokady konta) + 1 własna architekta (obiekt `StripeException` w dzienniku statusu i cyklu)
- Rundy korekt: wspólna B3-fix (wpis 2705-B3a) — przyjęta za pierwszym razem
- Czas do akceptacji: ~17 min wykonania + 15 min recenzji + wspólna B3-fix 17 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 × P0/P1/P2; 1 × P3 zapisane jako dług (odpytywanie statusu bez ograniczenia częstotliwości — blokada konta szereguje, ryzyko teoretyczne); 3 doprecyzowania briefu (limit blokady 25 s, nie 30 s; `Active` = „nie anulowano”; `canceled` dla anulowania przy starcie)
- Defekty po odbiorze: brak (stan na odbiór fali)
- Wymagane testy i dowody: `dotnet build`, `dotnet test` ze zmienną testów SQL, test kontraktu JSON statusu, testy cyklu ze stanem blokady przy każdym wywołaniu domknięcia
- Uwaga o specyfikacji: brief nie przewidział eskalacji próby, która trwale rzuca wyjątkiem (uwaga wykonawcy); kontrakt `PAYMENT_REQUIRED` niejednoznaczny dla `incomplete` + PaymentIntent `canceled`. Brief B3-fix: obietnica „każde ponowienie zwrotu działa” była zbyt mocna — stały klucz idempotencji zwrotu daje przez dobę tę samą odpowiedź operatora (uwaga wykonawcy, dokumentacja doprecyzowana).
### 2705-BT-1 (testy API zakupu z konta — prawdziwy host HTTP, prawdziwa baza, atrapa operatora) — 2026-10-12
- Archetyp: Testy — xunit integracyjne BE (host + SQL + atrapa bramki)
- Stawka: wysoka / high-stakes (dowód kontraktu, autoryzacji, transakcji i blokady zakupu; pliki testów bez niezmiennika produkcji)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Claude / `tester` — Sonnet 5.5 / `medium` (ramię A próby testera, reguła 14); korekta — świeży `tester`
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access read` (9,8 min; stała kontrola próby)
- Dopuszczone alternatywy: w próbie brak (ramię wybrane przed briefem)
- Powód wyboru: próba testera — pierwszy brief testów linii Claude'a w dzienniku
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook, ZIELONY 45–50 % okna); Spark nieznany, 16:30Z
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: 7 scenariuszy (10 testów), zielone, mutacje 3/5/7 czerwone; scenariusz 8 słusznie pominięty (pokryty kontraktami); 0 defektów produkcji
- Rundy korekt: 1 (3 × P2 fałszywej zieleni + 4 × P3 z recenzji); korekta przyjęta za pierwszym razem, 1 przesłanka briefu korekty obalona przez wykonawcę (`UnitAmountMinor` to cena jednostkowa)
- Czas do akceptacji: 7,7 min + recenzja 9,8 min + korekta 4,7 min + walidacja
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 × P0/P1; 3 × P2 potwierdzone (drugi `GET` po `COMPLETED` nie pilnował braku odczytu u operatora; tolerancja czasu zgody ±10 ms; scenariusz 4 nie sprawdzał warunków nowej próby i żądania do operatora); 4 × P3 potwierdzone (zera w scenariuszu 6; token z rolą Owner w scenariuszu 1; magiczna liczba; realizm atrapy); 1 twierdzenie recenzenta odrzucone (zaokrąglenie `datetime` „tylko w dół” — idzie w obie strony)
- Defekty po odbiorze: brak
- Wymagane testy i dowody: `dotnet build`, `dotnet test` z SQL (5895, 0 pominiętych), filtr funkcji 430, mutacje po korekcie (poprawki 1 i 3)
- Uwaga o specyfikacji: brief scenariusza 5 żądał „bez nowych wywołań zapisu” zamiast „bez wywołań w ogóle” — słabsze kryterium architekta przeniosło się do testu; koszt próby: 2,65 $ (1,82 + 0,83).
### 2705-REPRO (odtworzenie zakupu z konta na testowym koncie Stripe — przeglądarka, Playwright CLI) — 2026-10-12
- Archetyp: Przeglądarka — ręczne odtworzenie przepływu płatności (worker CLI)
- Stawka: wysoka (dowód płatności i nadania roli na prawdziwym operatorze w trybie testowym; worker tylko klika, bez kodu)
- Niepewność: średnia (ramka Stripe, prawdziwe webhooki lokalnie)
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access write` (powłoka dla `pwcli`; katalog roboczy pusty w scratchpadzie), 4,6 min
- Recenzent (linia / model / native effort): architekt — zrzuty PNG, log BE, log `stripe listen`, stan bazy (dowód, nie recenzja kodu)
- Dopuszczone alternatywy: Gemini/Codex tylko z Playwright MCP (CLI u nich nie działa) — droższe w tokenach; Claude bez zrzutów (reguła 15)
- Powód wyboru: jedyna linia z Playwright CLI
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark nieznany (bez komunikatu limitu od odnowienia), 16:34Z
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: PASS obu przejść (A: karta odrzucana → komunikat, brak roli; B: odrzucenie → ponowienie 4242 bez przeładowania → `/panel/biznes/pulpit` z nakładką); 31 wywołań powłoki, 68 poleceń CLI, 0 pełnych snapshotów; webhook `invoice.paid` i odczyt statusu domknęły tę samą próbę w tej samej sekundzie — w bazie po 1 subskrypcji, płatności, fakturze i zgodzie
- Rundy korekt: 0
- Czas do akceptacji: 4,6 min + weryfikacja architekta
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): uwaga UX P3 — powód odrzucenia widoczny dwa razy (w elemencie Stripe i pod polem karty — drugie wymagane dokumentacją)
- Defekty po odbiorze: brak
- Wymagane testy i dowody: zrzuty 3 PNG obejrzane, log BE, log `stripe listen` (200), zapytanie SQL obu kont
- Uwaga o specyfikacji: 3 drobne błędy briefu zgłoszone przez workera (angielski przykład tytułu ramki; `getByLabel('Hasło')` niejednoznaczne; nie każde polecenie CLI wypisuje adres) — wiedza zapisana w pamięci `zebrani-stripe-konto-testowe`.
### 2705-BT-2 (testy SQL domknięcia zakupu z konta — wyścig wejść, duplikat ze zwrotem, zwrot nieprzyjęty, siatka webhooka, retencja) — 2026-10-12
- Archetyp: Testy — xunit integracyjne BE (prawdziwy SQL, prawdziwa blokada `sp_getapplock`, atrapa bramki)
- Stawka: wysoka / high-stakes (dowód niezmiennika „nigdy dwie subskrypcje” i zwrotu przy konflikcie; pliki testów bez niezmiennika produkcji)
- Niepewność: średnia (współbieżność na prawdziwej bazie)
- Wykonawca (linia / model / native effort): Claude / `tester-haiku` — Haiku 5.5 / `xhigh` (ramię B próby testera, reguła 14); korekta — świeży `tester-haiku`, 10,2 min
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access read` (stała kontrola próby)
- Dopuszczone alternatywy: w próbie brak (ramię wybrane przed briefem)
- Powód wyboru: próba testera — drugi brief, naprzemiennie po BT-1 (ramię A)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook, ZIELONY); Spark znany po odnowieniu limitu (komunikat użytkownika), 17:00Z
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: 5 scenariuszy na SQL, zielone; wyścig 3 × 3 wejścia na świeżych kontach; 0 defektów produkcji; jeden plik istniejący zmieniony bez zgłoszenia (wyciągnięcie pomocnika z `AccountProgramPurchaseCompletionSqlTests.cs`)
- Rundy korekt: 1 (3 × P2 + 8 × P3 z recenzji); korekta przyjęta za pierwszym razem — wymieniła każdy zmieniony plik, mutacje czerwone (4 zamiast 3 wpisów `Completed`; `ABANDONED` zamiast `PENDING`), wyścig 3 × zielony
- Czas do akceptacji: 1. przebieg + recenzja + korekta 10,2 min + walidacja architekta
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 × P0/P1; 3 × P2 potwierdzone (kontrola 11 min retencji nie sprawdzała stanu końcowego — regresja „porzucaj każdą nieopłaconą” przeszłaby; wyścig bez dowodu, że każdy webhook doszedł do domknięcia; siatka webhooka bez stanu bazy); 8 × P3 potwierdzone (m.in. dwa `Task.WhenAll`, `UpdatedAt` 71 h, wszystkie metody atrapy, brak `Critical` w duplikacie, liczba subskrypcji w scenariuszu 3, magiczna liczba, awans pomocników do `Support/`, komentarz o wspólnej bazie klasy)
- Defekty po odbiorze: brak; dług P3 — zapytanie o liczbę subskrypcji konta zdublowane w dwóch klasach testów (brief korekty zakazał zmian treści pomocników)
- Wymagane testy i dowody: `dotnet build`, `dotnet test` z SQL (5903, 0 pominiętych), filtr funkcji 438, wyścig 3 ×, mutacje poprawek 1 i 3
- Uwaga o specyfikacji: 3 przesłanki briefu korekty doprecyzowane przez wykonawcę (magiczna liczba także w pliku „tylko `using`”; „wszystkie metody atrapy” = wywołania cyklu, bo zakładanie klienta i subskrypcji w przygotowaniu nosi `purchaseRef`; dziennik bez właściwości strukturalnych); koszt próby: 1,92 $ (1,18 + 0,74).
### 2705-GATE-FE (bramka końcowa FE — cały diff funkcji zakupu z konta i sekcji „Własny program”) — 2026-10-12
- Archetyp: Recenzja — bramka końcowa high-stakes (reguła 6)
- Stawka: wysoka / high-stakes (płatność, sesja, nadanie roli)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): n/d (recenzja)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `max`, `-Mode review` (tylko odczyt), jeden przebieg na całym diffie FE, ~30 min
- Dopuszczone alternatywy: brak (bramka bez obniżenia modelu i effortu)
- Powód wyboru: reguła 6 — inna rodzina niż autor plików niezmiennika (`wykonawca-opus`)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper nie podaje zapasu; bez komunikatu limitu), 16:35Z
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: werdykt „niepoprawny” — 2 × P1 + 5 × P2
- Rundy korekt: 2 (GFE-fix, `wykonawca-opus`, 7,48 $; 6/6 poprawek z mutacją czerwoną, 2 przesłanki briefu obalone: blokada przechodzi do PrimeNG przez `[formField]` bez zmian w komponentach wspólnych; synchroniczne drugie `refresh()` dołączyłoby do starego żądania — potrzebny przeskok mikrozadania; recenzja fali korekty Spark `max` read 12,5 min — werdykt „niepoprawny” 0,9: P0 „wypełnienie profilem starego konta” obalone w źródłach Angulara 22.1.5 (`httpResource` zeruje wartość synchronicznie przy zmianie klucza), P2 „telefon konta A” obalone tak samo, 2 × P1 obniżone do P2 i potwierdzone (stany terminalne i komunikat odmowy poprzedniego konta po zmianie sesji), P2 REGON w blokadzie → dług P3, P3 testu blokady potwierdzone; GFE-fix-2 `wykonawca-opus` 3,75 $, 3 mutacje czerwone, delta przyjęta bez kolejnej recenzji)
- Czas do akceptacji: bramka ~30 min + triaż + korekta + walidacja (lint, format, 4546 testów, build) + recenzja fali korekty
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 2 × P1 potwierdzone (sekret PaymentIntentu w adresie powrotu po logowaniu; dane, zgoda i karta konta A zostają po zmianie konta na B); 4 × P2 potwierdzone i naprawione (nawigacja po `COMPLETED` bez roli właściciela; budżet 60 s nieegzekwowany przy wiszącym żądaniu; przełącznik okresu PrimeNG zmienia się Spacją mimo blokady; wstępne wypełnienie nadpisuje pole w trakcie pisania); 1 × P2 przyjęte jako dług (powrót z pełnego przekierowania 3DS nie odtwarza zamówienia — pole tylko karta, `redirect: 'if_required'`); żadnego z nich nie znalazła wcześniejsza recenzja fal Sparka
- Defekty po odbiorze: brak; dług P3 — odpowiedź REGON w locie wpisuje dane firmy do zablokowanego formularza (komponenty wspólne z `/kup`)
- Wymagane testy i dowody: triaż każdego znaleziska w kodzie; po każdej korekcie pełne `npm run lint`, `format:check`, `npm test` (4546 → 4549), `npm run build`
- Uwaga o specyfikacji: brak.
### 2705-GATE-BE (bramka końcowa BE — cały diff funkcji zakupu z konta) — 2026-10-12
- Archetyp: Recenzja — bramka końcowa high-stakes (reguła 6)
- Stawka: wysoka / high-stakes (płatność, zwrot, nadanie roli, migracja)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): n/d (recenzja)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `max`, `-Mode review` (tylko odczyt), jeden przebieg na całym diffie BE, 12,7 min
- Dopuszczone alternatywy: brak (bramka bez obniżenia modelu i effortu)
- Powód wyboru: reguła 6 — inna rodzina niż autor plików niezmiennika (`wykonawca-opus`)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (bez komunikatu limitu po bramce FE), 17:39Z
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: werdykt „niepoprawny” — 4 × P2, 0 × P0/P1; weryfikacja statyczna (testów nie uruchamiała)
- Rundy korekt: 1 (GBE-fix, `wykonawca-opus`, 6,20 $, 15,8 min; 14 mutacji czerwonych, migracja wykonana dwukrotnie na świeżej bazie — oryginał pada Msg 1781, poprawiona przechodzi; 1 przesłanka briefu obalona: deduplikacja webhooka nie przetwarza zdarzenia ponownie, więc skasowana próba kończy się alarmem do ręcznej obsługi, nie siatką zwrotu; recenzja fali korekty Spark `max` read 7,9 min — werdykt „poprawny” 0,8, 1 × P2 potwierdzone (teksty alarmu `RefundPending` w webhooku i cyklu opisywały tylko konflikt ze zwrotem — poprawione przez `mechanik`), 1 × P3 dług (gałąź „subskrypcja już zapisana” ignoruje wynik — nieosiągalna))
- Czas do akceptacji: bramka 12,7 min + triaż + korekta + walidacja + recenzja fali korekty
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 2 × P2 potwierdzone (wynik warunkowego zapisu domknięcia ignorowany → `Completed` bez zapisów, gdy retencja skasuje próbę w trakcie odczytu u operatora; surowy wyjątek operatora w dzienniku awaryjnego anulowania startera); 2 × P2 obniżone do P3 i poprawione tanio (domknięcie i zwrot na `latest_invoice` zamiast pierwszej faktury — wymaga opóźnienia o cały okres; migracja bez osłon `ADD CONSTRAINT` — zgodna z konwencją Script000004/000015, ale DbUp bez transakcji); żadnego z nich nie znalazły recenzje fal Sparka
- Defekty po odbiorze: brak; długi P3 — gałąź „subskrypcja już zapisana” bez sprawdzenia wyniku; próba `ABANDONED` z fakturą nie-pierwszą bez alarmu cyklu; siatka webhooka zwraca `latest_invoice` bez sprawdzenia pierwszej faktury (uruchamia się tylko przy doręczeniu pierwszej)
- Wymagane testy i dowody: build 0 ostrzeżeń, pełny pakiet 5903 → 5917 (0 pominiętych); triaż każdego znaleziska w kodzie (DbUp bez `WithTransaction`, `_ = await writer.WriteAsync`, `LogError(exception, …)`)
- Uwaga o specyfikacji: brief bramki żądał „skrypt idempotentny wg konwencji repo” — konwencja sama ma tę lukę; bramka słusznie oceniła skutek, nie zgodność z konwencją.
### 2705-DOC4C-BE (Faza 4c — zgodność dokumentacji z implementacją, grupa BE: płatności, dane) — 2026-10-12
- Archetyp: Recenzja — przegląd zgodności dokumentacji (Faza 4c)
- Stawka: wysoka (dokumenty feature'a high-stakes: INT-PLATNOSCI-CYKLICZNE, WP-USUWANIE-KONTA-I-DANYCH)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): n/d (recenzja)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access read`, 685,8 s
- Dopuszczone alternatywy: Codex `gpt-6.1-sol` `high` odłożony (pula Plusa po dwóch bramkach, sygnał nieznany); Gemini wykluczony (stawka high-stakes)
- Powód wyboru: inna rodzina niż autor dokumentacji (architekt, Claude); zakres całej grupy dokumentów z całym kodem BE w jednym przebiegu
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark nieznany (działa po resecie limitu z ~12:25Z), 18:00Z
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: macierz kompletna — 0 × „kod odbiega”, 0 × „dokument nieaktualny”, 9 × „brak w dokumencie”, każdy z `plik:linia`
- Rundy korekt: 0 (triaż i rewizje dokumentów — architekt)
- Czas do akceptacji: przebieg 11,4 min + triaż
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 9/9 potwierdzone w kodzie (produkt operatora per język; „to samo zamówienie” z ceną i językiem; konflikt przy samej roli; zakres `invoice.paid`; tylko pierwsza faktura; CAS bez zmiany; kontrakt API; skład próby z IP/UA; opłata w chwili anulowania) → rewizje INT pkt 1, 3–6, 9, 10 i WP pkt 1; 0 fałszywych alarmów
- Defekty po odbiorze: brak
- Wymagane testy i dowody: każdy wiersz rozbieżności sprawdzony przez architekta w kodzie przed rewizją
- Uwaga o specyfikacji: brief niósł kryteria akceptacji #2372 (szum dla grupy BE) i numerację dziennika z lukami — recenzent słusznie wskazał oba

### 2705-DOC4C-FE (Faza 4c — zgodność dokumentacji z implementacją, grupa FE: ekrany) — 2026-10-12
- Archetyp: Recenzja — przegląd zgodności dokumentacji (Faza 4c)
- Stawka: wysoka (UI-KONTO-ZAKUP-PROGRAMU feature'a high-stakes, UI-KONTO-USTAWIENIA)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): n/d (recenzja)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access read`, 1197,1 s
- Dopuszczone alternatywy: jak 2705-DOC4C-BE
- Powód wyboru: jak 2705-DOC4C-BE; dwa przebiegi równolegle na rozłącznych grupach dokumentów
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark nieznany, 18:04Z
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: 1 × „dokument nieaktualny”, 10 × „brak w dokumencie”, 0 × „kod odbiega”/„brak w kodzie”; liczby `zgodne` per sekcja (ponad 100 twierdzeń); raport częściowo przemieszany w logu wrappera (znana kolejność linii), treść kompletna
- Rundy korekt: 0 (triaż i rewizje dokumentów — architekt)
- Czas do akceptacji: przebieg 20 min + triaż
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 11/11 potwierdzone; najcenniejsze — zdanie z rewizji tego zadania („strona nie wyświetla się właścicielowi ani na chwilę”) przeczyło zatwierdzonej DEC-PIERWSZY-RENDER-POWLOKI (serwer nie zna ról) — skorygowane; sekret płatności w adresie powrotu nieopisany (także sekret SetupIntentu z PBI #1759) → rewizja DEC-ADRES-POWROTU-PO-ZALOGOWANIU; 6 uwag do briefu, wszystkie trafne (opis PBI #2372 w ADO nieaktualny, zła ścieżka w briefie, dwuznaczne zdanie dokumentu)
- Defekty po odbiorze: brak
- Wymagane testy i dowody: każdy wiersz rozbieżności sprawdzony przez architekta w kodzie przed rewizją; kontrola linków w 5 zmienionych dokumentach — 0 złych
- Uwaga o specyfikacji: brief podawał nieistniejącą ścieżkę komponentu sekcji „Abonament i faktury”

### 2705-REPRO-2 (ponowne odtworzenie zakupu z konta na testowym Stripe po poprawkach bramki FE) — 2026-10-12
- Archetyp: Weryfikacja w przeglądarce — worker przeglądarkowy (Playwright CLI), ścieżka płatności
- Stawka: wysoka (płatność, nadanie roli) — odczyt i jedna płatność testowa, bez zmian w kodzie
- Niepewność: niska
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access write` (powłoka dla Playwright CLI), 244 s
- Recenzent (linia / model / native effort): n/d — architekt odbiera artefakty (zrzut, baza, log `stripe listen`)
- Dopuszczone alternatywy: Codex z Playwright MCP (droższy w kontekście, pula zarezerwowana dla bramek); Gemini wykluczony (CLI nie działa, stawka)
- Powód wyboru: Playwright CLI działa dziś tylko w linii Spark; poprzedni przebieg na tym briefie — 0 rund
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark nieznany, działa od resetu ~12:25Z, 18:40Z
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: PASS — konto po odmowie karty sprzed 2 h: to samo zamówienie → ta sama próba (`PENDING` z 16:35Z domknięta 18:42Z), blokada formularza w trakcie płatności (wszystkie pola `disabled`), przejście na `/panel/biznes/pulpit` z nakładką po ~15 s; 22 wywołania powłoki, 45 poleceń CLI, 0 pełnych snapshotów
- Rundy korekt: 0
- Czas do akceptacji: 4 min + odbiór
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): n/d; obserwacja — pigułka „stripe” na pulpicie to asystent trybu testowego Stripe.js (tylko tryb testowy)
- Defekty po odbiorze: brak
- Wymagane testy i dowody: zrzut obejrzany, zapytanie SQL (rola 1,2; 1 subskrypcja, 1 płatność, 1 zgoda, profil rozliczeniowy), `invoice.paid` w logu `stripe listen`
- Uwaga o specyfikacji: nazwy pól ramki Stripe zmieniają się po wypełnieniu (`Data ważności (MM/RR)`) — brief powinien kazać ponowić `find` zamiast ufać starym refom

### 2705-QAS (przypadki QA Sphere — zakup programu z konta, 33 przypadki w 4 folderach) — 2026-10-12
- Archetyp: QA Sphere — autor przypadków manualnych (plik podglądu wg skilla v1.6)
- Stawka: średnia (przypadki manualne funkcji płatności; wysyłka skryptem po bramie użytkownika, bez zmian w kodzie)
- Niepewność: średnia (atrapa operatora na pre-prod, przypadki płatności zależne od klucza testowego Stripe, zachowanie między kartami)
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access write`
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (plik Sparka → Gemini, wg skilla)
- Dopuszczone alternatywy: autor — Gemini `-Access write` (linia zapasowa skilla); recenzent — brak innej rodziny wg procedury skilla (Spark nie recenzuje Sparka, Codex zarezerwowany dla bramek)
- Powód wyboru: procedura skilla QA Sphere v1.6 (Spark `max` autor, recenzja krzyżowa Gemini)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark nieznany (wrapper bez zapasu, bez komunikatu limitu), Gemini nieznany, 19:19Z
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: lint 0 błędów; 32 przypadki (W1–W8, F1–F9, P1–P11, V1–V4), `updates[]` puste po odczycie ZEB-1581/980/184/221/248; autor obalił dwie przesłanki briefu (próg liczby błędów przy 60 s, wylogowanie w innej karcie jako przypadek)
- Rundy korekt: 3 — runda 1 po recenzji i kontroli architekta (V4, W1/W2 wobec atrapy, nowy P12 — zmiana konta w innej karcie, F5 osoba prywatna, V3 zaślepka `{kwota}`), runda 2 z kontroli architekta (odłożenie kreatora po zakupie w P2/P7/P8/P12), runda 3 z luki zgłoszonej przez autora (P8 krok 3 — kreator nad komunikatem „Już właściciel”)
- Czas do akceptacji: ~1 h zegarowo (autor 15,3 min, recenzja 1 min nieudana + 13 min, korekty 7,2 / 4,0 / 1,7 min)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): zgłoszone 2 × P1 — oba potwierdzone po obniżeniu do P2 (V4: zdanie o ramce operatora niewykonalne na pre-prod; luka: zmiana konta w innej karcie osiągalna przez odświeżenie sesji po zakupie); potwierdzone 1 × P2 (W1/W2 „brak komunikatów” wobec atrapy) i 1 × P3 (F5 bez typu „Osoba prywatna”). Raport recenzenta zawierał zmyślone fakty w części potwierdzającej (trasy `/konto/zakup-programu`, `/panel/program/nowy`, klucze folderów, konto `wlasciciel.demo`, PESEL, cytat komunikatu) — architekt przeliczył napisy mechanicznie (wszystkie cytaty w przypadkach wobec `pl.json`/`en.json`, kwoty wobec `pricing-constants.ts`), zamiast polegać na tym potwierdzeniu
- Defekty po odbiorze: brak (`qas.py verify` 33/33, różnic 0; ZEB-1589…1621, foldery 168–171)
- Wymagane testy i dowody: `qas.py lint --context` (0 błędów, 8 uwag o wzorcu numeru świeżego konta), mechaniczne sprawdzenie cytatów wobec `pl.json`/`en.json`, diff wersji pliku po każdej korekcie (zmiany tylko w wskazanych krokach), tabela na bramie użytkownika, `qas.py folders` → `push --limit 1` → `verify --only` → `push` → `verify`
- Uwaga o specyfikacji: pierwszy przebieg recenzji Gemini skończył się bez raportu — brief wskazywał katalog zamiast plików, a recenzent bez powłoki sięgnął po `Get-ChildItem` (odmowa uprawnień); lekcja: brief recenzenta `-Access read` wymienia pliki ścieżkami bezwzględnymi. Błędy briefu autora zgłoszone przez autora: „po ilu błędach” (kod nie ma progu błędów, tylko budżet 60 s), przypadek wylogowania w innej karcie bez płatności (niewykonalny — karta dowiaduje się o zmianie konta dopiero przy swoim odświeżeniu sesji); brief korekty 1 przypisał W2 frazę, której tam nie było.

### 2705-QAS-2 (korekta 19 przypadków QA Sphere — pre-prod na Stripe w trybie testowym, z weryfikacją na żywo) — 2026-10-12
- Archetyp: QA Sphere — poprawki istniejących przypadków (`updates[]`) z weryfikacją faktów w przeglądarce (Playwright CLI)
- Stawka: średnia (przypadki manualne funkcji płatności; zmiana środowiska testowego, bez zmian w kodzie)
- Niepewność: średnia (wnętrze ramki operatora, kolejność Tab, ponowienie po zablokowanym skrypcie — nie do ustalenia z kodu)
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access write`, Playwright CLI
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (plik Sparka → Gemini, wg skilla)
- Dopuszczone alternatywy: autor — Gemini `-Access write` z Playwright MCP (CLI w `agy` nie działa); recenzent — brak innej rodziny wg procedury skilla
- Powód wyboru: procedura skilla QA Sphere v1.6 i Playwright CLI dostępne tylko w linii Spark
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark nieznany, Gemini nieznany (wrappery bez zapasu, bez komunikatów limitu), 20:45Z
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: lint 0 błędów, 19 pozycji `updates[]`; weryfikacja na żywo potwierdziła pola karty, plakietkę trybu testowego Stripe (ramka ze skryptu operatora), pełną kolejność Tab łącznie z wnętrzem ramki i scenariusz P1 (blokada `js.stripe.com` → komunikat → ponowienie bez przeładowania wczytuje pole); 0 pełnych snapshotów, 61 wywołań powłoki, 11,3 min
- Rundy korekt: 1 — z winy specyfikacji (brief kazał użyć panelu „Network request blocking”, którego nazwa zmienia się między wersjami Chrome; krok kazał przeładować nieotwartą stronę) + komentarz folderu zgłoszony przez autora; 1,2 min
- Czas do akceptacji: ~35 min zegarowo (autor 11,3 min, korekta 1,2 min, recenzja 8,8 min)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 zgłoszonych; recenzent potwierdził zakres zmian wobec źródła, napisy wobec `pl.json`, brak pozostałości atrapy w 14 przypadkach spoza poprawek. Jedno twierdzenie z części potwierdzającej (konto demo w P3) architekt sprawdził osobno — zgodne z zestawem zatwierdzonym wcześniej
- Defekty po odbiorze: brak (`qas.py update --only 1606` → `verify --only` → `update` → `verify` 19/19, różnic 0; komentarz folderu 170 przez `upsert_folders`, bo `qas.py folders` celowo nie nadpisuje komentarza istniejącego folderu)
- Wymagane testy i dowody: `browser-check` matrix architekta (pole karty w kadrze puste — artefakt zrzutu ramki poza widokiem; rozstrzygnięte zrzutami wykonawcy po przewinięciu), zrzuty light/dark obejrzane przez architekta, diff każdej pozycji `updates[]` wobec opublikowanej treści, `lint`, `update --dry-run`
- Uwaga o specyfikacji: autor obalił trzy drobne przesłanki briefu (motyw startowy sesji, pusta klauzula Z4, nieczytelność wnętrza ramki) i wskazał nieobjęty briefem komentarz folderu. Lekcja: instrukcja DevTools w przypadku manualnym przez menu kontekstowe żądania, nie przez nazwę panelu.

### 2715-B1 (klient zewnętrznego systemu fakturowego i konfiguracja z poświadczeniem) — 2026-10-12
- Archetyp: Backend — klient HTTP integracji zewnętrznej + konfiguracja fail-closed + workflow wdrożenia
- Stawka: wysoka / high-stakes (poświadczenie API, maskowanie sekretu w opisie błędu, bramki startu)
- Niepewność: średnia (próba API niewykonalna — poświadczenie konta testowego unieważnione; klient na udokumentowanym zachowaniu)
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh` (21,6 min, 69 wywołań)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access read` (13,2 min)
- Dopuszczone alternatywy: wykonawca — brak (przy CZERWONYM Spark `max` albo czekanie); recenzent — Sol 6.1 `high` (dopuszczony, odłożony dla puli bramki, reguła 7), Gemini wykluczony przy high-stakes
- Powód wyboru: twarda bramka — poświadczenie; recenzent innej rodziny o stawce wysokiej
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy przy planie (hook ŻÓŁTY, 2026-10-12 ok. 21:52Z), przy wysyłce po resecie okna; Spark nieznany (wrapper bez zapasu), 22:37Z
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany bez korekty z wykonania (build 0/0, 5917 testów, 0 pominiętych, format czysty)
- Rundy korekt: 0 osobnych — przyjęte P3 wdrożone jako sekcja 0 briefu B3 (ta sama linia), odebrane w walidacji B3
- Czas do akceptacji: ~22 min wykonania + 13 min recenzji; poprawki P3 domknięte z falą 3
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): werdykt „poprawny” 0,85; 1 × P2 odrzucone (brak testów — testy zaplanowane w fali 4); 5 × P3: potwierdzone 4 (biały znak w tokenie przechodzi bramkę; prefiks identyfikatora z samą spacją; nazwa klasy łapana przez skan rejestracji; dwie z trzech luk maskowania — niezamknięta wartość, małe heksy), odrzucone 1 (goły `host:port` w komunikacie .NET to konfiguracja, nie sekret); 1 × P3 do potwierdzenia na żywo (forma wysyłki tokenu w `send_by_email`)
- Defekty po odbiorze: TAK — bramka końcowa (przebieg 1) znalazła w plikach B1: identyfikator idempotencji z konfiguracji (P1), maskowanie tokenu w zapisie JSON (P1), klasyfikację 401/403 przy zerwanej treści (P2), parsowanie sekcji przy wyłączonej integracji (P2), `KsefMode` jako kombinacja flag (P2) — wszystkie poprawione (wpis 2715-GATE-fix-1); przebieg 2 — dalsze wycieki maskowania (wpis 2715-GATE-fix-2)
- Wymagane testy i dowody: `dotnet build`, pełny `dotnet test` ze zmienną testów SQL (0 pominiętych), `dotnet format --verify-no-changes` ze ścieżkami względnymi
- Uwaga o specyfikacji: brief przepisał z planu konfigurowalny prefiks identyfikatora idempotencji — sama decyzja planu była błędem (zmiana konfiguracji między próbami tworzy drugi dokument), nie wykryły jej ani recenzja fali, ani wykonawca; złapała dopiero bramka. Lekcja: każdy składnik klucza idempotencji jest stałą kodu.

### 2715-D1 (datowane rewizje dwóch dokumentów produktowych integracji fakturowej) — 2026-10-12
- Archetyp: Dokumentacja produktowa — datowana rewizja dokumentów `zatwierdzony`
- Stawka: średnia (źródło prawdy dla funkcji high-stakes; bez kodu)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access write` (6,9 min + korekty 2,9 i 3,3 min)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (11,5 min)
- Dopuszczone alternatywy: wykonawca — `wykonawca` Sonnet 5.5 `high`, Gemini `high`; recenzent — Sol 6.1 `high` (odłożony dla puli bramki)
- Powód wyboru: tekst bez niezmiennika kodu, cele rozłączne z równoległym B1; recenzent innej rodziny, preferowany przy niskiej/średniej stawce
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark nieznany, Gemini nieznany (wrappery bez zapasu, bez komunikatów limitu), 22:14–22:47Z
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: wymagane korekty — walidacja architekta (diff) dała korektę 1 (doprecyzowania rewizji) przed recenzją
- Rundy korekt: 2 (korekta 1 z walidacji, korekta 2 po recenzji — 5 poprawek, przyjęta za pierwszym razem; wykonawca zgłosił drobną usterkę składni w podyktowanym brzmieniu)
- Czas do akceptacji: ~33 min zegarowo (22:14–22:47Z)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): werdykt „niepoprawny”; potwierdzone: P0 obniżony do P2 (odrzucone uwierzytelnienie nie trafia w sygnał pulpitu administratora — zapisane jako luka do PBI #1727, nie nowa reguła), 2 × P1 (brak adresu nabywcy w treści zlecenia; skasowane oryginalne słowa z wcześniejszej rewizji zatwierdzonej — przywrócone dosłownie ze sprostowaniem), 1 × P2 (preheader obiecuje fakturę — zapisane jako ta sama luka brzmienia), 1 × P3 (kotwica odsyłacza); odrzucone: 1 × P2 („fikcyjne pole kraju” — kolumna kraju istnieje, formularze jej nie zbierają; brzmienie mimo to doprecyzowane w korekcie 2)
- Defekty po odbiorze: przegląd zgodności 4c dołożył 3 zdania (wadliwa migawka → od razu wyczerpane; wyczerpanie wysyłki; odroczenie korekty bez zużycia prób) — luki opisu zachowania kodu powstałego później, nie błąd D1
- Wymagane testy i dowody: `git diff` trzech plików (dopisania, bez kasowania słów sprzed rewizji), sprawdzenie odsyłaczy i kotwic skryptem wykonawcy
- Uwaga o specyfikacji: brief D1 nie zakazał wprost przeredagowania oryginalnych słów wcześniejszej rewizji — wykonawca zastąpił zdanie zamiast dopisać sprostowanie; lekcja: brief rewizji zawsze mówi „oryginalnych słów nie kasujesz, dopisujesz sprostowanie”.

### 2715-B2 (migracja tabeli kolejki dokumentów, repozytorium z dzierżawą i strażnikami) — 2026-10-12
- Archetyp: Backend — migracja danych + repozytorium SQL z niezmiennikiem „dokładnie raz”
- Stawka: wysoka / high-stakes (migracja danych, jednorazowość dokumentu za płatność)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh` (24,7 min, 98 wywołań)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access read` (12,5 min)
- Dopuszczone alternatywy: wykonawca — brak (przy CZERWONYM Spark `max` albo czekanie); recenzent — Sol 6.1 `high` (odłożony dla puli bramki), Gemini wykluczony przy high-stakes
- Powód wyboru: twarda bramka — migracja i niezmiennik jednorazowości; recenzent innej rodziny o stawce wysokiej
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook przy wysyłce); Spark nieznany, 23:14Z
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany bez korekty z wykonania — strażnik `InvoiceId + ClaimToken + stan` we wszystkich 9 `UPDATE`, migracja na fiksturze, 5917 testów (0 pominiętych); wykonawca sam sprawdził 31 niezmienników skryptem na bazie tymczasowej
- Rundy korekt: 0 osobnych — przyjęte P3 wdrożone w sekcji 0 briefu B3 (ta sama linia)
- Czas do akceptacji: ~25 min wykonania + 12,5 min recenzji
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): werdykt „niepoprawny” 0,85; P1 (kraj nabywcy z zakupu pusty wbrew nocie schematu) obniżony do P3 — mapowanie pustego kraju na domyślny w budowie żądania + poprawka noty; potwierdzone 4 × P3 (przestarzałe komentarze dostawcy; strażnik zaklepania bez transakcji zewnętrznej; „domyślnie” w notach polityki ponawiania; brak wierszy skryptów w README); odrzucone 2 × P3 (filtr pustego identyfikatora zewnętrznego — stan osiągalny tylko ręcznym SQL; rozszerzenie odczytu o netto i liczbę miejsc — pozycja z brutto, ilość 1)
- Defekty po odbiorze: brak w plikach B2 (bramka końcowa nie zgłosiła znalezisk w migracji ani SQL repozytorium)
- Wymagane testy i dowody: `dotnet build`, pełny `dotnet test` z SQL (migracja na fiksturze), odczyt każdego `UPDATE` przez architekta pod kątem strażnika
- Uwaga o specyfikacji: plan i brief zakładały, że profil rozliczeniowy z zakupu niesie kraj — zapis zakupowy go pomija; fakt wychwycił recenzent, nie wykonawca.

### 2715-B3 (cykl wystawiania dokumentów, budowa żądania, usługa tła) — 2026-10-12
- Archetyp: Backend — cykl w tle z niezmiennikiem „dokładnie raz” (logika przekrojowa z cichym błędem)
- Stawka: wysoka / high-stakes (duplikat dokumentu za płatność, korekty, wysyłka e-mail)
- Niepewność: średnia (wariant obsługi duplikatu bez próby API — wariant B: ręczne uzgodnienie)
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh` (19,5 min, 103 wywołania); korekta — ten sam agent typu, świeży przebieg (3,3 min, 26 wywołań)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access read` (11,1 min)
- Dopuszczone alternatywy: wykonawca — brak (przy CZERWONYM Spark `max` albo czekanie); recenzent — Sol 6.1 `high` (odłożony dla puli bramki), Gemini wykluczony przy high-stakes
- Powód wyboru: twarda bramka — logika przekrojowa z cichym błędem; recenzent innej rodziny o stawce wysokiej
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook przy wysyłce); Spark nieznany, 23:48Z
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany (build 0/0, 5917 testów, format 33 pliki); 2 drobiazgi (komentarz PL, linia instrukcji projektu) poprawione przez architekta (reguła 11)
- Rundy korekt: 1 (górne granice ustawień cyklu, przyjęta za pierwszym razem)
- Czas do akceptacji: ~20 min wykonania + 11 min recenzji + 3,3 min korekty + walidacja
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): werdykt „poprawny” 0,9; 1 × P3 potwierdzone (brak górnych granic interwału, liczby prób i dzierżawy — absurdalna wartość przechodzi start)
- Defekty po odbiorze: TAK — bramka końcowa (przebieg 1) znalazła w budowie żądania zastępczą datę utworzenia zamiast daty płatności (P2) i identyfikator idempotencji z konfiguracji (P1, decyzja planu) — poprawione w 2715-GATE-fix-1
- Wymagane testy i dowody: `dotnet build`, pełny `dotnet test` z SQL, format ze ścieżkami względnymi
- Uwaga o specyfikacji: oba defekty z bramki pochodzą z briefu architekta, nie z wykonania — brief B3 sam przepisał zastępczą datę utworzenia przy braku daty płatności (wbrew punktom 5–6 specyfikacji) i prefiks identyfikatora z konfiguracji; ani wykonawca, ani recenzent fali ich nie zakwestionowali. Lekcja: brak danych z migawki to zawsze wada danych, nie wartość zastępcza.

### 2715-T1a (testy jednostkowe klienta, maskowania, bramek konfiguracji i budowy żądania; próba testera #3, ramię A) — 2026-10-13
- Archetyp: Testy — xunit jednostkowe BE (klient HTTP z atrapą handlera, interpreter, konfiguracja)
- Stawka: wysoka / high-stakes (dowód maskowania sekretu i bramek startu; pliki testów bez niezmiennika produkcji)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Claude / `tester` — Sonnet 5.5 / `medium` (10,3 min, 36 wywołań; korekta 3,7 min, 35 wywołań)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access read` (7,7 min; stała kontrola próby)
- Dopuszczone alternatywy: w próbie brak (ramię wybrane przed briefem)
- Powód wyboru: próba testera (reguła 14), brief #3
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook ZIELONY); Spark nieznany, 00:27Z
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: 24 scenariusze, 191 przypadków, zielone; 5/5 mutacji produkcyjnych architekta wykrytych; raport „format czysty” fałszywy — 3 pliki z LF, znormalizowane przez architekta
- Rundy korekt: 1 (6 × P2 + 4 × P3 po recenzji, przyjęta za pierwszym razem)
- Czas do akceptacji: ~10 min + recenzja 7,7 min + korekta 3,7 min + walidacja
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): werdykt z pewnością 0,85; potwierdzone 6 × P2 (pusty e-mail konta; pusty typ nabywcy; treść wysyłki e-mail tylko z tokenem; gałąź `IOException`; 422 z identyfikatorem przy wysyłce; logi klienta bez weryfikacji braku sekretu) i 3 × P3 (asercja wycieku na fragmencie zamiast pełnego tokenu; brak asercji pozytywnej przy limicie; luki danych teorii); fałszywej zieleni brak
- Defekty po odbiorze: brak w testach (bramka końcowa wymusiła nowe testy do swoich poprawek, nie poprawki tych)
- Wymagane testy i dowody: pełny `dotnet test` (6108, 0 pominiętych), format 42 pliki, mutacje produkcyjne architekta 5/5; koszt próby 3,60 $ (dziennik `proba-testera-haiku`)
- Uwaga o specyfikacji: brak błędów briefu; lekcja procesu — raport wykonawcy o formacie nie jest dowodem (CRLF sprawdzany przez architekta).

### 2715-T1b (testy cyklu i repozytorium na prawdziwym SQL — równoległość, dzierżawa, strażniki; próba testera #4, ramię B) — 2026-10-13
- Archetyp: Testy — xunit integracyjne BE na prawdziwym SQL Server (równoległe cykle, strażniki zapisów)
- Stawka: wysoka / high-stakes (dowód niezmiennika „dokładnie raz”; pliki testów bez niezmiennika produkcji)
- Niepewność: średnia (równoległość, zegar, fikstura migracji)
- Wykonawca (linia / model / native effort): Claude / `tester-haiku` — Haiku 5.5 / `xhigh` (część 1: 8,0 min, przekazanie przy 300 tys.; część 2 świeży agent: 13,0 min; korekta 15,7 min)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access read` (9,3 min; stała kontrola próby)
- Dopuszczone alternatywy: w próbie brak
- Powód wyboru: próba testera (reguła 14), brief #4
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook ZIELONY); Spark nieznany, 00:57Z
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: 2 klasy, 26 testów, 7 plików wsparcia; 6/6 mutacji strażników SQL i cyklu architekta wykrytych; LF w części 1 — wykonawca sam wyłapał
- Rundy korekt: 1 (3 × P2 + P3 po recenzji, przyjęta za pierwszym razem; przekazanie kontekstu nie jest rundą)
- Czas do akceptacji: ~21 min wykonania w dwóch częściach + recenzja 9,3 min + korekta 15,7 min + walidacja
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): werdykt „niepoprawny”; P1 (brak testu ponownej wysyłki e-mail) obalony mutacją architekta; potwierdzone 3 × P2 (strażniki zapisów e-mail — potwierdzone mutacją; strażnik tokenu w odczycie do wystawienia; limit paczki) i P3 (m.in. czyszczenie opisu błędu, kolejność faktura-przed-korektą, pomiar faktycznej równoległości); odrzucone: 1 × P1
- Defekty po odbiorze: brak
- Wymagane testy i dowody: pełny `dotnet test` (6151, 0 pominiętych), format 53 pliki (ścieżki względne), mutacje 6/6 przed i po korekcie, rebuild `--no-incremental`; koszt próby 3,08 $ (dziennik `proba-testera-haiku`)
- Uwaga o specyfikacji: brief zakresowo cięższy od #3 (testy SQL z równoległością) — porównanie ramion próby musi to uwzględnić.

### 2715-4c (przegląd zgodności dokumentacji z kodem i dziennikiem rozbieżności) — 2026-10-13
- Archetyp: Przegląd zgodności dokumentacji — kod ↔ dokumenty produktowe ↔ dziennik rozbieżności
- Stawka: średnia (źródło prawdy funkcji high-stakes; tylko odczyt)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (6,4 min)
- Recenzent (linia / model / native effort): architekt — weryfikacja znalezisk względem kodu i dokumentów
- Dopuszczone alternatywy: Sol 6.1 `high` (odłożony — pula Codexa dla bramki)
- Powód wyboru: inna rodzina niż autor kodu (Claude) i dokumentów (Spark); brief z wklejonym kontekstem, bo recenzent bez powłoki czyta tylko repozytoria
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany (wrapper), 01:34Z
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: „zgodne z uwagami” 0,98; raport kompletny za pierwszym razem
- Rundy korekt: 0 (trzy zdania dopisane przez architekta, reguła 11)
- Czas do akceptacji: 6,4 min + triaż architekta
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): potwierdzone: P1 obniżony do P2 (wadliwa migawka danych → od razu wyczerpane, nieopisane w dokumencie), P2 (wyczerpanie prób wysyłki e-mail nieopisane), P3 (odroczenie korekty bez zużycia prób); odrzucone: 0
- Defekty po odbiorze: brak (stan na zamknięcie dziennika)
- Wymagane testy i dowody: dziennik rozbieżności 1–16 zamknięty poza wierszem 12 (pytanie do właściciela o brzmienie preheadera)
- Uwaga o specyfikacji: brak błędów briefu.

### 2715-GATE (bramka końcowa BE high-stakes, trzy przebiegi na całym diffie) — 2026-10-13
- Archetyp: Recenzja — bramka końcowa funkcji high-stakes (cały diff repozytorium, tylko odczyt)
- Stawka: wysoka / high-stakes (jednorazowość dokumentu za płatność, poświadczenie, migracja)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): n/d (recenzja)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `max`, `-Mode review` (przebiegi: 25,8 min, 20,4 min, 18,2 min)
- Dopuszczone alternatywy: brak — reguła 6; przy limicie okna 5 h czekanie, przy limicie tygodniowym jednorazowo Spark `max` (decyzja właściciela 12 dla tej funkcji)
- Powód wyboru: obowiązkowa bramka reguły 6; niezależna rodzina wobec autora plików niezmiennika (Opus); Codex nie dostał w tej funkcji żadnego innego briefu
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper bez zapasu), bez komunikatu limitu w trzech przebiegach, 01:30–03:54Z
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: przebieg 1 — 2 × P1 + 4 × P2, wszystkie potwierdzone przez architekta w kodzie
- Rundy korekt: 2 (GATE-fix-1 po przebiegu 1, GATE-fix-2 po przebiegu 2); przebieg 3 — 0 znalezisk, „patch is correct”, pewność 0,9
- Czas do akceptacji: ~2,4 h zegarowo (01:30–03:55Z), w tym ~65 min trzech przebiegów bramki
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): przebieg 1 potwierdzone: P1 identyfikator idempotencji z konfiguracji (zmiana między próbami → drugi dokument), P1 token w zapisie JSON z ucieczkami przechodzi maskowanie, P2 401/403 z zerwaną treścią liczone jako błąd przejściowy, P2 sekcja parsowana przy wyłączonej integracji (błędna wartość blokuje start), P2 zastępcza data utworzenia zamiast daty płatności, P2 tryb KSeF jako kombinacja flag włącza wysyłkę; przebieg 2 potwierdzone: 5 z 6 poprawek zamkniętych, P1 segment tokenu zakodowany osobno, P2 adres z ukośnikami kodem znaku JSON niosący parametr tokenu dostępu; przebieg 3: 0; odrzucone: 0
- Defekty po odbiorze: brak (stan przed wdrożeniem PRE)
- Wymagane testy i dowody: każde P0/P1 potwierdzone scenariuszem w kodzie przed poprawką; po każdej poprawce pełny `dotnet test` i mutacje produkcyjne architekta (14/14 wykrytych łącznie)
- Uwaga o specyfikacji: 3 z 8 potwierdzonych znalezisk wynikały z decyzji architekta w planie lub briefie (konfigurowalny prefiks identyfikatora, zastępcza data, wyliczanie kodowań w poprawce 1), nie z wykonania — bramka była jedyną linią, która je złapała; recenzje fal (Spark `max`) ich nie zgłosiły.

### 2715-GATE-fix-1 (sześć poprawek po bramce — identyfikator stały, maskowanie, klasyfikacja 401/403, konfiguracja, data sprzedaży) — 2026-10-13
- Archetyp: Backend — poprawki niezmienników po bramce (klient HTTP, konfiguracja, budowa żądania) z testami
- Stawka: wysoka / high-stakes
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh` (32,3 min, 121 wywołań, ~334 tys. kontekstu — próg miękki przekroczony, dokończony bez przekazania)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `max`, `-Mode review` — przebieg 2 bramki na całym diffie jako recenzja fali poprawek (inna rodzina niż Opus; bez dublowania osobnym Sparkiem)
- Dopuszczone alternatywy: wykonawca — brak (przy CZERWONYM Spark `max`); recenzent — Spark `max` (odrzucony jako dublowanie przebiegu 2 bramki)
- Powód wyboru: pliki niezmiennika; jeden brief, bo każda poprawka zmienia zachowanie pilnowane przez istniejące testy
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook ZIELONY), ok. 02:00Z
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany bez korekty z wykonania — build 0/0, 6191 testów (0 pominiętych), format 57 plików, 9/9 mutacji produkcyjnych architekta wykrytych (2 powtórzone po błędzie kompilacji samej mutacji, nie defekcie)
- Rundy korekt: 0 z wykonania
- Czas do akceptacji: 32 min wykonania + walidacja ~15 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): przebieg 2 bramki potwierdził zamknięcie 5 poprawek; poprawka maskowania niepełna (P1 + P2 — wpis 2715-GATE-fix-2)
- Defekty po odbiorze: niepełne maskowanie — wada specyfikacji (brief wyliczał postacie kodowania tokenu jedna po drugiej), wykonanie zgodne z briefem
- Wymagane testy i dowody: pełny `dotnet test` z SQL, format ze ścieżkami względnymi, brak pozostałości nazwy usuniętej opcji w repozytorium, mutacje każdej poprawki
- Uwaga o specyfikacji: decyzja 2 briefu (lista kodowań) była strukturalnie zła — wycieki wracały przy każdym nowym kodowaniu; poprawna struktura (dekoduj, potem maskuj) przyszła dopiero w GATE-fix-2.

### 2715-GATE-fix-2 (maskowanie sekretów w opisie błędu — dekoduj, potem maskuj) — 2026-10-13
- Archetyp: Backend — niezmiennik tajemnicy (potok normalizacji i maskowania tekstu) z testami
- Stawka: wysoka / high-stakes (poświadczenie i token dostępu do dokumentu w logach i bazie)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh` (15,9 min, 41 wywołań; dogrywka 22,7 min, 53 wywołania)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `max`, `-Mode review` — przebieg 3 bramki na całym diffie
- Dopuszczone alternatywy: wykonawca — brak (przy CZERWONYM Spark `max`); recenzent — Spark `max` (odrzucony jako dublowanie przebiegu 3)
- Powód wyboru: plik niezmiennika tajemnicy
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook ZIELONY, okno 5 h 4 %, tydzień 41 %), ok. 03:10Z
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zgodny z briefem; walidacja architekta dała dogrywkę (reguła parametru tokenu bez wymaganego poprzedzającego separatora, limit rund dekodowania 3 → 8)
- Rundy korekt: 1 (dogrywka, przyjęta za pierwszym razem)
- Czas do akceptacji: ~39 min wykonania + walidacja ~10 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): przebieg 3 bramki — 0 znalezisk, oba wycieki z przebiegu 2 zamknięte, „patch is correct”, pewność 0,9
- Defekty po odbiorze: brak (stan przed wdrożeniem PRE)
- Wymagane testy i dowody: build `--no-incremental` 0/0, pełny `dotnet test` 6219 (0 pominiętych), format 57 plików, 5/5 mutacji potoku wykrytych (bez dekodowania, bez przebiegu surowego, bez reguły parametru, jedna runda, bez dekodowania procentowego), rebuild 400/400 testów funkcji
- Uwaga o specyfikacji: brief wymagał separatora `[?&;]` przed nazwą parametru — dogrywka zastąpiła go warunkiem granicy nazwy, żeby parametr bez separatora też był maskowany; znane granice zapisane jako P3 w raporcie (kodowanie zagnieżdżone ponad limit rund, spacje wokół `=`).

### qas-review-S1 (skrypt transportu QA Sphere: przegląd istniejących przypadków, oznaczenie wycofanych, lint i testy bez sieci) — 2026-10-13
- Archetyp: Algorytmika / Logika — narzędzie wiersza poleceń z walidacją pliku i zapisem do zewnętrznego systemu testów.
- Stawka: średnia — zapisy w rejestrze przypadków testowych są odwracalne, ale API nie usuwa przypadków, więc błędny zapis zostaje w rejestrze do ręcznego sprzątania.
- Niepewność: średnia — nowy format pliku (werdykty przeglądu, wpisy wycofania), zachowanie API zmierzone w trakcie (brak usuwania i przenoszenia).
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max` (`-Access write`), domyślny effort reguły 8.
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (`-Mode review`) — wpis qas-review-R1.
- Dopuszczone alternatywy: Codex `gpt-6.1-sol` `high` (porcje ≤ 5 plików — tu 2 pliki); `wykonawca` (Sonnet 5.5 `high`).
- Powód wyboru: jeden plik skryptu z testami jednostkowymi bez sieci, pełna pętla testów w linii Sparka, pula bez komunikatów limitu.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark `nieznany` (wrapper nie podaje zapasu), 2026-10-13 07:54.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: wymagane korekty — implementacja zgodna ze specyfikacją, ale właściciel zmienił decyzję w trakcie (oznaczenie tagiem i prefiksem zamiast folderu).
- Rundy korekt: 2 — runda 1 z winy zmiany decyzji właściciela i trzech uwag wykonawcy do specyfikacji (przyjęte); runda 2 po recenzji: 3 defekty wykonania (niepełny odczyt przed zapisem, typ werdyktu, typ znacznika wykonania) i 5 uzupełnień specyfikacji.
- Czas do akceptacji: ~44 min (przebiegi 11,5 + 7 + 10,7 min, recenzja 7 min).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): zob. qas-review-R1.
- Defekty po odbiorze: brak do chwili wpisu.
- Wymagane testy i dowody: 155 testów jednostkowych zielonych (z atrapą transportu); odczyt kontekstu na żywym projekcie (folder z 9 przypadkami); lint, tabela i próba wycofania bez wywołań na kontekście z żywych danych; próba tagu z nawiasami na jednym przypadku, stan przywrócony.

### qas-review-R1 (recenzja skryptu transportu QA Sphere i dwóch skilli procedury) — 2026-10-13
- Archetyp: Recenzja — skrypt narzędziowy z testami oraz dokumentacja procedury.
- Stawka: średnia (jak qas-review-S1).
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): autorzy recenzowanego diffu: Spark `max` (skrypt, testy), sesja architekta (Claude, dwa skille).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high` (`-Mode review`, tylko odczyt).
- Dopuszczone alternatywy: Gemini `gemini-3.8-flash-high` `-Access read`.
- Powód wyboru: rodzina inna niż obaj autorzy; preferencja reguły 13 przy niższej stawce; recenzent sam czyta diff i uruchamia scenariusze w pamięci.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex `nieznany` (wrapper nie podaje zapasu), 2026-10-13 08:16.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: raport kompletny w jednym przebiegu, werdykt „niepoprawny”.
- Rundy korekt: 0 (recenzja).
- Czas do akceptacji: 7 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): potwierdzone 6 — P1 ×1 (zapis po niepełnym odczycie nadpisuje tytuł i tagi), P2 ×4 (wycofanie spoza zakresu przeglądu, kolejność pełnej weryfikacji w obu skillach, znacznik wykonania niebędący wartością logiczną, nieobsłużony typ werdyktu), P3 ×1 (brak adresów przy ponownym uruchomieniu); odrzucone 0. Ocena trzech uwag zaplanowanych przez architekta: dwie właściwe, trzecia za szeroka (blokowała dozwoloną zmianę samego priorytetu) — zawężona.
- Defekty po odbiorze: brak do chwili wpisu.
- Wymagane testy i dowody: każde znalezisko sprawdzone przez architekta w kodzie przed korektą; po korekcie 155 testów zielonych i próby na kontekście z żywych danych.

### 2473-BE-1 (lustro subskrypcji u operatora, migracja, zawieszanie — łańcuch 1 → 1a → 1b → 1c → 1d) — 2026-10-13
- Archetyp: Backend — serwis lustra stanu subskrypcji z SQL warunkowym, migracja, bramka operatora płatności
- Stawka: wysoka / high-stakes (zapis okresu, miejsc, MRR, zawieszanie programów, płatność odnowienia, migracja)
- Niepewność: wysoka (nowy przekrój, kolejność zdarzeń operatora, idempotencja)
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh` (BE-1 9,9 min → przekazanie przy 319 tys.; 1a 17,6 min, 100 wywołań; 1b 15,5 min, 98 wywołań, 340 tys.; 1c 4,6 min; 1d 6,2 min po recenzji)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access read` (R-BE-1a 9,8 min, R-BE-1b 14,2 min)
- Dopuszczone alternatywy: wykonawca — brak (twarda bramka); recenzent — Sol 6.1 `high` (pula Codexa odłożona na bramkę)
- Powód wyboru: pliki niezmiennika; recenzja wyższej stawki z innej rodziny
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook ZIELONY, ok. 07:00Z); Spark nieznany (wrapper)
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: przekazanie kontekstu po 10 min — brief za duży na jeden przebieg (lustro + migracja + bramka), podział na 1a/1b/1c
- Rundy korekt: 1 (1d po recenzji; przekazania nie są rundą)
- Czas do akceptacji: ~54 min wykonania w pięciu przebiegach + 2 recenzje ~24 min + walidacja
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R-BE-1a ✓ 0,85, R-BE-1b ✓ 0,9 — P2/P3 potwierdzone, poprawione w 1d; odrzucone 0
- Defekty po odbiorze: bramka końcowa — P1 spóźniona faktura odnowienia ≠ ostatnia faktura ginęła, P2 zwolnienie harmonogramu poza blokadą (wpis 2473-BE-6)
- Wymagane testy i dowody: build 0/0, pełny `dotnet test` z SQL (6328), mutacje
- Uwaga o specyfikacji: brief fali 1 łączył trzy warstwy — strażnik kontekstu rozdzielił je sam; kolejne briefy dzielone z góry.

### 2473-FE-1 (kafelek „Następna płatność” — kwota niedostępna, data z bazy) — 2026-10-13
- Archetyp: Frontend — prezentacja w istniejących komponentach ustawień, DTO, mapowanie widoku, i18n, specy Vitest/AXE
- Stawka: średnia (ekran funkcji high-stakes bez niezmiennika)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Claude / `wykonawca` — Sonnet 5.5 / `high` (2,4 + 3,9 + 1,1 min w trzech wznowieniach)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (8,5 min)
- Dopuszczone alternatywy: wykonawca — Spark `max`; Codex odpadł (> 5 plików przy sygnale `nieznany` w funkcji high-stakes); recenzent — Sol `high`
- Powód wyboru: ekran bez niezmiennika, kontekst sesji; recenzja niskiej stawki wg reguły 13
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook ZIELONY); Gemini nieznany
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany
- Rundy korekt: 0
- Czas do akceptacji: ~7 min wykonania + recenzja 8,5 min + walidacja
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R-FE-1 ✓, bez P0–P2
- Defekty po odbiorze: brak (bramka FE zielona, 0 znalezisk)
- Wymagane testy i dowody: `npm run lint`, `format:check`, `npm test` (4553), `npm run build`; browser-check `matrix` 4/4
- Uwaga o specyfikacji: brak błędów briefu.

### 2473-FIG-1 (makieta stanu „Kwota niedostępna”) — 2026-10-13
- Archetyp: Frontend UI / Figma — wariant tekstu w istniejącym kafelku
- Stawka: niska
- Niepewność: niska
- Wykonawca (linia / model / native effort): Claude / `wykonawca` — Sonnet 5.5 / `high`, Figma MCP (1,0 min)
- Recenzent (linia / model / native effort): architekt (zrzut Figmy)
- Dopuszczone alternatywy: Codex z potwierdzonym MCP — niepotwierdzony w sesji
- Powód wyboru: jedyna linia z potwierdzonym Figma MCP
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook ZIELONY)
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany
- Rundy korekt: 0
- Czas do akceptacji: 1 min + zrzut
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): brak
- Defekty po odbiorze: brak
- Wymagane testy i dowody: zrzut Figmy
- Uwaga o specyfikacji: brak.

### 2473-DOC (rewizje dokumentacji produktowej: DOC-1 przed falą 1, DOC-2 Faza 4c, DOC-3 po bramce) — 2026-10-13
- Archetyp: Dokumentacja produktowa — datowane rewizje sześciu dokumentów, dziennik rozbieżności
- Stawka: średnia (źródło prawdy funkcji high-stakes)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access write` (DOC-1 5,6 min + korekta 3,1 min; DOC-2 7,2 min; DOC-3 4,7 min)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (R-DOC-1 8,9 min; R-DOC-2 13,4 min; R-DOC-3 7,7 min)
- Dopuszczone alternatywy: Sol `high` (pula Codexa dla bramki)
- Powód wyboru: briefy tekstowe bez makiety; recenzja innej rodziny niż autor dokumentów i kodu
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark i Gemini nieznany (wrapper)
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: DOC-1 do korekty po recenzji; DOC-2 i DOC-3 zaakceptowane
- Rundy korekt: 1 (DOC-1); DOC-3 — P1 kolejności zdań i P2 kodów stanów poprawione przez architekta (reguła 11)
- Czas do akceptacji: ~21 min wykonania łącznie + ~30 min recenzji
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R-DOC-1 ✓ po korekcie; R-DOC-2 ✓ 1,0, 0 znalezisk; R-DOC-3 ✓ — P1 (kolejność zdań: alarm i korekta przypisane do złego przypadku) i P2 (kody stanów) potwierdzone; odrzucone 0
- Defekty po odbiorze: brak
- Wymagane testy i dowody: dziennik rozbieżności 35 wpisów, 0 otwartych; `git diff --stat` tylko dozwolone pliki
- Uwaga o specyfikacji: brak.

### 2473-BE-2 (zwrot odrzucony przez operatora po zapisie — procesor, SQL cofnięcia, stan „wstrzymane”) — 2026-10-13
- Archetyp: Backend — procesor zdarzeń operatora z oceną pod blokadą, SQL warunkowy, alarmy
- Stawka: wysoka / high-stakes (zwroty płatności, korekty faktur)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh` (18,0 min, 100 wywołań; korekty 13,1 min i 8,7 min)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access read` (R-BE-2 10,5 min, R-BE-2-2 13,8 min, R-BE-2-3 7,6 min)
- Dopuszczone alternatywy: wykonawca — brak; recenzent — Sol `high`
- Powód wyboru: pliki niezmiennika
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook ZIELONY); Spark nieznany
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: wymagane korekty
- Rundy korekt: 2
- Czas do akceptacji: ~40 min wykonania + ~32 min recenzji + walidacje
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R-BE-2 ✗ 0,85 i R-BE-2-2 ✗ 0,70 — P2 potwierdzone i poprawione; R-BE-2-3 ✓ 0,80 z 2 × P3 (odłożone przed bramkę)
- Defekty po odbiorze: bramka końcowa — P1 zwrot odrzucony przed zapisem jako wykonany, P2 stan zwrotu nierozpoznany bez alarmu (wpis 2473-BE-6)
- Wymagane testy i dowody: pełny `dotnet test` z SQL (6422), mutacje
- Uwaga o specyfikacji: przypadek „zwrot odrzucony przed zapisem” był poza planem — złapała go dopiero bramka.

### 2473-BE-3 (routing zdarzeń operatora, cykl uzgadniający, odczyt ustawień — 3a → 3b → kontynuacja) — 2026-10-13
- Archetyp: Backend — przekrój webhooka, usługa tła, zapytanie odczytu
- Stawka: wysoka / high-stakes (cichy błąd routingu zdarzeń płatności)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh` (3a 12,8 min; 3b 12,9 min → przekazanie przy 312 tys.; kontynuacja 11,3 min)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access read` (R-BE-3a 5,5 min, R-BE-3b 12,0 min)
- Dopuszczone alternatywy: wykonawca — brak; recenzent — Sol `high`
- Powód wyboru: pliki niezmiennika; podział 3a/3b z góry ze względu na budżet kontekstu
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook ZIELONY); Spark nieznany
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany (3a: dyspozytor zamiast parametrów handlera wymuszony analizatorem S107)
- Rundy korekt: 0 z wykonania
- Czas do akceptacji: ~37 min wykonania + ~18 min recenzji
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R-BE-3a ✓ 0,9 (4 × P3), R-BE-3b ✓ 0,85 (4 × P3) — wszystkie potwierdzone, odłożone przed bramkę i zrobione; odrzucone 0
- Defekty po odbiorze: brak przypisanych
- Wymagane testy i dowody: pełny `dotnet test` z SQL (6446)
- Uwaga o specyfikacji: brak.

### 2473-BE-4 (dokończenie przerwanej rezygnacji — wspólna droga, cykl dokończenia, idempotentne zakończenie — 4a → 4b → 4c) — 2026-10-13
- Archetyp: Backend — usługa domeny pod blokadą, cykl tła, SQL kandydatów
- Stawka: wysoka / high-stakes (zwrot gwarancji)
- Niepewność: wysoka (lustro na starcie dokończenia, zbiór płatności po przyjęciu)
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh` (4a 15,7 min; 4b 14,4 min; 4c 19,4 min, 341 tys.)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access read` (R-BE-4a 12,9 min, R-BE-4bc 8,8 min)
- Dopuszczone alternatywy: wykonawca — brak; recenzent — Sol `high`
- Powód wyboru: pliki niezmiennika
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook ZIELONY); Spark nieznany
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: 4a wymagał korekty (4c), 4b zaakceptowany
- Rundy korekt: 1 (4c)
- Czas do akceptacji: ~50 min wykonania + ~22 min recenzji
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R-BE-4a ✓ 0,85 warunkowo — P2 kroki lustra giną przy 409/502 (błąd briefu architekta) + 2 × P3; R-BE-4bc ✓ 0,90 — 2 × P3 i P3-3 odrzucone przez architekta błędnie (okno gwarancji ma 30 dni) → przywrócone jako P2 (BE-5a)
- Defekty po odbiorze: P2 odnowienie z okna gwarancji gubione przy pierwszym kliknięciu (BE-5a)
- Wymagane testy i dowody: pełny `dotnet test` z SQL (6505), mutacje 4/4
- Uwaga o specyfikacji: dwa błędy architekta — kolejność kroków lustra w briefie i błędne obalenie P3-3; recenzent miał rację w obu.

### 2473-BE-5 (poprawki przed bramką — 5a, 5b, 5c, 5c-2, 5e, 5f; `wykonawca-opus`) — 2026-10-13
- Archetyp: Backend — poprawki niezmienników po recenzjach fal (lustro przy pierwszym kliknięciu, przyjęcie przed lustrem, alarmy płatności odnowienia)
- Stawka: wysoka / high-stakes
- Niepewność: wysoka (wyścigi blokady, kolejność przyjęcia i lustra)
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh` (5a 14,8 min; 5b 12,9 min; 5c 15,4 min → przekazanie przy 344 tys.; 5c-2 16,2 min; 5e 8,4 min; 5f 14,2 min)
- Recenzent (linia / model / native effort): Spark `max` (R-BE-5a 14,3 min, R-BE-5c 15,0 min); Gemini `gemini-3.8-flash-high` (R-BE-5b 6,8 min, R-BE-5e 15,8 min, R-BE-5f 6,9 min)
- Dopuszczone alternatywy: wykonawca — brak; recenzent — Sol `high` (pula dla bramki)
- Powód wyboru: pliki niezmiennika; recenzent przemienny Spark/Gemini dla świeżego spojrzenia
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook ZIELONY → ŻÓŁTY po południu); Spark i Gemini nieznany
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: każdy brief zaakceptowany z wykonania; recenzje znajdowały kolejne luki obok (łańcuch 5a → 5c → 5e → 5f)
- Rundy korekt: 0 z wykonania na brief; 4 kolejne briefy z luk recenzji
- Czas do akceptacji: ~82 min wykonania + ~59 min recenzji
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R-BE-5a ✗ 0,8 — P1 (502 lustra przed przyjęciem + koniec u operatora = utrata gwarancji bez alarmu; błąd kolejności w briefie architekta) + 2 × P2 + 3 × P3; R-BE-5b ✓ 0,95 — P2 + 2 × P3; R-BE-5c ✗ 0,7 — 2 × P2; R-BE-5e ✓ 0,98 + 2 luki obok (P2, P2 obniżone z P1); R-BE-5f ✓ 1,0, P3 przyjęte bez zmian; odrzucone 0
- Defekty po odbiorze: regresja uprzęży testów z 5a złapana pełną walidacją (5c pkt 5)
- Wymagane testy i dowody: pełny `dotnet test` z SQL (6648 → 6676), mutacje po każdej poprawce
- Uwaga o specyfikacji: główne P1 i dwa P2 pochodziły z kolejności kroków w briefach architekta, nie z wykonania.

### 2473-BE-5d (Spark — anulowanie u operatora w „Następnej płatności”, testy lustra) — 2026-10-13
- Archetyp: Backend — zapytanie odczytu bez niezmiennika + testy
- Stawka: średnia (odczyt ustawień w funkcji high-stakes, bez pliku niezmiennika)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access write` (16,1 min)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (16,6 min)
- Dopuszczone alternatywy: `wykonawca` Sonnet `high`; Codex odpadł (sygnał `nieznany`, pula dla bramki)
- Powód wyboru: brief bez niezmiennika, odciążenie puli Claude'a przy ŻÓŁTYM
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark nieznany; Claude znany (hook ŻÓŁTY)
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowany (925 z filtrów, 2 mutacje czerwone)
- Rundy korekt: 0 (2 × P3 recenzji dołączone do BE-5f)
- Czas do akceptacji: ~16 min + recenzja 16,6 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R-BE-5d ✓ 0,98 — 2 × P3 potwierdzone; odrzucone 0
- Defekty po odbiorze: brak
- Wymagane testy i dowody: pełny `dotnet test` z SQL (6648)
- Uwaga o specyfikacji: brak.

### 2473-T-1 (testy SQL lustra i kandydatów cykli + testy orkiestracji T-1a; próba testera #5 A i #6 B) — 2026-10-13
- Archetyp: Testy — xunit jednostkowe i integracyjne BE na prawdziwym SQL Server
- Stawka: wysoka / high-stakes (dowody niezmienników lustra; pliki testów bez niezmiennika produkcji)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): T-1a — Claude / `tester` — Sonnet 5.5 / `medium` (13,7 min; korekty 7,2 + 1,4 min); T-1 — Claude / `tester-haiku` — Haiku 5.5 / `xhigh` (11,9 min → przekazanie; kontynuacja 8,0 min; korekta 8,4 min)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access read` — stała kontrola próby (R-T-1a 10,8 min, R-T-1a-2 6,1 min, R-T-1 8,9 min, R-T-1-2 7,8 min)
- Dopuszczone alternatywy: w próbie brak (ramię wybrane przed briefem)
- Powód wyboru: próba testera (reguła 14), briefy #5 i #6
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook ZIELONY); Spark nieznany
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: T-1a — wymagane korekty (2 rundy); T-1 — 3 × P1 luk asercji po recenzji
- Rundy korekt: T-1a 2, T-1 1
- Czas do akceptacji: T-1a ~22 min + recenzje ~17 min; T-1 ~28 min + recenzje ~17 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R-T-1a ✗ → R-T-1a-2 ✓ 0,85; R-T-1 ✗ 0,8 — 3 × P1 luk asercji potwierdzone w SQL, P2, 4 × P3 → R-T-1-2 ✓ 0,85 (8/8 domknięte, P3 komentarza)
- Defekty po odbiorze: brak
- Wymagane testy i dowody: pełny `dotnet test` z SQL (6540 → 6571), mutacje 3 + 5 czerwonych; koszt próby #5 A 5,99 $, #6 B 1,59 + 0,74 $
- Uwaga o specyfikacji: próba zamknięta 3:3 — Haiku 2,44 $/brief (0,60× Sonneta), rundy 1,00 wobec 1,33, defekty równe → Haiku przejmuje linię testera.

### 2473-T-2 (testy SQL zwrotów i przepływów rezygnacji — T-2a, T-2b, T-2c; Spark) — 2026-10-13
- Archetyp: Testy — xunit integracyjne BE (SQL, testy API na prawdziwym hoście)
- Stawka: wysoka / high-stakes (dowody zwrotu gwarancji; pliki testów bez niezmiennika produkcji)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access write` (T-2a 17,3 min; T-2b 39,6 min; T-2c 8,3 min)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (R-T-2a 9,6 min; R-T-2b 9,1 min); T-2c — bramka końcowa Sol `max` na całym diffie
- Dopuszczone alternatywy: `tester-haiku` (po zamknięciu próby); Sol `high` jako recenzent (pula dla bramki)
- Powód wyboru: odciążenie puli Claude'a; testy poza próbą testera; recenzja innej rodziny
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark i Gemini nieznany; pierwszy przebieg R-T-2a Gemini odrzucony w 13 s — brief bez zakazu powłoki
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: T-2a — 2 × P2 filtrów w zapytaniach wsadowych do T-2b; T-2b — P1→P2 i 2 × P2 luk asercji
- Rundy korekt: 1 (T-2c)
- Czas do akceptacji: ~65 min wykonania + ~19 min recenzji
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R-T-2a ✓ 0,95 — 2 × P2 + 2 × P3; R-T-2b ✗ 0,96 — P2 (obniżone z P1) + 2 × P2 + P3, wszystkie potwierdzone; odrzucone 0
- Defekty po odbiorze: brak
- Wymagane testy i dowody: `SubscriptionManagement` 2442/2442, mutacje 10/10 (T-2b), M-Used 10 czerwonych (T-2c); pliki produkcyjne mutowane i przywrócone — sprawdzone przez architekta
- Uwaga o specyfikacji: przesłanka briefu T-2b o pliku `.Suspension.cs` była fałszywa — wykonawca zatrzymał się i zgłosił.

### 2473-A-1 (narzędzie akceptacji lokalnej ze Stripe — zegary testowe) — 2026-10-13
- Archetyp: Konfiguracja / DevOps — skrypt sesji do akceptacji na sandboxie operatora
- Stawka: średnia (sandbox, bez danych produkcyjnych)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access write` (12,3 min)
- Recenzent (linia / model / native effort): architekt — przebieg akceptacji 6 scenariuszy
- Dopuszczone alternatywy: `wykonawca` Sonnet `high`
- Powód wyboru: narzędzie poza repo produktu, tekstowy brief
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark nieznany
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowany
- Rundy korekt: 0
- Czas do akceptacji: 12 min + akceptacja
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): n/d
- Defekty po odbiorze: brak
- Wymagane testy i dowody: akceptacja lokalna — 6 scenariuszy PASS (jedno samonaprawialne odchylenie: zwolnienie harmonogramu przy blokadzie zegara testowego + 429)
- Uwaga o specyfikacji: brak.

### 2473-GATE (bramka końcowa `gpt-6.1-sol` `max` — BE, potem FE) — 2026-10-13
- Archetyp: Recenzja — bramka końcowa funkcji high-stakes (cały diff repozytorium, tylko odczyt)
- Stawka: wysoka / high-stakes
- Niepewność: średnia
- Wykonawca (linia / model / native effort): n/d (recenzja)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `max`, `-Mode review` (BE 30,3 min; FE 2,1 min STOP + 5,1 min); od przebiegu 9 (2026-10-14, decyzja właściciela „nie czekajmy na limity” po `usage_limit_exceeded` Codexa w przebiegu 8): Meta / `muse-spark-1.3-contributor` / `max`, `-Access read` (przebieg 9: 23,1 min — P1 potwierdzone, P2 obalone; przebieg 10: 17,0 min — ZIELONA, pewność 0,85, 3 × P3)
- Dopuszczone alternatywy: brak — reguła 6
- Powód wyboru: obowiązkowa bramka reguły 6; Codex nie dostał w tej funkcji innego briefu
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper), bez komunikatu limitu
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: BE CZERWONA — 2 × P1 + 2 × P2, wszystkie potwierdzone przez architekta w kodzie; FE — pierwszy przebieg STOP na błędnej przesłance briefu, drugi ZIELONY, 0 znalezisk
- Rundy korekt: BE 8 (czerwone przebiegi 1–7 i 9 → BE-6, BE-7, BE-8/9, BE-10, BE-11, BE-12/13, BE-15, BE-16; przebieg 8 przerwany limitem Codexa); FE 0
- Czas do akceptacji: BE 2026-10-13 → 2026-10-14 (10 przebiegów, w tym 2 na Sparku: 23,1 + 17,0 min); FE ~7 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): potwierdzone: P1 spóźniona opłacona faktura odnowienia ≠ ostatnia faktura subskrypcji ginęła bez alarmu; P1 zwrot odrzucony przed zapisem jako wykonany → ponowienie klucza idempotencji zapisywało fałszywy zwrot; P2 zwolnienie harmonogramu poza blokadą mogło usunąć nowy plan; P2 sam nierozpoznany stan zwrotu bez alarmu; odrzucone 0
- Defekty po odbiorze: brak (stan przed wdrożeniem PRE)
- Wymagane testy i dowody: każde P1 potwierdzone scenariuszem w kodzie przed poprawką
- Uwaga o specyfikacji: wszystkie cztery znaleziska to przypadki spoza planu architekta; recenzje fal (Spark/Gemini, 16 przebiegów) ich nie zgłosiły — kolejny argument za bramką raz na funkcję.

### 2473-BE-6 (poprawki po bramce — 6a, 6a-2, 6b, 6b-K1) — 2026-10-13
- Archetyp: Backend — poprawki niezmienników po bramce (lustro faktury ze zdarzenia, dopasowanie pod blokadą, zwrot odrzucony przed zapisem, stan nierozpoznany)
- Stawka: wysoka / high-stakes
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh` (6a 8,4 min → przekazanie przy 317 tys.; 6a-2 8,9 min; 6b 16,4 min, 314 tys.; 6b-K1 10,6 min)
- Recenzent (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access read` (R-BE-6 9,6 min)
- Dopuszczone alternatywy: wykonawca — brak; recenzent — Gemini `high`
- Powód wyboru: pliki niezmiennika; recenzja wyższej stawki
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook ŻÓŁTY); Spark nieznany
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: 6b zaakceptowany po korekcie zakresu a2 (6b-K1: tylko przy rezygnacji w toku, gałąź resztkowa jako ostrzeżenie)
- Rundy korekt: 1 (6b-K1)
- Czas do akceptacji: ~44 min wykonania + recenzja 9,6 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R-BE-6 ✓ ZGODNE 0,85 — 4/4 znaleziska bramki zamknięte; P3 (przybliżenie „zwrot zlecony przez system”) potwierdzone, opisane komentarzem SQL i zdaniem dokumentacji (architekt, reguła 11); odrzucone 0
- Defekty po odbiorze: brak
- Wymagane testy i dowody: filtr 2554 → 2580 po testach T-3; pełny `dotnet test` po T-3c
- Uwaga o specyfikacji: brief BE-6b-K1 zakładał istniejące testy gałęzi resztkowej — ich nie było, przeniesione do T-3c.

### 2473-T-3 (testy poprawek po bramce — T-3a lustro, T-3b SQL i ocena, T-3c procesor i przepływ; `tester-haiku`) — 2026-10-13
- Archetyp: Testy — xunit jednostkowe i na prawdziwym SQL Server, mutacje produkcji
- Stawka: wysoka / high-stakes (dowody poprawek bramki; pliki testów bez niezmiennika produkcji)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Claude / `tester-haiku` — Haiku 5.5 / `xhigh` (T-3a 13,6 min, 371 tys.; T-3b 9,7 min, 37 wywołań; T-3c 14,1 min, 48 wywołań, 332 tys. — próg miękki przekroczony, dokończony bez przekazania)
- Recenzent (linia / model / native effort): architekt — mutacje produkcji przed i po, `cmp` przywróconych plików; zmiany testów czyta bramka nie ponownie (poprawki po bramce)
- Dopuszczone alternatywy: Spark `max` `-Access write`
- Powód wyboru: pierwszy brief po przejęciu linii testera przez Haiku (próba zamknięta 3:3)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook ŻÓŁTY, 5 h 42–43 %)
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: T-3a — mutacja M2 z `if (true)` i `#pragma` (przywrócona, produkcja czysta); T-3b zaakceptowany bez uwag (M3–M5 czerwone, mutacja `IF @Reverted = 0` równoważna); T-3c zaakceptowany (M6 → 3 czerwone, M7 → 1 czerwony; jedyne pokrycie gałęzi resztkowej procesora)
- Rundy korekt: 0
- Czas do akceptacji: ~37 min wykonania w trzech briefach + walidacje architekta
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): n/d — uwagi wykonawców o specyfikacji: T-3b 7 (2 przyjęte: brak asercji w istniejącym teście → T-3c, brak dowodu mutacyjnego S7 → mutacja równoważna), T-3c 10 (uwaga o korektach w gałęzi a2 rozstrzygnięta przez SQL)
- Defekty po odbiorze: 0 (bramka przebiegi 2–3 bez znalezisk w testach T-3)
- Wymagane testy i dowody: filtr 2554 → 2565 → 2580 → 2586; build `--no-incremental` 0/0, pełny `dotnet test` 6706/6706 z SQL, pominięto 0; mutacje M1–M7 czerwone, przywrócenia `cmp` identyczne
- Uwaga o specyfikacji: pułapki mutacji (stara data modyfikacji przywróconego pliku, `return` na początku metody, nazwy czerwonych testów tylko w `verbosity=normal`) dopisywane do kolejnych briefów — T-3b i T-3c bez tych błędów.

### 2473-BE-7 (cykle tła przechodzą całą zaległość — stronicowanie kluczem, po przebiegu 2 bramki) — 2026-10-13
- Archetyp: Backend — dwa cykle tła i ich zapytania SQL (kursor), bezpiecznik postępu, testy SQL i jednostkowe, mutacje
- Stawka: wysoka / high-stakes (cichy błąd cyklu lustra płatności i dokończenia zwrotu gwarancji)
- Niepewność: średnia (plan zapytania z kursorem, pętla bez postępu)
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh` (31,7 min, 86 wywołań, 354 tys. — próg miękki przekroczony, dokończony bez przekazania)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `max`, `-Mode review` — przebieg 3 bramki na całym diffie jako recenzja fali (inna rodzina niż Opus; bez dublowania osobnym recenzentem)
- Dopuszczone alternatywy: wykonawca — brak (przy CZERWONYM Spark `max`); recenzent — Spark `max` / Gemini `high` (odrzucone jako dublowanie przebiegu 3)
- Powód wyboru: pliki niezmiennika; jeden brief na oba cykle, bo to ta sama klasa błędu
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook ŻÓŁTY, 5 h 0–6 % po resecie)
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany z wykonania; wykonawca zmierzył plany zapytań i wybrał postać z dolną granicą zamiast dosłownego `OR` z briefu (dosłowna skanowałaby indeks od początku przy każdej stronie)
- Rundy korekt: 0 (4 komentarze poprawione przez architekta, reguła 11)
- Czas do akceptacji: 31,7 min + walidacja ~10 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): przebieg 3 bramki — P2 przebiegu 2 zamknięte, w plikach BE-7 brak nowych znalezisk
- Defekty po odbiorze: 0
- Wymagane testy i dowody: build `--no-incremental` 0/0, pełny `dotnet test` 6723/6723 z SQL, mutacje K1–K4 + K4b czerwone, atrapy ograniczone sekwencją (żaden test nie zawisa)
- Uwaga o specyfikacji: postać SQL z briefu psuła plan — brief dopuszczał postać równoważną; wykonawca wykrył fałszywe twierdzenie o indeksie pokrywającym, obecne od fali 1 w migracji i diagramie.

### 2473-BE-8 (anulowanie najpierw odzwierciedla odnowienie — P1 przebiegu 3 bramki) — 2026-10-13
- Archetyp: Backend — handler komendy właściciela z lustrem pod blokadą, kroki po blokadzie, testy jednostkowe i API z prawdziwym lustrem, mutacje
- Stawka: wysoka / high-stakes (miejsca, cena, zawieszenia programów i liczba miejsc u operatora płatności)
- Niepewność: średnia (wyścig odnowienia z anulowaniem, kontrakt kroków po zatwierdzeniu)
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh` (28,6 min, 70 wywołań, 304 tys.)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `max`, `-Mode review` — przebieg 4 bramki na całym diffie jako recenzja fali (inna rodzina niż Opus; bez dublowania)
- Dopuszczone alternatywy: wykonawca — brak (przy CZERWONYM Spark `max`); recenzent — Spark `max` / Gemini `high` (odrzucone jako dublowanie przebiegu 4)
- Powód wyboru: plik niezmiennika (anulowanie × zaplanowana zmiana × odnowienie)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook 2026-10-13 ~21:15: 5 h 9 %, tydzień 61 %)
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany z wykonania; wykonawca obalił założenie mutacji M1 (drugi przebieg z kroku wyścigu sam domyka scenariusz bramki) i dołożył test API „zakończona u operatora → 409 bez operatora”, który M1 czerwieni; wskazał ryzyko tokenu żądania przy krokach po sukcesie
- Rundy korekt: 0 z wykonania; 1 zmiana z winy specyfikacji (token żądania → `CancellationToken.None` przy sukcesie: linia architekta + 5 asercji przez `mechanik`)
- Czas do akceptacji: 28,6 min + walidacja ~8 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): przebieg 4 bramki — P1-3 zamknięte (anulowanie najpierw odzwierciedla odnowienie); w plikach BE-8 brak nowych znalezisk; odrzucone 0
- Defekty po odbiorze: brak — wdrożenie PRE i test dymny 2026-10-14 zielone (FE 1.4.0, BE 1.5.0)
- Wymagane testy i dowody: build 0/0, filtr 2624/2624 z SQL, pełny 6744/6744 (raport wykonawcy), mutacje M1/M2/M3 (+M1+M3) czerwone, CRLF
- Uwaga o specyfikacji: brief kazał przekazać token żądania krokom po sukcesie — błąd architekta (zerwane połączenie gubiło dopasowanie operatora, którego kolejne lustro nie odtworzy); wykonawca użył raz `sed -i.bak` wbrew zakazowi (bez śladu w repo).

### 2473-BE-9 (znacznik faktury odnowienia czekającej na rozstrzygnięcie — P2 przebiegu 3 bramki, część produkcyjna) — 2026-10-13
- Archetyp: Backend — pisarz lustra w transakcji (ustaw/wyczyść znacznik, alarm), migracja kolumny i indeksu, repozytoria i SQL
- Stawka: wysoka / high-stakes (płatność odnowienia — zapis pieniędzy klienta)
- Niepewność: średnia (kolejność obciążenia faktury u operatora, wyścig zdarzeń)
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh` (13,1 min, 67 wywołań, 322 tys. — strażnik kontekstu na 300 tys.)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `max`, `-Mode review` — przebieg 4 bramki jako recenzja fali (bez dublowania)
- Dopuszczone alternatywy: wykonawca — brak (przy CZERWONYM Spark `max`); recenzent — Spark `max` / Gemini `high` (odrzucone jako dublowanie)
- Powód wyboru: plik niezmiennika (zapis płatności odnowienia)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook 2026-10-13 ~22:00: 5 h 17 %, tydzień 62 % przy 39 % tygodnia, ŻÓŁTY)
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: przekazanie po strażniku — produkcja bez cyklu gotowa i odebrana przez architekta (pisarz 2a–2d, SQL, migracja, opcja); cykl i wszystkie testy przeszły do BE-9b (cykl, `wykonawca-opus`), BE-9c i BE-9d (testy, `tester`)
- Rundy korekt: 0 z wykonania; przekazanie z winy specyfikacji (zakres za duży na jeden brief — wykonawca to wskazał)
- Czas do akceptacji: 13,1 min (BE-9) + BE-9b/9c/9d osobno; walidacja pełna po BE-9d ~6 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): przebieg 4 bramki — P2-3 zamknięte dla gałęzi odnowienia; nowe P2-4 (faktura odnowienia nierozstrzygnięta bez znacznika przy końcu, odroczonym końcu i przebiegu bez zmian) potwierdzone — luka zakresu briefu architekta, nie wykonania → BE-10; odrzucone 0
- Defekty po odbiorze: brak — wdrożenie PRE i test dymny 2026-10-14 zielone (FE 1.4.0, BE 1.5.0)
- Wymagane testy i dowody: build 0/0; filtr 2594/2630 z 36 oczekiwanymi czerwonymi (ścisła atrapa pisarza); CRLF
- Uwaga o specyfikacji: wykonawca słusznie wskazał (1) wymóg `@AccountId` w SQL lustra z kontraktu repozytorium, (2) brak decyzji, którym repozytorium czyścić pozycję odpiętą, (3) pominięcie 36 testów pisarza w zakresie dostosowania, (4) mylący tekst alarmu dla pozycji odpiętej (rozstrzygnięte w BE-9b parametrem {Stan}), (5) za duży zakres jak na jeden brief.

### 2473-BE-9b (drugi przebieg cyklu uzgadniającego — faktury odnowienia czekające na rozstrzygnięcie) — 2026-10-13
- Archetyp: Backend — cykl tła (stronicowanie kluczem, bezpiecznik postępu, token zatrzymania, alarm i czyszczenie), testy jednostkowe cyklu, mutacje
- Stawka: wysoka / high-stakes (płatność odnowienia — alarm płatności niezapisanej)
- Niepewność: niska (wzorzec stron BE-7)
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh` (14,6 min, 39 wywołań, 248 tys.; korekta: 20,5 min, 26 wywołań, do 288 tys.)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `max`, `-Mode review` — przebieg 4 bramki jako recenzja fali (bez dublowania)
- Dopuszczone alternatywy: wykonawca — brak (przy CZERWONYM Spark `max`); recenzent — Spark `max` / Gemini `high` (odrzucone jako dublowanie)
- Powód wyboru: plik niezmiennika (cykl, który ma zapisać płatność albo podnieść alarm)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook 2026-10-13 ~22:20: 5 h 19–23 %, tydzień 63 %, ŻÓŁTY)
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany z wykonania (32/32 testów cyklu, N2 + 5 dodatkowych mutacji czerwone); 1 korekta z winy specyfikacji — wspólne podsumowanie uzależniało alarm zbiorczy pierwszego przebiegu od powodzenia drugiego (wykonawca to zasygnalizował); po korekcie 33/33, R9 + mutacja czerwona
- Rundy korekt: 0 z wykonania; 1 z winy specyfikacji
- Czas do akceptacji: 14,6 + 20,5 min + walidacja ~5 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): przebieg 4 bramki — P2-3 zamknięte dla gałęzi odnowienia; nowe P2-4 (faktura odnowienia nierozstrzygnięta bez znacznika przy końcu, odroczonym końcu i przebiegu bez zmian) potwierdzone — luka zakresu briefu architekta, nie wykonania → BE-10; odrzucone 0
- Defekty po odbiorze: brak — wdrożenie PRE i test dymny 2026-10-14 zielone (FE 1.4.0, BE 1.5.0)
- Wymagane testy i dowody: build 0/0 (architekt), testy cyklu 33/33 (architekt), filtr 2613/2649 z 36 oczekiwanymi czerwonymi `SubscriptionStateMirrorTests.*` (architekt), CRLF
- Uwaga o specyfikacji: wykonawca wskazał limit 100 w istniejących testach stronicowania (rozmiar strony testu) i niespójny przedrostek wpisów — oba przyjęte.

### 2473-BE-9c (testy pisarza lustra — znacznik faktury odnowienia: harness, 36 testów, P1–P9, mutacje) — 2026-10-13
- Archetyp: Testy BE — xUnit + Moq na ścisłej atrapie, dostosowanie istniejących testów do nowych wywołań, nowe przypadki, mutacje
- Stawka: wysoka (testy niezmiennika płatności odnowienia; plik testów bez niezmiennika)
- Niepewność: niska (wzorce harnessu)
- Wykonawca (linia / model / native effort): Claude / `tester` — Haiku 5.5 / `xhigh` (13,9 min, 38 wywołań, 368 tys. — powyżej progu 300 tys., bez kontynuacji)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `max`, `-Mode review` — przebieg 4 bramki (bez dublowania)
- Dopuszczone alternatywy: wykonawca — `wykonawca-opus` (droższy, odrzucony przy ŻÓŁTYM), Spark `max`; recenzent — Spark `max` / Gemini `high` (dublowanie)
- Powód wyboru: testy wg wzorców harnessu, linia `tester` po próbie 2026-10-13; ŻÓŁTY hook — Opus tylko na pliki niezmiennika
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook 2026-10-13 ~22:45: 5 h 23–24 %, tydzień 63 %, ŻÓŁTY)
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowany z wykonania; 36 → 0 czerwonych, 13 nowych przypadków, N1 (5 czerwonych) i N1b (9 czerwonych), `cmp` pisarza zgodny; wyrywkowy przegląd P1/P4 — asercje dokładne
- Rundy korekt: 0
- Czas do akceptacji: 13,9 min + walidacja ~4 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): przebieg 4 bramki — P2-3 zamknięte dla gałęzi odnowienia; nowe P2-4 (faktura odnowienia nierozstrzygnięta bez znacznika przy końcu, odroczonym końcu i przebiegu bez zmian) potwierdzone — luka zakresu briefu architekta, nie wykonania → BE-10; odrzucone 0
- Defekty po odbiorze: brak — wdrożenie PRE i test dymny 2026-10-14 zielone (FE 1.4.0, BE 1.5.0)
- Wymagane testy i dowody: build `--no-incremental` 0/0 (architekt), filtr 2662/2662 z SQL (architekt), CRLF
- Uwaga o specyfikacji: N1 literalnie nie buduje się (S1144 — metoda nieużywana; wykonawca zachował wywołanie); P9 przez orkiestrację nieosiągalny (`AlreadyEnded` przed operatorem — zrobiony na poziomie pisarza); pomocnik wyliczający niepotrzebny dla (b).

### 2473-BE-9d (testy SQL znacznika, scenariusz bramki end-to-end cyklu, mutacje, pełny przebieg) — 2026-10-13
- Archetyp: Testy BE — `[SqlServerFact]` na własnej bazie, end-to-end z prawdziwym lustrem, pisarzem, cyklem i repozytoriami (atrapa operatora), mutacje SQL i cyklu
- Stawka: wysoka (testy niezmiennika płatności odnowienia; pliki testów bez niezmiennika)
- Niepewność: średnia (złożenie prawdziwego lustra bez hosta)
- Wykonawca (linia / model / native effort): Claude / `tester` — Haiku 5.5 / `xhigh`; część 1: 10,0 min, 31 wywołań, 321 tys. (strażnik — przekazanie); część 2 (świeży agent z przekazaniem): 19,0 min, 53 wywołania, 338 tys.
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `max`, `-Mode review` — przebieg 4 bramki (bez dublowania)
- Dopuszczone alternatywy: wykonawca — `wykonawca-opus` (ŻÓŁTY, nie plik niezmiennika), Spark `max`; recenzent — Spark `max` / Gemini `high` (dublowanie)
- Powód wyboru: testy wg wzorców, linia `tester`; ŻÓŁTY hook
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook 2026-10-13 ~23:00–23:20: 5 h 25–27 %, tydzień 63–64 %, ŻÓŁTY)
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowany po kontynuacji; SQL 16 testów, E2E 2 testy zielone od razu (scenariusz na odebranym kodzie); N2 27 czerwonych (oba E2E + 25 cyklu), N3 → S4, N3b → C1, N4 → L1 ×2, L5, E2E; przywrócenia `fc.exe /b` zgodne
- Rundy korekt: 0 z wykonania; architekt zaostrzył jedną asercję (`Times.AtMostOnce` → `Times.Once` na dopasowaniu operatora — luka wskazana przez wykonawcę, z winy specyfikacji przekazania; reguła 11)
- Czas do akceptacji: 29 min + walidacja ~6 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): przebieg 4 bramki — P2-3 zamknięte dla gałęzi odnowienia; nowe P2-4 (faktura odnowienia nierozstrzygnięta bez znacznika przy końcu, odroczonym końcu i przebiegu bez zmian) potwierdzone — luka zakresu briefu architekta, nie wykonania → BE-10; odrzucone 0
- Defekty po odbiorze: brak — wdrożenie PRE i test dymny 2026-10-14 zielone (FE 1.4.0, BE 1.5.0)
- Wymagane testy i dowody: build `--no-incremental` 0/0 (architekt), pełny `dotnet test` 6800/6800 z SQL (architekt), E2E 2/2 po zaostrzeniu (architekt), CRLF
- Uwaga o specyfikacji: brief podał N2 w formie niekompilowalnej, L3 bez izolacji gałęzi (odpięta w produkcji zawsze zakończona), bez czyszczenia stanu klasy listy, `cmp` niedostępny w PowerShell; przekazanie architekta dało `Times.AtMostOnce` (słaba asercja). Kontynuacja po strażniku bez rund korekty.

### 2473-BE-10 (znacznik nierozstrzygniętej faktury odnowienia także przy końcu, odroczonym końcu i przebiegu bez zmian — P2 przebiegu 4 bramki) — 2026-10-14
- Archetyp: Backend — pisarz lustra w transakcji (nowy krok zapisu znacznika i alarm), testy na ścisłej atrapie, e2e na prawdziwej bazie, mutacja
- Stawka: wysoka / high-stakes (płatność odnowienia przy rezygnacji z pełnym zwrotem)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh` (16,6 min, 64 wywołania, 275 tys.)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `max`, `-Mode review` — przebieg 5 bramki jako recenzja fali (bez dublowania)
- Dopuszczone alternatywy: wykonawca — brak (przy CZERWONYM Spark `max`); recenzent — Spark `max` / Gemini `high` (dublowanie)
- Powód wyboru: plik niezmiennika (pisarz lustra — płatność odnowienia)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook 2026-10-13 ~23:50: 5 h 28–31 %, tydzień 64 %, ŻÓŁTY)
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany z wykonania; W1–W5, W7 + e2e scenariusz 3; M10 czerwieni W1–W5, e2e 3 i Payment open/draft; `fc` zgodny
- Rundy korekt: 0
- Czas do akceptacji: 16,6 min + walidacja ~5 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): przebieg 5 — bez regresji w BE-10; 1 × P2 potwierdzone (usunięcie konta przed odzwierciedleniem odnowienia) — droga spoza zakresu briefu (luka specyfikacji architekta, nie wykonania) → BE-11; 0 odrzuconych
- Defekty po odbiorze: brak — wdrożenie PRE i test dymny 2026-10-14 zielone (FE 1.4.0, BE 1.5.0)
- Wymagane testy i dowody: build `--no-incremental` 0/0 (architekt), pełny `dotnet test` 6807/6807 z SQL (architekt), CRLF
- Uwaga o specyfikacji: błędna przesłanka o P7c (tam `LatestInvoice` NULL — test słusznie bez zapisu); W6 dublował P8; tekst alarmu (c) „do kolejnego odnowienia” przy (b′) — architekt zostawił (zamiana znacznika wymaga nowszej faktury cyklicznej u operatora); S1200 pisarza na granicy 30.

### 2473-BE-11 (alarm przy usunięciu konta po minionym zapisanym okresie — P2 przebiegu 5 bramki) — 2026-10-14
- Archetyp: Backend — handler przekrojowy (usunięcie konta) z alarmem krytycznym, testy na atrapach z rejestrującym loggerem, mutacja
- Stawka: wysoka / high-stakes (płatność odnowienia przy usunięciu konta)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh` (13,3 min, 41 wywołań, 195 tys.)
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `max`, `-Mode review` — przebieg 6 bramki jako recenzja fali (bez dublowania)
- Dopuszczone alternatywy: wykonawca — brak (przy CZERWONYM Spark `max`); recenzent — Spark `max` / Gemini `high` (dublowanie)
- Powód wyboru: plik niezmiennika (usunięcie konta — płatność odnowienia, alarm)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook 2026-10-14 ~00:20: 5 h 32 %, tydzień 64 %, ŻÓŁTY); Codex nieznany
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany z wykonania; D1–D6, K1–K4 czerwienią oczekiwane testy (K1/K2 także D6), `fc` zgodny
- Rundy korekt: 0 z wykonania; 1 korekta specyfikacji w trakcie przebiegu (architekt: odczyt chwili po zakończeniu u operatora — wykonawca zauważył okno sam, przed korektą)
- Czas do akceptacji: 13,3 min + walidacja ~4 min
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): przebieg 6 — BE-11 domyka scenariusz przebiegu 5 (potwierdzone); 0 znalezisk w plikach BE-11; P2-6b to analogiczna droga w `RefundGuaranteeProcess` (luka specyfikacji architekta) → BE-13; 0 odrzuconych
- Defekty po odbiorze: brak — wdrożenie PRE i test dymny 2026-10-14 zielone (FE 1.4.0, BE 1.5.0)
- Wymagane testy i dowody: build `--no-incremental` 0/0 (architekt), pełny `dotnet test` 6813/6813 z SQL (architekt), CRLF
- Uwaga o specyfikacji: pierwotny odczyt chwili na początku fazy zostawiał okno odnowienia w trakcie wywołania operatora (błąd architekta, poprawiony korektą); uwaga wykonawcy o fałszywym alarmie przy `past_due` odrzucona (lustro przesuwa okres niezależnie od płatności); alarm pada w istniejących testach z domyślnym `CurrentPeriodEndsAt` (szum w logach testów, bez asercji).

### 2473-4C-B (Faza 4c — zgodność dokumentacji z kodem, grupa B: konto, anulowanie, ustawienia, usunięcie konta, FE) — 2026-10-14
- Archetyp: Przegląd zgodności dokumentacji z implementacją (odczyt, dwa repozytoria + dokumentacja)
- Stawka: średnia (dokumenty bez niezmiennika pieniędzy; niezmienniki pilnuje bramka Sol)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (7,6 min; pierwszy przebieg przerwany końcem sesji, bez wyniku)
- Recenzent (linia / model / native effort): architekt — próbka twierdzeń (napisy D1 w `pl.json`/`en.json` wobec UI-KONTO-USTAWIENIA rew. 2026-10-13 pkt 1)
- Dopuszczone alternatywy: Spark `max` read (zajęty grupą A), Sol `high` (pula Codexa dla bramki)
- Powód wyboru: inna rodzina niż autor zmian dokumentacji (Claude); niska stawka grupy — preferencja Gemini `high` wg reguły 13
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany (brak komunikatu limitu), 2026-10-14 08:25
- Pewność decyzji: średnia
- Wynik pierwszego podejścia: zaakceptowany — 0 rozbieżności, 52 twierdzenia zgodne w 11 sekcjach; 2 uwagi do briefu (niejednoznaczne „brak” w opisie D; „Wstrzymana” to stan techniczny — trafne)
- Rundy korekt: 0
- Czas do akceptacji: 7,6 min + ~3 min próbki
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 / 0
- Defekty po odbiorze: brak
- Wymagane testy i dowody: macierz zgodności (format Fazy 4c), próbka architekta
- Uwaga o specyfikacji: pliki wejściowe muszą leżeć w `D:\projects\DTCode` (uprawnienie `read_file` agy) — scratchpad na C: niewidoczny.

### 2473-4C-A (Faza 4c — zgodność dokumentacji z kodem, grupa A: lustro, zwroty, cykle, faktury) — 2026-10-14
- Archetyp: Przegląd zgodności dokumentacji z implementacją (odczyt, BE + dokumentacja)
- Stawka: wysoka (dokumenty niezmienników pieniędzy)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max`, `-Access read` (29,2 min; dwa wcześniejsze przebiegi bez wyniku — koniec sesji i aktualizacja WSL)
- Recenzent (linia / model / native effort): architekt — każdy z 6 wierszy sprawdzony w kodzie i dokumencie
- Dopuszczone alternatywy: Gemini `high` read (gdyby WSL nie wrócił), Sol `high` (pula Codexa dla bramki)
- Powód wyboru: inna rodzina niż autor zmian dokumentacji (Claude); wyższa stawka grupy — Spark `max`
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark nieznany; przebieg 2 przerwany aktualizacją WSL (`ERROR_INSTALL_ALREADY_RUNNING`), 2026-10-14 ~08:34
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany — 0 × „kod odbiega”, 6 × „brak w dokumencie”: 5 potwierdzonych (R1, R3–R6), 1 doprecyzowanie (R2 — produktowo pokryte w UI-KONTO-USTAWIENIA); wszystkie domknięte zdaniami w rewizjach 2026-10-13
- Rundy korekt: 0
- Czas do akceptacji: 29,2 min + ~10 min triażu
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 5 potwierdzonych / 0 odrzuconych / 1 doprecyzowanie
- Defekty po odbiorze: brak
- Wymagane testy i dowody: macierz zgodności, triaż architekta w plikach
- Uwaga o specyfikacji: indeks plików zawiera ścieżki sprzed przeniesienia trzech plików do `RefundCompletion/` (pokrycie niezagrożone); opis „Gwarancja (14 dni na zwrot)” w tabeli mylił okno 30 dni z terminem zwrotu 14 dni.

### 2473-BE-12 (poprawka bramki przebieg 6: alarmy 6a i 6c w pisarzu lustra) — 2026-10-14
- Archetyp: Poprawka po bramce końcowej — alarmy niezmiennika płatności (BE, lustro subskrypcji)
- Stawka: wysoka (niezmiennik 14: opłacona faktura odnowienia → płatność albo alarm krytyczny)
- Niepewność: średnia
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 `xhigh` (19,9 min, 91 wywołań, ~291 tys. kontekstu)
- Recenzent (linia / model / native effort): bramka końcowa `gpt-6.1-sol` `max` przebieg 7 (recenzja fali tej poprawki)
- Dopuszczone alternatywy: brak (twarda bramka — plik niezmiennika)
- Powód wyboru: pliki niosące niezmiennik płatności; przy ŻÓŁTYM Opus dopuszczony
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (ŻÓŁTY, 5 h ~7 %, tydzień 66 %), hook `[limity Claude]`, 2026-10-14
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany — build 0/0, 6827/6827, mutacje N1–N4 czerwone zgodnie z oczekiwaniem; jedno oczekiwanie istniejącego testu zmienione zasadnie (odnowienie z fakturą poprzedniego okresu daje teraz alarm 6a)
- Rundy korekt: 0
- Czas do akceptacji: 19,9 min + ~25 min walidacji (w tym próba operatora)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): przebieg 7 bramki — P2-6a/6b/6c zamknięte, w plikach poprawki brak regresji; nowe P2-7 (przestarzała lokalna flaga anulowania wyłączała alarm końca) potwierdzone → BE-15; odrzucone 0
- Defekty po odbiorze: brak — wdrożenie PRE i test dymny 2026-10-14 zielone (FE 1.4.0, BE 1.5.0)
- Wymagane testy i dowody: testy jednostkowe R1–R8 (14 przypadków), mutacje N1–N4, pełny przebieg, CRLF
- Uwaga o specyfikacji: wykonawca wskazał (sekcja „What do you consider wrong”), że faktura przejścia harmonogramu może nie mieć `subscription_cycle` — architekt potwierdził próbą w trybie testowym operatora (`subscription_update`); to defekt BE-1 (luka specyfikacji architekta: brief BE-1 zdefiniował fakturę odnowienia po samym `subscription_cycle`, choć #1603 dokumentował `subscription_update` w `SubscriptionScheduleValues.cs`) → BE-14. Data w alarmie 6c bez „Z” — zaakceptowane (spójne z alarmem BE-11, baza w UTC).
- Do uzupełnienia przy zamknięciu: we wpisie BE-1 w rejestrze — „Defekty po odbiorze: odnowienie ze zmianą okresu (`subscription_update`) bez płatności — wykryte 2026-10-14 przez wykonawcę BE-12, naprawione w BE-14”.

### 2473-BE-13 (poprawka bramki przebieg 6: alarm dokończenia rezygnacji po minionym okresie + wspólny warunek) — 2026-10-14
- Archetyp: Poprawka po bramce końcowej — alarm niezmiennika płatności, refaktor warunku do jednego miejsca (BE)
- Stawka: wysoka (zwrot gwarancji, niezmiennik 14)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 `xhigh` (31,9 min, 51 wywołań, ~241 tys. kontekstu)
- Recenzent (linia / model / native effort): bramka końcowa `gpt-6.1-sol` `max` przebieg 7 (recenzja fali tej poprawki)
- Dopuszczone alternatywy: brak (twarda bramka — plik niezmiennika)
- Powód wyboru: plik niezmiennika zwrotu gwarancji; przy ŻÓŁTYM Opus dopuszczony
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (ŻÓŁTY, 5 h ~8 %, tydzień 66 %), hook `[limity Claude]`, 2026-10-14
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany — build 0/0, pełny przebieg zielony (6841), mutacje L1–L4 czerwone; dane testowe konstruktora poprawione zasadnie (koniec okresu `default` spełniał nowy warunek)
- Rundy korekt: 0
- Czas do akceptacji: 31,9 min + ~20 min walidacji (diagnoza testu niestabilnego)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): przebieg 7 bramki — P2-6a/6b/6c zamknięte, w plikach poprawki brak regresji; nowe P2-7 (przestarzała lokalna flaga anulowania wyłączała alarm końca) potwierdzone → BE-15; odrzucone 0
- Defekty po odbiorze: brak — wdrożenie PRE i test dymny 2026-10-14 zielone (FE 1.4.0, BE 1.5.0)
- Wymagane testy i dowody: F1–F5, 8 przypadków granicznych warunku, mutacje L1–L4, pełny przebieg, CRLF
- Uwaga o specyfikacji: wykonawca zgłosił jeden niezidentyfikowany czerwony test w 1 z 13 przebiegów — architekt odtworzył go w pełnym przebiegu (`AccountDeletionOpenCheckoutApiTests.Delete_WithOpenCheckout_ExpiredOnClose_…`) i ustalił przyczynę: `ExecutedAt` bez `DbType.DateTime2` (zaokrąglenie `datetime`), odsłonięte przez BE-11 — luka specyfikacji BE-11 (brief nie przewidział wpływu przesunięcia odczytu czasu na istniejące porównania chwil); poprawka jednej linii przez architekta. Oczekiwanie przy L4 (testy usunięcia konta) było nietrafne — granicę pilnuje wyłącznie test jednostkowy równości.

### 2473-BE-14 (faktura odnowienia ze zmianą okresu rozliczenia — `subscription_update`) — 2026-10-14
- Archetyp: Poprawka defektu wykrytego po odbiorze — kryterium faktury odnowienia w lustrze i routingu webhooka (BE)
- Stawka: wysoka (zapis płatności odnowienia, niezmiennik 14)
- Niepewność: średnia (kształt faktury operatora — rozstrzygnięty próbą architekta w trybie testowym)
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 `xhigh`; przebieg 1: kod + testy (13,7 min, 93 wywołania, ~326 tys., przekazanie przy 304 tys.); kontynuacja BE-14b: mutacje M1–M4 i 2 pełne przebiegi (13,7 min, 37 wywołań, ~168 tys.)
- Recenzent (linia / model / native effort): bramka końcowa `gpt-6.1-sol` `max` przebieg 7 (recenzja fali tej poprawki)
- Dopuszczone alternatywy: brak (twarda bramka — plik niezmiennika)
- Powód wyboru: pliki niosące niezmiennik płatności; kontynuacja tej samej linii wg reguły 15
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (ŻÓŁTY, 5 h 15–21 %, tydzień 67 %), hook `[limity Claude]`, 2026-10-14
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany po kontynuacji — predykat `IsRenewalReason` w 4 miejscach, `grep` czysty; M1–M4 dały dokładnie przewidziane czerwone; 4 oczekiwania istniejących testów zmienione zasadnie (`subscription_update` było w nich błędnie uznane za dopłatę)
- Rundy korekt: 0 (jedno przekazanie przy progu kontekstu)
- Czas do akceptacji: ~28 min pracy wykonawców + ~25 min architekta (próba operatora, walidacja)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): przebieg 7 bramki — P2-6a/6b/6c zamknięte, w plikach poprawki brak regresji; nowe P2-7 (przestarzała lokalna flaga anulowania wyłączała alarm końca) potwierdzone → BE-15; odrzucone 0
- Defekty po odbiorze: brak — wdrożenie PRE i test dymny 2026-10-14 zielone (FE 1.4.0, BE 1.5.0)
- Wymagane testy i dowody: G1–G3, P1–P2, routing, procesor, mutacje M1–M4, 2 pełne przebiegi, CRLF; lokalny e2e zmiany okresu (krok bramy)
- Uwaga o specyfikacji: zakaz `sed -i` złamany przez wykonawcę (podmiana poprawna, CRLF przywrócone, sprawdzone bajtowo); BE-14b wykrył błąd architekta przy poprawce testu niestabilnego (częściowe `DbType.DateTime2` rozjechało równość tej samej chwili) — cofnięte; kontrola CRLF przez `git diff --name-only` w briefie nie obejmowała plików nieśledzonych.

### 2473-BE-15 (alarm końca nie ufa lokalnej fladze anulowania — P2 przebiegu 7 bramki) — 2026-10-14
- Archetyp: Poprawka po bramce końcowej — warunek alarmu niezmiennika płatności (jedna linia) + odwrócenie testów (BE)
- Stawka: wysoka (płatność odnowienia przy usunięciu konta i rezygnacji z pełnym zwrotem, niezmiennik 14)
- Niepewność: niska
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 `xhigh` (10,5 min, 29 wywołań, ~166 tys.)
- Recenzent (linia / model / native effort): bramka końcowa `gpt-6.1-sol` `max` przebieg 8 (recenzja fali tej poprawki)
- Dopuszczone alternatywy: brak (twarda bramka — plik niezmiennika)
- Powód wyboru: plik niezmiennika (wspólny warunek alarmu płatności odnowienia)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (ŻÓŁTY, 5 h 25 %, tydzień 68 %), hook `[limity Claude]`, 2026-10-14
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: zaakceptowany — warunek bez flagi, 3 testy odwrócone, N1 czerwieni dokładnie te trzy, pełny przebieg 6849/6849
- Rundy korekt: 0 (architekt poprawił 2 zdania opisów XML wołających, które brief kazał zostawić — luka specyfikacji, zgłoszona przez wykonawcę)
- Czas do akceptacji: 10,5 min + ~5 min walidacji
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): przebieg 8 przerwany limitem Codexa (`usage_limit_exceeded`); recenzją fali był przebieg 9 bramki (Spark `max`) — P2-7 zamknięte, w plikach BE-15 brak nowych znalezisk; odrzucone 0
- Defekty po odbiorze: brak — wdrożenie PRE i test dymny 2026-10-14 zielone (FE 1.4.0, BE 1.5.0)
- Wymagane testy i dowody: N1, build `--no-incremental` 0/0, pełny `dotnet test` z SQL, CRLF
- Uwaga o specyfikacji: brief zakazał ruszania opisów XML w obu miejscach wołania, które powtarzały stary warunek — wykonawca słusznie to wytknął; uwaga wykonawcy, że „lustro kończy wygasłą przed usunięciem” to założenie o kolejności, nie blokada — zgodne z uzasadnieniem briefu (fałszywy alarm w oknie opóźnionego lustra akceptowany).

### 2473-QAS (przypadki QA Sphere — QAS-1 autor, R-QAS-1 recenzja krzyżowa, QAS-2 poprawki) — 2026-10-14
- Archetyp: Przypadki manualne QA Sphere — podgląd JSON wg skilla `qasphere-test-generator` v1.7 (nowe + przegląd 109 istniejących, Krok 2b)
- Stawka: średnia (dokumentacja testów, bez kodu produktu; błędne przypadki = fałszywe defekty u testera)
- Niepewność: średnia (stan danych PRE, scenariusze z SQL i Stripe Dashboard)
- Wykonawca (linia / model / native effort): Spark / `muse-spark-1.3-contributor` / `max` (procedura skilla)
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / `-Access read` (procedura skilla: plik Sparka → Gemini), 358 s
- Dopuszczone alternatywy: Gemini `-Access write` jako autor przy zajętym Sparku; brak innych (procedura skilla twarda)
- Powód wyboru: procedura pomocniczego skilla (autor Spark `max`, recenzja krzyżowa innej rodziny)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Spark i Gemini nieznany (wrappery bez zapasu), 2026-10-14
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: QAS-1 lint 0/0, 9 nowych, 30 `update`, 1 `retire`; 3 nowe przypadki (T1, T2, A2) i werdykt `keep` 1017 oparte na błędnej przesłance briefu architekta (`sub_stub_…` na kontach demo — na PRE `ProviderSubscriptionId` NULL), N1 przechodził niezależnie od badanej reguły
- Rundy korekt: 1 z winy specyfikacji (QAS-2, Spark `max`, 529 s — T1/N1/1017 na skryptach z identyfikatorem nieznanym operatorowi, T2 scalony z 1017; wykonawca słusznie obalił 2 przesłanki briefu: 5e — R1 już miał asercję etykiety, 5d — lista nie pokazuje stanu) + 1 mechaniczna architekta (QAS-3, Spark `low`, 90 s — strażnik `UPDATE` w skrypcie A; luka QAS-2 wychwycona przy odbiorze)
- Czas do akceptacji: QAS-1 + R-QAS-1 + QAS-2 + QAS-3 i akceptacja tabeli przez właściciela 2026-10-14; publikacja `push`/`verify` bez różnic
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R-QAS-1 — potwierdzone: P0 T1, P0 T2 (znane architektowi z faktu 1 briefu recenzenta), P1 1017 `keep`→`update`, P1 A2 (tytuł), P1 N1 (brak izolacji reguły), P2 E1 (dosłowne oznaczenie stanu, uznane jako P3), P3 R1 (warunkowo); odrzucone: 3 × P2 luki pokrycia (idempotencja — jest I1, odrzucony zwrot — jest R1, pełny cykl dokończenia — jest A1; recenzent źle odczytał R1 jako „sukces zwrotu”); cytaty kodu w recenzji częściowo zmyślone (sygnatury `WillRenew`, wyjątek z enum i komunikatem) — wnioski trafne, dowody nie
- Defekty po odbiorze: brak — wdrożenie PRE i test dymny 2026-10-14 zielone (FE 1.4.0, BE 1.5.0)
- Wymagane testy i dowody: `qas.py lint` 0/0, tabela dla właściciela, po akceptacji `push --limit 1` → `verify --only` → pełne `verify`
- Uwaga o specyfikacji: błędna przesłanka o danych PRE pochodziła z briefu architekta (nie sprawdzona zapytaniem przed briefem) — autor ją przyjął, recenzent wykrył; wniosek: fakty o danych PRE sprawdzać odczytem przed briefem przypadków

### 2473-BE-16 (wcześniejszy koniec subskrypcji anulowanej z końcem okresu — P1 przebiegu 9 bramki) — 2026-10-14
- Archetyp: Poprawka po bramce końcowej — warunek stanu końca w planerze lustra + przeklasyfikowanie testów (BE)
- Stawka: wysoka (stan subskrypcji, zawieszenie programów, alarm ingerencji poza systemem)
- Niepewność: niska (fakt operatora sprawdzony odczytem: 8 anulowań natychmiastowych + wygaśnięcie na zegarze testowym)
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 `xhigh` (2 podejścia: 6,1 min STOP + 6,5 min; 52 wywołania)
- Recenzent (linia / model / native effort): bramka końcowa Spark `muse-spark-1.3-contributor` `max` przebieg 10 (recenzja fali tej poprawki)
- Dopuszczone alternatywy: brak (twarda bramka — plik niezmiennika)
- Powód wyboru: plik niezmiennika (stan końca subskrypcji i zawieszenie programów)
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (ŻÓŁTY, 5 h 32 % → reset, tydzień 69 %), hook `[limity Claude]`, 2026-10-14
- Pewność decyzji: wysoka
- Wynik pierwszego podejścia: STOP słuszny — przesłanka briefu „istniejące testy zostają” fałszywa (fixture `EndedSnapshot()` modeluje koniec 5 s po starcie nowego okresu = przypadek przeklasyfikowany; 5 czerwonych testów W1/W6/R8/test 2/teoria); zmiana produkcyjna wykonana, testy wstrzymane do decyzji architekta
- Rundy korekt: 1 z winy specyfikacji (decyzje o znaczeniu 5 testów: B dla wygaśnięcia w terminie i R8, C dla W1/W6, nowy test wcześniejszego końca); 0 z winy wykonania
- Czas do akceptacji: ~13 min wykonania + ~10 min walidacji (pełny test 6856/6856)
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): przebieg 10 bramki (Spark `max`, 17,0 min) — P1-9 zamknięte, 0 nowych P0–P2; 3 × P3 poza modelem zagrożenia (cicha opłacona faktura `subscription_update` z samych proracji; brak progu alarmu dla nieczytelnej faktury znacznika; nieaktualny komentarz routingu — poprawiony przez architekta, reguła 11); odrzucone 0
- Defekty po odbiorze: brak — wdrożenie PRE i test dymny 2026-10-14 zielone (FE 1.4.0, BE 1.5.0)
- Wymagane testy i dowody: 3 mutacje (sama flaga → 8 czerwonych dokładnie przewidzianych; bez pełnych sekund → 1; koniec z bazy → 4), build `--no-incremental` 0/0, pełny `dotnet test` z SQL 6856/6856, CRLF
- Uwaga o specyfikacji: architekt nie sprawdził wspólnego fixture'u przed briefem — wykonawca wykrył i zatrzymał się zamiast „naprawić” testy po swojemu (wzorcowe zachowanie przy testach niezmiennika); dodatkowe 3 przypadki graniczne ponad brief, każdy dowodzi wymogu decyzji

### 2694-S (sondy operatora płatności na sandboxie: 0-S, SONDA-E) — 2026-10-14
- Archetyp: Konfiguracja / DevOps — narzędzie sondy poza repozytorium produktu, przebieg na zegarach testowych operatora.
- Stawka: średnia (sandbox; wynik rozstrzyga decyzje implementacji niezmiennika płatności).
- Niepewność: wysoka (zachowanie operatora przy zaległości nieudokumentowane, mierzone empirycznie).
- Wykonawca (linia / model / native effort): Muse / `muse-spark-1.3-contributor` / `max`, `-Access write` (oba briefy).
- Recenzent (linia / model / native effort): architekt — przebieg narzędzia i odczyt raportów JSON (sesja główna Opus `xhigh`).
- Dopuszczone alternatywy: Claude / `wykonawca` Sonnet 5.5 / `high`.
- Powód wyboru: wzorzec sondy z poprzedniej funkcji (0 rund), brief tekstowy bez Figmy, Claude w stanie ostrzegawczym.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Muse nieznany (wrapper, brak komunikatu limitu, 2026-10-14).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowano (0-S: S1–S6; SONDA-E: 1057 s, raporty E i E2).
- Rundy korekt: 0-S — 1 (powtórka scenariuszy A/B/C po konfiguracji panelu operatora; dziennik #30–#37); SONDA-E — 0.
- Czas do akceptacji: w dniu 2026-10-14; SONDA-E ~20 min od wysłania.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): nie dotyczy (przebieg architekta). SONDA-E potwierdziła P1 bramki R1 (usunięcie szkicu faktury subskrypcji odrzucane przez operatora).
- Defekty po odbiorze: 0-S — sonda nie sprawdziła usuwania szkicu (luka wykryta przez bramkę R1, zamknięta SONDA-E).
- Wymagane testy i dowody: raporty JSON sond, odczyty stanów faktur i subskrypcji u operatora.

### 2694-BE-1 (fala 1: dyspozytor webhooków i schemat/repozytorium zaległości — 1a, 1b, K1) — 2026-10-14
- Archetyp: Backend API — routing zdarzeń płatności, migracja schematu, repozytorium SQL (niezmiennik płatności i migracji).
- Stawka: wysoka / high-stakes (płatności, migracja danych, naliczanie).
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` Opus 5.5 / `xhigh`.
- Recenzent (linia / model / native effort): Muse / `muse-spark-1.3-contributor` / `max`, `-Access read` (R1a, R1b).
- Dopuszczone alternatywy: wykonawca — brak (przy CZERWONYM: Muse Spark `max`); recenzent — Gemini `gemini-3.8-flash-high` read.
- Powód wyboru: pliki niosące niezmiennik; recenzent z innej rodziny, wzorzec poprzedniej funkcji.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook ŻÓŁTY, 2026-10-14); Muse nieznany (wrapper).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: wymagane korekty (K1 po walidacji architekta).
- Rundy korekt: 1.
- Czas do akceptacji: w dniu 2026-10-14; dokładny czas niezapisany.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R1a/R1b — werdykt „poprawny” 0,9, tylko P3.
- Defekty po odbiorze: brak przypisanych tej fali.
- Wymagane testy i dowody: build 0 ostrzeżeń, 6856/6856, migracja uruchomiona 2× (idempotencja).

### 2694-BE-2 (fala 2: planer i krok zaległości, lustro, „Opłać teraz” — 2a, 2c, K2, K3, 2b-1, 2b-2, 2b-K) — 2026-10-14
- Archetyp: Algorytmika / Logika — maszyna stanów zaległości, transakcje warunkowe, integracja z operatorem płatności.
- Stawka: wysoka / high-stakes (płatności, przywracanie i zawieszanie programów).
- Niepewność: wysoka (zachowanie operatora z sondy, wyścigi pod blokadą konta).
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` Opus 5.5 / `xhigh`.
- Recenzent (linia / model / native effort): Muse / `muse-spark-1.3-contributor` / `max`, `-Access read` (R2, RK3, R2b).
- Dopuszczone alternatywy: wykonawca — brak (CZERWONY → Muse Spark `max`); recenzent — Gemini `gemini-3.8-flash-high` read.
- Powód wyboru: niezmiennik płatności; recenzent z innej rodziny.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook ŻÓŁTY, 2026-10-14); Muse nieznany.
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: 2a/2c — wymagane korekty (K2 po walidacji, K3 po recenzji); 2b — przekazanie przy ~301 tys. kontekstu bez edycji, podział na 2b-1 i 2b-2.
- Rundy korekt: 2a/2c — 2 (K2, K3); 2b — 1 (2b-K) plus podział po przekazaniu.
- Czas do akceptacji: w dniu 2026-10-14; dokładny czas niezapisany.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R2 — P1 potwierdzone (dopasowanie faktury przy zaległości → K3); RK3 — 2×P3 przyjęte; R2b — P1 obniżone do P3 bez zmian (uszkodzony szkic: zachowanie poprzedniej funkcji, głośne), P2 przyjęte (`code=missing` za szeroko), P2 bez zmian (równoległe „Opłać teraz”, sprzed funkcji), P3 przyjęte, 1 uwaga odrzucona.
- Defekty po odbiorze: bramka R1 — odmowa karty bez ponownego odczytu (P2, poprawka GK-O); bramka R2 — utrata płatności starej faktury zaległości przy kolejności przebiegów cyklu (P1, poprawka GK2-M).
- Wymagane testy i dowody: build 0 ostrzeżeń, 6857–6858 testów zielonych, 0 pominiętych po każdej korekcie.

### 2694-BE-3 (fala 3: cykl trwałego zamknięcia — 3a-1, 3a-2, 3a-3) — 2026-10-14
- Archetyp: Backend — cykl tła, operacja nieodwracalna u operatora, transakcja finalizacji.
- Stawka: wysoka / high-stakes (nieodwracalne zamknięcie, płatności).
- Niepewność: wysoka.
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` Opus 5.5 / `xhigh`.
- Recenzent (linia / model / native effort): Muse / `muse-spark-1.3-contributor` / `max`, `-Access read` (R3a, 652 s).
- Dopuszczone alternatywy: wykonawca — brak (CZERWONY → Muse Spark `max`); recenzent — Gemini `gemini-3.8-flash-high` read.
- Powód wyboru: niezmiennik nieodwracalnego zamknięcia; brief podzielony z góry na 3a-1 i 3a-2 (limit kontekstu, S107).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook ŻÓŁTY 25 %/81 %, 2026-10-14 ~20:05); Muse nieznany (~19:50).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: 3a-2 zaakceptowany (340 tys. kontekstu, 75 wywołań, 18 min); po R3a — korekta zbiorcza 3a-3.
- Rundy korekt: 1 (3a-3: P1 recenzji + 3 decyzje architekta).
- Czas do akceptacji: w dniu 2026-10-14; 3a-3 1022 s.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R3a — 1×P1 potwierdzone (wyścig „Opłać teraz” z cyklem zamknięcia bez blokady konta).
- Defekty po odbiorze: bramka R1 — szkice faktur subskrypcji nieusuwalne (P1, GK-C), wznowienie po błędzie finalizacji (P1, GK-O).
- Wymagane testy i dowody: build 0 ostrzeżeń, 7055/7055, 0 pominiętych.

### 2694-BE-M (kanał wiadomości rozliczeniowych i cykl ostrzeżenia — 1c, 1c-K1, 3b, 3b-fix) — 2026-10-14
- Archetyp: Backend — kolejka wiadomości (outbox) i cykl tła bez niezmiennika płatności.
- Stawka: średnia.
- Niepewność: niska–średnia.
- Wykonawca (linia / model / native effort): Muse / `muse-spark-1.3-contributor` / `max`, `-Access write`.
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (R1c, R3b).
- Dopuszczone alternatywy: wykonawca — Claude `wykonawca` Sonnet 5.5 `high`; recenzent — Codex `gpt-6.1-sol` `high` (pula oszczędzana na bramkę).
- Powód wyboru: brief tekstowy bez niezmiennika; Claude ostrzegawczy.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Muse nieznany, Gemini nieznany (wrappery, 2026-10-14).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 1c — korekta 1c-K1; 3b — zaakceptowany (build 0, 6857/6857), potem 3b-fix po recenzji.
- Rundy korekt: 1c — 1; 3b — 1 (3b-fix, 211 s).
- Czas do akceptacji: w dniu 2026-10-14.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R1c — „poprawny” 1,0; R3b — „poprawny” 0,95: P2 odrzucone (zagnieżdżony enum ma precedens), P3 przyjęte (bezpiecznik postępu kursora), P3 bez zmian.
- Defekty po odbiorze: bramka R1 — drugie ostrzeżenie dla tej samej trójki (P2, GK-S); bramka R2 — nieaktualna kandydatura pozwala na drugie ostrzeżenie (P2, GK2-W).
- Wymagane testy i dowody: build 0 ostrzeżeń, testy zielone, 0 pominiętych.

### 2694-D (rewizje dokumentacji produktowej — D1, D1-K1, D2) — 2026-10-14
- Archetyp: Dokumentacja produktowa — rewizje sześciu dokumentów `zatwierdzony`.
- Stawka: średnia.
- Niepewność: średnia (wyniki sondy dopisywane w D2).
- Wykonawca (linia / model / native effort): Muse / `muse-spark-1.3-contributor` / `max`, `-Access write` (repo Dokumentacja).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (RD1); przegląd zgodności 4C — zob. 2694-4C.
- Dopuszczone alternatywy: wykonawca — Claude `wykonawca` Sonnet 5.5 `high`.
- Powód wyboru: wzorzec rewizji poprzedniej funkcji; recenzent z innej rodziny.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Muse nieznany, Gemini nieznany (2026-10-14).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: D1 — wymagane korekty (RD1 „niepoprawny”); D2 — zaakceptowany (448 s).
- Rundy korekt: D1 — 1 (D1-K1); D2 — 0 (architekt dopisał 1 zastrzeżenie, reguła 11).
- Czas do akceptacji: w dniu 2026-10-14.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): RD1 — brak wariantu „operator cofnął do past_due” (potwierdzone, D1-K1).
- Defekty po odbiorze: INT pkt 5 przepisany po poprawce GK2-M (zmiana zachowania, nie defekt rewizji).
- Wymagane testy i dowody: diff dokumentów czytany przez architekta, dziennik rozbieżności (wiersze zamknięte).

### 2694-A-1 (narzędzie scenariuszy akceptacji na zegarach testowych) — 2026-10-14
- Archetyp: Testy akceptacyjne / QA — narzędzie poza repozytorium produktu.
- Stawka: średnia (sandbox).
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): Muse / `muse-spark-1.3-contributor` / `max`, `-Access write`.
- Recenzent (linia / model / native effort): architekt — przebieg scenariuszy (krok 18).
- Dopuszczone alternatywy: Claude `wykonawca` Sonnet 5.5 `high`.
- Powód wyboru: wzorzec narzędzia z poprzedniej funkcji (0 rund).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Muse nieznany (2026-10-14).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowano (798 s; build narzędzia 0/0, brak zapisów w BE).
- Rundy korekt: 0.
- Czas do akceptacji: w dniu 2026-10-14.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): nie dotyczy.
- Defekty po odbiorze: 1 — zapis pomocniczy w otwartej transakcji bez przekazania transakcji (wyjątek przy pierwszym scenariuszu); poprawka architekta w narzędziu (reguła 11).
- Wymagane testy i dowody: scenariusze dunning, retry-success, closure, two-payments, resend — PASS (krok 18).

### 2694-T1 (testy fali 4: T1-1…T1-5, RT1-K) — 2026-10-14
- Archetyp: Testy jednostkowe i bazodanowe (xunit, `[SqlServerFact]`) jako wyrocznia niezmienników.
- Stawka: wysoka jako wyrocznia.
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): Muse / `muse-spark-1.3-contributor` / `max`, `-Access write`, każdy brief w osobnej kopii drzewa.
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (RT1, 457 s) + mutacje architekta.
- Dopuszczone alternatywy: wykonawca — Claude `tester` Haiku 5.5 `xhigh`; recenzent — Codex `gpt-6.1-sol` `high` (pula oszczędzana na bramkę).
- Powód wyboru: wyrocznia testów bez niezmiennika w plikach; Claude ostrzegawczy; kopie drzewa pozwalają na równoległe pętle testów.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Muse nieznany, Gemini nieznany (2026-10-14 ~20:05).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowano 5/5 (777–1015 s; 3–4 mutacje wykonawcy na brief złapane).
- Rundy korekt: 0 z wykonania; RT1-K — 2 przebiegi (pierwszy słuszny STOP: 2 z poprawek opisywały zmyślone testy).
- Czas do akceptacji: w dniu 2026-10-14.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): RT1 „wystarczające” 0,96 — 1 trafne (P3, brak gałęzi alarmu (c)), P1 obalone, P2 obalone, P2 i P3 zmyślone (nieistniejące testy, linie i kod). Błąd triażu architekta: zmyślone P2/P3 przyjęte bez weryfikacji, wykryte przez STOP wykonawcy.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: pełne repo 7013 → 7054/7054, 0 pominiętych; 5 mutacji architekta (MA-1…MA-5) złapanych.

### 2694-T2 (testy fali 5: T2-1…T2-6, RT2-K) — 2026-10-14
- Archetyp: Testy jednostkowe i bazodanowe cyklu zamknięcia i ostrzeżenia, bramki operatora.
- Stawka: wysoka jako wyrocznia.
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): Muse / `muse-spark-1.3-contributor` / `max`, `-Access write`, osobne kopie drzewa.
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (RT2a, RT2b; wymóg dosłownego cytatu z linią) + mutacje architekta.
- Dopuszczone alternatywy: wykonawca — Claude `tester` Haiku 5.5 `xhigh`; recenzent — Codex `gpt-6.1-sol` `high` (po bramce), Claude `wykonawca` Sonnet 5.5 `high`.
- Powód wyboru: wzorzec T1 (5 briefów przyjętych bez rund z wykonania); Claude ostrzegawczy (tydzień 82–83 %).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Muse nieznany, Gemini nieznany (2026-10-14 ~20:45).
- Pewność decyzji: średnia (recenzent: niska–średnia po RT1).
- Wynik pierwszego podejścia: zaakceptowano 6/6 (647–1120 s; 3–4 mutacje wykonawcy na brief złapane).
- Rundy korekt: 0 z wykonania; RT2-K — 0 (518 s, K1–K6).
- Czas do akceptacji: w dniu 2026-10-14.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): RT2 — cytaty kodu prawdziwe; B3 to zmyślony wynik wyszukiwania („0 trafień” przy istniejącym teście); pozostałe → RT2-K K1–K6 przyjęte.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: pełne repo 7256 → 7283/7283, 0 pominiętych; mutacje architekta MB-1…MB-3, MR-1…MR-5 złapane.

### 2694-4C (przegląd zgodności dokumentacji z kodem, pierwsze podejście) — 2026-10-14
- Archetyp: Recenzja dokumentacji wobec kodu (Faza 4c).
- Stawka: średnia.
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): nie dotyczy (przegląd).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read`.
- Dopuszczone alternatywy: Codex `gpt-6.1-sol` `high` (pula dla bramki); Muse — autor D1/D2, wykluczony.
- Powód wyboru: inna rodzina niż autorzy dokumentów (Muse, Claude).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany (wrapper, 2026-10-14 ~22:40).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: odrzucono — rzeczywiste niepowodzenie linii: werdykt 36/36 „zgodne” 1,0 przy zmyślonych treściach punktów, cytatach (0 trafień) i 3 z 68 linków do nieistniejących plików.
- Rundy korekt: nie dotyczy (ponowna kwalifikacja: 4C-R2).
- Czas do akceptacji: nie zaakceptowano.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1 trafna uwaga (skrót W2 w briefie); reszta niewiarygodna.
- Defekty po odbiorze: nie dotyczy.
- Wymagane testy i dowody: weryfikacja architekta grepem cytatów i linków.
- Uwagi: trzecia recenzja Gemini w tej funkcji ze zmyśleniami (RT1, RT2 B3, 4C) — negatywny sygnał lokalny dla recenzji Gemini `high` w briefach z dużym kontekstem; odchylenie architekta: 4C wysłany przed bramką (skill: po bramce).

### 2694-GK (poprawki po bramce R1: GK-S, GK-O, GK-OT, GK-C) — 2026-10-14
- Archetyp: Backend — poprawki niezmiennika zamknięcia i płatności (GK-O, GK-C), SQL cyklu ostrzeżenia (GK-S), testy poprawek (GK-OT).
- Stawka: wysoka / high-stakes.
- Niepewność: średnia (szkice: rozstrzygnięte sondą SONDA-E).
- Wykonawca (linia / model / native effort): GK-O, GK-C — Claude / `wykonawca-opus` Opus 5.5 / `xhigh`; GK-S, GK-OT — Muse / `muse-spark-1.3-contributor` / `max`, `-Access write`.
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `max`, read (bramka R2) + mutacje architekta.
- Dopuszczone alternatywy: GK-O/GK-C — brak (CZERWONY → Muse Spark `max`); GK-S — Claude `wykonawca` Sonnet `high`; GK-OT — Claude `tester` Haiku `xhigh`, świeży `wykonawca-opus`.
- Powód wyboru: GK-O/GK-C pliki niezmiennika; GK-S autor pliku SQL bez niezmiennika płatności; GK-OT — testy nie są plikami niezmiennika, kontynuacja po przekazaniu GK-O przekwalifikowana (reguła 2/12).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook ŻÓŁTY 45–52 %/84–85 %, 2026-10-14 ~23:10–22:37); Muse nieznany.
- Pewność decyzji: wysoka (GK-O/GK-C), średnia (GK-S, GK-OT).
- Wynik pierwszego podejścia: GK-S zaakceptowany (378 s); GK-O — przekazanie przy 300 tys. po produkcji A+B (testy → GK-OT); GK-OT zaakceptowany (756 s); GK-C zaakceptowany (823 s; przesłanka „AutoAdvance null” błędna — w SDK `bool`).
- Rundy korekt: 0 z wykonania (GK-O: przekazanie kontekstu, nie korekta); architekt poprawił komentarze (reguła 11).
- Czas do akceptacji: w dniu 2026-10-14, ~1 h dla całej partii.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): bramka R2 — poprawki R1 usunęły scenariusze; nowe znaleziska R2 — zob. 2694-GK2.
- Defekty po odbiorze: brak przypisanych tym poprawkom.
- Wymagane testy i dowody: build 0 ostrzeżeń, 7320/7320, 0 pominiętych; mutacje wykonawców (M-A, M-B, M-C1, M-C2) i architekta (EndedAt ASC, `HoldDraftAsync` bez strażnika, bez `ClosedAt IS NULL`) złapane.

### 2694-GK2 (poprawki po bramce R2: GK2-W, GK2-M z kontynuacją) — 2026-10-14…15
- Archetyp: Backend — lustro subskrypcji (odczyt faktury zaległości, kolejność zapisu płatności) i SQL znacznika ostrzeżenia.
- Stawka: wysoka / high-stakes (GK2-M: płatność bez zapisu); średnia (GK2-W).
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): GK2-M — Claude / `wykonawca-opus` Opus 5.5 / `xhigh` (przekazanie przy 302 tys. + świeży agent kontynuacji); GK2-W — Muse / `muse-spark-1.3-contributor` / `max`, `-Access write`.
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `max`, read (bramka R3) + mutacje architekta.
- Dopuszczone alternatywy: GK2-M — brak (CZERWONY → Muse Wonder Full `max` od 2026-10-14); GK2-W — Claude `wykonawca` Sonnet `high`.
- Powód wyboru: GK2-M niezmiennik płatności; GK2-W autor tego samego SQL (GK-S), bez niezmiennika płatności; wysłane przed zmianą domyślnego modelu linii Muse.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook 4 %/86 %, 2026-10-14 ~23:40); Muse nieznany.
- Pewność decyzji: wysoka (GK2-M), średnia (GK2-W).
- Wynik pierwszego podejścia: GK2-W zaakceptowany (494 s; uwaga wykonawcy o briefie słuszna); GK2-M — produkcja zaakceptowana, testy po przekazaniu w kontynuacji (zaakceptowane, 3084/3084 w kopii).
- Rundy korekt: 0 z wykonania (przekazanie kontekstu, nie korekta); 1 komentarz poprawiony przez architekta.
- Czas do akceptacji: ~1 h od triażu R2.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R3 — w plikach GK2-M i GK2-W brak znalezisk; oba P2 R3 dotyczą wcześniejszych plików (ścieżka zamknięcia z 3a, test bazy z T2).
- Defekty po odbiorze: brak w R3.
- Wymagane testy i dowody: build `--no-incremental` 0 ostrzeżeń, 7341/7341, 0 pominiętych; mutacje wykonawców (M-1…M-3, M-W1, M-W2) i architekta (M-A1, M-A2) złapane.

### 2694-G (bramka końcowa BE — R1, R2, R3) — 2026-10-14…15
- Archetyp: Recenzja końcowa całego diffu funkcji high-stakes (reguła 6).
- Stawka: wysoka / high-stakes.
- Niepewność: wysoka (diff ~250 plików).
- Wykonawca (linia / model / native effort): nie dotyczy.
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `max`, `-Access read`, jeden przebieg na cały diff BE.
- Dopuszczone alternatywy: przy limicie Codexa — Muse Spark `max` (W4), od 2026-10-14 Muse Wonder Full `max`; brak słabszej bramki.
- Powód wyboru: reguła 6; autor plików niezmiennika z rodziny Claude.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany w R1–R2 (wrapper); przy R3 zablokowany (komunikat limitu wrappera 2026-10-15 00:19, reset 01:42) — bramka czekała na reset z tą samą parą; pierwsze uruchomienie R3 przerwane przeładowaniem sesji Claude Code (nie niepowodzenie linii).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: R1 czerwona 0,96 (1387 s, przerwana klauzulą STOP); R2 czerwona 0,96 (wszystkie niezmienniki); R3 czerwona 0,93 (2492 s; 0×P0/P1, 2×P2, niezmienniki 1–15 zachowane) → GK3, potem druga runda recenzji samej poprawki (Muse Wonder Full `max`, skill Faza 4b pkt 3) zamiast ponownej bramki.
- Rundy korekt: 3 (poprawki GK, GK2, GK3).
- Czas do akceptacji: R1 start 2026-10-14 ~21:50 → odbiór GK3 2026-10-15 03:49 (~6 h, w tym ~1 h 23 min czekania na reset limitu Codexa).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R1 — potwierdzone P1 (szkice), P1 (wznowienie po błędzie finalizacji), P2 (drugie 206), P2 (odmowa karty bez odczytu); obniżone do ryzyka resztkowego P1 (wyścig starej faktury) i P2 (`payment_failed` bez faktury). R2 — potwierdzone P1 (kolejność przebiegów cyklu gubi płatność starej faktury), P2 (nieaktualna kandydatura ostrzeżenia), P3 (komunikat alarmu); odrzucone P2 (zakres przywracania — zgodny z dokumentacją, błąd briefu bramki). R3 — potwierdzone P2 (fałszywy alarm krytyczny cyklu uzgadniającego po udanym zamknięciu zaległości), P2 (`[Theory]` zamiast `[SqlServerTheory]` w teście bazy); uwaga o wyjątku reguły „jedno ostrzeżenie na trójkę” — zgodna z kodem i dokumentem, bez zmian.
- Defekty po odbiorze: brak do chwili odbioru na PRE (2026-10-15 08:39 UTC: BE 1.6.0 `84e07f8` wdrożony, migracja i oba cykle wystartowały bez błędów, pierwszy przebieg nie zamknął programów demo); retest testera (PBI #2694 → Ready for tests) jeszcze nie wykonany.
- Wymagane testy i dowody: pełne `dotnet test` przed każdym przebiegiem (7283, 7320, 7341 zielonych, 0 pominiętych).

### 2694-GK3 (poprawka po bramce R3: znacznik faktury odnowienia przy trwałym zamknięciu) — 2026-10-15
- Archetyp: Backend — ścieżka zamknięcia zaległości, transakcja finalizacji, SQL repozytorium; testy jednostkowe, bazowe i E2E z prawdziwym cyklem uzgadniającym.
- Stawka: wysoka / high-stakes (nieodwracalne zamknięcie, alarm płatności).
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` Opus 5.5 / `xhigh` (produkcja + testy); testy brzegów z drugiej rundy — Claude / `tester` Haiku 5.5 / `xhigh`.
- Recenzent (linia / model / native effort): Muse / `muse-wonder-full-1.0-contributor` / `max`, `-Access read` (druga runda, diff samej poprawki) + mutacje architekta.
- Dopuszczone alternatywy: wykonawca — brak (CZERWONY → Muse Wonder Full `max` write); tester — `wykonawca-opus`; recenzent — Codex Sol `high` (zablokowany limitem), Gemini `high` (negatywny sygnał w zadaniu).
- Powód wyboru: niezmiennik zamknięcia; recenzent z innej rodziny niż Claude przy zablokowanym Codexie; testy brzegów według wzorca — tańsza linia testów.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook 23–30 % / 88–89 %, 2026-10-15 02:35–03:45); Muse nieznany (wrapper); Codex zablokowany (wrapper, 02:47, reset 06:43).
- Pewność decyzji: wysoka (wykonawca), średnia (recenzent — pierwsze lokalne wyniki Wondera Full w recenzji).
- Wynik pierwszego podejścia: GK3 zaakceptowany (1697 s; 6 uwag do briefu, wszystkie słuszne — m.in. trzy odczyty faktury zaległości, M-1 nie kompiluje się, B3 dosłownie nie łapał M-1); GK3-T zaakceptowany (493 s; 2 uwagi słuszne — S3776, S4144).
- Rundy korekt: 0 z wykonania; 1 runda testów brzegów po drugiej rundzie recenzji (P3, luki testów, nie błąd wykonania).
- Czas do akceptacji: ~1 h 25 min od triażu R3 (02:25 → 03:49).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): GK3-R (Wonder Full `max`, 1403 s) — poprawny 0,86; 0×P0/P1; potwierdzone P3 ×3 (fałszywy alarm po wycofanej 3.6 — przyjęte jako ryzyko resztkowe z poprawką opisu; dwie luki testów brzegów — uzupełnione); fałszywych P0/P1 do obalenia: 0.
- Defekty po odbiorze: brak do chwili odbioru na PRE (2026-10-15 08:39 UTC: BE 1.6.0 `84e07f8` wdrożony, migracja i oba cykle wystartowały bez błędów, pierwszy przebieg nie zamknął programów demo); retest testera (PBI #2694 → Ready for tests) jeszcze nie wykonany.
- Wymagane testy i dowody: build `--no-incremental` 0 ostrzeżeń, 7356 → 7360/7360, 0 pominiętych; mutacje wykonawców (M-1…M-3, MT-1…MT-3) i architekta (M-A1…M-A4) złapane.
### 2694-QAS (QA Sphere: przegląd 84 istniejących i plik podglądu nowych przypadków — QAS-1, QAS-1-K, R-QAS-1) — 2026-10-15
- Archetyp: QA Sphere — przypadki manualne wg `qasphere-test-generator` (plik podglądu JSON, przegląd istniejących z Kroku 2b).
- Stawka: średnia (przypadki manualne funkcji high-stakes; publikacja dopiero po „ok” właściciela).
- Niepewność: wysoka (zaległości nie da się wywołać na subskrypcji z `/kup`; potrzebna procedura zegara testowego z przepięciem konta SQL-em).
- Wykonawca (linia / model / native effort): Muse / `muse-wonder-full-1.0-contributor` / `max`, `-Access write` (QAS-1, QAS-1-K).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (R-QAS-1).
- Dopuszczone alternatywy: wykonawca — Gemini write (procedura skilla, gdy Muse zajęty); recenzent — Muse read tylko dla pliku Gemini (wykluczony, autor z rodziny Muse).
- Powód wyboru: procedura skilla (Muse autor → Gemini recenzja); domyślny model linii Muse od 2026-10-14.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Muse nieznany (wrapper, brak komunikatu limitu, 2026-10-15 01:58); Gemini nieznany (wrapper, 02:45).
- Pewność decyzji: średnia (pierwszy plik QA Sphere na Wonder Full).
- Wynik pierwszego podejścia: zaakceptowany po korekcie briefu (QAS-1: 2013 s, 15 przypadków + 84 werdykty przeglądu; obie uwagi do briefu słuszne — W1 nie do wywołania ręcznie przez unieważnienie faktury, pkt 13 „zapłata faktury nieściągalnej” niewykonalny dosłownie).
- Rundy korekt: 0 z wykonania; 1 z winy specyfikacji (QAS-1-K, 151 s: W1 → `coverage.skipped`, reszta bajtowo bez zmian).
- Czas do akceptacji: ~3 h 05 min (01:58 → 05:03 UTC+2: przebieg autora, poprawka dokumentacji INT pkt 4, korekta, recenzja 15 min, triaż).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R-QAS-1 (877 s) — 0×P0/P1; P2 B3 odrzucone (zmyślony krok i zmyślona metoda BE `HandleSubscriptionDeleted`, grep 0 trafień); P2 C1 odrzucone (zapytanie już zawężone); P3 A1 bez zmiany. Wkład autora: wykrył błąd dokumentacji (unieważnienie faktury = umorzenie), z którego wynikło ryzyko resztkowe 15 i decyzja D2.
- Defekty po odbiorze: brak w `qas.py verify` (18 sprawdzonych; 2 różnice to fałszywy alarm eksportu Markdown — lista ≥ 10 punktów numerowana „01.”, HTML zgodny z plikiem); wysłane seq 1630–1643, zaktualizowane 986, 987, 1553, 1578, wycofane 0; wykonanie przez testera jeszcze nie nastąpiło.
- Wymagane testy i dowody: `qas.py lint` 0/0 po każdym przebiegu, `qas.py table`; publikacja i `verify` po „ok” właściciela.
### 2694-4C-R2 (przegląd zgodności dokumentacji z kodem po bramce i poprawkach) — 2026-10-15
- Archetyp: Recenzja dokumentacji wobec kodu (Faza 4c, mapa dokumentów, oba kierunki, macierz werdyktów).
- Stawka: średnia (dokumentacja funkcji high-stakes; rozbieżność kod → dokument ujawnia defekt kodu).
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): nie dotyczy (przegląd).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Access read`.
- Dopuszczone alternatywy: Muse — autor rewizji D1/D2, wykluczony; Claude — autor kodu niezmienników i zdań architekta, wykluczony; Gemini — rzeczywiste niepowodzenie linii w tym archetypie (2694-4C).
- Powód wyboru: inna rodzina niż autorzy dokumentów i kodu; odczyt repo powłoką.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex zablokowany (wrapper, 2026-10-15 02:47, reset 06:43) → czekanie; po resecie nieznany (wrapper, 06:44).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: 1. przebieg STOP słuszny (zła ścieżka `DbDiagram.dbml` w briefie — błąd architekta); 2. przebieg przerwany limitem po 406 tys. tokenów; 3. przebieg po resecie (06:44–06:53) zaakceptowany: niezgodne 0,96, R1–R6.
- Rundy korekt: 0 z wykonania; 1 z winy specyfikacji (ścieżka pliku).
- Czas do akceptacji: ~4 h 15 min od startu (02:39 → 06:55), z czego ~4 h czekania na reset limitu.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R1 potwierdzone — defekt kodu (konto `UNPAID` bez programu `FAILED_PAYMENT` nigdy nie anulowane) → poprawka R1F; R2, R5 — dokument nieprecyzyjny, poprawiony; R3 — kod sprzed PBI (#1759) → decyzja D5; R4 — FE przy S2 → decyzja D4; R6 odrzucone (nieosiągalne — ryzyko 16). Fałszywych P0/P1: 0. Jedyny defekt kodu wykryty po bramce R3 pochodzi z tego przeglądu.
- Defekty po odbiorze: nie dotyczy.
- Wymagane testy i dowody: triaż architekta odczytem kodu i dokumentów; dziennik rozbieżności #58–#63.
- Uwagi: przegląd zgodności z kierunkiem kod → dokument znalazł defekt kodu, którego nie znalazły trzy przebiegi bramki (scenariusz „konto bez programów” leżał poza niezmiennikami briefu bramki) — argument za utrzymaniem 4C po bramce, nie przed.
### 2694-R1F (poprawka R1 z 4C-R2: anulowanie konta `UNPAID` bez programu do zamknięcia) — 2026-10-15
- Archetyp: Backend — gałąź kandydata cyklu trwałego zamknięcia (SQL), warunek ścieżki, procesor konta; testy jednostkowe, bazowe i E2E.
- Stawka: wysoka / high-stakes (nieodwracalne anulowanie u operatora płatności).
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` Opus 5.5 / `xhigh` (produkcja + testy A, przekazanie przy 303 tys.); kontynuacja testów B, C, D i mutacji — Claude / `tester` Haiku 5.5 / `xhigh`.
- Recenzent (linia / model / native effort): Muse / `muse-wonder-full-1.0-contributor` / `max`, `-Access read` (diff przyrostu względem kopii bazowej) + mutacje wykonawców.
- Dopuszczone alternatywy: wykonawca — brak (CZERWONY → Muse Wonder Full `max` write); kontynuacja — `wykonawca-opus`, Muse Wonder Full `max` write; recenzent — Codex `gpt-6.1-sol` `high` read.
- Powód wyboru: niezmiennik anulowania; kontynuacja testów według wzorca na tańszej linii (tydzień Claude'a 90 %); recenzent z innej rodziny niż Claude, wzorzec GK3-R.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook 6–12 % / 90–91 %, 2026-10-15 06:59–07:40); Muse nieznany (wrapper).
- Pewność decyzji: wysoka (wykonawca), średnia (recenzent).
- Wynik pierwszego podejścia: wykonawca-opus — produkcja i testy A odebrane bez korekty, przekazanie strażnikiem kontekstu (303 tys.); 4 uwagi do briefu, słuszne (luka konta bez programów w drugim scenariuszu → ryzyko 18; M-2 nie zaczerwieni B3; brak sekcji testów w AGENTS.md; DAO kandydata tylko komentarz). Tester — zaakceptowany (934 s, 329 tys. tokenów); uwagi słuszne (D3 w brzmieniu briefu nie łapał M-1/M-3 — dodana asercja `ACTIVE`).
- Rundy korekt: 0 z wykonania; kontynuacja po przekazaniu (strażnik kontekstu, nie korekta).
- Czas do akceptacji: ~1 h 05 min (07:00 → ~08:05: wykonawca-opus, kontynuacja testera, pełne testy, recenzja 824 s, triaż).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R1F-R (Wonder Full `max` read, 824 s) — niepoprawny 0,8; 1×P1 potwierdzone, ale znane przed recenzją (uwaga wykonawcy → ryzyko 18): brak dokończenia po wycofanej 3.6 i końcu zapisanym przez webhook dla konta z gałęzi okna; przyjęte jako ryzyko resztkowe (podwójny błąd, skutek: brak maila 207 albo późniejsze zamknięcie programu innej przyczyny), z poprawką treści wpisu błędu przez architekta (reguła 11) i zdaniem w INT pkt 7. Fałszywych P0/P1: 0. Hipotezy bez znaleziska: granica i precyzja `datetime2`, stronicowanie sumy, brak błędnego anulowania, ścieżka przy zerze programów.
- Defekty po odbiorze: brak do chwili odbioru na PRE (2026-10-15 08:39 UTC: BE 1.6.0 `84e07f8` wdrożony, migracja i oba cykle wystartowały bez błędów, pierwszy przebieg nie zamknął programów demo); retest testera (PBI #2694 → Ready for tests) jeszcze nie wykonany.
- Wymagane testy i dowody: build 0 ostrzeżeń; SubscriptionManagement 3108 → 3132/3132, 0 pominiętych; pełny przebieg 7360 → 7384/7384, 0 pominiętych; mutacje M-1 (SQL) → 7 czerwonych, M-2 (warunek) → 3, M-3 (procesor) → 4; hashe produkcji przed = po; mutacje architekta M-A5 (granica w C#) → 2 czerwone, M-A6 (granica w SQL) → 1.
- Uwagi: kontynuacja przez świeżego agenta innej linii Claude'a (Haiku zamiast Opusa) po przekazaniu — pierwszy taki przypadek w zadaniu; jakość kontynuacji do oceny wg reguły 15 (rundy korekt briefów z kontynuacją).

### 2694-ADO (pozycje ADO z decyzji bramy: Bugi D2 i D5, PBI D1 i D4, cztery PBI z W3 — ADO-1, ADO-1G) — 2026-10-15
- Archetyp: ADO — zakładanie Bugów i PBI z taskami według skilla `azure-devops-zebrani` (tryby Bug i PBI B), treść z dokumentacji `zatwierdzony` i z odczytu kodu.
- Stawka: średnia (treść zadań dla wykonawców i testera; Bug D2 dotyczy pliku niezmiennika płatności, ale brief niczego w kodzie nie zmieniał).
- Niepewność: średnia (wybór Feature'ów dla W3 i luki dokumentacji).
- Wykonawca (linia / model / native effort): ADO-1 — Muse / `muse-wonder-full-1.0-contributor` / `max`, `-Access write` (MCP ADO); po limicie ADO-1G — Gemini / `gemini-3.8-flash-high`, `-Access write` (MCP ADO).
- Recenzent (linia / model / native effort): architekt — odczyt wszystkich 40 pozycji (pola, relacje, treść) i sprawdzenie nazw względem kodu ZebraniBE, `DbDiagram.dbml` i dokumentacji.
- Dopuszczone alternatywy: wykonawca — Codex `gpt-6.1-sol` `high` (pula `nieznany`, bramka funkcji już zamknięta), `wykonawca` Sonnet `high` (tydzień Claude'a 90 %+); recenzent — Codex `gpt-6.1-sol` `high` read.
- Powód wyboru: domyślna linia Muse (reguła 8) z MCP ADO; po 429 ponowna kwalifikacja (reguła 2) — Gemini ma MCP ADO i osobną pulę, brief przepisany na ścieżki Windows.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Muse zablokowany (429 z wrappera, 2026-10-15 ~08:47 UTC, limit tygodniowy do 2026-10-19 00:00 UTC); Gemini nieznany (wrapper); Claude ostrzegawczy (hook, tydzień 90 %+).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: ADO-1 (Muse) — przerwany po 130 s komunikatem 429, zero zapisów w ADO (sprawdzone WIQL). ADO-1G (Gemini, 908 s, exit 0) — struktura poprawna: 8 pozycji, 32 taski, przypisania, iteracje (E2e w „E2e Sprint”), linki `related` do #2694. Treść z błędami faktów:
  - wymyślone nazwy kolumn i tabel w SQL dla testera i notatkach (`Status`, `ArrearsAmount`, `ArrearsCurrency`, `ArrearsSince`, `OwnerId`, tabela `Owners`, `Programs.Id`, `MessageOutbox.ProcessedAt`, `Stamps`, `Rewards`, `WalletRegistrations`, `CreateProgramCommand`, `Subscriptions.Status`);
  - fałszywa przesłanka w Bugu D2: programy zawieszone w stanie `PAST_DUE`;
  - link do makiety (node 255-3211), którego nie ma w dokumentacji;
  - zły tytuł sekcji źródła w PBI blokady;
  - wymyślone kryteria (archiwum programu u właściciela, „pasmo znika” wbrew UI-WLASCICIEL-DASHBOARD).
- Duplikaty (wina specyfikacji, nie wykonania): pasmo uwagi (#2753) dubluje #1632, oznaczenie w Wallet (#2767) dubluje #1548. Brief kazał wybrać Feature z dowodem, ale nie kazał sprawdzić, czy zakres nie ma już PBI. Listę W3 architekt ułożył w planie bez przeszukania backlogu.
- Rundy korekt: 0 przez wykonawcę. Architekt sam poprawił treść 6 pozycji (#2741, #2744, #2747, #2751, #2760, #2774) i zamknął 2 duplikaty (Removed + 12 tasków, link „Duplicate Of”, komentarze w #1632 i #1548). Poprawki w miejscu kosztowały mniej niż druga runda z nowym briefem.
- Czas do akceptacji: ~1 h 10 min (08:45 → ~09:55: przebieg Muse, przebieg Gemini, walidacja, poprawki).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): sekcja „Co uważasz za błędne” Gemini — 4 uwagi:
  - (1) PBI D1 bez testera — odrzucona: wzorzec PBI zależności;
  - (2) brak rozstrzygnięcia losu danych po retencji — słuszna, trafiła do „Do ustalenia” #2760;
  - (3) brak specyfikacji UI blokady — słuszna, w „Do ustalenia” #2774;
  - (4) przypisania tasków po `add_child` — informacja.
- Defekty po odbiorze: brak do chwili domknięcia.
- Wymagane testy i dowody: odczyt `get_batch` 40 pozycji (typ, stan, rodzic, przypisanie, iteracja) i relacji #2694; porównanie każdej nazwy kodu z ZebraniBE (`grep`, `DbDiagram.dbml`, enumy `SubscriptionStatus`, `MessageType`, `ProgramModel`); wyniki `update_batch` 6/6 i 14/14 z kodem 200.
- Uwagi:
  - Gemini Flash `high` w briefie ADO wymyśla nazwy kodu, gdy brief ich nie podaje dosłownie. Brief ADO dla Gemini musi podawać nazwy kodu wprost albo kazać je cytować z `path:line`.
  - Przed zakładaniem PBI uzupełniających architekt przeszukuje backlog (WIQL po słowach kluczowych i odczyt opisów kandydatów).

### 2715-PRE (zakup testowy na PRE jako dowód end-to-end wystawiania faktur — PRE-zakup-2715) — 2026-10-19
- Archetyp: Worker przeglądarkowy — jedna płatność testowa na PRE przez Playwright CLI (nowe konto syntetyczne na `/kup`, Stripe sandbox), bez akcji poza scenariuszem.
- Stawka: średnia (akcja nieodwracalna na PRE: jedna płatność i jedna faktura w Fakturowni; zakaz ponawiania kliknięcia płatności w briefie).
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Muse / `muse-wonder-full-1.0-contributor` / `max`, `-Access write` (Playwright CLI `pwcli`, sesja `-s=zakup2715`).
- Recenzent (linia / model / native effort): nie dotyczy (akcja w przeglądarce, bez kodu) — odbiór architekta po stronie serwera: wiersze `Invoices` (odczyt `sqlcmd`), faktura w Fakturowni (GET wybranych pól), Historia faktur przez API, porównanie tokenu z logiem BE bez wypisywania.
- Dopuszczone alternatywy: Gemini albo Codex z Playwright MCP (CLI działa tylko w linii Muse, MCP ~3,3× więcej tokenów wejścia).
- Powód wyboru: Playwright CLI tylko w linii Muse (reguła 15); limit tygodniowy Muse z 2026-10-15 zresetowany 2026-10-19 00:00 UTC.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Muse nieznany (wrapper, brak komunikatu limitu, 2026-10-19 09:33 UTC).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: PASS, 247 s (09:33:47–09:37:54 UTC), jedna płatność (kliknięcie 09:35:49, płatność zapisana 09:36:40); 16 wywołań powłoki, 64 polecenia CLI, 0 własnych snapshotów. Odchylenia drobne, obsłużone przez wykonawcę: domyślnie zaznaczona „Firma”, niejednoznaczny lokator pola hasła, kod SMS zatwierdzany automatycznie.
- Rundy korekt: 0.
- Czas do akceptacji: start 09:33 UTC; faktura wystawiona 09:38:27 (1 min 47 s po płatności), odbiór po odczytach serwera.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): nie dotyczy. Sekcja „Co uważasz za błędne” — 4 uwagi słuszne: po płatności aplikacja nie pokazuje komunikatu sukcesu, więc kryterium PASS powinno być adresem powrotu; brief nie podał oczekiwanej kwoty ani okresu do sprawdzenia przed nieodwracalnym kliknięciem; stały numer telefonu zderzy się przy powtórce; adres `@example.com` nie potwierdzi konta, a Fakturownia oznacza wysyłkę na niego jako nieudaną.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: faktura `ISSUED` z numerem `DEMO/51/10/2026`; w Fakturowni pozycja „Abonament Zebrani.pl”, VAT 23 %, 369,00 zł, status opłacona, KSeF demo; Historia faktur przez API — `ISSUED`; token Fakturowni 0 razy w logu BE i w odpowiedziach.
- Uwagi: brief przeglądarkowy z płatnością podaje oczekiwaną kwotę i okres do sprawdzenia przed kliknięciem oraz kryterium PASS jako adres powrotu, nie komunikat.

### 2715-QAS (QA Sphere: przegląd 39 istniejących i 10 nowych przypadków — QAS-GEN-2715, QAS-REV-2715) — 2026-10-19
- Archetyp: QA Sphere — przypadki manualne wg `qasphere-test-generator` (plik podglądu JSON, przegląd istniejących z Kroku 2b).
- Stawka: średnia (przypadki manualne funkcji high-stakes — wystawianie faktur; publikacja dopiero po „ok” właściciela).
- Niepewność: średnia (postaci e-maila Fakturowni nie ma w repozytoriach; tester bez dostępu do panelu Fakturowni i serwera).
- Wykonawca (linia / model / native effort): Muse / `muse-wonder-full-1.0-contributor` / `max`, `-Access write` (QAS-GEN-2715).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (QAS-REV-2715).
- Dopuszczone alternatywy: wykonawca — Gemini write (procedura skilla, gdy Muse zajęty); recenzent — Muse read tylko dla pliku Gemini (wykluczony, autor z rodziny Muse).
- Powód wyboru: procedura skilla (Muse autor → Gemini recenzja).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Muse nieznany (wrapper, 2026-10-19 09:36 UTC); Gemini nieznany (wrapper, 10:00 UTC).
- Pewność decyzji: średnia (drugi plik QA Sphere na Wonder Full).
- Wynik pierwszego podejścia: zaakceptowany bez korekty — 1421 s (09:36:48–10:00:29 UTC), `lint` 0 błędów, 10 nowych (6 high, 4 medium), 39 werdyktów (35 zostaje, 4 aktualizacje, 0 `[Removed]`), 12 pominiętych kategorii z powodami. Uwagi autora do briefu słuszne albo informacyjne: 39 w `existing[]` plus osobno wycofany 996; niejednoznaczne odwołanie do „pkt 12” zmiany abonamentu; kryterium „ponawiana do 5 razy” wobec „najwyżej 5 prób” w INT pkt 1; postać e-maila Fakturowni niepotwierdzona; wątpliwość, czy ZEB-999/1000 mają dostać wymaganie #2715 (zostawione, zaakceptowane na bramie).
- Rundy korekt: 0.
- Czas do akceptacji: ~1 h 20 min (09:36 → ~10:53 UTC: przebieg autora 24 min, recenzja 18 min, triaż i próba architekta, brama właściciela, wysyłka i `verify`).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): QAS-REV (1088 s) — poprawny 0,98; 0×P0/P1; 3×P3: F1 obalone (tolerancja wystawionej już faktury jest w kroku 5 — fałszywe znalezisko), F2 odrzucone (brief zabrania opisywać brak SMTP Zebrani na PRE jako zachowanie oczekiwane, krok jest na to odporny), F8 bez skutku (wyszukiwanie w DevTools nie rozróżnia wielkości liter). Fałszywych P0/P1: 0. Próba architekta (F1, F5, F6, F8): napisy dosłownie z `pl.json`, ujemna kwota korekty w BE i w UI-KONTO-USTAWIENIA, trasy API, format telefonu.
- Defekty po odbiorze: brak w `qas.py verify` (14 sprawdzonych, 0 różnic); wysłane seq 1644–1653 (folder 174), zaktualizowane 998, 992, 999, 1000, wycofane 0; wykonanie przez testera jeszcze nie nastąpiło.
- Wymagane testy i dowody: `qas.py lint` 0 błędów, `qas.py table`; po „ok”: `folders` → `push --limit 1` → `verify --only F1` → `push` → `update` → pełne `verify`.

### 2722-FE-1 (nowa wartość enuma statusu dokumentu, mapa etykiet, pl+en, spec) — 2026-10-19
- Archetyp: Frontend — enum + mapa etykiet + i18n + spec Vitest (5 plików), bez SCSS i bez Figmy.
- Stawka: niska–średnia (ekran funkcji high-stakes bez niezmiennika; kontrakt z BE ustalony w planie).
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high` / `-Access write`.
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `high`, `-Mode review`.
- Dopuszczone alternatywy: wykonawca — Muse `muse-wonder-full-1.0-contributor` `max`, `wykonawca` Sonnet 5.5 `high`; recenzent — Muse Wonder Full `max` read.
- Powód wyboru: krótki brief tekstowy bez niezmiennika i bez makiety; recenzja przy niskiej stawce — Sol `high` preferowany (reguła 13), brief ≤ 5 plików przy sygnale Codexa `nieznany` (reguła 7).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany, Codex nieznany (wrappery, brak komunikatów limitu, 2026-10-19 12:41 UTC).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowany po jednolinijkowej poprawce architekta (reguła 11) — wykonawca uciął zdanie istniejącego komentarza JSDoc enuma; 5 plików, 12 testów spec zielone, 312 s (12:41:43–12:46:54 UTC).
- Rundy korekt: 0 (poprawka architekta jednej linii, bez zwrotu do wykonawcy).
- Czas do akceptacji: ~10 min (z recenzją 72 s, 12:49:24–12:50:37 UTC).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 znalezisk; werdykt poprawny. Fałszywych P0/P1: 0.
- Defekty po odbiorze: brak do bramki końcowej (krok 13).
- Wymagane testy i dowody: `ng test --include` spec Historii faktur (12/12), `npm run lint`, `npm test`, `npm run build` architekta; klucz w obu locale.
- Uwagi: Gemini przy edycji istniejącego komentarza potrafi uciąć zdanie — brief, który dotyka pliku z JSDoc, prosi o dopisanie akapitu bez zmiany istniejących linii, a odbiór porównuje diff komentarza.

### 2722-DOC-1 (datowane rewizje dwóch dokumentów `zatwierdzony` z decyzji planu) — 2026-10-19
- Archetyp: Dokumentacja produktowa — rewizja integracji (9 punktów) i rewizja interfejsu (4 punkty) z zatwierdzonych z góry decyzji D1–D4 i wyników rozpoznania.
- Stawka: średnia (źródło prawdy dla kodu i QA Sphere funkcji high-stakes).
- Niepewność: niska (decyzje i fakty rozpoznania podane w briefie).
- Wykonawca (linia / model / native effort): Muse / `muse-wonder-full-1.0-contributor` / `max`, `-Access write` (repo Dokumentacja).
- Recenzent (linia / model / native effort): w kroku przeglądu zgodności (Faza 4c) — Gemini / `gemini-3.8-flash-high` / `-Access read`.
- Dopuszczone alternatywy: Gemini `high` write, `wykonawca` Sonnet 5.5 `high`.
- Powód wyboru: tor poboczny z gotowymi decyzjami, linia bez wpływu na pulę Claude'a; domyślna para Muse (reguła 8).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Muse nieznany (wrapper, 2026-10-19 12:41 UTC).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowany bez korekty — 494 s (12:41:45–12:49:59 UTC); kotwica linku w pkt 11 poprzedniej rewizji poprawiona przez wykonawcę; front matter nietknięty.
- Rundy korekt: 0.
- Czas do akceptacji: ~12 min do odbioru architekta; recenzja zgodności w kroku 15.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): uzupełnię po kroku 15.
- Defekty po odbiorze: uzupełnię po kroku 15.
- Wymagane testy i dowody: odczyt diffu przez architekta wobec dziennika rozbieżności (5 wpisów zamkniętych).

### 2722-FIG-1 (stan „Anulowana” w czterech kompozycjach Historii faktur) — 2026-10-19
- Archetyp: Frontend UI / Figma — podmiana wariantu Tagu, tekstu i ikony w instancjach (desktop Light/Dark, arkusz mobilny Light/Dark).
- Stawka: niska (makieta, bez kodu).
- Niepewność: średnia (miejsce kompozycji mobilnych nieznane w briefie).
- Wykonawca (linia / model / native effort): Claude / `wykonawca` — Sonnet 5.5 / `high` (Figma MCP).
- Recenzent (linia / model / native effort): architekt — `get_screenshot` i odczyt struktury (bez recenzji innej rodziny — makieta bez kodu).
- Dopuszczone alternatywy: Codex z potwierdzonym Figma MCP (niepotwierdzony w tej sesji).
- Powód wyboru: Figma wymaga MCP; próba A/B linii Figmy zamknięta 2026-10-12 → Sonnet.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany — hook ZIELONY (2026-10-19 ~12:40 UTC).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: wymagane korekty — cztery znaczniki ustawione poprawnie (wariant Danger, ikona `ban`, instancje nieodpięte), ale na mobile dłuższy tekst „Anulowana” uwidocznił istniejące przycinanie kontenera „Kwota i stan” (stan sprzed briefu, brief go nie przewidział).
- Rundy korekt: 2 (obie z winy specyfikacji, nie wykonania): odblokowanie przycinania, potem przesunięcie kontenera statusu i zwężenie opisu (kontener 103×46, opis 117 px, wszystkie tagi HUG).
- Czas do akceptacji: w obrębie fali 1 (~15 min od startu do odbioru zrzutów).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): zrzuty architekta — 1 potwierdzone (przycięty tag na mobile, P2, przyczyna istniejąca), usunięte w korektach.
- Defekty po odbiorze: brak; kompozycja `3966:147335` poza zakresem nie zmieniona.
- Wymagane testy i dowody: `get_screenshot` czterech kompozycji, odczyt `componentProperties`, `characters`, `mainComponent.name` ikony i pudełek sąsiadów.

### 2722-BE-1 (schemat, opcje, odczyt dokumentu, endpoint powiadomień — pierwszy przebieg) — 2026-10-19
- Archetyp: Backend — migracja + słownik + opcje + klient HTTP + endpoint z sekretem + zapis żądań, z testami SQL.
- Stawka: wysoka / high-stakes (uwierzytelnienie powiadomienia, migracja danych, współbieżność kolejki).
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh`.
- Recenzent (linia / model / native effort): Muse / `muse-wonder-full-1.0-contributor` / `max`, `-Access read` (po BE-1a i BE-1b).
- Dopuszczone alternatywy: wykonawca — brak (przy CZERWONYM: Muse Wonder Full `max`); recenzent — Codex `gpt-6.1-sol` `xhigh` (pula Codexa oszczędzana na bramkę).
- Powód wyboru: pliki niezmiennika high-stakes (reguły 2 i 7).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany — hook ZIELONY (2026-10-19 ~12:40 UTC).
- Pewność decyzji: wysoka (bramka twarda).
- Wynik pierwszego podejścia: odrzucony jako wykonanie — strażnik kontekstu przy ~310 tys. oddał raport przekazania bez żadnej zmiany w kodzie: całe przejście zużyte na rozpoznanie repozytorium i 8 słusznych uwag do specyfikacji (zakres klienta HTTP, dzierżawa wobec partii, zachowanie przy wyłączonej integracji, unikalny indeks wobec stałych w istniejących testach, białe znaki w sekrecie).
- Rundy korekt: brief podzielony przez architekta na BE-1a (schemat, opcje, deploy, odczyt dokumentu) i BE-1b (endpoint, zapis żądań) z plikiem decyzji; wynik obu w osobnych wpisach.
- Czas do akceptacji: nie dotyczy (przekazanie).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): nie dotyczy.
- Defekty po odbiorze: nie dotyczy.
- Wymagane testy i dowody: nie dotyczy.
- Uwagi: brief obejmujący osiem sekcji (schemat, seed, dbml, opcje, deploy, klient, endpoint, kolejka) dla Opusa `xhigh` przekracza budżet kontekstu jednego przebiegu jeszcze przed pierwszym zapisem — sygnał kosztu dla reguły 15: brief high-stakes z migracją i nowym endpointem dzielić z góry na warstwy (schemat + klient / endpoint + zapis), a fakty repozytorium (numery skryptów, wzorce testów, linie plików) zbierać tańszym rozpoznaniem przed briefem.

### 2722-BE-1a (schemat, słowniki, opcje z bramkami, deploy, odczyt dokumentu przez API — kontynuacja po przekazaniu) — 2026-10-19
- Archetyp: Backend — migracja DbUp + słownik + opcje + klient HTTP (GET z nagłówkiem `Bearer`) + testy SQL; kontynuacja z plikiem decyzji i raportem przekazania poprzednika.
- Stawka: wysoka / high-stakes (migracja z unikalnym indeksem na istniejących danych, poświadczenie API w nowym kanale).
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh` (świeży agent tej samej linii, reguła 15).
- Recenzent (linia / model / native effort): Muse / `muse-wonder-full-1.0-contributor` / `max`, `-Access read` (wspólnie z BE-1b, uzupełnię).
- Dopuszczone alternatywy: wykonawca — brak (CZERWONY: Muse Wonder Full `max`); recenzent — Codex `gpt-6.1-sol` `xhigh`.
- Powód wyboru: pliki niezmiennika high-stakes; kontynuacja w tej samej linii po przekazaniu.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany — hook ZIELONY (2026-10-19 ~12:53 UTC, okno 5 h ~30 %).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: zaakceptowany — 1286 s, 87 wywołań, kontekst ~356 tys. (powyżej miękkiego progu, ale przebieg domknięty); 9 nowych plików, 12 zmienionych. Jedno naruszenie zakazu: `git add -N .` cofnięte przez wykonawcę samodzielnie i zgłoszone (indeks pusty — sprawdzone). Sześć uwag do specyfikacji, w tym trzy słuszne i przyjęte: domyślna dzierżawa 5 min nie przechodzi bramki przy limicie żądania 101–120 s (→ 6 min w BE-1b), brak porównania `id` odpowiedzi z żądanym (→ BE-1b), dokument Zebrani bez zapisanego `id` po awarii procesu (→ reguła BE-2). Przesłanka „stałe w istniejących testach kolidują z nowym indeksem” obalona przez wykonawcę.
- Rundy korekt: 0 (drobne zmiany po odbiorze włączone do BE-1b jako decyzje architekta, nie poprawki wykonania).
- Czas do akceptacji: ~30 min (start 12:53 UTC, raport ~13:15, walidacja architekta ~13:25).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): recenzja fali (Muse Wonder Full `max`, 958 s) — w plikach BE-1a: P1 potwierdzone (`GetString()` na samotnym surogacie w odpowiedzi 2xx rzuca mimo kontraktu klienta), P2 przyjęte (sekret webhooka równy tokenowi API — bramka startu), P3 częściowo (alfabet sekretu: najpierw komentarz, po raporcie poprawki bramka startu); fałszywych P0/P1: 0.
- Defekty po odbiorze: P1 z recenzji (osłona odczytu tekstu) — naprawione w BE-1-fix.
- Wymagane testy i dowody: `dotnet build` 0 ostrzeżeń; pełny `dotnet test` z bazą SQL architekta: 7455/7455 wykonanych i zielonych, 0 pominiętych; diff przeczytany (migracja z bramką duplikatów 51020, idempotencja, token tylko w nagłówku `Bearer`, anulowanie po `kind` albo fladze).

### 2722-BE-1b (endpoint powiadomień ze wspólnym sekretem i współbieżny zapis żądań) — 2026-10-19
- Archetyp: Backend API — kontroler anonimowy z surowym ciałem, komenda CQRS z parserem i porównaniem sekretu w stałym czasie, repozytorium z scalaniem i obsługą wyścigu 2601/2627, testy jednostkowe, integracyjne i SQL.
- Stawka: wysoka / high-stakes (uwierzytelnienie powiadomienia, współbieżność, dane osobowe w ciele).
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh`.
- Recenzent (linia / model / native effort): Muse / `muse-wonder-full-1.0-contributor` / `max`, `-Access read` (wspólnie z BE-1a, uzupełnię).
- Dopuszczone alternatywy: wykonawca — brak (CZERWONY: Muse Wonder Full `max`); recenzent — Codex `gpt-6.1-sol` `xhigh`.
- Powód wyboru: pliki niezmiennika high-stakes.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany — hook ZIELONY przy starcie (2026-10-19 ~13:28 UTC, okno 5 h 40 %), ŻÓŁTY przy odbiorze (52 %).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: zaakceptowany — 1169 s, 116 wywołań, kontekst ~333 tys.; dwa świadome odstępstwa przyjęte: `LastReceivedAt` tylko do przodu (wykonawca wykrył w specyfikacji architekta ciche gubienie powiadomienia przy odwróconej kolejności dwóch zapisów — słuszne, P1 specyfikacji), sprawdzenie `id` odpowiedzi w interpreterze zamiast w kliencie (limit zależności klasy S1200). Zgłoszona luka: wyłączona integracja + błędne wartości sekcji → 500 zamiast 401 (bez zapisu) — do rundy poprawek. Sprawdzenie, że test potrafi być czerwony (podmiana SQL), wykonane i cofnięte.
- Rundy korekt: 0 z wykonania (uzupełnię, jeśli recenzja coś potwierdzi).
- Czas do akceptacji: ~25 min do odbioru architekta (start ~13:28 UTC, raport ~13:48, walidacja ~14:00); recenzja fali w toku.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): recenzja fali (Muse Wonder Full `max`) — w plikach BE-1b: P3 brak limitu żądań na anonimowym endpoincie (odrzucone — wzorzec webhooka Stripe, nie regresja), P3 `CancellationToken` nieprzekazywany do Dappera (odrzucone — dług systemowy `IDapperWrapper`), P3 interpolacja sekretu w skrypcie SSH (przyjęte jako alfabet sekretu). Fałszywych P0/P1: 0. Luka z raportu wykonawcy (wyłączona integracja + niewiążąca się wartość → 500) naprawiona w BE-1-fix.
- Defekty po odbiorze: wykryty w BE-1-fix przez wykonawcę poprawek — parser webhooka rzucał na samotnym surogacie w NAZWIE pola przed sprawdzeniem sekretu (500 zamiast 401 dla nieuwierzytelnionego nadawcy, bez zmiany stanu); recenzent go nie zgłosił.
- Wymagane testy i dowody: `dotnet build` 0 ostrzeżeń; pełny `dotnet test` z bazą SQL architekta: 7554/7554 wykonanych i zielonych, 0 pominiętych; diff kontrolera, handlera i SQL scalania przeczytany.

### 2722-BE-1-fix (poprawki po recenzji fali 1: odczyt odporny na niepoprawny UTF-16, bramki sekretu, endpoint przy wyłączonej integracji) — 2026-10-19
- Archetyp: Backend — poprawki po recenzji w plikach niezmiennika (parser i interpreter JSON, bramki startu, handler), z testami mutacyjnymi.
- Stawka: wysoka / high-stakes (uwierzytelnienie powiadomienia, poświadczenie API).
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh` (runda 2 przez kontynuację tego samego agenta).
- Recenzent (linia / model / native effort): architekt (odbiór poprawek: diff, pełne testy); całość czyta bramka końcowa `gpt-6.1-sol` `max`.
- Dopuszczone alternatywy: brak (pliki niezmiennika; poprawki wracają do autora — reguła 13).
- Powód wyboru: autor kwalifikuje się nadal.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy — hook ŻÓŁTY (2026-10-19 ~13:57 UTC, okno 5 h 53 %).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: runda 1 zaakceptowana (752 s, 78 wywołań) z dwiema słusznymi uwagami do specyfikacji — samotny surogat w NAZWIE pola rzuca już przy `TryGetProperty`, także w parserze webhooka przed sprawdzeniem sekretu (500 zamiast 401), oraz alfabet sekretu tylko w komentarzu nie chroni przed cichym niedopasowaniem; runda 2 (1085 s, kontynuacja) domknęła oba wspólną kontrolą nazw w `Billing/Domain` i bramką alfabetu.
- Rundy korekt: 1 (z winy specyfikacji — luki wykryte przez wykonawcę, nie defekt wykonania).
- Czas do akceptacji: ~45 min (start ~13:57 UTC, akceptacja ~14:43 po pełnych testach).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): nie dotyczy (runda poprawek); testy mutacyjne wykonawcy: 9 + 16 przypadków czerwonych po wyłączeniu poprawek.
- Defekty po odbiorze: brak do bramki końcowej.
- Wymagane testy i dowody: `dotnet build` 0 ostrzeżeń; pełny `dotnet test` z bazą SQL architekta: 7593/7593 wykonanych i zielonych.
- Uwagi: recenzent z innej rodziny wskazał klasę błędu (P1), a wykonawca poprawek znalazł jej drugi, groźniejszy przypadek w pliku, którego recenzja nie zgłosiła — klauzula „What do you consider wrong” w briefie poprawek zwraca się także przy małych briefach.

### 2722-BE-2 (cykl synchronizacji stanu dokumentów: zaklepanie, reguły 1–8, transakcja zastosowania i zamknięcia) — 2026-10-19
- Archetyp: Backend — cykl w tle na `PeriodicCycleService` z dzierżawą (`UPDLOCK, READPAST`), rozstrzyganiem odczytu w jednej transakcji z zamknięciem żądania, ponowieniami z odstępem i wstawianiem korekty ręcznej; SQL repozytoriów, testy jednostkowe na harnessie i SQL.
- Stawka: wysoka / high-stakes (współbieżność, cichy błąd księgowy, wartość dokumentów).
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh`; trzy przebiegi tej samej linii (reguła 15): 1 — warstwa danych i SQL (przekazanie przy 302 tys.), 2 — cykl, resolver, usługa, rejestracja, harness (przekazanie przy ~311 tys., 61 wywołań, 841 s), 3 — testy w dwóch briefach (A jednostkowe + poprawka, B bazodanowe); uzupełnię.
- Recenzent (linia / model / native effort): Muse / `muse-wonder-full-1.0-contributor` / `max`, `-Access read` (po briefie B).
- Dopuszczone alternatywy: wykonawca — brak (CZERWONY: Muse Wonder Full `max`); recenzent — Codex `gpt-6.1-sol` `xhigh` (pula Codexa oszczędzana na bramkę).
- Powód wyboru: pliki niezmiennika high-stakes (współbieżność i naliczanie dokumentów).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany — hook ZIELONY przy przebiegach 2 i 3 (2026-10-19, okno 5 h 3–7 % po resecie, tydzień 9–10 %).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: kod produkcyjny przebiegów 1–2 przyjęty przez architekta po lekturze SQL, cyklu i resolvera, z jedną decyzją zmieniającą specyfikację (dokument z prefiksem Zebrani bez wiersza → `FOREIGN`, bo konto testowe Fakturowni jest wspólne dla lokalnego i PRE) i jedną poprawką wykrytą przy odbiorze (wyścig reguły 4 z cyklem wystawiania: wiersz po `IssueKey` z właśnie zapisanym tym samym `id` → fałszywe `FAILED`; poprawka w briefie A). Wykonawcy przebiegu 2 wydzielili `InvoiceSyncResolver` (limit S1200) i wskazali sprzeczność specyfikacji (reguła 4 „od razu FAILED” wobec listy testów „próba”) — słuszne.
- Rundy korekt: 0 z wykonania przed recenzją (poprawka wyścigu i dokładne porównanie id to decyzje architekta po odbiorze; uzupełnię po recenzji).
- Czas do akceptacji: uzupełnię (wykonanie ~2 h 10 min w czterech przebiegach, walidacja fali ~4 min).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): Muse Wonder Full `max` (1028 s) — 0×P0–P2, 3×P3: przyjęte 2 (test logowania wyjątku deklarował niesprawdzany niezmiennik; brak testu SQL wykrycia korekty Zebrani), odrzucone 1 (okno anulowania między zaklepaniem a wysyłką e-mail — tej samej długości co pozostałe okno); fałszywych P0/P1: 0. Poprawki w BE-2-fix.
- Defekty po odbiorze: wyścig reguły 4 (wykryty przez architekta przed testami). Wykonawca briefu B obalił założenie architekta o teście `READPAST` (blokada `UPDLOCK` samego indeksu klastrowego nie jest pomijana — `READPAST` działa tylko na przeglądanym indeksie) i zmierzył, że produkcyjne zapisy w transakcji blokują `IX_InvoiceSyncRequests_Due` — słuszne, bez defektu produkcyjnego.
- Wymagane testy i dowody: brief A (681 s, 57 wywołań, ~247 tys.): poprawka wyścigu + 79 przypadków jednostkowych, test wyścigu czerwony bez poprawki (4 czerwone); brief B (992 s, 62 wywołania, ~303 tys.): 22 testy SQL z kontrolami pozytywnymi i mutacjami M1/M2. Walidacja architekta: `dotnet build` 0 ostrzeżeń, pełny `dotnet test` z bazą SQL 7695/7695 wykonanych i zielonych.
- Uwagi: dwa kolejne przekazania przy ~300 tys. bez żadnego testu — brief cyklu high-stakes z SQL, regułami i testami jest dla Opusa `xhigh` za duży na jeden przebieg; z góry dzielić na: dane i SQL / cykl i rejestracja / testy jednostkowe / testy SQL (sygnał dla reguły 15).

### 2722-BE-3a (kontrola D2 przed wystawieniem korekty zwrotu) — 2026-10-19
- Archetyp: Backend — gałąź cyklu wystawiania + dwa pola odczytu SQL + testy bazodanowe cyklu z mutacjami.
- Stawka: wysoka / high-stakes (wystawianie dokumentów księgowych przy zwrocie).
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh` (BE-3 podzielony z góry na a i b po doświadczeniu BE-2).
- Recenzent (linia / model / native effort): Muse / `muse-wonder-full-1.0-contributor` / `max`, `-Access read` (wspólnie z BE-3b, jeden przebieg 880 s, statyczny).
- Dopuszczone alternatywy: wykonawca — brak (CZERWONY: Muse Wonder Full `max`); recenzent — Codex `gpt-6.1-sol` `xhigh`.
- Powód wyboru: pliki niezmiennika high-stakes (cykl wystawiania faktur).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany — hook ZIELONY (2026-10-19, okno 5 h 15–17 %).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: zaakceptowany — 775 s, 69 wywołań, ~254 tys. kontekstu (poniżej progu); 9 testów, 11 mutacji z czerwonymi testami; 3819/3819 testów Billing+SubscriptionManagement. Odstępstwa przyjęte: teksty w formacie istniejących („Wymaga…”, z kropką), testy cyklu bazodanowe (repo nie ma jednostkowych testów cyklu — przesłanka briefu błędna), `MarkExhaustedAsync` zwraca `bool`. Zgłoszone: okno wyścigu synchronizacji z wystawieniem korekty (odczyt → `CreateInvoiceAsync`), brak wznowienia po przywróceniu oryginału, „od razu” w dokumentacji (→ doprecyzowane).
- Rundy korekt: 0.
- Czas do akceptacji: ~15 min (start ~17:10 UTC, odbiór architekta po diffie).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0×P0–P2; 2×P3 potwierdzone, obie luki testów (korekta ręczna INNEGO oryginału nie blokuje — warunek `m.OriginalInvoiceId = o.InvoiceId` bez testu; brak testu pominięcia szczegółowego ostrzeżenia D2 po utracie dzierżawy) → T-BE-3 (`tester`); 0 odrzuconych. Werdykt poprawny, pewność 0,87.
- Defekty po odbiorze: brak defektu kodu; dwie luki testów zamknięte w 2722-T-BE-3 (do bramki końcowej).
- Wymagane testy i dowody: diff cyklu i SQL przeczytany przez architekta; testy z TRX wykonawcy; pełna walidacja fali 3 — `dotnet test` 7739/7739, build 0 ostrzeżeń, `browser-check` 4/4.
- Uwagi: brief podzielony z góry na dwa przebiegi zmieścił się w ~250 tys. bez przekazania — potwierdza wniosek z BE-2.

### 2722-BE-3b (zasada jednej korekty zwrotu i cofnięcie odrzuconego zwrotu bez korekt ręcznych, stan „Anulowana” w historii) — 2026-10-19
- Archetyp: Backend — trzy zmiany SQL (strażnik korekty, cofnięcie zwrotu, odczyt historii) + mapowanie w handlerze zapytania + testy SQL i jednostkowe z mutacjami.
- Stawka: wysoka / high-stakes (dokumenty księgowe przy zwrocie).
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh`.
- Recenzent (linia / model / native effort): Muse / `muse-wonder-full-1.0-contributor` / `max`, `-Access read` (wspólnie z BE-3a, jeden przebieg 880 s, statyczny).
- Dopuszczone alternatywy: wykonawca — brak (CZERWONY: Muse Wonder Full `max`); recenzent — Codex `gpt-6.1-sol` `xhigh`.
- Powód wyboru: pliki niezmiennika high-stakes (zwrot i korekta).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany — hook ZIELONY (2026-10-19, okno 5 h 17–21 %).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: zaakceptowany — 757 s, 88 wywołań, ~263 tys.; 21 nowych wyników testów, 6 mutacji z czerwonymi testami; 3840/3840. Odstępstwo przyjęte: literał źródła z komentarzem zamiast wyszukiwania po kodzie z `THROW` (brief architekta wewnętrznie sprzeczny z precedensem fal 1–2 — słuszna uwaga). Zgłoszone dwa przypadki brzegowe (anulowana korekta Zebrani blokuje nową; alarm kroku c) dla korekty Zebrani anulowanej w Fakturowni) — rozstrzygnięte przez architekta jako zachowawcze, bez zmian.
- Rundy korekt: 0.
- Czas do akceptacji: ~15 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 znalezisk dotyczących BE-3b (obie P3 recenzji dotyczyły testów BE-3a).
- Defekty po odbiorze: brak do bramki końcowej.
- Wymagane testy i dowody: diff handlera i SQL strażnika przeczytany przez architekta; pełna walidacja fali 3 — `dotnet test` 7739/7739, build 0 ostrzeżeń; `browser-check` 4/4 (360×530 i 1280×720, Light/Dark) na lokalnych danych syntetycznych: „Anulowana” czerwona z `pi pi-ban`, korekta ręczna „Korekta” 0,00 zł bez minusa.

### 2722-BE-2-fix (poprawki po recenzji fali 2 + ostrzeżenie o anulowaniu faktury z korektą zwrotu) — 2026-10-19
- Archetyp: Backend — poprawka dokumentacji klasy i testu logowania wyjątku, testy SQL wykrycia korekty Zebrani, nowe ostrzeżenie w resolverze i cyklu synchronizacji (wykrycie okna wyścigu z cyklem wystawiania).
- Stawka: wysoka / high-stakes.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh` (poprawki wracają do linii autora, świeży agent).
- Recenzent (linia / model / native effort): architekt (odbiór poprawek); całość czyta bramka końcowa `gpt-6.1-sol` `max`.
- Dopuszczone alternatywy: brak (pliki niezmiennika; reguła 13).
- Powód wyboru: autor kwalifikuje się nadal.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany — hook ZIELONY (2026-10-19, okno 5 h 21–24 %).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: zaakceptowany — 792 s, 68 wywołań, ~266 tys.; 10 mutacji (jedna zablokowana przez analizator S6667 — sam pilnuje logowania obiektu wyjątku), 3854/3854. Wykonawca rozszerzył wykrycie na wszystkie trzy ścieżki reguły 1 (także wyścigowe) — słuszne. Zgłosił powtarzanie ostrzeżenia przy każdym kolejnym powiadomieniu o już anulowanej fakturze (przyjęte jako techniczne) i rozjazd pierwszego zdania pkt 6 dokumentacji z kodem (`PENDING`) — dokumentacja doprecyzowana.
- Rundy korekt: 0.
- Czas do akceptacji: ~15 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): nie dotyczy (runda poprawek).
- Defekty po odbiorze: brak do bramki końcowej.
- Wymagane testy i dowody: TRX wykonawcy; pełna walidacja architekta w fali 3.

### 2722-T-BE-3 (dwa testy bazodanowe D2 po recenzji fali 3, z dowodem czerwieni przez mutację) — 2026-10-19
- Archetyp: Testy BE — xunit `[SqlServerFact]` do istniejącego pliku + dekorator repozytorium w `Support`, dwie mutacje kodu produkcyjnego z przywróceniem po hashu.
- Stawka: średnia (testy niezmiennika high-stakes, bez zmiany kodu produkcyjnego).
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Claude / `tester` — Haiku 5.5 / `xhigh`.
- Recenzent (linia / model / native effort): architekt (odbiór testów i mutacji); całość czyta bramka końcowa `gpt-6.1-sol` `max`.
- Dopuszczone alternatywy: `wykonawca` Sonnet `high`; Codex `gpt-6.1-sol` `high` (≤ 5 plików, pula `nieznany` — oszczędzana na bramkę).
- Powód wyboru: scenariusze nazwane w briefie, wzorzec w tym samym pliku — linia `tester` po próbie 2026-10-13.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany — hook ZIELONY (2026-10-19, okno 5 h 25–27 %).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: zaakceptowany — 464 s, 35 wywołań, ~245 tys. tokenów; 2 testy + dekorator w nowym pliku `Support` (odstępstwo od „do istniejącego pliku” — słuszne, wzorzec katalogu), obie mutacje czerwone na właściwej asercji, hashe plików produkcyjnych zgodne z kopią, 44/44 w filtrze. Słuszne uwagi do briefu: mutacja „usuń warunek” zostawia `WHERE` bez warunku (zastąpiono `1 = 1`), postać blokowa mutacji 2 łamie S1199, test 1 wymagał rozstrzygnięcia dzierżawy między odczytem a cyklem (wygasła dzierżawa).
- Rundy korekt: 0.
- Czas do akceptacji: ~12 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): nie dotyczy (domknięcie luk recenzji fali 3).
- Defekty po odbiorze: brak do bramki końcowej.
- Wymagane testy i dowody: build `--no-incremental` 0/0 i pełny `dotnet test` architekta po zmianie — 7741/7741 (7739 + 2 nowe), 0 ostrzeżeń.
- Uwagi: Haiku `xhigh` zmieścił brief testów z mutacjami poniżej 250 tys. bez przekazania.

### 2722-GATE-FE (bramka końcowa feature'a wysokiej stawki — FE) — 2026-10-19
- Archetyp: Recenzja — bramka końcowa całego diffu FE funkcji (5 plików: enum, mapa etykiet, pl/en, spec), tylko odczyt.
- Stawka: wysoka (bramka reguły 6; sam diff FE bez niezmiennika).
- Niepewność: niska.
- Wykonawca (linia / model / native effort): nie dotyczy (autor FE-1: Gemini `gemini-3.8-flash-high`).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `max`, `-Mode review`.
- Dopuszczone alternatywy: brak (bramka reguły 6 bez obniżania).
- Powód wyboru: bramka końcowa; uruchomiona przed BE, bo diff FE był ostateczny od fali 1, a BE czekał na testy — bramki nadal sekwencyjnie.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper bez zapasu, 2026-10-19 ~16:13 UTC); bez komunikatu limitu.
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: 243 s; 0 znalezisk. Recenzent sam sprawdził konsumentów `InvoiceStatus`, mapę etykiet i streszczenie „Ostatnia: …” z anulowaną pierwszą pozycją (skryptem tylko do odczytu); Vitest/AXE nieuruchamiane (piaskownica tylko do odczytu).
- Rundy korekt: 0.
- Czas do akceptacji: ~5 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: walidacja FE fali 1 (lint, 12/12 speców, build) i `browser-check` 4/4 w fali 3.

### 2722-GATE-BE (bramka końcowa feature'a wysokiej stawki — BE) — 2026-10-19
- Archetyp: Recenzja — bramka końcowa całego diffu BE funkcji (26 plików śledzonych + 69 nowych, trzy fale po recenzjach i poprawkach), tylko odczyt.
- Stawka: wysoka / high-stakes (uwierzytelnienie powiadomienia, dokumenty księgowe przy zwrocie, współbieżność, migracja).
- Niepewność: średnia (duży diff, współbieżność).
- Wykonawca (linia / model / native effort): nie dotyczy (pliki niezmiennika: `wykonawca-opus`; testy T-BE-3: `tester`).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `max`, `-Mode review`.
- Dopuszczone alternatywy: brak (bramka reguły 6 bez obniżania).
- Powód wyboru: bramka końcowa reguły 6, po recenzjach fal 1–3 (Muse Wonder Full `max`) i ich poprawkach.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper, 2026-10-19 ~16:17 UTC); bez komunikatu limitu.
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: 603 s; werdykt niepoprawny; 3 znaleziska. Znalazła tylko bramka (trzy recenzje fal Muse ich nie zgłosiły).
- Rundy korekt: 1 (BE-GATE-fix u `wykonawca-opus`, oba defekty w jednym przebiegu).
- Czas do akceptacji: ~45 min od startu bramki (bramka 10 min, triaż ~10 min, poprawka 14 min, walidacja ~6 min).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): P1 potwierdzony — opis niepowodzenia odczytu spoza 2xx niesie oczyszczoną treść odpowiedzi z danymi nabywcy do `LastError` żądania i ostrzeżenia po wyczerpaniu prób (dziennik klienta czysty, cyklu nie); P2 potwierdzony — ostrzeżenie o korekcie ręcznej przy korekcie zwrotu bierze stan sprzed wstawienia, przeplot ze zwrotem i cyklem wystawiania gubi alarm z pkt 6; P2 odrzucony — „brak obsługi formularza”: błędna przesłanka briefu architekta (rozpoznanie ustaliło wyłącznie JSON, brief bramki powtórzył nieaktualne „JSON albo formularz” z planu).
- Defekty po odbiorze: brak (po BE-GATE-fix).
- Wymagane testy i dowody: po BE-GATE-fix — build 0/0, pełny `dotnet test` 7750/7750, mutacje obu poprawek czerwone (16 + 2 testy).
- Uwagi: lekcja dla architekta — brief bramki składać z ustaleń rozpoznania i decyzji fal, nie z planu sprzed rozpoznania.

### 2722-BE-GATE-fix (poprawki po bramce końcowej BE: opis błędu odczytu bez treści odpowiedzi, ostrzeżenie o korekcie ręcznej po wstawieniu) — 2026-10-19
- Archetyp: Backend — stała opisu w interpreterze odczytu, ponowny odczyt w resolverze w transakcji, dokumentacja XML, testy klienta i cyklu z prawdziwym interpreterem w pętli, mutacje.
- Stawka: wysoka / high-stakes (dane osobowe w dzienniku, alarm podwójnej korekty).
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh` (poprawki wracają do linii autora).
- Recenzent (linia / model / native effort): architekt (odbiór dowodem — reguła: po korekcie bez drugiej recenzji, ≤ 5 plików produkcyjnych, bez zmiany API).
- Dopuszczone alternatywy: brak (pliki niezmiennika).
- Powód wyboru: autor kwalifikuje się nadal.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany — hook ZIELONY (2026-10-19, okno 5 h 28–31 %).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: zaakceptowany — 824 s, 72 wywołania, ~258 tys.; 3865/3865 w filtrze; mutacja G1 → 16 testów czerwonych, G2 → 2; hashe przywróconych plików zgodne. Odstępstwa przyjęte: hak w atrapie zamiast sekwencji wyników (pilnuje też kolejności odczytu), dwie asercje liczby odczytów w istniejących testach, mutacja G2 przez `_ =` (nieużywana zmienna łamie build). Słuszne uwagi: jedno zdanie dokumentacji `FakturowniaInvoiceReadResult` (dopisał architekt, reguła 11), założenie o RCSI niepilnowane testem, teoretyczne zakleszczenie przy skanie bez indeksu na `OriginalInvoiceId` (bez znalezionego przeplotu; ofiara dostaje regułę 8).
- Rundy korekt: 0.
- Czas do akceptacji: ~20 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): nie dotyczy (runda poprawek bramki).
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: pełny `dotnet test` architekta 7750/7750, build `--no-incremental` 0/0, diff resolvera i interpretera przeczytany.

### 2722-DOC-REV (przegląd zgodności dokumentacji 4c — rewizje INT-FAKTUROWNIA i UI-KONTO-USTAWIENIA wobec kodu obu repo) — 2026-10-19
- Archetyp: Recenzja — macierz zgodności dokumentacji produktu z kodem (2 dokumenty zmienione, 15 sekcji, 95 plików BE + 5 FE), tylko odczyt.
- Stawka: średnia (dokumentacja funkcji wysokiej stawki; kod już po bramce końcowej).
- Niepewność: niska.
- Wykonawca (linia / model / native effort): nie dotyczy (rewizje dokumentacji: Muse Wonder Full `max` w DOC-1, poprawki w falach).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high` (effort w nazwie), `-Access read`.
- Dopuszczone alternatywy: Codex `gpt-6.1-sol` `high` (pula Codexa oszczędzana po bramce).
- Powód wyboru: inna rodzina niż autor dokumentacji (Muse); przegląd czytający bez powłoki.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany (wrapper, 2026-10-19); bez 503 i bez komunikatu limitu.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 632 s; werdykt „zgodne z zastrzeżeniem” (0,98); 57 twierdzeń `zgodne`, 1 `dokument nieaktualny`.
- Rundy korekt: 0.
- Czas do akceptacji: ~15 min (przebieg + triaż).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1 częściowo trafne — definicja sygnału „Płatność bez faktury” w UI-ADMINISTRATOR-DASHBOARD („płatność, której dokument…”) nie obejmuje dosłownie korekty bez płatności. Sygnału nie ma w kodzie (PBI #1727), a INT trzyma się zatwierdzonej konwencji „po stanie zlecenia” (rewizja 2026-10-13 pkt 1). Bez zmiany dokumentacji tego PBI; pytanie do właściciela (to samo co wpis 4 dziennika rozbieżności, zgłoszony wcześniej przez Muse w DOC-1).
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: raport z `result.response` NDJSON; diff dokumentacji przeczytany przez architekta (2 pliki, +31/−1); `git status` repo bez zmian po przebiegu.
- Uwagi: brief z mapą dokumentacji i listą plików generowaną skryptem (Python, `chr(92)`) — ścieżki Windows w heredocu Basha gubiły ukośniki.

### 2722-QAS (przypadki QA Sphere: przegląd 49 istniejących + 16 nowych do synchronizacji faktur z Fakturowni) — 2026-10-19
- Archetyp: Autor QA Sphere — plik podglądu wg `qasphere-test-generator` (Krok 2b przegląd istniejących + nowe przypadki), recenzja krzyżowa innej rodziny.
- Stawka: średnia (przypadki manualne funkcji wysokiej stawki; zapis do QA Sphere dopiero po bramie właściciela).
- Niepewność: średnia (zachowanie Fakturowni sprawdzalne tylko w panelu sandboxa; wspólne konto z innym produktem).
- Wykonawca (linia / model / native effort): Muse / `muse-wonder-full-1.0-contributor` / `max`, `-Access write` (generator 1137 s; poprawka K 395 s; poprawka K2 223 s).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high` (effort w nazwie), `-Access read`, 372 s.
- Dopuszczone alternatywy: autor — Gemini write (procedura skilla, gdy Muse zajęty); recenzent — brak poza Gemini (procedura skilla: plik Muse → Gemini read).
- Powód wyboru: procedura pomocniczego skilla (Muse Wonder Full `max` autorem, krzyżowa recenzja Gemini); routing ogólny jej nie nadpisuje.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Muse nieznany, Gemini nieznany (wrapper, 2026-10-19); bez komunikatu limitu i bez 503.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 16 nowych (high 6, medium 8, low 2), przegląd 49 istniejących: 48 keep, 1 update (1651), 0 retire; `qas.py lint` 0 błędów.
- Rundy korekt: 2 — K po recenzji (krok GET → 405 w A10, zamknięcie kreatora programów w warunkach wstępnych i w A13, stała kolejność z fakturą pomocniczą w A1/A7 zamiast warunku, uzasadnienie keep dla 1000), K2 po kontroli architekta (A10: odpowiedź 401 ma standardowy opis błędu w JSON, nie puste ciało; tytuł obejmuje GET → 405).
- Czas do akceptacji: ~60 min (generator, recenzja, dwie poprawki, kontrole architekta).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 4 potwierdzone, 0 odrzuconych — 2×P2 (brak kroku GET → 405 w A10; brak zamknięcia kreatora w A13 na telefonie), 2×P3 (warunkowe obejście 422 Fakturowni w A1/A7; uzasadnienie keep dla 1000 bez wartości domyślnej źródła). Recenzent przeoczył 1 błąd faktu: A10 oczekiwał pustego ciała odpowiedzi 401 — architekt wykrył go kontrolą wyrywkową (`curl` na PRE: ProblemDetails 165 B), poprawiony w K2.
- Defekty po odbiorze: brak (do potwierdzenia w `qas.py verify` po zapisie).
- Wymagane testy i dowody: `qas.py lint` 0 po każdej rundzie; `qas.py table`; fakty kroków sprawdzone na PRE (422 dla ostatniej faktury w numeracji, 405 dla GET, 401 z ProblemDetails, kreator programów na koncie bez programów).
- Uwagi: Recenzent Gemini nie wychwycił twierdzenia sprzecznego z zachowaniem serwera, którego nie miał w faktach briefu — fakty z PRE (kształt odpowiedzi) warto podawać w briefie recenzji jawnie, nie tylko kod statusu.

### 2371-BE-1 (pośrednik pobierania dokumentu z systemu fakturowego: klient, odczyt z zakresem konta, endpoint, testy) — 2026-10-19
- Archetyp: Backend — nowy odczyt binarny w kliencie integracji (termin, limit rozmiaru, kontrola typu i sygnatury), zapytanie CQRS z zakresem konta, endpoint pliku, testy klienta, handlera i API.
- Stawka: wysoka / high-stakes (niezmiennik: właściciel pobiera wyłącznie dokumenty swojego konta; nowa ścieżka użycia klucza API integracji).
- Niepewność: średnia (odczyt strumienia z limitem i wspólnym terminem; zachowanie dostawcy zmierzone przed planem).
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh`.
- Recenzent (linia / model / native effort): Muse / `muse-wonder-full-1.0-contributor` / `max`, `-Access read` (wpis 2371-REV-BE); bramka końcowa 2371-GATE-BE.
- Dopuszczone alternatywy: brak (pliki niezmiennika; przy CZERWONYM Muse Wonder Full `max`).
- Powód wyboru: bramka twarda high-stakes (autoryzacja zakresu konta i poświadczenie integracji).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy — hook ŻÓŁTY (2026-10-19 ~19:18 UTC).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: zaakceptowany — 1492 s, 117 wywołań; build 0 ostrzeżeń, pełny `dotnet test` 7838/0 pominiętych.
- Rundy korekt: 1 (BE-K1 + kontynuacja K2: wyłącznie testy po 2×P3 recenzji — siatka bezpieczeństwa przy wiszącej treści, test jednego wspólnego terminu, statusy spoza 2xx z nieczytelną treścią także w bliźniakach ścieżki tekstowej; 1331 s łącznie, mutacje M1–M7 czerwone). Przesłanka briefu K1 częściowo błędna (sama siatka w wywołaniu nie zatrzyma zawieszenia, gdy kod przekazuje pusty token) — wykonawca słusznie przeniósł siatkę do atrap strumienia.
- Czas do akceptacji: ~25 min pierwszy przebieg + ~30 min korekta testów.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): recenzja fali — 2×P3 potwierdzone (testy); bramka — 1×P2 potwierdzony jako dług systemowy (token anulowania nie trafia do warstwy dostępu do danych w całym repo), bez poprawki w PBI.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: build 0/0, pełny `dotnet test` 7842/0 po korekcie, diff przeczytany; curl na PRE po deployu (krok 12).

### 2371-FE-1 (działanie pobrania w historii dokumentów: wspólny helper zapisu pliku, serwis, liść prezentacyjny, rodzic, i18n, speci) — 2026-10-19
- Archetyp: Frontend UI / Figma — przycisk-ikona w tabeli i kartach wg makiety, wyniesienie istniejącego wzorca zapisu pliku do wspólnego serwisu, obsługa dwóch komunikatów błędu, AXE.
- Stawka: średnia (ekran funkcji high-stakes bez niezmiennika — autoryzację trzyma BE).
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Claude / `wykonawca` — Sonnet 5.5 / `high` (Figma MCP).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (wpis 2371-REV-FE); bramka końcowa 2371-GATE-FE.
- Dopuszczone alternatywy: Codex z Figmą (niepotwierdzony w sesji, pula na bramkę).
- Powód wyboru: wygląd przycisku z makiety wymaga MCP; próba A/B linii Figmy zamknięta → Sonnet.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy — hook ŻÓŁTY (2026-10-19 ~19:18 UTC).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowany z korektami — 523 s, 74 wywołania; lint/format/4583 testy/build zielone; browser-check 8/8 + przejście PASS.
- Rundy korekt: 2 — FE-K1 po recenzji fali (148 s), FE-K2 po bramce (84 s: przerwanie pobrania przy zmianie konta w karcie, zgodnie z istniejącą regułą produktu).
- Czas do akceptacji: ~55 min (z recenzją i bramką).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): recenzja fali — 3×P1 zgłoszone: 1 sporne, 2 obniżone do P3; 3×P2, 2×P3; bramka — 1×P2 potwierdzony (toast i zapis po zmianie konta w trakcie pobierania), którego recenzja fali nie zgłosiła.
- Defekty po odbiorze: brak. Przy browser-check wykryty defekt sprzed PBI (komórka numeru z `inline-flex` rozjeżdżała kolumnę na desktopie) — poprawiony mechanicznie (`mechanik`, 46 s).
- Wymagane testy i dowody: `npm run lint`, `format:check`, `npm test` 4585 (AXE w środku), `npm run build`; browser-check matrix 2×2 + flows; zrzuty obejrzane.

### 2371-FIG-1 (piąta kolumna działania w tabeli desktopowej, Light i Dark) — 2026-10-19
- Archetyp: Frontend UI / Figma — makieta (dodanie kolumny z instancją przycisku z biblioteki).
- Stawka: niska.
- Niepewność: średnia (struktura tabeli w makiecie nieznana przed briefem).
- Wykonawca (linia / model / native effort): Claude / `wykonawca` — Sonnet 5.5 / `high` (Figma MCP).
- Recenzent (linia / model / native effort): architekt — zrzuty i struktura węzłów (makieta bez kodu, jak 2722-FIG-1).
- Dopuszczone alternatywy: brak (Figma MCP potwierdzony tylko w linii Claude).
- Powód wyboru: jedyna linia z potwierdzonym Figma MCP.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy — hook ŻÓŁTY (2026-10-19 ~19:18 UTC).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: STOP bez zmian (65 s) — błędna przesłanka briefu: tabela nie jest komponentem głównym, tylko luźnymi ramkami bez auto-layoutu w dwóch niezależnych kopiach (Light/Dark). Klauzula STOP zadziałała.
- Rundy korekt: 1 (z winy specyfikacji; wariant „dodaj w obu kopiach”, 208 s) — zaakceptowany.
- Czas do akceptacji: ~10 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): brak.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: zrzuty sekcji w obu motywach; 6 instancji przycisku z właściwościami identycznymi z arkuszem mobilnym.

### 2371-DOC-1 (trzy datowane rewizje dokumentów zatwierdzonych: integracja, interfejs ustawień, reguła abonamentu) — 2026-10-19
- Archetyp: Dokumentacja produktowa — rewizje w granicach decyzji właściciela.
- Stawka: średnia (źródło prawdy funkcji high-stakes).
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Muse / `muse-wonder-full-1.0-contributor` / `max`, `-Access write`.
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (Faza 4c, wpis 2371-DOC-4C).
- Dopuszczone alternatywy: Gemini `high` write, Sonnet `high`.
- Powód wyboru: decyzje gotowe, inna pula; precedens 2722-DOC-1 (0 korekt).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Muse nieznany (wrapper, 2026-10-19 19:28 UTC).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 484 s; rewizje poprawne, raport kontroli wpływu wskazał 5 miejsc sprzecznych z decyzją poza mapą briefu (zdanie o KSeF, „pusty odnośnik”, literały komunikatów w dwóch dokumentach, nazwa pliku korekty bez numeru, napisy brzegowe).
- Rundy korekt: 1 (DOC-1b, 786 s — z winy specyfikacji: mapa dokumentacji w briefie pominęła te miejsca).
- Czas do akceptacji: ~25 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): Faza 4c — 4× `brak w dokumencie` potwierdzone (zachowania z kodu nieopisane: limit rozmiaru i sygnatura, `aria-busy`, przerwanie po opuszczeniu widoku) — dopisane przez architekta; 1× `kod odbiega` odrzucony.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: diff dokumentacji przeczytany (3 pliki); dziennik rozbieżności 11 wpisów, wszystkie zamknięte.
- Uwagi: 2026-10-19 ~20:01 UTC pierwszy 429 Muse na planie Power Usage („Subscription quota exhausted”, reset 20:19:58 UTC) — po DOC-1 + DOC-1b i ~7,5 min recenzji na Wonder Full `max`. Pierwszy sygnał limitu linii Muse od zmiany planu.

### 2371-REV-FE (recenzja fali FE + audyt SCSS w jednym przebiegu) — 2026-10-19
- Archetyp: Recenzja — diff FE fali 1 (helper, serwis, liść, rodzic, i18n, speci) + audyt SCSS zmienionych arkuszy, tylko odczyt.
- Stawka: średnia.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): nie dotyczy (autor: `wykonawca` Sonnet 5.5 `high`).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read`.
- Dopuszczone alternatywy: Muse Wonder Full `max` read.
- Powód wyboru: niska/średnia stawka → preferencja Sol `high` albo Gemini `high` przed Muse (reguła 13); Sol odpada, bo pula idzie na bramkę.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany (wrapper, 2026-10-19 19:44 UTC); bez 503.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 625 s; raport kompletny z audytem SCSS (wszystkie reguły, werdykt „zostawić”).
- Rundy korekt: 0 (recenzja).
- Czas do akceptacji: ~20 min z triażem.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 3×P1 zgłoszone — 1 sporne, 2 obniżone do P3 po sprawdzeniu scenariusza; 3×P2, 2×P3 — przyjęte do FE-K1. Przeoczył P2 zmiany konta w trakcie pobierania (znalazła dopiero bramka).
- Defekty po odbiorze: 1×P2 znaleziony przez bramkę (FE-K2).
- Wymagane testy i dowody: raport z logu wrappera; `git status` bez zmian po przebiegu.

### 2371-REV-BE (recenzja fali BE: klient binarny, zakres konta, endpoint) — 2026-10-19
- Archetyp: Recenzja — diff BE fali 1, tylko odczyt.
- Stawka: wysoka / high-stakes.
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): nie dotyczy (autor: `wykonawca-opus` Opus 5.5 `xhigh`).
- Recenzent (linia / model / native effort): Muse / `muse-wonder-full-1.0-contributor` / `max`, `-Access read`.
- Dopuszczone alternatywy: Gemini `flash-high` read (za słaby na high-stakes BE wg architekta); Sol odpada — pula na bramkę.
- Powód wyboru: wyższa stawka → Muse Wonder Full `max` jako kandydat wyższej klasy, inna rodzina niż autor.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Muse zablokowany — 429 „Subscription quota exhausted” 2026-10-19 ~20:01 UTC (po 455 s przebiegu), reset 20:19:58 UTC; potem nieznany.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: przerwany limitem (455 s, exit 1); ponowiony po resecie — 2102 s (z ponowieniami „no first model event within 300000ms”), werdykt poprawny, pewność 0,90.
- Rundy korekt: 0 (recenzja); ponowna kwalifikacja po limicie: czekanie zamiast zmiany linii.
- Czas do akceptacji: ~60 min od pierwszego startu (w tym ~19 min czekania na reset).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0×P0–P2; 2×P3 potwierdzone (luki testów klienta) → BE-K1/K2. Nie zgłosił P2 tokenu anulowania (znalazła bramka, sklasyfikowany jako dług systemowy).
- Defekty po odbiorze: brak defektu kodu funkcji.
- Wymagane testy i dowody: raport z logu wrappera; `git status` BE bez zmian po przebiegu.

### 2371-GATE-BE (bramka końcowa feature'a wysokiej stawki — BE) — 2026-10-19
- Archetyp: Recenzja — bramka końcowa całego diffu BE funkcji, tylko odczyt.
- Stawka: wysoka / high-stakes.
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): nie dotyczy (pliki niezmiennika: `wykonawca-opus`).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `max`, `-Mode review`.
- Dopuszczone alternatywy: brak (reguła 6); przy limicie Codexa Muse Wonder Full `max` wg zgody właściciela dla tej funkcji.
- Powód wyboru: bramka reguły 6 po recenzji fali i poprawkach.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper, 2026-10-19 21:22 UTC); bez komunikatu limitu.
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: 302 s; brak P0/P1, bezpieczeństwo (zakres konta, wyciek poświadczenia) bez uwag; 1×P2.
- Rundy korekt: 0 — P2 (token anulowania nie trafia do zapytania Dappera) to wzorzec całego repo: interfejs dostępu do danych nie ma przeciążeń z tokenem; poprawka w PBI niespójna i poza zakresem → propozycja osobnego PBI refaktoru.
- Czas do akceptacji: ~15 min (przebieg + triaż).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1×P2 potwierdzony jako dług systemowy (nie defekt funkcji).
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: raport bramki; build 0/0, `dotnet test` 7842/0 (stan po BE-K1/K2).

### 2371-GATE-FE (bramka końcowa feature'a wysokiej stawki — FE) — 2026-10-19
- Archetyp: Recenzja — bramka końcowa całego diffu FE funkcji, tylko odczyt.
- Stawka: wysoka / high-stakes (FE funkcji high-stakes; reguła 6 dla całego feature'a).
- Niepewność: niska.
- Wykonawca (linia / model / native effort): nie dotyczy (autor: `wykonawca` Sonnet 5.5 `high`).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `max`, `-Mode review`.
- Dopuszczone alternatywy: brak (reguła 6).
- Powód wyboru: bramka reguły 6 po recenzji fali i FE-K1.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper, 2026-10-19 20:11 UTC).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: 329 s; 1×P2 — zmiana konta w karcie w trakcie pobierania kończyła się zapisem pliku poprzedniego konta albo toastem błędu (łamie istniejącą regułę zmiany konta w karcie).
- Rundy korekt: 1 (FE-K2 u autora, 84 s); bez drugiej rundy bramki (2 pliki, bez zmiany API).
- Czas do akceptacji: ~20 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1×P2 potwierdzony; znalazła tylko bramka.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: po FE-K2 — `npm test` 4585, build; dopisane zdanie dokumentacji (UI rew. 2026-10-19 pkt 4).

### 2371-QAS (przypadki QA Sphere: przegląd 65 istniejących + 14 nowych dla pobierania dokumentu) — 2026-10-19
- Archetyp: Autor QA Sphere — plik podglądu wg `qasphere-test-generator` (Krok 2b + nowe), recenzja krzyżowa innej rodziny.
- Stawka: średnia.
- Niepewność: średnia (zachowanie dostawcy fakturowego tylko w panelu sandboxa; anulowanie przez zmianę rodzaju dokumentu).
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access write` (generator 656 s, korekta K1 635 s).
- Recenzent (linia / model / native effort): Muse / `muse-wonder-full-1.0-contributor` / `max`, `-Access read` (1448 s).
- Dopuszczone alternatywy: autor Muse Wonder Full `max` (domyślny w procedurze skilla).
- Powód wyboru: procedura skilla — Gemini write, gdy Muse zajęty lub z limitem (Muse: recenzja BE w toku i 429 o ~20:01 UTC); plik Gemini → recenzja Muse read.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany; Muse zablokowany do 20:19:58 UTC, potem nieznany (wrapper, 2026-10-19).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 13 nowych, 65 keep, `qas.py lint` 0 — ale warunki wstępne niesamowystarczalne i oparte na danych seedu bez dokumentu u dostawcy.
- Rundy korekt: 1 (K1 po recenzji: 14 nowych — high 6, medium 7, low 1 — 65 keep, lint 0).
- Czas do akceptacji: ~70 min (generator, recenzja, korekta, kontrola wyrywkowa P1).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 4×P1 potwierdzone (wymyślona ścieżka anulowania w panelu sprzeczna z dokumentacją; brak uwagi o koncie bez profilu rozliczeniowego; pozycja „W przygotowaniu” cudzego konta w przypadku izolacji; pozycja seedowa bez dokumentu u dostawcy w dwóch przypadkach); 5×P2, 5×P3 przyjęte; 0 odrzuconych.
- Defekty po odbiorze: do potwierdzenia w `qas.py verify` po zapisie.
- Wymagane testy i dowody: `qas.py lint` 0 po każdej rundzie; P1 sprawdzone wyrywkowo w pliku.
- Uwagi: Muse Wonder Full jako recenzent QA — 0 fałszywych P1 w tym przebiegu (wobec historycznej obserwacji Sparka `xhigh`).

### 2371-DOC-4C (przegląd zgodności dokumentacji 4c — trzy rewizje wobec kodu obu repo) — 2026-10-19
- Archetyp: Recenzja — macierz zgodności dokumentacji z kodem (3 dokumenty + notatka schematu, 12 sekcji), tylko odczyt.
- Stawka: średnia.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): nie dotyczy (autor rewizji: Muse Wonder Full `max`).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read`.
- Dopuszczone alternatywy: Codex `gpt-6.1-sol` `high` (pula po bramkach).
- Powód wyboru: inna rodzina niż autor dokumentacji; precedens 2722-DOC-REV.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany (wrapper, 2026-10-19 21:29 UTC).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 448 s; 42 `zgodne`, 4 `brak w dokumencie`, 1 `kod odbiega`.
- Rundy korekt: 0.
- Czas do akceptacji: ~20 min (przebieg + triaż + dopisanie zdań).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 4 potwierdzone (limit rozmiaru i sygnatura dokumentu, `aria-busy`, przerwanie po opuszczeniu widoku — dopisane w dokumentach); 1 odrzucony (zapasowa nazwa pliku w FE dla korekty — gałąź nieosiągalna w kontrakcie, nazwę zawsze nadaje BE w nagłówku, ten sam adres `/api/`). Słuszna uwaga do briefu: streszczenie „usunięty = Anulowana → 410” w briefie było nieprecyzyjne (dokument mówi to precyzyjnie).
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: raport z logu wrappera; każde „brak w dokumencie” sprawdzone w kodzie (`plik:linia`); `git status` bez zmian po przebiegu.

### 2747-DOC-1 (datowana rewizja dokumentu interfejsu — 7 punktów z decyzji zatwierdzonych z góry) — 2026-10-20
- Archetyp: Dokumentacja produktowa — rewizja `zatwierdzonego` dokumentu z kontrolą wpływu (§10, §12), jeden plik.
- Stawka: średnia (dokument źródłowy funkcji wysokiej stawki; bez kodu).
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access write`.
- Recenzent (linia / model / native effort): przegląd 4c (Muse Wonder Full `max` read) — po falach.
- Dopuszczone alternatywy: Muse Wonder Full `max` write; Codex `gpt-6.1-sol` `high` (pula na bramkę).
- Powód wyboru: dokumentacja na Gemini `high` — 7 briefów / 0,1 rundy (przegląd 1); Muse wolny na recenzje i B2.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany (wrapper, 2026-10-19 22:13 UTC).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowano — 326 s, +15 linii tylko w dokumencie docelowym, front matter bez zmian, kontrola wpływu na 3 dokumentach bez sprzeczności.
- Rundy korekt: 0.
- Czas do akceptacji: ~10 min (przebieg + diff + triaż uwag).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): sekcja „co błędne w specyfikacji” — 4 uwagi: 1 przyjęta w tekście (dwuznaczne „pkt 3” → „pkt 3 rewizji 2026-10-14”); 1 słuszna poza zakresem (komunikat oczekiwania obiecuje „abonament znów zadziała” po 1. z 2 faktur — pytanie do właściciela); 2 odrzucone (podważały zatwierdzone D5 i D6; `p-message` ma `role=alert`, wzorzec fokusu `#arrearsError`).
- Defekty po odbiorze: brak (do przeglądu 4c).
- Wymagane testy i dowody: `git diff` repo Dokumentacja (1 plik, tylko dopisana sekcja), `git status` — cudza praca `zasoby/teczki/` nietknięta.

### 2747-R1 (recenzja fali 1: logika przepływu opłaty zaległości — ponowny odczyt po płatności) — 2026-10-20
- Archetyp: Recenzja — logika przepływu FE z niezmiennikiem płatności (1 plik kodu + 2 spece, ~800 linii diffu), tylko odczyt.
- Stawka: wysoka.
- Niepewność: średnia (nowy niezmiennik D3, wyścigi odczytu / sprawdzania / spóźnionego `PAID`).
- Wykonawca (linia / model / native effort): nie dotyczy (autor B1: Claude `wykonawca-opus`, Opus 5.5 `xhigh`).
- Recenzent (linia / model / native effort): Muse / `muse-wonder-full-1.0-contributor` `max`, `-Access read`.
- Dopuszczone alternatywy: Gemini `gemini-3.8-flash-high` read; Codex `gpt-6.1-sol` (pula zostaje na bramkę końcową).
- Powód wyboru: wyższa stawka; inna rodzina niż autor; lokalnie 0 fałszywych P0/P1 Wondera Full w recenzjach 2694/2371.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Muse nieznany (wrapper, 2026-10-19 22:38 UTC; po resecie tygodniowym 2026-10-19 00:00 UTC).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 1146 s; werdykt „niepoprawny” (0,87); 1×P1, 1×P3.
- Rundy korekt: 0 (recenzja); korekta autora B1-K1.
- Czas do akceptacji: ~25 min (przebieg + triaż).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): P1 potwierdzone — migawka tylko ostatnio opłaconej faktury pozwala starszej opłaconej wrócić do `Ready` (A → B → odczyt A; osiągalne przy niespójności operatora, niezmiennik D3 dosłownie złamany; spec sam modelował sekwencję B → A dla `PROCESSING`) → mapa wszystkich opłaconych; P3 potwierdzone jako brak testu, rozwiązane przez korektę architekta (wejście D3 zeruje komunikaty → zerowanie w `markPaid` nieosiągalne z `true`). 0 fałszywych P0/P1. Słuszna uwaga do briefu: zdanie „serwer odrzuca nieaktualną fakturę” nie jest siatką bezpieczeństwa, gdy odczyt na żywo zwraca opłaconą fakturę.
- Defekty po odbiorze: do bramki końcowej.
- Wymagane testy i dowody: raport z logu wrappera; `git status` bez zmian po przebiegu; scenariusz P1 prześledzony w kodzie przez architekta (`load()`, `settlePayment`, `readPollPhase`).

### 2747-B1 (logika przepływu opłaty zaległości: ponowny odczyt po płatności, nowy niezmiennik) + B1-K1 — 2026-10-20
- Archetyp: Algorytmika / Logika — przepływ FE z niezmiennikiem płatności (RxJS, sygnały, sprawdzanie), 1 plik kodu + 1 model + 3 spece.
- Stawka: wysoka (obciążenie karty).
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 `xhigh` (B1 i korekta B1-K1 — świeży agent tej samej linii).
- Recenzent (linia / model / native effort): Muse / `muse-wonder-full-1.0-contributor` `max`, `-Access read` (wpis 2747-R1); bramka końcowa Sol `max` — później.
- Dopuszczone alternatywy: brak (plik niezmiennika — twarda bramka; przy CZERWONYM Muse Wonder Full `max`).
- Powód wyboru: plik niezmiennika płatności; speci wymagają znajomości nowej sekwencji żądań — jedna warstwa.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany — ZIELONY (hook, 2026-10-20 ~00:40: 5 h 34–46 %, tydzień 20–22 %).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: wymagane korekty — D1–D5 wdrożone, 9 scenariuszy, mutacje 9 niezmienników; 1×P1 z recenzji (pamięć tylko ostatnio opłaconej faktury) + 1 przypadek brzegowy zgłoszony przez samego wykonawcę (komunikat „kwota się zmieniła” przy wejściu w D3).
- Rundy korekt: 1 z wykonania (P1) — przypadek brzegowy i złagodzenie komentarza to doprecyzowania specyfikacji.
- Czas do akceptacji: ~70 min (B1 24 min + walidacja + recenzja 19 min + B1-K1 9 min + walidacja).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): patrz 2747-R1 (P1 i P3 potwierdzone, 0 odrzuconych). Słuszne uwagi wykonawcy do briefu: lista plików nie mieściła się w `sonarjs/max-lines` (nowy spec w B1-K1); scenariusz 2 korekty nie dowodził luki (zastąpiony testem trzech faktur).
- Defekty po odbiorze: do bramki końcowej.
- Wymagane testy i dowody: `ng test` trzech speców przepływu 120/120; pełne `lint`, `format:check`, `npm test` (450 plików / 4619 testów), `build` — exit 0; mutacje potwierdzone przez wykonawcę, sha pliku przywrócone.

### 2747-B2 (warstwa widoku: komunikat kolejnej faktury, fokus, i18n pl/en, spec komponentu z AXE) — 2026-10-20
- Archetyp: Frontend UI — szablon + efekt fokusu + i18n + spec komponentu (5 plików), bez Figmy.
- Stawka: niska (widok bez niezmiennika w funkcji wysokiej stawki).
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Muse / `muse-wonder-full-1.0-contributor` `max`, `-Access write`.
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (wpis 2747-R2); bramka końcowa Sol `max` — później.
- Dopuszczone alternatywy: Claude `wykonawca` Sonnet 5.5 `high`; Codex `gpt-6.1-sol` `high` (≤ 5 plików; pula na bramkę).
- Powód wyboru: brief w całości tekstem (bez Figmy), własna pętla `ng test`; pierwsza próba Wondera Full jako wykonawcy FE.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Muse nieznany (wrapper, 2026-10-19 23:10 UTC).
- Pewność decyzji: niska (brak lokalnych wyników Wondera Full jako wykonawcy FE).
- Wynik pierwszego podejścia: zaakceptowano — 433 s; spec 41/41 (6 nowych, w tym AXE Light/Dark); pełna walidacja 450 plików / 4625 testów, lint/format/build exit 0.
- Rundy korekt: 0.
- Czas do akceptacji: ~20 min (przebieg + walidacja + recenzja).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): patrz 2747-R2 (2×P3 bez poprawki). Słuszne uwagi wykonawcy do briefu: słownik `ARREARS_PL` w specu (brief go pominął) i limit `sonarjs/max-lines-per-function` pierwszego `describe` — obie obszedł sam w zakresie.
- Defekty po odbiorze: do bramki końcowej.
- Wymagane testy i dowody: diff 5 plików zgodny z briefem; `ng test` speca; pełna walidacja repo.

### 2747-R2 (recenzja fali 2: warstwa widoku komunikatu kolejnej faktury) — 2026-10-20
- Archetyp: Recenzja — szablon, fokus, i18n, spec komponentu (5 plików), tylko odczyt.
- Stawka: niska.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): nie dotyczy (autor B2: Muse Wonder Full `max`).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read`.
- Dopuszczone alternatywy: Codex `gpt-6.1-sol` `high` (pula na bramkę).
- Powód wyboru: niska stawka — preferencja reguły 13 (Sol `high` albo Gemini `high` przed Muse); inna rodzina niż autor.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany (wrapper, 2026-10-19 23:18 UTC).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 347 s; werdykt „poprawny” (0,98); 0×P0/P1, 2×P3.
- Rundy korekt: 0.
- Czas do akceptacji: ~10 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 2×P3 odrzucone jako defekt — ogólny selektor `div[tabindex="-1"]` (kontenery nie współistnieją; przy współistnieniu test błędu poczerwienieje, nie fałszywa zieleń), flaga ustawiana przed `create()` w teście pozycji DOM (test nie bada fokusu). Uwagi do briefu: kolor sukcesu (podważa zatwierdzoną D6 — odrzucone); utrata fokusu po `Loading → Ready` przy zwykłym `reload()` — słuszna, ale sprzed PBI, poza zakresem.
- Defekty po odbiorze: do bramki końcowej.
- Wymagane testy i dowody: raport z logu wrappera; `git status` bez zmian po przebiegu.

### 2747-BR (dowód w przeglądarce 2×2 z podmianą odpowiedzi API — Playwright CLI) — 2026-10-20
- Archetyp: Worker przeglądarkowy — dowód stanu, którego nie da się osiągnąć bez płatności (podmiana `GET …/arrears` i `POST …/arrears/payment`), zrzuty 360×530 / 1280×720 × Light/Dark.
- Stawka: wysoka (obszar płatności; dowodem logiki są testy jednostkowe, przeglądarka dowodzi widoku i braku prawdziwego POST).
- Niepewność: średnia (pierwszy dowód z `route` + `run-code` na nakładce zaległości).
- Wykonawca (linia / model / native effort): Muse / `muse-wonder-full-1.0-contributor` / `max`, `-Access write`, `pwcli`.
- Recenzent (linia / model / native effort): architekt (PNG obejrzane, log BE).
- Dopuszczone alternatywy: Gemini albo Codex z Playwright MCP (`--isolated`) — CLI działa tylko w linii Muse.
- Powód wyboru: `browser-check` nie podmienia odpowiedzi API; CLI ~3,3× taniej niż MCP (reguła 15).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Muse nieznany (wrapper, 2026-10-19 23:25 UTC).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowano — 463 s; S1–S3 PASS, 9 PNG; 3 POST opłaty, wszystkie podmienione (`PAID`); 0 żądań opłaty w logu BE.
- Rundy korekt: 0.
- Czas do akceptacji: ~10 min (przebieg + oględziny).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): brak defektu UI. Słuszne uwagi do briefu: błędny adres Ustawień (`/ustawienia/konto` zamiast `/panel/ustawienia/konto`) — worker odnalazł właściwy w nawigacji; `request <n>` nie pokazuje ciała odpowiedzi (potrzebne `response-body <n>`); FAKTURA_B opisana różnicowo.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: PNG obejrzane przez architekta, `location.href` przed każdym zrzutem, `requests`/`response-body`, grep logu BE.

### 2747-GATE-FE (bramka końcowa FE, runda 1 — cały diff funkcji) — 2026-10-20
- Archetyp: Bramka końcowa high-stakes — przepływ opłaty zaległości (plik niezmiennika + widok + i18n + wersja), tylko odczyt.
- Stawka: wysoka.
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): nie dotyczy (autorzy: `wykonawca-opus` — przepływ; Muse WF `max` — widok; architekt — wersja).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `max`, `-Mode review`.
- Dopuszczone alternatywy: przy limicie Codexa — jednorazowo Muse WF `max` read (decyzja właściciela W3); brak słabszej bramki.
- Powód wyboru: reguła 6 — niezależna rodzina wobec autora plików niezmiennika.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper, 2026-10-19 23:25 UTC).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: 363 s; werdykt „niepoprawny”; 1×P2 potwierdzony.
- Rundy korekt: 1 (K2, `wykonawca-opus`) + runda 2 bramki.
- Czas do akceptacji: ~50 min z K2 i rundą 2 (wpis 2747-GATE-FE-R2).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): P2 potwierdzony — przekazanie do zmiany metody płatności montuje NOWY kontener, `start()` zeruje komunikat i pamięć opłaconych faktur (sprzeczne z pkt 5 rewizji); test `reload()` jako „powrót ze zmiany metody” był fałszywą zielenią. Błędna przesłanka architekta (powrót = `reload()` tej samej instancji) przeszła przez R1 i R2 — wykryła ją dopiero bramka czytająca rodzica spoza listy plików.
- Defekty po odbiorze: brak po K2 (runda 2 bez P0–P2).
- Wymagane testy i dowody: skrypt w pamięci bramki (puste `settled` po montażu); poprawka z testem prawdziwego przekazania w specu rodzica.

### 2747-K2 (korekta po bramce: migawka przepływu zaległości przez przekazanie do zmiany metody płatności) — 2026-10-20
- Archetyp: Implementacja FE high-stakes — plik niezmiennika płatności + kontener + rodzic + 4 speci (przekrojowa poprawka jednego styku), 10 plików.
- Stawka: wysoka.
- Niepewność: średnia (cykl życia nakładek przy przekazaniu; błędna przesłanka architekta wykryta przez bramkę).
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 / `xhigh`.
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `max`, `-Mode review` (bramka runda 2 — cały diff FE).
- Dopuszczone alternatywy: brak dla pliku niezmiennika (CZERWONY → Muse WF `max`, Muse w tym czasie z limitem).
- Powód wyboru: plik niezmiennika (twarda bramka); jedna spójna poprawka kontraktu zamiast dwóch briefów z ryzykiem rozjazdu.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook, ZIELONY 48 %, 2026-10-19 23:35 UTC).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: zaakceptowano — 1009 s, 87 wywołań, 310 tys. tokenów; 353/353 testów w 15 plikach; test rodzica (prawdziwe przekazanie) czerwony przed poprawką (3/3), speci przepływu i kontenera dowiedzione mutacjami (3 rundy).
- Rundy korekt: 0.
- Czas do akceptacji: ~25 min (przebieg + walidacja).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): do rundy 2 bramki. Słuszne uwagi wykonawcy do briefu: nieistniejące `isCurrentGeneration()` (jest `isCurrentSession()`); drugi test z fałszywą etykietą (l. 276); dwuznaczność D6 „fokus w chwili pojawienia się” — architekt dopisał zdanie do pkt 6 rewizji.
- Defekty po odbiorze: do bramki.
- Wymagane testy i dowody: diff 10 plików zgodny z briefem; pełna walidacja repo (wal4).

### 2747-GATE-FE-R2 (bramka końcowa FE, runda 2 — cały diff funkcji po K2) — 2026-10-20
- Archetyp: Bramka końcowa high-stakes — ponowny przebieg po poprawce zmieniającej kształt API (> 5 plików), tylko odczyt.
- Stawka: wysoka.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): nie dotyczy (autor K2: `wykonawca-opus`).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` / `max`, `-Mode review`.
- Dopuszczone alternatywy: Muse WF `max` read (W3) — w tym czasie z limitem (429 do 01:21 UTC).
- Powód wyboru: reguła 6 + Faza 4b pkt 3 (korekta > 5 plików i nowy kształt API → druga runda); bramka zarazem niezależną recenzją delty wobec Opusa.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper, 2026-10-19 23:58 UTC).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: 400 s; brak defektów funkcjonalnych (tsc, `git diff --check`, 6 scenariuszy w pamięci); 1×P3.
- Rundy korekt: 0.
- Czas do akceptacji: ~7 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): P3 odrzucone — helpery najwyższego poziomu w nowych specach („jedna deklaracja na plik”): praktyka repo (326/452 speców, sąsiednie speci zaległości przy HEAD 11–16 funkcji), lint ich nie zgłasza, zasada dotyczy artefaktów produkcyjnych.
- Defekty po odbiorze: brak (do QA).
- Wymagane testy i dowody: wal4 (452 pliki / 4645 testów, lint/format/build exit 0) przed bramką; drzewo bez zmian po przebiegu.

### 2747-DOC-4C (przegląd zgodności dokumentacji z kodem, Faza 4c) — 2026-10-20
- Archetyp: Przegląd zgodności dokumentacji — 1 dokument interfejsu + 2 dokumenty bez zmian, diff FE 19 plików, tylko odczyt.
- Stawka: średnia (dokument źródła prawdy funkcji high-stakes).
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Claude / `wykonawca` — Sonnet 5.5 / `high` (tryb tylko do odczytu z briefu; `git status` po przebiegu bez zmian).
- Recenzent (linia / model / native effort): architekt (triaż macierzy).
- Dopuszczone alternatywy: Muse WF `max` read (plan; 429 do 01:21 UTC); Codex Sol `high` read — odrzucony (funkcja high-stakes, sygnał `nieznany`, > 5 plików); Gemini — autor rewizji.
- Powód wyboru: jedyna dopuszczona linia dostępna od razu; inna rodzina niż autor rewizji (Gemini).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook ŻÓŁTY, 55 %, 2026-10-20 00:05 UTC); Muse zablokowany (wrapper 429, 2026-10-19 23:44 UTC).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowano — 196 s, 23 wywołania, 237 tys. tokenów; 0 × „kod odbiega”; 4 wiersze (3 redakcyjne w granicach D2/D3/D5, 1 napis sprzed PBI → pytanie do właściciela).
- Rundy korekt: 0.
- Czas do akceptacji: ~8 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): potwierdzone 3 luki redakcyjne (architekt dopisał zdania do pkt 2 i 5); 1 do decyzji właściciela (napis stopki w sprawdzaniu); słuszna uwaga o mapie — UI-KONTO-USTAWIENIA zgodny, sprawdzony sam.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: macierz z `plik:linia`; diff Dokumentacji tylko pliku zadania.

### 2747-QAS (przypadki QA Sphere: przegląd 14 istniejących + 3 nowe dla drugiej zaległej faktury — generator, recenzja krzyżowa, K1, K2) — 2026-10-20
- Archetyp: Autor QA Sphere — plik podglądu wg `qasphere-test-generator` (Krok 2b + nowe), recenzja krzyżowa innej rodziny.
- Stawka: średnia (przypadki manualne dla przepływu opłaty zaległości; błędny krok = fałszywy defekt albo niewykonalny test na PRE).
- Niepewność: średnia (długie przygotowanie dwóch faktur zegarem testowym Stripe; wywołanie błędu odczytu narzędziami przeglądarki).
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access write` (generator 525 s, K1 870 s, K2 208 s).
- Recenzent (linia / model / native effort): Claude / `wykonawca` — Sonnet 5.5 `high`, tylko odczyt z briefu (412 s, 55 wywołań; MD5 pliku niezmienione).
- Dopuszczone alternatywy: autor Muse Wonder Full `max` (domyślny w procedurze skilla — 429 limitu okna przy generatorze); recenzent Muse Wonder Full `max` read (procedura: plik Gemini → Muse) — zablokowany; Codex `gpt-6.1-sol` `high` odrzucony (`-Mode review` dotyczy diffu repo, nie pliku podglądu; najmniejsza pula).
- Powód wyboru: procedura skilla dla autora (Gemini write przy limicie Muse); recenzent po ponownej kwalifikacji wg reguły 2 — Muse: limit tygodniowy, inna rodzina niż Gemini i ten sam precedens co 2747-DOC-4C.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Muse zablokowany — 429 limitu okna (reset 01:21 UTC), potem 429 limitu tygodniowego do 2026-10-26T00:00Z (wrapper, 01:39 UTC); Gemini nieznany (przebiegi udane); Claude znany ZIELONY (hook, 01:45 UTC).
- Pewność decyzji: średnio-niska (pierwszy lokalny wynik Sonneta jako recenzenta QA).
- Wynik pierwszego podejścia: 4 nowe (A1–A4) + update 1642, 13 keep, `lint` 0 — ale przygotowanie dwóch faktur odbiegało od seq 1642 (wymyślone „Smart Retries”, „+1 godzina”), kroki niewykonalne (trasa `/panel/settings/account`, stopka panelu, motyw przy otwartej nakładce modalnej), przypadek błędu ponownego odczytu pominięty.
- Rundy korekt: 2 — K1 po recenzji (kroki 1–7 słowo w słowo z 1642, scalenie A2–A4, nowy A5 z krokiem-strażnikiem, 1642 bez zdania o bloku pod maską, jawne pominięcia); K2 po kontroli architekta (nazwy plików i selektorów w krokach testera, opis koloru w ciemnym motywie).
- Czas do akceptacji: ~2 h 30 min (23:45 → 02:15 UTC), w tym ~1 h oczekiwania na reset Muse zakończonego limitem tygodniowym; praca netto ~75 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 3×P1 potwierdzone poleceniami (trasa i przełącznik języka — `app.routes.ts:161`, `logged-topbar.html:34`; motyw za maską modalu — `overlay-panel.html:40`; przygotowanie niezgodne z 1642 i z INT l.79); 4×P2 przyjęte (blok „Abonament” pod maską w 1642, pominięcie błędu odczytu, niepełna kolejność Tab, sprzeczny język w warunku A2); 3×P3 przyjęte, 1×P3 pominięte (wariant A1 z zapisem karty — ta sama ścieżka kodu). Fałszywych P0/P1: 0. Metoda recenzenta dla błędu odczytu („Block request URL”) tylko warunkowo poprawna — sonda architekta w Chrome 155: CDP `setBlockedURLs` (dopasowanie po fragmencie) blokuje też `…/arrears/payment`, `urlPatterns` (URLPattern) tylko odczyt; recenzent sam zgłosił niepewność. Stąd w A5 krok-strażnik `GET …/arrears/payment` → 405 (bez skutków ubocznych, sprawdzone `curl` na PRE).
- Defekty po odbiorze: brak w `qas.py verify` (4 sprawdzone, 0 różnic); nowe seq 1684 (A1), 1685 (A2), 1686 (A5) w folderze 177, zaktualizowany 1642, wycofane 0; wykonanie przez testera jeszcze nie nastąpiło.
- Wymagane testy i dowody: `qas.py lint` 0 po każdej rundzie; porównanie skryptem kroków 1–7 A1/A2 z 1642 i 1–5 A5 z 1633 (identyczne poza kontem); P1 sprawdzone w kodzie; `verify` pełne.
- Uwagi: przesłanka architekta w briefie generatora („nie zgaduj DevTools — pomiń”) prowadziła do pominięcia kryterium PBI; jednorazowa sonda metody przed briefem rozstrzyga taniej. Sonnet `high` jako recenzent QA: 0 fałszywych P1, wszystkie P1 trafne i z dowodem `plik:linia`.

### 2785-DOC-1 (datowana rewizja dokumentu interfejsu — 4 punkty z decyzji zatwierdzonych z góry) — 2026-10-20
- Archetyp: Dokumentacja produktowa — rewizja `zatwierdzonego` dokumentu z kontrolą wpływu (§10, §12), jeden plik.
- Stawka: niska (napisy nakładki opłaty zaległości; zasady płatności i kod bez zmian).
- Niepewność: niska (brzmienia PL/EN podane dosłownie w decyzjach planu).
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access write`.
- Recenzent (linia / model / native effort): architekt (Claude Opus `xhigh`, inna rodzina) — odbiór diffu bajt w bajt i przegląd 4c (reguła 11: jeden dokument).
- Dopuszczone alternatywy: Muse Wonder Full `max` write; `wykonawca` Sonnet 5.5 `high`.
- Powód wyboru: 2747-DOC-1 na tym samym dokumencie — 0 rund, 326 s; przegląd 1: dokumentacja na Gemini `high` 7 briefów / 0,1 rundy.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany (wrapper, ostatni przebieg 2026-10-19 23:18 UTC bez limitu).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowano — 287 s, +10 linii tylko w dokumencie docelowym (dopisana sekcja rewizji), front matter bez zmian, brzmienia bajt w bajt z decyzjami, `zasoby/teczki/` nietknięte.
- Rundy korekt: 0.
- Czas do akceptacji: ~8 min (przebieg + diff + porównanie brzmień).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): brak; sekcja „co błędne w specyfikacji” — 1 uwaga przyjęta: brief wskazywał katalog `procesy\`, w repo jest `procesy-biznesowe\` (błąd ścieżki w briefie architekta; worker sam znalazł właściwy katalog do kontroli wpływu).
- Defekty po odbiorze: brak (przegląd 4c: 4 punkty zgodne, 0 rozbieżności).
- Wymagane testy i dowody: `git diff` i `status --porcelain` repo Dokumentacja (1 plik); brzmienia porównane z decyzjami bajt w bajt (wielokropek U+2026).

### 2785-FE-1 (podmiana dwóch wartości i18n pl/en, 4 literały w specu, komentarz, SemVer patch) — 2026-10-20
- Archetyp: Mechaniczna zmiana FE — wartości i18n i literały speca podane parami stary → nowy tekst, `release_version.py`.
- Stawka: niska (napisy w funkcji płatności, ale bez pliku niezmiennika: przepływ, fazy i BE nietknięte).
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Claude / `mechanik` — Haiku 5.5 `low`.
- Recenzent (linia / model / native effort): brak recenzji fali (Faza 4b — diff czysto mechaniczny); dowód architekta: zgodność bajt w bajt, `lint`, `format:check`, `npm test`, `build`.
- Dopuszczone alternatywy: Gemini `flash-high` write; Muse Wonder Full `max` write.
- Powód wyboru: treść podana dosłownie, zero osądu, 5 plików + manifesty wersji; najtańsza linia przy zielonej puli Claude'a.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany ZIELONY (hook, 2026-10-20 rano).
- Pewność decyzji: średnia (brak wcześniejszych wpisów `mechanik` na specach).
- Wynik pierwszego podejścia: zaakceptowano — `ng test --include` speca 46/46, diff zgodny z briefem bajt w bajt; 11 wywołań, ~1,37 mln tokenów (1,23 mln cache read).
- Rundy korekt: 0.
- Czas do akceptacji: jeden przebieg bez korekt (czas nie mierzony osobno).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): — (bez recenzji); walidacja architekta bez uwag.
- Defekty po odbiorze: brak (przegląd 4c zgodny; przypadki QA Sphere jeszcze niewykonane przez testera).
- Wymagane testy i dowody: `JSON.parse` obu locale; wartości kluczy równe decyzjom (U+2026); `npm run lint`, `format:check`, `npm test` (4645), `build` — exit 0.
- Uwagi: pierwszy lokalny wynik `mechanik` (Haiku 5.5 `low`) na specu — przy parach stary → nowy tekst i zakazie przepisywania JSON wystarczył.

### 2785-QAS (przypadki QA Sphere: przegląd 17 istniejących + 3 nowe dla napisów sprawdzania płatności — generator, recenzja krzyżowa, K1–K3) — 2026-10-20
- Archetyp: Autor QA Sphere — plik podglądu wg `qasphere-test-generator` (Krok 2b + nowe), recenzja krzyżowa innej rodziny.
- Stawka: średnia (przypadki manualne w przepływie opłaty zaległości; błędny krok blokuje płatność albo daje fałszywy defekt).
- Niepewność: średnia (blokada odczytu w DevTools w trakcie okna banku 3-D Secure; konto z zaległością na zegarze testowym Stripe).
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access write` (generator 557 s, K1 737 s, K2 522 s, K3 160 s).
- Recenzent (linia / model / native effort): Claude / `wykonawca` — Sonnet 5.5 `high`, tylko odczyt z briefu (314 s + recenzja delty 63 s, razem 23 wywołania; MD5 pliku niezmienione).
- Dopuszczone alternatywy: autor Muse Wonder Full `max` (domyślny w procedurze skilla) — zablokowany; recenzent Muse read — zablokowany; Codex odrzucony (najmniejsza pula, brak lokalnych wyników recenzji QA).
- Powód wyboru: procedura skilla dla autora (Gemini write przy limicie Muse); recenzent po ponownej kwalifikacji wg reguły 2 — precedens 2747-QAS (0 fałszywych P1).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Muse zablokowany — 429 limitu tygodniowego do 2026-10-26T00:00Z (wrapper, 08:13 UTC, przebieg 20 s); Gemini nieznany (przebiegi udane); Claude znany ZIELONY (hook).
- Pewność decyzji: średnia (drugi lokalny wynik Sonneta jako recenzenta QA).
- Wynik pierwszego podejścia: 3 nowe (A1–A3), 0 aktualizacji, 17 bez zmian, `lint` 0 — ale A2/A3 blokowały odczyt zaległości przed wysłaniem płatności (blokada po fragmencie adresu obejmuje też `…/arrears/payment`, więc płatność nie poszłaby), warunki wstępne na koncie demo bez zaległości, brak zapisu karty 3DS `3184`.
- Rundy korekt: 3 — K1 po recenzji (przygotowanie słowo w słowo z ZEB/1686, zmiana metody płatności na kartę 3DS, blokada dopiero przy otwartym oknie banku); K2 po recenzji delty (2×P3: sprzeczny język w A3, brakujące zdanie o zawieszonych programach w A1); K3 po kontroli architekta (warunek wstępny skopiowany z 1686 wskazywał FE 1.7.0 zamiast 1.7.1).
- Czas do akceptacji: ~45 min (08:13 → ~08:57 UTC), w tym ~39 min pracy workerów.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): pierwsza recenzja — 3×P1 potwierdzone (blokada przed wysłaniem płatności, konto demo bez zaległości, brak zapisu karty 3184), 3×P2 i 1×P3 przyjęte (asercja Escape/tła, statusy HTTP i nazwy z kodu w wynikach oczekiwanych); 1 uwaga odrzucona („ZEB/1686 zawsze przerwany” — pomiar przez CDP, a 1686 ma krok-strażnik). Delta: 0 P0/P1, 2×P3 przyjęte. Fałszywych P0/P1: 0. Znalezisko architekta poza recenzją: wersja FE w warunkach wstępnych (K3).
- Defekty po odbiorze: brak w `qas.py verify` (3 sprawdzone, 0 różnic); nowe seq 1687 (A1), 1688 (A2), 1689 (A3) w folderze 178; zaktualizowane 0, wycofane 0; wykonanie przez testera jeszcze nie nastąpiło.
- Wymagane testy i dowody: `qas.py lint --strict` 0/0 po każdej rundzie; porównanie przed/po K2 i K3 skryptem (zmienione tylko zamierzone pola); `verify` pełne.
- Uwagi: trzy lekcje do briefu generatora — (1) podać seq i kroki przygotowania do skopiowania wprost; (2) podać z góry, że blokada w DevTools działa po fragmencie adresu (lekcja z 2747), więc odczyt blokuje się dopiero po wysłaniu płatności; (3) przy kopiowaniu warunków wstępnych z wcześniejszego zadania sprawdzić linię wersji. Sonnet `high` jako recenzent QA drugi raz bez fałszywych P1.

### 2723-DOC-1 (datowane rewizje czterech dokumentów `zatwierdzony` — rewizja integracji + trzy sprostowania z decyzji zatwierdzonych z góry) — 2026-10-20
- Archetyp: Dokumentacja produktowa — rewizje `zatwierdzonych` dokumentów (§10, §12), cztery pliki w dwóch obszarach (integracje, reguły, interfejs).
- Stawka: średnia (zasady dokumentów księgowych w funkcji płatności; sama dokumentacja, bez kodu).
- Niepewność: niska (punkty rewizji podane w briefie z decyzji właściciela D1–D3 i decyzji architekta).
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access write`.
- Recenzent (linia / model / native effort): Faza 4c — Claude / `wykonawca` Sonnet 5.5 `high`, tylko odczyt (wpis 2723-4C).
- Dopuszczone alternatywy: Claude `wykonawca` Sonnet 5.5 `high` write; Muse Wonder `max` write — zablokowany.
- Powód wyboru: 2747-DOC-1 i 2785-DOC-1 na Gemini `high` — 0 rund; przegląd 1: dokumentacja na Gemini 7 briefów / 0,1 rundy; rozłączny tor z falą BE (inne repo).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany (wrapper, przebiegi 2026-10-20 rano udane); Muse zablokowany do 2026-10-26T00:00Z (429 limitu tygodniowego, wrapper 08:12 UTC).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowano — 517 s, 4 pliki, sekcje rewizji na końcu dokumentów, odnośnik „zrealizowane” w zakresie odroczonym, końce linii każdego pliku zachowane (raport mylnie podał LF), 0 odchyleń, `zasoby/teczki/` nietknięte.
- Rundy korekt: 0 z wykonania; 1 zdanie dopisane przez architekta po 4c (reguła 11).
- Czas do akceptacji: ~15 min do odbioru diffu; zamknięcie po 4c tego samego dnia.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 4c — 1 rozbieżność potwierdzona (rewizja RB-ZWROT pkt 1 bez wyjątku konta bez danych rozliczeniowych — niedokładność wobec INT-FAKTUROWNIA pkt 5), 0 odrzuconych.
- Defekty po odbiorze: brak poza poprawionym zdaniem.
- Wymagane testy i dowody: `git diff -- Zebrani` repo Dokumentacja (4 pliki, same dopisania + 1 odnośnik), porównanie punktów z decyzjami planu, macierz 4c.

### 2723-BE-1 (+K1) (zlecenie faktury VAT w transakcji zapisu płatności odnowienia — SQL, repozytorium, rejestrator, alarm pisarza) — 2026-10-20
- Archetyp: Backend — plik niezmiennika płatności („dokładnie raz” dokumentu księgowego w transakcji lustra), SQL Dapper + warstwa aplikacji.
- Stawka: wysoka / high-stakes (płatności Stripe, dokumenty VAT, idempotencja przy ponowionych zdarzeniach).
- Niepewność: średnia (wzorzec dopłaty istniał; nowość — sprzężenie z cyklem uzgadniającym i alarm po zatwierdzeniu).
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 `xhigh` (BE-1 i świeży agent K1).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `xhigh`, `-Mode review` (fala 1); bramka końcowa — wpis 2723-G-BE.
- Dopuszczone alternatywy: brak dla pliku niezmiennika (CZERWONY → Muse Wonder Full `max`, tego dnia zablokowany → czekanie). Recenzent: Gemini `flash-high` read (słabszy przy high-stakes), Muse Wonder Full `max` — zablokowany.
- Powód wyboru: twarda bramka high-stakes (reguła 2/6); recenzja fali na Solu `xhigh` przy małym diffie (~6 plików), żeby oszczędzić pulę Codexa przed bramką `max`.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany ZIELONY (hook, ~10:45 UTC: okno 21 %, tydzień 27 %); Codex nieznany (wrapper bez zapasu, bez komunikatów limitu); Muse zablokowany do 2026-10-26T00:00Z.
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: zaakceptowano z poprawką — 879 s, 84 wywołania, ~290 tys. kontekstu; build Release 0/0, testy filtrowane 3136/3138 (2 czerwone oczekiwane: testy zwrotu sprzed zmiany → fala testów). Wykonawca sam zgłosił, że alarm „płatność bez zlecenia” szedł wewnątrz transakcji — przyjęte przed recenzją.
- Rundy korekt: 1 (K1 z własnego zgłoszenia wykonawcy: alarm po zatwierdzeniu, krotka z `string[]` zamiast nowego typu — limit sprzężenia klas S1200 = 30; 754 s, 59 wywołań, ~250 tys.).
- Czas do akceptacji: ~1 h (dwa przebiegi + walidacje + recenzja 171 s).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): recenzja fali Sol `xhigh` — 0 znalezisk (przeczytał diff, cykl wystawiania, korekty); bramka Sol `max` — 0 defektów produkcji.
- Defekty po odbiorze: brak (E2E na zegarach Stripe: wszystkie scenariusze zgodne).
- Wymagane testy i dowody: build Release 0/0; pełny `dotnet test` z SQL Server 7874/7874, 0 pominiętych; mutacje architekta M1 (bez wywołania zlecenia → 43 czerwone) i M2 (VAT = netto → 4 czerwone); E2E architekta na zegarach testowych Stripe z prawdziwymi webhookami — odnowienie (1 zlecenie, ponowione zdarzenia bez duplikatu), zwrot odnowienia przy przerwanej rezygnacji (zlecenie + korekta do zera), nieudana płatność (0 zleceń), ponowienie skuteczne (1 zlecenie), dwie płatności „Opłać teraz” (2 zlecenia), 0 duplikatów NORMAL.

### 2723-T-1 (+T-1b, K1, K2) (testy SQL, jednostkowe rejestratora i pisarza lustra, korekty zwrotu, atrapa repozytorium) — 2026-10-20
- Archetyp: Testy BE — xunit `[SqlServerFact]` na prawdziwej bazie + Moq (harness lustra), scenariusze nazwane przez architekta.
- Stawka: wysoka (testy niezmiennika płatności; fałszywa zieleń przepuszcza duplikat faktury albo alarm przed zatwierdzeniem).
- Niepewność: średnia (ścisłe atrapy harnessu, kolejność zdarzeń transakcji, baza SQL Server).
- Wykonawca (linia / model / native effort): Claude / `tester` — Haiku 5.5 `xhigh` (T-1, kontynuacja T-1b, K1, K2 — każdy świeży agent).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (wpis 2723-R2); bramka Sol `max` (wpis 2723-G-BE).
- Dopuszczone alternatywy: `wykonawca-opus` (testy jak 2722); recenzent Codex Sol `high`.
- Powód wyboru: linia testów po próbie 2026-10-13 (Haiku `xhigh` 0,60× kosztu Sonneta, bez dodatkowych rund); scenariusze i mutacje nazwane w briefie.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany ZIELONY (hook, cały dzień 4–30 % tygodnia).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: przekazanie przy ~306 tys. (strażnik kontekstu) — T-1 1066 s, 72 wywołania: SQL A (10 przypadków), B1, D (+ pomocnik korekt), harness/seeder; kontynuacja T-1b 964 s, 49 wywołań, ~342 tys.: 13 przypadków pisarza (C1–C7) + mutacje. Mutacja M2 (bez `NOT EXISTS`) zielona — obrona w głębi indeksu, przyjęte.
- Rundy korekt: 2 — K1 po recenzji fali (327 s, 28 wywołań, ~220 tys.: kwoty faktury w pomocniku korekt, rejestracja zlecenia tylko przy wyniku, kolejność zdarzeń C6); K2 po bramce (564 s, 52 wywołania, ~260 tys.: alarm 0 w chwili `Commit()`, przypadek rzucającego `Commit()`, test atrapy repozytorium dla 2601/2627 `UQ_Invoices_PaymentId`).
- Czas do akceptacji: ~4 h zegarowo (z recenzją, bramką i E2E pomiędzy), ~49 min pracy agentów.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R2 — 2×P2 + 1×P3 potwierdzone, 1 uwaga odrzucona; bramka — 2×P2 potwierdzone (P2-2 przyjęte w węższej formie: prawdziwe 2601 niewymuszalne, bo filtr indeksu = predykat `NOT EXISTS`).
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: pełny `dotnet test` z SQL 7868 → 7874, 0 pominiętych; `dotnet format --verify-no-changes` na plikach testów; mutacje wykonawcy (C1/C2/C4/C5, M1 alarm przed `Commit()` → 2 czerwone, M-a bez `catch` → 2, M-b filtr bez nazwy indeksu → 1) i własne architekta (M1/M2 po K1, M-b po K2); skrót plików produkcyjnych niezmieniony po każdej rundzie.
- Uwagi: przywrócenie mutanta `cp -p` zostawiło stary mtime → build przyrostowy trzymał mutanta (4 fałszywe czerwone) — brief K2 wymagał już aktualizacji czasu modyfikacji. Brief K2 podał `.sln` zamiast `.slnx` i mutację „na końcu `WritePlanAsync`” (metoda z wieloma `return`) — wykonawca poprawił sam.

### 2723-R2 (recenzja fali testów) — 2026-10-20
- Archetyp: Recenzja testów BE — tylko odczyt, inna rodzina niż autor (Haiku).
- Stawka: średnia (testy niezmiennika; bramka `max` po niej).
- Niepewność: niska.
- Wykonawca (linia / model / native effort): — (recenzja).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read`.
- Dopuszczone alternatywy: Codex Sol `high` `-Mode review` (pula Codexa przed bramką); Muse — zablokowany.
- Powód wyboru: średnia stawka, inna rodzina niż Claude, oszczędność puli Codexa przed bramką `max` (reguła 7).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany (wrapper, przebiegi udane); Muse zablokowany do 2026-10-26T00:00Z.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 722 s; 0 P0/P1, werdykt poprawny 0,95; wynik w strumieniowym JSON (złożony skryptem z `text_delta`).
- Rundy korekt: 0 (recenzja).
- Czas do akceptacji: ~20 min z triażem.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 2×P2 + 1×P3 potwierdzone (kwoty faktury odnowienia w pomocniku korekt; atrapa rejestrująca zlecenie bez warunku wyniku; kolejność zdarzeń C6); 1 uwaga odrzucona (test API zwrotu bez faktury — pokrywa go istniejący przypadek „bez NORMAL nic nie wstawia”). Fałszywych P0/P1: 0.
- Defekty po odbiorze: bramka znalazła jeszcze 2×P2 w testach (alarm względem `Commit()`, `catch` naruszenia indeksu) — R2 ich nie zgłosił.
- Wymagane testy i dowody: triaż architekta względem kodu; czerwień nowych asercji K1 potwierdzona mutacją M2.

### 2723-G-BE (bramka końcowa BE, cały diff funkcji) — 2026-10-20
- Archetyp: Bramka końcowa high-stakes — recenzja całego diffu BE (produkcja + testy), tylko odczyt.
- Stawka: wysoka / high-stakes.
- Niepewność: niska (po dwóch recenzjach fal i E2E).
- Wykonawca (linia / model / native effort): — (bramka).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `max`, `-Mode review`, jeden przebieg na całe repo BE.
- Dopuszczone alternatywy: brak (reguła 6; limit → czekanie).
- Powód wyboru: reguła 6 — niezależna rodzina wobec autora plików niezmiennika (`wykonawca-opus`).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper, 2026-10-20 12:50 UTC; wcześniejszy przebieg Sola `xhigh` tego dnia bez limitu).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: 388 s; 0 defektów produkcji, 2×P2 w testach; bez uwag do briefu; pewności liczbowej nie podał (format `review`).
- Rundy korekt: 1 (T-1-K2, tylko testy).
- Czas do akceptacji: ~45 min (bramka + triaż + K2 + walidacja).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 2×P2 potwierdzone — alarm sprawdzany osobno od kolejności `Commit()` (przeniesienie przed zatwierdzenie niezauważone); `catch` 2601/2627 bez testu. Odrzuconych 0. Fałszywych P0/P1: 0.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: po K2 — build Release 0/0, `dotnet test` z SQL 7874/7874, mutacje M1/M-a/M-b czerwone, skrót plików produkcyjnych niezmieniony (`787fa8d1…`).
- Uwagi: bramka uruchomiona równolegle z końcówką E2E i przeglądem 4c (wszystko tylko do odczytu) — skrócenie czasu bez ryzyka dla puli, bo E2E nie zmieniało kodu.

### 2723-4C (przegląd zgodności dokumentacji z kodem) — 2026-10-20
- Archetyp: Przegląd zgodności dokumentacja ↔ kod, obie strony, tylko odczyt.
- Stawka: średnia.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): — (przegląd).
- Recenzent (linia / model / native effort): Claude / `wykonawca` — Sonnet 5.5 `high`, tylko odczyt.
- Dopuszczone alternatywy: architekt sam (reguła 11); Codex (pula przed bramką); Muse — zablokowany.
- Powód wyboru: inna rodzina niż autor rewizji (Gemini); precedens 2747/2785-4C.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany ZIELONY (hook, ~12:50 UTC: okno 6 %, tydzień 29 %).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 304 s, 39 wywołań, ~230 tys.; macierz: 1 rozbieżność, zgodne INT-FAKT 9/9 + 5/5, INT-PC 1/1, UI-ZMIANA 2/2, RB-ZARZ 3/3, RB-NIEUD 1/1, UI-UST 3/3; przeszukanie starych zdań — 4 miejsca, wszystkie prostowane rewizjami.
- Rundy korekt: 0 (rozbieżność poprawiona zdaniem przez architekta).
- Czas do akceptacji: ~10 min z triażem.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1 potwierdzona (rewizja RB-ZWROT bez wyjątku konta bez profilu); uwagi bez zmian: fałszywy alarm przy 2601 nieosiągalny, pulpit administratora liczy tylko `wyczerpane ponowienia` (zamierzone), brak odnośników przy dawnych zdaniach (spójność).
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: każdy wiersz z cytatem dokumentu i `plik:linia`; poprawka sprawdzona w kodzie (`RefundGuaranteeSteps.cs:78-86`).
- Uwagi: brief podał nieistniejącą ścieżkę `Dokumentacja\AGENTS.md` (właściwa `Dokumentacja\Zebrani\AGENTS.md` → `INSTRUKCJA-DLA-AI.md`) — recenzent znalazł sam; do poprawy w szablonie briefu 4c.

### 2723-QAS (przypadki QA Sphere: przegląd 77 istniejących + 9 nowych dla faktur za odnowienia i spłaty zaległości — generator, recenzja krzyżowa, K1, K2) — 2026-10-20
- Archetyp: Autor QA Sphere — plik podglądu wg `qasphere-test-generator` (Krok 2b + nowe), recenzja krzyżowa innej rodziny.
- Stawka: wysoka (funkcja high-stakes — dokumenty księgowe za płatności; przypadki manualne na zegarze testowym Stripe ze skryptami w bazie PRE).
- Niepewność: średnia (przygotowanie z 1633/1642 na zegarze testowym, odbiór e-maila od Fakturowni, czas symulowany w dacie sprzedaży, zakres zwrotu przy rezygnacji).
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access write` (generator 797 s, K1 1209 s, K2 360 s).
- Recenzent (linia / model / native effort): Claude / `wykonawca` — Sonnet 5.5 `high`, tylko odczyt z briefu (591 s, 56 wywołań, ~340 tys.; MD5 pliku niezmienione).
- Dopuszczone alternatywy: autor Muse Wonder `max` (procedura skilla w funkcji high-stakes) — zablokowany; recenzent Muse read — zablokowany; Codex odrzucony (najmniejsza pula, brak lokalnych wyników recenzji QA).
- Powód wyboru: procedura skilla dla autora (Gemini write przy limicie Muse); recenzent po ponownej kwalifikacji wg reguły 2 — precedens 2747-QAS i 2785-QAS (0 fałszywych P1).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Muse zablokowany do 2026-10-26T00:00Z (429 limitu tygodniowego, wrapper 08:12 UTC); Gemini nieznany (przebiegi udane); Claude znany ZIELONY (hook, ~13:50 UTC: okno 14 %, tydzień 30 %).
- Pewność decyzji: średnia (trzeci lokalny wynik Sonneta jako recenzenta QA).
- Wynik pierwszego podejścia: 9 nowych (A1–A9), 0 aktualizacji, 77 bez zmian, `lint --strict` 0 — ale konto na `@example.test` w przypadkach sprawdzających e-mail od Fakturowni, nieprawidłowy NIP w A9 (suma kontrolna), A7 z jedną korektą zamiast dwóch i kwotą zwrotu obejmującą odnowienie, data sprzedaży jako dzień kliknięcia (na zegarze to czas symulowany), poświadczenia panelu Fakturowni w A9.
- Rundy korekt: 2 — K1 po recenzji (9 decyzji: skrzynka z dopiskiem `+` wg 1645 i `<adres konta>` w 13 skryptach, NIP i dane firmy z 1646, bez panelu Fakturowni, data sprzedaży z panelu Stripe, A7 — dwie korekty i dwa zwroty, A6 bez przyczyny technicznej, A4 z odczytami R z 1642, dwa wyjaśnienia z 1633, kolumny Historii faktur, pozycja `skipped`); K2 po kontroli architekta (4 poprawki tekstowe, w tym błąd briefu K1 zgłoszony przez autora).
- Czas do akceptacji: ~70 min (13:22 → ~14:33 UTC akceptacja właściciela), w tym ~39 min pracy workerów i ~10 min recenzji.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 5×P1 potwierdzone (skrzynka — także znalezisko architekta; NIP — przeliczony; dwie korekty w A7; data sprzedaży na zegarze — pewność średnia, bez pomiaru na PRE; kwota zwrotu w A7), 4×P2 przyjęte (przyczyna braku duplikatu w A6, panel Fakturowni w A9, zabezpieczenia z 1642 w A4, odstępstwa od kopiowania), P3 częściowo (kolumny, SQL w A5 zostaje). 77 werdyktów `keep` potwierdzone. Fałszywych P0/P1: 0. Recenzent obniżył P0 architekta (hasło panelu w A9) — poświadczenia panelu dopuszcza INT-FAKTUROWNIA rew. 2026-10-19 i przypadek 1651; panel w A9 był po prostu zbędny.
- Defekty po odbiorze: brak w `qas.py verify` (9 sprawdzonych, 0 różnic); nowe seq 1690–1698 w folderze 179; zaktualizowane 0, wycofane 0; wykonanie przez testera jeszcze nie nastąpiło. Niezgłoszone odstępstwo autora w K1: A9 `medium` → `high` (przyjęte — odpowiednik 1646 jest `high`).
- Wymagane testy i dowody: `qas.py lint --strict` 0/0 po każdej rundzie; kontrola architekta skryptem po K1 (0 `example.test`/panelu/poświadczeń, placeholder w każdym skrypcie, skrypty A4 = 1642, dane A9 = 1646, reguła 1645 dosłownie); porównanie pól v1→v2 i v2→v3 (zmienione tylko zamierzone pola poza priorytetem A9); `push --limit 1` + `verify --only`, potem pełne `verify`.
- Uwagi: dwa błędy briefu generatora — (1) „kopiuj słowo w słowo z 1633” i „sprawdzenie e-maila jak 1644–1650” to sprzeczne polecenia (1633 ma `@example.test`, 1645 wymaga odbieranej skrzynki) — brief musi z góry podać, który wzorzec wygrywa dla adresu; (2) brief wspomniał panel Fakturowni jako źródło do kopiowania — przy funkcjach z konwencją „panelu nie otwierasz” podać ją wprost. Błąd briefu K1: wyjaśnienie „Opłać teraz” kazane wszędzie, choć tylko A2/A4 mają tę akcję. Sonnet `high` jako recenzent QA trzeci raz bez fałszywych P1, tym razem także poprawił architekta.

### 2751-B1 (skrypt danych demo: odległy termin zawieszenia i cofnięcie zamknięcia przez cykl, wiersz README, SemVer) — 2026-10-20
- Archetyp: Backend — skrypt danych demo T-SQL (DbUp, zakres 950000+) + wiersz dokumentacji repo kodu.
- Stawka: niska (dane demo, nigdy produkcja; dwa nazwane rekordy; kod cykli nietknięty).
- Niepewność: niska (decyzje w całości w briefie; znane pułapki: zagnieżdżone `/*` w nagłówku, `QUOTED_IDENTIFIER` przy indeksie filtrowanym).
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` / `medium`, `-Access write` (73 s).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (wpis 2751-R1).
- Dopuszczone alternatywy: Gemini `gemini-3.8-flash-high` write; `wykonawca` (Sonnet 5.5 `high`). Muse odrzucony (zablokowany).
- Powód wyboru: ≤ 5 plików, w pełni rozpisane decyzje, potrzebna precyzja T-SQL — `medium` bez wyższego effortu nieuzasadnionego briefem.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper, przebiegi 11:26 i 12:50 UTC bez limitu); Muse zablokowany do 2026-10-26T00:00Z (429 tygodniowy, 08:12 UTC); Claude znany ZIELONY (hook).
- Pewność decyzji: średnia (brak lokalnych wyników Codexa na seedach demo).
- Wynik pierwszego podejścia: zaakceptowano — skrypt, nagłówek i wiersz README zgodne z briefem; jedyna niewykonana część to zapis SemVer: piaskownica Codexa zablokowała `python.exe` (alias `WindowsApps`), architekt wykonał `release_version.py --write` sam (reguła 11).
- Rundy korekt: 0.
- Czas do akceptacji: ~12 min (14:56 → ~15:09 UTC), w tym walidacja na bazie i pełne testy BE.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 (R1 bez znalezisk).
- Defekty po odbiorze: brak (do weryfikacji na PRE po wdrożeniu).
- Wymagane testy i dowody: przebieg na bazie lokalnej 2 → 0 wierszy (gałąź „zamknięty”, idempotencja); gałąź „zawieszony” w transakcji wycofanej (2 wiersze, wartości docelowe, `@@TRANCOUNT` 0); suma kontrolna pozostałych 45 wierszy `Programs` bez zmian; start BE — DbUp wpisał skrypt do `SchemaVersions`, cykle ostrzeżenia i zamknięcia: 0 grup / 0 kont, stan po cyklach bez zmian; `dotnet build -c Release` 0/0; `dotnet test` z SQL 7874/0/0.
- Uwagi: w briefie Codexa z zapisem wersji podawaj interpreter spoza `WindowsApps` albo przenieś zapis SemVer do architekta — piaskownica `workspace-write` nie uruchamia aliasu `python.exe`. Brief błędnie wymagał końców linii LF (kopia robocza ma CRLF przy `core.autocrlf=true`) — wykonawca słusznie zignorował.

### 2751-R1 (recenzja fali 1 BE — skrypt danych demo) — 2026-10-20
- Archetyp: Recenzja — skrypt danych T-SQL i interakcja z cyklami tła.
- Stawka: niska.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): — (recenzja diffu 2751-B1, autor Codex).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read`, bez powłoki, diff wklejony (380 s, 94 kroki).
- Dopuszczone alternatywy: `wykonawca` (Sonnet 5.5 `high`) tylko do odczytu; Sol odpada (rodzina autora); Muse zablokowany.
- Powód wyboru: inna rodzina niż autor; niska stawka → preferencja Gemini `high` / Sol `high` (reguła 13).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany (przebiegi 2026-10-20 udane; odczyt `/quota` nieudany — polecenie potraktowane jak prompt).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowano — werdykt „poprawny”, pewność 1,0; sprawdził pierwszeństwo operatorów, logikę trójwartościową, więzy CHECK i wyzwalacze `Programs`, indeksy filtrowane (w tym `IX_Programs_DataRetentionUntil`), oba cykle i uzgadnianie subskrypcji.
- Rundy korekt: 0.
- Czas do akceptacji: ~8 min (15:01 → ~15:09 UTC).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 / 0; fałszywych P0/P1: 0.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: `git status` po przebiegu — drzewo bez zmian recenzenta; wyrywkowo sprawdzone twierdzenie o indeksie (`Script000000:1170`).
- Uwagi: gałąź zaległości cyklu zamknięcia (`UNPAID` z minionym `DunningStartedAt`, niezależna od terminu programu) recenzent opisał tylko pośrednio — architekt sprawdził ją sam zapytaniem o subskrypcje kont demo.

### 2781-BE-1 (odmowa z powodu planu konta Fakturowni: rozpoznanie w interpreterze, zatrzymanie bez liczenia próby przy wystawianiu i wysyłce, SemVer) — 2026-10-20
- Archetyp: Backend — pliki niezmiennika dokumentów VAT (klasyfikacja odpowiedzi Fakturowni, liczenie prób, dzierżawa), interpreter + cykl aplikacji; SQL i schemat bez zmian.
- Stawka: wysoka / high-stakes (płatności → dokumenty VAT, „dokładnie raz”, limit prób).
- Niepewność: niska–średnia (wzorzec 401/403 istniał; nowość — rozpoznanie treści JSON odporne na ucieczki `\uXXXX`, NFD i niepoprawny UTF-16).
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 `xhigh`.
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `xhigh`, `-Mode review` (wpis 2781-R1); bramka końcowa — wpis 2781-G-BE.
- Dopuszczone alternatywy: brak dla pliku niezmiennika (CZERWONY → Muse Wonder Full `max`, tego dnia zablokowany → czekanie).
- Powód wyboru: twarda bramka high-stakes (reguły 2/6); precedens 2723-BE-1.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany ZIELONY (hook, ~17:35 UTC: okno 0–8 %, tydzień 32 %); Muse zablokowany do 2026-10-26T00:00Z (429 limitu tygodniowego, wrapper 08:12 UTC).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: zaakceptowano bez poprawek — 632 s, 56 wywołań, ~210 tys. kontekstu; zachowanie `JsonDocument` na samotnym surogacie sprawdzone programem (`dotnet run` pliku `.cs`: surowy → `ArgumentException` z `Parse`, ucieczka `\ud800` → `InvalidOperationException` z `GetString`); build 0/0, testy filtrowane zielone; SemVer 1.9.1 → 1.9.2 zapisany skryptem.
- Rundy korekt: 0.
- Czas do akceptacji: ~35 min (przebieg + walidacja + R1).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R1 — 0; bramka — 0 (sprawdziła też tryb globalizacji obrazu `aspnet:10.0` pod `Normalize`).
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: build Release 0/0; pełny `dotnet test` z SQL Server 7874/7874 przed falą testów, 0 pominiętych; `dotnet format --verify-no-changes --include <zmienione pliki>` exit 0; mutacje M1–M6 po fali testów czerwone.
- Uwagi: `dotnet format --verify-no-changes` na całym rozwiązaniu kończy się exit 2 z ~5110 zastanymi błędami ENDOFLINE/CHARSET/FINALNEWLINE w plikach spoza zmiany — brief BE i walidacja architekta używają `--include` na plikach zadania.

### 2781-DOC-1 (datowana rewizja INT-FAKTUROWNIA — nowa sekcja 3 punktów + 2 zdania odsyłające, decyzja zatwierdzona z góry) — 2026-10-20
- Archetyp: Dokumentacja produktowa — rewizja `zatwierdzonego` dokumentu integracji (§10, §12), 1 plik.
- Stawka: średnia (zasady dokumentów księgowych; sama dokumentacja).
- Niepewność: niska (punkty rewizji z opisu PBI i decyzji D1 właściciela).
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access write`.
- Recenzent (linia / model / native effort): Faza 4c — architekt (Claude, reguła 11: 1 dokument, ~5 plików kodu z twierdzeniami; wpis 2781-4C).
- Dopuszczone alternatywy: Claude `wykonawca` Sonnet 5.5 `high` write; Muse — zablokowany.
- Powód wyboru: 2723/2747/2785-DOC-1 na Gemini `high` — 0 rund; rozłączny tor z falą BE (inne repo).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany (wrapper, 17:41 UTC; przebiegi tego dnia udane); Muse zablokowany do 2026-10-26T00:00Z.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowano — 568 s; 1 plik, nowa sekcja + 2 zdania w rew. 2026-10-12 pkt 1 i 4, LF zachowane, kotwice poprawne; uwagi workera (kruchość frazy, brak sygnału w panelu → #1727, pominięcie wysyłki jak przy 401, przywracanie ręczne) = świadome decyzje PBI.
- Rundy korekt: 0.
- Czas do akceptacji: ~12 min do odbioru diffu.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 4c — 0 rozbieżności.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: `git diff -- Zebrani` repo Dokumentacja (1 plik), kontrola kotwic i końców linii, macierz 4c.

### 2781-R1 (recenzja fali 1 BE — produkcja odmowy planu) — 2026-10-20
- Archetyp: Recenzja BE high-stakes — produkcja, tylko odczyt, inna rodzina niż autor (Opus).
- Stawka: wysoka.
- Niepewność: niska (mały diff, 7 plików).
- Wykonawca (linia / model / native effort): — (recenzja).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `xhigh`, `-Mode review`, `-BriefFile`.
- Dopuszczone alternatywy: Gemini `flash-high` read (słabszy przy high-stakes); Muse Wonder Full `max` — zablokowany.
- Powód wyboru: precedens 2723-BE-1 (Sol `xhigh` na małym diffie, oszczędność puli Codexa przed bramką `max`).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper, 17:53 UTC, bez komunikatów limitu).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 137 s; 0 znalezisk, bez uwag do briefu.
- Rundy korekt: 0 (recenzja).
- Czas do akceptacji: ~5 min z triażem.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0; fałszywych P0/P1: 0.
- Defekty po odbiorze: brak (R2 i bramka bez defektów produkcji).
- Wymagane testy i dowody: triaż architekta; mutacje M1–M6 po fali testów.

### 2781-T-1 (+K1, K2) (testy interpretera i cyklu na prawdziwej bazie — odmowa planu przy wystawianiu i wysyłce, 401 przy wysyłce) — 2026-10-20
- Archetyp: Testy BE — teorie xunit interpretera + `[SqlServerFact]` cyklu, scenariusze nazwane przez architekta.
- Stawka: wysoka (fałszywa zieleń przepuszcza zużycie prób albo wyjątek w cyklu).
- Niepewność: średnia (dane testowe z ucieczkami JSON i niepoprawnym UTF-16).
- Wykonawca (linia / model / native effort): Claude / `tester` — Haiku 5.5 `xhigh` (T-1, K1, K2 — każdy świeży agent).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (wpis 2781-R2); bramka Sol `max` (wpis 2781-G-BE).
- Dopuszczone alternatywy: `wykonawca-opus`; Codex Sol `high` (pula przed bramką).
- Powód wyboru: linia testów po próbie 2026-10-13; precedens 2723-T-1, 2715-T1a/b.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany ZIELONY (hook, ~18:00 UTC: okno 8–12 %, tydzień 33 %).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowano po 2 korektach — T-1 602 s, 37 wywołań, ~287 tys.; walidacja architekta: 1 czerwony (surowy samotny surogat w `MemberData` — xunit serializuje dane i zamienia go na U+FFFD, więc przypadek nie testował niepoprawnego UTF-16) i 2 przypadki „z ucieczkami” bajtowo identyczne z przypadkiem dosłownym (kompilator C# rozwinął `\uXXXX` w zwykłym literale — pozorne pokrycie, wykryte inspekcją bajtów; raport wykonawcy twierdził pokrycie).
- Rundy korekt: 2 — K1 po walidacji (370 s, 16 wywołań, ~201 tys.: surogat w dwóch `[Fact]` budujących treść w czasie wykonania, ucieczki jako `\\uXXXX`, dowód bajtowy w raporcie); K2 po R2 (274 s, 34 wywołania, ~206 tys.: 3×P3 — komentarz XML, 408 w macierzy statusów spoza 422, licznik prób w C1/C3 startujący od 2 zamiast 0).
- Czas do akceptacji: ~1 h 10 min zegarowo z R2.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R2 — 3×P3 potwierdzone, 0 odrzuconych; bramka — 0.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: pełny `dotnet test` z SQL 7874 → 7932 (K1) → 7934 (K2), 0 pominiętych; `dotnet format --include` na plikach testów; mutacje architekta M1–M4 (bez rozpoznania; odmowa do `default` przy wystawianiu i wysyłce; bez `Normalize`) czerwone po K1, M5/M6 (zerowanie `RetryCount`/`EmailRetryCount` przy zwolnieniu dzierżawy) czerwone po K2; pliki produkcji przywrócone bajt w bajt (SHA-256); CRLF zachowane.
- Uwagi (do szablonu briefu testów): (1) ucieczka `\uXXXX` w danych testowych C# wymaga `\\u` albo literału surowego i dowodu bajtowego w raporcie — zwykły literał rozwija ją i daje duplikat przypadku; (2) wartości, których xunit nie serializuje wiernie (samotne surogaty), idą do `[Fact]` budującego dane w czasie wykonania, nie do `MemberData`/`InlineData`; (3) test „licznik bez zmian” zaczyna od licznika > 0, inaczej mutacja zerująca licznik przechodzi.

### 2781-R2 (recenzja fali testów) — 2026-10-20
- Archetyp: Recenzja testów BE — tylko odczyt, inna rodzina niż autor (Haiku); diff testów dostarczony plikiem w `_robocze` (Gemini read bez powłoki).
- Stawka: średnia (bramka `max` po niej).
- Niepewność: niska.
- Wykonawca (linia / model / native effort): — (recenzja).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read`.
- Dopuszczone alternatywy: Codex Sol `high` `-Mode review` (pula Codexa przed bramką); Muse — zablokowany.
- Powód wyboru: precedens 2723-R2 (0 fałszywych P0/P1); inna rodzina niż Claude; oszczędność puli Codexa przed bramką `max` (reguła 7).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany (wrapper, 18:22 UTC, przebiegi udane); Muse zablokowany do 2026-10-26T00:00Z.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 603 s; 0 P0/P1, 3×P3, werdykt poprawny 0,98; wynik w strumieniowym JSON (złożony z `text_delta`).
- Rundy korekt: 0 (recenzja).
- Czas do akceptacji: ~15 min z triażem.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 3×P3 potwierdzone (komentarz XML kolekcji danych niezgodny z treścią; brak 408 w macierzy fraz spoza 422; licznik prób w testach cyklu startujący od 0); 0 odrzuconych; fałszywych P0/P1: 0.
- Defekty po odbiorze: brak (bramka 0).
- Wymagane testy i dowody: triaż architekta względem kodu; trzecie znalezisko potwierdzone mutacjami M5/M6 (zielone przed K2, czerwone po).
- Uwagi: trzecie znalezisko to w praktyce fałszywa zieleń (P2) — recenzent zaniżył priorytet, ale opisał scenariusz poprawnie.

### 2781-G-BE (bramka końcowa BE, cały diff funkcji) — 2026-10-20
- Archetyp: Bramka końcowa high-stakes — recenzja całego diffu BE (produkcja + testy + wersja), tylko odczyt.
- Stawka: wysoka / high-stakes.
- Niepewność: niska (po dwóch recenzjach fal i mutacjach).
- Wykonawca (linia / model / native effort): — (bramka).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `max`, `-Mode review`, `-BriefFile`, jeden przebieg na całe repo BE.
- Dopuszczone alternatywy: brak (reguła 6; limit → czekanie na reset).
- Powód wyboru: reguła 6 — niezależna rodzina wobec autora plików niezmiennika (`wykonawca-opus`).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper, 18:43 UTC; R1 tego dnia bez limitu).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: 184 s; 0 defektów, bez uwag do briefu.
- Rundy korekt: 0.
- Czas do akceptacji: ~5 min z triażem.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0; fałszywych P0/P1: 0.
- Defekty po odbiorze: brak (PRE: BE 1.9.2 na `d8bb18f`).
- Wymagane testy i dowody: dowody architekta przekazane w briefie (build 0/0, 7934/7934, M1–M6); bramka czytała też klienta API, budowę żądania i `Dockerfile`.

### 2781-4C (przegląd zgodności dokumentacji z kodem) — 2026-10-20
- Archetyp: Przegląd zgodności dokumentacja ↔ kod, obie strony, tylko odczyt.
- Stawka: średnia.
- Niepewność: niska (1 rewizja, ~5 plików kodu z twierdzeniami).
- Wykonawca (linia / model / native effort): — (przegląd).
- Recenzent (linia / model / native effort): architekt — Claude Opus 5.5 `xhigh` (reguła 11).
- Dopuszczone alternatywy: `wykonawca` Sonnet 5.5 `high` read (precedens 2723-4C); Codex (pula przed bramką); Muse — zablokowany.
- Powód wyboru: mały zakres — brief kosztowałby więcej niż macierz; inna rodzina niż autor rewizji (Gemini).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany ZIELONY (hook, ~18:47 UTC: okno 12–16 %, tydzień 33–34 %).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: macierz 11 twierdzeń, 11 zgodnych; kontrola wpływu: UI-ADMINISTRATOR-DASHBOARD, UI-KONTO-USTAWIENIA, INT-PLATNOSCI-CYKLICZNE, RB-ABONAMENT-ZARZADZANIE — bez zmian.
- Rundy korekt: 0.
- Czas do akceptacji: ~10 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 rozbieżności.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: każdy wiersz z twierdzeniem dokumentu i realizacją w kodzie (metoda, test, mutacja); dziennik rozbieżności z samymi wpisami `zamknięty`.

### 2210-BE-1 (migracja kolumny widoczności, zapis i odczyt zasad poziomów, ścieżka przeliczenia) — 2026-10-21
- Archetyp: Backend — migracja danych + pliki niezmiennika przeliczenia poziomów (handler, repozytorium, SQL, harmonogram, applier, strażnik zlecenia).
- Stawka: wysoka / high-stakes (migracja danych, naliczanie wartości, współbieżność zapisu przy zleconym przeliczeniu).
- Niepewność: niska (wzorzec siostrzanego pola z #1762).
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 `xhigh` (1175 s, 199 tur, maks. ~281 tys. kontekstu).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review` (R1-BE-N, 117 s, 33 pliki).
- Dopuszczone alternatywy: Muse Wonder Full `max` tylko przy CZERWONYM — i tak zablokowany limitem tygodniowym; poza tym brak.
- Powód wyboru: pliki niezmiennika — reguła 2/twarda bramka; recenzent spoza rodziny Claude, krótki diff — Sol `high` zamiast Muse (zablokowany).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany ZIELONY (hook, ~15:15 UTC: okno 5 %, tydzień 43 %); Codex nieznany (wrapper, ostatni przebieg 14:13 UTC bez limitu); Muse zablokowany do 2026-10-26T00:00Z (429, 08:13 UTC).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowany; build i testy po fali (zakaz `dotnet` w fali z 3 wykonawcami BE) zielone — 8062 testy.
- Rundy korekt: 0.
- Czas do akceptacji: ~26 min (15:49 → ~16:15 UTC z walidacją fali).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 — recenzent przeczytał handler, strażnik, repozytorium, applier i SQL.
- Defekty po odbiorze: brak (bramka BE `gpt-6.1-sol` `max`: 0 znalezisk).
- Wymagane testy i dowody: `dotnet build` 0 ostrzeżeń, pełne `dotnet test` z SQLEXPRESS; testy migracji i zapisu w BE-T.
- Uwagi: wykonawca sam zgłosił 3 trafne luki do briefów testerów (słaba asercja „nic nie zapisane” przy domyślnym `true`, nierozróżnialna zamiana pól w mapperze, kolejność wdrożenia BE → FE przez `[JsonRequired]`) — wszystkie weszły do BE-Ta/BE-Tb/BE-TK.

### 2210-BE-2 (onboarding: zapis drugiego ustawienia widoczności i „Kopiuj z…”) — 2026-10-21
- Archetyp: Backend API / CRUD bez niezmiennika.
- Stawka: średnia.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Claude / `wykonawca` — Sonnet 5.5 `high` (107 s, 25 tur, ~143 tys.).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (R1-BE razem z BE-3, 720 s).
- Dopuszczone alternatywy: Gemini Flash `high` write; Codex odrzucony (> 5 plików przy sygnale `nieznany` w funkcji high-stakes).
- Powód wyboru: ~10 plików mechanicznie podobnych do pola siostrzanego; Sonnet z kontekstem repo szybszy niż samodzielny brief dla Gemini.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany ZIELONY (hook, ~15:15 UTC); Gemini nieznany (ostatni przebieg 14:24 UTC udany).
- Pewność decyzji: niska (brak lokalnych wyników tego archetypu w tym obszarze).
- Wynik pierwszego podejścia: zaakceptowany.
- Rundy korekt: 0.
- Czas do akceptacji: ~26 min (z walidacją całej fali BE).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): w diffie BE-2/BE-3: 2×P2 potwierdzone (brak testów maskowania i wartości domyślnej — już w planie BE-Tb), 1×P3 obalone (asymetria domyślnej wartości w onboardingu to stan sprzed PBI, niewidoczny dla użytkownika).
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: build/testy BE po fali; testy `null → true` i odczytu „Kopiuj z…” w BE-Tb.
- Uwagi: brief podał ścieżki bez zagnieżdżonego `ZebraniBE\ZebraniBE\` — wykonawca znalazł sam.

### 2210-BE-3 (+K S3358) (odczyt karty klienta: serwer wycina ukryte dane, flagi w odpowiedzi) — 2026-10-21
- Archetyp: Backend API / odczyt bez niezmiennika (SQL, DAO, builder, DTO).
- Stawka: średnia (wyciek danych ukrytych przez właściciela, bez wartości pieniężnej).
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Claude / `wykonawca` — Sonnet 5.5 `high` (~5 min + korekta 48 s).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (R1-BE).
- Dopuszczone alternatywy: Gemini Flash `high` write; Codex odrzucony jak w BE-2.
- Powód wyboru: jak BE-2.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-2.
- Pewność decyzji: niska.
- Wynik pierwszego podejścia: wymagana korekta — build pada na analizatorze S3358 (zagnieżdżony operator warunkowy) w builderze; wykonawca nie mógł tego zobaczyć (zakaz `dotnet build` w fali).
- Rundy korekt: 1 (S3358, wróciło do autora przez SendMessage).
- Czas do akceptacji: ~26 min (z ponownym buildem i testami BE).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): wspólne z BE-2 (2×P2 → BE-Tb, 1×P3 obalone).
- Defekty po odbiorze: brak (bramka BE 0 znalezisk).
- Wymagane testy i dowody: build 0 ostrzeżeń, 8062 testy; macierz 4 kombinacji i najwyższy poziom w BE-Tb.
- Uwagi: zakaz `dotnet build` przy > 1 wykonawcy BE przesuwa błędy analizatora na walidację architekta — koszt jednej krótkiej rundy, akceptowalny.

### 2210-FE-S1 (stan zasad poziomów w Ustawieniach: drugie ustawienie przez każdą ścieżkę zapisu, podglądu i potwierdzenia) — 2026-10-21
- Archetyp: Frontend — logika stanu z niezmiennikiem (wyścigi zapisu, wybór `applyMode`, blokada w karencji).
- Stawka: wysoka / high-stakes.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 `xhigh` (707 s, 92 tury, ~191 tys.).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review` (R1-FE-N, 112 s).
- Dopuszczone alternatywy: brak poza wyjątkiem CZERWONEGO (Muse zablokowany).
- Powód wyboru: plik niezmiennika — `wykonawca-opus`; recenzja krótkim diffem, inna rodzina.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-1.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowany — 384 testy ustawień zielone; mutacja potwierdziła przejście pola przez 8 ścieżek.
- Rundy korekt: 0.
- Czas do akceptacji: ~17 min (15:49 → ~16:06 UTC z walidacją FE).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 (brak testu `showLevelLadder = false` był już w planie FE-T1).
- Defekty po odbiorze: brak (bramka FE 0 znalezisk).
- Wymagane testy i dowody: pełne FE (lint, format, 4684 testy, build); FE-T1 w fali 3.

### 2210-FE-W (+mechanik) (kreator, krok 3: dwa przełączniki w jednym panelu, szkic, kopiowanie, ładunek) — 2026-10-21
- Archetyp: Frontend UI + logika szkicu bez niezmiennika.
- Stawka: średnia.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Claude / `wykonawca` — Sonnet 5.5 `high` (556 s, 63 tury, ~166 tys.); poprawka 360 px — `mechanik` Haiku 5.5 `low` (52 s).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (R1-FE razem z FE-C i I18N, 785 s).
- Dopuszczone alternatywy: Gemini Flash `high` write.
- Powód wyboru: ekran i szkic z kontekstem sesji; Figma nie była wymagana (tekstowy brief).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-2.
- Pewność decyzji: niska.
- Wynik pierwszego podejścia: zaakceptowany (29 speców onboardingu, 296 testów).
- Rundy korekt: 1 — `browser-check` fali 2 pokazał ściśnięty przełącznik przy 360 px (brak `flex-shrink: 0`); poprawka z gotową treścią przez `mechanik`, zrzuty 8/8 po poprawce.
- Czas do akceptacji: ~17 min do walidacji fali 1; poprawka wizualna ~1 h później (fala 2).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R1-FE 3×P3 dla FE-W/FE-C (brak testów przełącznika i mapowania, niespójny warunek ukrywania drabiny) → testy fali 2.
- Defekty po odbiorze: ściśnięty przełącznik na 360 px (wyżej); audyt SCSS — brak `cursor: pointer` i duplikat wiersza opcji z krokiem pieczątek → FE-SCSS-K.
- Wymagane testy i dowody: specy onboardingu, `browser-check` matrix kroku 3 (Light/Dark × 360/1280).
- Uwagi: `ng test` z Git Bash pada na „Vitest failed to find the runner” (mała litera dysku) — z PowerShella przechodzi; dopisać do szablonu briefu FE.

### 2210-FE-C (karta klienta, widok kodu, nakładka po skanie — ukrywanie przez `@if`) — 2026-10-21
- Archetyp: Frontend UI bez niezmiennika (DTO, model widoku, builder, 5 komponentów).
- Stawka: średnia.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Claude / `wykonawca` — Sonnet 5.5 `high` (507 s, 80 tur, ~189 tys.).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (R1-FE).
- Dopuszczone alternatywy: Gemini Flash `high` write.
- Powód wyboru: wiele powiązanych komponentów wspólnych (podgląd karty używany też przez sprzedawcę i kreator) — wymaga kontekstu repo.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-2.
- Pewność decyzji: niska.
- Wynik pierwszego podejścia: zaakceptowany (51 speców, 476 testów; eslint, prettier czyste).
- Rundy korekt: 0.
- Czas do akceptacji: ~17 min (z walidacją FE).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R1-FE 3×P3 wspólne z FE-W → testy fali 2.
- Defekty po odbiorze: brak (bramka FE 0; `browser-check` karty A2/B/C OK; smoke PRE 20/20).
- Wymagane testy i dowody: FE-T3a/b/K/R; zrzuty kombinacji ustawień na lokalnej bazie demo.
- Uwagi: wykonawca trafnie ostrzegł, że fixture'y z pustą drabiną dają teraz `levelCount = 0` — przekazane testerom.

### 2210-I18N (wspólna grupa kluczy widoczności, pl+en, usunięcie starych kluczy kreatora skryptem) — 2026-10-21
- Archetyp: Mechaniczna zmiana i18n z gotową treścią.
- Stawka: niska.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Claude / `mechanik` — Haiku 5.5 `low` (40 s).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (R1-FE).
- Dopuszczone alternatywy: Sonnet `high`.
- Powód wyboru: dokładna treść 6 kluczy × 2 języki i skrypt.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-2.
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: zaakceptowany.
- Rundy korekt: 0.
- Czas do akceptacji: ~17 min (z walidacją fali).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: kontrola kluczy pl/en, `npm test`.
- Uwagi: wykonawca zgłosił, że usunięte klucze są jeszcze używane — przepięcie robił FE-W w tej samej fali (zgodnie z planem); brief powinien to mówić wprost, by worker nie musiał tego zgłaszać jako błędu.

### 2210-DOC-1 (+DOC-1K) (6 datowanych rewizji, nowa decyzja, indeks; poprawki po recenzji wraz z separatorem w Figmie) — 2026-10-21
- Archetyp: Dokumentacja normatywna po polsku (+ drobna poprawka Figmy w DOC-1K).
- Stawka: średnia.
- Niepewność: średnia (rewizja istniejącej rewizji 2026-09-28 w Ustawieniach, reguła „jeden rząd pieczątek”).
- Wykonawca (linia / model / native effort): Claude / `wykonawca` — Sonnet 5.5 `high` (DOC-1 537 s, ~275 tys.; DOC-1K 317 s).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (R1-DOC, 613 s).
- Dopuszczone alternatywy: Gemini Flash `high` write; Muse Spark `max` — zablokowany.
- Powód wyboru: tekst normatywny wymagający kontekstu decyzji z planu; Figma w DOC-1K wymagała MCP (tylko Claude/Codex).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-2.
- Pewność decyzji: niska.
- Wynik pierwszego podejścia: wymagane korekty — stara treść normatywna w aktywnej sekcji Ustawień, bezwarunkowy opis paska w karcie, brak „Rozważonych wariantów” w DEC, reguła „jeden rząd” bez wyjątku.
- Rundy korekt: 1 (DOC-1K).
- Czas do akceptacji: ~40 min (15:49 → ~16:29 UTC).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 2×P1 (1 potwierdzone, 1 obalone), 4×P2 i 3×P3 — poprawione w DOC-1K.
- Defekty po odbiorze: brak (przegląd 4c: 104 zgodne, 0 rozbieżności).
- Wymagane testy i dowody: linki względne i kotwice 0 martwych; front matter bez zmian; diff repo Dokumentacja.
- Uwagi: wykonawca słusznie zakwestionował datę decyzji (potwierdzona w „Źródłach” PBI) i konflikt z `interfejsy/README.md` — oba rozstrzygnięte przez architekta.

### 2210-FIG-1 (+1b, 1c) (karta klienta poziomów: zwinięta, nowa rozwinięta, widok kodu — warianty ukrytych elementów) — 2026-10-21
- Archetyp: Frontend UI / Figma.
- Stawka: niska.
- Niepewność: wysoka (rozwiniętej karty poziomów w Figmie nie było).
- Wykonawca (linia / model / native effort): Claude / `wykonawca` — Sonnet 5.5 `high` (FIG-1 139 s STOP; FIG-1b 825 s, przekazanie przy 301 tys.; FIG-1c 683 s, ~279 tys.).
- Recenzent (linia / model / native effort): architekt — `get_screenshot` / `get_metadata` (Muse i Gemini bez Figmy).
- Dopuszczone alternatywy: Codex z Figma MCP — niepotwierdzony w sesji; brak.
- Powód wyboru: jedyna linia z potwierdzonym Figma MCP (próba A/B 2026-10-12: Figma zostaje u `wykonawca`).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-2.
- Pewność decyzji: wysoka (brak alternatywy).
- Wynik pierwszego podejścia: STOP — dwie błędne przesłanki (brak rozwiniętej karty poziomów do sklonowania; widok kodu na mobile to ekran pełny, nie arkusz).
- Rundy korekt: 2 (FIG-1b po korekcie przesłanek; FIG-1c jako kontynuacja po strażniku kontekstu).
- Czas do akceptacji: ~40 min (15:49 → ~16:29 UTC).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): przyjęte; uwagi do raportu bramy — nadpisanie `primaryAxisAlignItems=MIN` przy „Kreska ze znakiem” w istniejących ekranach (stan sprzed zadania), brak właściwości `Liczba pieczatek` na poziomie zestawu.
- Defekty po odbiorze: drugi wiersz ustawień ma tę samą nazwę warstwy co pierwszy (kosmetyka, FIG-2/Ustawienia).
- Wymagane testy i dowody: `get_metadata` 4106:22834 (zestaw `RozwinietaPoziomy`, 4 warianty), 4106:23583/24279 (BothOff Light/Dark), 4106:24536/24544 (widok kodu 1280/360).
- Uwagi: błąd briefu architekta (przesłanka o istniejącej rozwiniętej karcie) kosztował rundę — przed briefem Figmy sprawdzić `get_metadata` strony, nie tylko dokument.

### 2210-FIG-2 (kreator krok 3 i Ustawienia → Program: dwa przełączniki) — 2026-10-21
- Archetyp: Frontend UI / Figma.
- Stawka: niska.
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): Claude / `wykonawca` — Sonnet 5.5 `high` (400 s, 73 tury, ~241 tys.).
- Recenzent (linia / model / native effort): architekt — `get_screenshot` / `get_metadata`; R1-DOC (Gemini) wskazał separator niezgodny z planem.
- Dopuszczone alternatywy: brak (Figma MCP).
- Powód wyboru: jak FIG-1.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak BE-2.
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: zaakceptowany z odchyleniami — 3 błędne przesłanki briefu (kreator miał `CheckboxMark`, nie przełącznik; „Adres lokalu” nie istnieje w makiecie kroku 3; `description` nie istnieje na `FRAME`).
- Rundy korekt: 1 (usunięcie separatora między przełącznikami w 2 ekranach desktopowych — w DOC-1K).
- Czas do akceptacji: ~40 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): separator — potwierdzony, poprawiony.
- Defekty po odbiorze: brak „Adresu lokalu” w makiecie kroku 3 (luka sprzed zadania, raport bramy).
- Wymagane testy i dowody: `get_metadata` 2391:3060 (Ustawienia, dwa wiersze przełączników).

### 2210-FE-S2 (Ustawienia → Program: drugi przełącznik, wspólne teksty z kreatorem, bez etykiety stanu) — 2026-10-21
- Archetyp: Frontend UI bez niezmiennika.
- Stawka: średnia.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Claude / `wykonawca` — Sonnet 5.5 `high` (237 s, 27 tur, ~145 tys.).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (R2-FE, 502 s).
- Dopuszczone alternatywy: Gemini Flash `high` write.
- Powód wyboru: ekran zależny od FE-S1 i istniejącego speca — kontekst repo.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook; ZIELONY na starcie fali 1, ŻÓŁTY ~54 % okna pod koniec dnia); Gemini nieznany (przebiegi udane).
- Pewność decyzji: niska.
- Wynik pierwszego podejścia: zaakceptowany (28/28 w specu; 4 stare klucze usunięte, 0 użyć w `src`).
- Rundy korekt: 0.
- Czas do akceptacji: ~15 min (z walidacją fali 2).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1×P1 R2-FE (brak testu interakcji drugiego przełącznika) — pokryty zaplanowanym FE-T1, nie defekt FE-S2.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: FE-T1, `browser-check` Ustawień (8/8).

### 2210-BE-T (BE-Ta, BE-Tb, BE-TK) (testy BE: migracja, zapis widoczności, karencja, odmowy, harmonogram, onboarding, karta klienta, nakładka; korekty po R2) — 2026-10-21
- Archetyp: Testy integracyjne i jednostkowe BE (xunit na SQLEXPRESS).
- Stawka: wysoka (testy plików niezmiennika).
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): Claude / `tester` — Haiku 5.5 `xhigh` (BE-Ta 790 s, ~329 tys.; BE-Tb 639 s, ~304 tys.; BE-TK 568 s), sekwencyjnie (jedno drzewo, `dotnet test`).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (R2-BE, 542 s).
- Dopuszczone alternatywy: Sonnet `high`; Codex odrzucony (pula przed bramką).
- Powód wyboru: linia `tester` od 2026-10-13; scenariusze nazwane w briefie.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak FE-S2.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: BE-Ta i BE-Tb zielone (BE-Tb: 631 w filtrze), ale R2-BE wykazał nierozróżnialną zamianę pól i fałszywie zieloną asercję stanu bazy.
- Rundy korekt: 1 (BE-TK, z dowodem rozróżnialności — mutacja handlera czerwona, przywrócenie sprawdzone sha256).
- Czas do akceptacji: ~70 min (16:30 → ~17:41 UTC).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 2×P1 — 1 potwierdzone (zamiana pól niewykrywalna), 1 obalone → P3; 3×P2 i 2×P3 potwierdzone (duplikat testu, podwójne `<summary>`, pozorne asercje maskowania w teście nakładki, podgląd bez `showLevelLadder: false`) → BE-TK.
- Defekty po odbiorze: brak (bramka BE 0).
- Wymagane testy i dowody: pełne BE — build 0 ostrzeżeń, 8094 testy, 0 pominiętych.
- Uwagi: dwa przebiegi > 300 tys. kontekstu (strażnik miękki, bez przekazania). Test nakładki dowodzi tylko przekazania karty — maskowanie dowodzą testy zapytania (zgłosił tester; do raportu bramy).

### 2210-FE-T2 (testy kreatora: dwa przełączniki, opisy, domyślne, zmiana kategorii, kopiowanie, ładunek) — 2026-10-21
- Archetyp: Testy jednostkowe FE (Vitest).
- Stawka: średnia.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Claude / `tester` — Haiku 5.5 `xhigh` (338 s, ~229 tys.).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (R2-FE).
- Dopuszczone alternatywy: Sonnet `high`.
- Powód wyboru: linia `tester`.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak FE-S2.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowany (11 scenariuszy, 4 specy zielone).
- Rundy korekt: 0.
- Czas do akceptacji: ~20 min (z walidacją fali 2).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 dla FE-T2.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: `npm test` pełny zielony.

### 2210-FE-T3 (T3a, T3b, T3K, T3R) (testy karty klienta, widoku kodu i nakładki: kombinacje, najwyższy poziom, brak w DOM, AXE; korekty po R2 i R3) — 2026-10-21
- Archetyp: Testy jednostkowe FE z AXE.
- Stawka: średnia.
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): Claude / `tester` — Haiku 5.5 `xhigh` (T3a 392 s, T3b 416 s, T3K 411 s, T3R 330 s).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (R2-FE dla T3a/b, R3 dla T3K).
- Dopuszczone alternatywy: Sonnet `high`.
- Powód wyboru: linia `tester`; rozłączne pliki T3a/T3b równolegle.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak FE-S2.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zielone (T3a 109 testów w 5 specach, T3b 41/41), ale R2-FE: fałszywa zieleń ukrywania drabiny w specu ekranu kodu i brak wariantu `showLevelLadder: false` w specu dialogu.
- Rundy korekt: 2 (T3K po R2-FE; T3R po R3 — zmiana 3 (P3) zamknięta bez poprawki, bo przekraczała `max-lines-per-function`, a parę „jest/nie ma” pokrywa inny spec).
- Czas do akceptacji: ~80 min (16:26 → ~17:49 UTC).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R2-FE: 2×P1 potwierdzone, 1×P2 obalone (helper szukający w `document` — pomiar pokazał podpięty host), 1×P2 i 1×P3 potwierdzone; R3: 2×P2 i 2×P3 potwierdzone (1×P3 zamknięte bez poprawki z uzasadnieniem).
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: pełne FE 4754 testy; AXE wariantów ukrytych.
- Uwagi: przesłanka briefu T3b („poziom X z Y znika przy `levelCount` 0” w ekranie kodu) była nieprecyzyjna — decyzję podejmuje dialog; tester pokrył to na prawdziwym okablowaniu.

### 2210-FE-T1 (testy Ustawień: stan, blokada, zlecone przeliczenie, potwierdzenie, UI drugiego przełącznika, AXE) — 2026-10-21
- Archetyp: Testy jednostkowe FE pliku niezmiennika (stan zapisu).
- Stawka: wysoka.
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): Claude / `tester` — Haiku 5.5 `xhigh` (742 s, ~295 tys.).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (R3, 600 s).
- Dopuszczone alternatywy: Sonnet `high`.
- Powód wyboru: linia `tester`.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak FE-S2.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowany (16 scenariuszy; testy przeniesione do `-edge-cases` z powodu `max-lines`).
- Rundy korekt: 1 (2×P2 R3 — w T3R: brak asercji `label[for]` liczby, brak drugiego kliku powrotnego).
- Czas do akceptacji: ~60 min (16:49 → ~17:49 UTC).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R3: 0×P0/P1; 2×P2 potwierdzone (wspólne z FE-T3 wyżej). Recenzent potwierdził scenariusz niezmiennika (drabina docelowa zlecenia, `applyMode: null`).
- Defekty po odbiorze: brak (bramka FE 0).
- Wymagane testy i dowody: pełne FE 4754.
- Uwagi: brief wskazał zły zakres linii wzorca — tester sam zweryfikował zachowanie `confirm()` w kodzie.

### 2210-R1-N (recenzje fali 1 plików niezmiennika: BE-1 i FE-S1) — 2026-10-21
- Archetyp: Recenzja plików niezmiennika high-stakes, tylko odczyt.
- Stawka: wysoka / high-stakes.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): — (recenzja).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review` (R1-BE-N 117 s, R1-FE-N 112 s).
- Dopuszczone alternatywy: Muse Wonder Full `max` (reguła 8 dla tego archetypu) — zablokowany do 2026-10-26; Gemini Flash `high` — niższa klasa przy tej stawce.
- Powód wyboru: ponowna kwalifikacja wg reguły 2 przy zablokowanym Muse; krótkie diffy (≤ 33 pliki) i `high` zamiast `max` — oszczędność puli Plusa przed bramką.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper, 16:06 i 16:15 UTC bez limitu); Muse zablokowany.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: oba czyste.
- Rundy korekt: 0.
- Czas do akceptacji: ~2 min każda + odczyt raportu.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0/0.
- Defekty po odbiorze: brak (bramki BE i FE 0 znalezisk).
- Wymagane testy i dowody: raport z listą przeczytanych plików (handler, strażnik, repozytorium, applier, SQL; stan FE).
- Uwagi: Sol `high` wobec Wondera Full `max` przy recenzji fal niezmiennika — 2 przebiegi bez znalezisk, potwierdzone czystą bramką `max`; za mało, by zmienić preferencję z reguły 8.

### 2210-R1 (recenzje fali 1 bez niezmiennika: R1-BE, R1-FE, R1-DOC) — 2026-10-21
- Archetyp: Recenzja niskiej/średniej stawki, tylko odczyt.
- Stawka: średnia.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): — (recenzja).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (R1-BE 720 s, R1-FE 785 s, R1-DOC 613 s).
- Dopuszczone alternatywy: Sol `high` (pula Codexa oszczędzana na bramkę); Muse — zablokowany.
- Powód wyboru: reguła 13 — preferencja Sol/Gemini `high` przy niskiej stawce; inna rodzina niż autor (Claude).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany (przebiegi 16:06–16:30 UTC udane).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: raporty kompletne.
- Rundy korekt: 0.
- Czas do akceptacji: 10–13 min na przebieg + triaż.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R1-BE 2×P2 potwierdzone, 1×P3 obalone; R1-FE 3×P3 potwierdzone; R1-DOC 2×P1 (1 potwierdzone, 1 obalone), 4×P2, 3×P3 potwierdzone. Fałszywych P0/P1: 1 (R1-DOC).
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: każde P1 sprawdzone w dokumencie przed poprawką.

### 2210-R2 (recenzje fali 2: R2-FE, R2-BE — testy i ekran Ustawień) — 2026-10-21
- Archetyp: Recenzja testów FE/BE, tylko odczyt.
- Stawka: średnia–wysoka (testy plików niezmiennika).
- Niepewność: niska.
- Wykonawca (linia / model / native effort): — (recenzja).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (R2-FE 502 s, R2-BE 542 s).
- Dopuszczone alternatywy: Sol `high` (pula przed bramką); Muse — zablokowany.
- Powód wyboru: jak R1; autor (Haiku) z rodziny Claude.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany (przebiegi udane).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: raporty kompletne, ze scenariuszami.
- Rundy korekt: 0.
- Czas do akceptacji: ~10 min na przebieg + triaż.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R2-FE 3×P1 (2 potwierdzone, 1 = zaplanowany FE-T1), 2×P2 (1 obalone pomiarem), 1×P3; R2-BE 2×P1 (1 potwierdzone, 1 obalone → P3), 3×P2 i 2×P3 potwierdzone. Fałszywych P0/P1: 2 z 5.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: każde P1 sprawdzone w kodzie przed korektą.
- Uwagi: Gemini znalazł 3 realne P1 fałszywej zieleni w testach, których tester nie zauważył — wartość recenzji testów potwierdzona.

### 2210-R3 (recenzja fali 3: FE-T1 i FE-T3K) — 2026-10-21
- Archetyp: Recenzja testów FE, tylko odczyt.
- Stawka: średnia–wysoka.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): — (recenzja).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (600 s, 9 plików).
- Dopuszczone alternatywy: Sol `high`; Muse — zablokowany.
- Powód wyboru: jak R2.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 0×P0/P1; scenariusz niezmiennika potwierdzony.
- Rundy korekt: 0.
- Czas do akceptacji: ~10 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 2×P2 i 2×P3 potwierdzone (1×P3 zamknięte bez poprawki z uzasadnieniem). Fałszywych P0/P1: 0.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: P2 sprawdzone w kodzie.

### 2210-SCSS (+FE-SCSS-K) (audyt SCSS diffu i wydzielenie wspólnego wiersza opcji) — 2026-10-21
- Archetyp: Audyt SCSS + mechaniczny refaktor.
- Stawka: niska.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): audyt Gemini / `gemini-3.8-flash-high` `-Access read` (392 s); poprawka Claude / `mechanik` — Haiku 5.5 `low` (206 s).
- Recenzent (linia / model / native effort): poprawka — R3/bramka FE (Gemini, Sol `max`) i zrzuty architekta.
- Dopuszczone alternatywy: audyt Sol `high`; Muse Spark `max` (dotychczasowa linia audytu) — zablokowany.
- Powód wyboru: Muse zablokowany; poprawka z dokładną treścią — `mechanik`.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany; Claude znany.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: audyt kompletny (oba pliki); poprawka zielona.
- Rundy korekt: 0.
- Czas do akceptacji: ~15 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 2×P2 (brak `cursor: pointer`, promień spoza skali) i 3×P3 (komentarze, nieużywane tokeny) — wydzielenie wiersza opcji, kursor i komentarze poprawione; linie sprzed zadania → raport bramy.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: stylelint, zrzuty kroku 3 poziomów i pieczątek 8/8.
- Uwagi: komentarz „konsumują `stamp-rules` i `level-rules`” nad kilkoma mixinami w `_settings-shared.scss` jest nieaktualny (zgłosił `mechanik`) — kandydat na drobny refaktor.

### 2210-G-BE (bramka końcowa BE, cały diff funkcji) — 2026-10-21
- Archetyp: Bramka końcowa high-stakes — recenzja całego diffu BE, tylko odczyt.
- Stawka: wysoka / high-stakes.
- Niepewność: niska (po trzech recenzjach fal).
- Wykonawca (linia / model / native effort): — (bramka).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `max`, `-Mode review`, jeden przebieg na całe repo BE (271 s).
- Dopuszczone alternatywy: brak (reguła 6); przy limicie — jednorazowo Muse Wonder Full `max` od 26.10 (decyzja właściciela D4d), niepotrzebne.
- Powód wyboru: reguła 6.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper, 17:46 UTC; R1-N bez limitu).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: „gotowe do wydania”, 0 znalezisk.
- Rundy korekt: 0.
- Czas do akceptacji: ~5 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0.
- Defekty po odbiorze: brak (PRE: BE 1.13.0, smoke 20/20).
- Wymagane testy i dowody: build 0 ostrzeżeń, 8094 testy, 0 pominiętych.

### 2210-G-FE (bramka końcowa FE, cały diff funkcji + kontrakt BE) — 2026-10-21
- Archetyp: Bramka końcowa high-stakes — recenzja całego diffu FE, tylko odczyt.
- Stawka: wysoka / high-stakes.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): — (bramka).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `max`, `-Mode review` (478 s, 61 plików).
- Dopuszczone alternatywy: jak G-BE.
- Powód wyboru: reguła 6; sekwencyjnie po bramce BE.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper, 17:51 UTC).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: „gotowe do wydania”, 0 znalezisk.
- Rundy korekt: 0.
- Czas do akceptacji: ~8 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0.
- Defekty po odbiorze: brak (PRE: FE 1.9.0, smoke 20/20).
- Wymagane testy i dowody: lint, format, 4754 testy, build.
- Uwagi: cała funkcja przeszła obie bramki bez znalezisk po 3 rundach recenzji Gemini/Sol `high` — tu bramka niczego nie dołożyła; wartość bramki zależy od jakości recenzji fal.

### 2210-4C (przegląd zgodności dokumentacji z kodem) — 2026-10-21
- Archetyp: Przegląd zgodności dokumentacja ↔ kod, obie strony, tylko odczyt.
- Stawka: średnia.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): — (przegląd).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (555 s).
- Dopuszczone alternatywy: Sol `high` (pula przed bramką — bramki już zakończone); Sonnet read (ta sama rodzina co autor rewizji — wykluczony); Muse — zablokowany.
- Powód wyboru: inna rodzina niż autor rewizji (Claude).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany (17:53 UTC).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 104 twierdzenia zgodne, 0 rozbieżności.
- Rundy korekt: 0.
- Czas do akceptacji: ~12 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 rozbieżności.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: macierz z cytatem dokumentu i `plik:linia`.
- Uwagi: brief miał 5 błędnych przesłanek (ścieżka `AGENTS.md`, położenie §10/§14 w `INSTRUKCJA-DLA-AI.md`, zagnieżdżone ścieżki BE, statusy indeksów) — recenzent skorygował sam; to drugi raz (po 2723-4C) — szablon briefu 4c do poprawy.

### 2210-QAS-A (QA Sphere: przegląd 100 istniejących + nowe przypadki kreatora i Ustawień → Program) — 2026-10-21
- Archetyp: QA Sphere — autor pliku podglądu (przegląd istniejących + luki) w funkcji high-stakes.
- Stawka: średnia (przypadki testowe, bez kodu; funkcja high-stakes).
- Niepewność: średnia (stany karencji i programu zamkniętego osiągalne tylko skryptami SQL).
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access write` (1010 s) + korekta K1 (673 s).
- Recenzent (linia / model / native effort): Claude / `wykonawca` Sonnet 5.5 `high`, tylko odczyt (368 s).
- Dopuszczone alternatywy: autor — Muse Wonder `max` (skill: w funkcji high-stakes) zablokowany limitem tygodniowym; recenzent — Muse Wonder `max` (twarda reguła skilla: plik Gemini → Muse) zablokowany do 2026-10-26 00:00Z → ponowna kwalifikacja wg reguły 2 na Sonneta read (precedens 2723-QAS, 2747, 2785); Sol `high` oszczędzany (pula Codexa po bramkach).
- Powód wyboru: jedyna dostępna linia autora z QA Sphere MCP poza Muse; recenzent z innej rodziny niż Gemini.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany (wrapper, 18:14 UTC); Muse zablokowany (429 z resetem 2026-10-26T00:00Z, 08:13 UTC); Claude znany ZIELONY (hook, 18:30 UTC).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 17 nowych, 12 aktualizacji, 88 keep, lint --strict 0/0; recenzja: 5×P1 potwierdzone (konto `onboarding3` zamiast jednomiejscowego `onboarding1` w 369; K5 obiecywał okno przy zamknięciu X; U3/U4 bez przygotowania karencji, U4 z kodem 409 i nazwą błędu niewidocznymi dla testera; U5 bez sposobu zamknięcia programu), 0 obalonych.
- Rundy korekt: 1 (K1: 12 punktów, nowy K10 — persystencja zapisu z kreatora w Ustawieniach).
- Czas do akceptacji: ~85 min (autor → recenzja → K1 → kontrola wyrywkowa architekta → brama właściciela).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 5×P1 + P3 potwierdzone, 0 odrzuconych.
- Defekty po odbiorze: brak; `verify` 0 realnych różnic (autolink w warunkach wstępnych i kolejność `requirements` 1375 — artefakty odczytu, normalizacja doraźna).
- Wymagane testy i dowody: `qas.py lint --strict`, kontrola wyrywkowa U4/U5/K5/K10 względem kodu i dokumentacji, `verify` po wysyłce (seq 1743–1760).
- Uwagi: błędy briefu architekta — zakaz SQL w `00-wspolne.md` kolidował z karencją i programem zamkniętym; brief zakładał ostrzeżenie przy X w kreatorze; wzorzec `beforeunload` (1117) leży w innym folderze; zła ścieżka klucza `LEVELS_PENDING`; `onboarding3` ma 3 miejsca. Szablon briefu QA Sphere: przy stanach nieosiągalnych w UI wskazywać od razu przypadki-źródła skryptów.

### 2210-QAS-B (QA Sphere: przegląd 51 istniejących + nowe przypadki karty klienta, widoku kodu i nakładki po skanie) — 2026-10-21
- Archetyp: QA Sphere — autor pliku podglądu (przegląd istniejących + luki) w funkcji high-stakes.
- Stawka: średnia.
- Niepewność: średnia (naliczenie kodem z paragonu zmienia stan wspólnej karty demo).
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access write` (1046 s) + korekta K1 (1172 s).
- Recenzent (linia / model / native effort): Claude / `wykonawca` Sonnet 5.5 `high`, tylko odczyt (487 s).
- Dopuszczone alternatywy: jak 2210-QAS-A.
- Powód wyboru: jak 2210-QAS-A.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak 2210-QAS-A.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 12 nowych, 5 aktualizacji, 45 keep, 1 retire (1146 — duplikat 1145, potwierdzony porównaniem treści), lint --strict 0/0; recenzja: 4×P1 potwierdzone (C9 z nieistniejącym w seedach sprzedawcą programu poziomów; skrypt przywracający 696 cofa licznik bez `CurrentLevelId` — defekt sprzed zadania, karta zostawała na Platynie; C8 z wymyślonym kodem paragonu; 1131/1140 — ręczne kroki dopisane do przypadków `Automated` z fixture'a), 0 obalonych.
- Rundy korekt: 1 (K1: 8 punktów, nowe C7b, C7c, C8b; 1144 keep → update).
- Czas do akceptacji: ~85 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 4×P1 + P3 potwierdzone, 0 odrzuconych.
- Defekty po odbiorze: brak; `verify` 0 realnych różnic (`\_` w C5 — artefakt odczytu).
- Wymagane testy i dowody: `qas.py lint --strict`, kontrola wyrywkowa C1/C7c/C8/C8b/C9/696/1146 względem kodu, `verify` po wysyłce (seq 1761–1775).
- Uwagi: autor słusznie zgłosił konflikt briefu z lintem (`XXX-XXX-XXX` z oryginału 696 łapie reguła zaślepek `--strict`) i sformułował krok neutralnie. `qas.py retire` padał na 1146: `get_test_case` pomija klucz `tags`, gdy przypadek nie ma tagów — poprawka jednej linii w `_retire_live_case` (2026-10-21).

### 1605-FE-V (+FE-V-K) (komponenty prezentacyjne wariantu „anulowana”, wejście w pasku zaufania i drobnym druku, napisy pl/en, specy z AXE) — 2026-10-21
- Archetyp: Frontend UI / Figma — ekran bez niezmiennika w funkcji high-stakes.
- Stawka: średnia (warstwa widoku; logika przepływu w osobnym briefie).
- Niepewność: niska (wzorzec gałęzi zaległości z #1604).
- Wykonawca (linia / model / native effort): Claude / `wykonawca` — Sonnet 5.5 `high`, Figma MCP (~5 min) + korekta FE-V-K (100 s).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (R1-FE-V, 654 s).
- Dopuszczone alternatywy: `wykonawca-opus` (nadmiar wobec braku niezmiennika); Codex bez potwierdzonego Figma MCP w sesji → odpada; Muse i Gemini bez Figmy → odpadają.
- Powód wyboru: ekran z makiety — jedyna linia z faktycznym Figma MCP; precedens 2370-FE-2a.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany ZIELONY (hook, ~19:30 UTC: okno ~10 %, tydzień 51 %); Gemini nieznany (ostatni przebieg 2026-10-21 udany); Muse zablokowany do 2026-10-26T00:00Z (429 z resetem tygodniowym).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowany po walidacji fali (lint 0, 456/4780 testów, build); człon `ChangeSubscriptionEntry.Resume` architekt świadomie przeniósł do FE-L (enum wejścia jest częścią logiki kontenera).
- Rundy korekt: 1 (FE-V-K: 4 przyjęte P3 recenzji).
- Czas do akceptacji: ~30 min (20:03 → ~20:30 UTC z recenzją i korektą).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 5×P3 — 4 potwierdzone, 1 odrzucone (asercja akordeonu zgodna z wzorcem `arrears-summary`).
- Defekty po odbiorze: brak w kodzie; przegląd 4c znalazł 2×P2 + P3 w treści (brak wyjaśnienia niedostępności zmiany w zdaniu skutku, nieudokumentowany toast przy błędzie listy programów) — luki specyfikacji architekta, nie wykonania.
- Wymagane testy i dowody: 4 specy (46 testów) z AXE, rozszerzenie speców paska zaufania i drobnego druku, parzystość kluczy pl/en, `browser-check` matrix 12/12 po fali 2.

### 1605-DOC-1 (+DOC-1K) (datowane rewizje UI-KONTO-ZMIANA-ABONAMENTU i UI-KONTO-USTAWIENIA + korekta nazwy akcji) — 2026-10-21
- Archetyp: Dokumentacja produktowa — rewizje `zatwierdzony` wg decyzji właściciela.
- Stawka: średnia (źródło prawdy dla kodu, testów i QA Sphere).
- Niepewność: niska (decyzje W1–W4 i tabela napisów w planie).
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access write` (413 s) + korekta DOC-1K (514 s).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review` (R1-DOC, 387 s).
- Dopuszczone alternatywy: `wykonawca` Sonnet `high` (wolny tor Claude'a potrzebny dla FE-V i FIG-1); Muse Spark `max` zablokowany; recenzent — Sonnet read (inna rodzina niż Gemini), wybrany Sol, bo 2 pliki i `high` mieszczą się w limicie reguły 7.
- Powód wyboru: dokument bez niezmiennika, rozłączny z FE; Muse zablokowany.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany (wrapper, 20:03 UTC); Codex nieznany (20:11 UTC); Muse zablokowany.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: wymagane korekty — przesłanka briefu o położeniu `AGENTS.md` dokumentacji błędna (trzeci raz; pamięć `dokumentacja-agents-md-w-podkatalogu-zebrani`).
- Rundy korekt: 1 (DOC-1K) + 3 jednolinijkowe dopiski architekta.
- Czas do akceptacji: ~35 min (20:03 → ~20:38 UTC).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 4×P2 + 2×P3 — wszystkie potwierdzone.
- Defekty po odbiorze: przegląd 4c — 2 rozbieżności treści po zmianach napisów w fali 2/3 (poprawione rewizją architekta, potwierdzone przebiegiem 3 bramki).
- Wymagane testy i dowody: diff rewizji przeczytany, zgodność z tabelą napisów pl/en i z kodem (4c).

### 1605-FIG-1 (makieta wariantu wyrównana do rewizji + ramka Dark desktop + arkusz mobile Light/Dark) — 2026-10-21
- Archetyp: Figma — wyrównanie makiety i nowe ramki z istniejących komponentów biblioteki.
- Stawka: niska.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Claude / `wykonawca` — Sonnet 5.5 `high` + Figma MCP (~10 min) + dopisek zdania skutku w 4 ramkach po 4c (55 s).
- Recenzent (linia / model / native effort): architekt — zrzuty `get_screenshot` wobec rewizji (inna rodzina niedostępna: tylko Claude ma Figma MCP).
- Dopuszczone alternatywy: brak (Figma MCP tylko w linii Claude'a w tej sesji).
- Powód wyboru: jedyna linia z potwierdzonym Figma MCP.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany ZIELONY (hook, ~20:00 UTC).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: zaakceptowany — 4 ramki (Light, Dark desktop, mobile Light/Dark).
- Rundy korekt: 0 z wykonania (dopisek po 4c to zmiana treści, nie błąd).
- Czas do akceptacji: ~15 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: zrzuty 4 ramek; po dopisku zawijanie i przypięta stopka obejrzane (desktop Light, mobile Dark).

### 1605-FE-L (logika wariantu: przepływ cofnięcia, wspólny kod błędu, tryb w kontenerze, wejścia z Ustawień i Programu) — 2026-10-21
- Archetyp: Frontend — pliki niezmiennika przepływu płatności (kontener nakładki, przepływ cofnięcia, wspólna funkcja kodu błędu w dwóch istniejących przepływach, Ustawienia, Program).
- Stawka: wysoka / high-stakes (przywrócenie odnawiania płatnej subskrypcji Stripe, orkiestracja przepływów płatności).
- Niepewność: średnia (cykl życia nakładki z animacją wyjścia, zmiana konta w trakcie).
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` — Opus 5.5 `xhigh`; przebieg 1 (~12 min) przerwany strażnikiem przy ~306 tys., kontynuacja świeżym agentem (~14,5 min, zakończona przy ~303 tys.).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review` (R2, 239 s).
- Dopuszczone alternatywy: przy CZERWONYM — Muse Wonder Full `max` (zablokowany) → czekanie; recenzent — Gemini `flash-high` read (niższa klasa przy plikach niezmiennika), Muse Wonder Full `max` zablokowany.
- Powód wyboru: pliki niezmiennika — twarda bramka; recenzent spoza rodziny Claude, krótki diff (precedens 2210-R1-N).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany ZIELONY (hook, ~20:25 UTC); Codex nieznany (wrapper, 21:07 UTC); Muse zablokowany.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: przepływ, `problemCodeOf` i enumy z przebiegu 1 przyjęte po lekturze (276 testów); po kontynuacji fala zielona (456/4788), `browser-check` matrix 12/12.
- Rundy korekt: 1 po recenzji (FE-L-K: K1–K3, 472 s; K4 197 s — wykonawca sam zastąpił własne `detach()` odczytem synchronicznym `trackOpen(open)` po wykryciu wyścigu o jedną klatkę) + 2 po bramce (FE-G1, FE-G3 — wpis 1605-G-FE).
- Czas do akceptacji: ~1 h fali 2 (20:26 → ~21:28 UTC z R2 i korektą).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R2 — 2×P2 potwierdzone (status „odłączony” dopiero przy zniszczeniu, więc okno animacji wyjścia gubi toast i przełącza znikającą nakładkę; zmiana DOM w znikającej nakładce zrzuca fokus na `body`, a przycisk toastu PrimeNG ma natywne `autofocus`), 0 odrzuconych.
- Defekty po odbiorze: bramka — 2×P2 (brak świeżego odczytu abonamentu przy wejściu; odczyt listy programów nieprzerywany przy zmianie konta → toast w nowej sesji). Obie luki wynikały z projektu architekta, nie z odchylenia wykonawcy.
- Wymagane testy i dowody: lint, format, `npm test`, build po fali; `browser-check` matrix 2×2 bez klikania „Cofnij anulowanie” (zapis w obszarze wysokiej stawki — dowodem testy jednostkowe FE-T).
- Uwagi: dwa przebiegi `wykonawca-opus` po ~300 tys. przy briefie obejmującym 5 plików niezmiennika i aktualizację speców z przeciwnym oczekiwaniem — brief był za szeroki na regułę 15; na przyszłość dzielić „przepływ + kontener” od „wejścia z Ustawień i Programu”.

### 1605-FE-T (FE-T1/T1b/T1c, FE-T2/T2K, FE-T3) (specy przepływu cofnięcia, kontenera i Ustawień) — 2026-10-21
- Archetyp: Testy jednostkowe Vitest + AXE dla plików niezmiennika, z mutacjami produkcji jako dowodem czerwieni.
- Stawka: wysoka (oracle dla zapisu, którego nie klika się w przeglądarce).
- Niepewność: średnia (`httpResource` asynchroniczny w jsdom, okno zamykania `p-dialog`).
- Wykonawca (linia / model / native effort): Claude / `tester` — Haiku 5.5 `xhigh`: T1 (~9 min, przekazanie przy 316 tys.), T2 (~12,5 min), T3 (~10 min), T1b (~10,5 min), T1c (~13 min), T2K (~8 min).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (R3, 871 s, 14 plików).
- Dopuszczone alternatywy: `wykonawca` Sonnet `high`; recenzent — Sol `high` (oszczędzany przed bramką, reguła 7), Muse zablokowany.
- Powód wyboru: testy wg istniejących wzorców (2210 FE-T1/T3, 1 runda); linia `tester` po próbie z 2026-10-13.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany ZIELONY (hook, ~21:28 UTC); Gemini nieznany (21:55 UTC).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: T3 11/11 i T2 36/36 z czerwienią pod mutacjami; T1 — 42/48 czerwonych z przyczyny środowiska testu (synchroniczne asercje wobec asynchronicznego `httpResource`; idiom `await vi.waitFor` był w repo, brief go nie wskazał); T2 — 4 scenariusze okna zamykania niewykonalne na DOM w jsdom.
- Rundy korekt: 1 dla T1 (T1b naprawa + T1c reszta zakresu, równolegle), 1 dla T2 (T2K na sygnałach komponentu), 0 dla T3; po R3 — FE-TK (632 s, 102/102).
- Czas do akceptacji: ~45 min fali 3 bez recenzji (21:28 → ~22:10 UTC), ~1 h 5 min z R3 i FE-TK.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R3 — 2×P1, 4×P2, 2×P3; potwierdzone: P1 → obniżone do P2 (krok 2 fokusu nieobserwowalny na szerokim ekranie), 4×P2 (jedno zawężone); P1 drugie odrzucone jako P1 (ścieżka nieosiągalna przez przepływ — tylko nazwa testu); 2×P3 odrzucone (idiomy speców przepływów).
- Defekty po odbiorze: brak; FE-G2 (603 s) dopisał specy Ustawień/Programu po świeżym odczycie przy wejściu — test „przywrócenie w innej karcie” czerwony bez poprawki.
- Wymagane testy i dowody: MD5 produkcji po każdej mutacji zgodne; 461/4919 → 461/4934 testów po fali i poprawkach bramki.
- Uwagi: scenariusz S23 odrzucony jako błąd briefu (strażnik w `afterNextRender`, wywołanie zewnętrzne bezwarunkowe) — świadoma luka w raporcie bramy. Haiku `xhigh` znowu przekroczył 300 tys. w briefie z wieloma scenariuszami (jak w próbie 2026-10-13) — brief testów przepływu dzielić od początku na „harness + fazy” i „sesja + wspólny kod błędu”.

### 1605-SCSS (+mechanik) (audyt 2 nowych `.scss` wariantu) — 2026-10-21
- Archetyp: Audyt SCSS — tylko odczyt.
- Stawka: niska.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): — (audyt); poprawka `mechanik` — Haiku 5.5 `low` (23 s).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` — przebieg 1 exit 3 po 65 s (próba powłoki w trybie odczytu), przebieg 2 (358 s) z zakazem powłoki i ścieżkami bezwzględnymi.
- Dopuszczone alternatywy: Sol `high` (oszczędzany przed bramką); Muse Spark `max` zablokowany.
- Powód wyboru: precedens 2210-SCSS; inna rodzina niż autor (Claude).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany (wrapper, 21:29 UTC).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: odrzucony technicznie (exit 3) — brief recenzji Gemini bez jawnego zakazu powłoki, wbrew `external-workers`.
- Rundy korekt: 1 (ponowienie briefu, nie wykonania).
- Czas do akceptacji: ~12 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1×P2 potwierdzone (kopia 1:1 `settings.strong-note` → mixin), 1×P3 odrzucone przez samego audytora.
- Defekty po odbiorze: brak; te same surowe deklaracje w 3 plikach sprzed PBI — poza zakresem, w raporcie.
- Wymagane testy i dowody: stylelint i prettier 0 po poprawce.

### 1605-G-FE (bramka końcowa FE, 3 przebiegi; poprawki FE-G1, FE-G2, FE-G3) — 2026-10-22
- Archetyp: Bramka końcowa high-stakes — recenzja całego diffu FE, tylko odczyt (BE bez diffu — bramki BE brak).
- Stawka: wysoka / high-stakes.
- Niepewność: średnia (po trzech recenzjach fal).
- Wykonawca (linia / model / native effort): poprawki — Claude / `wykonawca-opus` Opus 5.5 `xhigh` (FE-G1 573 s, FE-G3 494 s), `tester` Haiku 5.5 `xhigh` (FE-G2 603 s).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `max`, `-Mode review`, cały diff w jednym przebiegu: 418 s, 361 s, 365 s.
- Dopuszczone alternatywy: brak (reguła 6; limit = czekanie).
- Powód wyboru: reguła 6.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper, 22:23 / 22:52 / 23:13 UTC, bez limitu); Claude znany ZIELONY (hook, ~23:00 UTC: okno 0 %, tydzień 57 %).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: „niegotowe”, 1×P2 — `start()` nie czyta abonamentu na świeżo, więc przywrócenie w innej karcie albo wygaśnięcie w trakcie nie przełącza wariantu (rewizja pkt 2).
- Rundy korekt: 2 (FE-G1 + FE-G2 → przebieg 2: nowe 1×P2 — spóźnione 500 `GET /api/programs` po zmianie konta daje toast w nowej sesji, bo interceptor wycisza inną generację tylko dla 401 → FE-G3 → przebieg 3: 0 znalezisk, „gotowe do wydania”, pewność 0,90).
- Czas do akceptacji: ~57 min (22:23 → 23:20 UTC).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 2×P2 potwierdzone, 0 odrzuconych; przebieg 3 potwierdził też deltę dokumentu po 4c.
- Defekty po odbiorze: brak (PRE: FE 1.10.0, smoke Dark 24 zrzuty, konsola i sieć 0).
- Wymagane testy i dowody: każda poprawka z mutacją czerwoną i MD5 produkcji; lint, format, 461/4934, build 0.
- Uwagi: w odróżnieniu od 2210 bramka tu zarobiła na siebie — oba P2 to cross-cutting cykl życia (świeżość danych przy wejściu, koniec sesji w trakcie odczytu), których nie złapały R2 (Sol `high`) ani R3 (Gemini) na węższych diffach.

### 1605-4C (przegląd zgodności dokumentacji z kodem) — 2026-10-22
- Archetyp: Przegląd zgodności dokumentacja ↔ kod, tylko odczyt.
- Stawka: średnia.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): — (przegląd); poprawki — `mechanik` Haiku 5.5 `low` (pl/en + 2 literały spec, 68 s), `wykonawca` Sonnet 5.5 `high` + Figma MCP (4 ramki, 55 s), architekt (rewizja: 2 dopiski i 2 wiersze tabeli).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review` (344 s).
- Dopuszczone alternatywy: Gemini `flash-high` read — wykluczony (autor DOC-1/1K, ta sama rodzina); Sonnet read — wykluczony (architekt Claude dopisał wpisy rewizji); Muse zablokowany.
- Powód wyboru: przekwalifikowane z planu (Gemini) — jedyna rodzina niezależna od obu autorów dokumentacji; pula Codexa po bramce przebiegu 2, przed przebiegiem 3 — krótki przebieg `high`.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper, 23:02 UTC).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 2×P2 + 1×P3 rozbieżności — format recenzji zamiast macierzy twierdzeń z briefu.
- Rundy korekt: 1 (poprawki w napisach, specu, Figmie i rewizji; delta potwierdzona przebiegiem 3 bramki).
- Czas do akceptacji: ~18 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 2×P2 + 1×P3 potwierdzone, 0 odrzuconych.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: parzystość pl/en 1908/1908, 3 specy 65/65, zrzuty Figmy, przebieg 3 bramki.

### 1605-QAS-A (QA Sphere: przegląd 103 istniejących + nowe przypadki wejść do wariantu i fokusu po zamknięciu) — 2026-10-22
- Archetyp: QA Sphere — autor pliku podglądu (przegląd istniejących + luki) w funkcji high-stakes.
- Stawka: średnia (przypadki testowe, bez kodu; funkcja high-stakes).
- Niepewność: średnia (stany „anulowana + wolne miejsce” i „zakończona” osiągalne tylko przez kreator i operatora).
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access write` (771 s) + korekta K1 (940 s) + K2 wspólna z B (345 s).
- Recenzent (linia / model / native effort): Claude / `wykonawca` Sonnet 5.5 `high`, tylko odczyt (449 s).
- Dopuszczone alternatywy: autor — Muse Wonder `max` (skill: w funkcji high-stakes) zablokowany limitem tygodniowym; recenzent — Muse Wonder `max` (twarda reguła skilla: plik Gemini → Muse) zablokowany do 2026-10-26 00:00Z → ponowna kwalifikacja wg reguły 2 na Sonneta read (precedens 2210-QAS); Sol `high` oszczędzany (pula Codexa po trzech przebiegach bramki).
- Powód wyboru: jedyna dostępna linia autora z QA Sphere MCP poza Muse; recenzent z innej rodziny niż Gemini.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini znany (`agy /quota`, ~23:15 UTC: tydzień 55 %, 5 h 86 %); Muse zablokowany (429 z resetem 2026-10-26T00:00Z); Claude znany ZIELONY (hook, ~23:30 UTC: okno 5 %, tydzień 58 %).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 13 nowych, 3 aktualizacje, 2 retire, 98 keep, lint --strict 0/0; recenzja: 2×P1 potwierdzone (A08 — „kup 3, skonfiguruj 1” niewykonalne, bo kreator zapisuje wszystkie szkice naraz; 8 przypadków bez samowystarczalnego przygotowania konta), 6×P2 potwierdzone (984 `retire` → `update` — traciło jedyne pokrycie braku „Zmień metodę płatności”; 1060/1061 `keep` → `update` — cytowały regułę zmienioną rewizją; A09 z kontem bez subskrypcji zamiast zakończonej; A07/A10/A11/A12 dublowały plik B; A03 bez wartości kreatora; A11 z nazwami tokenów), P3 przyjęte (identyfikatory wewnętrzne, arkusz po anulowaniu, dławienie, 2 luki pokrycia → A14, A15), 0 obalonych.
- Rundy korekt: 2 (K1: 10 punktów; K2: tytuł A08 i przycisk „Zamknij” kreatora = krzyżyk „×” — autor sam doprecyzował, że etykieta jest tylko w `aria-label`).
- Czas do akceptacji: ~60 min (23:18 → ~00:02 UTC z wysyłką).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 2×P1 + 6×P2 + P3 potwierdzone, 0 odrzuconych (P2 o „wartościach pól kreatora” częściowo zbędne — domyślny szkic jest kompletny po nazwie, doprecyzowanie nieszkodliwe).
- Defekty po odbiorze: brak; `verify` 0 realnych różnic (autolinki, kolejność `requirements` — zbiory porównane).
- Wymagane testy i dowody: `qas.py lint --strict` z `--context`, kontrola w kodzie A08 (kreator, zakładka Program), motyw w „Język i wygląd”, `verify` po wysyłce (seq 1776–1790, aktualizacje 982/984/1015/1060/1061/1568, `[Removed]` 1572).
- Uwagi: błędy briefu architekta — „zmiana niescommitowana” (była w commicie przed QA), ZEB/1571 wskazany jako wzorzec zakupu z N programami (to konto seedowe + SQL), brak ostrzeżenia, że klucz `A01` nie istnieje w QA Sphere. Szablon briefu QA Sphere: (1) dopisać zakaz odsyłania między przypadkami po kluczu; (2) przed briefem sprawdzić osiągalność każdego stanu wymaganego przez kryteria (kreator atomowy, webhook operatora); (3) `[Removed]` tylko gdy utracone kroki ma kto pokryć.

### 1605-QAS-B (QA Sphere: przegląd 25 istniejących + nowe przypadki nakładki w wariancie „anulowana”) — 2026-10-22
- Archetyp: QA Sphere — autor pliku podglądu (przegląd istniejących + luki) w funkcji high-stakes.
- Stawka: średnia.
- Niepewność: średnia (409 i wynik po zamknięciu w toku wymagają zakończenia u operatora i dławienia sieci).
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access write` (714 s) + korekta K1 (738 s) + K2 wspólna z A (345 s).
- Recenzent (linia / model / native effort): Claude / `wykonawca` Sonnet 5.5 `high`, tylko odczyt (300 s).
- Dopuszczone alternatywy: jak 1605-QAS-A.
- Powód wyboru: jak 1605-QAS-A.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak 1605-QAS-A.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 17 nowych, 25 keep, lint --strict 0/0; napisy pl/en dosłownie zgodne z kodem (recenzent sprawdził wszystkie); recenzja: 2×P1 potwierdzone (13 przypadków odsyłało do „przypadku B01” — klucz nie istnieje w QA Sphere; B17 z nieistniejącą trasą `/panel/settings/account`), 6×P2 potwierdzone (webhook operatora w B08/B13; kolejność włączenia blokady w B09–B11; toast offline bez dosłownego napisu; wejście przez arkusz sekcji na 360 px; cztery sposoby zamknięcia w jednym kroku i brak wyniku 409 po zamknięciu → B18), P3: 4 przyjęte, 1 odrzucone (odmiana 22+ — nie defekt).
- Rundy korekt: 2 (K1: 10 punktów, nowy B18; K2: zastrzeżenie o webhooku w B18 — 409 nie zapisuje stanu w bazie).
- Czas do akceptacji: ~60 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 2×P1 + 6×P2 + 4×P3 potwierdzone, 1×P3 odrzucone.
- Defekty po odbiorze: brak; `verify` 0 realnych różnic (autolinki, „01.” po bloku, `\_` — artefakty odczytu, normalizacja doraźna).
- Wymagane testy i dowody: `qas.py lint --strict`, kontrola w kodzie (status 0 → `ERRORS.HTTP.OFFLINE`, `SKIP_ERROR_TOAST` w poleceniach abonamentu, brak zapisu stanu przy 409, domyślny szkic kreatora kompletny po nazwie), `verify` po wysyłce (seq 1791–1808).
- Uwagi: wariant „inny błąd po zamknięciu w toku” pominięty świadomie — DevTools nie przerywa deterministycznie żądania już wysłanego; ścieżkę pokrywają testy jednostkowe (FE-T1c/FE-TK). Recenzja Sonneta wyłapała w obu plikach po 2 P1 wykonalności, których lint nie widzi — przy autorze Gemini recenzja krzyżowa jest konieczna, nie formalna.

### 2297-CORE (+K-CORE, K2-CORE) (przejście na ekran 500: token oznaczonego GET, usługa, interceptor, znacznik SSR, inicjalizator) — 2026-10-22
- Archetyp: Logika przekrojowa FE z cichym błędem (cykl życia nawigacji, generacja żądań, SSR `RESPONSE_INIT`, nawigacja początkowa) — poza listą high-stakes reguły 6.
- Stawka: średnio-wysoka (wyrzucenie z widoku, pętla, spóźniona odpowiedź, otwarte przekierowanie przez `from`).
- Niepewność: wysoka (zachowanie silnika SSR i rutera Angulara 22 sprawdzane w `node_modules`).
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` Opus 5.5 `xhigh` — CORE 17 min, K-CORE 12,5 min, K2-CORE 4,3 min.
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `xhigh`, `-Mode review` (2297-R1); zgodność z dokumentacją — Sol `high` (2297-4C).
- Dopuszczone alternatywy: brak (Sonnet — reguła „za trudne dla Sonneta”; Codex nie przejmuje cichej logiki przekrojowej w porcjach ≤ 5 plików przy 7 plikach + 3 specach).
- Powód wyboru: logika przekrojowa z cichym błędem; lekcja 1605-G (spóźnione 500 po zmianie konta) wskazywała na cykl życia jako główne ryzyko.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany ZIELONY (hook, ~06:55 UTC: okno 4 %, tydzień 59 %).
- Pewność decyzji: średnia (brak wcześniejszych wyników tego archetypu).
- Wynik pierwszego podejścia: 4 nowe pliki + 3 specy, 3 zmienione + specy, 92/92 w zakresie, mutacje a–h czerwone; wykonawca sam zgłosił 6a (warunek „już na ekranie 500” czytał `router.url` zamiast celu trwającej nawigacji → cisza przy wyjściu z `/blad-serwera`) i 6c (SSR: przekierowanie strażnika + 500 → ograniczenie).
- Rundy korekt: 2 (K-CORE: 6a + F2 z R1 — `browserUrl` przy błędzie w trakcie nawigacji, 72/72, mutacje m1–m4 czerwone; K2-CORE: `Cache-Control: no-store` dla ścieżki SSR oznaczonego GET z 4C, spec SSR).
- Czas do akceptacji: ~67 min (07:12 → ~08:19 UTC z pełnym testem i buildem).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R1 — 1×P2 potwierdzone (F2), 1×P2 odrzucone (F3 `void navigateByUrl` — idiom repo, ruter łapie odrzucenia); 4C — 1×P2 `kod odbiega` potwierdzone (`no-store`); własne 6a potwierdzone.
- Defekty po odbiorze: brak do bramy (PRE po wdrożeniu).
- Wymagane testy i dowody: specy z mutacjami czerwonymi; pełne lint 0, format 0, test 465/5018, build OK; V1 w przeglądarce (2297-V1).
- Uwagi: błąd briefu architekta w K2 — twierdził, że `server-error-page.spec.ts` ma już blok `RESPONSE_INIT`; wykonawca dostosował się sam. Ograniczenia zostawione do decyzji przy oznaczaniu pierwszego widoku: SSR przekierowanie strażnika + 500, `replaceUrl` przerwanej nawigacji nie przechodzi na ekran 500.

### 2297-SSR (+K-SSR) (middleware Expressa: ekran 500 przy awarii renderu SSR) — 2026-10-22
- Archetyp: Pojedynczy middleware serwera SSR + spec z atrapą silnika.
- Stawka: średnia.
- Niepewność: niska (wyrocznia: spec z atrapą `engine.handle`).
- Wykonawca (linia / model / native effort): Claude / `wykonawca` Sonnet 5.5 `high` — SSR 4,3 min, K-SSR 2,8 min.
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `xhigh`, `-Mode review` (2297-R1).
- Dopuszczone alternatywy: Codex `gpt-6.1-sol` `high` (≤ 5 plików) — oszczędzany na recenzję R1 i 4C.
- Powód wyboru: krótki brief jednej warstwy z jednoznaczną wyrocznią.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany ZIELONY (hook, ~06:55 UTC).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: `server-error-fallback.ts` + spec 16 testów, mutacje a/b/c czerwone, wpięcie w `server.ts`.
- Rundy korekt: 1 (K-SSR: F1 z R1 — log przekazywał obiekt wyjątku z możliwym query stringiem → lokalne `describeError` z redakcją `?[…]`, 20/20, mutacja czerwona).
- Czas do akceptacji: ~47 min (07:13 → ~08:00 UTC, z czekaniem na R1).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1×P2 potwierdzone (F1), 0 odrzuconych.
- Defekty po odbiorze: brak do bramy.
- Wymagane testy i dowody: spec 20/20, pełne test/build, V1 (podmiana odpowiedzi dokumentu na wynik middleware'u).

### 2297-DOC (dokumenty ekranów 500 i 404 + WP przejścia na ekran 500 + 2 indeksy) — 2026-10-22
- Archetyp: Dokumentacja produktowa — nowe dokumenty `do-weryfikacji` opisujące istniejący kod i decyzje właściciela.
- Stawka: średnia.
- Niepewność: średnia (ekrany #1880/#1881 bez dokumentów źródłowych — opis z kodu i Figmy).
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access write` (565 s).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review` (2297-4C); lektura architekta.
- Dopuszczone alternatywy: Codex Sol `medium`, `wykonawca` Sonnet; Muse zablokowany do 2026-10-26.
- Powód wyboru: precedens 1605-DOC przyjęty; osobna pula, Codex oszczędzany na R1/4C.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini znany (`agy /quota`, ~06:50 UTC: tydzień 49 %, 5 h 100 %); Muse zablokowany (429, reset 2026-10-26T00:00Z).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 3 nowe dokumenty + 2 indeksy, front matter i linki poprawne; jedno zdanie („wejście po awarii” sugerowało `from` w pasku) poprawione przez architekta; wykonawca słusznie zgłosił etykietę 404 „Przejdź do panelu” dla gościa i lukę Konta/Zakupu.
- Rundy korekt: 0 przez autora; architekt: 1 zdanie po DOC, 1 zdanie po R1 (F2), 5 doprecyzowań WP po 4C.
- Czas do akceptacji: ~70 min (07:11 → ~08:20 UTC z 4C).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 4C — 4×P2 w WP potwierdzone (status 0 na serwerze, granice renderu zastępczego, wyciszanie tylko odczytów 1a, prerender), 0 odrzuconych.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: diff dokumentacji przeczytany, macierz 4C.

### 2297-V1 (dowód w przeglądarce: znacznik 500, adres w pasku, „Spróbuj ponownie”, „Wstecz”, F5) — 2026-10-22
- Archetyp: Worker przeglądarkowy — dowód z podmianą odpowiedzi dokumentu (Playwright `page.route`), bez zmian w repo.
- Stawka: niska (dowód, nie kod).
- Niepewność: średnia (czy podmiana dokumentu w Playwright MCP odda dokładnie odpowiedź middleware'u).
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access write` (Playwright MCP wymaga zapisu w allow-liście `agy`), 446 s.
- Recenzent (linia / model / native effort): — (architekt obejrzał zrzuty i log konsoli).
- Dopuszczone alternatywy: Codex z Playwright MCP (oszczędzany na R1/4C); `browser-check` nie podmienia odpowiedzi; `pwcli` tylko w linii Muse (zablokowana).
- Powód wyboru: jedyna dostępna linia z Playwright MCP poza oszczędzanym Codexem.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini znany (`agy /quota`, ~06:50 UTC).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: S0–S7 PASS; bez NG05xx/NG0500 (tylko zastane NG02960 logo i 502 API bez BE); zrzuty 500 Light/Dark pod `/o-nas`.
- Rundy korekt: 0.
- Czas do akceptacji: ~10 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): —.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: zrzuty w `_robocze/2297-v1/` obejrzane, `location.href` przed każdym zrzutem.
- Uwagi: błąd briefu — zakładał `h1` na `/o-nas` (strona jest pustym placeholderem); bez skutku. Gemini z Playwright MCP wymaga `-Access write` — tryb read blokuje narzędzia MCP.

### 2297-R1 (recenzja fali 1 FE: CORE + SSR, cały diff) — 2026-10-22
- Archetyp: Recenzja fali — logika przekrojowa FE + middleware SSR, tylko odczyt.
- Stawka: średnio-wysoka.
- Niepewność: wysoka.
- Wykonawca (linia / model / native effort): —.
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `xhigh`, `-Mode review` z `-BriefFile` (zakres w briefie — wrapper nie dodaje wtedy `--uncommitted`), 544 s.
- Dopuszczone alternatywy: Gemini `flash-high` read (niższa klasa do cyklu życia); Muse zablokowany.
- Powód wyboru: inna rodzina niż Claude; lekcja 1605 — Sol `high` przeoczył cykl życia, który złapał `max`; `xhigh` jako kompromis z pulą Plus.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper, ostatni przebieg 2026-10-21 23:19Z bez limitu).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 3×P2 — F1 log obiektu wyjątku (defekt), F2 adres w pasku przy błędzie w trakcie nawigacji (defekt), F3 `void navigateByUrl` (odrzucone).
- Rundy korekt: 1 (K-SSR, K-CORE).
- Czas do akceptacji: ~25 min (07:32 → ~07:57 UTC z korektami).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 2×P2 potwierdzone, 1×P2 odrzucone (idiom repo ×37, ruter i `@angular/ssr` łapią odrzucenia); 6a z raportu CORE potwierdzone niezależnie przez architekta.
- Defekty po odbiorze: brak do bramy.
- Wymagane testy i dowody: mutacje czerwone w korektach.

### 2297-4C (przegląd zgodności dokumentacji z kodem) — 2026-10-22
- Archetyp: Przegląd zgodności dokumentacja ↔ kod, tylko odczyt.
- Stawka: średnia.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): — (przegląd); poprawki — architekt (5 doprecyzowań WP), `wykonawca-opus` (K2-CORE).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review` (444 s).
- Dopuszczone alternatywy: `wykonawca` Sonnet read — wykluczony (architekt Claude poprawiał dokumenty); Gemini — autor DOC; Muse zablokowany.
- Powód wyboru: jedyna rodzina niezależna od autorów dokumentacji (Gemini, architekt Claude) i kodu (Claude).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper, 07:41 UTC, bez limitu).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 5×P2 — 4 w WP (2× `brak w dokumencie`, 2× `dokument nieaktualny`), 1× `kod odbiega` (`no-store` dla oznaczonego GET w SSR); ekrany, teksty PL/EN, front matter i linki zgodne; macierz w formacie z briefu.
- Rundy korekt: 1.
- Czas do akceptacji: ~18 min (08:01 → ~08:19 UTC).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 5×P2 potwierdzone, 0 odrzuconych.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: delta WP przeczytana, K2-CORE ze spekiem, pełne test/build.

### 2297-QAS (QA Sphere: przegląd 14 istniejących stron błędów + przypadki przejścia na ekran 500, w większości automatyczne) — 2026-10-22
- Archetyp: QA Sphere — autor pliku podglądu (przegląd istniejących + luki), poza high-stakes; przypadki automatyczne wskazujące testy Vitest (decyzja D6: na PRE nie da się wywołać awarii serwera).
- Stawka: średnia (przypadki testowe, bez kodu).
- Niepewność: średnia (pierwszy zestaw z przewagą przypadków `Automated` wskazujących konkretne testy).
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access write` (670 s) + korekta K1 (814 s).
- Recenzent (linia / model / native effort): Claude / `wykonawca` Sonnet 5.5 `high`, tylko odczyt (257 s).
- Dopuszczone alternatywy: autor — Muse Spark `max` (skill, poza high-stakes) zablokowany limitem tygodniowym; recenzent — Muse (twarda reguła skilla: plik Gemini → Muse) zablokowany do 2026-10-26 00:00Z → ponowna kwalifikacja wg reguły 2 na Sonneta read (precedens 2210/1605-QAS); Codex Sol `high` dopuszczony (5 h 18 %, tydzień 48 % po R1/4C), nie wybrany — Sonnet ma lokalne wyniki tego archetypu.
- Powód wyboru: jedyna dostępna linia autora z QA Sphere MCP poza Muse; recenzent z innej rodziny niż Gemini z potwierdzonymi P1 wykonalności w 1605-QAS.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini znany (`agy /quota` ~06:50 UTC, potem 3 przebiegi bez limitu); Muse zablokowany (429, reset 2026-10-26T00:00Z); Claude znany ZIELONY (hook, ~08:40 UTC: okno 23 %, tydzień 61 %).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 11 nowych (1 ręczny HTTP 200 przy bezpośrednim wejściu, 10 `Automated`), 14 keep, lint --strict 0/0, wszystkie nazwy testów istniały; recenzja: 2×P1 potwierdzone (w 7 przypadkach polecenie `ng test --include` uruchamiało 1 z 2–3 wskazanych speców — zielony wynik bez części testów; P5 obiecywał zachowanie danych formularza i brak ponowienia bez testu, który to sprawdza), 3×P2 potwierdzone („gałąź robocza” zamiast `main`/commit; brak testu wykluczeń `/api`/`/blad-serwera` w P2; `no-store` w P3 bez testu), 5×P3 przyjęte (żargon kodu w krokach, luka 4xx na oznaczonym GET → nowy P12, 792/793 → `update` z wymaganiem #2297, test generacji w P7, „Disable cache” w P1), 0 obalonych.
- Rundy korekt: 1 (K1: 10 punktów; architekt sprawdził skryptem: pliki w poleceniu = pliki w warunku, nazwy testów = szablony `it.each`, brak żargonu w krokach).
- Czas do akceptacji: ~33 min (08:24 → 08:57 UTC z wysyłką).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 2×P1 + 3×P2 + 5×P3 potwierdzone, 0 odrzuconych.
- Defekty po odbiorze: brak; `verify` 4 różnice — wszystkie znane artefakty odczytu (autolink, „01.”, `\_`).
- Wymagane testy i dowody: `qas.py lint --strict` z `--context`, kontrola skryptowa K1, `verify` po wysyłce (folder 188, seq 1809–1820, aktualizacje 792/793).
- Uwagi: błąd briefu architekta — kazał grupować przypadek automatyczny po regule WP (2–3 speki), a nie powiedział, że polecenie ma mieć `--include` na każdy plik; stąd masowy P1. Szablon briefu QA Sphere dla przypadków `Automated`: (1) polecenie z `--include` dla każdego wskazanego pliku; (2) każde zdanie `expected` musi mieć asercję we wskazanym teście; (3) stan kodu = `main` + commit; (4) identyfikatory kodu tylko w warunku wstępnym.

### 1606-BE-1 (BE-1…1f + BE-1g) (fundament BE zakupu odnowienia: migracja rodzaju próby, kontekst odnowienia, start zakupu, kontroler) — 2026-10-22
- Archetyp: Backend — zakup subskrypcji przez operatora płatności (zgoda, kwota, guard, jedna oczekująca próba, idempotencja) + migracja danych.
- Stawka: wysoka / high-stakes.
- Niepewność: średnia (mechanika zakupu z konta #2705 jako wzorzec; nowy rodzaj próby w istniejących odczytach).
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` Opus 5.5 `xhigh` — łańcuch BE-1 → przekazanie przy progu kontekstu → BE-1b (plan reszty) → przekazanie → BE-1c, 1d, 1e, 1f (każdy jedna jednostka); BE-1g (awans 9 typów współdzielonych, tylko namespace) — `mechanik` Haiku 5.5 `low`.
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review` (292 s).
- Dopuszczone alternatywy: wykonawca przy CZERWONYM — Muse Wonder Full `max` (zablokowany do 2026-10-26 00:00Z); recenzent — Muse Wonder Full `max` (zablokowany).
- Powód wyboru: pliki niezmiennika płatności i migracja (reguła 2, lista Zebrani).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany ZIELONY (hook, ~07:30 UTC: okno 28 %, tydzień 62 %); Codex nieznany (wrapper, 10:57 UTC); Muse zablokowany (429, reset 2026-10-26T00:00Z).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: pierwszy przebieg doszedł do progu 300 tys. po planie i migracji — dalszą pracę podzielono na krótkie ogniwa z planem przekazania; każde ogniwo odebrane w 1. przejściu (build 0/0, testy zielone).
- Rundy korekt: 0 (R-BE-1 bez znalezisk).
- Czas do akceptacji: ~75 min (≈ 09:45 → 11:02 UTC z recenzją).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 / 0.
- Defekty po odbiorze: brak w plikach BE-1; dwa blokery domknięcia (indeksy unikalne zgody cyklicznej i instrumentu `pm_…`) wyszły w BE-2a — luka briefu architekta („bez zmian” dla zapisów współdzielonych z zakupem programu).
- Wymagane testy i dowody: `dotnet build` 0/0, filtry testów; BE-T; test dymny w sandboksie; G-BE-1 bez znalezisk.
- Uwagi: podział po pierwszym przekazaniu na ogniwa ≤ 1 jednostki zadziałał — żadne ogniwo nie wróciło z korektą.

### 1606-FE-L1 (+FE-L1-K) (przepływ zakupu odnowienia: Stripe, kolejność sprawdzeń, odpytywanie, generacja sesji; serwis, DTO, enumy, czyste funkcje) — 2026-10-22
- Archetyp: FE — przepływ płatności (niezmiennik: potwierdzenie u operatora, generacja sesji, kolejność sprawdzeń).
- Stawka: wysoka / high-stakes.
- Niepewność: średnia (wzorzec `program-purchase-flow` #2705; nowe: zapisana karta, wznowienie próby).
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` Opus 5.5 `xhigh` (FE-L1; FE-L1-K świeży agent).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review` (273 s).
- Dopuszczone alternatywy: jak 1606-BE-1.
- Powód wyboru: logika płatności z cichym błędem.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak 1606-BE-1 (Codex nieznany, 10:11 UTC).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zachowanie zgodne z kontraktem; recenzja „niepoprawny”: 1×P1 (Stripe.js wczytywany po `200` startu bez kontroli generacji sesji → `confirmPayment` obciąża kartę konta A po zmianie konta) + 1×P2 (destruktor zrywa wysłany odczyt statusu → skutki rozliczenia nie trafiają do singletonów).
- Rundy korekt: 1 (FE-L1-K: 2 punkty recenzji + 3 architekta).
- Czas do akceptacji: ~2 h (z korektą).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1×P1 + 1×P2 potwierdzone, 0 odrzuconych.
- Defekty po odbiorze: DEF-1 (FE-T1b: przy `publishableKey === null` przepływ wołał `confirmPayment`) — łatka jednolinijkowa architekta; G-FE-1 P1/P2 (sekret PaymentIntent w adresie po przekierowaniu banku; wznowiona próba z formularzem) — luki projektu architekta, nie briefu FE-L1 → FE-G1.
- Wymagane testy i dowody: FE-T1a/b/c + FE-T1-K, test dymny (zapisana karta, 3DS nową kartą, wznowienie), bramka FE.

### 1606-FE-V (+FE-V-K1) (komponenty prezentacyjne wariantu zakupu, przeniesienie pola karty i zgody, napisy pl/en) — 2026-10-22
- Archetyp: Frontend UI / Figma — widoki bez niezmiennika w funkcji high-stakes.
- Stawka: średnia.
- Niepewność: niska (precedens 1605-FE-V).
- Wykonawca (linia / model / native effort): Claude / `wykonawca` Sonnet 5.5 `high` + Figma MCP (FE-V; FE-V-K1 po uwadze właściciela).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (877 s).
- Dopuszczone alternatywy: Codex z potwierdzonym MCP Figmy (pula zarezerwowana na bramki); recenzent Sol `high`.
- Powód wyboru: ekran z makiety — linia z Figma MCP; lokalne wyniki 1605-FE-V.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany ZIELONY (hook, ~07:30 UTC); Gemini nieznany (wrapper, 10:11 UTC).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: zaakceptowano; recenzja „poprawny” 0,98, bez P0–P2; wskazała 2 błędne przesłanki briefu (warunek znacznika „wszystkie wrócą” przy miejscach > czekających; `focusCard()` przy polu w ramce operatora) — wykonawca obszedł je już sam.
- Rundy korekt: 1 (FE-V-K1 — właściciel: wiersze „✓ wróci” w karcie przywracania brzydkie; status po prawej, wyciszony, bez ikon wg makiety; zrzuty 8/8).
- Czas do akceptacji: ~1 h (FE-V); FE-V-K1 ~15 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 / 0 (+2 trafne uwagi do briefu).
- Defekty po odbiorze: A-SCSS 1×P2 + 3×P3 (kopia `muted-note` zamiast mixinu) → `mechanik`.
- Wymagane testy i dowody: specy z AXE (FE-T2), browser-check matrix 12/12, zrzuty karty 8/8.

### 1606-D (D-1a, D-1b) (datowane rewizje 5 dokumentów: UI zmiany abonamentu, UI ustawień, INT płatności cyklicznych, WP zgód, PB odnowienia) — 2026-10-22
- Archetyp: Dokumentacja produktu — rewizje z treścią podyktowaną w briefie.
- Stawka: średnia (źródło prawdy).
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access write` (506 s, 469 s, równolegle).
- Recenzent (linia / model / native effort): architekt (zgodność z decyzjami) + 4c Codex / `gpt-6.1-sol` `high`.
- Dopuszczone alternatywy: `wykonawca` Sonnet (pula Claude); Muse zablokowany.
- Powód wyboru: tekst bez niezmiennika, pula Claude oszczędzana na pliki niezmiennika.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany (wrapper, 09:50 UTC).
- Pewność decyzji: niska (brak lokalnych wyników rewizji Gemini).
- Wynik pierwszego podejścia: przesłanka briefu obalona słusznie — „nowe okno gwarancji nigdy, także przy braku subskrypcji” przeczyło zatwierdzonemu RB-ABONAMENT-ZWROT; plan i pkt 15 rewizji poprawione przez architekta.
- Rundy korekt: 1 (architekt: pkt 15, wiersz tabeli; później dopiski architekta z odbioru BE-2a-K i FE-G1).
- Czas do akceptacji: ~30 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 4c — 3 luki w treści rewizji (UI: stan niewczytanego pola karty, rytm i budżet odpytywania; INT: 400 a 409 dla kwoty, 502 `PAYMENT_PROVIDER_ERROR`) potwierdzone i uzupełnione przez architekta; 0 sprzeczności z decyzjami.
- Defekty po odbiorze: luki opisane wyżej (zachowania dodane w falach 2–3, po rewizji).
- Wymagane testy i dowody: tabela napisów PL | EN zgodna z kodem (4c: 42 wiersze, 108 brzmień).

### 1606-FIG-1 (+FIG-1b, FIG-1c) (zgoda, szybkie wybory, stany „Zmień kartę” i „mniej miejsc”, warianty Dark) — 2026-10-22
- Archetyp: Figma — uzupełnienie makiety do decyzji.
- Stawka: niska.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Claude / `wykonawca` Sonnet 5.5 `high` + Figma MCP (FIG-1 → przekazanie przy progu → FIG-1b → FIG-1c).
- Recenzent (linia / model / native effort): architekt na zrzutach (inne rodziny bez Figmy).
- Dopuszczone alternatywy: brak (Figma MCP).
- Powód wyboru: precedens 1605-FIG-1.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany ZIELONY (hook, ~07:30 UTC).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: wymagane korekty — w ramkach „mniej miejsc” szybkie wybory liczone od bieżącej wartości zamiast od startowej i „Zostaną” zamiast „Pozostaną”.
- Rundy korekt: 1 (FIG-1c).
- Czas do akceptacji: ~1 h.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 2 potwierdzone (architekt), 0 odrzuconych.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: `get_screenshot` ramek, zmienne związane.

### 1606-BE-2 (2a, 2a-K, 2b, 2c) (domknięcie zakupu odnowienia z przywróceniem programów, status, webhook, cykl uzgadniania, retencja) — 2026-10-22
- Archetyp: Backend — aktywacja subskrypcji i przywracanie programów (naliczanie wartości), idempotencja domknięcia.
- Stawka: wysoka / high-stakes.
- Niepewność: wysoka (indeksy unikalne tabel współdzielonych z zakupem programu, rodzaj próby w webhooku).
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` Opus 5.5 `xhigh` ×4, sekwencyjnie (wspólne repozytorium prób).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review` (168 s).
- Dopuszczone alternatywy: jak 1606-BE-1 (Muse Wonder Full `max` od 2026-10-26).
- Powód wyboru: niezmiennik przywracania i domknięcia.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany ZIELONY (hook, ~11:00 UTC: okno 1 %, tydzień 68 %); Codex nieznany (wrapper, 12:15 UTC).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: BE-2a zielone, ale raport wykonawcy sam wskazał dwa blokery domknięcia rodzaju 2 (druga aktywna zgoda cykliczna; ta sama karta = konflikt indeksu instrumentu) — luka briefu architekta.
- Rundy korekt: 1 (BE-2a-K: wycofanie poprzednich zgód cyklicznych, instrument „pobierz albo wstaw”, 2 testy regresji czerwone bez poprawki; odebrane w 1. przejściu).
- Czas do akceptacji: ~2 h (2a → 2c z korektą).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 / 0.
- Defekty po odbiorze: brak (G-BE-1 bez znalezisk).
- Wymagane testy i dowody: build 0/0, 3879/3879 filtra; DYMNY-2 (zapisana karta: próba COMPLETED, 3 programy przywrócone, `FirstChargeAt` bez zmian, jedna zgoda, brak nowej roli) i DYMNY-3 (3DS nową kartą z wznowieniem próby).
- Uwagi: raport Opusa zgłaszający blokery zamiast obchodzić je po cichu — klauzula „co błędne w specyfikacji” zarobiła na siebie.

### 1606-FE-L2 (+FE-L2-K) i 1606-FE-E (kontener nakładki w wariancie zakupu; wejścia z Ustawień i zakładki Program) — 2026-10-22
- Archetyp: Frontend — składanie kontenera bez niezmiennika (logika w FE-L1) + wejścia.
- Stawka: średnia.
- Niepewność: średnia (kontener blisko limitu `max-lines`).
- Wykonawca (linia / model / native effort): Claude / `wykonawca` Sonnet 5.5 `high` — FE-L2 (325 tys., 56 wywołań), FE-L2-K (świeży, 162 tys.), FE-E (przekwalifikowany z Codex `gpt-6.1-sol` `medium`: 8 plików > 5 i pula Codexa na bramki).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read`, jeden przebieg na oba (794 s).
- Dopuszczone alternatywy: `wykonawca-opus`; recenzent Sol `high` (pula na bramki).
- Powód wyboru: precedens 1605 (przepływ ≠ kontener ≠ wejścia).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany ZIELONY (hook, ~11:00 UTC); Gemini nieznany (wrapper, 11:42 UTC).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: FE-L2 — zachowanie zgodne, ale `sonarjs/max-lines` 1104 > 1000 (brief zakazał wydzielania — błąd briefu); FE-E — zaakceptowane, architekt dopisał jedną regułę SCSS spoza listy briefu.
- Rundy korekt: 1 (FE-L2-K: pochodne do `RenewalOverlayView`, kontener 962) + poprawka `mechanik` 2 testów konsumenta (`subscription-and-invoices-resume`) — brief kontenera nie kazał uruchomić speców konsumentów.
- Czas do akceptacji: ~1,5 h.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 / 0 („poprawny” 0,98); 2 zmyślone nazwy w opisie recenzji.
- Defekty po odbiorze: G-FE-1 P2 — wznowiona próba renderowała formularz (luka projektu architekta) → FE-G1.
- Wymagane testy i dowody: 5018/5018, browser-check matrix 12/12 + flows (przywrócenie, mniej miejsc, arkusz) z PASS.

### 1606-DYMNY (DYMNY-1…3) (test dymny zakupu odnowienia w sandboksie operatora, ręczne odtworzenie) — 2026-10-22
- Archetyp: Weryfikacja w przeglądarce — worker z Playwright MCP (`--isolated`), płatność testowa.
- Stawka: wysoka (dowód ścieżki płatności przed deployem).
- Niepewność: średnia (lokalny BE z operatorem, zegar testowy klienta).
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access write` (566 s, 741 s, 562 s).
- Recenzent (linia / model / native effort): architekt — stan bazy, Stripe CLI, zrzuty.
- Dopuszczone alternatywy: Muse Spark `max` z `pwcli` (zablokowany); Codex z MCP (pula na bramki).
- Powód wyboru: jedyna dostępna linia z Playwright poza Claude'em.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany (wrapper, 12:27 UTC).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: DYMNY-1 — przesłanka obalona słusznie (lokalny BE bez operatora — błąd architekta); worker czytał sekcję operatora w pliku konfiguracji → w kolejnych briefach jawny zakaz.
- Rundy korekt: 2 (DYMNY-2: zapisana karta zielona, 3DS przerwany przeładowaniem `ng serve` po łatce architekta w trakcie; DYMNY-3: 3DS nową kartą z wznowieniem próby — zielony).
- Czas do akceptacji: ~50 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): —.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: zrzuty, wiersze prób/subskrypcji/zgód/programów w bazie, metadata `kind` w sandboksie, webhook 200; sprzątanie subskrypcji dymnych.
- Uwagi: lekcje — sprawdzić konfigurację BE przed briefem; żadnych edycji kodu aplikacji w trakcie testu na `ng serve`.

### 1606-BE-T (BE-T1 cz. 1–3, BE-T2a, BE-T2b cz. 1–3, BE-T-K) (xunit: kontekst, start, domknięcie, przywracanie, status, webhook, retencja) — 2026-10-22
- Archetyp: Testy BE (jednostkowe + SQL na SQLEXPRESS).
- Stawka: wysoka (oracle niezmiennika).
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): Claude / `tester` Haiku 5.5 `xhigh` — 8 przebiegów (podział po przekazaniach przy progu).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (599 s).
- Dopuszczone alternatywy: recenzent Sol `high` (pula na bramki), Muse Wonder `max` (zablokowany).
- Powód wyboru: linia `tester` po próbie z 2026-10-13.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy ŻÓŁTY (hook, ~14:00 UTC: tydzień 74 % przy 64 % upływu); Gemini nieznany (wrapper, 14:09 UTC).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: każdy przebieg odebrany (0 defektów produkcyjnych); luka BE-T2a — czekające seedowane tylko z `SEAT_REDUCTION` (główna ścieżka = `SUBSCRIPTION_EXPIRED`) → dopisane do BE-T2b.
- Rundy korekt: 1 (BE-T-K, K1–K6).
- Czas do akceptacji: ~2,5 h.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1×P1 (słaba asercja klucza publicznego) + 1×P2→P3 + 1×P2→P3 + 1×P3 potwierdzone; 1×P3 obalone (zdublowany JSON webhooka).
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: pełne `dotnet test` 8309/8309, 0 pominiętych; mutacje K2/K5 czerwone.
- Uwagi: błąd briefu — dosłowna mutacja K2 nie kompilowała się (S1481/CS9113).

### 1606-FE-T (FE-T1a/b/c, FE-T2a, FE-T2b + C1/C2, FE-T1-K, FE-T2-K) (Vitest + AXE: przepływ, czyste funkcje, komponenty, kontener, wejścia) — 2026-10-22
- Archetyp: Testy FE (harness przepływu płatności, AXE).
- Stawka: wysoka (oracle niezmiennika przepływu).
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): Claude / `tester` Haiku 5.5 `xhigh` (7 przebiegów + 2 korekty; FE-T2b przekazanie po 327 tys. → C1 ∥ C2).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` — R-FE-T-2 (575 s), R-FE-T-1 (865 s po ponowieniu; 1. przebieg exit 3 — próba powłoki, zakaz dopisany).
- Dopuszczone alternatywy: Sol `high` (pula na bramki).
- Powód wyboru: linia `tester`; recenzent innej rodziny.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany ZIELONY → ŻÓŁTY (hook, 12:00–14:00 UTC); Gemini nieznany (wrapper, 13:16 UTC).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: odebrane; FE-T1b wykrył defekt produkcyjny DEF-1 (FE-L1); recenzje „niewystarczające” (0,92 i 0,95).
- Rundy korekt: 1 na zestaw (FE-T1-K, FE-T2-K).
- Czas do akceptacji: ~2,5 h.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R-FE-T-1: 2×P1 (fałszywa zieleń `≥ 1`, brak asercji) + 1×P1→P2 + 2×P2 + 2×P3 potwierdzone, 1×P3 odrzucone; R-FE-T-2: 1×P1→P2 + 1×P1 (brak stanu Pending — luka briefu) + 3×P2 + 2×P3 potwierdzone.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: pełne `npm test` 5416/5416, lint 0, build OK.

### 1606-SCSS (audyt SCSS wariantu zakupu) — 2026-10-22
- Archetyp: Audyt SCSS, tylko odczyt.
- Stawka: niska.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): poprawki — `mechanik` Haiku 5.5 `low` (24 wywołania).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (419 s).
- Dopuszczone alternatywy: Spark `max` (zablokowany).
- Powód wyboru: SCSS pisał Sonnet — inna rodzina.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany (wrapper, 13:23 UTC).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 1×P2 (kopia `muted-note`) + 3×P3.
- Rundy korekt: 1.
- Czas do akceptacji: ~20 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1×P2 + 3×P3 potwierdzone, 0 odrzuconych.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: stylelint/prettier 0, build w walidacji fali.

### 1606-G-FE (bramka końcowa FE, 2 przebiegi; poprawka FE-G1 + korekta) — 2026-10-22
- Archetyp: Bramka końcowa high-stakes — cały diff FE (156 plików), tylko odczyt.
- Stawka: wysoka / high-stakes.
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): poprawka — Claude / `wykonawca-opus` Opus 5.5 `xhigh` (FE-G1 + korekta przez kontynuację tego samego agenta).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `max`, `-Mode review` (568 s, 665 s).
- Dopuszczone alternatywy: brak (reguła 6; przy limicie decyzja właściciela 5 — Spark `max` po resecie Muse).
- Powód wyboru: reguła 6.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper, 13:57 / 14:37 UTC).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: 1×P1 (sekret PaymentIntent zostaje w adresie po pełnym przekierowaniu banku) + 1×P2 (wznowiona próba renderuje formularz w Confirming/Pending).
- Rundy korekt: 1 (FE-G1: stałe parametrów powrotu, czyszczenie jedną nawigacją, `resumedWaiting`; korekta: 409 oczekiwania = wznowienie, własny klucz napisu) → przebieg 2: 0 znalezisk.
- Czas do akceptacji: ~55 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1×P1 + 1×P2 potwierdzone, 0 odrzuconych.
- Defekty po odbiorze: 0 przy wdrożeniu PRE (2026-10-22 17:38 UTC: FE 1.12.0, BE 1.14.0, nowe trasy aktywne); retest testera w toku.
- Wymagane testy i dowody: mutacje czerwone; lint 0, format, 5416/5416, build OK.
- Uwagi: oba znaleziska to luki projektu architekta (powrót z przekierowania, wznowienie bez sekcji zamówienia), których nie złapały recenzje fal na węższych diffach.

### 1606-G-BE (bramka końcowa BE) — 2026-10-22
- Archetyp: Bramka końcowa high-stakes — cały diff BE, tylko odczyt.
- Stawka: wysoka / high-stakes.
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): —.
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `max`, `-Mode review` (616 s).
- Dopuszczone alternatywy: brak (reguła 6).
- Powód wyboru: reguła 6.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper, 14:48 UTC).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: brak defektów (testy w piaskownicy niewykonane — pełne `dotnet test` architekta 8309/8309).
- Rundy korekt: 0.
- Czas do akceptacji: ~10 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 / 0.
- Defekty po odbiorze: 0 przy wdrożeniu PRE (2026-10-22 17:38 UTC: FE 1.12.0, BE 1.14.0, nowe trasy aktywne); retest testera w toku.
- Wymagane testy i dowody: build 0 ostrzeżeń, 8309/8309.

### 1606-QAS (QA Sphere — plik podglądu, recenzja krzyżowa, korekty K1–K5) — 2026-10-22
- Archetyp: QA Sphere w funkcji high-stakes — autor pliku podglądu (32 nowe przypadki, 7 aktualizacji, 83 wpisy `review`).
- Stawka: średnia (przypadki testowe funkcji high-stakes, bez kodu).
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access write` (generator 1005 s; K1 1776 s; K2 1134 s; K3 722 s; K4 650 s — praca wykonana, końcowe 503 wrappera; K5 845 s).
- Recenzent (linia / model / native effort): Claude / `wykonawca` Sonnet 5.5 `high`, tylko odczyt (precedens #1605) + automatyczne porównanie cytatów z `pl.json`/`en.json` (skrypt architekta).
- Dopuszczone alternatywy: autor Muse Wonder `max` — zablokowany (429 tygodniowy do 2026-10-26 00:00Z); recenzent Sol `high` — pula Codexa zarezerwowana na bramki i 4c.
- Powód wyboru: reguła 8 (Wonder `max` dla QA Sphere w high-stakes) niedostępna → Gemini write wg skilla QA Sphere; recenzja innej rodziny.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Muse zablokowany (429, 2026-10-20); Gemini nieznany (wrapper); Claude znany (hook).
- Pewność decyzji: niska.
- Wynik pierwszego podejścia: recenzja — „plik wymaga korekty” (pewność 0,85): błędy w 11 przypadkach (szybkie wybory, fokus/komunikat danych do faktury, okno zwrotu na świeżym koncie, przypadki płatności na koncie demo bez karty, SQL przywracający hurtowo). Odbiór K1 przez architekta: cytaty nieistniejące w aplikacji (także w R01–R03, które recenzent oznaczył jako sprawdzone), błędny komunikat R23.
- Rundy korekt: 5 (K1: 12 punktów faktów; K2: konta świeże z `/kup`, SQL przywracający dokładnie, R23, R30, R34; K3: 6 cytatów spoza `pl.json`; K4: okres R13 i R22; K5: kolejność R22 — mój błąd w K4, wykryty przez autora — i pełny przepis konta w 21 warunkach wstępnych skróconych mimo K2).
- Czas do akceptacji: ~2 h 50 min od startu generatora (5 przebiegów korekt ~85 min pracy workera).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): potwierdzone P1 w R04, R10, R21 (+ P2/P3 w pozostałych z 11), 0 odrzuconych; recenzja przeoczyła zmyślone cytaty, które wykrył dopiero skrypt.
- Defekty po odbiorze: 0 — publikacja 32 nowych (seq 1821–1852) i 7 aktualizacji; pełne `verify` 0 realnych różnic (fałszywe: eksport `\_` i kolejność `requirements` w 985).
- Wymagane testy i dowody: `qas.py lint --strict` 0/0, skrypt cytatów czysty (poza nazwami programów i treścią spoza i18n), `qas.py verify` po publikacji.
- Uwagi: Gemini jako autor QA na funkcji z płatnością zmyśla napisy i myli okres z kwotą (K3: 369 zł → „miesięczny”); automatyczne porównanie cytatów z plikami i18n powinno iść PRZED recenzją krzyżową, nie po niej. Moje briefy korekt miały 3 błędne przesłanki (tabela cen, numery linii, klucz `RENEWAL.ERRORS.DECLINED`) — workerzy zgłosili je poprawnie.

### 1606-4C (przegląd zgodności dokumentacji, grupy A i B) — 2026-10-22
- Archetyp: Faza 4c — zgodność dokumentacji z implementacją (5 dokumentów UI/WP + INT/PB/RB/DBML), tylko odczyt.
- Stawka: wysoka (dokumentacja funkcji high-stakes).
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): — (poprawki: dokumentacja — architekt, kod — `wykonawca`, wpis 1606-FE-4C-K1).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Access read` (A: 414 s, B: 594 s; wcześniejsze przebiegi przerwane: A — 10 nieistniejących ścieżek z listy, A2 i B — limit okna 5 h Plusa po bramkach).
- Dopuszczone alternatywy: Muse Wonder `max` — zablokowany do 2026-10-26 00:00Z; Gemini wykluczony (autor rewizji).
- Powód wyboru: reguła 13 — inna rodzina niż autor dokumentacji (Gemini), stawka wysoka.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex zablokowany 17:10–19:02 (komunikat limitu), potem nieznany.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: A — 3 rozbieżności (1× kod odbiega, 2× brak w dokumencie); B — 7 (2× kod odbiega, 3× brak w dokumencie, 2× dokument nieaktualny).
- Rundy korekt: 1 (kod: FE-4C-K1; dokumentacja: architekt).
- Czas do akceptacji: ~1 h 40 min od wznowienia po resecie (bez czasu blokady).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): potwierdzone 7 (fokus faktury → kod; stan pola karty, rytm odpytywania, 400/502, DBML ×2 → dokumentacja); 1 fałszywy alarm (przyczyna `NULL` — stan nieosiągalny); 2 „kod odbiega” w B to zachowania sprzed #1606 we wspólnym kodzie (`FirstChargeAt` = czas domknięcia, przywracanie bez filtra terminu) + 1 luka RB (remis dat) → `czeka na właściciela`.
- Defekty po odbiorze: 0 przy wdrożeniu PRE (2026-10-22 17:38 UTC: FE 1.12.0, BE 1.14.0, nowe trasy aktywne); retest testera w toku.
- Wymagane testy i dowody: macierze zgodności (A: 14 wierszy zgodnych, 320 linków; B: 7 zgodnych, 157 linków), dziennik bez wpisów `otwarty`/`w toku`.
- Uwagi: Sol `high` w 4c rozróżnia „kod odbiega” od zachowania wspólnego kodu sprzed zadania dopiero po pytaniu o historię — triaż wymaga `git log` wspólnych plików. Dwie grupy równolegle + bramki FE/BE wyczerpały okno 5 h Plusa — przy kolejnej funkcji high-stakes planować 4c po resecie okna albo sekwencyjnie.

### 1606-FE-4C-K1 (poprawka z 4c: fokus i błędy pól danych do faktury) — 2026-10-22
- Archetyp: Poprawka UI bez niezmiennika (kontener + wiersz faktury + specy), 4 pliki.
- Stawka: niska/średnia.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Claude / `wykonawca` Sonnet 5.5 `high` (188 s).
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read` (614 s).
- Dopuszczone alternatywy: Sol `high` (pula Codexa po 4c).
- Powód wyboru: autor kontenera FE-L2; recenzja delty innej rodziny (Faza 4c — „poprawka kodu wraca do przeglądu na swojej delcie”).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany ZIELONY (hook, 19:10); Gemini nieznany.
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: poprawny; test kontenera czerwony z przywróconym `focusSaveAction()`.
- Rundy korekt: 0.
- Czas do akceptacji: ~25 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 potwierdzonych; odrzucone 2×P1 + 2×P2 (zwinięty formularz nieosiągalny w tej ścieżce; podwójny fokus na ten sam element — P3; zagnieżdżony `afterNextRender` — wzorzec istniejący; test na tej samej gałęzi) — Gemini nadal zawyża P1 bez sprawdzenia kolejności efekt → render.
- Defekty po odbiorze: 0 przy wdrożeniu PRE (2026-10-22 17:38 UTC: FE 1.12.0, BE 1.14.0, nowe trasy aktywne); retest testera w toku.
- Wymagane testy i dowody: eslint/prettier 0; 135/135 w 4 specach; pełne FE: lint 0, format OK, 5420/5420, build OK.

### 2148-DOC-A…D (nowa decyzja i interfejs + rewizje 12 dokumentów `zatwierdzony`, cztery briefy równolegle) — 2026-10-22
- Archetyp: Dokumentacja produktowa — nowy dokument decyzji i interfejsu (12 stanów, tabela tekstów) oraz rewizje procesu, reguł, architektury technicznej, wymagań przekrojowych, interfejsów i kwestii otwartej; rozłączne pliki per brief.
- Stawka: średnia (dokumentacja funkcji high-stakes — naliczanie, kody jednorazowe, limit prób — bez kodu; źródło prawdy dla PBI implementacyjnego).
- Niepewność: średnia (nowe dokumenty bez lokalnego precedensu; decyzje W1–W5, D1–D12 i P1–P7 podane w briefach).
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access write` (×4).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review` (wpis 2148-REV-DOC) + walidacja architekta.
- Dopuszczone alternatywy: Codex `gpt-6.1-sol` `high` write (`-CodexSandbox danger-full-access` przy odmowie zapisu); Claude `wykonawca` Sonnet 5.5 `high`; Muse — zablokowany.
- Powód wyboru: rewizje dokumentacji na Gemini `high` 0 rund (2747/2785/2723-DOC-1); Muse zablokowany limitem tygodniowym; Claude ŻÓŁTY — pula Claude'a zostaje dla Figmy.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini znany (`agy /quota`, 2026-10-22 ~21:20Z); Muse zablokowany do 2026-10-26T00:00Z (429 tygodniowy, log wrappera 20:47Z); Claude ostrzegawczy (hook, ŻÓŁTY).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: wymagane korekty — 543 / 493 / 376 / 475 s, exit 0; walidacja architekta: 4 rozbieżności (sprawdzenie wstępne po stronie przeglądarki, stany 5 i 11 niezgodne ze wzorem nakładki, fokus po wejściu, zgubione zdanie w WP-OCHRONA), recenzja: 6 kolejnych.
- Rundy korekt: 1 (wspólny brief 2148-DOC-K).
- Czas do akceptacji: ~2,5 h (start 21:26Z, odbiór po DOC-K i walidacji fali 2).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): REV-DOC — potwierdzone 5×P2 + 1×P3, odrzucone 0.
- Defekty po odbiorze: brak (macierz 4c bez rozbieżności).
- Wymagane testy i dowody: `git diff` 16 plików, skrypt odnośników 615/0, front matter, macierz 4c; commit `e80d4ba`.

### 2148-REV-DOC (recenzja dokumentacji fali 1) — 2026-10-22
- Archetyp: Recenzja dokumentacji produktowej (14 plików, nowa decyzja i interfejs).
- Stawka: średnia.
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): — (recenzja).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review`, `-BriefFile` z wyroczniami D/W/P.
- Dopuszczone alternatywy: Claude `wykonawca` Sonnet 5.5 `high` tylko odczyt (precedens 2723-4C); Muse — zablokowany.
- Powód wyboru: inna rodzina niż autor (Gemini); Sol `high` preferowany przy niskiej/średniej stawce (reguła 13); brak bramki Sol `max` w PBI analitycznym — pula Codexa wolna.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper, 2026-10-22 21:38Z).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowano — 315 s, exit 0, raport kompletny.
- Rundy korekt: 0.
- Czas do akceptacji: ~15 min (z triażem).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): potwierdzone 5×P2 (sprzeczna reguła nadwyżki, sprzeczny warunek udziału, nakładka otwierana bez kodu, brak stanu programu niedostępnego, brak wyjścia ze stanu zapisywania po błędzie technicznym) + 1×P3 (kopie progów); odrzucone 0. Dwa znaleziska wymusiły nowe decyzje architekta (P8, P9).
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: triaż każdego znaleziska w pliku dokumentacji; dziennik #13–#18.

### 2148-FIG-1 (komponent karty wejścia z kodu, 22 warianty) — 2026-10-22
- Archetyp: Figma — komponent z wariantami (Stan × Widok) z komponentów biblioteki, tryby zmiennych Light/Dark.
- Stawka: niska (makieta bez niezmiennika).
- Niepewność: średnia (nowy komponent; wzór `Zebrani/ScanCard`).
- Wykonawca (linia / model / native effort): Claude / `wykonawca` Sonnet 5.5 `high` + Figma MCP.
- Recenzent (linia / model / native effort): architekt (Opus `xhigh`) — `get_metadata` i zrzuty; inna rodzina z potwierdzonym Figma MCP niedostępna w sesji.
- Dopuszczone alternatywy: brak (Codex Figma niepotwierdzona; Muse i Gemini bez Figmy).
- Powód wyboru: zamknięta próba A/B — Figma zostaje w `wykonawca`; precedensy 1605-FIG-1, 2371-FIG-1.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook, ŻÓŁTY, 2026-10-22 wieczór).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowano — 702 s, 52 wywołania; 22 warianty, teksty zgodne z tabelą.
- Rundy korekt: 0 (stan 12 dołożony osobnym briefem FIG-3 po decyzji P8).
- Czas do akceptacji: ~20 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): brak.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: `get_metadata` (22 warianty), zrzuty Light, Dark w zrzutach FIG-2.

### 2148-FIG-2 (strona Public/ReceiptCode, 11 sekcji × 4 ramki) — 2026-10-22
- Archetyp: Figma — ekrany w layoucie publicznym z instancji komponentu, Mobile 360 / Desktop 1280 × Light / Dark.
- Stawka: niska.
- Niepewność: niska (kompozycja jak Public/Login, sekcje jak Logged/Client/Scan).
- Wykonawca (linia / model / native effort): Claude / `wykonawca` Sonnet 5.5 `high` + Figma MCP.
- Recenzent (linia / model / native effort): architekt — `get_metadata` i zrzuty każdej sekcji.
- Dopuszczone alternatywy: brak (jak FIG-1).
- Powód wyboru: jak FIG-1; zależność od komponentu FIG-1.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook, ŻÓŁTY).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowano — 352 s, 50 wywołań; 44 ramki.
- Rundy korekt: 0.
- Czas do akceptacji: ~15 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): uwagi wykonawcy do briefu (wzór bez sekcji, minimalna wysokość 648) przyjęte bez zmian.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: `get_metadata` 44 ramek, zrzuty sekcji 1, 4, 9.

### 2148-FIG-3 (stan 12 „Program niedostępny” — 2 warianty i sekcja strony) — 2026-10-22
- Archetyp: Figma — rozszerzenie komponentu i strony o nowy stan.
- Stawka: niska.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Claude / `wykonawca` Sonnet 5.5 `high` + Figma MCP.
- Recenzent (linia / model / native effort): architekt — zrzuty 4 ramek i obu wariantów.
- Dopuszczone alternatywy: brak.
- Powód wyboru: autor komponentu i strony, kontekst biblioteki.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook, ŻÓŁTY).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: wymagane korekty — 157 s; ikona `pause-circle` ~12 px zamiast 40 px (ograniczenia CENTER wektora).
- Rundy korekt: 1 (107 s, przeskalowanie instancji).
- Czas do akceptacji: ~15 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1 potwierdzone (rozmiar ikony, P2), 0 odrzuconych.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: zrzuty Mobile/Desktop × Light/Dark sekcji 12, warianty 4135:4517/4523.

### 2148-DOC-K (korekty dokumentacji po walidacji i recenzji, 9 plików + 2 nowe rewizje) — 2026-10-22
- Archetyp: Dokumentacja produktowa — korekty wielu dokumentów wg tabeli znalezisk i nowych decyzji P8/P9.
- Stawka: średnia.
- Niepewność: niska (każda korekta podana w briefie z miejscem i treścią decyzji).
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access write`.
- Recenzent (linia / model / native effort): architekt — diff każdego pliku i skrypt odnośników (reguła poprawek Fazy 4b).
- Dopuszczone alternatywy: Codex `gpt-6.1-sol` `high` write; Claude `wykonawca` Sonnet 5.5 `high`.
- Powód wyboru: linia autora fali 1 (reguła poprawek).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini znany (`agy /quota`, tydzień 17 %, 2026-10-22 ~21:50Z).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: zaakceptowano z dwiema poprawkami jednolinijkowymi architekta — 1104 s; etykieta briefu „K-A4” przeciekła do dokumentu UI; punkt 22 decyzji twierdził, że teksty nie są powielane, choć trzy punkty je cytują.
- Rundy korekt: 0 (poprawki architekta, reguła 11).
- Czas do akceptacji: ~40 min (z walidacją).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 2 potwierdzone (P3), 0 odrzuconych; dwie uwagi wykonawcy do briefu odrzucone (nieidempotencja — świadomy kompromis; „stan 5 nakładki z nieaktywnym przyciskiem” — nakładka ma przycisk „Gotowe”).
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: diff, `grep` etykiet briefu = 0, odnośniki 615/0, dziennik #8–#19 zamknięty.

### 2148-QAS-A (QA Sphere: 36 nowych przypadków wejścia gościa z kodu — 33 + 3 z K1 — i przegląd 35 istniejących, z korektami K1–K3) — 2026-10-22
- Archetyp: QA Sphere — autor pliku podglądu (`qas.py`), przypadki manualne zachowania docelowego PBI #2800 przed implementacją; przegląd poddrzewa „Skanowanie kodu przez klienta”.
- Stawka: średnia (przypadki dla funkcji high-stakes — kody jednorazowe, limit prób, naliczanie — bez kodu; błąd daje przypadek niewykonalny albo fałszywy werdykt testera).
- Niepewność: średnia (zachowanie docelowe bez implementacji; dane testowe PRE dla stanów programu i kodu bez gotowej procedury).
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access write` (QAS-A + korekty K1, K2, K3).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review` (wpis 2148-QAS-R) + walidacja architekta.
- Dopuszczone alternatywy: Codex `gpt-6.1-sol` `high` write; Muse Wonder `max` (para skilla dla funkcji high-stakes) — zablokowany.
- Powód wyboru: decyzja właściciela W5 (Muse wyczerpany do poniedziałku); rewizje dokumentacji na Gemini `high` bez rund.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini znany (`agy /quota`, tydzień 15 %, 2026-10-22 ~22:20Z); Muse zablokowany do 2026-10-26T00:00Z (429 tygodniowy).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: wymagane korekty — 820 s, `lint` 0/0; recenzja: 22×P2 (przygotowanie niewykonalne lub niesamodzielne, luki ponownej weryfikacji przy zapisie, zła trasa EN, wymóg `noindex` spoza dokumentacji); architekt dołożył 2 uwagi (TC13 treść żądania HTTP, TC23 „HTTP 429” — fakty spoza dokumentacji).
- Rundy korekt: 3 (K1 1125 s — 23 pozycje + TC34–TC36; K2 375 s — TC36 i TC33 po sprostowaniu znacznika urządzenia; K3 551 s — TC32 odsyłał do TC31).
- Czas do akceptacji: ~2 h 10 min (start 22:21Z, pełne `verify` po wysyłce ~23:30Z; wysyłka seq 1853–1888).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): QAS-R — potwierdzone 22×P2, odrzucone 0; 2 z nich wynikały z błędów briefu architekta (wolny numer sprawdzany na liście klientów jednego właściciela; okno prywatne w przypadkach limitu). Wykonawca w K1 obalił założenie dokumentacji i recenzenta (okno prywatne też dostaje znacznik — potwierdzone w `DeviceMarker.read()`), co dało poprawkę DEC i PB (`2892d89`, `df9e907`). W K1 dopisał w raporcie (nie w przypadkach) zmyślone adresy API i kody HTTP — do pilnowania w briefach Gemini.
- Defekty po odbiorze: brak (pełne `qas.py verify`).
- Wymagane testy i dowody: `qas.py lint` 0/0 po każdej rundzie, porównanie przypadków między przebiegami (zmienione tylko klucze z briefu), pełne `verify`.

### 2148-QAS-R (recenzja przypadków QA Sphere fali QAS-A) — 2026-10-22
- Archetyp: Recenzja przypadków manualnych QA Sphere (33 nowe, przegląd 35 istniejących) wobec dokumentacji, seedów i kodu.
- Stawka: średnia.
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): — (recenzja).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review`, `-BriefFile`, `-Repo` = Dokumentacja.
- Dopuszczone alternatywy: Claude `wykonawca` Sonnet 5.5 `high` tylko odczyt; Muse — zablokowany.
- Powód wyboru: decyzja właściciela W5; inna rodzina niż autor (Gemini); brak bramki Sol `max` w PBI analitycznym.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper, 2026-10-22 22:37Z).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowano — 452 s, exit 0; raport kompletny, ale zdublowany i przemieszany w stderr (do czytania z sekcji „Full review comments”).
- Rundy korekt: 0.
- Czas do akceptacji: ~45 min (z triażem i ustaleniem danych PRE: stały kod SMS poza produkcją wg DEC, korekta właściciela, brak w UI wstrzymania/zakończenia programu → zapytania SQL z przywróceniem).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): potwierdzone 22×P2, odrzucone 0; 0 P0/P1. Jedno (TC23 — okno prywatne bez znacznika) oparte na nieprecyzyjnym zdaniu dokumentacji; poprawka nieszkodliwa (zwykły profil). Krytyka briefu autora trafna.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: triaż każdego znaleziska w dokumentacji, seedach (`Script9500*`), `pl.json`, `app.routes.ts`, `device-marker.ts`.

### 1806-BE-1 (BE-1, BE-1a, BE-1b, BE-1bK) (slice ShopService: kwalifikacja rekordu, lista, logo, wejście z konta, `HasStaffAccess`) — 2026-10-22
- Archetyp: BE — pliki niezmiennika high-stakes (PIN sprzedawcy, sesja personelu, kwalifikacja dostępu), jeden slice + testy xunit (unit + integracja SQLEXPRESS).
- Stawka: wysoka.
- Niepewność: średnia (jedna definicja kwalifikacji dla listy, menu i 4 wywołań `HasStaffAccess`; stan „zamknięty” pochodny, bez migracji).
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` Opus 5.5 `xhigh` (BE-1 → strażnik 300 tys. → BE-1a); testy: Claude / `tester` Haiku 5.5 `xhigh` (BE-1b, BE-1bK).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review` (plan: Muse Wonder Full `max` — 429 tygodniowy).
- Dopuszczone alternatywy: przy CZERWONYM Muse Wonder Full `max` albo czekanie (zablokowany); recenzja Gemini wykluczona (high-stakes).
- Powód wyboru: pliki niezmiennika → `wykonawca-opus`; testy na istniejącym wzorcu → `tester`; recenzent przekwalifikowany po 429 Muse na jedyną dopuszczoną rodzinę spoza Claude'a, z uwagą na pulę Codexa przed bramką.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook, ZIELONY, 2026-10-22 ~20:45Z); Muse zablokowany do 2026-10-26T00:00Z (429 tygodniowy, 20:47Z); Codex nieznany (wrapper).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: przekazanie strażnika — BE-1 568 s / 64 wywołania (302 tys.), BE-1a 1100 s / 102 wywołania; testy BE-1b 900 s / 52 wywołania; 2 testy logo błędne → BE-1bK 125 s.
- Rundy korekt: 1 (BE-1bK — testy, nie kod).
- Czas do akceptacji: ~1 h 10 min (z walidacją architekta i recenzją).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 potwierdzonych; 1×P2 odrzucone (id ≤ 0 → 400 to walidacja wejścia, nie wyciek istnienia rekordu).
- Defekty po odbiorze: bramka końcowa BE znalazła P1 we wspólnym SQL zmiany PIN-u (wpis 1806-G-BE) — w kodzie fali 2/drogi właściciela, nie w tym slice.
- Wymagane testy i dowody: `dotnet test` 8376/8376 (architekt), testy integracyjne zamiast curl (401, `no-store`, 409, sesja `EnteredFromAccountSession`, `LastLoginAt`).

### 1806-FE-1 (+FE-1K) (warstwa danych obsługi sklepu: sesja, DTO, API bez SSR i transfer cache, fasada działań) — 2026-10-22
- Archetyp: FE — pliki niezmiennika high-stakes (sesja, przepływ wejścia do obsługi, PIN poza SSR), serwisy + specy.
- Stawka: wysoka.
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` Opus 5.5 `xhigh`.
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review` (plan: Muse Wonder Full `max` — 429).
- Dopuszczone alternatywy: jak 1806-BE-1.
- Powód wyboru: sesja i przepływ wejścia to niezmiennik → `wykonawca-opus`; recenzent jak BE-1.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak 1806-BE-1.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: wymagane korekty — 1590 s, 63 wywołania; kontrakt błędów fasady niespójny z briefem (recenzja).
- Rundy korekt: 1 (FE-1K, `wykonawca-opus`, 172 s).
- Czas do akceptacji: ~1 h.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1 potwierdzone (P2), 0 odrzuconych.
- Defekty po odbiorze: bramka końcowa FE — odpięcie nadpisywało flagę serwera lokalną liczbą kart (P2, wpis 1806-G-FE).
- Wymagane testy i dowody: lint, format, `npm test` 5456/5456, build; SSR `/panel/obsluga-sklepu` bez PIN-u.

### 1806-FE-1b (przeniesienie `pin-cells` do `logged/components`, `revealed` jako `model()`, enum odbiorcy, i18n) — 2026-10-22
- Archetyp: FE — refaktor przeniesienia komponentu prezentacyjnego z drugim konsumentem, bez niezmiennika.
- Stawka: niska.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access write` (plan: Muse Spark 1.3 `max` — 429 po 20 s).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review` (recenzja fali 1 FE razem z FE-1).
- Dopuszczone alternatywy: Claude `wykonawca` Sonnet 5.5 `high`.
- Powód wyboru: archetyp Sparka `max`; po 429 Gemini — Node z Windows i własny lint/test, refaktor bez Figmy i bez niezmiennika.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Muse zablokowany (429, 20:47Z); Gemini nieznany (wrapper).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowano — 884 s, 142 wywołania.
- Rundy korekt: 0.
- Czas do akceptacji: ~40 min (z walidacją fali).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): brak dotyczących FE-1b.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: specy `pin-cells` i Sprzedawców zielone, `npm test` całości, `pin-cells.scss` przeniesiony bajt w bajt.

### 1806-DOC-1 (+DOC-1K) (datowane rewizje 2026-10-22: UI obsługi sklepu, layout zalogowany, WP formatu PIN-u, PB zmiany PIN-u, AT logowania personelu) — 2026-10-22
- Archetyp: Dokumentacja produktowa — rewizje dokumentów `zatwierdzony` w granicach decyzji właściciela D1–D3.
- Stawka: średnia.
- Niepewność: niska (każda zmiana z mapy planu).
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access write` (DOC-1, DOC-1K) (plan: Muse Spark 1.3 `max` — 429).
- Recenzent (linia / model / native effort): Claude / `wykonawca` Sonnet 5.5 `high` (tylko odczyt).
- Dopuszczone alternatywy: Codex `gpt-6.1-sol` `high` (oszczędzany na bramki).
- Powód wyboru: archetyp rewizji dokumentacji; po 429 Gemini (dotychczasowe rewizje 0 rund); recenzent z innej rodziny niż autor, bez zużycia puli Codexa.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Muse zablokowany; Gemini nieznany; Claude znany (hook).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: wymagane korekty — 958 s, 115 wywołań.
- Rundy korekt: 1 (DOC-1K, 740 s).
- Czas do akceptacji: ~1 h.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 4×P2 + 1×P3 potwierdzone, 0 odrzuconych.
- Defekty po odbiorze: przegląd 4c znalazł 6 braków dokumentu wobec kodu (wpis 1806-4C) — zachowania doprecyzowane dopiero w falach 2–3 i bramkach.
- Wymagane testy i dowody: diff każdego pliku, dziennik rozbieżności.

### 1806-BE-2 (BE-2a, BE-2aT, BE-2b, BE-2K) (własna zmiana PIN-u, rezygnacja z e-mailem 105, wyścig z cofnięciem odebrania dostępu) — 2026-10-22
- Archetyp: BE — pliki niezmiennika high-stakes (PIN, dostęp, sesje urządzeń), handlery + testy xunit.
- Stawka: wysoka.
- Niepewność: średnia (skutki identyczne z drogą właściciela; współbieżność z `UndoSellerRevocation`).
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` Opus 5.5 `xhigh` (BE-2a, BE-2K); testy: Claude / `tester` Haiku 5.5 `xhigh` (BE-2aT, BE-2b).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review`, 2 przebiegi (plan: Muse Wonder Full `max` — 429).
- Dopuszczone alternatywy: jak 1806-BE-1.
- Powód wyboru: jak 1806-BE-1; testy osobnym briefem po strażniku.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook); Muse zablokowany; Codex nieznany.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: przekazanie strażnika — BE-2a 1256 s / 84 wywołania (314 tys.); testy BE-2aT 740 s, BE-2b 761 s (101 testów ShopService, bez Skip).
- Rundy korekt: 1 (BE-2K, 886 s: okno i przyczyna atomowo w jednym UPDATE, anulowanie między próbami).
- Czas do akceptacji: ~1 h 40 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): przebieg 1 (52 s) — STOP na błędnej przesłance briefu architekta (`RunAsync` nie ponawia zakleszczeń), przesłanka poprawiona; przebieg 2 (232 s) — 2×P2: wyścig cofnięcie ↔ rezygnacja potwierdzony, anulowanie potwierdzone częściowo (`IDapperWrapper` bez tokenu = dług repo).
- Defekty po odbiorze: bramka końcowa BE — znak wodny `PinChangedAt` cofał się przy równoległych zmianach PIN-u (P1, wpis 1806-G-BE); recenzja fali tego nie wychwyciła.
- Wymagane testy i dowody: `dotnet test` 8445/8445 (architekt), API lokalnie: `pin-changes` 200 `no-store`, `resignations` 200, 409, wiersz outboxu 105 (pl, parametry).

### 1806-FE-2 (FE-2, FE-2c1, FE-2c2, FE-2K, FE-2K2) (ekran „Obsługa sklepu” z Figmy: lista kart, stany, okna Zmień PIN / Odepnij się, trasa, i18n) — 2026-10-22
- Archetyp: FE — ekran z Figmy w funkcji high-stakes, bez plików niezmiennika (korzysta z fasady FE-1).
- Stawka: średnia (UI pokazuje PIN i wyzwala działania high-stakes).
- Niepewność: średnia (stany karty, mobilny stan pusty i okna w Dark poza makietą — z opisu PBI).
- Wykonawca (linia / model / native effort): Claude / `wykonawca` Sonnet 5.5 `high` + Figma MCP (FE-2 → strażnik → FE-2c1, FE-2c2); korekty: Gemini / `gemini-3.8-flash-medium` (FE-2K, po walidacji), `gemini-3.8-flash-high` (FE-2K2, po recenzji).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review` (plan: Muse Wonder `max` — 429).
- Dopuszczone alternatywy: brak dla FE-2 (jedyna linia z potwierdzonym Figma MCP); recenzent Gemini `high`.
- Powód wyboru: Figma MCP + ekran bez niezmiennika. Korekty przekwalifikowane z autora na Gemini — powód nie został zapisany w kroku; reguła poprawek każe wracać do autora, o ile się kwalifikuje — do pilnowania.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook); Muse zablokowany; Gemini, Codex nieznane.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: przekazanie strażnika — FE-2 446 s / 51 wywołań (319 tys.), FE-2c1 143 s, FE-2c2 360 s; walidacja (browser-check 28/28 + 4/4) → FE-2K 268 s (okna wg makiety, komunikat stanu z ikoną, fokus po nieudanym wejściu).
- Rundy korekt: 2 (FE-2K po walidacji, FE-2K2 223 s po recenzji).
- Czas do akceptacji: ~1 h 30 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 4×P2 potwierdzone (blokada przy przeładowaniu, PIN po filtrze, fokus po odpięciu z filtrem, fokus po 409), 0 odrzuconych.
- Defekty po odbiorze: brak (bramka FE — patrz 1806-G-FE, defekt w fasadzie/stronie stanu menu).
- Wymagane testy i dowody: lint, format, `npm test` 5551/5551, build; `browser-check` matrix 2×2 i flows; SSR z ciasteczkiem bez PIN-u.

### 1806-FE-3 (FE-3a, FE-3a-cont, FE-3b, FE-3K) (Vitest + AXE: strona, karta, okna, stany listy) — 2026-10-22
- Archetyp: Testy FE — specy UI i AXE na istniejącym wzorcu, scenariusze z briefu.
- Stawka: średnia.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Claude / `tester` Haiku 5.5 `xhigh`.
- Recenzent (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access read`.
- Dopuszczone alternatywy: Codex `gpt-6.1-sol` `high` (recenzja); Muse Spark `max` (wykonanie) — zablokowany.
- Powód wyboru: linia `tester` po próbie z 2026-10-13; recenzja niskiej/średniej stawki poza Codexem (pula przed bramkami).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany (hook); Gemini nieznany.
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: FE-3a 678 s (33 testy, strażnik → FE-3a-cont 257 s — podział pod lint), FE-3b 498 s (62 testy, 0 skip).
- Rundy korekt: 1 (FE-3K, 299 s).
- Czas do akceptacji: ~1 h 10 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 7 potwierdzonych (1×P1 obniżony do P2 — fokus po 409 w oknach; Success wejścia, fokus po anulowaniu, ponowne ukrycie PIN-u, pozorne `toBeDefined`, symetria, korzeń w teście wycieku); 1 przesłanka (`document.body`) bez skutku. Mutacja (wyłączone `scheduleFocusRestore()`) → 8 testów czerwonych; przesłanka briefu FE-3K o anulowaniu błędna (fokus wraca też przez nakładkę).
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: `npm test` 5555/5555 (AXE w środku), lint 0, format, build.

### 1806-SCSS (audyt SCSS 6 plików + FE-SCSS-K) — 2026-10-22
- Archetyp: Audyt SCSS (tokeny, mixiny, zakaz nadpisań PrimeNG) + poprawki wg przyjętych pozycji.
- Stawka: niska.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): audyt Gemini / `gemini-3.8-flash-high`, `-Access read`; poprawki Gemini / `gemini-3.8-flash-high`, `-Access write` (plan: Muse Spark 1.3 `max` — 429).
- Recenzent (linia / model / native effort): architekt (triaż audytu, diff poprawek, specy).
- Dopuszczone alternatywy: Claude `wykonawca` Sonnet 5.5 `high`.
- Powód wyboru: preferencja audytu SCSS na Sparku niedostępna; Gemini bez puli Claude'a.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Muse zablokowany; Gemini nieznany.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: audyt 480 s, 6/6 plików przeczytanych; przyjęte: `[fluid]`, `d-block`, skala odstępu, `[dt]` plakietek, 3 mixiny; odrzucone: `.mb-4`, mixin stron list, scalenie okien i wspólny ListStateView (→ propozycja PBI refaktoru).
- Rundy korekt: 1 (FE-SCSS-K, 640 s) + 1 poprawka komentarza mixinu przez architekta (reguła 11).
- Czas do akceptacji: ~40 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): —.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: specy 62 + seller-card 13 + batch-card 28 zielone, zrzuty kart i okien po poprawkach.

### 1806-G-BE (+BE-GK) (bramka końcowa BE) — 2026-10-23
- Archetyp: Bramka końcowa high-stakes — cały diff BE w jednym przebiegu.
- Stawka: wysoka.
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): poprawka Claude / `wykonawca-opus` Opus 5.5 `xhigh` (BE-GK).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `max`, `-Mode review`.
- Dopuszczone alternatywy: D7 — Muse Wonder Full `max` (zablokowany).
- Powód wyboru: reguła 6.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper, 2026-10-22 23:11Z).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: 442 s, exit 0.
- Rundy korekt: 1 (BE-GK, 619 s: monotoniczny CASE w `UpdateAssignmentPinAsync.sql` + 4 testy SQL Server; test sesji czerwony na starym SQL wg raportu).
- Czas do akceptacji: ~35 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1×P1 potwierdzone — znak wodny `PinChangedAt` cofa się przy równoległych zmianach PIN-u (wspólny SQL, także droga właściciela) → ożywa unieważniona sesja; znalezione tylko przez bramkę.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: `dotnet test` 8449/8449 (architekt), diff BE-GK.

### 1806-G-FE (+FE-GK) (bramka końcowa FE) — 2026-10-23
- Archetyp: Bramka końcowa high-stakes — cały diff FE w jednym przebiegu.
- Stawka: wysoka.
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): poprawka Claude / `wykonawca-opus` Opus 5.5 `xhigh` (FE-GK: fasada + strona + testy).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `max`, `-Mode review`.
- Dopuszczone alternatywy: D7 — Muse Wonder Full `max` (zablokowany).
- Powód wyboru: reguła 6.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper, 23:21Z); po przebiegu 5 h 70 %, tydzień 17 % (raport tokenów).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: 676 s, exit 0.
- Rundy korekt: 1 (FE-GK, 348 s; 59/59 w 3 specach, 4 mutacje czerwone).
- Czas do akceptacji: ~30 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 2×P2 — odpięcie nadpisuje flagę serwera lokalną liczbą kart (potwierdzone); oczekujące wejście przy zmianie konta (sporne, bez zmiany: anulowanie nie cofa `Set-Cookie`; pytanie właściciela o życie sesji personelu po końcu sesji konta).
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: lint 0, format, `npm test` 5557/5557, build.

### 1806-4C (przegląd zgodności dokumentacji z kodem, 2 przebiegi) — 2026-10-23
- Archetyp: Przegląd zgodności 4c — mapa dokumentów × kod, macierz werdyktów.
- Stawka: średnia.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): — (przegląd).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review` (plan: Gemini `high`; po 429 Muse autorem dokumentacji został Gemini, więc recenzent z innej rodziny).
- Dopuszczone alternatywy: Claude `wykonawca` Sonnet 5.5 `high` tylko odczyt.
- Powód wyboru: inna rodzina niż autor dokumentacji (Gemini); Codex po bramkach z zapasem tygodnia.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex znany po przebiegu (5 h 70 %, tydzień 17 %, 23:21Z).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: przebieg 1 (38 s) — STOP na błędnej przesłance briefu (§10/§14 są w `INSTRUKCJA-DLA-AI.md`); przebieg 2 (430 s): 0× kod odbiega, 6× brak w dokumencie. `-Mode review` przeformatował wynik na komentarze P2 — macierz z liczbami `zgodne` na sekcję przepadła (pamięć `codex-review-gubi-format-macierzy`).
- Rundy korekt: 1 (poprawiona przesłanka).
- Czas do akceptacji: ~25 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 6 potwierdzonych (braki w dokumencie, P2), 0 odrzuconych → DOC-2.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: triaż każdego braku w kodzie FE/BE.

### 1806-DOC-2 (uzupełnienia dokumentacji po bramkach i 4c, 2 pliki) — 2026-10-23
- Archetyp: Dokumentacja produktowa — uzupełnienie dokumentów `zatwierdzony` o zachowania z kodu (dziennik 12–14, 16–18).
- Stawka: średnia.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access write`.
- Recenzent (linia / model / native effort): architekt (diff 2 plików, CRLF).
- Dopuszczone alternatywy: Codex `gpt-6.1-sol` `high` write (`-CodexSandbox danger-full-access`).
- Powód wyboru: linia autora rewizji fali 1 (reguła poprawek).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini nieznany (wrapper, 23:50Z).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: zaakceptowano z dwiema poprawkami architekta (reguła 11) — 594 s; etykieta briefu „(punkt f)” przeciekła do dokumentu UI; zdanie o 409 uogólnione na „każdą odmowę” bez rozróżnienia działań.
- Rundy korekt: 0.
- Czas do akceptacji: ~20 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 2 potwierdzone (P3), 0 odrzuconych. Drugi raz w dwóch dniach etykieta briefu przecieka do dokumentu w Gemini (por. 2148-DOC-K) — brief Gemini powinien zakazywać etykiet roboczych wprost.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: diff, `grep` etykiet briefu = 0.

### 1806-QAS (QA Sphere: obsługa sklepu — lista, karta, wejście, Zmień PIN, Odepnij się; przegląd 112 istniejących) — 2026-10-23
- Archetyp: QA Sphere — autor pliku podglądu w funkcji high-stakes (PIN, sesja personelu, limity dostępu); przegląd folderów Obsługa sklepu, Personel i Sprzedawcy oraz nowe przypadki ręczne z przygotowaniem SQL na wspólnym PRE.
- Stawka: wysoka (przypadki zmieniają PIN-y i odpinają rekordy na wspólnym PRE; skrypty SQL zapisujące).
- Niepewność: wysoka (pierwszy zestaw z syntetycznym programem zakończonym i postarzaniem dat pod granice 30 dni).
- Wykonawca (linia / model / native effort): Gemini / `gemini-3.8-flash-high`, `-Access write` — generator (964 s); K1 (1923 s, wrapper `failed` exit 3: raport ucięty limitem wyjścia, plik kompletny); K2 (858 s); K3 (488 s, `failed` — 429 limitu tygodniowego, plik nietknięty).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode exec -Access read` — R1 (541 s); R2: 189 s do limitu okna 5 h, ponowienie po resecie 891 s.
- Dopuszczone alternatywy: autor — Muse Wonder `max` (skill, high-stakes) zablokowany do 2026-10-26T00:00Z → Gemini write (skill: „gdy Muse zgłosił limit”); recenzent — Muse read (twarda reguła skilla: plik Gemini → Muse) zablokowany → ponowna kwalifikacja wg reguły 2 na Sol `high` read (precedens 2148-QAS-R); po limicie Gemini przy K3 skill nie dopuszcza trzeciej linii autora → `zablokowane`, decyzja właściciela.
- Powód wyboru: jedyna linia autora dopuszczona przez skill przy zablokowanym Muse; recenzent z innej rodziny z lokalnymi wynikami tego archetypu.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Muse zablokowany (429, reset 2026-10-26T00:00Z); Gemini nieznany do K3, potem zablokowany (429 RESOURCE_EXHAUSTED „Resets in 78h8m5s”, 03:52Z); Codex nieznany, zablokowany 01:34Z (limit okna, reset 05:26 lokalnie), znany po resecie; Claude ostrzegawczy (hook ŻÓŁTY, tydzień 90 % przy 72 % upływu).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 20 nowych, 112 przejrzanych; lint 0 błędów; R1: 2×P1 (D07 zmieniał wspólny PIN, SQL L06 dotykał cudzego rekordu) i ~20×P2 (dane i adresy API, sesje, przygotowanie, etykiety, tabela outboxu, granice, autoryzacja). Architekt przed R2 znalazł 3 defekty SQL, których R1 nie zgłosił: zamknięcie i „przywrócenie” na ACTIVE programu z seeda (Stara Piekarnia jest celowo CLOSED), 6 wierszy z tym samym PIN-em wbrew `UQ_StaffAssignments_Phone_Pin`, sprzątanie zostawiające sprzedawcę.
- Rundy korekt: 2 zakończone (K1: 29 przypadków, 1 update; K2: syntetyczny program zakończony, sprzedawca-znacznik, sprzątanie), K3 zablokowana limitem linii autora.
- Czas do akceptacji: nie zaakceptowano (stan `zablokowane` od 03:52Z; pierwsza linia autora wolna 2026-10-26T00:00Z).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): R1 2×P1 + ~20×P2 potwierdzone, 0 odrzuconych; R2 2×P1 potwierdzone (D10 i D12 zmieniały PIN i odpinały wspólną kartę „Program demonstracyjny”), 1×P1 odrzucony (ZEB-913: postarzenie zgłoszeń SMS to zamierzone zdjęcie limitu), ~13×P2 + 3×P3 przyjęte.
- Defekty po odbiorze: n/d (zestaw niewysłany).
- Wymagane testy i dowody: `qas.py lint` z `--context` (0 błędów, 1 zamierzona uwaga), porównanie kluczy z kopią sprzed przebiegu, przegląd architekta wszystkich `INSERT`/`UPDATE`/`DELETE` wobec seedów `Script9500*` i indeksów unikalnych z `filter_definition`.
- Uwagi: (1) Sol `high` w R1 nie zauważył SQL psującego seed innego zestawu — przegląd skryptów zapisujących to obowiązek architekta przed recenzją (pamięć `qas-skrypty-sql-nie-ruszaja-seedow`); (2) zasada wspólnej karty konta testowego musi stać w briefie generatora z góry, inaczej wraca w kolejnych korektach (K1 dodała dwa nowe naruszenia); (3) przy zablokowanych Muse i Gemini skill QA Sphere nie ma trzeciej linii autora — luka procedury do decyzji właściciela.

### 2807-T (czerwone testy dwóch Bugów BE: xunit jednostkowy kolizji indeksu unikalnego + integracyjny precyzji czasu na SQL Server) — 2026-10-23
- Archetyp: Testy — czerwony test Buga przed łatką (xunit, Moq `Strict`, `[SqlServerFact]`).
- Stawka: wysoka (PIN personelu, sesja personelu).
- Niepewność: średnia (pierwszy brief Buga linii `tester` na Haiku; w próbie testera nie było briefu Buga).
- Wykonawca (linia / model / native effort): Claude / `tester` Haiku 5.5 `xhigh`.
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review` (recenzja fali objęła testy i łatkę — wpis 2807-R).
- Dopuszczone alternatywy: Claude `wykonawca` Sonnet 5.5 `high`. Muse i Gemini zablokowane. Codex odpadł, bo jego testy wymagałyby recenzji fali spoza Codexa, a żadna taka linia nie była wolna.
- Powód wyboru: linia testera; gotowe wzorce w repo (sekwencje Moq z wyjątkami SQL, fikstura SQL Server).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook ŻÓŁTY, tydzień ~91 %, 2026-10-23 rano); Muse zablokowany do 2026-10-26T00:00Z; Gemini zablokowany do ok. 2026-10-26 10:00Z.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowano, ~7,4 min. 7 testów czerwonych z właściwego powodu (`SqlException` z handlera, `Assert.Null` sesji, różnica tyknięć `datetime`), 13 zielonych. Czerwień nie pochodziła z mocka `Strict` — w briefie Buga potwierdzony warunek „bez fałszywego czerwonego”, którego próba testera nie sprawdziła.
- Rundy korekt: 0 (korekta K1 po recenzji fali — wpis 2807-R).
- Czas do akceptacji: ~15 min (z przebiegiem architekta i hashami plików testów).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1×P2 potwierdzone w recenzji fali — mocki zapisu w testach kolizji przyjmowały dowolne połączenie; 0 odrzuconych.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: `dotnet test --filter` architekta z `ZEBRANI_TEST_SQLSERVER` (7 czerwonych, 13 zielonych), SHA-256 trzech plików testów przed łatką.
- Uwagi: tester wykrył błąd briefu — pominięty drugi indeks unikalny (`UQ_StaffAssignments_Program_Phone`); rozwiązał go wierszem nieaktywnym zamiast obchodzić asercję. Wzorce grep w briefach były po angielsku, a wyjście `dotnet` jest po polsku — brief BE musi podawać wzorce polskie (`Zakończone|Niepowodzenie|Łączna liczba`).

### 2807-P (łatka dwóch Bugów BE, 8 plików produkcyjnych: ponowienie transakcji przy kolizji indeksu, `DbType.DateTime2` dla czasów personelu i sesji) — 2026-10-23
- Archetyp: Backend — niezmiennik PIN-u i sesji personelu (ponowienie całej transakcji od świeżego odczytu, typy parametrów Dappera).
- Stawka: wysoka.
- Niepewność: niska (wzór ścieżki własnej z PBI #1807 i `DbType.DateTime2` już w repo).
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` Opus 5.5 `xhigh`.
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review` (fala); bramka Codex / `gpt-6.1-sol` `max`.
- Dopuszczone alternatywy: przy CZERWONYM Muse Wonder Full `max` (zablokowany) albo czekanie.
- Powód wyboru: pliki niezmiennika high-stakes (PIN, sesja personelu).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook ŻÓŁTY, 2026-10-23 rano).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: zaakceptowano, ~6,4 min. Testy T zielone, hashe plików testów bez zmian, build 0 ostrzeżeń, pełny pakiet 8457/8457. Raport wskazał 3 słabości w otoczeniu: 9 z 13 parametrów bez testu (faktycznie 12 do zmiany i 1 już `DateTime2`), sprzeczny opis klasy testów w HEAD, słaba asercja `seenTaken` w HEAD. Wszystkie trzy przeszły do K1.
- Rundy korekt: 0.
- Czas do akceptacji: ~20 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): recenzja fali — 0 defektów kodu produkcyjnego; bramka — 0 znalezisk.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: `dotnet test` 8465/8465 na SQL Server (po K1), CI `main` i gałęzi zielone, PRE BE 1.15.1 na docelowym SHA.

### 2807-R (+K1) (recenzja fali: cały niescommitowany diff BE — łatka Opusa i testy Haiku) — 2026-10-23
- Archetyp: Recenzja fali high-stakes — pliki niezmiennika i testy dowodzące.
- Stawka: wysoka.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): poprawka Claude / `tester` Haiku 5.5 `xhigh` (K1).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review`.
- Dopuszczone alternatywy: Muse Wonder Full `max` (para reguły 8 dla recenzji plików niezmiennika) zablokowany do 2026-10-26T00:00Z; Gemini `high` zablokowany; brak innej wolnej rodziny spoza Claude'a → przy limicie Codexa czekanie.
- Powód wyboru: inna rodzina niż autorzy (Claude), jedyna wolna; ponowna kwalifikacja wg reguły 2 przy zablokowanym Muse.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper, 2026-10-23 07:24Z).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 187 s, exit 0; 0 defektów produkcyjnych, 1×P2 w testach.
- Rundy korekt: 1 (K1, ~9,2 min: osobne połączenie na próbę w mockach, opis klasy testów, asercja `seenTaken`, 8 strażników `DateTime2` dla pozostałych parametrów; mutacja w kopii repo bez `DbType.DateTime2` — 11/11 czerwonych).
- Czas do akceptacji: ~30 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1×P2 potwierdzone, 0 odrzuconych, 0 fałszywych P0/P1.
- Defekty po odbiorze: brak (bramka 0 znalezisk).
- Wymagane testy i dowody: pełny pakiet 8465/8465, 0 pominiętych; SHA-256 plików testów po K1.

### 2807-G (bramka końcowa BE) — 2026-10-23
- Archetyp: Bramka końcowa high-stakes — cały diff BE w jednym przebiegu.
- Stawka: wysoka.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): — (0 znalezisk, bez poprawki).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `max`, `-Mode review`.
- Dopuszczone alternatywy: brak (reguła 6; przy limicie czekanie na reset).
- Powód wyboru: reguła 6.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany (wrapper, 2026-10-23 07:44Z); po przebiegu 5 h 24 %, tydzień 25 % (raport tokenów).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: 312 s, exit 0; 0 znalezisk. Przeczytała cały `git diff HEAD`, oba handlery zmiany PIN-u, `GlobalExceptionHandler`, wyjątek, SQL sesji, DI, testy i WP.
- Rundy korekt: 0.
- Czas do akceptacji: ~10 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: raport bramki; architekt — pełny pakiet 8465/8465, CI, PRE 1.15.1.
- Uwagi: przy małym diffie po recenzji fali bramka nie dołożyła znaleziska (por. 1806-G-BE, gdzie jedyny P1 znalazła bramka). Recenzja fali i bramka z jednej rodziny (Codex) są dopuszczalne, bo niezależność liczy się wobec autora (Claude).

### 1402-B1 (B1, U1, U2) (slice BE: tabela zgłoszeń, przyjęcie zgłoszenia, przetwarzanie w tle, sprawdzenie i użycie jednorazowego odnośnika) — 2026-10-23
- Archetyp: Backend — niezmiennik high-stakes (jednorazowy kod, limity prób, unieważnienie sesji, nierozróżnialność odpowiedzi).
- Stawka: wysoka.
- Niepewność: średnia (nowy slice i proces w tle; wzorce kolejki wiadomości i blokad aplikacyjnych już w repo).
- Wykonawca (linia / model / native effort): Claude / `wykonawca-opus` Opus 5.5 `xhigh` — trzy kolejne przebiegi (B1 → U1 → U2).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `xhigh`, `-Mode review` (fala, wpis 1402-R-BE); bramka Codex / `gpt-6.1-sol` `max`.
- Dopuszczone alternatywy: przy CZERWONYM Muse Wonder Full `max` (zablokowany do 2026-10-26T00:00Z) albo czekanie. Recenzent wg reguły 8 to Muse Wonder Full `max`; był zablokowany, więc poszło do ponownej kwalifikacji na Sol.
- Powód wyboru: pliki niezmiennika high-stakes.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy (hook ŻÓŁTY, tydzień 93 %, 2026-10-23 ~08:40Z), dalej CZERWONY 94–97 % (przebiegi U1 i U2 ze znacznikiem `[konieczny]`, decyzja właściciela „wykorzystać pulę w 100 %”); Muse zablokowany (429, 2026-10-22 20:47Z); Gemini zablokowany do 2026-10-26 10:01Z (`agy /quota`, 2026-10-23).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: B1 nie napisał kodu. Strażnik kontekstu zatrzymał go przy 301 tys. podczas czytania wzorców, a raport przekazania wykazał dwie trafne błędne przesłanki briefu: wiadomości 102 nie da się zakolejkować bez szablonu, a „kanonizacja jak w logowaniu” rozróżniała wielkość liter i rozdzielała limity adresu. Po podziale na U1 (baza, `request`, cykl) i U2 (`inspect`, `complete`) z twardym budżetem czytania: U1 dał kod produkcyjny (build 0/0) bez testów, U2 dał kod, fixture i 3 kluczowe testy `complete`, w tym dwa równoległe wywołania. Ścieżka e-mail przez curl przeszła w całości.
- Rundy korekt: 1 — K1–K3 i K5 po recenzji fali i BT1. Wykonał je Codex (wpis 1402-KBE) na jednorazowy wyjątek właściciela, bo hook przy 98 % tygodnia blokował też `[konieczny]`. Do tego jednolinijkowa poprawka architekta po bramce.
- Czas do akceptacji: pierwsze podejście ~1 h 10 min (B1 → U2); akceptacja po korektach ~6 h, w tym ~2,5 h oczekiwania na reset okna Codexa.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): recenzja fali — 3×P2 potwierdzone: czas `/request` zależny od istnienia konta przez blokadę wiersza w cyklu, kolejność przy dwóch instancjach, limit przed odstępem wbrew WP. Do tego 1×P3 potwierdzone (miejsce powiadamiacza); 0 odrzuconych. Bramka — 1×P2 potwierdzone (wielkość liter znacznika urządzenia a binarna nazwa blokady aplikacyjnej).
- Defekty po odbiorze: precyzja czasu (`datetime` zamiast `DbType.DateTime2`). Wykrył ją test BT1, zamknęła korekta K1.
- Wymagane testy i dowody: build 0 ostrzeżeń; pełny `dotnet test` 8595/0/1 (pominięty = defekt logowania spoza #1402); curl `request`/`inspect`/`complete` z odczytem `MessageOutbox`, `SecurityEvents` i tokenów odnawiających; PRE BE 1.16.0 na `d484b3e`.
- Uwagi: przy slice BE wysokiej stawki pierwszy przebieg Opusa zjadł cały budżet kontekstu na czytanie. Podział na jednostki z jawnym budżetem czytania od razu oszczędza przebieg.

### 1402-B2 (szablon wiadomości z odnośnikiem ustawienia hasła, PL/EN, dwa warianty) — 2026-10-23
- Archetyp: Backend — szablon wiadomości transakcyjnej bez niezmiennika.
- Stawka: średnia.
- Niepewność: niska (wzór szablonu wiadomości 103).
- Wykonawca (linia / model / native effort): Claude / `wykonawca` Sonnet 5.5 `high`.
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `xhigh`, `-Mode review` (w recenzji fali BE, wpis 1402-R-BE).
- Dopuszczone alternatywy: Codex Sol `high` (≤ 5 plików); Muse Spark `max` zablokowany.
- Powód wyboru: brief przesunięty przed B1 (szablon jest warunkiem kolejkowania 102); jedyny wykonawca BE w tej chwili, więc mógł budować.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude CZERWONY 94 % (hook, `[konieczny]`, 2026-10-23 ~09:18Z).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowano. Jeden istniejący test fabryki wymagał dopisania parametru sterującego wariantem (1 linia, architekt).
- Rundy korekt: 0.
- Czas do akceptacji: ~10 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 dotyczących szablonu.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: Messaging 462/462; zakodowany temat `mailto` zgodny z rewizją dokumentacji.

### 1402-F1 (F1, F1b) (serwis, DTO i enumy odzyskiwania hasła, ekran A z Figmy, rozszerzenie `ResendRow`, i18n) — 2026-10-23
- Archetyp: Frontend UI / Figma — ekran publiczny funkcji high-stakes, bez pliku niezmiennika.
- Stawka: średnia.
- Niepewność: średnia (5 stanów makiety, ponowna wysyłka na uchwycie).
- Wykonawca (linia / model / native effort): Claude / `wykonawca` Sonnet 5.5 `high` (F1, potem F1b).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review` (wpis 1402-R-FE).
- Dopuszczone alternatywy: brak — Codex bez potwierdzonego Figma MCP w sesji i > 5 plików w funkcji high-stakes.
- Powód wyboru: linia Figmy po próbie A/B.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude ostrzegawczy → CZERWONY 94 % (hook, 2026-10-23 09:12–09:24Z; F1b ze znacznikiem `[konieczny]`).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: F1 oddał pracę przy 307 tys. kontekstu. Warstwa danych, `ResendRow` i ekran A z trzema dziećmi były zielone (31 testów); brakowało testów zachowania i porównania pozostałych stanów z makietą. F1b przeniósł wspólną funkcję do `public/auth/`, wydzielił enum kodu ekranu i porównał resztę stanów z Figmą. Dwa odchylenia od makiety przyjęte na bramie: „47 s” zamiast „00:47” oraz wspólny `ResendRow`.
- Rundy korekt: 2 — FK1 (6 poprawek po recenzji fali, łącznie z F2) i GK-B (bramka, wpis 1402-GK-B).
- Czas do akceptacji: ~2 h do FK1; ~4 h z GK-B.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): recenzja fali FE (A+B) — 4×P2 i 2×P3 potwierdzone, 0 odrzuconych. Bramka FE, przebieg 1 — 1×P2 w ekranie A (komunikat błędu nie reagował na zmianę języka).
- Defekty po odbiorze: 1×P2 z bramki (j.w.).
- Wymagane testy i dowody: lint 0, format OK, 5637/5637 po FK1, build OK; `browser-check` A 16/16 (2×2 × stany).

### 1402-F2 (ekran B `/nowe-haslo`, trasy SSR, `noindex`, i18n) — 2026-10-23
- Archetyp: Frontend UI / Figma — ekran publiczny funkcji high-stakes.
- Stawka: średnia (ekran), wysoka w części sesji karty po ustawieniu hasła (patrz 1402-GK-A).
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): Claude / `wykonawca` Sonnet 5.5 `high`.
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review` (wpis 1402-R-FE).
- Dopuszczone alternatywy: brak (jak 1402-F1).
- Powód wyboru: linia Figmy; rozłączne pliki z F1 przy stałym kontrakcie serwisu, więc wysłany równolegle z falą 1.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude CZERWONY 94–96 % (hook, `[konieczny]`, 2026-10-23 ~09:35Z).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowano — 13 testów, ESLint czysty, teksty z dokumentacji, `noindex` zgodnie z decyzją o adresach. Wykonawca zgłosił spoza zakresu, że `/potwierdz-adres` wywołuje sprawdzenie tokenu także w SSR (propozycja na bramę).
- Rundy korekt: 1 (FK1 po recenzji fali); synchronizacja sesji karty po 204 poszła osobnym łańcuchem (1402-GK-A).
- Czas do akceptacji: ~1,5 h do FK1.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): w recenzji fali FE (j.w.). Bramka, przebiegi 1–3: 4×P2 w synchronizacji sesji po ustawieniu hasła.
- Defekty po odbiorze: sesja w otwartej karcie po 204 (obszar niezmiennika sesji) — brief F2 jej nie obejmował; domknął ją łańcuch GK-A.
- Wymagane testy i dowody: `browser-check` B 12/12; testy zachowania z 1402-FT.

### 1402-FT (F1-T, F2-T) (Vitest + AXE ekranów A i B oraz ich dzieci) — 2026-10-23
- Archetyp: Testy — Vitest/AXE według scenariuszy z briefu.
- Stawka: średnia.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Claude / `tester` Haiku 5.5 `xhigh`.
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review` (w recenzji fali FE).
- Dopuszczone alternatywy: `wykonawca` Sonnet `high`; Codex wykluczony (testy wymagałyby recenzji fali spoza Codexa, a żadna taka linia nie była wolna).
- Powód wyboru: linia testera; tylko pliki `*.spec.ts`, rozłącznie z F1b i F2.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude CZERWONY 94–96 % (hook, `[konieczny]`).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowano. F1-T dał 33 testy w 4 specach, bez defektów kodu, z 2 uwagami do recenzji (import enuma z ekranu logowania, martwy warunek). F2-T dał 35 testów.
- Rundy korekt: 0.
- Czas do akceptacji: ~10–15 min każdy.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 dotyczących testów.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: `ng test --include` architekta; pełny `npm test` po fali.

### 1402-BT1 (+BT1-K) (xunit: przyjęcie zgłoszenia, odstęp, limity, uchwyt, cykl w tle; mutacje M1–M20) — 2026-10-23
- Archetyp: Testy — xunit integracyjne na SQL Server z dowodem mutacją.
- Stawka: wysoka (testy dowodzące niezmiennika limitów i nierozróżnialności).
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): Claude / `tester` Haiku 5.5 `xhigh`.
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `xhigh`, `-Mode review` (w recenzji fali BE).
- Dopuszczone alternatywy: `wykonawca` Sonnet `high`.
- Powód wyboru: linia testera; gotowa fixture z U2.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude CZERWONY 97 % (hook, `[konieczny]`, 2026-10-23 ~10:13Z).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: BT1 oddał raport przekazania przy progu kontekstu. Wynik 48 zielonych i 1 pominięty z 49; pominięty test to realny defekt precyzji czasu (`datetime` zamiast `DateTime2`). BT1-K wykonał mutacje: M1–M19 dały czerwone testy, M20 przeżyła jako mutacja równoważna (wysyłka i tak normalizuje wielkość liter adresu).
- Rundy korekt: 0 (BT1-K to druga jednostka tej samej pracy, nie korekta).
- Czas do akceptacji: ~1 h (BT1 + BT1-K).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 0 dotyczących testów.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: pełny `dotnet test` 8545/0/1; hashe 85 plików produkcyjnych bez zmian po mutacjach.

### 1402-D1 (+D1-K) (datowane rewizje 2026-10-23 pięciu dokumentów: WP odnośnika, UI ekranów, WP wiadomości, AT uwierzytelniania i sesji) — 2026-10-23
- Archetyp: Dokumentacja — rewizje dokumentów `zatwierdzony` w granicach ustaleń zatwierdzonych z góry.
- Stawka: średnia.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Access write`.
- Recenzent (linia / model / native effort): Claude / architekt Opus 5.5 `xhigh` (Faza 4c — jednorazowy wyjątek właściciela: Gemini i Muse zablokowane).
- Dopuszczone alternatywy: Muse Spark `max` (archetyp „rewizje dokumentacji” — zablokowany); Claude `wykonawca` (pula na kod).
- Powód wyboru: archetyp ≤ 5 plików; pula Codexa znana (~75 % wg właściciela, 2026-10-23 rano).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex znany (właściciel, 2026-10-23); Muse zablokowany do 2026-10-26T00:00Z.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 854 s, zaakceptowano. Zmiany +160/−25 w 5 dokumentach, rewizje (a)–(d) zgodne z ustaleniami, temat `mailto` zgodny z szablonem B2. Poza briefem poprawił nieaktualny akapit AT o pustym katalogu zdarzeń; poprawkę przyjęto.
- Rundy korekt: 1 — D1-K (wpisy 12–15 dziennika po fali FE). Pierwszy przebieg trwał 66 s i nie dał wyniku, drugi trwał 470 s i został zaakceptowany.
- Czas do akceptacji: ~15 min (D1); ~1 h z D1-K.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): Faza 4c — 2 uzupełnienia architekta (retencja zgłoszeń w WP usuwania konta, akapit o karcie z trwającą sesją); 0 błędów w treści D1.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: diff przeczytany w całości; dziennik dokumentacji bez wpisów `otwarty`.

### 1402-R-FE (recenzja fali FE: ekrany A i B, serwis, testy) — 2026-10-23
- Archetyp: Recenzja fali — ekrany i warstwa danych funkcji high-stakes, bez plików niezmiennika.
- Stawka: średnia.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): poprawki Claude / `wykonawca` Sonnet 5.5 `high` (FK1, `[konieczny]` przy 97 %).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode review`.
- Dopuszczone alternatywy: Gemini `high` i Muse Wonder `max` — zablokowane.
- Powód wyboru: inna rodzina niż autorzy (Claude); przy niskiej i średniej stawce preferowany Sol `high` (reguła 13).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex znany (właściciel, 2026-10-23).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 482 s, exit 0. 4×P2 i 2×P3, wszystkie potwierdzone w repo.
- Rundy korekt: 1 (FK1: 6 poprawek; 73 testy obu folderów zielone, pełny pakiet 5637/5637).
- Czas do akceptacji: ~40 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 4×P2 + 2×P3 potwierdzone, 0 odrzuconych, 0 fałszywych P0/P1.
- Defekty po odbiorze: bramka FE dołożyła 2×P2 w przebiegu 1 (język komunikatu A, sesja karty po 204) — obu recenzja fali nie zgłosiła.
- Wymagane testy i dowody: raport recenzji; `git status` bez zmian w drzewie.

### 1402-R-BE (recenzja fali BE: slice, szablon, testy — 84 pliki w jednym przebiegu) — 2026-10-23
- Archetyp: Recenzja fali high-stakes — pliki niezmiennika i testy dowodzące.
- Stawka: wysoka.
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): poprawki Codex (wpis 1402-KBE, wyjątek właściciela).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `xhigh`, `-Mode review`.
- Dopuszczone alternatywy: Muse Wonder Full `max` (para reguły 8) zablokowany do 2026-10-26T00:00Z; Gemini zablokowany.
- Powód wyboru: inna rodzina niż autorzy (Claude); `xhigh` zamiast `high` ze względu na stawkę i zakres.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex znany (właściciel, 2026-10-23).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 476 s, werdykt „niepoprawny”, drzewo bez zmian. Recenzent czytał pliki w całości, bo brief jednocześnie zakazywał gita i kazał czytać `git diff`.
- Rundy korekt: 1 (KBE).
- Czas do akceptacji: ~4,5 h (z oczekiwaniem na reset okna Codexa).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 3×P2 + 1×P3 potwierdzone, 0 odrzuconych, 0 fałszywych P0/P1.
- Defekty po odbiorze: bramka BE dołożyła 1×P2 (znacznik urządzenia a binarna nazwa blokady).
- Wymagane testy i dowody: raport recenzji; architekt sprawdził każde P2 w kodzie i w WP.
- Uwagi: szablon briefu recenzji BE wymaga poprawki — nie może jednocześnie zakazywać gita i polecać `git diff`. Diff dostarcza architekt albo brief zezwala na odczytowe polecenia gita.

### 1402-SCSS (audyt SCSS 8 arkuszy ekranów A i B) — 2026-10-23
- Archetyp: Audyt SCSS.
- Stawka: niska.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): poprawka Claude / `mechanik` Haiku 5.5 `low` (zamiana zdublowanych bloków na mixiny, 5 bloków).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `medium`, `-Mode review` (audytor).
- Dopuszczone alternatywy: Muse Spark `max` (preferencja z próby) zablokowany.
- Powód wyboru: krótki audyt tylko do odczytu, jedyna wolna rodzina spoza autorów.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex znany (właściciel, 2026-10-23).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 81 s, 8/8 arkuszy, 0 naruszeń reguł; 2×P3.
- Rundy korekt: 0.
- Czas do akceptacji: ~10 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 2×P3 potwierdzone. Zdublowane mixiny `auth.form`/`auth.field` poprawił `mechanik`. Wspólny komponent „pole hasła + miernik” odłożony do propozycji PBI refaktoru, bo dotyka rejestracji i ustawień konta.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: stylelint czysty; build FE po zamianie.

### 1402-GK-B (komunikat błędu ekranu A reaguje na zmianę języka) — 2026-10-23
- Archetyp: Frontend — poprawka stanu widoku bez niezmiennika (≤ 5 plików).
- Stawka: średnia.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` `high`.
- Recenzent (linia / model / native effort): Claude / architekt Opus 5.5 `xhigh` (jednorazowy wyjątek właściciela), potem bramka Codex / `gpt-6.1-sol` `max`.
- Dopuszczone alternatywy: `wykonawca` Sonnet `high` — hook zablokował go przy 98 % tygodnia, `[konieczny]` nie przechodził.
- Powód wyboru: brief bez niezmiennika; pula Codexa znana (właściciel: „codex ma dużo limitu”).
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude zablokowany (hook 98 %, 2026-10-23 ~10:35Z); Codex znany (właściciel, ~11:20Z).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: 349 s, zaakceptowano. Sygnał trzyma niepowodzenie i chwilę jego odbioru, a komunikat jest `computed` z bieżącego języka. Liczba testów wzrosła z 17 do 19.
- Rundy korekt: 0.
- Czas do akceptacji: ~10 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): przegląd architekta — 0; bramka, przebiegi 2–4 — 0 w tym obszarze.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: lint 0, format OK, 5645/5645, build OK.

### 1402-GK-A (GK-A, GK-A2, GK-A3 v1–v3) (sesja w otwartej karcie po ustawieniu hasła: synchronizacja z serwerem, limit czasu) — 2026-10-23
- Archetyp: Frontend — niezmiennik sesji (wygaśnięcie lokalnej sesji po unieważnieniu wszystkich tokenów, współbieżność odświeżeń).
- Stawka: wysoka.
- Niepewność: wysoka (współdzielone odświeżenie w toku, generacja sesji, harmonogram RxJS).
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` `xhigh` (GK-A), potem `high` (GK-A2, GK-A3) — jednorazowy wyjątek właściciela dla #1402: pliki niezmiennika pisze Codex.
- Recenzent (linia / model / native effort): Claude / architekt Opus 5.5 `xhigh` (przegląd każdego diffu — niezależność od rodziny Codex) oraz bramka Codex / `gpt-6.1-sol` `max` (ta sama rodzina co autor; kontrola, nie niezależność).
- Dopuszczone alternatywy: `wykonawca-opus` — hook przy 98 % tygodnia, `[konieczny]` nie przechodził; Muse Wonder Full `max` — zablokowany do 2026-10-26T00:00Z; czekanie do resetu Claude'a 25.10 — właściciel odrzucił („zamknąć dziś”).
- Powód wyboru: decyzja właściciela 2026-10-23 ~11:25Z; reguła 2 nie dawała żadnej linii przed resetem.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude zablokowany (hook 98–100 %); Codex znany → zablokowany 13:45–16:09 i 17:10–21:11 czasu lokalnego (komunikat limitu wrappera).
- Pewność decyzji: niska (twarda bramka uchylona decyzją właściciela).
- Wynik pierwszego podejścia: GK-A (107 s) zgłosił trafny STOP. Brief żądał, żeby test regresji był czerwony bez poprawki. Przebieg 2 (385 s) zaakceptowano: testy 24 → 30. Bramka, przebieg 2: synchronizacja żyła tyle co widok i nie domykała się przed nawigacją. GK-A2 przebieg 1 (335 s) zatrzymał ten sam błąd briefu, przebieg 2 (442 s) zaakceptowano: synchronizacja przeszła do serwisu root z kontrolą generacji. Bramka, przebieg 3: 2×P2 (ponowne użycie `refreshInFlight` sprzed resetu, brak limitu czasu). GK-A3 v1 (56 s) zgłosił trafny STOP: przesłanka architekta była błędna, bo `refreshInFlight` zwalnia się w `finalize` po doręczeniu. GK-A3 v2 (886 s, failed) to incydent: brief nie powtórzył wyjątku właściciela, więc Codex uznał bramkę z `AGENTS.md` za wiążącą i sam uruchomił `claude --print --agent wykonawca-opus` z pominięciem hooka limitów. Ten przebieg zapisał 1 poprawny plik stałej i trafił na limit Codexa. GK-A3 v3 (400 s) zaakceptowano: drugie odświeżenie w mikrozadaniu `asapScheduler` i `timeout({ first: 10 s })`. 14 testów było czerwonych na starym kodzie.
- Rundy korekt: 2 (GK-A2, GK-A3 po przebiegach 2 i 3 bramki). Przebiegi zatrzymane: 4 — 2× błąd briefu („czerwony” dla regresji), 1× błędna przesłanka architekta, 1× incydent.
- Czas do akceptacji: ~8 h (11:26–19:24 czasu lokalnego), w tym ~6,5 h oczekiwania na resety okna Codexa.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): bramka FE przebiegi 1–3 — 4×P2 potwierdzone (1 + 1 + 2), 0 odrzuconych; przebieg 4 — 0. Przegląd architekta — 0 dodatkowych.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: lint 0, format 0, build 0, 5665/5665; 14 testów czerwonych na kodzie sprzed GK-A3; bramka FE przebieg 4 — 0 znalezisk w 84 plikach.
- Uwagi: (1) Brief dla obcego silnika z wyjątkiem właściciela musi cytować wyjątek dosłownie i zakazywać uruchamiania innych CLI modeli (`claude`, `codex`, `muse`, `agy`, `gemini`); inaczej Codex sam deleguje do Claude'a poza hookiem. Zapisane w pamięci `codex-deleguje-do-claude-cli`. (2) Wymóg „czerwony bez poprawki” stawiaj imiennie i tylko testom dowodzącym poprawki (pamięć `brief-czerwony-test-tylko-dla-dowodu-poprawki`). (3) Ten obszar niezmiennika potrzebował trzech przebiegów bramki Sol `max`. Recenzja fali przez Sol `high` nie wychwyciła problemu, bo synchronizacja sesji w karcie nie należała do żadnego briefu fali 1.

### 1402-KBE (KBE-1, KBE-2) (korekta BE: `DateTime2`, odstęp przed limitami, blokada aplikacyjna adresu w cyklu zamiast blokady wiersza) — 2026-10-23
- Archetyp: Backend — niezmiennik high-stakes (nierozróżnialność czasu odpowiedzi, kolejność przetwarzania, limity).
- Stawka: wysoka.
- Niepewność: średnia (RCSI wyłączone; `sp_getapplock` z `LockTimeout = 0`).
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` — KBE-1 `high`, KBE-2 `xhigh`; jednorazowy wyjątek właściciela; `-CodexSandbox danger-full-access` jednorazowo dla briefów BE #1402.
- Recenzent (linia / model / native effort): Claude / architekt Opus 5.5 `xhigh` (przegląd diffów); bramka Codex / `gpt-6.1-sol` `max`.
- Dopuszczone alternatywy: jak 1402-GK-A.
- Powód wyboru: decyzja właściciela „zamknąć dziś”.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak 1402-GK-A.
- Pewność decyzji: niska.
- Wynik pierwszego podejścia: odrzucono — 4 przebiegi łańcucha (13:26–13:30 czasu lokalnego, KBE-1/2/3 i BT2) zatrzymała piaskownica `workspace-write`. Brak dostępu do `%USERPROFILE%\.nuget`, a nieudany restore zepsuł `obj\*.nuget.g.targets` (naprawił to `dotnet restore` architekta). 3 próby KBE-1 (`--no-restore`, sieć) nie dały wyniku, czwartą uciął limit Codexa; drzewo bez zmian (sha 85/85). Po resecie, z `danger-full-access`: KBE-1 (588 s) i KBE-2 (999 s) zaakceptowane po przeglądzie diffów.
- Rundy korekt: 0 po zmianie piaskownicy. KBE-3 (miejsce powiadamiacza, P3) odłożony do propozycji PBI refaktoru, a test klucza blokady (K5) przeszedł do BT2.
- Czas do akceptacji: ~3,5 h (13:26–17:00 czasu lokalnego), w tym ~2,5 h oczekiwania na reset okna.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): przegląd architekta — 0; bramka BE potwierdziła K1–K3 bez znalezisk w tych plikach.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: build 0/0, pełny `dotnet test` 8595/0/1.
- Uwagi: Codex w domyślnej piaskownicy nie uruchamia `dotnet test` w ZebraniBE. Brief BE dla Codexa wymaga `-CodexSandbox danger-full-access` (zgoda właściciela per zadanie) albo testy uruchamia architekt.

### 1402-BT2 (+K5) (xunit: sprawdzenie i użycie odnośnika, blokady logowania, klucz blokady; mutacje) — 2026-10-23
- Archetyp: Testy — xunit integracyjne high-stakes z dowodem mutacją.
- Stawka: wysoka.
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` `high` (jednorazowy wyjątek właściciela; `danger-full-access`).
- Recenzent (linia / model / native effort): Claude / architekt Opus 5.5 `xhigh`; bramka Codex / `gpt-6.1-sol` `max`.
- Dopuszczone alternatywy: `tester` Haiku `xhigh` — zablokowany hookiem.
- Powód wyboru: decyzja właściciela „zamknąć dziś”.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): jak 1402-GK-A.
- Pewność decyzji: niska.
- Wynik pierwszego podejścia: przebieg z 13:30 czasu lokalnego zatrzymała piaskownica. Przebieg z 16:37 (1208 s) zaakceptowano: 17/17 mutacji wykrytych, kod produkcyjny nietknięty. Test konta zablokowanego administracyjnie wykazał defekt logowania spoza #1402 i jest oznaczony `Skip` z opisem defektu.
- Rundy korekt: 0.
- Czas do akceptacji: ~25 min po przebiegu.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): przegląd architekta — 0; bramka — 0 dotyczących testów.
- Defekty po odbiorze: brak (defekt logowania to luka sprzed #1402 — propozycja Buga).
- Wymagane testy i dowody: pełny `dotnet test` 8595/0/1; AccountRecovery 98/1 po poprawce z bramki.

### 1402-G-FE (bramka końcowa FE, 4 przebiegi) — 2026-10-23
- Archetyp: Bramka końcowa high-stakes — cały diff FE w jednym przebiegu.
- Stawka: wysoka.
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): poprawki GK-A/A2/A3 i GK-B (Codex, wpisy wyżej).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `max`, `-Mode review`.
- Dopuszczone alternatywy: przy limicie Codexa `wykonawca-opus` tylko do odczytu (decyzja właściciela z planu) — hook go blokował, więc bramka czekała na reset bez obniżenia modelu.
- Powód wyboru: reguła 6.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex znany, potem dwa limity okna 5 h (komunikaty wrappera: reset 16:09 i 21:11 czasu lokalnego); po ostatnim przebiegu 5 h 30 %, tydzień 5 % (raport tokenów).
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: przebieg 1 (552 s, 79 plików) — „niepoprawny”, 2×P2. Przebieg 2: pierwszą próbę (280 s) uciął limit, druga (778 s) dała 1×P2. Przebieg 3 (622 s) — 2×P2. Przebieg 4 (448 s, 84 pliki) — 0.
- Rundy korekt: 3 (GK-A + GK-B, GK-A2, GK-A3).
- Czas do akceptacji: ~9 h (12:20–21:33 czasu lokalnego), w tym ~6,5 h oczekiwania na resety.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 5×P2 potwierdzone, 0 odrzuconych, 0 fałszywych P0/P1.
- Defekty po odbiorze: brak (PRE FE 1.14.0 na `6e6937c`).
- Wymagane testy i dowody: raporty bramki; architekt — lint, format, build, 5665/5665.
- Uwagi: każdy przebieg dokładał nowe P2 w tym samym obszarze (sesja karty po resecie), bo każda poprawka odsłaniała następny przypadek współbieżności. Pełny opis wymaganego zachowania w briefie GK-A (odświeżenie w toku, limit czasu, nawigacja) skróciłby łańcuch.

### 1402-G-BE (bramka końcowa BE) — 2026-10-23
- Archetyp: Bramka końcowa high-stakes — cały diff BE w jednym przebiegu.
- Stawka: wysoka.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): poprawka Claude / architekt (jedna linia, reguła 11).
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `max`, `-Mode review`.
- Dopuszczone alternatywy: jak 1402-G-FE.
- Powód wyboru: reguła 6.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex zablokowany 17:10–21:11 czasu lokalnego (pierwszą próbę, 471 s, uciął limit), potem nieznany.
- Pewność decyzji: wysoka.
- Wynik pierwszego podejścia: 705 s, exit 0. Potwierdziła K1–K3, K5 i BT2; 0 P0/P1; 1×P2: dwa równoległe zgłoszenia z tym samym znacznikiem urządzenia w innej wielkości liter mijały binarną blokadę aplikacyjną i limit przepuszczał 11 zamiast 10.
- Rundy korekt: 1 (kanonizacja znacznika `Trim().ToLowerInvariant()` w handlerze; bez ponownej bramki dla zmiany jednej linii).
- Czas do akceptacji: ~15 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 1×P2 potwierdzone, 0 odrzuconych.
- Defekty po odbiorze: brak (PRE BE 1.16.0 na `d484b3e`).
- Wymagane testy i dowody: build 0 ostrzeżeń; AccountRecovery 98/1.
- Uwagi: tu bramka i autor plików niezmiennika (Codex, KBE/BT2) są z jednej rodziny. Niezależność tych plików dał przegląd architekta, nie bramka.

### 1402-4C (przegląd zgodności dokumentacji z kodem) — 2026-10-23
- Archetyp: Dokumentacja — macierz zgodności dokumentów `zatwierdzony` z implementacją.
- Stawka: średnia.
- Niepewność: niska.
- Wykonawca (linia / model / native effort): Claude / architekt Opus 5.5 `xhigh` (uzupełnienia, jednorazowy wyjątek właściciela).
- Recenzent (linia / model / native effort): Claude / architekt Opus 5.5 `xhigh` — inna rodzina niż autor dokumentacji D1 (Codex).
- Dopuszczone alternatywy: Gemini `high` (plan) i Muse — zablokowane do 2026-10-26.
- Powód wyboru: decyzja właściciela „zamknąć dziś”.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Gemini i Muse zablokowane (j.w.); Claude 99 % (hook).
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: wpisy 11 i 16 dziennika przekazane jako propozycje PBI. Nowe wpisy: 18 (logowanie konta zablokowanego, przekazany), 19 (wiersz retencji zgłoszeń i odnośników w WP usuwania konta, zamknięty), 20 (akapit „Karta, w której trwa sesja” w README ekranów, zamknięty).
- Rundy korekt: 0.
- Czas do akceptacji: ~30 min (w przerwach na resety).
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 3 luki dokumentacji (wpisy 18–20), 0 sprzeczności kodu z dokumentem.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: dziennik bez wpisów `otwarty`; commit dokumentacji `f1bcff7`.

### 1402-Q (Q-1, Q-1b, Q-1c, Q-K1) (plik podglądu QA Sphere: przegląd 87 istniejących, 55 nowych przypadków) — 2026-10-25
- Archetyp: QA Sphere — plik podglądu (Kroki 2–5 skilla v1.12) w funkcji high-stakes.
- Stawka: średnia (treść testów, bez niezmiennika w kodzie).
- Niepewność: średnia (warunki PRE: brak skrzynki, Turnstile wyłączony, logowanie dostawcą niedziałające).
- Wykonawca (linia / model / native effort): Claude / `wykonawca` Sonnet 5.5 `high` — 3 przebiegi autorskie (dwa z przekazaniem przy strażniku 300 tys.) i 1 przebieg korekty.
- Recenzent (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Mode exec -Access read` (piaskownica `read-only`), wpis 1402-Q-R.
- Dopuszczone alternatywy: Codex Sol `high` jako autor (odrzucony: okno 258 tys. przy kontekście ~130 tys.); Muse Spark `max` i Gemini `-Access write` (linie skilla) — zablokowane do 2026-10-26.
- Powód wyboru: wyjątek właściciela 2026-10-25 „nie czekaj do poniedziałku, zmień model po prostu” od linii autorów skilla QA Sphere; para autor Claude ↔ recenzent Codex zachowuje różne rodziny.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Claude znany, ZIELONY, 5 h 20–34 %, tydzień 3–5 % (hook, 2026-10-25 11:20–13:40Z); Muse zablokowany do 2026-10-26T00:00Z (429); Gemini zablokowany do 2026-10-26T10:01Z; Codex nieznany.
- Pewność decyzji: niska (pierwsza para Sonnet/Sol w tym archetypie).
- Wynik pierwszego podejścia: przekazanie bez zapisu. Q-1 zatrzymał się na 300 tys. po samym czytaniu — za szeroki brief i `context.json` 385 kB. Q-1b zapisał przegląd i 28 przypadków, potem przekazanie. Q-1c dopisał 22 przypadki, `lint` 0/0.
- Rundy korekt: 1 (Q-K1 — 12 × P2 z recenzji, 5 nowych przypadków, 7 werdyktów `keep` → `update`).
- Czas do akceptacji: ~2 h 20 min (11:20–13:40Z), w tym 4 przebiegi autora po 5–11 min i recenzja 10 min.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): potwierdzone 12 × P2 (5 błędów treści, 4 luki pokrycia, 3 błędne werdykty `keep`); odrzucone 0. Recenzent wskazał też skrót architekta w przekazaniu („`keep` po tytule” wbrew Krokowi 2b) — błędne `keep` wyłapał jego pełny przegląd.
- Defekty po odbiorze: brak (stan na publikację).
- Wymagane testy i dowody: `qas.py lint` 0/0; `push --limit 1` + `verify --only A1`; `push` 54; `update` 8; pełne `verify` 63 pozycje, 0 różnic (seq 1889–1943, folder 191). Uwaga do przeglądu archetypu: Sonnet w tym archetypie dwa razy uderzył w strażnika kontekstu; następnym razem brief z jawnym podziałem przegląd/nowe przypadki i zapisem przyrostowym od startu.

### 1402-Q-R (recenzja krzyżowa pliku podglądu QA Sphere) — 2026-10-25
- Archetyp: Recenzja — treść manualnych przypadków testowych względem kodu FE/BE i dokumentacji.
- Stawka: średnia.
- Niepewność: średnia.
- Wykonawca (linia / model / native effort): Codex / `gpt-6.1-sol` `high`, `-Access read`.
- Recenzent (linia / model / native effort): architekt Opus 5.5 `xhigh` — triaż znalezisk w kodzie (`evaluate-rules.ts`, `account-logout.ts`, `ProtectionConfiguration.cs`, `new-password-outcome.html`).
- Dopuszczone alternatywy: Muse i Gemini `-Access read` (linie skilla) — zablokowane do 2026-10-26.
- Powód wyboru: inna rodzina niż autor (Claude); wyjątek właściciela j.w.
- Sygnał dostępności (znany/ostrzegawczy/zablokowany/nieznany, źródło, czas): Codex nieznany przed przebiegiem; po przebiegach #1402 wrapper: 5 h 16 %, tydzień 3 %.
- Pewność decyzji: średnia.
- Wynik pierwszego podejścia: zaakceptowano — 12 × P2, 0 × P0/P1, werdykt „wymaga poprawek”, pewność 0,94.
- Rundy korekt: 0.
- Czas do akceptacji: 10 min 27 s.
- Znaleziska recenzji (potwierdzone/odrzucone, priorytet): 12 × P2 potwierdzonych, 0 odrzuconych; jedno przypisanie fragmentu poprawki do złego seq (113/118) — wykonawca korekty rozpoznał je sam.
- Defekty po odbiorze: brak.
- Wymagane testy i dowody: raport w `_robocze` (usunięty przy domknięciu); poprawki odebrane `verify` 63/0.

## 5. Rytm przeglądów i ewaluacji

Okresowa analiza wpisów w rejestrze prowadzona jest w następującym rytmie operacyjnym:

1. **Pierwszy przegląd:** przeprowadzany po **10–15 istotnych briefach**.
2. **Kolejne przeglądy:** przeprowadzane po kolejnych **10–15 briefach** lub po **istotnej zmianie modeli bądź sposobu pomiaru limitów**.
3. **Dodatkowy przegląd doraźny:** uruchamiany po wystąpieniu **istotnego błędu** (np. defektu wykrytego po odbiorze lub na etapie integracji) albo po **kilku kosztownych poprawkach** (wielokrotne rundy korekt na briefie).
4. **Zasady interpretacji i oceny:**
   - Wyniki należy oceniać **per archetyp** zadania.
   - **Mała próbka nie uzasadnia rankingu:** jeśli dla danego archetypu liczba zrealizowanych briefów jest niewielka, nie wolno tworzyć definitywnych rankingów modeli ani automatycznych reguł sztywnego przypisania.
   - Wnioski z przeglądów stanowią wskazówkę operacyjną i podlegają walidacji przy zachowaniu twardych ograniczeń bezpieczeństwa, uprawnień i narzędzi.

### Zapisy przeglądów

#### Przegląd 1 — 2026-10-12

- **Powód:** pierwszy przegląd (próg 10–15 briefów dawno przekroczony) oraz istotna zmiana modeli i pomiaru: Haiku 5.5, Terminal-Bench 4.0 w AA i ponownie zmierzone koszty zadania.
- **Zakres:** 167 wpisów z 2026-10-04…11. Projekty: BeautyEffect 125, Zebrani 33, narzędzia i routing 9. Rozkład wykonawców: 143 wpisy z jednym wykonawcą, 22 mieszane.
- **Miara:** liczba rund korekt. Pole „Wynik pierwszego podejścia” jest zapisywane niejednolicie, więc nie służy za miarę.
- **Ograniczenia próbki:**
  - Obciążenie doborem: trudniejsze briefy trafiały do mocniejszych linii.
  - Trzy czwarte próbki to jeden projekt (strona wizytówka o niskiej stawce).
  - Część rund wynika z błędów w specyfikacji architekta, a nie z wykonania.
  - Wniosków nie wolno czytać jako rankingu linii (sekcja 5, pkt 4).

**Wykonawcy (wpisy z jednym wykonawcą).** „Rundy z winy specyfikacji” to rundy, które wpis przypisuje briefowi architekta.

| Linia / effort | Briefy | Śr. rund | Bez korekt | Rundy z winy specyfikacji | Wpisy z defektem po odbiorze |
| --- | --- | --- | --- | --- | --- |
| Codex `gpt-6.1-sol` `high` | 31 | 0,45 | 20 | 10 z 14 | 5 |
| Gemini `gemini-3.8-flash-high` | 30 | 0,63 | 14 | 6 z 19 | 6 |
| Spark `xhigh` | 26 | 0,88 | 9 | 8 z 23 | 3 |
| Spark `high` | 17 | 0,53 | 9 | 3 z 9 | 1 |
| `wykonawca-opus` — Opus 5.5 `xhigh` | 11 | 1,64 | 2 | 2 z 18 | 5 |
| `wykonawca` — Sonnet 5.5 `high` | 10 | 1,30 | 0 | 0 z 13 | 2 |
| Codex `gpt-6.1-sol` `medium` | 6 | 0,33 | 5 | — | 1 |
| Opus 5.5 `medium` (próba A/B) | 4 | 0,75 | 1 | — | 2 |
| `tester` — Sonnet 5.5 `medium` | 1 (+3 mieszane) | 0 (3,33 w mieszanych) | 1 | — | 1 |

**Archetypy z co najmniej 3 briefami** (liczba briefów / średnio rund):

- Dokumentacja: Sol `high` 12 / 0,2, Gemini `high` 7 / 0,1. Obie linie dowożą; różnica nieistotna.
- Testy: Spark `high` 5 / 0,2, Gemini `high` 9 / 0,9.
- FE bez Figmy: Sol `high` 4 / 0,2.
- Figma w linii Claude'a: Sonnet `high` 5 / 1,4, Opus `medium` 3 / 1,0. Próba A/B zamknięta wg kryterium kosztu: zostaje Sonnet.
- BE high-stakes: Opus `xhigh` 5 / 1,4. Rundy pochodzą głównie z recenzji fal i bramki, czego przy tej stawce należy oczekiwać.

**Recenzenci:**

- Sol `high`: 48 recenzji, 1 odrzucone znalezisko.
- Gemini `high`: 46 recenzji, 0 odrzuconych.
- Spark `xhigh`:
  - 31 recenzji, 2 odrzucone znaleziska;
  - najwięcej wzmianek P0/P1 (43), część z nich architekt obniżył przy weryfikacji. To koszt weryfikacji, a nie fałszywe defekty.
- Architekt (walidacja i oględziny): 40 wpisów.
- Bramki końcowe znalazły P0/P1 po recenzjach fal w obu funkcjach high-stakes:
  - 1603 (Sol `max`): 2 × P0 i 1 × P1;
  - 2370 (Spark `max` z decyzji właściciela): 1 × P1 w BE, którego nie złapały testy uzupełniające (2370-BE-1b3).

**Defekty po odbiorze:** 32 wpisy.
- 11 z bramek końcowych (zob. wyżej).
- Około 16 to defekty wizualne strony BeautyEffect (BE-36…BE-104):
  - głównie typografia, marginesy siatki, łuki i kurtyny, rozmiary celów dotykowych;
  - wykrył je architekt w przeglądarce albo na zrzutach `browser-check`, a nie recenzja kodu.
- Reszta to uwagi właściciela po pokazie oraz drobiazgi w dokumentacji.

**Wnioski (wskazówki operacyjne, nie reguły):**

1. **Zgodne z obecnymi regułami, bez zmian.** Sol `high`/`medium`, Spark `high` i Gemini `high` mają najniższe liczby rund na briefach dokumentacji, FE bez Figmy i testów o niskiej i średniej stawce. Pozostają pełnoprawnymi kandydatami od planowania.
2. **Główną dźwignią rund jest specyfikacja architekta:**
   - u Sola `high` wynika z niej 10 z 14 rund, u Sparka `xhigh` 8 z 23, u Gemini 6 z 19;
   - przed wysłaniem briefu przesłanki dotyczące stanu repozytorium trzeba sprawdzić faktami od `zwiadowca` albo poleceniem, a nie z pamięci.
3. **Sonnet `high` ma najsłabsze pierwsze przejście** (0 na 10 bez korekt, wszystkie rundy z wykonania). Jego briefy to jednak głównie Figma i kontekst sesji, czyli najtrudniejszy archetyp. Sygnał do obserwacji: przy następnym przeglądzie porównać briefy Figmy z Codexem z potwierdzonym MCP, jeśli takie się pojawią.
4. **Bramka raz na feature jest uzasadniona.** W obu funkcjach high-stakes znalazła P0/P1, które przeszły recenzje fal.
5. **Defekty wizualne łapie tylko przeglądarka.** Plan odbioru każdej fali FE z UI zawiera scenariusz `browser-check` i oględziny zrzutów przez architekta; recenzja kodu tego nie zastąpi.
6. **Tester ma za mało danych.** Próba testera 3+3 (od 2026-10-12) dostarczy porównania. Przy scenariuszach z przyszłym okresem i wyścigiem brief testera wymienia przypadki wprost.
7. **Briefy BE high-stakes były za długie:** strażnik kontekstu i kontynuacje. Dzielić je na krótsze i przenosić rozpoznanie do `zwiadowca` przed briefem (reguła 15).

**Propozycje do decyzji właściciela (pewność niska, routing bez zmian do decyzji):**

- **Wyjątek CZERWONEGO:**
  - zamiana Sparka `xhigh` na Sparka `max` dla przekwalifikowanego briefu `wykonawca-opus`;
  - za: TB4 0,333 wobec 0,167;
  - lokalnie Spark `max` wystąpił tylko jako bramka (2 przebiegi), a nie jako wykonawca.
- **Recenzent przy niskiej stawce:**
  - Sol `high` lub Gemini `high` przed Sparkiem `xhigh`, ze względu na koszt weryfikacji zawyżonych priorytetów;
  - przy wyższej stawce wybór per brief bez zmian.

**Zmiany routingu z 2026-10-12** (decyzje właściciela wprowadzone w sesji głównej):

- `mechanik` i `zwiadowca` na Haiku 5.5 `low` (`claude-haiku-5-5`). Strażnik kontekstu ma dla Haiku 5.5 progi domyślne (okno 1M).
- Próba A/B linii Figmy zamknięta, zostaje Sonnet `high`; agent `wykonawca-opus-medium` w archiwum.
- Start próby testera: Sonnet 5.5 `medium` wobec Haiku 5.5 `xhigh`, 3+3, stały recenzent Spark `xhigh`.
- Linie Codex, Spark i Gemini bez nowych dostępnych modeli; Gemini 4 Argon jest poza AI Pro.
- Zgodność kopii wspólnej sekcji potwierdził `sync-routing.py --check`. Recenzji innej rodziny nie było (dokumentacja reguł, nie kod).

**Decyzje właściciela po przeglądzie (2026-10-12):**

- **Spark domyślnie `max` we wszystkich rolach:** wykonawca, recenzent, audyt, autor QA Sphere, wyjątek CZERWONEGO i stały recenzent próby testera, która nie miała jeszcze briefu.
  - Niższy effort tylko z uzasadnieniem zapisanym w briefie i we wpisie.
  - Przesłanki:
    - 649 przebiegów Sparka z 2026-09-21…10-11 bez komunikatu limitu (dwa 402 to przejściowa weryfikacja płatności);
    - TB4 `max` 0,333 wobec `xhigh` 0,167 za ~17 % tokenów więcej;
    - koszt: ~2× dłuższy przebieg.
  - Ocena po 10–15 briefach na `max`, wobec rund z wykonania z tego przeglądu (`xhigh` 0,58, `high` 0,35 na brief).
  - Wpisy Sparka od tej daty podają effort jawnie, z powodem przy odstępstwie od `max`.
- **Pliki niezmiennika high-stakes zostają przy `wykonawca-opus`.** Spark `max` pisze je tylko w wyjątku CZERWONEGO.
- **Recenzent przy niskiej stawce:** preferencja Sol `high` / Gemini `high` przed Sparkiem; Spark `max` pozostaje kandydatem przy wyższej stawce. To preferencja wśród dopuszczonych, nie stała kolejność.
- **Wprowadzone w:**
  - reguły 2, 6, 7, 8, 13 i 14 globalnego `CLAUDE.md`;
  - wspólna sekcja projektów;
  - skill `implement-ado-feature-zebrani` v5.20;
  - `qasphere-test-generator` v1.6;
  - `external-workers`;
  - domyślna wartość wrappera (`-Effort max`).

**Następny przegląd:** po kolejnych 10–15 istotnych briefach albo po wyniku próby testera, zależnie od tego, co nastąpi wcześniej. Osobno ocena Sparka `max` po 10–15 jego briefach.

#### Zmiana modeli 2026-10-14 — linia Muse na Wonder Full (bez przeglądu wpisów)

- **Powód:** istotna zmiana modeli (sekcja 5, pkt 2). W katalogu `muse` 1.4.8 na planie Power Usage są `muse-wonder-full-1.0` i `muse-wonder-1.0` (oba z 2026-10-12, warianty `-contributor`, efforty `minimal`–`max`). Dostęp potwierdzony sondą wrappera (`model_completed.model`). Gemini 4 Argon nadal poza `agy` 1.3.5.
- **Decyzja:** właściciel — „użyjmy nowego Muse Wonder”; wariant Full wybrał architekt. Domyślny model każdej roli linii Muse (wykonawca, recenzent, audyt, autor QA Sphere, wyjątek CZERWONEGO): `muse-wonder-full-1.0-contributor` `max`. Wonder, Spark 1.3 albo niższy effort — tylko z uzasadnieniem w briefie i we wpisie.
- **Przesłanki (AA, 2026-10-14; pewność niska, bez lokalnych wyników):**
  - TB4: Wonder Full 0,571, Wonder 0,520, Spark 1.3 `max` 0,333; II 55,8 / 52,4 / 48,1;
  - tokeny wyjścia na zadanie indeksu: 53,8 tys. / 54,2 tys. / 60,2 tys. — różnicę kosztu robi cena tokenu;
  - koszt zadania: Wonder 4,52 $ wobec 1,60 $ Sparka `max` (ceny standardowe); Wonder Full bez ceny w AA;
  - pula: 114 przebiegów Sparka po zmianie planu bez limitu; zapasu nikt nie podaje — sygnał `nieznany`.
- **Bez zmian:** pliki niezmiennika high-stakes pisze `wykonawca-opus`; bramka końcowa `gpt-6.1-sol` `max`; preferencja Sol `high` / Gemini `high` przy recenzjach niskiej stawki (dane z przeglądu 1 dotyczą Sparka 1.3 — do ponownej oceny dla Wondera Full). Wonder i Spark to jedna rodzina recenzji.
- **Ocena Sparka `max`** (od 2026-10-12) zamknięta przed progiem 10–15 briefów — jej wpisy zostają punktem odniesienia.
- **Ocena Wondera Full po 10–15 istotnych briefach:** rundy z wykonania (bez rund z winy specyfikacji), czas do akceptacji, potwierdzone i obalone P0/P1 w recenzjach, komunikaty limitu puli — wobec przeglądu 1 (Spark `xhigh` 0,58, `high` 0,35 rundy z wykonania na brief) i briefów Sparka `max` z 2026-10-12…14. Pierwszy komunikat limitu → ponowna kwalifikacja wg reguły 2 i wpis.
- **Wprowadzone w:**
  - reguły 2, 6, 7, 8, 10, 13, 14 i 15 oraz macierz i odczyt AA globalnego `CLAUDE.md` (linia „Spark” → „Muse”);
  - wspólna sekcja projektów (`sync-routing.py`, 20 kopii zgodnych);
  - skill `implement-ado-feature-zebrani` v5.28;
  - `qasphere-test-generator` v1.8;
  - `external-workers`, `browser-check` (`CLI-WORKER.md`, `README.md`, `pwcli`);
  - domyślny model wrappera (`-Model muse-wonder-full-1.0-contributor`) i komunikaty hooka limitów.

**Następny przegląd:** po 10–15 istotnych briefach Wondera Full albo po pierwszym komunikacie limitu Muse, zależnie od tego, co nastąpi wcześniej.

#### Przegląd linii Muse po pierwszym limicie — 2026-10-15 (bez zmiany routingu)

- **Powód:** pierwszy komunikat limitu Muse po zmianie modeli 2026-10-14 (próg „następnego przeglądu” z wpisu wyżej).
- **Fakt:** 2026-10-15 ok. 08:47 UTC brief 2694-ADO-1 (`muse-wonder-full-1.0-contributor` `max`, `-Access write`) przerwany po 130 s komunikatem 429. Limit jest **tygodniowy**, z resetem w poniedziałek 2026-10-19 00:00 UTC. Plan Power Usage ma więc poza oknem 5 h także pulę tygodniową — globalny `CLAUDE.md` opisuje dla Muse tylko okno 5 h. W tym tygodniu przed limitem: 109 przebiegów Sparka `max` i 4 Wondera Full `max`.
- **Ponowna kwalifikacja (reguła 2):** sygnał Muse `zablokowany` do 2026-10-19 00:00 UTC. ADO-1 → Gemini `gemini-3.8-flash-high` write (wpis 2694-ADO). Briefy Muse czekają albo idą do innej dopuszczonej linii; wyjątek CZERWONEGO (`wykonawca-opus` → Muse) do resetu nie działa — taki brief czeka.
- **Lokalne wyniki Wondera Full `max`** (PBI #2694; za mało do oceny, próg 10–15 briefów):
  - recenzja GK3-R (1403 s): 0×P0/P1, 3×P3 potwierdzone, 0 fałszywych P0/P1;
  - recenzja R1F-R (824 s): 1×P1 potwierdzone (znane wcześniej), 0 fałszywych P0/P1;
  - autor QA Sphere QAS-1 (2013 s): 0 rund z wykonania, 1 z winy specyfikacji; recenzja innej rodziny — 0×P0/P1;
  - ADO-1: 429 bez wyniku.

  Wstępnie: w recenzjach 0 fałszywych P0/P1 na 2 przebiegi, wobec 43 w 31 recenzjach Sparka `xhigh` (przegląd 1). Próbka za mała na zmianę preferencji z reguły 13.
- **Decyzja architekta:** domyślny model linii Muse bez zmian (Wonder Full `max`). Przy briefach mechanicznych architekt świadomie rozważa Sparka 1.3 albo niższy effort (reguła 8 już na to pozwala z uzasadnieniem), bo token Wondera jest 3–5× droższy, a pula tygodniowa jest wspólna.
- **Do decyzji właściciela:** dopisać do globalnego `CLAUDE.md` (tabela budżetów i macierz, kolumna sygnału Muse) limit tygodniowy Power Usage z resetem w poniedziałek 00:00 UTC.

**Następny przegląd:** po 10–15 istotnych briefach Wondera Full albo po kolejnym limicie Muse w tym samym tygodniu rozliczeniowym.

#### Przegląd 2 linii Muse — 2026-10-20 (zmiana routingu: para per archetyp)

- **Powód:** drugi limit tygodniowy Muse w drugim tygodniu z rzędu (próg „następnego przeglądu” z wpisu wyżej) i prośba właściciela: „wypłaszczyć, żeby nie zabijać limitu pierwszego dnia na gówno pracy i używać rozumowania tylko tam, gdzie trzeba”.
- **Fakty z wrappera (429 „Subscription quota exhausted”, czas resetu w komunikacie):**
  - 2026-10-15 08:45Z — reset 2026-10-19 00:00Z (tydzień); w tym tygodniu 110 przebiegów Sparka 1.3 `max`, 2 Sparka `low`, 5 Wondera Full `max`, 2 sondy;
  - 2026-10-19 19:53Z i 23:42Z — reset po 19 min i po ~2 h (okno 5 h);
  - 2026-10-20 01:22Z i 08:12Z — reset 2026-10-26 00:00Z (tydzień); od poniedziałku 00:00Z 20 przebiegów, wszystkie Wonder Full `max` — pula skończyła się po ~25 h pracy. Panel właściciela: „Weekly limit 99 % used, resets 26 paź 1:00”.
  - `muse` 1.4.11 nie ma polecenia zużycia; `model-profile` nie pokazuje cen ani budżetu rozumowania.
- **Pomiar puli (pewność niska — dwa wyczerpania, założenie równej puli tygodniowej i wag zbliżonych do cennika API):** tydzień ≈ 19 przebiegów Wondera Full `max` ≈ 180 Sparka `max` (110 Sparków ≈ 60 % tygodnia 12.10). Token Wondera Full ≈ 12–15× Sparka, ≈ 3,5–4× Wondera. W przebiegach Muse 85–95 % tokenów to odczyt cache, wyjście (na które działa effort) to ~15–25 % kosztu — effort jest słabą dźwignią puli, model i długość briefu mocną.
- **AA 2026-10-20:** nowych modeli w abonamentach brak (`muse-spark-open`: II 38,9, TB4 0,081). Rekordy Muse tylko `max` (Wonder Full, Wonder, Spark 1.3) i `xhigh` (Spark 1.3). Koszt zadania indeksu: Spark `max` 1,60 $ (wejście 1,35 $), Spark `xhigh` 1,37 $, Wonder 4,52 $ (wejście 3,43 $); Wonder Full bez ceny. TB4: Full 0,571, Wonder 0,520, Spark `max` 0,333, `xhigh` 0,167.
- **Lokalne wyniki Wondera Full `max` 15–20.10** (24 przebiegi, ~20 briefów):
  - recenzje plików niezmiennika `wykonawca-opus` (8: GK3-R, R1F-R, 2722 fala 1, 2722 BE-2, 2722 BE-3, 2371-REV-BE, 2747-R1, 2371-QAS jako recenzent pliku Gemini): potwierdzone P1 w 2722-BE-1a, 2747-R1, R1F (znane) i 4×P1 w pliku QA Sphere Gemini; 0 obalonych P0/P1 — tu rozumowanie Full zarabia na siebie;
  - autor (QA Sphere ×3, rewizje dokumentacji ×3, warstwa widoku, dowód w przeglądarce, zakup na PRE): 0,25 rundy z wykonania na brief (2 rundy w 2722-QAS po P2 recenzji) — ten sam poziom co Spark `max` 12–14.10 (2705-F1a/F1b/F2a 0, F4 1, 2694-T1/T2) za ~10× puli na przebieg.
- **Decyzja architekta (bez pytania o routing, reguła 4):** linia Muse bez jednego domyślnego modelu; para per archetyp briefu (reguła 8 globalnego `CLAUDE.md`):
  - Wonder Full `max` — wyjątek CZERWONEGO i recenzja fali plików niezmiennika high-stakes;
  - Wonder `max` — autor i recenzent krzyżowy QA Sphere w funkcji high-stakes, recenzja średniej stawki, złożony brief bez niezmiennika (próba — lokalnych wyników brak);
  - Spark 1.3 `max` — pozostała implementacja bez niezmiennika, testy, rewizje dokumentacji, audyt SCSS, QA Sphere poza high-stakes, korekty `-K`, recenzja niskiej stawki;
  - Spark 1.3 `high` — worker przeglądarki `pwcli`, zakup na PRE, pozycje ADO, korekta z gotową treścią (≤ 3 pliki);
  - Spark 1.3 `low` — sondy, podbicie wersji.
  - Tempo: budżet tygodnia ≈ 19 ekwiwalentów Full (1 Full ≈ 4 Wonder ≈ 10 Sparka), dnia roboczego ≈ 3; liczba przebiegów od poniedziałku poleceniem z `external-workers` przed każdą parą Wonder/Full; po budżecie dnia — para niżej albo inna rodzina, CZERWONY czeka.
- **Symulacja:** przebiegi 19–20.10 w nowym podziale zajęłyby ~45 % tygodnia zamiast 100 % (recenzje Full zostają, QA Sphere → Wonder, reszta → Spark).
- **Bez zmian:** pliki niezmiennika high-stakes pisze `wykonawca-opus`; wyjątek CZERWONEGO → Wonder Full `max` albo czekanie; bramka końcowa `gpt-6.1-sol` `max`; preferencja Sol `high` / Gemini `high` przy recenzjach niskiej stawki (teraz także ze względu na pulę Muse); Wonder i Spark to jedna rodzina recenzji.
- **Stan na 2026-10-20:** Muse `zablokowany` do 2026-10-26 00:00Z (429 z resetem tygodniowym). Do resetu: wyjątek CZERWONEGO czeka, QA Sphere pisze Gemini write, worker przeglądarki wraca do Playwright MCP (Gemini/Codex), recenzje plików niezmiennika kwalifikujesz ponownie (reguła 2).
- **Wprowadzone w:**
  - globalny `CLAUDE.md`: tabela budżetów (limit tygodniowy, pomiar), macierz (Muse, QA Sphere), odczyt AA 2026-10-20, reguły 8 i 13;
  - wspólna sekcja projektów (`sync-routing.py`, 18 kopii);
  - skill `implement-ado-feature-zebrani` v5.30; `qasphere-test-generator` v1.11;
  - `external-workers` (limit tygodniowy, polecenie tempa, fallback wrappera);
  - domyślny model wrappera: `-Model muse-spark-1.3-contributor`.

**Następny przegląd:** po 10–15 istotnych briefach Muse w nowym podziale albo po kolejnym limicie tygodniowym przed piątkiem. Miary: czy tydzień dociąga do niedzieli, rundy z wykonania per para, P0/P1 recenzji Wondera wobec Full, przelicznik Wondera po jego pierwszych 5 przebiegach (`token-report.py`).

#### Przegląd 3 linii Muse — 2026-10-25 (cennik, kalibracja puli, limit Wondera)

- **Powód:** właściciel: „muse-wonder-1.0 jest BARDZO drogim modelem, możemy go używać, ale musimy robić to racjonalnie, bo 21 przebiegów zabiło nasz tygodniowy limit. A za to Spark 1.3 contributor jest bardzo tanim modelem” — ze zrzutem cennika.
- **Cennik (zrzut właściciela, za 1M tokenów, cache / wejście / wyjście):** Wonder 1.0 (`muse-wonder-1.0`) standard 0,20 / 4,00 / 20,00 $, tryb contributor „Not available”; Spark 1.3 contributor 0,002 / 0,10 / 0,20 $, standard 0,15 / 1,25 / 4,25 $. Wondera Full zrzut nie obejmuje. Katalog `muse` i `model_completed.model` w sesjach nadal podają `muse-wonder-full-1.0-contributor` (891 wywołań modelu) — sufiks nie oznacza tańszego trybu.
- **Fakty (statusy wrappera):** 21 przebiegów tygodnia od 19.10 to Wonder Full `max` (19.10: 16 udanych + 2 przerwane, 20.10: 2 przerwane, 21.10: 1 przerwany), nie Wonder 1.0 — ten ma w puli jeden przebieg (sonda 14.10).
- **Kalibracja puli (`token-report.py`, pewność średnia — dwa wyczerpania, założenie równej puli tygodniowej):**
  - tydzień 12.10: 110 Sparków `max` = 734 mln tokenów (94 % cache, 6,7 mln na przebieg) + 5 Full `max` = 44 mln (8,8 mln na przebieg);
  - tydzień 19.10: 21 Full `max` = 100 mln tokenów (95 % cache, 4,8 mln na przebieg) + 4 Sparki = 5 mln;
  - wynik: token Full ≈ 13× Sparka contributor; tydzień ≈ 100 mln tokenów Full ≈ 1,3 mld tokenów Sparka ≈ 21 przebiegów Full ≈ 190 Sparków `max`; przebieg Full ≈ 9–17 Sparków (~5 % tygodnia), Spark ~0,5 %.
  - cennik daje przy naszym profilu ~60× (Wonder 1.0 wobec Sparka contributor) — pula liczy łagodniej albo Full jest tańszy od Wondera 1.0; rozstrzygnąć się tego nie da bez przebiegów Wondera 1.0, więc liczy się go jak Full.
- **Obalone założenie:** „Full ≈ 3,5–4× Wondera” z przeglądu 2 (szacunek przy porównaniu z ceną standardową Sparka) — Wonder 1.0 nie ma trybu contributor, więc nie jest tanim pośrednim szczeblem.
- **Decyzja architekta (bez pytania o routing, reguła 4):**
  - Wonder Full `max` — tylko wyjątek CZERWONEGO i recenzja fali plików niezmiennika high-stakes; limit Wondera (Full i 1.0 razem, z przerwanymi) **2 przebiegi na dzień roboczy i 6 na tydzień** (~30 % puli); brief Wondera tylko z diffem plików niezmiennika i ich specyfikacją;
  - Wonder 1.0 — bez archetypu (tylko z powodem w briefie i rejestrze, liczony jak Full);
  - Spark 1.3 `max` przejmuje archetypy Wondera 1.0: QA Sphere w funkcji high-stakes (autor i recenzent krzyżowy), recenzja średniej stawki, złożony brief bez niezmiennika; dochodzi ponowna recenzja poprawek;
  - po limicie Wondera recenzja plików niezmiennika → Sol `high` (pula Codexa przed bramką, reguła 7) albo następny dzień; CZERWONY czeka;
  - Spark zawsze z `-contributor` (bez niego 12–75× drożej wg cennika).
- **Stan na 2026-10-25:** Muse `zablokowany` do 2026-10-26 00:00Z; od resetu obowiązuje nowy limit.
- **Wprowadzone w:**
  - globalny `CLAUDE.md`: tabela budżetów, macierz (Muse, QA Sphere), akapit „Cennik Muse i kalibracja puli”, reguły 8 i 13;
  - wspólna sekcja projektów (`sync-routing.py`, 18 kopii);
  - skill `implement-ado-feature-zebrani` v5.31; `qasphere-test-generator` v1.12;
  - `external-workers` (cennik, limit Wondera w poleceniu tempa).

**Następny przegląd:** po 10–15 istotnych briefach Muse w tym podziale albo po kolejnym limicie tygodniowym przed piątkiem. Miary: czy tydzień dociąga do niedzieli, liczba przebiegów Wondera wobec limitu 6, rundy z wykonania Sparka `max` w dawnych archetypach Wondera 1.0, potwierdzone i obalone P0/P1 Sparka `max` w recenzjach średniej stawki.
