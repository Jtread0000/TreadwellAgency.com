# Deploying to IONOS

This is a **plain static site** — no build step runs on the server, no Node,
no PHP, no database. Deploying = copying the repository's files into the
IONOS web document root.

## What to upload

Upload the **entire repository contents** (everything except the `.git/`
folder and this doc / the generator) to the site's document root. On IONOS
shared hosting the docroot is typically:

```
/homepages/NN/dXXXXXXXXX/htdocs/        (or a subfolder if the domain points to one)
```

Files that must land in the docroot:

```
index.html
404.html
.htaccess              # ships HTTPS redirect, caching, 404, security headers
robots.txt
sitemap.xml
services/index.html
training/index.html
ai-readiness/index.html
approach/index.html
about/index.html
assets/                # css, js, favicon, elements/, canvas/, canvas-preview.png
```

Not needed on the server (safe to exclude): `scripts/`, `README.md`,
`DEPLOY.md`, `.git/`.

## Important: the site is served from the domain ROOT

All internal links and asset URLs are **root-absolute** (e.g. `/assets/...`,
`/services/`). So the files must sit at the document root of
`https://treadwellagency.com/`. If they were placed in a subfolder
(e.g. `/site/`), the links would break. Deploy to the docroot itself.

Clean directory URLs (`/services/`) work automatically — Apache serves
`services/index.html` via `DirectoryIndex`. No rewrite rules are needed for
routing.

## Example rsync over SSH

From a clone of this repo:

```bash
rsync -avz --delete \
  --exclude '.git' --exclude 'scripts' \
  --exclude 'README.md' --exclude 'DEPLOY.md' \
  ./  USER@HOST:/path/to/htdocs/
```

(Include `.htaccess` — rsync copies dotfiles by default. Drop `--delete` if
the docroot contains other files you want to keep.)

## .htaccess notes

- Forces HTTPS and redirects `www` → non-www. **If you prefer `www`**, edit
  the two RewriteRules in `.htaccess`.
- Requires Apache `mod_rewrite`, `mod_headers`, `mod_expires`, `mod_deflate`
  — all standard and enabled on IONOS shared hosting. If any module is
  unavailable the `<IfModule>` guards make that block a no-op (site still
  works).

## After deploy — smoke test

```
https://treadwellagency.com/                 -> Home
https://treadwellagency.com/services/         -> Services
https://treadwellagency.com/ai-readiness/     -> AI Readiness
https://treadwellagency.com/assets/canvas/AI-Readiness-Canvas.pdf  -> PDF downloads
https://treadwellagency.com/nope              -> branded 404 page
```

Also confirm `http://` redirects to `https://`.

## Changing content later

Edit `scripts/build.py`, run `python3 scripts/build.py`, commit, and
re-deploy the regenerated HTML. The `EMAIL` used by every "Book a
consultation" CTA is set at the top of that file.
