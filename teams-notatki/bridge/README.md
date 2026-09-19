# teams-transcript-bridge

Serwis HTTP (Python, stdlib `http.server`) pobierający transkrypcje spotkań Microsoft Teams
z Microsoft Graph, w imieniu skonfigurowanych kont (uwierzytelnianie aplikacyjne, certyfikat).
Zależności runtime: `msal` oraz `tzdata` (baza stref czasowych IANA dla `zoneinfo` — wymagana,
bo `python:3.12-slim` i Windows nie gwarantują jej obecności w systemie; bez niej
`ZoneInfo("Europe/Warsaw")` rzuca `ZoneInfoNotFoundError` przy starcie).

## Zmienne środowiskowe

| Zmienna | Znaczenie |
|---|---|
| `GRAPH_TENANT_ID` | GUID tenantu |
| `GRAPH_CLIENT_ID` | GUID aplikacji |
| `GRAPH_CERT_PATH` | ścieżka do PEM certyfikatu (domyślnie `/app/secrets/graph-cert.pem`) |
| `GRAPH_KEY_PATH` | ścieżka do PEM klucza prywatnego (domyślnie `/app/secrets/graph-key.pem`) |
| `BRIDGE_ACCOUNTS` | JSON: lista `{"label": "Damian", "upn": "Damian.Dziura@DTCode.pl", "id": "<guid>"}` — konta, w których kontekście szukamy spotkań (kolejność = kolejność prób) |
| `BRIDGE_TOKENS` | JSON: obiekt `{"<token-hex>": "damian", "<token-hex>": "piotr"}` — token → etykieta wołającego (do logów) |
| `BRIDGE_PORT` | port nasłuchu w kontenerze, domyślnie `8080` |
| `BRIDGE_TIMEZONE` | strefa dla dat lokalnych w `resolve`, domyślnie `Europe/Warsaw` |

Brak lub niepoprawna zmienna → proces kończy się kodem `1` i czytelnym komunikatem na `stderr`
(nigdy nie wypisuje wartości tokenów). Zobacz `.env.example`.

## Uruchomienie

Lokalnie (bez Dockera, bez `msal` — wystarcza do testów jednostkowych):

```bash
PYTHONIOENCODING=utf-8 python -m unittest discover -s tests -v
```

Walidacja pliku compose (bez budowania obrazu):

```bash
docker compose -f docker-compose.yml config --quiet
```

Realne uruchomienie wymaga `msal`, pliku `.env` (skopiowanego z `.env.example` i wypełnionego
prawdziwymi wartościami) oraz katalogu `secrets/` z `graph-cert.pem` i `graph-key.pem`:

```bash
docker compose up -d --build
```

## Wdrożenie (pre-prod / prod, mikr.us)

1. Spakuj katalog serwisu (bez `.env`, bez `secrets/` — są w `.gitignore` i nie powinny trafić
   do archiwum):
   ```bash
   tar -czf teams-transcript-bridge.tar.gz --exclude .env --exclude secrets .
   ```
2. Skopiuj archiwum na serwer (`pscp`, PuTTY):
   ```bash
   pscp teams-transcript-bridge.tar.gz user@host:/opt/teams-transcript-bridge.tar.gz
   ```
3. Na serwerze rozpakuj do `/opt/teams-transcript-bridge`, uzupełnij `.env` i `secrets/`
   (certyfikat + klucz), następnie:
   ```bash
   cd /opt/teams-transcript-bridge
   docker compose up -d --build
   ```
4. Sprawdź `GET /health` (bez auth) — powinno wrócić `{"status":"ok","service":"teams-transcript-bridge"}`.

## Rotacja certyfikatu / tokenów

- **Certyfikat Graph:** wygeneruj nowy PEM (klucz + cert), zarejestruj publiczny certyfikat
  w aplikacji Entra (`Certificates & secrets`), podmień pliki w `secrets/graph-cert.pem` i
  `secrets/graph-key.pem` na serwerze, `docker compose restart teams-transcript-bridge`.
  Nie ma przechowywanego thumbprintu do zaktualizowania — serwis liczy go z PEM-a przy każdym
  pobraniu tokenu (`graph.py::compute_thumbprint`).
- **Tokeny wołających (`BRIDGE_TOKENS`):** wygeneruj nowy losowy token (np. `openssl rand -hex 32`),
  dodaj/zamień wpis w `.env` (`BRIDGE_TOKENS`), `docker compose restart teams-transcript-bridge`.
  Stary token przestaje działać natychmiast po restarcie — nie ma okresu przejściowego z dwoma
  aktywnymi tokenami dla jednego wołającego, jeśli stary wpis zostanie usunięty.

## Uprawnienia Graph

Aplikacja Entra mostka wymaga (po dodaniu w Entra potrzebna zgoda administratora):

- `OnlineMeetings.Read.All` — odczyt spotkań (`onlineMeetings`)
- `OnlineMeetingTranscript.Read.All` — transkrypcje spotkań planowanych
- `Calendars.Read` — podgląd kalendarza (`calendarView`) w resolve po dacie
- **`CallTranscripts.Read.All`** (nowe, 2026-09-19) — transkrypcje połączeń
  ad hoc (`/users/{id}/adhocCalls/…`); bez niego resolve po linku
  „Podsumowanie” i `GET /calls/…/transcript` zwracają błąd dostępu

## Kontrakt API

Wspólne:
- Odpowiedzi JSON UTF-8, `Content-Type: application/json; charset=utf-8`. Błędy zawsze
  `{"error": {"code": "<snake_case>", "message": "<po polsku, dla człowieka>"}}`.
- Każdy endpoint poza `/health` wymaga nagłówka `Authorization: Bearer <token>`; porównanie
  przez `hmac.compare_digest` z kluczami `BRIDGE_TOKENS`; brak/zły → `401 unauthorized`.
  Nieznana ścieżka → `404 not_found`. Zła metoda → `405 method_not_allowed`. Ciało > 64 KiB →
  `413 payload_too_large`. Nieparsowalny JSON → `400 bad_request`.
- Kody błędów Graph mapowane: 403 z `innerError.code == "GraphAccessToTranscriptsDisabled"` →
  `502 transcript_access_disabled` ("Administrator wyłączył dostęp API do transkrypcji w Teams
  Admin Center"); 403/401 inne → `502 graph_forbidden`; 404 → `404 ...` (zależnie od miejsca);
  timeout/5xx/sieć → `502 graph_error` z `message` zawierającym kod Graph i jego komunikat,
  **nigdy** token ani nagłówki. Timeout na Graph: 30 s.

### `GET /health` — bez zmian, bez auth.

### `POST /meetings/resolve`

Ciało (JSON), tryby:

1. **Po linku / identyfikatorze** — pole `link` (string). Akceptowane formy:
   - `https://teams.microsoft.com/meet/391328174033204?p=GBQvD2H3Gm5XAdUnBp` →
     `joinMeetingId = "391328174033204"`
   - `https://teams.microsoft.com/l/meetup-join/19%3ameeting_...%40thread.v2/0?context=%7b...%7d`
     (zakodowany albo już zdekodowany, może być z `&amp;`) → `joinWebUrl` znormalizowany do
     postaci zakodowanej, jaką zwraca Graph.
   - same cyfry, także ze spacjami: `"391 328 174 033 204"` → `joinMeetingId`.
   - inna wartość → `400 invalid_link`.

   Algorytm: dla każdego konta z `BRIDGE_ACCOUNTS` po kolei
   `GET /users/{id}/onlineMeetings?$filter=...`; pierwsze konto z niepustym `value` wygrywa
   (tego konta `id` idzie dalej w ścieżkach). Brak trafień we wszystkich → `404 meeting_not_found`
   z komunikatem, że spotkanie nie jest widoczne z żadnego ze skonfigurowanych kont (np. obcy
   tenant) i że można podać plik `.vtt` ręcznie.

2. **Po dacie / tytule** — pola: `date` (`YYYY-MM-DD`, lokalna w `BRIDGE_TIMEZONE`), opcjonalnie
   `time` (`HH:MM` lokalne; okno ±90 min od `start`), opcjonalnie `title` (dopasowanie: bez
   wielkości liter, bez polskich znaków po obu stronach, `title` jako podciąg `subject`),
   opcjonalnie `window_days` (int, domyślnie 0 = tylko podany dzień; N = od `date - N` do
   `date + N` dni). Gdy nie ma `date`, ale jest `title` → ostatnie 30 dni do teraz. Gdy nie ma
   ani `link`, ani `date`, ani `title` → `400 bad_request`.

   Algorytm: dla każdego konta `GET /users/{id}/calendarView?startDateTime=...&endDateTime=...
   &$top=50&$orderby=start/dateTime desc&$select=subject,start,end,organizer,isOnlineMeeting,
   onlineMeeting,body` (z obsługą `@odata.nextLink` do 200 zdarzeń). Odfiltrowanie po
   tytule/czasie. Dla każdego pasującego zdarzenia: identyfikator z `onlineMeeting.joinUrl` albo
   z `body.content`. Zdarzenia bez linku Teams pomijane (liczone w `skipped_without_teams_link`).
   Deduplikacja między kontami po `joinMeetingId`/`joinWebUrl`. Maks. 10 kandydatów, sortowane
   `start` malejąco.

Odpowiedź `200`:

```json
{
  "candidates": [
    {
      "meetingId": "MSoxNmQ4...",
      "account": {"label": "Damian", "upn": "Damian.Dziura@DTCode.pl", "id": "16d86420-..."},
      "subject": "test",
      "start": "2026-09-18T10:00:00Z",
      "end": "2026-09-18T10:30:00Z",
      "organizer": {"name": "Damian Dziura", "email": "Damian.Dziura@DTCode.pl"},
      "joinMeetingId": "391328174033204",
      "joinWebUrl": "https://teams.microsoft.com/l/meetup-join/...",
      "transcripts": [{"id": "ktViz...", "createdDateTime": "2026-09-18T09:36:28Z", "endDateTime": "2026-09-18T09:37:00Z"}]
    }
  ],
  "skipped_without_teams_link": 0
}
```

`organizer` z kalendarza gdy dostępne; w trybie po linku — `name: null`, `email: null` i
dodatkowo `organizerId` (GUID z `participants.organizer.identity.user.id`); jeśli GUID pasuje do
któregoś z `BRIDGE_ACCOUNTS`, uzupełniony `name`=`label`, `email`=`upn`. Daty w UTC ISO-8601 z
`Z`, sekundy bez ułamków. `transcripts` puste = spotkanie znalezione, transkrypcji (jeszcze) nie
ma — to NIE jest błąd.

### `GET /meetings/{accountId}/{meetingId}/transcript[?transcriptId=<id>][&format=vtt]`

- `accountId` = GUID z `candidates[].account.id`; musi być jednym z `BRIDGE_ACCOUNTS` (inaczej
  `400 unknown_account`). `meetingId` = `candidates[].meetingId` (Graph id; może zawierać `*`/`=`).
- Bez `transcriptId`: pobiera listę, bierze ostatnią po `createdDateTime`; lista pusta →
  `404 transcript_not_found` ("Spotkanie istnieje, ale nie ma transkrypcji — Teams udostępnia ją
  kilka minut po zakończeniu spotkania i tylko gdy transkrypcja była włączona").
- `format=vtt` → odpowiedź `200` `text/vtt; charset=utf-8` z surowym VTT.
- Domyślnie JSON:

```json
{
  "meeting": {"meetingId": "...", "subject": "test", "start": "...Z", "end": "...Z", "organizerId": "16d8...", "joinMeetingId": "391328174033204"},
  "transcript": {
    "id": "ktViz...", "createdDateTime": "...Z", "endDateTime": "...Z", "language": "pl-pl",
    "speakers": ["Damian Dziura"],
    "segments": [{"start": "00:00:07.153", "end": "00:00:08.593", "speaker": "Damian Dziura", "text": "To jest testowe spotkanie."}],
    "vtt": "WEBVTT\n\n..."
  }
}
```

Dane `meeting` pochodzą z `GET /users/{accountId}/onlineMeetings/{meetingId}` (404 →
`404 meeting_not_found`).

## Logowanie

Do stdout, jedna linia na żądanie, np.:

```
2026-09-18T10:00:00Z INFO POST /meetings/resolve caller=damian status=200 ms=812 mode=link accounts_tried=1
```

Nigdy nie loguje: treści transkrypcji, tokenów, nagłówka `Authorization`, ciała żądania.

## Struktura kodu

| Plik | Rola |
|---|---|
| `app.py` | serwer HTTP: routing, auth, JSON, logowanie |
| `config.py` | odczyt i walidacja zmiennych środowiskowych → `Settings` |
| `graph.py` | klient Graph: token (msal, cert), GET z obsługą błędów, thumbprint z PEM |
| `meetings.py` | parsowanie linku, resolve po linku/dacie/tytule, pobranie transkrypcji |
| `vtt.py` | parser WebVTT → segmenty |
