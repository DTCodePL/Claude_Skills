---
name: tachoping-design
description: Use this skill to generate well-branded interfaces and assets for TachoPing, either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping. TachoPing is a tachograph-deadline reminder service for small road-transport fleets (Polish, non-technical audience).
user-invocable: true
version: "1.5"
---
 
# TachoPing — Design System (monolithic)
 
> Everything needed to build on-brand TachoPing interfaces is embedded in this single file.
> No external file references required.
 
---
 
## 1. What is TachoPing?
 
TachoPing tells truck & van drivers (and their bosses) exactly when the law requires them
to download tachograph data — before they get fined. Under EU rules a vehicle's tachograph
must be read every **90 days** and a driver card every **28 days**; a missed read can cost
up to **500 PLN per file** and across a fleet escalate into thousands plus an ITD penalty.
 
Pitch: **"Zero sprzętu. Zero ingerencji w pojazd."** No device installed; works at the
organisational level, sends SMS/push reminders, driver confirms a read in a PIN-locked app.
 
Audience: **deliberately non-technical** — small-fleet owners and professional drivers.
Everything is plain-language, urgency-framed, and tap-friendly.
 
### Three surfaces
 
| Surface | Who | Theme |
|---|---|---|
| **Driver PWA** | Drivers, in-cab | **Dark** — near-black `#09090b`, green accent, PIN login |
| **Owner Dashboard** | Fleet owners / office | **Light** — slate neutrals, navy CTAs, fleet table |
| **Public / Marketing + Auth** | Prospects | **Light** — landing, pricing, login/register |
 
---
 
## 2. CONTENT VOICE
 
- **Polish primary.** Informal "you" (Ty/Twój). Brand uses "we": *Pilnujemy, Powiadamiamy.*
- **Lead with the stake, then the relief.** Bold declarative headline + sub-line that de-escalates.
  - *"Brak odczytu to nie 500 PLN. To paraliż Twojego biznesu."*
  - *"Zero sprzętu. Zero ingerencji w pojazd. Flota zawsze na zielono."*
- **Numbers are concrete:** "co 90 dni", "co 28 dni", "15 PLN/pojazd/mies.", "do 40 000 PLN".
- **Status vocabulary (fixed):** `Zabezpieczony` (green), `Zbliża się termin` (amber), `Ryzyko kary ITD` (red).
- **Casing:** sentence case for headings/body; UPPERCASE + letter-spacing only for eyebrow labels.
- **No emoji anywhere** in product or marketing. Icons = FontAwesome solid.
- **Vibe:** trustworthy, no-nonsense, slightly insistent. Reassurance verbs: *Pilnujemy, Powiadamiamy, Zabezpiecz, Gotowe.*
---
 
## 3. VISUAL FOUNDATIONS
 
### Two-theme system
 
**Driver PWA = dark:**
- Body `#09090b`, cards `#18181b`, raised tiles/PIN keys `#27272a`, hairlines `#3f3f46`
- Text `#e4e4e7` (off-white), muted `#71717a`
- Green `#10b981` is the single accent
- **No borders, no shadows on dark cards** — separated by luminance step only
**Owner + Public = light:**
- Page `#f8fafc` (slate-50), cards `#f1f5f9`/`#fff`
- Borders `#e2e8f0`/`#cbd5e1`, headings `#1e293b`, secondary text `#64748b`
- **Navy** (`#243b53` / `#334e68`) is CTA/primary, not green
### Colour = status, always
 
| State | Color | Light bg | Dark variant |
|---|---|---|---|
| Secured / OK | `#10b981` | `#bef8e2` | `#047857` |
| Approaching deadline | `#f59e0b` | `#fffbeb` | `#d38b11` |
| ITD penalty risk | `#ef4444` | `#fef2f2` | `#b91c1c` |
 
### Typography
 
- **Inter** for everything (300–900). Display/hero: Inter 800, tight tracking `-0.01em`.
- **DM Mono** for countdown timer, PIN digits, big stat figures — reinforces "instrument/dashboard" feel.
- Eyebrows: 11px, 600, uppercase, `0.07em` tracking, muted colour.
- Buttons: sentence case.
### Spacing & layout
 
- 4px base scale; cards 8–14px internal padding, 8–10px gaps.
- Driver app: single non-scrolling 100dvh viewport.
- Marketing: centred max-width ~1200px, **one dark navy band** (`#243b53`→`#1e293b`) for regulatory section.
### Corner radii
 
| Token | Value | Usage |
|---|---|---|
| `--tp-r-xs` | 4px | code chips, tiny tags |
| `--tp-r-sm` | 6px | buttons, inputs |
| `--tp-r-md` | 10px | light cards |
| `--tp-r-lg` | 12px | PIN keys, status tiles |
| `--tp-r-xl` | 14px | dark dashboard cards |
| `--tp-r-2xl` | 22px | PIN lock icon wrapper |
| `--tp-r-pill` | 999px | pills, avatars |
 
### Shadows (light surfaces only)
 
```
--tp-shadow-xs:  0 2px 8px rgba(15,23,42,0.07)
--tp-shadow-sm:  0 4px 6px rgba(15,23,42,0.08), 0 16px 32px rgba(15,23,42,0.20)
--tp-shadow-md:  0 10px 10px rgba(15,23,42,0.12), 0 24px 30px rgba(15,23,42,0.28)
--tp-focus-ring: 0 0 0 0.2rem rgba(51,78,104,0.15)
```
 
Dark theme uses luminance, never shadow.
 
### Backgrounds
 
Flat fills — **no gradients, no photos, no textures, no illustration** in core UI. Only logo and flag PNGs. Modal backdrop: dark scrim `rgba(113,117,122,0.70)`. No blur/glass.
 
### Motion
 
- Entrance: `slide-in-up` (translateY 12–20px + fade), 0.4s `ease-out`, staggered 60–80ms.
- PIN keys: springy `cubic-bezier(0.34,1.56,0.64,1)`, staggered 38ms.
- PIN dots: scale `1→1.5→0.88→1` with soft glow when filled.
- Marketing countdown red dot: blinks `2s infinite` (only looping animation).
- All gated behind `prefers-reduced-motion`.
- Hover/press: dark cards `filter: brightness(1.15)`; PIN keys `scale(0.95)`.
---
 
## 4. ICONOGRAPHY
 
- **FontAwesome Free 7.x (solid `fas`/`fa-solid`).** Only icon set.
- Load from CDN: `https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.0/css/all.min.css`
- Key glyphs: `fa-van-shuttle`, `fa-truck-front`, `fa-id-card`, `fa-circle-check`, `fa-chevron-right`, `fa-triangle-exclamation`, `fa-lock`, `fa-bell`
- Brand colour for active icon: green on dark, navy on light.
---
 
## 5. CSS VARIABLES (embed in every artifact)
 
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,400&family=DM+Mono:wght@400;500&display=swap');
 
:root {
  /* Brand */
  --tp-green:        #10b981;
  --tp-green-dark:   #047857;
  --tp-green-light:  #bef8e2;
  --tp-green-success:#e9fef6;
  --tp-green-50:     #ecfdf5;
  --tp-green-200:    #a7f3d0;
 
  --tp-navy-700:     #334e68;
  --tp-navy-800:     #243b53;
 
  /* Driver PWA — dark */
  --tp-background:   #09090b;
  --tp-surface:      #18181b;
  --tp-surface-2:    #27272a;
  --tp-border-dark:  #3f3f46;
  --tp-text:         #e4e4e7;
  --tp-muted:        #71717a;
 
  /* Owner + Public — light slate */
  --tp-slate-50:     #f8fafc;
  --tp-slate-100:    #f1f5f9;
  --tp-slate-200:    #e2e8f0;
  --tp-slate-300:    #cbd5e1;
  --tp-slate-400:    #94a3b8;
  --tp-slate-500:    #64748b;
  --tp-slate-600:    #475569;
  --tp-slate-800:    #1e293b;
  --tp-white:        #ffffff;
 
  /* Semantic state */
  --tp-amber:        #f59e0b;
  --tp-amber-light:  #f8cf8b;
  --tp-amber-dark:   #d38b11;
  --tp-amber-bg:     #fffbeb;
  --tp-red:          #ef4444;
  --tp-red-dark:     #b91c1c;
  --tp-red-200:      #fecaca;
  --tp-red-bg:       #fef2f2;
  --tp-info:         #3b82f6;
  --tp-overlay:      rgba(113,117,122,0.70);
 
  /* Elevation */
  --tp-shadow-xs:  0 2px 8px rgba(15,23,42,0.07);
  --tp-shadow-sm:  0 4px 6px rgba(15,23,42,0.08), 0 16px 32px rgba(15,23,42,0.20);
  --tp-shadow-md:  0 10px 10px rgba(15,23,42,0.12), 0 24px 30px rgba(15,23,42,0.28);
  --tp-focus-ring: 0 0 0 0.2rem rgba(51,78,104,0.15);
 
  /* Radii */
  --tp-r-xs:   4px;
  --tp-r-sm:   6px;
  --tp-r-md:   10px;
  --tp-r-lg:   12px;
  --tp-r-xl:   14px;
  --tp-r-2xl:  22px;
  --tp-r-pill: 999px;
 
  /* Spacing (4px base) */
  --tp-space-1: 4px;  --tp-space-2: 8px;  --tp-space-3: 12px;
  --tp-space-4: 16px; --tp-space-5: 24px; --tp-space-6: 32px;
 
  /* Fonts */
  --tp-font-sans: 'Inter', system-ui, -apple-system, sans-serif;
  --tp-font-mono: 'DM Mono', ui-monospace, monospace;
 
  /* Type scale */
  --tp-h1-size: 40px;    --tp-h1-weight: 800; --tp-h1-lh: 1.1;  --tp-h1-ls: -0.01em;
  --tp-h2-size: 28px;    --tp-h2-weight: 700; --tp-h2-lh: 1.15; --tp-h2-ls: -0.01em;
  --tp-h3-size: 20px;    --tp-h3-weight: 700; --tp-h3-lh: 1.25;
  --tp-title-size: 17px; --tp-title-weight: 700; --tp-title-lh: 1.3;
  --tp-body-size: 15px;  --tp-body-weight: 400; --tp-body-lh: 1.5;
  --tp-small-size: 13px; --tp-small-lh: 1.45;
  --tp-caption-size: 11px; --tp-caption-weight: 600; --tp-caption-lh: 1.4;
  --tp-eyebrow-ls: 0.07em;
  --tp-stat-size: 28px;  --tp-stat-weight: 700;
}
 
/* Semantic helper classes */
.tp-h1 { font-family:var(--tp-font-sans); font-size:var(--tp-h1-size); font-weight:var(--tp-h1-weight); line-height:var(--tp-h1-lh); letter-spacing:var(--tp-h1-ls); color:var(--tp-slate-800); margin:0; }
.tp-h2 { font-family:var(--tp-font-sans); font-size:var(--tp-h2-size); font-weight:var(--tp-h2-weight); line-height:var(--tp-h2-lh); letter-spacing:var(--tp-h2-ls); color:var(--tp-slate-800); margin:0; }
.tp-h3 { font-family:var(--tp-font-sans); font-size:var(--tp-h3-size); font-weight:var(--tp-h3-weight); line-height:var(--tp-h3-lh); color:var(--tp-slate-800); margin:0; }
.tp-title { font-family:var(--tp-font-sans); font-size:var(--tp-title-size); font-weight:var(--tp-title-weight); line-height:var(--tp-title-lh); margin:0; }
.tp-body { font-family:var(--tp-font-sans); font-size:var(--tp-body-size); font-weight:400; line-height:var(--tp-body-lh); color:var(--tp-slate-500); margin:0; }
.tp-small { font-family:var(--tp-font-sans); font-size:var(--tp-small-size); line-height:var(--tp-small-lh); color:var(--tp-slate-500); margin:0; }
.tp-eyebrow { font-family:var(--tp-font-sans); font-size:var(--tp-caption-size); font-weight:600; letter-spacing:var(--tp-eyebrow-ls); text-transform:uppercase; color:var(--tp-slate-500); margin:0; }
.tp-stat { font-family:var(--tp-font-mono); font-size:var(--tp-stat-size); font-weight:700; line-height:1; }
.tp-mono { font-family:var(--tp-font-mono); }
```
 
---
 
## 6. COMPONENT PATTERNS
 
### tp-card (light)
```css
background: var(--tp-slate-100);  /* or #fff for inner cards */
border: 1px solid var(--tp-slate-300);
border-radius: var(--tp-r-md);    /* 10px */
box-shadow: var(--tp-shadow-xs);
padding: 24px 28px;
```
 
### tp-input (light)
```css
background: var(--tp-slate-50);
border: 1px solid var(--tp-slate-200);
border-radius: var(--tp-r-sm);    /* 6px */
padding: 10px 12px;
font-size: 15px;
color: var(--tp-slate-800);
/* placeholder color: var(--tp-slate-400) */
/* focus: border-color var(--tp-navy-700), box-shadow var(--tp-focus-ring) */
```
 
### tp-btn-primary (light)
```css
background: var(--tp-navy-800);
color: var(--tp-slate-50);
border: none;
border-radius: var(--tp-r-sm);    /* 6px */
padding: 11px 20px;
font-size: 15px;
font-weight: 600;
/* hover: background var(--tp-slate-800) */
```
 
### tp-btn-outline (light)
```css
background: var(--tp-slate-50);
color: var(--tp-navy-700);
border: 1.5px solid var(--tp-navy-700);
border-radius: var(--tp-r-sm);
padding: 10px 20px;
font-size: 14.5px;
font-weight: 600;
```
 
### label (light forms)
```css
font-size: 14px;
font-weight: 500;           /* or 600 for Semi Bold variant */
color: var(--tp-navy-700);  /* or var(--tp-slate-600) */
```
 
### Status badge
```html
<span style="display:inline-flex;align-items:center;gap:6px;padding:3px 10px 3px 8px;
border-radius:999px;border:1px solid {border};background:{bg};color:{color};
font-size:12px;font-weight:600;">
  <span style="width:7px;height:7px;border-radius:50%;background:{dot}"></span>
  {label}
</span>
```
- Secured: color `--tp-green`, bg `--tp-green-50`, border `--tp-green-200`
- Upcoming: color `--tp-amber-dark`, bg `--tp-amber-bg`, border `--tp-amber-light`
- Danger: color `--tp-red-dark`, bg `--tp-red-bg`, border `--tp-red-200`
### Owner sidebar
```css
width: 248px;
background: var(--tp-slate-800);
/* nav item active: background var(--tp-navy-800), color #fff, font-weight 600 */
/* nav item default: color var(--tp-slate-400), font-weight 500 */
/* footer border: 1px solid rgba(255,255,255,.08) */
```
 
### Dark surface card (Driver PWA)
```css
background: var(--tp-surface);     /* #18181b */
border-radius: var(--tp-r-xl);     /* 14px */
/* No border, no shadow — use --tp-surface-2 for raised elements */
```
 
### PIN key
```css
background: var(--tp-surface-2);   /* #27272a */
border-radius: var(--tp-r-lg);     /* 12px */
width: 70px; height: 70px;
font-family: var(--tp-font-mono);
font-size: 26px; font-weight: 500;
color: var(--tp-text);
/* press: transform scale(0.95) */
/* animation: springy cubic-bezier(0.34,1.56,0.64,1), staggered 38ms */
```
 
---
 
## 7. OWNER DASHBOARD UI KIT
 
### Shell structure
```html
<div class="shell"> <!-- display:flex; height:100vh -->
  <OwnerSidebar />  <!-- 248px, slate-800 bg -->
  <div class="main"> <!-- flex:1, overflow:auto -->
    <div class="topbar"> <!-- sticky, border-bottom slate-200 -->
      <h1>Panel floty</h1>
      <span class="lang"><!-- flag + language selector --></span>
    </div>
    <div class="content"> <!-- padding:24px 28px, max-width:1080px -->
      <!-- optional amber warning banner -->
      <SummaryCards />
      <FleetTable />
    </div>
  </div>
</div>
```
 
### SummaryCards (4 stat counters)
```jsx
const cards = [
  { label:'Pojazdy',           value:'12', sub:'w Twojej flocie',  tone:'neutral' },
  { label:'Zabezpieczone',     value:'9',  sub:'wszystko na czas', tone:'ok'      },
  { label:'Zbliża się termin', value:'2',  sub:'poniżej 21 dni',   tone:'warning' },
  { label:'Wymaga działania',  value:'1',  sub:'ryzyko kary ITD',  tone:'danger'  },
];
// value uses DM Mono; color: neutral=slate-800, ok=green, warning=amber, danger=red
// card: bg slate-50, border slate-300, radius 10px, padding 10px 12px
// grid: 4 columns, gap 8px
```
 
### FleetTable columns
- Vehicles: Pojazd · Ostatni odczyt · Status · Plik · Do terminu · (actions)
- Drivers: Kierowca · Ostatni odczyt · Status · Potwierdzenia · Do terminu · (actions)
- Row bg by status: secured=`#fff`, upcoming=`--tp-amber-bg`, danger=`--tp-red-bg`
- Hover darkens tint slightly
- Header: `--tp-slate-100` bg, 11px uppercase 600 tracking `.8px`
- Actions: trash (danger hover) + edit icons, 30×30px, radius 5px
### Warning banner
```css
background: var(--tp-amber-bg);
border: 1px solid var(--tp-amber-light);
border-radius: 10px;
padding: 12px 16px;
color: var(--tp-amber-dark);
font-size: 13.5px;
/* icon: fa-triangle-exclamation, color --tp-amber, 18px */
```
 
---
 
## 8. DRIVER PWA UI KIT
 
### App shell (dark, single viewport)
```css
background: var(--tp-background);  /* #09090b */
height: 100dvh; overflow: hidden;
font-family: var(--tp-font-sans); color: var(--tp-text);
```
 
### App bar
```css
display:flex; align-items:center; padding:14px 16px;
border-bottom: 1px solid var(--tp-border-dark);
/* left: logo; right: flag + language */
```
 
### PIN lock screen
```
/* Lock icon wrapper: 72px, radius 22px, bg surface-2 */
/* 4 PIN dots: 14px circles, filled=green glow, empty=border-dark */
/* Keypad: 3×4 grid, keys 70×70px, surface-2, radius 12px, DM Mono */
/* "Zapomniałem PINu" link: muted colour */
```
 
### DriverDashboard layout
```
DriverCard (surface, radius 14px)
  avatar (48px, navy-800, radius 10px) + name + vehicle line
 
2-col grid: StatCard × 2
  label: 9px uppercase muted
  value: 32px DM Mono, colour by tone
  sub: 12px muted
 
Eyebrow: "CO DZISIAJ ZGRAŁEŚ?"
 
SyncCard × 3 (surface-2, radius 14px)
  icon tile (46px, border-dark bg, radius 12px)
  title 16px 700 + sub 13px muted
  chevron-right green
 
"Mam problem ze zgraniem pliku" text button
```
 
### Slide-up entrance animation
```css
@keyframes tpSlideUp {
  from { opacity:0; transform:translateY(16px); }
  to   { opacity:1; transform:translateY(0); }
}
/* usage: animation: tpSlideUp .4s ease-out {delay}ms both */
/* stagger: card1=0ms, card2=80ms, card3=140ms, etc. */
```
 
---
 
## 9. PUBLIC (MARKETING + AUTH) UI KIT
 
### Auth card (light)
```css
max-width: 440px;
background: var(--tp-slate-100);
border: 1px solid var(--tp-slate-200);
border-radius: 12px;
padding: 40px 32px;
```
 
### Auth input
```css
border: 1px solid var(--tp-slate-200);
background: var(--tp-slate-50);
color: var(--tp-slate-800);
border-radius: 6px;
padding: 10px 12px;
font-size: 15px;
width: 100%; box-sizing: border-box;
```
 
### Auth label
```css
font-size: 14px;
font-weight: 500;
color: var(--tp-navy-700);
```
 
### CTA button (auth)
```css
background: var(--tp-navy-800);
color: var(--tp-slate-50);
border-radius: 6px;
padding: 11px;
font-size: 15px; font-weight: 600;
width: 100%;
```
 
### Hero section
```
Eyebrow pill: green border, green-50 bg, green text, radius pill
H1: Inter 800, 40px, slate-800, tracking -0.01em
Sub: 18px, slate-500
CTA: navy-800 button (full or fixed width)
Fine print: 13px slate-400
Live countdown: DM Mono, large, red dot blinks 2s infinite
```
 
### Regulatory dark band
```css
background: var(--tp-navy-800);  /* to var(--tp-slate-800) gradient is ok */
color: #fff;
/* 4-column country grid: PL · DE · FR · GB */
/* penalty amounts in DM Mono, amber/red */
```
 
### Pricing section
```
Promo banner: amber-bg, amber border
Slider: range input, navy accent
Calculator: card with line items + total in large DM Mono
```
 
### Footer
```css
background: var(--tp-zinc-950);  /* #09090b */
color: var(--tp-slate-400);
/* link columns, logo, legal */
```
 
---
 
## 10. ARTIFACT TEMPLATE (HTML mock)
 
When building HTML artifacts/mocks, always use this boilerplate:
 
```html
<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TachoPing — [Screen name]</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.0/css/all.min.css">
<style>
/* Paste full CSS variables block from §5 here */
* { box-sizing: border-box; }
body { margin: 0; font-family: var(--tp-font-sans); }
</style>
</head>
<body>
<!-- content -->
</body>
</html>
```
 
For React artifacts, import React from CDN and write JSX inline with Babel standalone,
using inline styles referencing the CSS variables above.
 
---
 
## 11. FIGMA DESIGN TOKENS (for use_figma plugin API)
 
When writing Figma plugin scripts, use these resolved hex values:
 
```js
const TP = {
  // Light theme
  slate50:   { r:0.973, g:0.980, b:0.988 },  // #f8fafc — page bg
  slate100:  { r:0.945, g:0.957, b:0.973 },  // #f1f5f9 — cards
  slate200:  { r:0.886, g:0.906, b:0.941 },  // #e2e8f0 — dividers
  slate300:  { r:0.796, g:0.835, b:0.882 },  // #cbd5e1 — borders
  slate400:  { r:0.580, g:0.639, b:0.722 },  // #94a3b8 — faint labels
  slate500:  { r:0.392, g:0.455, b:0.545 },  // #64748b — secondary text
  slate600:  { r:0.271, g:0.337, b:0.412 },  // #475569 — labels
  slate800:  { r:0.118, g:0.161, b:0.231 },  // #1e293b — headings
  navy700:   { r:0.200, g:0.306, b:0.408 },  // #334e68 — CTA
  navy800:   { r:0.141, g:0.231, b:0.325 },  // #243b53 — CTA hover
  white:     { r:1,     g:1,     b:1     },
  // Accent
  green:     { r:0.063, g:0.725, b:0.506 },  // #10b981
  greenLight:{ r:0.745, g:0.973, b:0.886 },  // #bef8e2
  amber:     { r:0.961, g:0.620, b:0.043 },  // #f59e0b
  amberBg:   { r:1,     g:0.984, b:0.922 },  // #fffbeb
  red:       { r:0.937, g:0.267, b:0.267 },  // #ef4444
  redBg:     { r:0.996, g:0.949, b:0.949 },  // #fef2f2
  // Dark theme
  background:{ r:0.035, g:0.035, b:0.043 },  // #09090b
  surface:   { r:0.094, g:0.094, b:0.106 },  // #18181b
  surface2:  { r:0.153, g:0.153, b:0.165 },  // #27272a
  borderDark:{ r:0.247, g:0.247, b:0.275 },  // #3f3f46
  text:      { r:0.894, g:0.894, b:0.906 },  // #e4e4e7
  muted:     { r:0.443, g:0.443, b:0.478 },  // #71717a
};
```
 
**tp-card shadow (light):**
```js
effects: [
  { type:'DROP_SHADOW', color:{r:0,g:0,b:0,a:0.07}, offset:{x:0,y:2}, radius:8, spread:0, visible:true, blendMode:'NORMAL' }
]
```
 
**tp-shadow-sm (modals):**
```js
effects: [
  { type:'DROP_SHADOW', color:{r:0.059,g:0.090,b:0.165,a:0.08}, offset:{x:0,y:4}, radius:6, spread:0, visible:true, blendMode:'NORMAL' },
  { type:'DROP_SHADOW', color:{r:0.059,g:0.090,b:0.165,a:0.20}, offset:{x:0,y:16}, radius:32, spread:0, visible:true, blendMode:'NORMAL' }
]
```
 
---
 
## 12. LOGOS & ASSETS
 
Logos are not embeddable as text. When building HTML artifacts, use placeholder divs styled
with the brand colours, or ask the user to provide logo URLs. Structure:
 
```
assets/
  logo-small.png        — light bg, ~26px tall
  logo-big.png          — light bg, larger
  logo-dark-small.png   — dark bg (use in dark sidebar/header)
  logo-dark-big.png     — dark bg, larger
  logo-dark-theme.png   — full dark theme variant
  flags/pl.png, gb.png, ua.png, ru.png  — language switcher (13px tall)
```
 
**Logo placeholder (when PNG not available):**
```html
<!-- Light bg -->
<span style="font-family:var(--tp-font-sans);font-weight:700;font-size:18px;">
  <span style="color:var(--tp-slate-800)">Tacho</span><span style="color:var(--tp-green)">Ping</span>
</span>
<!-- Dark bg -->
<span style="font-family:var(--tp-font-sans);font-weight:700;font-size:18px;">
  <span style="color:#fff">Tacho</span><span style="color:var(--tp-green)">Ping</span>
</span>
```
 
---
 
## 13. QUICK REFERENCE CHEATSHEET
 
| Need | Value |
|---|---|
| Page bg (light) | `#f8fafc` |
| Card bg (light) | `#f1f5f9` or `#fff` |
| Input bg | `#f8fafc`, border `#e2e8f0` |
| Input focused border | `#334e68` |
| Heading (light) | `#1e293b` Inter 700 |
| Label (light) | `#475569` Inter 500/600 14px |
| Secondary text | `#64748b` |
| Placeholder | `#94a3b8` |
| CTA button | bg `#243b53`, text `#f8fafc`, radius 6px |
| CTA hover | bg `#1e293b` |
| Sidebar bg | `#1e293b` |
| Sidebar active item | bg `#243b53` |
| Body bg (dark) | `#09090b` |
| Card bg (dark) | `#18181b` |
| Raised tile (dark) | `#27272a` |
| Hairline (dark) | `#3f3f46` |
| Text (dark) | `#e4e4e7` |
| Muted (dark) | `#71717a` |
| Green (secured) | `#10b981` |
| Amber (upcoming) | `#f59e0b` |
| Red (danger) | `#ef4444` |
| Font | Inter (UI), DM Mono (numbers/PIN) |
| Icons | FontAwesome solid 7.x |
| Radii | btn/input=6px, card=10px, dark-card=14px |
| Modal shadow | `0 4px 6px rgba(15,23,42,.08), 0 16px 32px rgba(15,23,42,.20)` |
