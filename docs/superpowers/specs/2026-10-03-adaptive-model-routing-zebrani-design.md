# Adaptacyjny dobór modeli w procedurze ADO Zebrani — projekt

Data: 2026-10-03

Status: zaakceptowany przez właściciela 2026-10-03; gotowy do planowania wdrożenia

## Cel

Zmienić procedurę ADO Zebrani tak, aby architekt Opus planował pracę, a model i effort były dobierane dla każdego briefu spośród wykonawców kwalifikujących się do danego zadania. Celem jest zwiększanie liczby zaakceptowanych zadań realizowanych w dostępnych abonamentach, przy zachowaniu minimalnego poziomu jakości i obowiązujących zabezpieczeń.

Jednostką doboru jest **brief wykonawczy**, a nie work item ADO. Rozmiar tasków ADO jest zbyt różny, by sam numer lub typ work itemu mówił, jaki model powinien go wykonać.

## Kontekst obecnego procesu

- Kanoniczna procedura mieszka w `Implement ADO Feature – Zebrani/SKILL.md`; globalne reguły routingu są w `~/.claude/CLAUDE.md`.
- `ZebraniFE/AGENTS.md` i `ZebraniBE/AGENTS.md` zawierają projektową kopię reguł routingu.
- Skill w Codexie jest adapterem. Używa narzędzi Codexa i wyraźnie wyklucza uruchamianie Claude’owych agentów, Sparka i Gemini. Pozostaje osobnym adapterem.
- Obecny proces już ma planowanie, fale o rozłącznych plikach, weryfikację architekta po fali i niezależną recenzję innej rodziny. Obecna zmiana dotyczy przede wszystkim kryteriów wyboru wykonawcy i trwałej oceny jakości routingu.
- `worker-run.ps1` zapisuje m.in. silnik, model, effort, czas i identyfikator przebiegu. `token-report.py` zestawia wykorzystanie modeli dla work itemu ADO. Nie zastępujemy tych mechanizmów.

## Zasady projektowe

1. **Ograniczenia jakości i ryzyka są bramkami, nie składnikami średniej.** Tańszy wybór nie może skompensować niespełnionego wymogu bezpieczeństwa, narzędzi lub weryfikacji.
2. **Dobór jest adaptacyjny, ale uzasadniony.** Każdy brief wykonawczy i recenzencki dostaje wybraną parę `model + native effort` oraz krótkie uzasadnienie. Efforty różnych dostawców nie uznaje się za równoważne tylko dlatego, że mają tę samą nazwę.
3. **Celem jest zaakceptowana praca, nie zużycie całego limitu.** Uwzględniamy spodziewane poprawki i czas do akceptacji, nie wyłącznie koszt pierwszego przebiegu.
4. **Dowody z repozytorium mają pierwszeństwo przed publicznym rankingiem.** Zewnętrzne rankingi mogą być wskazówką przy braku danych lokalnych, ale nie rozstrzygają samodzielnie routingu.
5. **Nie zgadujemy stanu abonamentu.** Każda decyzja o obciążeniu opisuje sygnał jako znany, ostrzegawczy, zablokowany albo nieznany. Nie dopisujemy procentów, których narzędzie nie podało.
6. **Architekt pozostaje odpowiedzialny.** Model może zaproponować route, ale to Opus zapisuje plan, zatwierdza briefy, sprawdza artefakty i podejmuje decyzję o akceptacji.

## Przepływ planowania i doboru

### 1. Podział pracy

Architekt tworzy plan po polsku, wskazuje zatwierdzoną dokumentację produktową, decyzje, pliki, zależności, kryteria akceptacji oraz dowody weryfikacji. Dzieli pracę na fale z rozłącznymi zbiorami plików zgodnie z regułami wspólnego drzewa roboczego. Brief pozostaje samodzielny i obejmuje jedną warstwę.

Niewiadoma, która wpływa na zachowanie produktu, API, bezpieczeństwo, dane lub kryterium odbioru, pozostaje pytaniem do właściciela. Plan nie przedstawia jej jako rozstrzygniętej.

### 2. Opis briefu

Przed wyborem modelu architekt zaznacza:

- stawkę i skutki błędu, w tym przynależność do istniejącej listy zadań wysokiej stawki;
- niepewność i nowość rozwiązania;
- zależności, zakres plików i potencjalny wpływ przekrojowy;
- potrzebne narzędzia, uprawnienia i kontekst, np. Figma, repo FE/BE, Playwright lub QA Sphere;
- dostępny test oracle: test jednostkowy, test integracyjny, przegląd w przeglądarce, PRE lub inny dowód;
- kryteria ukończenia, na podstawie których architekt zaakceptuje wynik.

### 3. Lista dopuszczonych kandydatów

Najpierw odrzucamy pary model-effort, które nie spełniają wymagań briefu. Kryteria kwalifikacji obejmują:

- poziom ryzyka i istniejące ograniczenia dla high-stakes;
- dostęp do potrzebnych narzędzi i kontekstu;
- możliwość bezpiecznego zapisu albo trybu tylko do odczytu;
- zgodność z zakresem testów i repozytorium;
- ograniczenia właściwych skilli pomocniczych, np. `qasphere-test-generator`;
- wymaganą niezależność rodziny modelu w recenzji.

Dotychczasowe zabezpieczenia zadań wysokiej stawki, Figma, sesji, płatności, danych, naliczania wartości i innych krytycznych niezmienników pozostają nienaruszone w pilotażu. Ekran z Figmy nadal wymaga wykonawcy z dostępem do Figmy. Praca równoległa nadal wymaga rozłącznych celów. Model nie może recenzować własnego diffu ani diffu swojej rodziny.

Globalna routing table utrzymuje się jako **macierz możliwości i ograniczeń**, nie macierz stałych przydziałów. Dla każdej linii wskazuje dostępne narzędzia i repozytoria, poziomy dostępu, rodziny wykluczone z recenzji, natywne efforty, stabilne wymogi wysokiej stawki oraz dane o dostępności. Kryteria obowiązkowe są wizualnie oddzielone od preferencji wynikających z dotychczasowych wyników.

### 4. Wybór modelu i effortu

Wśród dopuszczonych par architekt wybiera konfigurację z najlepszą przewidywaną szansą na akceptację przy rozsądnym zużyciu dostępnej przepustowości i czasie do wyniku. Bierze pod uwagę lokalne wyniki dla podobnych briefów, spodziewany koszt korekt i bieżące sygnały dostępności. Reguła obejmuje również recenzenta: kandydaci muszą mieć dostęp tylko do odczytu, kompetencje odpowiednie do zakresu oraz inną rodzinę niż autor.

Nie wprowadza się punktowej formuły ani stałej tabeli „typ taska → model” przed zebraniem danych lokalnych. W pierwszym pilotażu:

- model wysokiej klasy pozostaje architektem na `xhigh`, aby odseparować jakość planowania od zmiany routingu wykonawców;
- Codex staje się pełnoprawnym kandydatem do kwalifikujących się zadań, a nie tylko awaryjnym przelewem;
- model oraz effort wybiera się jawnie dla briefu z zachowaniem natywnych nazw opcji danego narzędzia;
- przy braku danych podobnego zadania wybór zachowuje wymagany poziom ryzyka, a pewność routingu oznacza się jako niską;
- po rzeczywistym niepowodzeniu architekt ponownie ocenia kwalifikujących się kandydatów i może przełączyć linię;
- po błędzie limitu architekt ponownie wylicza kwalifikujące się pary; jeśli żadna bezpieczna linia nie jest dostępna, zatrzymuje pracę i zgłasza blokadę zamiast wymuszać niedopuszczony fallback;
- wynik nie jest optymalizowany pod „zużyjmy wszystkie limity”.

Plan zachowuje tabelę `etap → fala → brief → linia`, ale dodaje model, native effort, krótkie uzasadnienie wyboru, pewność oraz dopuszczone alternatywy. Podsumowanie liczby briefów per linia pozostaje informacją o obciążeniu, nie kryterium poprawności planu.

### 5. Sygnały wykorzystania abonamentów

Wykorzystujemy istniejące sygnały i telemetrię. Hook Claude’a daje ostrzeżenie lub blokadę. Workery zewnętrzne zapisują przebieg i usage w istniejących raportach, ale nie dostarczają równomiernego, dokładnego podglądu pozostałego limitu wszystkich abonamentów. Gdy nie ma wiarygodnego odczytu zapasu, plan pokazuje `nieznany`; może użyć historii przypisanej pracy i faktycznych komunikatów limitu, lecz nie podaje pozornej precyzji.

Zmiana nie wymaga przebudowy `worker-run.ps1` ani `token-report.py` w pierwszej fazie. Jeżeli pilotaż pokaże, że brak wcześniejszego sygnału dla zewnętrznych pul uniemożliwia lepszy dobór, osobny projekt może rozważyć dodatkową telemetrię.

## Recenzja i odbiór

- Po każdej fali zachowujemy niezależną recenzję diffu przez inną rodzinę modelu niż autor. W mieszanej fali recenzujemy zbiory zmian per autor.
- Wybór modelu i effortu recenzenta jest adaptacyjny w obrębie dopuszczonych, niezależnych rodzin; zadania o wyższej stawce wymagają wyższej klasy recenzji.
- Architekt po każdej fali sprawdza rzeczywisty diff, testy, format, build i wymagane dowody; raport wykonawcy sam w sobie nie jest dowodem.
- Znaleziska recenzji weryfikuje się względem repozytorium i wymagań. Model recenzujący nie jest traktowany jako źródło prawdy.
- Dla obecnej listy high-stakes zachowujemy końcowy przegląd całego feature’a. Trwającego porównania Astry i Sola nie zmieniamy w ramach pilota routingu wykonawców.
- Przegląd jakości konkretnego kodu pozostaje po każdej fali. Nie zastępujemy go rzadszą recenzją zbiorczą po kilkunastu briefach.

## Rejestr pilotażu i okresowa ocena routingu

Dodajemy `docs/model-routing-evaluation.md` w repozytorium `Claude_Skills`. Zawiera krótki rekord na istotny brief — bez promptów, diffów, danych osobowych ani surowych tokenowych zestawień. Rekord ma pola:

- identyfikator lub typ zadania, bez treści biznesowej;
- archetyp, stawkę i poziom niepewności;
- wybraną linię, model i effort dla wykonania oraz recenzji, a także dopuszczone alternatywy;
- powód wyboru, bieżący sygnał dostępności i pewność routingu;
- wynik pierwszego podejścia i liczbę rund korekt;
- czas do akceptacji, potwierdzone i odrzucone znaleziska recenzenta według priorytetu oraz błędy wykryte po odbiorze, jeśli wystąpią;
- wynik właściwych testów, PRE lub innego wymaganego dowodu.

Wykorzystanie tokenów pozostaje w istniejącym raporcie per ADO — rejestr nie dubluje tych danych. Małe mechaniczne briefy bez istotnej pracy implementacyjnej nie wymagają osobnego wpisu.

Pierwszy przegląd routingu odbywa się po 10–15 istotnych briefach, a następne po kolejnych 10–15 briefach albo po istotnej zmianie modeli lub sposobu pomiaru limitów. To rytm operacyjny do oceny, nie twierdzenie o statystycznej wystarczalności. Wyniki rozpatrujemy per archetyp; jeśli próbka dla danego typu jest mała, nie wyciągamy z niej rankingu. Dodatkowy przegląd uruchamia też istotny błąd lub kilka kosztownych poprawek.

## Zakres zmian

Po akceptacji projektu implementacja obejmie:

1. Kanoniczny skill ADO Zebrani — zastąpienie tabeli przypisującej wykonawców głównie według rodzaju pracy regułami kwalifikacji i decyzji per brief oraz bump wersji z `5.14` do `5.15`.
2. Globalne `~/.claude/CLAUDE.md` — zmianę nadrzędnych reguł i tabel routingu, tak by nie przeczyły nowemu procesowi.
3. `ZebraniFE/AGENTS.md` i `ZebraniBE/AGENTS.md` — zsynchronizowanie projektowych kopii zasad routingu.
4. Nowy rejestr `docs/model-routing-evaluation.md` wraz z polami i regułą wpisu opisanymi wyżej.

Adapter Codexa pozostaje adapterem Codexa i nie zyskuje wywołań agentów Claude’a, Sparka ani Gemini. Skill `external-workers` pozostaje instrukcją wywoływania i nie dostaje odpowiedzialności za decyzję „kiedy”. `qasphere-test-generator` zachowuje swoje osobne ograniczenia wykonawcze w pilotażu; routing nie może ich nadpisywać. Instrukcje produktu, API, UI ani zachowania aplikacji się nie zmieniają, więc dokumentacja produktowa Zebrani pozostaje poza zakresem.

## Poza zakresem

- Automatyczny router kodowy, scoring numeryczny albo automatyczne uruchamianie kilku modeli dla tego samego briefu.
- Zmiana architekta lub jego effortu w pierwszym pilotażu.
- Usunięcie ograniczeń high-stakes, dostępu do Figmy, niezależnej rodziny recenzenta lub istniejących bramek testów.
- Zmiana końcowej bramki Astry/Sola przed rozstrzygnięciem już rozpoczętej próby.
- Modyfikacja wrappera i skryptu raportującego tokeny bez osobnego uzasadnienia z pilotażu.
- Commit, push, publikacja nowej wersji skilla ani zmiany statusów ADO jako część samego projektu.

## Kryteria akceptacji projektu po wdrożeniu

1. Każdy istotny brief ma jawne kryteria akceptacji, wymagania narzędziowe, wybór modelu i effortu oraz krótkie uzasadnienie.
2. Żaden wybór dynamiczny nie omija twardych ograniczeń ryzyka, dostępu ani niezależnej recenzji.
3. Codex może być wybrany do kwalifikujących się zadań bez czekania na awarię innej linii.
4. Architekt nadal weryfikuje artefakty i dowody po każdej fali; recenzja kodu nie zostaje zredukowana do okresowego przeglądu.
5. Procedura odróżnia obciążenie znane od nieznanego i nie raportuje wymyślonych procentów limitu.
6. Rejestr umożliwia okresowe porównanie pierwszego przejścia, poprawek, czasu, usterek z recenzji i wymaganego testowania per typ briefu.
7. Globalne reguły oraz instrukcje FE i BE są zgodne z kanonicznym skillem; adapter Codexa zachowuje ograniczenia swoich narzędzi.

## Samokontrola dokumentu

- Brak nierozstrzygniętych placeholderów.
- Kierunek nie wymaga wyliczeń kosztu, którego obecne narzędzia nie dostarczają.
- Rozdzielono recenzję fali od okresowej oceny routingu.
- Okres pilotażu 10–15 briefów jest oznaczony jako próg operacyjny, nie naukowy.
- Zakres zachowuje dotychczasowe zabezpieczenia wysokiej stawki oraz osobny adapter Codexa.
