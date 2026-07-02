# Project Standards — Frontend (Angular 22) + Backend (.NET CQRS)

This repository is opened as a **single VS Code workspace** containing two separate codebases.
Apply the rules for the stack you are currently editing — **never apply one stack's rules to the other.**

| You are editing…                            | Apply the section |
| ------------------------------------------- | ----------------- |
| `.ts` / `.html` / `.scss` — the Angular app | **FRONTEND**      |
| `.cs` / `.sql` — the ASP.NET Core app       | **BACKEND**       |

Watch for language-specific rules that **conflict by design** and must stay scoped:

- **`async`/`await`:** Backend (C#) requires it everywhere; Frontend (Angular) forbids it in services/components (prefer `Observable`).
- **`var`:** Backend (C#) bans `var` (explicit types); Frontend (TypeScript) prefers type inference when obvious.
- **Naming/structure:** Frontend uses suffixless files + feature folders; Backend uses CQRS naming + layered folders.

## Planning Mode (both stacks)

- When writing a plan (plan mode / EnterPlanMode), always write it in Polish.

## Git Workflow (both stacks)

- Pushing **directly to `main` without a PR** is allowed.
- Every push to `main` must carry the related **Azure DevOps PBI number** in **both** the branch name and the commit message (e.g. branch `feature/978-projekty-fe-be`, commit `feat: ... (PBI #978)`).
- If you don't know which PBI a change belongs to, ask before pushing — never push to `main` without a PBI number.

---

# FRONTEND (Angular 22)

You are an expert in TypeScript, Angular 22, SSR, and scalable web application development. You write functional, maintainable, performant, and accessible code following the canonical standard below. This standard is **mandatory** — prefer the documented successor over anything older, and never silently deviate.

## FE · Core Architecture

- **Angular 22**, standalone, **signal-first**, **zoneless**, **OnPush**, **SSR + SEO-first** (every route is server-rendered or prerendered; full HTML for crawlers), **UI = PrimeNG** (styled mode, design tokens).
- TypeScript 6 (`strict`). Node 26. Builder `@angular/build:application`.

## FE · TypeScript Best Practices

- Use strict type checking; prefer type inference when the type is obvious.
- Avoid `any`; use `unknown` when the type is uncertain.
- Always declare explicit access modifiers (`public` / `protected` / `private`) on **every** class member — fields, methods, constructor parameters. Never rely on the implicit `public`.
- One public declaration per file (class / interface / enum / type / function). Never put multiple things in one file. The file name matches that one declaration.

## FE · Observables vs Promises

- **Always prefer `Observable` over `Promise`.** Never use `async`/`await` or `Promise` in Angular services or components — use RxJS.
- Convert Promise-based APIs to Observable via `from()`. Use `forkJoin()` over `Promise.all()`, `switchMap()` over `.then()`, `finalize()` over `.finally()`.
- Only acceptable Promise uses: `bootstrapApplication().catch()` in `main.ts`; `import(...).then(m => m.X)` in lazy routes; SSR handler code in `server.ts`; `firstValueFrom()` / `lastValueFrom()` when a framework API needs a single scalar (e.g. `provideAppInitializer`).

## FE · Angular Best Practices

- Always standalone components. **Must NOT set `standalone: true`** (default in v20+).
- Use signals for state. Implement lazy loading for feature routes.
- Put host bindings in the `host` object of the decorator. **Do NOT use `@HostBinding` / `@HostListener`.**
- Use `inject()` instead of constructor injection.
- Use `NgOptimizedImage` for all static images. It does **not** work for inline base64 images.

## FE · Components

- Keep components small and single-responsibility. Prefer a **smart parent composing presentational sub-components**; **never build god components**. Split a growing component instead of letting it bloat.
- Use `input()` / `output()` / `model()` functions, not decorators. Use `computed()` for derived state.
- Set `changeDetection: ChangeDetectionStrategy.OnPush` explicitly.
- Presentational sub-components take only `input`/`output`, inject no services; keep them next to the parent (`components/<parent>/`, `components/steps/`).
- Prefer inline templates for small components. When external, use paths relative to the component TS file.
- **Do NOT use `ngClass`** → use `[class.x]` bindings. **Do NOT use `ngStyle`** → use `[style.x]` bindings.
- Components must be **SSR-safe** (no DOM access at construction/init).

## FE · Templates

- Use native control flow `@if` / `@for (… ; track …)` / `@switch`. Never `*ngIf` / `*ngFor` / `*ngSwitch`.
- Use the **async pipe** for observables.
- Do **not** assume globals like `new Date()` are available (SSR) — the component supplies the value.
- Lazy-render with `@defer` (use `@defer (hydrate on …)` under SSR).

## FE · Forms

- **Signal Forms** (`@angular/forms/signals`) are the standard. Model = `signal<T>(...)`; `form(model, schemaFn)`; bind `[formField]="form.field"`; read field state via `form.field().valid()/.touched()/.errors()`; submit via `submit(form, async () => …)`.
- Schemas live one-per-file in `schemas/`; compose with `schema<T>()` + `apply`/`applyWhen`/`applyEach`. A validator returns `undefined` (not `null`) when valid.
- Do not mix `@angular/forms` with `@angular/forms/signals`.
- Public/auth forms are protected by Cloudflare Turnstile (server-verified token; widget loaded SSR-safe).

## FE · State Management

- Use signals for state and `computed()` for derived state; keep transformations pure.
- Change signals with `set` / `update` — **never `mutate`**.
- Remote data via `resource` / `httpResource` / `rxResource`. RxJS only for event streams and interop (`toSignal` / `toObservable`).
- No NgRx (optional `@ngrx/signals` SignalStore for large shared state).
- Browser storage via **ngx-webstorage** (`LocalStorageService` / `SessionStorageService`), always behind `isPlatformBrowser` (no storage on the SSR server).

## FE · Services & HTTP

- Single-responsibility services with **`@Service()`** (singleton root, no `providedIn`). Inject with `inject(HttpClient)`; `apiUrl = environment.apiUrl + 'x/'`.
- Reads → `httpResource(...)` / `rxResource({...})` (use SSR transfer cache to avoid double fetch). Commands/streams → `HttpClient` + `Observable`, map `response → model`. Fetch is the default transport.

## FE · Rendering (SSR) & Platform Safety

- Hybrid rendering. Pair `app.routes.ts` with `app.routes.server.ts` (`ServerRoute[]` + `RenderMode`), wired via `provideServerRendering(withRoutes(serverRoutes))`.
- Render-mode strategy: `Prerender` (SSG) for marketing/static content (`getPrerenderParams` for dynamic params); `Server` (SSR) for per-request/per-user and indexable data; `Client` (CSR) only for highly interactive areas (+ `withAppShell`); `**` → `Server`.
- `provideClientHydration()` (incremental hydration on by default; event replay enabled). Configure `withHttpTransferCacheOptions(...)`.
- **Never touch `window` / `document` / `localStorage` directly.** Gate with `isPlatformBrowser(inject(PLATFORM_ID))`; run DOM/overlay code (PrimeNG overlays, Turnstile, editors) in `afterNextRender` / `afterRender`; access the document via `inject(DOCUMENT)`.

## FE · SEO

- Per-route `Title` + `Meta`, canonical link, Open Graph / Twitter Cards, JSON-LD structured data — centralized in a `SeoService` (`core/seo/`).
- `NgOptimizedImage`, `sitemap.xml`, `robots.txt`; correct statuses/redirects at the `ServerRoute` level.

## FE · Accessibility

- Semantic HTML first. Use **`@angular/aria`** for complex patterns instead of hand-rolled ARIA. Manage focus / focus-trap in overlays; visible focus ring; keyboard navigation.
- Meet **WCAG AA** (contrast enforced at the semantic-token level, light + dark). It **MUST pass AXE** (automated audit in tests/CI).

## FE · Animations

- The UI is **always animated** (entrances, hover/press, state transitions), but animations are authored **only in SCSS** (`@keyframes` / `transition` + motion tokens for duration/easing) — **never in TypeScript**.
- **Never import `@angular/animations`** and never use the `animations:` metadata key. Use CSS / `animate.enter` / `animate.leave` when a lifecycle hook is required.
- All motion is gated by `@media (prefers-reduced-motion: reduce)`; no infinite loops (justified exceptions only).

## FE · Responsive (mobile-first)

- **All responsiveness MUST be built on the Bootstrap grid** (`.container`/`.container-fluid`, `.row`, `.col-*`, `.col-{sm,md,lg,xl,xxl}-*`, `.g-*` gutters, offsets). Compose responsive layouts with grid rows/columns and breakpoint column classes — do **not** hand-roll bespoke CSS Grid/media-query column systems for page/section layout.
- **Only the Bootstrap _grid_ is allowed from Bootstrap — nothing else.** It is vendored as a single local file `src/vendor/bootstrap-grid.min.css` (grid + flex/spacing utilities only) and wired via `angular.json` `styles`. **Never** install the `bootstrap` npm package, never import Bootstrap components/reboot/JS, and never add other Bootstrap CSS. Keep breakpoints aligned with Bootstrap (`sm 576 / md 768 / lg 992 / xl 1200 / xxl 1400`); component SCSS breakpoint variables must match these.
- For data-heavy views use the canonical **desktop table ↔ mobile cards** pattern, fed by **one** signal/computed stream (no duplicated logic; switch driven by the grid/container queries). Touch-friendly targets.

## FE · Deprecated APIs — NEVER USE

- Never use any symbol marked `@deprecated` — `@typescript-eslint/no-deprecated` flags this as an error; build deprecation warnings are treated as errors.
- Never import from `@angular/animations` — use CSS animations (see FE · Animations).
- Never use `@HostBinding` / `@HostListener`, `ngClass` / `ngStyle`, `*ngIf` / `*ngFor` / `*ngSwitch`, or signal `mutate`.
- **One documented exception:** `provideAnimations()` is kept solely because PrimeNG (Dialog/Overlay/Tooltip) still requires it. It is tracked technical debt — remove it once PrimeNG migrates to `animate.enter` / `animate.leave`. This does **not** permit `@angular/animations` in our own code.

## FE · Styling & Colors

- Style PrimeNG **only through theming** (preset + design tokens). **Never override PrimeNG with your own CSS** — no `::ng-deep`, no targeting `.p-*` classes.
- **Never hardcode color values** (hex, rgb, rgba, hsl, named colors) in SCSS or templates. Colors come **only** from variables: `var(--p-*)` or `dt('…')`.
- Maintain one color base as the source of truth: `theme/palette.ts` (primitives) + `theme/app.preset.ts` (`definePreset(...)` mapping primitive → semantic → component), wired in `providePrimeNG`. Dark mode via `darkModeSelector` + `colorScheme`, not separate CSS.
- If no existing variable/token fits, **STOP and ask** before adding a new token. Never introduce a raw color unilaterally.

## FE · Notifications (Toasts & Dialogs)

- Route everything through a single `NotificationService` facade (`success/error/warn/info/confirm`). Components never call the UI library directly.
- Toasts via **ngx-toastr** (`ToastrService`); dialogs/confirmations via **PrimeNG** (`DialogService` / `ConfirmationService`).
- **Never** use browser `alert()` / `confirm()` or custom toasts. Pass a **translated string** to toasts, not a key.

## FE · Internationalisation (i18n)

- Every user-facing string MUST go through `ngx-translate` — visible text, button labels, placeholders, tooltips, `aria-label`, `aria-describedby`, toast text. Never hardcode strings.
  - Template: `{{ 'KEY' | translate }}`, `[attr.aria-label]="'KEY' | translate"`.
  - Component: `translate.instant('KEY')` or `translate.stream('KEY')`.
- Keys are written in **English**, dot-notation scoped to the feature: `FEATURE.COMPONENT.KEY`.
- **The project locale set is `pl` (default) + `en` — ALWAYS create/update both.** Every new key MUST be added to **both** `src/assets/i18n/pl.json` and `src/assets/i18n/en.json` (and to any further locale added later) before committing; never ship a key in only one language. New locales must also be wired into the SSR loader (`translate-server-loader.ts`) and `addLangs`. PrimeNG strings via `PrimeNG.setTranslation` / PrimeLocale.

## FE · Errors & Monitoring

- Global `ErrorHandler` (`{ provide: ErrorHandler, useClass: AppErrorHandler }`) reports runtime errors and surfaces a message via `NotificationService`.
- HTTP error interceptor maps statuses to user messages (`401` → refresh/logout); no raw errors leak to the UI.
- Monitoring SDK (Sentry-class) initialized **separately for client and SSR server**; source maps in build; no PII. Log SSR via the server logger, not `console`.
- Wrap fragile template sections in `@boundary` so a section error does not crash the page.

## FE · Naming & Files

- **Suffixless** files and classes: `user-profile.ts` → `UserProfile`. Exceptions that keep a suffix: **Pipe**, **NgModule**, **functional cross-cutting artifacts** (dot-style `.guard.ts` / `.interceptor.ts` / `.resolver.ts`, e.g. `auth.guard.ts`, `http-error.interceptor.ts`), and **DTO** (`.request.ts` / `.response.ts`).
- Files are kebab-case; types/classes PascalCase; functional artifacts (guard/interceptor/resolver) camelCase. The class name describes the role, not the mechanism.
- Component selectors: app prefix + kebab-case; directive selectors: camelCase.
- **Enums over union types** for closed value sets — always prefer a plain `enum` (not `const enum`) over a `type X = 'a' | 'b'` union, one enum per file in `enums/`. Localized labels/severity/icons live in a separate map file next to the enum (e.g. `account-status-labels.ts` → `Record<AccountStatus, …>`). (The database mirrors the same closed sets as enum-style columns, not dictionary tables — see **BE · Database Schema**.)

**Canonical naming table** (app selector prefix = `uz`):

| Artifact                    | File                                                   | Class / symbol                             | Selector / name                        |
| --------------------------- | ------------------------------------------------------ | ------------------------------------------ | -------------------------------------- |
| Component                   | `user-profile.ts`                                      | `UserProfile`                              | `uz-user-profile` (app prefix + kebab) |
| Layout shell                | `logged-layout.ts`                                     | `LoggedLayout`                             | `uz-logged-layout`                     |
| Directive                   | `highlight.ts`                                         | `Highlight`                                | `[uzHighlight]` (camelCase)            |
| Service / store             | `user-data.ts` / `accounts.store.ts`                   | `UserData` / `AccountsStore`               | —                                      |
| Guard                       | `is-logged.guard.ts`                                   | `isLoggedGuard`                            | —                                      |
| Interceptor                 | `auth.interceptor.ts`                                  | `authInterceptor`                          | —                                      |
| Resolver                    | `seo.resolver.ts`                                      | `seoResolver`                              | —                                      |
| **Pipe** (suffix exception) | `to-currency-pipe.ts`                                  | `ToCurrencyPipe`                           | name string `toCurrency`               |
| Model                       | `account.ts`                                           | `Account`                                  | —                                      |
| **DTO** (suffix exception)  | `login-by-pin.request.ts` / `login-by-pin.response.ts` | `LoginByPinRequest` / `LoginByPinResponse` | —                                      |
| Enum                        | `account-status.ts`                                    | `AccountStatus`                            | members `PascalCase` / `UPPER_CASE`    |
| Enum label map              | `account-status-labels.ts`                             | `accountStatusLabels`                      | —                                      |
| Form schema                 | `login-schema.ts`                                      | `loginSchema`                              | —                                      |
| Server routes               | `app.routes.server.ts`                                 | `serverRoutes`                             | —                                      |
| Test                        | `user-profile.spec.ts`                                 | —                                          | —                                      |

## FE · DTO Conventions

- Place DTOs in `[feature]/DTO/Requests/` and `[feature]/DTO/Responses/`.
- Name the file after the service method, kebab-case + `.request.ts` / `.response.ts` (e.g. `login-by-pin.request.ts` → `LoginByPinRequest`).
- Each folder has a barrel `index.ts` re-exporting its DTOs; import via the barrel (`import { ... } from '../DTO/Requests'`).

## FE · Project Structure

- Top-level split is **by access context**: cross-cutting `core/` (`seo/`, `platform/`, `errors/`, `notifications/`, `security/`, `auth/`), `shared/`, `theme/`, `layout/` — alongside the **areas** `public/` (unauthenticated) and `logged/` (behind auth). Each area groups feature folders. No flat `features/`.
- **Colocation + hoisting** is the core rule for every artifact (component, service, DTO, enum, model, schema): keep it next to its only consumer; when a second consumer appears, hoist it to the lowest common ancestor. Promotion ladder: page component → feature → area (`public`/`logged`) → `shared`/`core`. The bucket set (`components/`, `services/`, `models/`, `enums/`, `schemas/`, `DTO/`) repeats at every level. **Pages (route-level components) live under `components/`** too (e.g. `public/auth/components/login/`).
- Each area has a layout **shell component** (e.g. `LoggedLayout`, `PublicLayout`) hosting `<router-outlet>`; child routes mount in the shell. Shells stay in `layout/`.
- Expose each feature's public API via a flat barrel `index.ts`; avoid deep barrels and cross-imports. Import across areas only through path aliases (`@app/*`, `@core/*`, `@shared/*`, `@public/*`, `@logged/*`, `@layout/*`) and barrels; intra-feature imports stay relative.

## FE · Tooling

- ESLint 9 (flat config) + angular-eslint + Prettier + stylelint. Tests with **Vitest**.
- Lint enforces: `@typescript-eslint/no-deprecated`, `explicit-member-accessibility`, `no-explicit-any`, no `@HostBinding`/`@HostListener`, no `ngClass`/`ngStyle`, Observable-over-Promise, `max-classes-per-file: 1`, enum-over-union, no color literals (outside `theme/`), no `::ng-deep`/`.p-*`, no `@angular/animations`, AXE in CI.

## FE · Finishing Every Implementation

After completing any frontend task, you MUST always:

1. Run `npm run lint:fix` and fix any remaining lint errors manually.
2. Run `npm run format`.
3. Re-run until there are **zero** lint errors.
4. Verify: all i18n keys exist in every locale file; AXE passes; no hardcoded colors; no `@deprecated` usage.

---

# BACKEND (C# / .NET, ASP.NET Core, CQRS)

You are an expert in C# .NET, ASP.NET Core, and scalable backend application development. You write clean, maintainable, and performant code following .NET and CQRS best practices.

## BE · Request-Handling Flow

Every feature follows a strict layered flow. Never skip a layer or bypass it.

```
Controller  →  MediatR Command/Query  →  Handler  →  Repository  →  .sql file
```

### 1. Controller (`Controllers/`)

- Controllers are thin — they only validate input, call `mediator.Send(...)`, and return the result.
- Never put business logic in a controller.
- Create a dedicated Command or Query class for every action.

```csharp
var result = await mediator.Send(new GetCarInfoQuery(request.CompanyGuid, request.CarId));
```

### 2. Commands & Queries (`Commands/` / `Queries/`)

- **Commands** = write operations (insert, update, delete). Place in `Commands/{Feature}/{OperationName}/`.
- **Queries** = read operations. Place in `Queries/{Feature}/{OperationName}/`.
- Each operation has two files in its folder:
  - `{OperationName}Command.cs` / `{OperationName}Query.cs` — the MediatR request record/class.
  - `{OperationName}CommandHandler.cs` / `{OperationName}QueryHandler.cs` — implements `IRequestHandler<,>`.
- Handlers contain business logic and call the relevant repository method. They do NOT execute SQL directly.

```csharp
var car = await carsRepository.GetCarAsync(query.CarId, Guid.Parse(query.CompanyGuid));
```

### 3. Repository (`Repositories/`)

- Every entity has `I{Entity}Repository` interface + `{Entity}Repository` implementation.
- Repositories use **Dapper** for data access. They do NOT contain SQL strings inline.
- Load SQL from embedded `.sql` files via `SqlHelper.GetSql("{MethodName}")`.
- Group parameters in `Repositories/Parameters/{Entity}/` and DAOs in `Repositories/DAO/{Entity}/`.

```csharp
string sqlQuery = SqlHelper.GetSql("GetCarByIdAsync");
await connection.QueryFirstOrDefaultAsync<CarDAO>(sqlQuery, parameters, connection.CurrentTransaction);
```

### 4. SQL Files (`Repositories/Sql/{RepositoryName}/{MethodName}.sql`)

- One `.sql` file per repository method. Name matches the method name exactly.
- Example: `Repositories/Sql/CarsRepository/GetCarByIdAsync.sql`
- SQL files are embedded resources — set `Build Action: Embedded Resource` in the project file.

## BE · Security & Multi-Tenancy

- Derive the tenant identifier from the **authenticated context** (token claims) — never trust a tenant id supplied in the request body, route, or query (e.g. a tenant/company id field).
- **Scope every read and write to the current tenant.** No query or command may return or mutate data belonging to another tenant; filter by the tenant id on every data-access call.
- Enforce authorization before acting: required role/permission, resource ownership, and a valid (non-expired) token. Reject cross-tenant or unauthorized access with the appropriate status — never by silently returning empty data.

## BE · Validation & Pipeline Behaviors

- Validate input with **FluentValidation** at the Command/Query boundary via a MediatR `ValidationBehavior` — **not** inside handlers.
- Put cross-cutting concerns in **MediatR pipeline behaviors** (validation, logging, performance, transaction) instead of repeating them in handlers.
- Propagate `CancellationToken` end-to-end: `mediator.Send(..., ct)` → handler → repository method → Dapper command.

## BE · Database Schema

- Whenever you add, remove, or rename a table, column, index, or relationship in the database, you MUST update `DbDiagram.dbml` (located at the root of the backend repository) to reflect the change before considering the task done.
- **Prefer enums over dictionary/lookup tables** for closed value sets (statuses, kinds, categories). Model the value as an enum-style column — a `tinyint`/`int` backed by the corresponding enum, optionally guarded by a `CHECK` constraint — instead of creating a separate reference table with an FK just to enumerate a fixed set. The C# side **MUST replicate the exact same set as a real `enum`** (one enum per file); the DB column's allowed values equal the enum members, and both stay in sync. This mirrors the frontend rule (**FE · Naming & Files** — enums over union types), so the same closed set is expressed as an enum on every layer (TS enum ↔ C# enum ↔ enum-style column).

## BE · Database Migrations

- ALL schema changes (CREATE/ALTER TABLE, indexes, constraints, etc.) MUST go through a **numbered SQL script file** in `Scripts/` — never inline DDL in code, commands, or instructions.
- Naming: `Script{NNNNN} - {short-description-in-english}.sql` (zero-padded 5-digit; pick the next number in sequence).
- **Mock/seed data goes in a separate script in the `90000+` number range** (e.g. `Script90001 - seed-legal-acts-mock-data.sql`), never mixed into a real DDL migration. Rationale: the high range clearly separates throwaway mock/demo data from production migrations, so it's easy to spot and delete later. Keep seeds idempotent (`IF NOT EXISTS`).
- Update `DbDiagram.dbml` in the same change (see BE · Database Schema).

## BE · Data Integrity

- Money is always `decimal` — never `double` / `float`.
- Store and expose dates in **UTC**; convert to the local (PL) timezone only at the edges (presentation / API boundary).
- Write operations (Commands) run inside a transaction (`connection.CurrentTransaction`); reads run without one. One transaction per command.
- SQL is always parameterized (Dapper parameters) — never string-concatenate values into SQL.

## BE · Errors, Logging & Observability

- Map exceptions to a consistent HTTP contract via global exception-handling middleware (**ProblemDetails**). Never swallow exceptions; never leak raw exception details to clients.
- Use structured logging (**Serilog**) plus the monitoring SDK (**Sentry**); attach a correlation id per request.
- **Never log PII or secrets** (tokens, API keys, certificates, payment data).

## BE · Naming Conventions

| Artifact             | Pattern                          | Example                                  |
| -------------------- | -------------------------------- | ---------------------------------------- |
| Command              | `{Action}{Entity}Command`        | `ConfirmCarTachographReadCommand`        |
| Command handler      | `{Action}{Entity}CommandHandler` | `ConfirmCarTachographReadCommandHandler` |
| Query                | `{Action}{Entity}Query`          | `GetCarInfoQuery`                        |
| Query handler        | `{Action}{Entity}QueryHandler`   | `GetCarInfoQueryHandler`                 |
| Repository interface | `I{Entity}Repository`            | `ICarsRepository`                        |
| Repository class     | `{Entity}Repository`             | `CarsRepository`                         |
| Parameters class     | `{MethodName}Parameters`         | `ConfirmCarTachographReadParameters`     |
| DAO class            | `{Entity}DAO`                    | `CarDAO`                                 |
| SQL file             | `{MethodName}.sql`               | `GetCarByIdAsync.sql`                    |

## BE · General Rules

- NEVER use `var` — always declare explicit types (e.g. `string sqlQuery`, `CarDAO car`). This applies everywhere: local variables, loop variables, `using` declarations, and `out` parameters.
- Use `async`/`await` throughout — no `.Result` or `.Wait()`.
- Never catch and swallow exceptions silently.
- Keep handlers focused on one operation — no handler should do two unrelated things.
- Do not add DTOs, parameters, or DAOs that are not used by any handler or repository method.
- Use `record` types for Commands and Queries (immutable requests).
- Enable nullable reference types; treat warnings as errors.
- Map `request → Command/Query` and `DAO → response model` explicitly; a DAO must never leak to the API surface.
- Paginate list endpoints and avoid N+1 queries.
