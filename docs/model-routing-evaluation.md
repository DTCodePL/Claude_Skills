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

### Wpisy

## 5. Rytm przeglądów i ewaluacji

Okresowa analiza wpisów w rejestrze prowadzona jest w następującym rytmie operacyjnym:

1. **Pierwszy przegląd:** przeprowadzany po **10–15 istotnych briefach**.
2. **Kolejne przeglądy:** przeprowadzane po kolejnych **10–15 briefach** lub po **istotnej zmianie modeli bądź sposobu pomiaru limitów**.
3. **Dodatkowy przegląd doraźny:** uruchamiany po wystąpieniu **istotnego błędu** (np. defektu wykrytego po odbiorze lub na etapie integracji) albo po **kilku kosztownych poprawkach** (wielokrotne rundy korekt na briefie).
4. **Zasady interpretacji i oceny:**
   - Wyniki należy oceniać **per archetyp** zadania.
   - **Mała próbka nie uzasadnia rankingu:** jeśli dla danego archetypu liczba zrealizowanych briefów jest niewielka, nie wolno tworzyć definitywnych rankingów modeli ani automatycznych reguł sztywnego przypisania.
   - Wnioski z przeglądów stanowią wskazówkę operacyjną i podlegają walidacji przy zachowaniu twardych ograniczeń bezpieczeństwa, uprawnień i narzędzi.
