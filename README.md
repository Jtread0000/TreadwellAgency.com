# Treadwell Agency — Marketing Website

Static marketing website for **Treadwell Agency LLC**, a Workforce &
Organization Transformation agency. Tagline: **“We solve for the human
factor.”** Every primary CTA opens a `mailto:` to book a consultation.

Built as **plain static HTML/CSS** with real routes (great SEO, no runtime
framework, deploy anywhere). A tiny Python generator keeps the shared chrome
(header, footer, `<head>`) in one place and emits the pages.

## Routes / pages

| Route            | File                    | Notes                                   |
|------------------|-------------------------|-----------------------------------------|
| `/`              | `index.html`            | Home                                    |
| `/services/`     | `services/index.html`   | Services                                |
| `/training/`     | `training/index.html`   | Training (Corporate · WIOA · Cyber)     |
| `/ai-readiness/` | `ai-readiness/index.html` | Product page + free Canvas download   |
| `/approach/`     | `approach/index.html`   | Approach / point of view                |
| `/about/`        | `about/index.html`      | Company (reached via footer/logo)       |

## Project layout

```
index.html, services/, training/, ai-readiness/, approach/, about/   generated pages
assets/
  css/site.css        design tokens + component classes (Button, Card, Tag, …)
  js/nav.js           mobile hamburger toggle
  favicon.svg         brand T-mark
  elements/*.png      decorative brand motifs
  canvas-preview.png  AI Readiness Canvas preview image
  canvas/AI-Readiness-Canvas.pdf   downloadable one-page Canvas
robots.txt, sitemap.xml
scripts/build.py      the generator (source of truth for page content)
```

## Editing & rebuilding

All page **content lives in `scripts/build.py`**. Edit there, then regenerate:

```bash
python3 scripts/build.py
```

The HTML files in the repo are generated output — regenerate rather than
hand-editing them so shared header/footer stay in sync.

### Configurable inputs (top of `scripts/build.py`)

- `EMAIL` — contact address used by every `mailto:` CTA
  (default `hello@treadwellagency.com`).
- `SITE_URL` — canonical/OG base URL.
- Home “Topic this month” block and hero motif are set inline in `home_body()`.

## Local preview

```bash
python3 -m http.server 8000
# open http://localhost:8000/
```

## Deploy

It’s a static site — publish the repository root to any static host
(Netlify, Vercel, Cloudflare Pages, GitHub Pages, S3/CloudFront). No build
step is required at deploy time; the committed HTML is ready to serve. The
routes use clean directory URLs (`/services/`), which every static host
serves as `services/index.html` by default.

## Design system notes

- **Colors:** brand blue `#271DCC`, action red `#FF220C`, signal yellow
  `#F4C500`, ink `#0A0A0A`. Signature depth cue is a hard, no-blur blue
  offset shadow.
- **Type:** Archivo (display/body) + JetBrains Mono (eyebrows/labels), loaded
  from Google Fonts. These are the licensed-font substitutes noted in the
  design handoff — swap in the brand font before a formal launch.
- Components (Button, Card, Tag, Eyebrow, Logo) are recreated as CSS classes
  in `assets/css/site.css`, matching the handed-off design-system tokens.
