# aria-progress — the living WP3 progress page

A password-gated, continuously-updated progress page for George Jenkinson's WP3 work
on the ARIA Robot Dexterity programme. The page is **generated** — nobody edits
`site/index.html` by hand. Content lives in small, structured files; `build.py`
assembles them; GitHub Actions publishes to GitHub Pages on every push.

```
areas/      one file per work area: title, status chip, one-line take-home, bullets
updates/    append-only log: one small .md per update (result / new version / note)
demos/      versioned interactive artefacts:  demos/<area>/<vN>/<file>.html
media/      figures & videos referenced by updates
config.json page framing: title, groups (milestone sections), area ordering, pw hash
templates/  the page shell (CSS, gate, layout)
build.py    validates everything and writes site/   (fails loudly on bad content)
```

**Page structure it produces:** a take-homes overview (each area's one-liner — the
30-second read) → per-milestone sections with an area card each (status, bullets,
latest demos/figures, version history) → a reverse-chronological updates timeline.

---

## Publishing an update (the agent contract)

This is what "update the progress page with this latest version" means, from any
project directory. There is a `/publish-progress` skill that encodes these steps.

1. **Pull** this repo.
2. **Copy the artefact in:**
   - a new interactive version → `demos/<area>/v<N+1>/` (never overwrite old versions)
   - a figure/video → `media/` (suggested naming: `<area>_<slug>.png`)
3. **Write `updates/YYYY-MM-DD_<area>_<short-slug>.md`:**

   ```markdown
   ---
   area: feature-space            # must match a file in areas/
   date: 2026-07-02
   type: version                  # version | result | note
   version: v2                    # required if type: version
   title: One-line headline
   media: [media/feature-space_map-v2.png]
   demo: demos/actuator-map/v2/mockup_map.html
   ---
   Two to four sentences, written for the PI / ARIA, not for the lab notebook.
   ```

4. **Refresh the area's `take_home`/`status` in `areas/<area>.md`** if the headline
   state changed (this is what the overview shows).
5. **Validate & ship:** `python build.py --check`, then commit and push. The GitHub
   Action rebuilds and republishes the page automatically.

Valid `area` slugs = the filenames in `areas/`. The build **fails** on an unknown slug
or a missing media/demo file, so a bad update cannot silently publish.

To add a whole new area (a new project/thread): add `areas/<slug>.md` and list the
slug in a `config.json` group. That's the entire super-structure hook — any new
project plugs in with one content file and one line of config.

---

## One-time deployment setup

1. Create a **new GitHub repository** (public repo is fine for the Pages free tier —
   but note the repo contents are then public; a private repo needs GitHub Pro for
   Pages, or use Cloudflare Pages instead).
2. Push this directory to it (`main` branch).
3. Repo → Settings → Pages → Source: **GitHub Actions**.
4. Push anything — the action builds and deploys. The URL will be
   `https://<user>.github.io/<repo>/`.

Local preview: `python build.py`, then open `site/index.html`.

## Password / security

The gate is **client-side** (SHA-256 compared in-browser, sessionStorage persistence).
It deters casual visitors; it is **not security**: the page source is public if the
repo is public, and deep links to `media/…` or `demos/…` bypass the gate entirely.
Don't put anything here that must not leak. For real access control, host the same
`site/` output on **Cloudflare Pages + Cloudflare Access** (free tier, genuinely
private) — the build system doesn't change.

Change the password: `printf '%s' 'new-password' | sha256sum`, put the hash in
`config.json` (`pw_hash`), rebuild.

## Reporting tie-in

`updates/` is the raw material for quarterly reports: the weekly rollup is a date
filter over it, and the quarterly report is an editing pass over `areas/` + the
quarter's updates. The session→weekly→master reporting system lives in `reporting/`
in this repo (see its README and `reporting/PROJECT_AIMS.md` for the milestone
mapping and area-slug registry — the slugs there and in `areas/` must agree).
