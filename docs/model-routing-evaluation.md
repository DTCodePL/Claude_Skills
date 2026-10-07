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

## 5. Rytm przeglądów i ewaluacji

Okresowa analiza wpisów w rejestrze prowadzona jest w następującym rytmie operacyjnym:

1. **Pierwszy przegląd:** przeprowadzany po **10–15 istotnych briefach**.
2. **Kolejne przeglądy:** przeprowadzane po kolejnych **10–15 briefach** lub po **istotnej zmianie modeli bądź sposobu pomiaru limitów**.
3. **Dodatkowy przegląd doraźny:** uruchamiany po wystąpieniu **istotnego błędu** (np. defektu wykrytego po odbiorze lub na etapie integracji) albo po **kilku kosztownych poprawkach** (wielokrotne rundy korekt na briefie).
4. **Zasady interpretacji i oceny:**
   - Wyniki należy oceniać **per archetyp** zadania.
   - **Mała próbka nie uzasadnia rankingu:** jeśli dla danego archetypu liczba zrealizowanych briefów jest niewielka, nie wolno tworzyć definitywnych rankingów modeli ani automatycznych reguł sztywnego przypisania.
   - Wnioski z przeglądów stanowią wskazówkę operacyjną i podlegają walidacji przy zachowaniu twardych ograniczeń bezpieczeństwa, uprawnień i narzędzi.
