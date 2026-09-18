# Kontrakt API mostka `teams-transcript-bridge`

Wiążący kontrakt serwisu `https://teamsnotes.tojest.dev` (adres i token domyślne
są wbudowane w `scripts/bridge.py` — nie trzeba niczego konfigurować). Ten plik
jest referencją dla `bridge.py` i **fallbackiem `curl`**, gdy na urządzeniu nie
jest dostępny Python.

Wszystkie odpowiedzi to JSON UTF-8. Błędy mają zawsze kształt:

```json
{"error": {"code": "nazwa_kodu", "message": "komunikat po polsku"}}
```

Uwierzytelnianie: nagłówek `Authorization: Bearer <token>` — wymagany na
wszystkich endpointach **poza** `/health`.

Token domyślny wbudowany w `scripts/bridge.py` (`DEFAULT_TOKEN`):

```
362a87cf8e5d6560e80f074082667f9569cf0073f4768c43
```

Adres domyślny (`DEFAULT_URL`):

```
https://teamsnotes.tojest.dev
```

Oba można nadpisać zmiennymi środowiskowymi `TEAMS_NOTATKI_URL` /
`TEAMS_NOTATKI_TOKEN` — ale nic tego nie wymaga.

---

## `GET /health`

Bez nagłówka `Authorization`.

**Odpowiedź `200`:**

```json
{"status": "ok", "service": "teams-transcript-bridge"}
```

**curl:**

```bash
curl -sS "https://teamsnotes.tojest.dev/health"
```

---

## `POST /meetings/resolve`

Szuka spotkania — po linku Teams **albo** po dacie/godzinie/tytule.

### Tryb: po linku

```json
{"link": "https://teams.microsoft.com/meet/391328174033204?p=..."}
```

Akceptowane formy `link`:

- `https://teams.microsoft.com/meet/391328174033204?p=...`
- `https://teams.microsoft.com/l/meetup-join/...`
- gołe cyfry ID spotkania, mogą być ze spacjami (np. `391 328 174 033 204`)

### Tryb: po dacie/tytule

```json
{
  "date": "2026-09-18",
  "time": "10:00",
  "title": "status projektu",
  "window_days": 0
}
```

- `date` — opcjonalne, `YYYY-MM-DD`.
- `time` — opcjonalne, `HH:MM`, czas lokalny PL, okno wyszukiwania ±90 min.
- `title` — opcjonalne, podciąg tytułu, bez rozróżniania wielkości liter i
  polskich znaków.
- `window_days` — opcjonalne, `N` = szukaj w oknie ±N dni od `date`.
- Jeśli podano `title` bez `date` → mostek szuka w ostatnich 30 dniach.

### Odpowiedź `200`

```json
{
  "candidates": [
    {
      "meetingId": "MSoxNjZm...",
      "account": {"label": "Damian", "upn": "damian@dtcode.pl", "id": "16d8f2b0-..."},
      "subject": "Status projektu",
      "start": "2026-09-18T10:00:00Z",
      "end": "2026-09-18T10:30:00Z",
      "organizer": {"name": "Damian Dziura", "email": "damian@dtcode.pl"},
      "joinMeetingId": "391 328 174 033 204",
      "joinWebUrl": "https://teams.microsoft.com/l/meetup-join/...",
      "transcripts": [
        {"id": "...", "createdDateTime": "2026-09-18T10:31:12Z", "endDateTime": "2026-09-18T10:31:40Z"}
      ]
    }
  ],
  "skipped_without_teams_link": 0
}
```

- Maksymalnie 10 kandydatów, sortowane po `start` malejąco (najnowsze pierwsze).
- `transcripts: []` — spotkanie istnieje, transkrypcji (jeszcze) nie ma.

### Błędy

| HTTP | `code`                       | Znaczenie                                          |
| ---- | ---------------------------- | --------------------------------------------------- |
| 400  | `invalid_link`                | Link nie jest rozpoznawalnym linkiem Teams          |
| 400  | `bad_request`                 | Ciało żądania niepoprawne                           |
| 401  | `unauthorized`                | Token nieaktualny/niepoprawny                       |
| 404  | `meeting_not_found`           | Nie znaleziono spotkania                            |
| 502  | `transcript_access_disabled`  | Dostęp do transkrypcji wyłączony w Teams Admin Center |
| 502  | `graph_forbidden`             | Microsoft Graph odmówił dostępu                    |
| 502  | `graph_error`                 | Inny błąd Microsoft Graph                           |

**curl (po linku):**

```bash
curl -sS -X POST "https://teamsnotes.tojest.dev/meetings/resolve" \
  -H "Authorization: Bearer 362a87cf8e5d6560e80f074082667f9569cf0073f4768c43" \
  -H "Content-Type: application/json" \
  -d '{"link": "https://teams.microsoft.com/meet/391328174033204?p=..."}'
```

**curl (po dacie/tytule):**

```bash
curl -sS -X POST "https://teamsnotes.tojest.dev/meetings/resolve" \
  -H "Authorization: Bearer 362a87cf8e5d6560e80f074082667f9569cf0073f4768c43" \
  -H "Content-Type: application/json" \
  -d '{"date": "2026-09-18", "time": "10:00", "title": "status projektu"}'
```

---

## `GET /meetings/{account.id}/{meetingId}/transcript`

Query opcjonalny: `?transcriptId=…` (konkretna transkrypcja) i `&format=vtt`
(zamiast domyślnego JSON, zwraca `text/vtt` z surową treścią VTT).

`meetingId` może zawierać znaki `*` i `=` — w URL-u koduj je
(`urllib.parse.quote(meeting_id, safe="")` w Pythonie; w `curl`/bash
odpowiada temu `--data-urlencode` albo ręczne `%2A` / `%3D`).

### Odpowiedź `200` (domyślnie, JSON)

```json
{
  "meeting": {
    "meetingId": "MSoxNjZm...",
    "subject": "Status projektu",
    "start": "2026-09-18T10:00:00Z",
    "end": "2026-09-18T10:30:00Z",
    "organizerId": "16d8f2b0-...",
    "joinMeetingId": "391 328 174 033 204"
  },
  "transcript": {
    "id": "...",
    "createdDateTime": "2026-09-18T10:31:12Z",
    "endDateTime": "2026-09-18T10:31:40Z",
    "language": "pl-PL",
    "speakers": ["Damian Dziura", "Piotr Tuński"],
    "segments": [
      {"start": "00:00:07.153", "end": "00:00:08.593", "speaker": "Damian Dziura", "text": "..."}
    ],
    "vtt": "WEBVTT\n\n..."
  }
}
```

**Uwaga:** obiekt `meeting` tu ma tylko `organizerId` (identyfikator), **nie**
imię i nazwisko organizatora — to jest tylko w `organizer.name` z odpowiedzi
`/meetings/resolve`. Jeśli potrzebujesz imienia i nazwiska w finalnej notatce,
weź je z wcześniejszego wyniku `resolve`, nie z `transcript`.

### Odpowiedź z `format=vtt`

`Content-Type: text/vtt`, ciało to surowy plik VTT (pole `vtt` z wersji JSON).

### Błędy

| HTTP | `code`                | Znaczenie                                          |
| ---- | ---------------------- | --------------------------------------------------- |
| 404  | `transcript_not_found`  | Spotkanie istnieje, transkrypcji (jeszcze) brak     |
| 404  | `meeting_not_found`     | Nie znaleziono spotkania                            |
| 400  | `unknown_account`       | `account.id` nie odpowiada żadnemu skonfigurowanemu kontu |
| 401  | `unauthorized`          | Token nieaktualny/niepoprawny                       |
| 502  | `transcript_access_disabled` / `graph_forbidden` / `graph_error` | jak wyżej |

**curl (JSON):**

```bash
curl -sS "https://teamsnotes.tojest.dev/meetings/16d8f2b0-.../MSoxNjZm.../transcript" \
  -H "Authorization: Bearer 362a87cf8e5d6560e80f074082667f9569cf0073f4768c43"
```

**curl (VTT):**

```bash
curl -sS "https://teamsnotes.tojest.dev/meetings/16d8f2b0-.../MSoxNjZm.../transcript?format=vtt" \
  -H "Authorization: Bearer 362a87cf8e5d6560e80f074082667f9569cf0073f4768c43"
```

---

## Kody wyjścia `scripts/bridge.py` (odzwierciedlają powyższe błędy)

| Kod wyjścia | Kiedy                                                        |
| ----------- | ------------------------------------------------------------- |
| `0`         | sukces                                                        |
| `1`         | błąd użycia CLI (złe/brakujące argumenty)                     |
| `3`         | `meeting_not_found` / `transcript_not_found`                  |
| `4`         | `unauthorized`                                                |
| `5`         | inne błędy mostka (400/502/…) albo brak połączenia z mostkiem |
