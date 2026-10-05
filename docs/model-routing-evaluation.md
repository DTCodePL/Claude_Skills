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

## 5. Rytm przeglądów i ewaluacji

Okresowa analiza wpisów w rejestrze prowadzona jest w następującym rytmie operacyjnym:

1. **Pierwszy przegląd:** przeprowadzany po **10–15 istotnych briefach**.
2. **Kolejne przeglądy:** przeprowadzane po kolejnych **10–15 briefach** lub po **istotnej zmianie modeli bądź sposobu pomiaru limitów**.
3. **Dodatkowy przegląd doraźny:** uruchamiany po wystąpieniu **istotnego błędu** (np. defektu wykrytego po odbiorze lub na etapie integracji) albo po **kilku kosztownych poprawkach** (wielokrotne rundy korekt na briefie).
4. **Zasady interpretacji i oceny:**
   - Wyniki należy oceniać **per archetyp** zadania.
   - **Mała próbka nie uzasadnia rankingu:** jeśli dla danego archetypu liczba zrealizowanych briefów jest niewielka, nie wolno tworzyć definitywnych rankingów modeli ani automatycznych reguł sztywnego przypisania.
   - Wnioski z przeglądów stanowią wskazówkę operacyjną i podlegają walidacji przy zachowaniu twardych ograniczeń bezpieczeństwa, uprawnień i narzędzi.
