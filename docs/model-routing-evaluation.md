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

## 5. Rytm przeglądów i ewaluacji

Okresowa analiza wpisów w rejestrze prowadzona jest w następującym rytmie operacyjnym:

1. **Pierwszy przegląd:** przeprowadzany po **10–15 istotnych briefach**.
2. **Kolejne przeglądy:** przeprowadzane po kolejnych **10–15 briefach** lub po **istotnej zmianie modeli bądź sposobu pomiaru limitów**.
3. **Dodatkowy przegląd doraźny:** uruchamiany po wystąpieniu **istotnego błędu** (np. defektu wykrytego po odbiorze lub na etapie integracji) albo po **kilku kosztownych poprawkach** (wielokrotne rundy korekt na briefie).
4. **Zasady interpretacji i oceny:**
   - Wyniki należy oceniać **per archetyp** zadania.
   - **Mała próbka nie uzasadnia rankingu:** jeśli dla danego archetypu liczba zrealizowanych briefów jest niewielka, nie wolno tworzyć definitywnych rankingów modeli ani automatycznych reguł sztywnego przypisania.
   - Wnioski z przeglądów stanowią wskazówkę operacyjną i podlegają walidacji przy zachowaniu twardych ograniczeń bezpieczeństwa, uprawnień i narzędzi.
