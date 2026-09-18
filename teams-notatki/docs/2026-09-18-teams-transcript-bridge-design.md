# Teams Transcript Bridge – design

## Goal

Provide a shared, secure service for Damian and Piotr that retrieves a Teams meeting transcript by meeting link or by calendar time and title, then makes the text available to a Codex skill for note generation.

## Scope of the first deploy

Deploy an isolated health-checked bridge on the Mikrus VPS so the provider can attach a public HTTPS subdomain to port 40002. It exposes no Microsoft credential, transcript, or note endpoint until the Microsoft access policies and service authentication are configured.

## Architecture

The bridge runs as its own Docker container on port 40002, separate from existing VPS containers. The Mikrus HTTP/HTTPS proxy will terminate public TLS and proxy to the bridge only after a subdomain is created. The bridge listens only for `GET /health` during this deploy and returns no sensitive data.

Later phases add a protected MCP-facing API, store the Microsoft client credential only on the VPS, query Graph, and deliver a transcript to the Codex skill without retaining raw transcript files. The transcript permission will be restricted to the two approved users. Microsoft documents that lookup by meeting link with application permissions does not support the same access-policy restriction, so automatic link lookup must not be enabled until its metadata-scope trade-off is explicitly approved.

## Security boundaries

- Existing VPS applications, containers, ports, and databases are out of scope.
- The health endpoint contains no identifiers or secrets.
- No Entra client secret is created or stored in this phase.
- Transcript retrieval will be limited to Damian.Dziura@DTCode.pl and Piotr.Tunski@DTCode.pl before a credential is enabled.
- The final public API must require per-user authentication; a shared raw Graph credential must never be installed on client devices.

## Acceptance criteria for this deploy

1. `GET /health` returns HTTP 200 and JSON with `status: "ok"`.
2. Docker publishes port 40002 on the VPS.
3. The Mikrus subdomain validation can reach the endpoint through IPv6.
4. Existing Docker containers stay running unchanged.

## Errata (2026-09-18, po weryfikacji na żywym tenantcie)

- Zdanie o tym, że lookup po linku spotkania „nie wspiera application access policy”, jest **błędne** — gwiazdka w dokumentacji Graph dotyczy wyłącznie `videoTeleconferenceId`. `/users/{guid}/onlineMeetings?$filter=joinMeetingIdSettings/joinMeetingId eq '…'` działa z uprawnieniami aplikacyjnymi i przyjmuje GUID organizatora **lub** zaproszonego uczestnika. Lookup po linku jest włączony.
- Polityka `Grant-CsApplicationAccessPolicy` nadana globalnie (tenant = dwie osoby); polityka Exchange na kalendarze pominięta z tej samej przyczyny.
- Uwierzytelnianie aplikacji certyfikatem (klucz prywatny tylko na VPS), nie kluczem tajnym.
- Decyzja właściciela: token mostka jest wbudowany w `scripts/bridge.py` (zero konfiguracji na urządzeniu) — patrz `teams-notatki/README.md`, rotacja.
