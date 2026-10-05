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

## 5. Rytm przeglądów i ewaluacji

Okresowa analiza wpisów w rejestrze prowadzona jest w następującym rytmie operacyjnym:

1. **Pierwszy przegląd:** przeprowadzany po **10–15 istotnych briefach**.
2. **Kolejne przeglądy:** przeprowadzane po kolejnych **10–15 briefach** lub po **istotnej zmianie modeli bądź sposobu pomiaru limitów**.
3. **Dodatkowy przegląd doraźny:** uruchamiany po wystąpieniu **istotnego błędu** (np. defektu wykrytego po odbiorze lub na etapie integracji) albo po **kilku kosztownych poprawkach** (wielokrotne rundy korekt na briefie).
4. **Zasady interpretacji i oceny:**
   - Wyniki należy oceniać **per archetyp** zadania.
   - **Mała próbka nie uzasadnia rankingu:** jeśli dla danego archetypu liczba zrealizowanych briefów jest niewielka, nie wolno tworzyć definitywnych rankingów modeli ani automatycznych reguł sztywnego przypisania.
   - Wnioski z przeglądów stanowią wskazówkę operacyjną i podlegają walidacji przy zachowaniu twardych ograniczeń bezpieczeństwa, uprawnień i narzędzi.
