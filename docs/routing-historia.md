# Historia routingu — archiwum globalnego CLAUDE.md

> **Nie jest to plik normatywny.** Obowiązują wyłącznie reguły w `~/.claude/CLAUDE.md`
> (oraz streszczenie „Working Mode” w plikach reguł projektów). Tutaj leżą dane
> historyczne, które wcześniej zajmowały większość globalnego pliku: datowane
> odczyty Artificial Analysis, tabele i porównania kosztu, przebiegi prób,
> uzasadnienia dawnych decyzji i kalibracje pul. Czytasz je przy przeglądzie
> routingu (reguła 13) i przed zmianą reguły — nie przy zwykłym briefie.
>
> **Część 1** to dosłowna kopia globalnego `CLAUDE.md` z 2026-11-01 sprzed diety
> instrukcji (67 188 B, kopia też w `~/.claude/kopie/2026-11-01/CLAUDE.md`).
> Reguły w niej zapisane są nieaktualne tam, gdzie nowy plik je zmienił —
> rozstrzyga zawsze plik normatywny. Nowe pomiary i odczyty dopisujesz w części 2
> (datowane, najnowsze na górze), nie w pliku normatywnym.

## Część 2 — pomiary i odczyty od 2026-11-01 (najnowsze na górze)

### 2026-11-01 — kalibracja czterech pul (analiza workflow i routingu)

- **Claude (Max 5×):** pula tygodnia ≈ 1 230 $ ekwiwalentu API (regresja przyrostów procentu tygodnia z `historia.jsonl` na koszt tokenów, R² 0,67); wagi licznika: odczyt cache ≈ 1,0× ceny API, zapis ≈ 1,2×, wyjście ≈ 0,6× — Opus nie liczy się ciężej niż cennik. Zapotrzebowanie przy dotychczasowym tempie ≈ 1 750 $ / 7 dni (luka ≈ 30 %). Podział kosztu 14 dni (2 239 $): sesje główne 68 %, `wykonawca-opus` ≈ 22 %, `wykonawca` ≈ 9 %, `tester` ≈ 1 %; w kosztach architekta PBI wysokiej stawki 72 % (26 z 31 PBI rejestru to wysoka stawka). Tydzień resetuje się w niedzielę 04:00.
- **Muse (Power Usage):** tydzień padł przy 40,3 $ (tydz. 19.10, sam Wonder) i 45,5 $ (tydz. 26.10: Wonder 39,5 $ z 17 przebiegów + Spark 6,0 $ ze 188) po cenniku z 2026-10-25 → tydzień ≈ 40–46 $, okno 5 h ≈ 13–14,5 $. Wonder Full ≈ 2,3 $ / przebieg (≈ 5 % tygodnia), Spark `max` ≈ 0,03 $ (≈ 0,07 %) — ~70× taniej, nie 10×. Kalibracja „tydzień ≈ 190 Sparków” pochodziła z 12.10 (dzień zmiany planu, pula padła przy ~22 $) i zawyżała koszt Sparka ~7×. 29.10: CZERWONY Claude'a → 10 przebiegów Wondera jednego dnia → Muse zablokowany do 2026-11-02. `muse usage --json` istnieje (1.4.14), dziś zwraca `server_sent_no_usage`.
- **Codex (Plus):** `codex app-server` → `account/rateLimits/read` podaje okno 5 h i tydzień z `usedPercent` i `resetsAt` bez tury modelu. 2026-11-01: 5 h 9 %, tydzień 78 % (reset czw. 5.11 22:06); darmowy pełny reset (tydzień + 5 h) ważny do 2026-11-30. Od 05.10 tylko trafienia okna 5 h.
- **Google AI Pro (`agy` 1.4.12):** `agy models` pokazuje tylko Gemini 3.8 Flash, Claude 4.6 i GPT-OSS (te dwa znikają 2.11); Gemini 4 Argon i Claude 5.5 wg dokumentacji Antigravity tylko na płatnym / nie-próbnym planie. `agy -p "/quota"` w trybie bez interfejsu nie działa. Druga licencja do automatycznego przełączania kont: nie kupować (brak wyboru konta w `agy`, ryzyko blokady konta wg forum).
- **Research R1–R4** (`D:\projects\DTCode\_robocze\routing-2026-11-research\`, do sprzątnięcia po zamknięciu): tańsi recenzenci tracą czułość, nie precyzję — stąd przebieg obalający P0/P1; słabe wyrocznie testowe; orkiestrator Sonnet wobec Opusa 7/2/1 przy 0,49× kosztu (źródło zewnętrzne, mała próba).
- **Muse natywnie na Windows** (`muse` 1.4.14, `%LOCALAPPDATA%\Programs\muse`): bez `--no-foreign-personal-context` sesja wczytuje globalny `~/.claude/CLAUDE.md` jako reguły i skille z `~/.claude/skills` / `~/.codex/skills` (sonda `--provider echo`, bez zużycia puli); z flagą — 0 wystąpień, MCP (5 serwerów) i 10 skilli jak w WSL.

---

## Część 1 — globalny CLAUDE.md z 2026-11-01 (dosłownie)
# Zasady globalne — dobór silnika do zadania

**Polityka nadrzędna — adaptacyjny dobór per brief (2026-10-04).**
Te reguły obowiązują wszystkie projekty DTCode i ich projektowe streszczenia
FE/BE. Skille projektowe (kanoniczne skille ADO projektów) muszą być z nimi
zgodne; rejestr `D:\projects\DTCode\Claude_Skills\docs\model-routing-evaluation.md`
jest wspólny dla projektów.
Macierz opisuje dopuszczalność i możliwości, nie stały przydział zwykłych
briefów do silnika. Architekt sam wybiera silnik, model i native effort;
nie pyta użytkownika o routing. Odpowiada za plan, samodzielny brief,
dowody i końcową akceptację. W pilotażu architektem pozostaje Opus `xhigh`.

**Dowody jakości.** Główną przesłanką są lokalne wyniki zaakceptowanych
podobnych briefów: pierwsze przejście, rundy korekt, czas do akceptacji,
potwierdzone i odrzucone znaleziska oraz wymagane testy/PRE. Publiczne
rankingi, ceny i indeksy są wyłącznie pomocniczym kontekstem; nie
rozstrzygają samodzielnie ani nie kompensują niespełnionej twardej bramki.
Bez danych lokalnych zachowujesz wymagany poziom jakości i ryzyka,
oznaczasz pewność jako niską i nie tworzysz rankingu z małej próbki.


Mam do dyspozycji **cztery niezależne silniki na czterech abonamentach** (czwarty,
Gemini, w pilocie od 2026-09-23). Przy każdym
zadaniu wymagającym pracy wykonawczej rozważam, **który z nich ma je wykonać** —
zanim zacznę robić je sam lub odruchowo sięgnę po subagenta Claude'a.

Dane do routingu: **API Artificial Analysis** —
`GET https://artificialanalysis.ai/api/v2/data/llms/models`, nagłówek
`x-api-key: <klucz w ~/.claude/CLAUDE.md; w archiwum usunięty>`. Każdy effort to osobny rekord
(`gpt-6-1-sol-high` — w AA z łącznikiem zamiast kropki; rekord bez przyrostka = najwyższy effort modelu: `max` u Claude'a, GPT i Muse, `high` u Gemini Flash); koszt zadania indeksu jest
tylko na stronie modelu (`artificialanalysis.ai/models/<slug>`).

## Budżety — cztery osobne kieszenie

| Silnik         | Abonament            | Jak liczony                                                                                                                                                                                             | Co kosztuje                          |
| -------------- | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| Claude         | Max 5× (~$100)       | okno 5 h + **jeden wspólny limit tygodniowy** na wszystkie modele i apki — **największa pula w wartościach bezwzględnych**                                                                              | model **i** effort (tokeny × cena)   |
| Muse (`muse`)  | Power Usage (189 zł/mies., od 2026-10-12; wcześniej High, $15) | **tokenami** w przesuwnym oknie 5 h **i w limicie tygodniowym z resetem w poniedziałek 00:00 UTC** (429 „Subscription quota exhausted” podaje czas resetu: 2026-10-15 i 2026-10-20 → reset pon. 00:00Z = tydzień, 2026-10-19 → reset po 19 min = okno 5 h); 20× pula planu Everyday; cennik za 1M tokenów (zrzut właściciela 2026-10-25): Spark 1.3 contributor 0,002 $ cache / 0,10 $ wejście / 0,20 $ wyjście (standard 0,15 / 1,25 / 4,25 $), Wonder 1.0 **tylko standard** 0,20 / 4,00 / 20,00 $ — trybu contributor dla Wondera nie ma, choć katalog i `model_completed.model` podają `-contributor`; Wondera Full w cenniku brak. Tydzień w liczbach (kalibracja `token-report.py` na dwóch wyczerpaniach, 2026-10-25, pewność średnia): ~21 przebiegów Wonder Full `max` (tydzień 19.10: 21 przebiegów, 100 mln tokenów) albo ~190 Sparka 1.3 `max` (tydzień 12.10: 110 przebiegów, 734 mln tokenów ≈ 60 % tygodnia) — token Full ≈ 13× Sparka contributor, przebieg Wondera ≈ 10 przebiegów Sparka (~5 % tygodnia). Katalog od 2026-10-14 (sonda wrappera): `muse-wonder-full-1.0`, `muse-wonder-1.0` (oba z 2026-10-12) i `muse-spark-1.3`, każdy z wariantem `-contributor`; efforty `minimal`–`max`; `none` CLI odrzuca, `ultra` ma zamkniętą bramkę i po cichu biegnie jako `xhigh`. Wrapper i panel nazywają linię `spark` (`-Engine spark`). Procentu zapasu CLI nie podaje (`muse` 1.4.11 nie ma polecenia zużycia) — sygnał `nieznany` do pierwszego 429, tempo pilnuje liczba przebiegów od poniedziałku (reguła 8) | model, potem kontekst; effort słabo (85–95 % tokenów to ponowny odczyt kontekstu, wyjście ~15–25 % kosztu) |
| Codex          | ChatGPT Plus ($20)   | „wiadomościami" / 5 h + tydzień, widełki per model — ale **waga wiadomości rośnie z modelem, kontekstem i effortem** (oficjalnie: „model choice, context, reasoning, tool use… all affect usage") | model **i** effort, jak w Claude     |
| Gemini (`agy`) | Google AI Pro (~$20) | Antigravity CLI, pilot od 2026-09-23; dwie pule (Gemini / Claude+GPT), każda okno 5 h + tydzień, zużycie proporcjonalne do kosztu tokenów — stan bez zużycia: `agy -p="/quota"`. 503 „Eligibility check failed" to przejściowa awaria kontroli kont Google przed turą — wrapper ponawia sam | model (effort jest w nazwie modelu) |

Limity **nie przelewają się między silnikami** — wyczerpany Muse nie uszczupla
Claude'a. Ale **wewnątrz Claude'a jest jedna wspólna pula**, obejmująca wszystkie
modele oraz przeglądarkę, apkę mobilną i Claude Code: przesiadka na słabszy model
**nie odblokowuje** limitu, który już wyczerpałem — pomaga wyłącznie niższym
tempem spalania.


### Twarde bramki — przed porównaniem kosztu lub preferencji

Jednostką decyzji jest brief wykonawczy albo recenzencki, nie work item
ADO. Najpierw opisujesz stawkę/skutki błędu, niepewność/nowość, zależności
i pliki, potrzebne narzędzia/uprawnienia/kontekst, test oracle i kryteria
akceptacji. Odrzucasz każdą parę model–native effort, która nie spełnia
któregokolwiek warunku:

- High-stakes: uwierzytelnianie i sesja, płatności, poświadczenia/PIN-y
  dostępowe, migracje danych, naliczanie wartości (punkty, nagrody, salda),
  jednorazowe kody i limity prób oraz briefy za trudne dla Sonneta
  (współbieżność, niezmienniki bezpieczeństwa, logika przekrojowa z cichym
  błędem) pozostają na `wykonawca-opus` — Opus `xhigh`. Projekt doprecyzowuje
  własną listę w swoich regułach projektowych i swoim skillu. Chodzi o pliki
  niosące niezmiennik, nie wolumen ani ekran/style/i18n bez tego
  niezmiennika. Jedyny zachowany wyjątek blokady hooka opisuje reguła 2.
  Gemini nigdy nie dostaje high-stakes; Codex nie zastępuje tu Opusa.
- Wykonawca ekranu z Figmy ma faktyczny Figma MCP i sam pobiera
  `get_design_context`. Link lub transkrypcja nie zastępują dostępu.
  Muse i Gemini odpadają; Claude lub Codex muszą mieć dostęp potwierdzony
  w konkretnej sesji.
- Narzędzia, repo FE/BE, uprawnienia i niezbędny kontekst są faktycznie
  dostępne. Wykonawca może bezpiecznie zapisać i zweryfikować własne pliki,
  a recenzent ma tylko odczyt. Zewnętrzny worker dostaje samodzielny
  brief; nie zakładasz dziedziczenia kontekstu sesji.
- Recenzent ma zdolności odpowiednie do stawki oraz inną rodzinę niż autor.
  Sonnet/Opus/Haiku/Fable to rodzina Claude; Sol/Luna/Astra to rodzina
  Codex; Muse (Wonder Full, Wonder, Spark) i Gemini to odrębne rodziny.
  Fable nie recenzuje.
  Niezależność końcowej bramki Sol (rodzina Codex) dotyczy plików niosących
  niezmiennik high-stakes: te zawsze pisze `wykonawca-opus` (wyjątek
  CZERWONEGO: Muse Wonder Full `max`), więc bramka z rodziny Codex jest wobec nich
  niezależna. Codex może pisać briefy bez niezmiennika w funkcji
  high-stakes (ekrany, szablony, style, i18n, testy bez niezmiennika);
  ich niezależność zapewnia recenzja fali z rodziny innej niż Codex.
  Bramka czyta cały diff funkcji, także te pliki, ale dla nich nie
  zastępuje recenzji fali. W funkcji high-stakes przy sygnale puli Codexa
  `nieznany` Codex dostaje co najwyżej krótkie briefy bez niezmiennika
  (≤ 5 plików, effort nie wyższy niż `high`); po jego komunikacie limitu
  przed bramką (`zablokowany`) nie dostaje kolejnych briefów tej funkcji —
  bramka ma pierwszeństwo (pula Codexa, reguła 7).
- Jeden brief obejmuje jedną warstwę, równoległe cele są rozłączne,
  a wymagane sprawdzenia są wykonalne. Obowiązują reguły 14–15.
- Model i native effort są obsługiwane przez wybrane narzędzie.
  Agent Claude'a jest nazwany, z effortem zapisanym w definicji; nie
  podstawiasz gołego `Agent` dziedziczącego effort i nie obchodzisz hooka.
- Ograniczenia skilli pomocniczych, zwłaszcza `qasphere-test-generator`,
  pozostają twarde; ogólny routing ich nie nadpisuje.

### Preferencje — wyłącznie wśród dopuszczonych kandydatów

Wybierasz wykonawcę i recenzenta per brief na podstawie lokalnych wyników
podobnego archetypu, spodziewanych korekt, czasu do akceptacji i wiarygodnego
sygnału dostępności. Złożoność, nowość i zależności wpływają na dobór effortu.
Codex jest pełnoprawnym kandydatem od planowania, bez czekania na limit
innej linii. Dotychczasowe wyniki Spark/Gemini w recenzji, Sola w researchu
i Sparka w audycie SCSS (zmierzone na Sparku 1.3, nie na Wonderze) są
preferencjami do ponownej oceny, nie wyłącznością ani automatyczną
kolejnością silników.

Dla wykonawcy i recenzenta zapisujesz linię, dokładny model + native effort,
krótkie uzasadnienie, pewność, dopuszczone alternatywy (lub jawnie brak)
i status dostępności ze źródłem i czasem sygnału. `high`, `xhigh` i `max`
różnych dostawców nie są równoważne. Nie dodajesz scoringu, wymyślonych
procentów ani sztywnego progu kosztu. Celem jest zaakceptowany wynik
w dostępnej przepustowości, nie wyczerpanie limitów lub najtańszy pierwszy
przebieg. Koszty i ograniczenia effortu poszczególnych silników poniżej
stosujesz w decyzji konkretnego briefu.

## Macierz możliwości, uprawnień i twardych ograniczeń

Wskazane efforty są natywnymi konfiguracjami danej linii. Przed wywołaniem
potwierdzasz obsługę pary i narzędzi; sama nazwa modelu nie dowodzi dostępu.
Status dostępności jest ustalany na czas decyzji wg reguły 2, nie wpisany
na stałe. Możliwość wykonania nie oznacza automatycznego przydziału.

| Linia / model / native effort | Możliwości, narzędzia i uprawnienia | Twarde bramki i rodzina recenzji | Sygnał dostępności |
| --- | --- | --- | --- |
| Sesja główna — Opus `xhigh` | plan, decyzje, briefy, WCAG/tokeny, dowody, triaż i odbiór ADO | architekt; bez kodu/testów poza regułą 11; rodzina Claude | hook Claude'a |
| `wykonawca-opus` — Opus `xhigh` | repo FE/BE i narzędzia sesji po potwierdzeniu; zapis plików niezmiennika high-stakes albo briefu za trudnego dla Sonneta | nie wolumen, ekran/style/i18n bez niezmiennika; hook; nie recenzuje Claude | hook Claude'a |
| `wykonawca` — Sonnet 5.5 `high` | Figma MCP, kontekst sesji i repo FE/BE; zapis/implementacja, inne narzędzia po potwierdzeniu | jedna warstwa; bez niezmienników wymagających Opusa; nie recenzuje Claude | hook Claude'a |
| Muse — `muse-spark-1.3-contributor`, `muse-wonder-1.0-contributor`, `muse-wonder-full-1.0-contributor`; każdy `minimal / low / medium / high / xhigh / max` (`none` odrzuca CLI, `ultra` ma zamkniętą bramkę i biegnie jako `xhigh` — wrapper odrzuca oba, 2026-10-12); para per archetyp briefu (od 2026-10-25, reguła 8): Spark `max` domyślnie (także średnia stawka i QA Sphere w funkcji high-stakes), Spark `high` operacyjnie, Wonder Full `max` tylko high-stakes w limicie Wondera (2 dziennie, 6 tygodniowo); Wonder 1.0 bez archetypu | `-Engine spark`; `-Access write`: Node z Windows przez interop, własne testy, MCP ADO/Playwright/Angular/QA Sphere/Mikrus; `-Access read`: audyt i recenzja | bez Figmy, gita i `npm install`; high-stakes tylko wyjątek reguły 2; nie recenzuje Muse (Wonder i Spark to jedna rodzina); rozłączne cele, bez limitu slotów | komunikaty wrappera/raporty (429 z resetem tygodniowym = `zablokowany` do poniedziałku 00:00Z); brak odczytu zapasu = `nieznany`; tempo — liczba przebiegów Wondera (Full i 1.0) od poniedziałku wobec limitu z reguły 8 |
| Gemini — `agy`, `gemini-3.8-flash-low`, `gemini-3.8-flash-medium`, `gemini-3.8-flash-high`; effort w sufiksie (Gemini 4 Argon poza AI Pro — `agy models`, 2026-10-12 i ponownie 2026-10-14 na `agy` 1.3.5) | Windows, zapis i własny lint/test; MCP ADO/Playwright/Angular/QA Sphere/Mikrus; `-Access read` do recenzji | nigdy high-stakes, Figma; absolutne ścieżki, jawny odczyt `AGENTS.md`; recenzja bez powłoki wg `external-workers`; nie recenzuje Gemini | komunikaty wrappera; 3 × 503 = rzeczywiste niepowodzenie, ponowna kwalifikacja |
| Codex — `gpt-6.1-sol`: `low / medium / high / xhigh / max / ultra`; `gpt-6-luna`: `low / medium / high / xhigh / max` | implementacja/testy/research; Figma i Playwright po potwierdzeniu w sesji; `-Mode review` do odczytu | pełnoprawny kandydat; implementacja i testy porcjami ≤ 5 plików, recenzji nie dzielisz na porcje (bramka końcowa z reguły 6 zawsze czyta cały diff w jednym przebiegu); nie przejmuje high-stakes Opusa (plików niezmiennika); w funkcji high-stakes tylko briefy bez niezmiennika z recenzją fali spoza rodziny Codex, przy sygnale puli `nieznany` co najwyżej krótkie (≤ 5 plików, effort ≤ `high`), po limicie przed bramką żadnych kolejnych (reguła 7); nie recenzuje Codexa; research bez poleceń powłoki | komunikaty wrappera/raporty; brak odczytu zapasu = `nieznany` |
| `tester` — Haiku 5.5 `xhigh` (od 2026-10-13, po próbie z reguły 14; wcześniej Sonnet 5.5 `medium`) | Vitest/AXE/xunit i czerwony test Buga | test przed łatką, odrębne briefy; autor łatki nie edytuje testu; rodzina Claude | hook Claude'a |
| `mechanik` — Haiku 5.5 `low` | mechaniczne klucze i18n/rename/przeniesienie pliku | nie implementacja high-stakes; rodzina Claude | hook Claude'a, zachowany wyjątek CZERWONEGO |
| `zwiadowca` — Haiku 5.5 `low` | fakty z repo przed decyzją | tylko odczyt; rodzina Claude | hook Claude'a, zachowany wyjątek CZERWONEGO |
| `audytor-a11y` — Opus `high` | delegowany audyt kontrastu/fokusu/tokenów | audyt, nie przejęcie implementacji; nie recenzuje Claude | hook Claude'a |
| QA Sphere — Muse: Spark 1.3 `max`, także w funkcji high-stakes (reguła 8, od 2026-10-25); Gemini `-Access write` gdy Muse zajęty lub z limitem | plik podglądu wg `qasphere-test-generator`; publikacja/poprawki/weryfikacja architekta skryptem `qas.py` | plik Muse → Gemini `-Access read`, plik Gemini → Muse `-Access read`; sesja nie pisze przypadków ani nie woła `create_test_case`/`update_test_case` | procedura pomocniczego skilla, ogólny routing jej nie zastępuje |
| Bramka końcowa — `gpt-6.1-sol` `max` (od 2026-10-05; Astra `max` nie mieści się w Plusie) | tylko odczyt, cały feature high-stakes po recenzjach fal, osobno FE i BE, sekwencyjnie | niezależna rodzina wobec autora plików niezmiennika (`wykonawca-opus`, przy CZERWONYM Muse Wonder Full `max`); czyta cały diff funkcji, ale dla briefów Codexa bez niezmiennika nie zastępuje recenzji fali spoza rodziny Codex; bramka reguły 6, nie zwykły przydział; nie zastępuje recenzji fal | rzeczywisty limit blokuje bramkę, bez obniżenia modelu/effortu |
| Pozostali niezależni recenzenci — Muse/Gemini/Codex z jawnie wybraną parą | odczyt repo i dowodów właściwych dla briefu | zdolność odpowiednia do stawki, inna rodzina niż autor; Fable wykluczony | kwalifikacja wg bieżącego sygnału, bez stałego fallbacku |

### Zachowane porównania i ograniczenia kosztu

Poniższe datowane pomiary, ceny i porównania pozostają kontekstem
operacyjnym o określonych modelach/effortach. Nie opisują bieżącego zapasu
abonamentu, wyniku nowego briefu ani uniwersalnej mapy modeli. Wnioski
o jakości sprawdzasz w lokalnym rejestrze. Zachowujesz ograniczenia kosztu
poszczególnych silników; wybór spośród obsługiwanych effortów uzasadniasz
dla briefu. Stałe bramki ryzyka i końcowa bramka Sol `max` mają pierwszeństwo.

Poniższe porównania cen, widełek, effortów i lokalnych wyników są danymi
historycznymi z podanych dat (w tym 2026-09-30), a nie pomiarem bieżącego
zapasu abonamentów ani automatyczną kolejnością silników. Opisane wówczas
warianty nie przydzielają zwykłych briefów. Architekt dobiera dopuszczoną
parę model–effort per brief według złożoności, niepewności, ryzyka,
dostępności, narzędzi i lokalnych wyników zaakceptowanych briefów.

**Cennik Muse i kalibracja puli (2026-10-25, najnowsze).** Właściciel:
„muse-wonder-1.0 jest BARDZO drogim modelem, możemy go używać, ale
racjonalnie — 21 przebiegów zabiło tygodniowy limit; Spark 1.3 contributor
jest bardzo tani”. Cennik za 1M tokenów (zrzut właściciela): Wonder 1.0 —
cache 0,20 $, wejście 4,00 $, wyjście 20,00 $, tryb contributor
niedostępny; Spark 1.3 contributor — 0,002 / 0,10 / 0,20 $ (standard
0,15 / 1,25 / 4,25 $); Wondera Full cennik nie podaje. Przy naszym profilu
(94–95 % tokenów to odczyt cache) token Wondera kosztuje wg cennika ~60×
tokenu Sparka contributor (cache 100×, wejście 40×, wyjście 100×). Pula
liczy łagodniej, ale rząd wielkości zostaje: `token-report.py` na dwóch
wyczerpaniach — tydzień 12.10 = 110 Sparków `max` (734 mln tokenów) +
5 Full `max` (44 mln), tydzień 19.10 = 21 Full `max` (100 mln; 16 udanych,
5 przerwanych) + 4 Sparki (5 mln) — daje token Full ≈ 13× Sparka i tydzień
≈ 100 mln tokenów Full ≈ 1,3 mld tokenów Sparka, czyli ≈ 21 przebiegów
Full albo ≈ 190 Sparka `max`. Przebieg Full kosztował 4,8–8,8 mln tokenów,
przebiegi QA Sphere 7–25 mln. Wonder 1.0 ma w puli jeden przebieg (sondę),
jego kosztu względem Full nie zmierzono, a cennik nie daje mu trybu
contributor — nie jest tańszym pośrednim szczeblem, liczysz go jak Full.
Stąd zaostrzenie reguły 8 z 2026-10-25.

**Odczyt AA z 2026-10-20 i pomiar puli Muse.** Nowych modeli
w naszych abonamentach brak (`muse-spark-open` z 2026-10-15: II 38,9, TB4
0,081 — słabszy od Sparka 1.3). AA nadal ma tylko rekordy `max` obu Wonderów
i `max`/`xhigh` Sparka — niższych effortów Muse nie mierzy. Struktura kosztu
zadania indeksu: Spark 1.3 `max` 1,60 $ (wejście 1,35 $), Wonder 4,52 $
(wejście 3,43 $, z tego zapis i odczyt cache 3,36 $), Wonder Full bez ceny;
w naszych przebiegach 85–95 % tokenów Muse to odczyt cache. Effort steruje
tylko wyjściem (15–25 % kosztu), więc **dźwignią puli Muse jest model, potem
długość kontekstu, a dopiero na końcu effort** — Spark `xhigh` oszczędza
wobec `max` 14 % za połowę TB4 (0,167 wobec 0,333). Dwa wyczerpania limitu
tygodniowego (15.10 po 110 Sparkach `max` + 5 Wonder Full `max`; 20.10 po
19 Wonder Full `max`) dają token Wondera Full ≈ 12–15× Sparka — pewność
niska, bez odczytu zapasu; szacunek „Full ≈ 3,5–4× Wondera” obalił cennik
z 2026-10-25 (akapit wyżej). Stąd podział linii Muse per archetyp
w regule 8.

**Odczyt AA z 2026-10-14.** Jedyne nowe modele w naszych
abonamentach to **Muse Wonder** i **Muse Wonder Full** (Meta, 2026-10-12;
AA ma tylko rekordy `max`; CI i TB 2.1 brak). Wonder Full: II **55,8** (≈ Opus
5.5 `xhigh` 56,0), TB4 **0,571** (= Sonnet `xhigh` i Gemini 4 Argon; Opus
`xhigh` 0,596, Sol `max` 0,561), SciCode 0,626; ceny i kosztu zadania AA nie
podaje. Wonder: II 52,4, TB4 0,520 (= Fable `max`, ≈ Sol `high` 0,515), SciCode
0,603, $4/$20 za 1M (Spark 1.3: $1,25/$4,25), **4,52 $ na zadanie** wobec
1,60 $ Sparka 1.3 `max` (II 48,1, TB4 0,333). Gadatliwość ta sama: tokenów
wyjścia na zadanie indeksu Wonder Full 53,8 tys., Wonder 54,2 tys., Spark 1.3
`max` 60,2 tys. — różnicę kosztu robi wyłącznie cena tokenu. Prędkość Wondera
113 tok/s (= Spark `max`), Full niezmierzony. Oba są w katalogu `muse` 1.4.8
na Power Usage, dostęp potwierdzony sondą wrappera (`model_completed.model`)
2026-10-14 — stąd zmiana domyślnego modelu linii Muse (reguła 8). **Gemini 4
Argon** nadal poza `agy` (1.3.5: tylko Flash 3.8, Claude 4.6, GPT-OSS).
Nowych modeli Claude'a i Codexa AA nie ma.

**Odczyt AA z 2026-10-12.** Nowy w puli Claude'a **Haiku 5.5**
(`claude-haiku-5-5`, 2026-10-07): $0,10/$0,50 do 100 tys. tokenów promptu,
$0,50/$2,50 powyżej, okno 1M, efforty `low`–`max`; II `low` 29,5 (0,024 $ na
zadanie) · `medium` 34,5 (0,047 $) · `high` 37,8 (0,079 $) · `xhigh` 41,2
(0,12 $) · `max` 43,4 (0,21 $), wobec Haiku 4.5 II 16,9 za 0,28 $. Od
2026-10-12 `mechanik` i `zwiadowca` mają go przypiętego pełnym ID (Claude Code
≥ 2.1.296 — 2.1.286 zgłasza `unrecognized_model`, liczy okno 200 tys. i alias
`haiku` daje tam Haiku 4.5). W naszym profilu Haiku `xhigh` zużywa na zadanie
~6× więcej tokenów wejścia niż Sonnet `medium`, a powyżej 100 tys. promptu
cena rośnie 5× — przewaga ceny tokenu spada z 20× do 4×; stąd próba testera
(reguła 14), nie przełączenie — zamknięta 2026-10-13: Haiku `xhigh` przejął
linię `tester` (0,60× kosztu Sonneta na brief). **Terminal-Bench 4.0** (TB4) AA policzył dla
wszystkich naszych modeli (CI i TB 2.1 modeli od 2026-09-17 nadal brak, TB 2.1
był nasycony): Sonnet 5.5 `max` 0,636 · Opus 5.5 `xhigh` = `max` 0,596
(`high` 0,566, `medium` 0,525, `low` 0,313) · Astra `max` 0,591 · Sonnet
`xhigh` 0,571 · Sol 6.1 `max` 0,561 · `xhigh` 0,540 · `high` 0,515 · `medium`
0,480 · `low` 0,308 · Fable 5.1 `max` 0,520 · Sonnet `high` 0,439 · `medium`
0,298 · `low` 0,207 · Spark `max` 0,333 · `xhigh` 0,167 · Haiku 5.5 `max`
0,328 · `xhigh` 0,293 · Gemini 3.8 Flash `high` 0,197 · Luna `max` 0,126 ·
`xhigh` 0,081. TB4 to długie zadania agentowe, a nasze briefy są krótkie
i warstwowe — lokalne wyniki (Spark przeważnie 0–1 rundy) mają pierwszeństwo;
Spark `xhigh` < `max` (2× na TB4 za +17 % kosztu) — od 2026-10-12 `max`
jest domyślnym effortem Sparka (reguła 8). AA przemierzył Sonneta 5.5: koszt zadania
`low` 0,35 $ (II 35,9) · `medium` 0,48 $ · `high` 0,88 $ · `xhigh` 2,01 $ ·
`max` 5,46 $ (wcześniej 0,59 / 1,08 / 2,74 / 7,62 $); Opus, Sol, Spark
i Gemini bez zmian. II na 1 $ (2026-10-12): Haiku 5.5 `low` 1206 · `medium`
734 · `high` 476 · `xhigh` 333 · `max` 204 · Sonnet `low` 104 · `medium` 84 ·
`high` 53 · `xhigh` 26 · `max` 10. **Gemini 4 Argon** (2026-09-30; II 52,6,
TB4 0,571, 1,99 $ na zadanie) nie jest dostępny w `agy` na AI Pro (`agy
models`, 2026-10-12: Flash 3.6–3.8, 3.1 Pro, Claude 4.6, GPT-OSS) — sprawdzam
przy kolejnym odczycie. Nowych modeli Codexa i Sparka AA nie ma.

Uzasadnienie liczbowe (Artificial Analysis, API z 2026-09-23). **Coding Index
modeli wydanych od 2026-09-17 — Opus 5.5, GPT-6 Sol, GPT-6 Luna — AA jeszcze
nie policzył** (brak Terminal-Bench, składowej o wadze 2/3: CI ≈ (2·TB +
SciCode)/3), więc nowe modele porównuję Intelligence Indexem (II) i kosztem
zadania indeksu ze strony modelu na AA (od 2026-10-12 także TB4 — odczyt wyżej). Spark xhigh: CI **76,5**, II 45,1,
305 tok/s w odczycie z 23.09, 162 z 30.09 — ok. 2× szybciej niż Opus 5.5
`xhigh` (84) i za 1/4 jego ceny tokenu, na
osobnym abonamencie. Opus 5.5 `max`: II **57,6**, najwyżej w całym
zestawieniu (Fable 5.1 `max` 53,4, Astra `max` 52,7), za **5,98 $ na zadanie**.
**Od 2026-09-28 sesja architekta biegnie na `xhigh`** (II 56,0 za 3,46 $) —
decyzja użytkownika: `max` to przerost formy nad treścią, a `modelSettings`
w `~/.claude/settings.json` i tak już tak ustawiało. `xhigh` nadal ma wyższy
II niż Fable 5.1 `max` i Astra `max`. Opus jako wykonawca
(`wykonawca-opus`, od 2026-09-25) biegnie na **`xhigh`**: między `high`
a `xhigh` SciCode rośnie o 4,6 pkt (0,604 → 0,650; II 53,6 → 56,0), między
`xhigh` a `max` już tylko o 1,9 pkt (→ 0,669; II 57,6), a koszt zadania
indeksu to 1,82 → 3,46 → 5,98 $ — kolano krzywej leży na `xhigh`. Nawet
`high` ma wyższy II niż Fable 5.1 `max` (53,4), Gemini (40,9) i Sonnet 5.5
`high` (46,7). TB4 z 2026-10-12 potwierdza wybór: `xhigh` = `max` (0,596),
`high` 0,566. GPT-6 Sol ma token tańszy niż Terra
($2/$10 wobec $2/$12) przy inteligencji Sola: `medium` **39,8** wobec 30,1
Terry `medium`, `high` **42,8** (0,37 $ na zadanie) wobec 42,3 Sola 5.6 — stąd
Sol przejmuje wszystkie role Terry. **Od 2026-09-30 role Sola biegną na
GPT-6.1 Sol (`gpt-6.1-sol`)**: ta sama cena tokenu ($2/$10), a zadanie
tańsze (`medium` 0,21 $ wobec 0,25 $, `high` 0,32 $ wobec 0,38 $; 25 M
tokenów wyjścia na indeks przy `high`, jak 6 Sol) i II wyżej o 4–8 pkt na
każdym efforcie — `low` 42,1 · `medium`
**47,8** · `high` **50,2** · `xhigh` 51,0 · `max` 51,8 (6 Sol: 33,9 · 39,8 ·
42,8 · 44,1 · 47,5); `high` ≈ Astra `high` (50,9) za 0,32 $ wobec 1,73 $
na zadanie (5,4× taniej), `max` 51,8 za 0,72 $ wobec Astry `max` 52,7 za
3,26 $ (4,5× taniej).
Widełki Plusa z odczytu 2026-09-30: 15–160 wiadomości / 5 h (6 Sol 15–150). CI i Terminal-Bench
6.1 AA jeszcze nie policzył — Astra (`max` 52,7,
CI 76,9) pozostawała w tym porównaniu twardą bramką końcową,
a przy tej różnicy kosztu 6.1 Sol `max` szedł obok niej na ograniczoną próbę;
od 2026-10-05 6.1 Sol `max` jest bramką (reguła 6 — Astra nie mieści się w Plusie). Historyczna obserwacja z 2026-09-30: przy porównaniu przelewu `wykonawca-opus` przy CZERWONYM na Sparku
`xhigh` (CI 76,5): Sol 6.1 `high` ma wyższy II (50,2 wobec 45,1), ale CI
nie ma; TB4 z 2026-10-12: Sol 6.1 `high` 0,515 wobec Sparka `xhigh` 0,167
(`max` 0,333; Muse Wonder Full `max` 0,571 — odczyt 2026-10-14). Ten benchmark nie zmienia wyjątku z reguły 2: przy CZERWONYM brief `wykonawca-opus` może zostać przekwalifikowany na Muse Wonder Full `max` (do 2026-10-12 Spark `xhigh`, do 2026-10-14 Spark `max`) albo poczekać; nigdy na Gemini, Sonneta ani Codexa, a high-stakes nie otwiera się poza tym wyjątkiem. GPT-6 Luna `xhigh` ma II 33,9 ≈ Luna 5.6
`xhigh` 34,6, ale przy 2,25× tańszym tokenie i starcie odpowiedzi 9 s zamiast
29 s. Historyczne obserwacje AA z 2026-09-30 dla zastępstw przy limicie Claude'a (Sonnet 5.5): Sol 6.1 `high` (50,2) > Sonnet 5.5 `high` (46,7, `wykonawca`);
Sol 6.1 `low` (42,1) > Sonnet 5.5 `medium` (40,7, `tester`) — **dla Luny obserwacja była odwrotna**:
`xhigh` 33,9 i `max` 37,3 były poniżej testera; w ówczesnym porównaniu koszt Sola 6.1 `low` to 0,13 $ na zadanie wobec 0,04 $ Luny
`xhigh` — ~3× więcej z puli Codexa, wciąż 4,5× mniej niż sam tester (0,59 $),
a Luna `xhigh` była w ówczesnym porównaniu obserwowana przy mechanice
jako wariant porównawczy (> Haiku 4.5: 16,9; CI 43,9). Sonnet 5.5 na efforcie: 41→47→52→56
dla medium→high→xhigh→max (Sonnet 5: 28→32→34→38) — a myślenie jest
w briefie. **II na 1 $ kosztu zadania indeksu** (od 2026-09-30 zamiast
ceny tokenu, która pomija gadatliwość — tokenów wyjścia na indeks: Sonnet 5.5
`max` 410 M, Fable 5.1 `max` 190 M, Gemini 170 M, Spark `xhigh` 140 M,
Opus 5.5 `xhigh` 100 M, Sol 6.1 `high` 25 M; ceny API): Luna `xhigh` **806**
(0,04 $) · Sol 6.1 `low` 322 (0,13 $) · `medium` 224 (0,21 $) · `high` 157
(0,32 $) · `max` 72 (0,72 $) · Sonnet 5.5 `medium` 69 (0,59 $) · `high` 43
(1,08 $) · Gemini `high` 33 (1,24 $) · Spark `xhigh` 33 (1,37 $ po cenie
standardowej; tier contributor jest 12–21× tańszy, więc realnie ~395–690) ·
Opus 5.5 `high` 29 (1,82 $) · Astra `high` 29 (1,73 $) · Opus 5.5 `xhigh` 16
(3,46 $) · Astra `max` 16 (3,26 $) · Opus 5.5 `max` 9,6 (5,98 $) · Sonnet 5.5
`max` 7,3 (7,62 $) · Fable 5.1 `max` 7,0 (7,63 $). Między abonamentami architekt kwalifikuje brief według bieżących ograniczeń i dowodów; kolejność linii w tym zestawieniu nie wybiera silnika. Historyczne porównanie nie stanowi automatycznego fallbacku.
**Pełna macierz kosztu zadania (2026-09-30, 38 rekordów: każdy effort Opusa
i Sonneta 5.5, Fable 5.1, Haiku 4.5, 6.1 Sola, Luny, Astry, Sparka 1.3
i Gemini 3.8 Flash; tabela w rozpisce).** Wnioski: (1) w puli Claude'a Opus
5.5 wypiera Sonneta 5.5 z granicy efektywności wszędzie poza `high` — Opus
`low` 42,3 za 0,55 $ wobec Sonneta `medium` 40,7 za 0,59 $, Opus `medium`
51,2 za 1,34 $ wobec Sonneta `xhigh` 51,9 za 2,74 $; przy tym samym II Sonnet
zużywa 1,7–4,7× więcej tokenów wejścia (więcej tur). Ale indeks to krótkie
zadania bez cache, a u nas 54–81 % kosztu to ponowne czytanie kontekstu po
cenie wejścia 2× wyższej u Opusa — liczone samym wejściem Opus `low` wychodzi
~1,2× Sonnet `medium`, Opus `medium` ~1,3× Sonnet `high`. Opus `medium` w linii Figmy przeszedł próbę A/B (2026-10-04…05, reguła 14):
koszt 1,36× Sonneta > progu 1,3× — zostaje Sonnet (próba zamknięta 2026-10-12). Historyczna obserwacja bez próby dla testera: Opus `low` ≈ Sonnet `medium` kosztem,
a +1,6 pkt II mieści się w szumie. Bieżący pilotaż architekta działa na Opusie `xhigh` (effort wynika z reguły 4;
obserwacja z 2026-09-30): `high` obciąłby ~5–9 % kosztu sesji architekta za −2,4 pkt II
w roli, która decyduje i waliduje.
(2) Koszt krańcowy punktu II Opusa: `low`→`medium` 0,09 $, →`high` 0,20 $,
→`xhigh` 0,68 $, →`max` 1,58 $ — największy skok przy wejściu na `xhigh`;
u nas effort to 9–18 % kosztu (reguła 15), więc to dźwignia jakości, nie
kosztu. (3) 6.1 Sol wypiera Astrę na każdym poziomie (Sol `max` 51,8 za
0,72 $ wobec Astry `medium` 49,6 za 1,54 $) — Astra broniła się policzonym CI
i próbą bramki; od 2026-10-05 bramką jest 6.1 Sol `max` (reguła 6). (4) Historyczna obserwacja AA z 2026-09-30: Gemini Flash `medium` jest o 25 % tańszy od
`high`, ale TB 83,9 wobec 87,6 — w ówczesnym porównaniu obserwowano `high`. (5) Historyczna obserwacja z 2026-09-30: Fable 5.1 `xhigh`
(CI 80,7 za 5,98 $) ≈ `max` (81,6 za 7,63 $) — przy pojedynczym wywołaniu
w ówczesnym porównaniu obserwowano `max`. (6) Historyczna obserwacja z 2026-09-30: Haiku 4.5 (16,9 za 0,28 $) — najtańsza alternatywa
w puli Claude'a kosztuje 2× (Opus `low`), obserwowana przy prostych,
walidowanych zadaniach; od 2026-10-12 zastąpiony przez Haiku 5.5 (odczyt
2026-10-12). Braki w AA (2026-10-12): Gemini Flash `low`, Spark `high` (linia
lekkich briefów nie ma pomiaru). Koszt zadania liczy
każdy model na jego własnym koszyku zadań (koszt indeksu / koszt zadania
1000–2350) — porównanie jest przybliżone.
**Od 2026-09-28 Sonnet 5.5 (`claude-sonnet-5-5`) zastępuje Sonneta 5
w 100 %** — decyzja użytkownika: szybszy i lepszy za tę samą cenę ($2/$10,
cache 0,20 $; 1M kontekstu, 128K wyjścia). `wykonawca` ma go przypiętego
pełnym ID, nie aliasem `sonnet` (`tester` do 2026-10-13, potem Haiku 5.5). Wymaga Claude Code ≥ 2.1.284
(`claude update`; w VS Code przeładować okno, żeby sesja wstała na nowym
rozszerzeniu). AA policzył Sonneta 5.5 2026-09-30 (II `medium` 40,7 ·
`high` 46,7 · `xhigh` 51,9 · `max` 56,0; CI i TB jeszcze nie). **Równy II
nie znaczy równego kosztu**: Sonnet 5.5 `max` ma II Opusa 5.5 `xhigh` (56,0),
ale zużywa 410 M tokenów wyjścia na indeks wobec 100 M, więc zadanie kosztuje
7,62 $ wobec 3,46 $ — 2,2× drożej mimo tokenu 2× tańszego. `xhigh` (51,9 za
2,74 $) przegrywa z Opusem `high` (53,6 za 1,82 $); `high` (46,7 za 1,08 $)
to najtańsze zadanie w rodzinie. W porównaniu z 2026-09-30 zestawiano `wykonawca-opus` `xhigh` i `wykonawca` `high`; to opis ówczesnego podziału, a nie niezmienny przydział zwykłych briefów. Opus `medium` (51,2 za
1,34 $) wygląda na papierze lepiej od Sonneta `high`, ale indeks AA to głównie
krótkie zadania, a nasz koszt to w 54–81 % ponowne czytanie kontekstu po cenie
wejścia 2× wyższej u Opusa (reguła 15) — sam indeks nie uzasadniał wtedy zmiany routingu bez lokalnych pomiarów na naszych briefach. Historyczny odczyt z 2026-09-30 dla porównania abonamentów obejmującego Claude, Spark i Codex: Codex
miał wówczas najmniejsze widełki w tym odczycie (Sol 6.1 15–160 wiadomości / 5 h). Historyczna obserwacja z 2026-09-16: effort na Codexie
zweryfikowany 2026-09-16 jako **stosowany**, nie tylko przyjmowany (Luna 5.6
`low` policzyła zadanie rozumowe źle, `xhigh` dobrze).

Recenzje (rollouty Codexa, 2026-09-21…23): Sol 5.6 `high` kosztował 0,6–3,5 $
i 3–23 pkt okna 5 h na recenzję, Astra `max` na całym PBI #2137 — ~7 $, 66 pkt
okna 5 h i 10 % tygodnia. Ok. 80 % kosztu recenzji to czytanie kodu (wejście),
reasoning ~9 % — **effort nie jest dźwignią kosztu recenzji, wybór diffów
jest**. Jakość: na tym samym diffie (CR #2263 BE) 2 z 3 znalezisk były wspólne,
Astra dołożyła wyścig przy limicie prób, Sol — złamanie reguły hoistingu;
po dwóch recenzjach Sola i poprawkach (PBI #2137) Astra znalazła jeszcze pięć
realnych defektów. Stąd bramka końcowa raz na feature, a nie recenzent
etapów (do 2026-10-05 na Astrze, od tego dnia na 6.1 Solu `max` — reguła 6). Spark `xhigh` ma w odczycie historycznym Coding Index Sola 5.6 `high` (76,5 wobec
77,2) i jest z trzeciej rodziny (Meta) — historyczna obserwacja do oceny per brief, bez stałego przypisania Sparka do diffów Sonneta. Gemini 3.8 Flash `high`: CI 76,3 (≈ Spark `xhigh`
76,5 i Sol 5.6 `high` 77,2), II 40,9, $0,75/$3,75 — czwarta rodzina modeli,
historyczna obserwacja do oceny per brief, bez stałego przypisania do diffów Sparka; bieżący wybór recenzenta to niezależna rodzina per brief (reguła 13). Jako wykonawca (AA, odczyt
2026-09-24): Terminal-Bench 2.1 **88 %** — najwyżej w łańcuchu poza Fable
(Sol 5.6 `high` 87, Spark `xhigh` 85, Sonnet 5 `max` 81), SciCode 57; koszt
zadania indeksu 1,24 $ mimo taniego tokenu — model gadatliwy, pulę AI Pro
zjada szybciej, niż sugeruje cena. Druga pula AI Pro (Opus 4.6 II 31,9,
Sonnet 4.6 CI 63, GPT-OSS 120B CI 30,4) jest słabsza od zastępstw na Codexie
— poza routingiem. Historyczna obserwacja: research na Gemini — próba zakończona 2026-09-24 (źródła
bez adresów). Wynik jest historycznym sygnałem i preferencją do ponownej oceny per brief, bez zakazu researchu Gemini i bez stałego przydziału do Sola `medium`.

## Twarde reguły

1. **Subagenta Claude'a wywołuję wyłącznie jako nazwanego agenta z
   `~/.claude/agents/`** (`wykonawca`, `wykonawca-opus`, `tester`,
   `mechanik`, `zwiadowca`, `audytor-a11y`). Gołe `Agent` z samym `model` **dziedziczy effort sesji** —
   narzędzie nie ma parametru `effort`, ma go tylko definicja agenta. Każde
   takie wywołanie to Sonnet lub Haiku myślący jak Opus.

2. **Sygnały dostępności i ponowna kwalifikacja po limicie.**
   Nie pytasz o ręczne `/usage`. Hook `~/.claude/bin/limity-hook.mjs`
   czyta endpoint co ≤ 90 s i dopisuje `[limity Claude]`; wrappery
   zewnętrzne dostarczają rzeczywiste komunikaty i raporty przebiegów.

   Status zapisujesz dla wybranej pary ze źródłem i czasem:
   `znany` = wiarygodny bieżący odczyt; `ostrzegawczy` = ostrzeżenie
   (np. ŻÓŁTY); `zablokowany` = blokada hooka/CZERWONY lub rzeczywisty
   limit; `nieznany` = brak wiarygodnego odczytu zapasu. Historia przydziałów
   i raport tokenów nie dają procentu pozostałego limitu. Nie wymyślasz
   procentów ani nie wymagasz jednakowego pomiaru różnych abonamentów.

   ŻÓŁTY ostrzega, nie blokuje mocnego wykonawcy na zapas. CZERWONY
   blokuje subagentów Claude'a poza `zwiadowca` i `mechanik`.
   Zachowany wyjątek `[konieczny: powód]` dla krytycznego briefu wymaga
   zgłoszenia użytkownikowi; nie rozszerzasz go ze względu na koszt.
   Przy CZERWONYM brief `wykonawca-opus` może trafić do Muse Wonder
   Full `max` albo czekać — nigdy do Gemini, Sonneta ani Codexa. Ten wyjątek
   nie otwiera high-stakes na inne linie.

   Limit albo rzeczywiste niepowodzenie nie uruchamiają stałej kolejności
   fallbacków. Odbierasz stan artefaktów, aktualizujesz sygnał (limit →
   `zablokowany`), ponownie kwalifikujesz wykonawcę lub recenzenta
   i zapisujesz nową parę model/native effort, powód, pewność i alternatywy.
   Figma nadal wymaga faktycznego MCP, recenzja innej rodziny, a testy
   właściwego oracle. Bramka Sol `max` zachowuje model i effort;
   jej limit nie uprawnia do słabszej bramki. Gemini po 3 × 503 traktujesz
   jako rzeczywiste niepowodzenie linii i ponownie oceniasz kandydatów.

   Gdy żadna bezpieczna linia nie jest dostępna, zatrzymujesz zadanie
   i zgłaszasz blokadę z brakującym warunkiem. Zmianę linii meldujesz
   jednym zdaniem. Po resecie limitu ponownie kwalifikujesz kandydatów,
   bez automatycznego powrotu do stałego przydziału.

3. **Kwalifikacja wykonawcy zamiast stałego przydziału do linii.**
   Zwykłe briefy bez niezmiennika high-stakes mogą trafić do każdej
   kwalifikującej się linii, także Codexa już w planie. Dostęp do Figmy,
   narzędzi/test oracle i kontekstu oraz uprawnienia są bramkami, nie
   argumentami do równoważenia ceną. Wykonawca ekranu sam czyta Figmę;
   Muse/Gemini dostają samodzielny tekstowy brief niewymagający makiety.

   Przydział planujesz w falach o rozłącznych plikach, jedną warstwą
   na brief. Wykonawca sprawdza tylko własne pliki i raportuje zwięźle;
   architekt odbiera rzeczywiste artefakty oraz pełne sprawdzenia fali.
   Koszt korekt i czas do akceptacji liczą się razem z kosztem pierwszego
   przebiegu. Nie traktujesz publicznego indeksu ani samej ceny tokenu
   jako dowodu jakości. Ograniczenia `external-workers` i skilli
   pomocniczych pozostają wiążące.

4. **Architekt pozostaje na Opusie `xhigh` w pierwszym pilotażu.**
   Odpowiada za dokumentację źródłową, decyzje, plan, briefy, wymagania
   narzędziowe, dowody, triaż i końcową akceptację. Nie pisze kodu/testów
   poza jednolinijkowym wyjątkiem reguły 11. Niewiadome dotyczące produktu,
   API, danych, bezpieczeństwa lub odbioru wracają do właściciela;
   pytania o wybór silnika rozstrzyga sam architekt. Zmiana routingu
   wykonawców nie zmienia architekta ani jego effortu.

5. **Start każdego subagenta Claude'a kosztuje ~58 k tokenów promptu**
   (zmierzone 2026-09-16) — drobiazgi łączę w jeden brief, nie rozsyłam
   pięciu wywołań po jednej linii.

6. **Bramka high-stakes — `gpt-6.1-sol` `max` (od 2026-10-05).**
   Fable nie recenzuje: jest z rodziny Sonneta i Opusa. Dla feature'a
   z uwierzytelnianiem/sesją, płatnościami, poświadczeniami/PIN-ami
   dostępowymi, migracją danych, naliczaniem wartości (punkty, nagrody,
   salda), jednorazowymi kodami albo limitami prób — według listy
   doprecyzowanej w regułach projektu — zachowujesz jedną końcową recenzję
   całego diffu przez `gpt-6.1-sol` `max`, po recenzjach fal i ich
   poprawkach, przed bramą potwierdzenia. Tylko odczyt i inna rodzina niż
   autor plików niezmiennika — te zawsze pisze `wykonawca-opus` (wyjątek
   CZERWONEGO: Muse Wonder Full `max`). Briefy Codexa bez niezmiennika w tej funkcji
   bramka też czyta, ale dla nich nie zastępuje recenzji fali z rodziny
   innej niż Codex (reguły 7 i 13). Recenzji nie dzielisz na porcje;
   bramka końcowa zawsze czyta cały diff w jednym przebiegu.

   Koszt wejścia (recenzja to w ~80 % czytanie kodu) i dotychczasowe
   lokalne znaleziska uzasadniają bramkę raz na feature, nie na etap.
   Przy dużym diffie bramka idzie osobno na każde repozytorium (FE, BE),
   sekwencyjnie — każde w całości, w jednym przebiegu. Nie obniżasz jej
   modelu ani effortu dla oszczędności ani po limicie. Twarda bramka nie
   staje się automatycznym wyborem Sola `max` dla zwykłych briefów.

   **Dlaczego nie Astra (decyzja właściciela 2026-10-05).** `gpt-6-astra`
   `max` nie mieści się w ChatGPT Plus: widełki 5–45 wiadomości / 5 h
   (Sol 6.1: 15–160), a 2026-10-05 jeden przebieg Astry `max` na 88 plikach
   FE wyczerpał okno 5 h po 6 minutach, bez raportu (wcześniej Astra ∥ Sol
   na 195 plikach BE — po 13 minutach). 6.1 Sol `max` ma II 51,8 za 0,72 $
   na zadanie wobec Astry `max` 52,7 za 3,26 $ (AA, 2026-09-30). Próba
   Astra/Sol z 2026-09-30 jest zamknięta jako niewykonalna na Plusie.
   Gdy Codex jest zablokowany limitem, bramka czeka na reset; 2026-10-05
   (PBI #1604 + #2370) właściciel zlecił jednorazowo bramkę na Sparku `max`
   — to decyzja dla tej funkcji, nie zastępstwo z reguły.

7. **Codex — dopuszczalny od planowania, z kosztem i effortem per brief.**
   `gpt-6.1-sol` obsługuje natywne `low/medium/high/xhigh/max/ultra`,
   a `gpt-6-luna` `low/medium/high/xhigh/max`; potwierdzasz obsługę
   w danym narzędziu. Nie wysyłasz nieobsługiwanego effortu, nie utożsamiasz
   go z Claude'em/Muse/Gemini i nie wybierasz niższego effortu
   wbrew stawce. Zachowane porównania kosztu Sola/Luny oraz próbę
   researchu stosujesz jako ograniczone dane, bez automatycznego
   `research → Sol medium` ani `recenzja → Sol high`.

   Implementacja/testy/research/audyt i recenzja są dopuszczalne po
   kwalifikacji; implementację i testy dzielisz na porcje ≤ 5 plików.
   Recenzji nie dzielisz na porcje; bramka końcowa z reguły 6 zawsze czyta
   cały diff w jednym przebiegu. Figma/Playwright wymagają
   potwierdzonego dostępu. Research bez poleceń powłoki, recenzja
   `-Mode review` tylko do odczytu, nie własna rodzina. Codex nie
   przejmuje high-stakes wymagającego Opusa: pliki niosące niezmiennik
   zawsze pisze `wykonawca-opus` (wyjątek CZERWONEGO: Muse Wonder Full `max`), więc
   końcowa bramka Sol z rodziny Codex jest wobec nich niezależna.
   W funkcji high-stakes Codex może pisać briefy bez niezmiennika (ekrany,
   szablony, style, i18n, testy bez niezmiennika); ich niezależność
   zapewnia recenzja fali z rodziny innej niż Codex. Bramka czyta cały
   diff funkcji, także te pliki, ale dla nich nie zastępuje recenzji fali.
   Limit powoduje ponowną kwalifikację wg reguły 2, nie z góry wskazaną
   słabszą linię. Adapter Codexa zachowuje własne ograniczenia narzędzi.

   **Pula Codexa.** Codex działa na ChatGPT Plus — najmniejszej puli
   (bramka Astra `max` na PBI #2137 zjadła ~66 pkt okna 5 h i ~10 %
   tygodnia, a 2026-10-05 jeden przebieg Astry `max` wyczerpał okno po
   6 minutach — stąd bramka na Solu, reguła 6). Sygnał puli Codexa jest zwykle `nieznany` (wrapper nie podaje
   zapasu) — nie szacujesz procentu z historii ani z ceny. W funkcji
   high-stakes przy sygnale `nieznany` Codex dostaje co najwyżej krótkie
   briefy bez niezmiennika (≤ 5 plików, effort nie wyższy niż `high`);
   dłuższe lub cięższe idą do innej dopuszczonej linii. Po pierwszym
   komunikacie limitu Codexa przed bramką (sygnał `zablokowany`) nie
   przydzielasz mu kolejnych briefów tej funkcji — bramka ma pierwszeństwo.
   Ogólnie przy kwalifikacji Codexa liczysz zużycie jego puli: bez długich
   przebiegów i bez wysokich effortów nieuzasadnionych briefem.

   **Zachowane ograniczenia i konfiguracja CLI Codexa.** Poniższe
   informacje techniczne pozostają w mocy; opis domyślnej konfiguracji
   CLI nie przydziela briefu do modelu. Architekt zapisuje jawnie wybraną
   obsługiwaną parę model/native effort po kwalifikacji.

   Obsługiwane efforty Codexa, zgodnie z `worker-run.ps1`: nazwy effortów to `minimal`, `low`, `medium`, `high`, `xhigh`, `max` i `ultra`, lecz żaden model GPT-6 nie wspiera `minimal`; Sol/Astra
   (GPT-6.1 Sol, GPT-6 Sol i GPT-6 Astra) — `low`, `medium`, `high`,
   `xhigh`, `max` i `ultra`; Luna (GPT-6) — `low`, `medium`,
   `high`, `xhigh` i `max`.
   Dla par wymienionych w tabeli wrapper odrzuca nieobsługiwany effort przed startem; dla sluga spoza tabeli ostrzega bez lokalnej weryfikacji. Historyczna obserwacja z 2026-09-30: Luna `max` (II 37,3 ≈ Sonnet 5 `max` 38,2)
   była obserwowana jako opcja per zadanie, gdy poprawność ważniejsza niż ~100-sekundowy start. Codex jest dopuszczony do zwykłych briefów. Architekt kwalifikuje
   każdy brief i wybiera
   dopuszczoną parę model–effort według jego złożoności, niepewności,
   ryzyka, dostępności, narzędzi i lokalnych wyników zaakceptowanych briefów. Historyczny odczyt widełek Plusa / 5 h (oficjalne, odczyt 2026-09-30): Luna
   350–3000 · Sol 6.1 15–160 · Astra 5–45; `gpt-6-sol` (15–150) w tym odczycie historycznym. Macierz pilotażu wymienia tylko 6.1 Sol/Lunę jako zakres wybranej macierzy kandydatów, nie jako ograniczenie adaptera — adapter obsługuje także `gpt-6-sol` i linię GPT-5.6. **GPT-6 wymaga Codex CLI ≥ 0.155**
   — na 0.153.4 API odrzuca model komunikatem „not supported when using Codex
   with a ChatGPT account" (zmierzone 2026-09-23); `gpt-6.1-sol` przyszedł
   w katalogu klienta 0.159.2 i na nim działa (test 2026-09-30), 0.156.1
   nie sprawdzony.

8. **Muse — model i effort per archetyp briefu (od 2026-10-20,
   zaostrzone 2026-10-25).** Właściciel 2026-10-20: „wypłaszczyć, żeby nie
   zabijać limitu pierwszego dnia i używać rozumowania tylko tam, gdzie
   trzeba” — tydzień od 19.10 wyczerpał się po ~25 h na 21 przebiegach
   Wondera Full `max`. 2026-10-25: Wonder jest „BARDZO drogi — możemy go
   używać, ale racjonalnie”, a Spark 1.3 contributor „bardzo tani” (cennik
   i kalibracja puli — akapit „Cennik Muse” wyżej). Linia Muse ma dwa
   szczeble kosztu, bez pośredniego: Spark contributor (~0,5 % tygodnia na
   przebieg) i Wonder (~5 % tygodnia na przebieg, Full i 1.0 tak samo).
   Parę wyznacza archetyp briefu:

   | Archetyp briefu w linii Muse | Para | Dowód |
   | --- | --- | --- |
   | Wyjątek CZERWONEGO (plik niezmiennika `wykonawca-opus`); recenzja fali plików niezmiennika high-stakes | Wonder Full `max`, w limicie Wondera (niżej) | najbliżej Opusa `xhigh` (TB4 0,571 wobec 0,596); 8 recenzji 15–20.10: potwierdzone P1 (2722-BE-1a, 2747-R1, R1F), 0 obalonych P0/P1 |
   | Implementacja bez niezmiennika (ekran bez Figmy, serwis, BE CRUD, testy), złożony brief bez niezmiennika, rewizje dokumentacji, audyt SCSS, QA Sphere (także w funkcji high-stakes), korekty `-K`, ponowna recenzja poprawek, recenzja niskiej i średniej stawki | Spark 1.3 `max` | 12–14.10: 110 przebiegów, briefy 0–1 rundy z wykonania (2705-F1a/F1b/F2a/F4, 2694-T1/T2); Full w QA Sphere, dokumentacji i warstwie widoku 15–20.10 dał ten sam wynik za ~10× puli |
   | Operacyjne: worker przeglądarki (`pwcli`), zakup na PRE, pozycje ADO, korekta z gotową treścią (≤ 3 pliki) | Spark 1.3 `high` | mało rozumowania; przegląd 1: `high` 0,35 rundy z wykonania, mediana 4 min |
   | Sonda dostępu, podbicie wersji | Spark 1.3 `low` | — |

   **Wonder 1.0 nie ma archetypu.** Cennik nie daje mu trybu contributor
   (standard 4 / 20 $ za 1M, ~60× Sparka contributor przy naszym
   profilu), a pula nie pokazała, że jest tańszy od Full — za tę samą cenę
   bierzesz silniejszego Full. Wonder 1.0 przydzielasz tylko z powodem
   zapisanym w briefie i rejestrze; liczy się do limitu jak Full.

   Parę wyższą niż w tabeli bierzesz tylko z powodem zapisanym w briefie
   i we wpisie rejestru (np. Spark `high` → `max` po `NEED_FALLBACK`/`LOOP`
   przeglądarki, Spark → Wonder Full przy recenzji, której stawka okazała
   się high-stakes). Effort Muse to słaba dźwignia puli (odczyt AA
   2026-10-20): oszczędzasz modelem i krótszym briefem (reguła 15), nie
   zejściem z `max` na `xhigh`. Spark zawsze z sufiksem `-contributor` —
   `muse-spark-1.3` bez niego kosztuje wg cennika 12–75× więcej.

   **Limit Wondera i tempo tygodnia.** Tydzień ≈ 21 przebiegów Wondera
   ≈ 190 przebiegów Sparka `max` (1 Wonder ≈ 10 Sparków). Wonder — Full
   i 1.0 razem, łącznie z przebiegami przerwanymi — dostaje najwyżej
   **2 przebiegi na dzień roboczy i 6 na tydzień** (~30 % puli); reszta
   (~130 przebiegów) zostaje dla Sparka. Przed przydziałem pary Wonder
   sprawdzasz przebiegi od poniedziałku 00:00 UTC (polecenie w skillu
   `external-workers`). Po limicie recenzja plików niezmiennika idzie do
   innej dopuszczonej rodziny (Sol `high` z uwagą na pulę Codexa przed
   bramką, reguła 7) albo czeka na następny dzień; wyjątek CZERWONEGO
   czeka. Brief Wondera trzyma kontekst krótko — diff plików niezmiennika
   i ich specyfikacja, bez przeglądu całego repo (przebieg Full kosztował
   4,8–8,8 mln tokenów). To szacunek z dwóch wyczerpań, nie procent zapasu
   — po 429 obowiązuje reguła 2, a 429 z resetem w poniedziałek 00:00Z
   oznacza `zablokowany` do resetu. Pliki niezmiennika high-stakes poza
   wyjątkiem CZERWONEGO nadal pisze wyłącznie `wykonawca-opus` (decyzja
   właściciela 2026-10-12) — wyższy II Wondera Full nie otwiera
   high-stakes. Ograniczenia narzędzi/uprawnień macierzy pozostają twarde;
   brak Figmy nie jest kosztem do skompensowania.

   Ocena po 10–15 istotnych briefach Muse w tym podziale: czy tydzień
   dociąga do niedzieli, ile przebiegów Wondera zużył wobec limitu, rundy
   z wykonania per para (wobec Sparka `max` 12–14.10 i Wondera Full
   15–20.10), potwierdzone i obalone P0/P1 Sparka `max` w recenzjach
   średniej stawki i w QA Sphere funkcji high-stakes (wobec Wondera Full
   15–20.10).

   Historia: od 2026-10-12 domyślny był Spark 1.3 `max` (TB4 0,333 wobec
   `xhigh` 0,167, II 48,1 wobec 45,1, ~17 % więcej tokenów, ~2× wolniej);
   2026-10-14…19 Wonder Full `max` w każdej roli (właściciel: „użyjmy
   nowego Muse Wonder”). Bilans 15–20.10: recenzje plików niezmiennika
   uzasadniły Full (potwierdzone P1); QA Sphere, rewizje dokumentacji, PRE,
   przeglądarka i warstwa widoku dały ten sam wynik, który Spark `max`
   dawał 12–14.10 (0–1 rundy), za ~10× puli na przebieg. 2026-10-20…24
   Wonder 1.0 `max` miał średnią stawkę i QA Sphere funkcji high-stakes
   (założenie: token ~3,5–4× tańszy od Full) — bez ani jednego przebiegu,
   bo pula była zablokowana do 26.10; cennik z 2026-10-25 obalił założenie
   i te archetypy przeszły na Sparka `max`.

9. **Wynik obcego silnika zawsze waliduję** — czytam diff, uruchamiam `lint`,
   testy i build. Raport workera **nie jest dowodem** (zasada „evidence closes
   a task" obowiązuje tu podwójnie).
10. **Brief dla workera musi być samowystarczalny.** Muse i Codex startują bez
    kontekstu rozmowy. Braku kontekstu nie nadrobią domysłem — zrobią coś innego.
11. Jeśli zadanie jest **pytaniem, jednolinijkową zmianą albo czymś, gdzie
    napisanie briefu kosztuje więcej niż wykonanie** — robię je sam. Routing nie
    jest obowiązkiem delegowania.
12. **Zmiana pary po limicie lub niedostępności.** Architekt sam ponownie
    kwalifikuje brief i wybiera dopuszczoną parę model–effort, uwzględniając
    złożoność, niepewność, ryzyko, aktualną dostępność, faktyczne narzędzia
    i lokalne wyniki zaakceptowanych briefów oraz wszystkie twarde bramki.
    Melduje zmianę jednym zdaniem i nie pyta użytkownika o routing.
    Brak dopuszczonej pary oznacza blokadę briefu, nie obejście ograniczeń.

13. **Niezależna recenzja po każdej fali, adaptacyjny wybór recenzenta.**
    Przed rozpoczęciem zależnej fali kwalifikujesz i wybierasz recenzenta
    per brief: tylko odczyt, właściwy kontekst/narzędzia, zdolność odpowiednia
    do stawki oraz inna rodzina niż autor. Wyższa stawka wymaga wyższej
    klasy recenzji. Przy niskiej stawce preferujesz Sola `high` albo
    Gemini `high` przed Muse (decyzja właściciela 2026-10-12 po
    przeglądzie 1: Spark `xhigh` zgłaszał najwięcej P0/P1 do obalenia —
    43 w 31 recenzjach; Wonder Full w 8 recenzjach 15–20.10 nie zgłosił
    P0/P1 do obalenia, ale przy niskiej stawce preferencja zostaje ze
    względu na tygodniową pulę Muse); przy wyższej stawce Muse jest
    kandydatem z parą z tabeli reguły 8 — Wonder Full `max` dla plików
    niezmiennika (w limicie Wondera), Spark `max` dla średniej stawki
    (od 2026-10-25; wcześniej Wonder `max`) — preferencja wśród
    dopuszczonych, nie stała kolejność. Sol jest kandydatem bez
    oczekiwania na limit, ale nie recenzuje Codexa; Muse nie recenzuje
    Muse (Wonder i Spark to jedna rodzina), Gemini nie recenzuje Gemini,
    a Fable nie recenzuje wcale. W mieszanej fali dzielisz zbiory zmian
    per autor i dla każdego zapewniasz inną rodzinę. Nie ograniczasz
    liczby potrzebnych recenzji; nie dublujesz ich równolegle.

    Model/native effort, uzasadnienie, pewność, dopuszczone alternatywy
    i status dostępności zapisujesz również dla recenzenta. Limit recenzenta
    prowadzi do ponownej kwalifikacji wg reguły 2; brak niezależnej
    bezpiecznej linii jest blokadą. Publiczny ranking ani historyczna
    przewaga Spark/Gemini nie tworzą wyłączności lub stałego fallbacku.

    Brief recenzenta wymaga sprawdzenia scenariusza P0/P1 przed zgłoszeniem.
    Architekt weryfikuje znaleziska względem repo i wymagań, sprawdza
    rzeczywisty diff, testy, format, build oraz wymagane dowody po fali.
    Raport wykonawcy/recenzenta sam nie dowodzi ukończenia. Poprawki wracają
    do autora, o ile nadal się kwalifikuje; w przeciwnym razie oceniasz
    kandydatów ponownie. Odbiór poprawki pozostaje odpowiedzialnością
    architekta. Okresowa ocena routingu nie zastępuje recenzji kodu.

    Istotne briefy zapisujesz w `docs/model-routing-evaluation.md`
    w repo `Claude_Skills`; pola i szablon wpisu wg sekcji 3–4
    `docs/model-routing-evaluation.md`. Bez promptów, diffów, danych
    osobowych, poświadczeń i surowych tokenów.
    Tokeny pozostają w raporcie per ADO. Mechaniczne drobiazgi nie
    wymagają wpisu. Pierwszy przegląd po 10–15 istotnych briefach,
    kolejne po 10–15 lub istotnej zmianie modeli/pomiaru limitów;
    dodatkowy po istotnym błędzie lub kilku kosztownych poprawkach.
    Oceniasz per archetyp; mała próbka nie ustanawia rankingu.

    Zachowane datowane wyniki poniżej są materiałem do oceny lokalnej,
    nie uniwersalnym przypisaniem recenzenta.

    Historyczny wynik próby recenzji (2026-09-23, 3 etapy: PBI #2282 + DomSztukiFE ×2):
    w tej próbie Spark recenzował diffy Sonneta/Codexa, a Gemini — diffy Sparka; Sol
    nie dublował ich na tych plikach (w tej próbie Sol miał trudny research, bramkę Astry
    i przelew). Obaj próbowani nie przegapili żadnego P1 Sola i znaleźli więcej
    realnych defektów, ale produkują fałszywe P0/P1 (Spark 5, Gemini 2) —
    brief recenzenta wymaga sprawdzenia scenariusza P0/P1 przed zgłoszeniem,
    a architekt obala każde P0/P1 jednym poleceniem przed poprawką.
    To wynik historyczny bez obecnej wyłączności: bieżący wybór recenzenta to niezależna rodzina wybrana per brief (reguła 13).
    Historyczny wynik próby researchu (2026-09-24, audyt landingu DTCode): warunek
    powrotu spełniony — raport trendów podał statystyki konwersji ze źródłem
    w postaci gołej domeny (medium.com, unbounce.com, nngroup.com), a 2 z 5
    sprawdzonych nagród Awwwards miały zły adres lub datę; raport techniczny
    był rzetelny. Research Gemini z 2026-09-24 jest historycznym sygnałem jakości,
    preferencją do ponownej oceny per brief — bez zakazu researchu Gemini
    i bez stałego przydziału rutynowego researchu do Sola `medium`.
    Historyczna obserwacja audytu SCSS na Sparku — 1 przebieg bez
    pominiętego pliku, próba nadal ograniczona.

14. **Fale o rozłącznych celach i zachowane limity równoległości.**
    Architekt dzieli plan na `etap → fala → brief → linia`, dopisując
    model/native effort, powód, pewność, alternatywy i dostępność wykonawcy
    oraz recenzenta. Liczba briefów per linia opisuje obciążenie, nie
    poprawność planu. Nie rozdzielasz mechanicznie „FE do Sonneta,
    BE do Muse, i18n do Gemini”; kandydatów wybierasz wg bramek
    i dowodów danego briefu. Ekran high-stakes bez niezmiennika jest
    osobnym briefem od pliku niezmiennika wymagającego Opusa.

    Briefy jednej fali wysyłasz naraz, subagentów i wrappery w tle,
    każde osobnym wywołaniem wrappera, bez `Start-Job`. Cele/pliki
    nie mogą się nakładać. Zachowujesz najwyżej ~4 briefy z pętlą
    testów jednocześnie, do ~10 briefów na falę i rezerwę na 2–3 korekty.
    Muse bez limitu slotów nie omija rozłączności ani limitu pętli testów.

    Wykonawcy sprawdzają własne pliki, z cichym wyjściem i zwięzłym
    raportem: `npx --no-install eslint <pliki>`,
    `npx --no-install prettier --check <pliki>`,
    `ng test --include <spec>`. Zakaz gita zmieniającego stan,
    `npm install`, `npm run lint:fix`, `npm run format` i
    `npm run build`; przy > 1 wykonawcy BE także zakaz
    `dotnet build`/`dotnet test`. Brief każdej linii mówi to wprost,
    również nadpisując „Finishing Every Implementation” dla Claude'a.
    Architekt wykonuje pełną walidację po fali i odbiera niezależną
    recenzję przed zależną falą.

    Tory poboczne (Figma, dokumentacja, ADO) ruszają, gdy gotowa jest
    decyzja, od której zależą, i ich cele są rozłączne. Aktualizacja
    dokumentacji przy zmianie zachowania/API jest obowiązkowa.
    Wykonawcę dobierasz do briefu; Figma wymaga właściwego MCP,
    QA Sphere osobnej procedury. Samodzielne briefy nie polegają na
    kontekście głównej sesji. Równoległe operacje na jednej stronie
    przeglądarki/sekcji Figmy nie są rozłączne; weryfikujesz
    `location.href` przed każdym zrzutem.

    **Próby ograniczone.** Poniższe datowane warunki, modele/efforty
    i porównania kosztu dotyczą tylko opisanych prób, nie wszystkich
    briefów danej linii. Nie rozszerzają dostępu MCP, nie zmieniają
    architekta pilotażu i nie zastępują odbioru artefaktów.

    **Próba A/B linii Figmy — zamknięta 2026-10-12, zostaje Sonnet.**
    `wykonawca` (Sonnet 5.5 `high`) wobec Opusa 5.5 `medium`, po 3 briefy
    (PBI #1603/#2369, stały recenzent Spark `xhigh`): Sonnet 4,71 $/brief,
    1,67 rundy, 4,0 defektu; Opus `medium` 6,42 $/brief (1,36× > progu
    1,3×), 1,0 rundy, 2,67 defektu. Decyzja właściciela wg kryterium
    ustalonego przed próbą; agent `wykonawca-opus-medium` przeniesiony do
    `~/.claude/agents-archiwum/`. Dane: rejestr (wpisy 1603-FE-2…K-1)
    i pamięć `proba-ab-linii-figmy`.

    **Próba testera na Haiku 5.5 — zamknięta 2026-10-13, Haiku przejmuje
    linię `tester`.** `tester` (Sonnet 5.5 `medium`) wobec `tester-haiku`
    (Haiku 5.5 `xhigh`), po 3 briefy (PBI #2705, #2715, #2473; stały
    recenzent Spark `max`): Sonnet 4,08 $/brief, 1,33 rundy, 10,3 realnego
    defektu; Haiku 2,44 $/brief (0,60× ≤ progu 0,75×), 1,00 rundy, 10,3
    defektu. Kryterium ustalone przed próbą spełnione; od 2026-10-13
    `tester` biegnie na Haiku 5.5 `xhigh`, stary agent (Sonnet) i agent
    próby `tester-haiku` przeniesione do `~/.claude/agents-archiwum/`.
    Zastrzeżenia do obserwacji w kolejnych briefach: w próbie nie było
    briefu Buga (warunek „fałszywy czerwony” niesprawdzony), Haiku miał
    3 P1 fałszywej zieleni wobec 2 u Sonneta (wszystkie w jednym briefie),
    a 2 z 3 jego briefów przekroczyły 300 tys. kontekstu i szły
    z kontynuacją (koszt wliczony). Dane: rejestr (wpisy 2705-BT-1/2,
    2715-T1a/b, 2473-T-1) i pamięć `proba-testera-haiku`.

15. **Długość kontekstu to główny koszt w puli Claude'a** (pomiar
    2026-09-28, transkrypty 09-18…28, koszt w cenach API): 54–81 % kosztu
    każdej linii to ponowne czytanie kontekstu przy każdym wywołaniu
    narzędzia, a wyjście, na które działa effort, to tylko 9–18 %. Przebiegi
    dobijające do 700–970 tys. tokenów kosztowały po 40–98 $; średni
    przebieg `wykonawca-opus` 31,7 $, `wykonawca` 14,7 $. Stąd:
    - jeden brief = jedna warstwa (slice BE albo ekran FE albo testy), cel
      ≤ ~150 wywołań i ≤ ~300 tys. kontekstu; większą pracę dzielę na
      briefy w fali — koszt rośnie mniej więcej z kwadratem długości
      przebiegu, więc dwa krótsze kosztują razem mniej niż jeden długi;
    - brief każe uruchamiać sprawdzenia z cichym wyjściem (same błędy), bez
      zrzucania całych plików i pełnych logów do kontekstu;
    - **Weryfikacja w przeglądarce — najpierw `browser-check`** (od
      2026-10-04, decyzja użytkownika; projekty z UI webowym): zrzuty 2×2
      i przejścia opisane w scenariuszu JSON robi architekt narzędziem
      `D:\projects\DTCode\Claude_Skills\browser-check`. Scenariusz to plik
      sesji — specyfikacja odbioru z planu, nie test w repo produktu (E2E
      prowadzi kto inny; Playwright tylko do ręcznego odtworzenia, nigdy
      testy E2E w kodzie) i nie zastępstwo czerwonego testu jednostkowego
      Buga — chyba że błąd widać wyłącznie w przeglądarce. Tryb
      `matrix` bez modelu, tryb `flows` z Jev (TypeSafe, poza abonamentami;
      w tekście strony maskowane są sekrety, e-maile i telefony, reszta
      tekstu i `testData` idą jawnie — `testData` tylko syntetyczne).
      Werdykt: asercje, PNG oglądane przez architekta i błędy konsoli/sieci
      z raportu; PASS bez żadnej akcji (`passedWithoutActions`) to wada
      scenariusza, nie dowód. Pomiar 2026-10-04, te same 5 przejść: 18 s
      wobec 149 s Sparka przez MCP, ~100× mniej tokenów. Pełny triaż wyników
      — skill projektu. **Worker przeglądarkowy** wchodzi dopiero, gdy raport
      nie rozstrzyga (np. `NEED_FALLBACK`, `LOOP`, `MAX_STEPS`, wynik
      powtórzony po jednej powtórce) albo dla interakcji spoza scenariusza:
      architekt wybiera go per brief (Muse, Gemini lub Codex z faktycznie
      potwierdzonym narzędziem, bez stałej trasy), licząc wzrost kosztu
      kontekstu powodowany zrzutami; jego brief dziedziczy zakazy scenariusza
      i zakaz akcji nieodwracalnych. **Od 2026-10-12 (decyzja użytkownika)
      tam, gdzie działa, steruje przez Playwright CLI**
      (`Claude_Skills/browser-check/pwcli`, opis i sekcje briefu
      w `CLI-WORKER.md`): łączy polecenia w jednym wywołaniu powłoki
      i celuje `find` / `--raw eval` zamiast pełnych snapshotów. Pomiar
      2026-10-12 (Spark `max`, 5 przejść, 2 przebiegi na ramię, 30/30 PASS):
      CLI 0,59–0,64 mln tokenów wejścia i 18–19 tur wobec MCP 1,83–2,25 mln
      i 37–42 tur; MCP z tą samą instrukcją oszczędzania — 1,77–2,16 mln
      i 43–50 tur, więc zysk daje łączenie poleceń, nie sam zakaz
      snapshotów. CLI działa dziś tylko w linii Muse: Gemini (`agy`) ubija
      demona sesji po każdym wywołaniu powłoki, a piaskownica Codexa blokuje
      `%LOCALAPPDATA%\ms-playwright` — tam zostaje Playwright MCP
      z `--isolated`. Różnica kosztu jest argumentem przy kwalifikacji
      linii, nie stałą trasą.
      Subagenci Claude'a zrzutów nie wykonują (koszt kontekstu). Sesji
      przeglądarki nie wolno współdzielić równolegle (osobna `-s=<nazwa>`
      w CLI, osobny przebieg MCP); przed każdym zrzutem sprawdź
      `location.href`.
    - **strażnik kontekstu subagentów** (od 2026-09-28, hook PostToolUse
      `~/.claude/bin/kontekst-hook.mjs`, progi w nim): przy 300 tys.
      (miękko, raz) subagent kończy normalnie, jeśli zostało ~20 wywołań,
      inaczej domyka bieżącą jednostkę pracy i oddaje raport przekazania;
      przy 450 tys. (twardo, powtarzane co +50 tys.) nie zaczyna nowej
      jednostki. Nikogo nie przerywa w pół kroku — złoty środek między
      kosztem a jakością (decyzja użytkownika: „bez utraty jakości”).
      Raport przekazania waliduję jak każdy wynik (diff zrobionego), a resztę
      zlecam **świeżemu agentowi tej samej linii**: pierwotny brief + raport
      przekazania (decyzje i pułapki dosłownie) + „nie powtarzaj zrobionego,
      zacznij od sprawdzenia stanu poleceniem X”. Dziennik:
      `~/.claude/limity/kontekst.jsonl`. **Ocena jakości:** rundy korekty
      briefów z kontynuacją wobec briefów bez niej (dane jak w próbie fal);
      jeśli kontynuacje wymagają więcej poprawek, podnoszę progi, zamiast
      je utrzymywać. Progi zależą od okna modelu: min(300 tys., 60 % okna)
      i min(450 tys., 80 % okna) — Haiku 4.5 (okno 200 tys.) dostaje
      120/160 tys., Sonnet, Opus i Haiku 5.5 (1M) 300/450 tys.;
    - **workerów zewnętrznych strażnik nie widzi** (osobny proces, bez
      hooka) i według pomiaru go nie potrzebują (09-14…28,
      `python ~/.claude/bin/kontekst-workerow.py`): Spark — mediana
      100 tys., p90 182 tys., > 300 tys. w 1 na 186 przebiegów (okno 1M,
      własna kompakcja `--context-compaction-*` na domyślnych progach);
      Gemini — mediana 144 tys., p90 244 tys., 1 na 72; Codex ma okno
      258 tys. i kompaktuje sam (maks. 238 tys.). Ich pilnuje podział briefu
      z pierwszego punktu; pomiar powtarzam przy ocenie etapów, a próg
      w wrapperze dokładam dopiero wtedy, gdy przebiegi > 300 tys. przestaną
      być wyjątkiem;
    - `autoCompactWindow: 400000` w `~/.claude/settings.json` ma kompaktować
      sesję główną przy ~400 tys. — **niepotwierdzone**: sesja, w której go
      dopisano, skompaktowała się przy 577 tys.; sprawdzam w nowej sesji
      (`compact_boundary.preTokens` w transkrypcie). Subagentów pilnuje
      strażnik, nie kompakcja (domyślna kompakcja subagenta przyszła przy
      956 tys. i jest stratnym streszczeniem, nie przekazaniem);
    - raport wykonawcy jest zwięzły (co zmienione, dowody, odchylenia), bez
      wklejonego diffu — diff czytam sam, celowo i tylko potrzebne pliki.

Mechanika wywołań — komendy, tłumaczenie ścieżek, szablon briefu, pułapki:
skill **`external-workers`**.

**Wspólna sekcja w projektach (od 2026-09-28, decyzja użytkownika: wszystkie
projekty DTCode mają ten sam routing i zasady).** Każdy projekt ma w plikach
reguł identyczną sekcję „## Working Mode — Orchestrator + Subagents (both
stacks)” — angielskie streszczenie tego pliku. Źródło:
`D:\projects\DTCode\ZebraniFE\.claude\CLAUDE.md`; po każdej zmianie routingu
tutaj poprawiam ją tam i uruchamiam `python ~/.claude/bin/sync-routing.py`
(`--check` tylko sprawdza), potem commit i push we wszystkich repo. Progów
hooka sekcja nie powtarza — odsyła do reguły 2. Skrypt ostrzega, gdy
`AGENTS.md` przekroczy 64 000 B (limit `muse`; ZebraniFE jest najbliżej).
**Skrypt nie obejmuje skilla `implement-ado-feature-zebrani`** — jego
źródło (`D:\projects\DTCode\Claude_Skills\Implement ADO Feature – Zebrani\SKILL.md`,
Fazy 1, 2 i 4b) niesie routing i po każdej zmianie tutaj poprawiam je ręcznie,
potem commit i push w `Claude_Skills`. Loadery w repo projektu (wzorzec
`implement-ado-feature-loader Zebrani.md`, kopie w ZebraniFE i ZebraniBE) są
celowo neutralne silnikowo i przy zmianie routingu ich nie ruszam
(od 2026-09-28 — wcześniejsze streszczenie w loaderze zostało w tyle o dwie
wersje routingu).

## Zmiana progu CZERWONEGO okna 5 h — 2026-11-04

Decyzja właściciela (2026-11-04, Feature Zebrani #1690): próg blokady startu subagentów Claude'a w oknie 5 h podniesiony
z 85 % do **95 %** (`DENY_H5` w `~/.claude/bin/limity-hook.mjs`; opisy agentów `wykonawca` i `wykonawca-opus`).
Powód: 85 % zostawiało niewykorzystane ~15 pp okna, które i tak odnawia się co 5 h. Ostatnie ~5 pp to rezerwa sesji
architekta na odbiór i przekazania. Kontekst pomiaru z tego dnia: okno wzrosło z 17 % do 68 % w ~2,5 h przy dwóch
przebiegach `wykonawca-opus` (~320 tys. tokenów każdy), koordynatorze fali, jednym `wykonawca` i sesji architekta —
jeden brief Opusa to na oko 10–15 pp okna (pewność niska, pomiar mieszany). Próg tygodnia (95 %), ŻÓŁTY (okno 50 %,
tydzień 85 %, tempo +20 pp) i znacznik `[konieczny]` bez zmian.

## Codex: GPT-6.1 Terra jako kandydat w miejsce Sola `high` — 2026-11-04

Sonda przez wrapper (`-Model gpt-6.1-terra -Effort low -Access read`): exit 0 w 9 s, w logu `model: gpt-6.1-terra`.
Katalog klienta `codex-cli 0.159.2` podaje efforty `low…ultra`. Oficjalny cennik Codexa (learn.chatgpt.com/docs/pricing):
na Plusie GPT-6.1 Terra ma 35–285 wiadomości lokalnych na 5 h, GPT-6.1 Sol 15–160. Pro „from $100” ($100/$200/$500),
bez okna 5 h. Plus i Pro mogą dokupić kredyty.

Artificial Analysis (API i strony modeli, 2026-11-04):

| Wariant | Indeks inteligencji | Koszt zadania indeksu | Tokeny wyjścia indeksu |
| --- | --- | --- | --- |
| Sol `max` | 54,6 | — | — |
| Terra `max` | 51,3 | 0,96 $ | 99,4 mln |
| Sol `high` | 50,3 | 0,59 $ | 24,7 mln |
| Sol `medium` | 46,3 | 0,36 $ | 15,1 mln |
| Terra `xhigh` | 45,3 | 0,40 $ | 34,7 mln |
| Terra `high` | 42,4 | 0,26 $ | 20,6 mln |
| Spark 1.3 `max` (Muse) | 36,6 | — | — |

Ceny tokenów: Sol 2/10 $, Terra 1/5 $ za 1 mln (wejście/wyjście). Koszt indeksu AA jest zdominowany przez wyjście,
a nasze przebiegi — przez wejście. Rollouty Codexa od 2026-10-26: Sol `high` (92 przebiegi) — 8,6 mln wejścia bez
cache, 100 mln z cache, 0,63 mln wyjścia; przy cenniku Sola (cache 10 % ceny wejścia, założenie) koszt rozkłada się
40 % wejście, 46 % cache, 15 % wyjście. Szacunek kosztu przebiegu wobec Sola `high` (= 1,0): Terra `max` ≈ 0,73,
Terra `xhigh` ≈ 0,53, Terra `high` ≈ 0,49 (połowa ceny wejścia + wyjście skalowane gadatliwością z AA). Pewność niska:
nie wiadomo, czy limit Plusa liczy dokładnie wg ceny API, a gadatliwość agenta nie musi skalować się jak w indeksie.
Decyzja (reguła 7): Terra `max` — kandydat tam, gdzie Sol `high`/`medium`; nie bramka; recenzja plików niezmiennika
dopiero po ≥ 5 zaakceptowanych briefach Terry nie gorszych niż Sol `high`.

## Muse: kalibracja puli po zmianie planu — 2026-11-04

Właściciel: plan Muse kosztuje ~100 $/mies. (`muse usage` nadal podaje tier „Power Usage”). Koszt przebiegów tygodnia
od 2026-11-02 liczony z `payload.event.usage` zdarzeń `model_completed` w `session.jsonl` (konwencja: `input_tokens`
zawiera `cache_read_tokens`), cennik Spark contributor 0,002/0,10/0,20 $, Wonder 0,20/4,00/20,00 $ za 1 mln
(cache/wejście/wyjście):

- Spark (148 przebiegów, głównie `max`): 6,62 $ — średnio 0,045 $.
- Wonder Full `max` (8 przebiegów): 25,98 $ — średnio 3,25 $; 1 Wonder ≈ 73 Sparki; 80 % zużycia tygodnia.
- Odczyty `museUsage` przed kolejnymi Wonderami (tydzień): 0, 2, 2, 11, 17, 22, 24, 28 %; między odczytami ≈ 0,8–1,3 $
  na punkt procentowy → tydzień ≈ 100–115 $ po cenniku (wcześniej 40–46 $), Wonder ≈ 3,2 %, Spark `max` ≈ 0,045 %.
- 28 % przy ~42 % upływu tygodnia — w tym tempie ~65 % na koniec tygodnia. Limit wrappera 10 Wonderów/tydzień
  ≈ 32 % puli; 8 z 10 zużyte w środę. Limit bez zmian (decyzja właściciela).
