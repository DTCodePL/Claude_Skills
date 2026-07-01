---
name: qasphere-test-generator
description: Generuje kompletny zestaw test case'ów (happy + negative paths, dążąc do 100% pokrycia przypadków użycia) na podstawie wykonanego zadania/feature'a i tworzy je bezpośrednio w QA Sphere przez REST API. Test casy są po polsku, standalone, z pełnymi repro stepami (dane wejściowe, wyjściowe, instrukcje konfiguracji) tak, by wykonała je osoba widząca aplikację pierwszy raz. Skill sam mapuje repozytorium na właściwy projekt w QA Sphere. UŻYWAJ ZAWSZE, gdy user prosi o wygenerowanie test case'ów, pokrycie testowe, "testy do tego feature'a", "pokryj testami", "wrzuć testy do QA Sphere", "test casy z tego co zrobiliśmy" — nawet jeśli nie padnie słowo "skill" ani "QA Sphere" wprost, a kontekstem jest właśnie ukończone zadanie deweloperskie.
user-invocable: true
version: 1.2
---

# QA Sphere — Test Generator (v1.2)

> Kanoniczna, wersjonowana wersja skilla. Źródło prawdy: `DTCodePL/Claude_Skills`.
> Lokalnie używany jest tylko cienki loader, który pobiera ten plik z GitHuba.
>
> **Changelog**
>
> - **1.2** — foldery **zawsze** zagnieżdżane w folderze-korzeniu projektu (nigdy na najwyższym poziomie obok niego); doprecyzowanie budowy `path` i przykładu `folder/bulk`.
> - **1.1** — loader pobierający kanoniczną wersję skilla z GitHuba (raw URL); logika trzymana wyłącznie w repo `DTCodePL/Claude_Skills`.
> - **1.0** — pierwsza wersja: mapowanie repo→projekt, generowanie happy+negative z dążeniem do 100% pokrycia, standalone PL test casy, tworzenie przez REST API QA Sphere (foldery bulk-upsert, pole `automation`).

Skill bierze **ukończone zadanie** (zaimplementowany feature / naprawiony bug / zmiana w repo), wymyśla **wszystkie sensowne przypadki testowe** (happy + negatywne + brzegowe), zapisuje je jako **standalone test casy po polsku** i tworzy je w **QA Sphere przez API** — w **projekcie odpowiadającym aktualnemu repozytorium**.

## Konfiguracja (stałe)

```
BASE_URL  = https://dtcode.eu1.qasphere.com/api/public/v0
API_KEY   = apikey_eu13rznp1e.1CcVhdYnB_Tyomu8wuzDgcK.RvTs6WpatefApFqDFgDXauu
AUTH      nagłówek: Authorization: ApiKey <API_KEY>
```

Nie używaj polskich znaków, po prostu daj UTF-8.

**Wartości pola `automation`** (custom field, dropdown, system name `automation`): `Planned`, `Cannot be Automated`, `In Progress`, `Automated`, `Broken`. Świeżo wygenerowane testy są manualne → ustawiaj **`Planned`** (chyba że user powie inaczej).

Rate limit API: **20 req/s** na klucz. Przy seryjnym tworzeniu rób ~0,1 s przerwy między requestami — z zapasem.

---

## Przebieg (wykonuj po kolei)

### Krok 1 — Zidentyfikuj projekt QA Sphere odpowiadający repo

Skill działa w różnych repo, więc najpierw ustal właściwy projekt — **nie zgaduj, potwierdź**.

1. Ustal tożsamość repo:
   ```bash
   git remote get-url origin
   basename "$(git rev-parse --show-toplevel)"
   ```
2. Pobierz listę projektów:
   ```bash
   curl -s -H "Authorization: ApiKey $API_KEY" "$BASE_URL/project"
   ```
   Zwraca `{ projects: [{ id, code, title, links: [{url,text}], ... }] }`.
3. Dopasuj projekt do repo w tej kolejności pewności:
   - **a)** któryś z `links[].url` projektu zawiera URL remote'a repo (host + ścieżka org/repo) → najmocniejszy sygnał;
   - **b)** `code` lub `title` projektu odpowiada nazwie repo / produktu (np. repo `tachoping*` → projekt TachoPing; repo `ustawozerca*` → Ustawożerca);
   - **c)** brak jednoznacznego trafienia → **pokaż userowi listę projektów (code + title) i zapytaj, do którego wrzucić**. Nie twórz niczego bez potwierdzenia.
4. Zapamiętaj `PROJECT` = `code` wybranego projektu (np. `BD`). Kolejne wywołania używają `/project/$PROJECT/...`.

> Jeśli user wprost poda projekt — użyj go, ale zweryfikuj, że istnieje na liście.

### Krok 2 — Przeanalizuj zadanie i wylicz WSZYSTKIE przypadki

Cel: **100% pokrycia przypadków użycia**. Zbierz kontekst z rozmowy, diffa (`git diff`, `git log -1 -p`), zmienionych plików, opisu feature'a. Następnie wypisz przypadki, przechodząc przez **każdą** kategorię (pomiń tylko ewidentnie nie dotyczące — i powiedz, że pominąłeś):

- **Happy path** — główny scenariusz sukcesu i poprawne warianty.
- **Ścieżki alternatywne** — inne poprawne drogi do celu.
- **Walidacja wejścia** — pola puste/wymagane, za krótkie/za długie, zły format, znaki specjalne, biały znak, PL/Unicode, wstrzyknięcia (`<script>`, SQL-like).
- **Wartości brzegowe** — min, max, min-1, max+1, 0, granice dat/kwot/ilości.
- **Dane negatywne / błędne** — niespójne kombinacje, nieistniejące rekordy, złe ID.
- **Stany puste** — brak danych, pusta lista, pierwszy raz, brak wyników.
- **Uprawnienia i autoryzacja** — role, brak dostępu, niezalogowany, wygasła sesja/token, cudzy zasób.
- **Stany i konfiguracja** — feature flagi, ustawienia konta/projektu, plany/subskrypcje, zależności konfiguracyjne.
- **Błędy zewnętrzne** — timeout, 4xx/5xx zależnego API, brak sieci, padnięcie integracji (płatności, WhatsApp, KSeF).
- **Idempotencja / podwójne akcje** — podwójny submit, ponowne wysłanie, równoległe edycje.
- **Persystencja** — odświeżenie, powrót, ponowne wejście — czy stan się utrzymuje.
- **Lokalizacja / i18n** — jeśli wielojęzyczne (PL/EN/RU/UA).
- **Wydajność / wolumen** — duże listy, paginacja (jeśli dotyczy).

Dla każdego przypadku zanotuj: priorytet (high = krytyczny/happy path głównej ścieżki, medium = istotny, low = edge), kategorię (tag/folder), oczekiwany rezultat.

### Krok 3 — Napisz test casy jako STANDALONE (reguły treści)

Wykonalne przez osobę, która **pierwszy raz widzi aplikację**. Wszystko po **polsku**. Obowiązkowo:

- **Tytuł** — konkretny, zorientowany na rezultat: _"<Aktor> powinien <rezultat>, gdy <warunek>"_.
- **Precondition** — pełne, samowystarczalne: środowisko/URL; wymagane konto i rola + jak je zdobyć/dane logowania; konfiguracja krok po kroku (jak co ustawić); konkretne dane testowe.
- **Kroki** — każdy = **akcja** + **dokładne dane wejściowe** (realne wartości) + **oczekiwany rezultat kroku**. Ostatni krok = jasny **finalny output** (dokładny komunikat, stan, wartość, przekierowanie).
- Bez założeń „user wie jak". Trzeba coś skonfigurować → podaj instrukcję.
- Dane wej/wyj **wprost** (np. „NIP: `123-456-78-90`", „Oczekiwany komunikat: _Nieprawidłowy NIP_").

### Krok 4 — Zmapuj na strukturę QA Sphere

Pola test case'a (API):

- `type`: `"standalone"`
- `title`: 1–511 znaków
- `priority`: `"high"` | `"medium"` | `"low"`
- `precondition`: `{ "text": "<html>" }`
- `steps`: `{ "description": "<html>", "expected": "<html>" }`
- `tags`: tytuły tagów, np. `["happy-path"]`, `["negatywny"]`, `["walidacja"]`, + nazwa feature'a
- `customFields`: `{ "automation": { "value": "Planned" } }` (warunkowo — patrz niżej)

**HTML w treści**: akapity `<p>...</p>`, listy `<ol><li>...</li></ol>`. PL znaki UTF-8. Cudzysłowy w JSON escapuj.

**Foldery (wymagany `folderId`)**:

> ⚠️ **Nowe foldery ZAWSZE zagnieżdżaj w folderze-korzeniu projektu.** Każda tworzona ścieżka
> (`path`) MUSI zaczynać się od tytułu **folderu-korzenia projektu** — pozycji najwyższego poziomu
> reprezentującej cały projekt (zwykle nazwanej jak projekt/produkt, np. `Ustawożerca`). **Nigdy**
> nie twórz folderu na najwyższym poziomie **obok** korzenia projektu — to rozbija strukturę drzewa
> (QA Sphere nie ma DELETE w API, więc takiego błędu nie da się łatwo cofnąć).

1. Pobierz istniejącą strukturę i **dopasuj się do niej**:
   ```bash
   curl -s -H "Authorization: ApiKey $API_KEY" "$BASE_URL/project/$PROJECT/tcase/folders?limit=200"
   ```
2. **Ustal folder-korzeń projektu `ROOT`**: z powyższej listy weź pozycję najwyższego poziomu
   (rodzic = katalog główny drzewa, np. `parentId: 0`) o tytule odpowiadającym projektowi
   (porównaj z `title` z `GET /project`). Zapamiętaj jego **dokładny tytuł** — ze znakami
   diakrytycznymi tak, jak jest zapisany (np. `Ustawożerca` z `ż`) — aby dopasować istniejący
   folder zamiast tworzyć duplikat. Gdy korzenia jeszcze nie ma → będzie to pierwszy segment
   ścieżki (utworzy się automatycznie). Gdy jest kilku kandydatów najwyższego poziomu i wybór jest
   niejednoznaczny → **zapytaj usera**.
3. Rekomendacja ścieżki: `[ROOT, "<Moduł>", "<Feature>"]` (minimum `[ROOT, "<Moduł/Feature>"]`).
   Kategorię (happy/negatywny/walidacja) oznaczaj **tagiem**. Jeśli projekt ma własną konwencję
   podfolderów — trzymaj się jej, ale **zawsze pod `ROOT`**.
4. Utwórz/uzupełnij ścieżkę (idempotentnie), odbierz `folderId` (**ostatni** ID w zwróconej tablicy = liść):
   ```bash
   curl -s -X POST -H "Authorization: ApiKey $API_KEY" -H "Content-Type: application/json" \
     -d '{"folders":[{"path":["Ustawożerca","Ustawienia konta"],"comment":"<p>Testy modułu ustawień</p>"}]}' \
     "$BASE_URL/project/$PROJECT/tcase/folder/bulk"
   # → {"ids":[[1,123]]}  → folderId = 123 (ostatni w tablicy = liść; pierwszy to ROOT)
   ```
   > Pominięcie `ROOT` na początku `path` (np. `path:["Ustawienia konta"]`) utworzy folder na
   > najwyższym poziomie, **obok** projektu — **to błąd**. Zawsze prefiksuj ścieżkę tytułem `ROOT`.

**Pole `automation` (warunkowo)**: custom fieldy muszą istnieć w projekcie. W dtcode pole `automation` istnieje. Domyślnie dodawaj `"customFields":{"automation":{"value":"Planned"}}`; jeśli `POST` zwróci 400 przez nieznany/wyłączony custom field → **ponów bez `customFields`** i zaznacz to w raporcie.

### Krok 5 — Pokaż podgląd i POCZEKAJ na potwierdzenie

Zanim cokolwiek polecisz do API:

- wypisz **listę test case'ów** (tytuł + priorytet + kategoria/tag + folder) i **projekt** docelowy;
- podaj liczbę i które kategorie pokrycia objąłeś (i co świadomie pominąłeś);
- zapytaj o akceptację/poprawki. Twórz **dopiero po „ok"**.

### Krok 6 — Utwórz test casy w QA Sphere

```bash
curl -s -X POST -H "Authorization: ApiKey $API_KEY" -H "Content-Type: application/json" \
  -d '{
    "type":"standalone",
    "folderId":123,
    "title":"Użytkownik powinien zobaczyć błąd, gdy poda NIP o niepoprawnej długości",
    "priority":"high",
    "precondition":{"text":"<p>Środowisko: https://pre.tachoping.pl. Zalogowany jako właściciel floty (konto testowe owner@dtcode.pl). Otwarta strona rejestracji firmy.</p>"},
    "steps":[
      {"description":"<p>W polu NIP wpisz wartość <b>123-456-78</b> (9 znaków zamiast 10).</p>","expected":"<p>Pole NIP zostaje oznaczone jako błędne.</p>"},
      {"description":"<p>Kliknij przycisk <b>Zarejestruj</b>.</p>","expected":"<p>Formularz nie zostaje wysłany, pod polem NIP pojawia się komunikat: <i>Nieprawidłowy NIP</i>.</p>"}
    ],
    "tags":["walidacja","rejestracja"],
    "customFields":{"automation":{"value":"Planned"}}
  }' \
  "$BASE_URL/project/$PROJECT/tcase"
# → 201 {"id":"...","seq": N}
```

Zasady: twórz seryjnie z ~0,1 s przerwy; zapisuj `seq`/`id`; przy 4xx/5xx pokaż błąd i napraw payload (tytuł >511, brak `folderId`), przy błędzie `customFields` → ponów bez nich; przy 429 odczekaj 1 s i ponów.

### Krok 7 — Raport końcowy

Podsumuj: projekt (code + title), folder(y), liczbę utworzonych test case'ów z `seq` i tytułami, ostrzeżenia (np. wyłączone `automation`). Linki:

```
https://dtcode.eu1.qasphere.com/project/<PROJECT>/tcase/<seq>
```

---

## Szybka ściąga endpointów

| Cel                                  | Metoda + ścieżka                                                                    |
| ------------------------------------ | ----------------------------------------------------------------------------------- |
| Lista projektów                      | `GET /project`                                                                      |
| Lista folderów                       | `GET /project/{PROJECT}/tcase/folders?limit=200`                                    |
| Utwórz/uzupełnij foldery (ID liścia) | `POST /project/{PROJECT}/tcase/folder/bulk` body `{folders:[{path:[ROOT,...],comment}]}` (ścieżka zawsze od korzenia projektu) |
| Utwórz test case                     | `POST /project/{PROJECT}/tcase`                                                     |
| Lista test case'ów (duplikaty)       | `GET /project/{PROJECT}/tcase?search=...`                                           |
| Aktualizuj test case                 | `PATCH /project/{PROJECT}/tcase/{id_or_seq}`                                        |

Auth: `Authorization: ApiKey <API_KEY>`. Treści w HTML. `priority`: `high|medium|low`. `type` przy tworzeniu: `standalone`.

## Zasady jakości (twardo)

- Język **polski**, zawsze.
- Każdy test case **samowystarczalny** — wykona go ktoś, kto pierwszy raz widzi aplikację.
- Dane wej/wyj **konkretne**, nie placeholdery.
- **Nie twórz** niczego przed potwierdzeniem projektu (Krok 1) i akceptacją podglądu (Krok 5).
- Dąż do **pełnego pokrycia** — przejdź każdą kategorię z Kroku 2 i jawnie zaznacz pominięcia.
- Nowe foldery **zawsze** pod folderem-korzeniem projektu — `path` zaczyna się od tytułu `ROOT` (nigdy folder na najwyższym poziomie obok projektu).
