# fala-odbior

Odbiór fali briefów jednym poleceniem: zakres względem bazy zapisanej przed
falą, sprawdzenia, krótki werdykt (≤ 40 linii) i pełne logi w katalogu.

Tylko biblioteka standardowa Pythona 3.12+. Bez instalacji pakietów.

## Wywołania

Baza przed falą (jedna linia na stdout):

```
python fala-odbior.py --repo <ścieżka> --zapisz-baze <plik.json>
```

Odbiór po fali:

```
python fala-odbior.py --repo <ścieżka> --baza <plik.json> --pakiet <pakiet.json> [--brief <id>] [--pelny] [--katalog-logow <katalog>]
```

- `--brief <id>` — odbiór tylko plików jednego briefu (bez przebiegów `--pelny`).
- `--pelny` — pełne przebiegi: FE `npm run lint`, `npm run format:check`,
  `npm test -- --watch=false`, `npm run build`; BE `dotnet build`,
  `dotnet test`. Bez `--pelny` BE raportuje tylko zakres i statystykę.
  `--pelny` sprawdza całe drzewo, więc cudza niezacommitowana praca może dać
  błąd niezwiązany z falą — werdykt trzeba wtedy rozdzielić po plikach z logu.
- `--katalog-logow` — domyślnie `<temp>/fala-odbior/<RRRRMMDD-HHMMSS>`.
- `--limit-czasu <minuty>` — limit czasu na każde polecenie (domyślnie 60);
  po przekroczeniu drzewo procesów jest zabijane, a sprawdzenie kończy się
  kodem 124.

## Format pakietu

```json
{
  "stos": "fe",
  "briefy": [
    { "id": "B1", "autor": "ktoś", "pliki": ["src/app/**", "src/assets/i18n/*.json"] }
  ]
}
```

- `stos`: `fe` albo `be`. Gdy brak — wykrywanie: `package.json`
  z `@angular/core` daje `fe`, plik `*.slnx`/`*.sln` w korzeniu daje `be`.
- Globy: `**` przechodzi przez `/`, `*` nie przechodzi.
- Plik fali bez briefu to BŁĄD; plik w kilku briefach to OSTRZEŻENIE
  („wspólny”); brief bez plików to OSTRZEŻENIE.
- Przeniesienie pliku przez brief wymaga podania w pakiecie obu ścieżek;
  usunięta ścieżka spoza globów to celowo BŁĄD „plik spoza briefów”.

## Format bazy

JSON: `repo`, `head` (SHA), `czas` (ISO 8601 UTC), `pliki`
(ścieżka względna → identyfikator bloba albo `null` dla usuniętego).
Plik należy do fali, gdy identyfikator treści w bazie różni się od bieżącego.

## Logi

- `<katalog-logow>/00-werdykt-pelny.log` — pełna lista: briefy, pliki, błędy,
  ostrzeżenia, „zniknął z listy zmian bez zmiany treści”.
- `<katalog-logow>/<nr>-<nazwa>.log` — pełne stdout/stderr każdego sprawdzenia.
- `*` przy pliku/briefie: plik był zmieniony już w bazie — statystyka
  obejmuje zmiany sprzed fali.

## Kody wyjścia

- `0` — OK lub ostrzeżenia.
- `1` — błędy.
- `2` — błąd użycia albo brak repo, bazy lub pakietu.

## Testy

```
python -m unittest discover -s narzedzia/fala-odbior -p "test_*.py"
```

z katalogu repozytorium. Tymczasowe repozytoria powstają
w `narzedzia/fala-odbior/.tmp-test/` i są sprzątane po każdym teście.
