# teams-notatki

Skill dla Claude Code i Codex: notatki po polsku ze spotkań Microsoft Teams na
podstawie transkrypcji, pobieranej przez mostek `https://teamsnotes.tojest.dev`.

To repozytorium (`DTCodePL/Claude_Skills`) jest źródłem prawdy. Na urządzeniu
użytkownika instaluje się tylko **cienki loader**, który przy każdym
uruchomieniu ściąga aktualną treść z GitHuba — nie z lokalnej kopii.

> Ten plik opisuje **skill** (jak go zainstalować i jak działa CLI). Wdrożenie
> samego mostka (serwer, Docker, konto Microsoft Graph) opisuje
> `teams-notatki/bridge/README.md` — to praca innego wykonawcy, nie duplikuj
> jej tutaj.

## Instalacja loadera na nowym urządzeniu

Potrzebne są dwie komendy — jedna dla Claude Code, jedna dla Codex. Loader nie
wymaga żadnej konfiguracji: adres mostka i token są wbudowane w
`scripts/bridge.py` po stronie repozytorium.

### Claude Code

**bash / Git Bash / macOS / Linux:**

```bash
mkdir -p ~/.claude/skills/teams-notatki
curl -sL "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/Teams%20notatki%20loader.md" \
  -o ~/.claude/skills/teams-notatki/SKILL.md
```

**PowerShell:**

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills\teams-notatki" | Out-Null
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/Teams%20notatki%20loader.md" `
  -OutFile "$HOME\.claude\skills\teams-notatki\SKILL.md"
```

### Codex

**bash / Git Bash / macOS / Linux:**

```bash
mkdir -p ~/.codex/skills/teams-notatki
curl -sL "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/Teams%20notatki%20loader.md" \
  -o ~/.codex/skills/teams-notatki/SKILL.md
```

**PowerShell:**

```powershell
New-Item -ItemType Directory -Force "$HOME\.codex\skills\teams-notatki" | Out-Null
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/Teams%20notatki%20loader.md" `
  -OutFile "$HOME\.codex\skills\teams-notatki\SKILL.md"
```

Od tej chwili, gdy poprosisz agenta o notatkę ze spotkania Teams, loader sam
pobierze pełny skill (`SKILL.md`, `scripts/bridge.py`, `references/*`) z tego
repozytorium i wykona zadanie.

## Rotacja tokenu mostka

Token jest **stałą wbudowaną w dwóch miejscach** — muszą się zgadzać:

1. `bridge/.env` na serwerze mostka (`teamsnotes.tojest.dev`) — to zmienia
   wykonawca odpowiedzialny za mostek; nie jest to opisane tutaj, patrz
   `teams-notatki/bridge/README.md`.
2. `DEFAULT_TOKEN` w `teams-notatki/scripts/bridge.py` w tym repozytorium
   (linia ze stałą na początku pliku) — po zmianie na serwerze zaktualizuj tę
   stałą i wypchnij commit na `main`. Loader na urządzeniach użytkowników
   dostanie nowy token przy następnym uruchomieniu, bez żadnej akcji z ich
   strony (zmienne środowiskowe `TEAMS_NOTATKI_TOKEN` nie są wymagane — służą
   tylko do awaryjnego nadpisania bez czekania na nowy commit).

Adres mostka (`DEFAULT_URL`) rotuje się analogicznie, w tym samym pliku.

## Struktura katalogu

```
teams-notatki/
  SKILL.md                    ← pełny skill (źródło prawdy dla loadera)
  README.md                   ← ten plik
  scripts/
    bridge.py                 ← CLI (stdlib, Python >= 3.10)
  references/
    szablon-notatki.md        ← szablon notatki ze spotkania
    szablon-spisu-zmian.md    ← szablon spisu zmian (ADO / QA Sphere / Figma / dokumentacja) po notatce
    api.md                    ← kontrakt API mostka + przykłady curl (fallback)
  tests/
    test_bridge_cli.py        ← unittest, stub transportu, bez sieci
  bridge/                     ← serwis mostka (Microsoft Graph) — inny wykonawca
  docs/                       ← dokumentacja projektowa mostka — inny wykonawca
```

`bridge/` i `docs/` nie są częścią tego skilla — to osobny projekt (serwer),
prowadzony równolegle. Ten skill i CLI (`scripts/bridge.py`) są tylko jego
**klientem** przez HTTPS.

## CLI `scripts/bridge.py`

Uruchomienie testów (bez sieci, ze stubem transportu):

```bash
cd teams-notatki
PYTHONIOENCODING=utf-8 python -m unittest discover -s tests -v
```

Podgląd komend:

```bash
python scripts/bridge.py --help
python scripts/bridge.py resolve --help
```

Transkrypcję połączenia ad hoc (1:1 z czatu, link „Podsumowanie”) pobiera
`transcript --call`:

```bash
python scripts/bridge.py transcript --account <id> --call <callId> --out transkrypcja.md
```

Zmienne środowiskowe `TEAMS_NOTATKI_URL` / `TEAMS_NOTATKI_TOKEN` nadpisują
stałe wbudowane w skrypt — przydatne do testów na innym mostku, nic nie
wymaga ich ustawienia w normalnym użyciu.
