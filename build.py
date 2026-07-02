"""Assemble site/index.html from config.json + areas/*.md + updates/*.md.

No dependencies beyond the standard library. Run from the repo root:

    python build.py            # build into site/
    python build.py --check    # validate only, no output

The build FAILS LOUDLY on: an update whose `area` has no areas/<slug>.md file,
a listed media/demo path that does not exist, or missing required front-matter.
That is deliberate — agents publishing updates get an immediate, clear error
instead of a silently wrong page.

Content contract (front-matter):

areas/<slug>.md         updates/YYYY-MM-DD_<slug>_<short>.md
  area: <slug>            area: <slug>          (required, must match an area)
  title: <card title>     date: YYYY-MM-DD      (required)
  status: <chip text>     title: <one line>     (required)
  rag: g|a|r              type: version|result|note   (required)
  take_home: <one line>   version: vN           (required if type: version)
  order: <int>            take_home: <one line> (optional; refreshes nothing,
  note: <optional line>                          just shown in the timeline)
  body: "- " bullets      media: [media/x.png, media/y.mp4]   (optional)
                          demo: demos/<area>/<vN>/file.html   (optional)
                          body: 2-4 sentences
"""
import html
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).parent
SITE = HERE / "site"
VIDEO_EXT = {".mp4", ".webm", ".mov"}


# ---------------------------------------------------------------- parsing

def parse_front_matter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        fail(f"{path.name}: missing front-matter (must start with ---)")
    try:
        end = text.index("\n---", 3)
    except ValueError:
        fail(f"{path.name}: unterminated front-matter")
    fm, body = {}, text[end + 4:].strip()
    for line in text[3:end].strip().splitlines():
        line = line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            fail(f"{path.name}: bad front-matter line: {line!r}")
        key, _, val = line.partition(":")
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            val = [v.strip() for v in val[1:-1].split(",") if v.strip()]
        fm[key.strip()] = val
    return fm, body


def fail(msg):
    print(f"BUILD FAILED: {msg}", file=sys.stderr)
    sys.exit(1)


def require(fm, keys, name):
    for k in keys:
        if not fm.get(k):
            fail(f"{name}: missing required front-matter key '{k}'")


def md_inline(s):
    """Escape HTML, then apply the **bold** / *italic* / `code` subset."""
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


# ---------------------------------------------------------------- loading

def load_all():
    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))

    areas = {}
    for f in sorted((HERE / "areas").glob("*.md")):
        fm, body = parse_front_matter(f)
        require(fm, ["area", "title", "status", "rag", "take_home"], f.name)
        fm["bullets"] = [l[2:].strip() for l in body.splitlines() if l.startswith("- ")]
        areas[fm["area"]] = fm

    updates = []
    for f in sorted((HERE / "updates").glob("*.md")):
        fm, body = parse_front_matter(f)
        require(fm, ["area", "date", "title", "type"], f.name)
        if fm["area"] not in areas:
            fail(f"{f.name}: unknown area '{fm['area']}' — "
                 f"add areas/{fm['area']}.md or fix the slug. "
                 f"Known: {', '.join(sorted(areas))}")
        if fm["type"] == "version" and not fm.get("version"):
            fail(f"{f.name}: type is 'version' but no 'version:' key")
        for m in fm.get("media", []) if isinstance(fm.get("media"), list) else []:
            if not (HERE / m).exists():
                fail(f"{f.name}: media file not found: {m}")
        if fm.get("demo") and not (HERE / fm["demo"]).exists():
            fail(f"{f.name}: demo file not found: {fm['demo']}")
        fm["body"] = body
        fm["file"] = f.name
        updates.append(fm)
    updates.sort(key=lambda u: u["date"], reverse=True)

    listed = [a for g in config["groups"] for a in g["areas"]]
    for slug in areas:
        if slug not in listed:
            fail(f"areas/{slug}.md exists but is not listed in any config.json group")
    for slug in listed:
        if slug not in areas:
            fail(f"config.json lists area '{slug}' but areas/{slug}.md does not exist")

    return config, areas, updates


# ---------------------------------------------------------------- rendering

def media_card(src, caption, link=None):
    ext = Path(src).suffix.lower()
    if ext in VIDEO_EXT:
        inner = f'<video src="{src}" controls muted loop></video>'
    else:
        inner = f'<img src="{src}" alt="{html.escape(caption, quote=True)}">'
    if link:
        inner = f'<a href="{link}" target="_blank" rel="noopener">{inner}</a>'
        caption = f'<a href="{link}" target="_blank" rel="noopener">{md_inline(caption)}</a>'
    else:
        caption = md_inline(caption)
    return (f'<figure class="demo" style="margin:0">{inner}'
            f'<figcaption class="cap">{caption}</figcaption></figure>')


def area_section(slug, area, updates):
    mine = [u for u in updates if u["area"] == slug]
    out = [f'<div class="area" id="area-{slug}">']
    out.append(f'<h3>{md_inline(area["title"])} '
               f'<span class="chip"><span class="dot {area["rag"]}"></span>'
               f'{md_inline(area["status"])}</span></h3>')
    out.append(f'<p class="take">{md_inline(area["take_home"])}</p>')
    if area["bullets"]:
        out.append('<ul class="prog">')
        out.extend(f"<li>{md_inline(b)}</li>" for b in area["bullets"])
        out.append("</ul>")

    # demo/media grid: newest updates first, up to 3 cards
    cards = []
    for u in mine:
        media = u.get("media") if isinstance(u.get("media"), list) else []
        demo = u.get("demo")
        if demo:
            poster = media[0] if media else None
            if poster:
                cards.append(media_card(poster, f'{u["title"]} — click to open', link=demo))
            else:
                cards.append(f'<figure class="demo" style="margin:0">'
                             f'<a href="{demo}" target="_blank" rel="noopener">'
                             f'<div class="ph">▶ open interactive demo</div></a>'
                             f'<figcaption class="cap"><a href="{demo}" target="_blank" '
                             f'rel="noopener">{md_inline(u["title"])}</a></figcaption></figure>')
            media = media[1:]
        for m in media:
            cards.append(media_card(m, u["title"]))
        if len(cards) >= 3:
            break
    if cards:
        out.append('<div class="grid">' + "".join(cards[:3]) + "</div>")

    versions = [u for u in mine if u["type"] == "version"]
    if versions:
        vs = " · ".join(
            (f'<a href="{u["demo"]}" target="_blank" rel="noopener">{u["version"]}</a>'
             if u.get("demo") else u["version"]) + f' <span class="mut">({u["date"]})</span>'
            for u in versions)
        out.append(f'<p class="versions">Versions: {vs}</p>')

    if area.get("note"):
        out.append(f'<div class="note">{md_inline(area["note"])}</div>')
    out.append("</div>")
    return "\n".join(out)


def build_html(config, areas, updates):
    nav = ['<a href="#overview">Overview</a>']
    nav += [f'<a href="#{g["id"]}">{html.escape(g["nav"])}</a>' for g in config["groups"]]
    nav.append('<a href="#updates">Updates</a>')

    # overview: every area's take-home, in config order
    take_homes = []
    for g in config["groups"]:
        for slug in g["areas"]:
            a = areas[slug]
            take_homes.append(f'<li><strong><a href="#area-{slug}">{md_inline(a["title"])}'
                              f'</a>:</strong> {md_inline(a["take_home"])}</li>')
    chips = "".join(f'<span class="chip"><span class="dot {c["rag"]}"></span>'
                    f'{html.escape(c["text"])}</span> ' for c in config["overview_chips"])

    sections = []
    for g in config["groups"]:
        body = "\n".join(area_section(slug, areas[slug], updates) for slug in g["areas"])
        sections.append(f'''
  <section id="{g["id"]}"><div class="wrap">
    <h2>{md_inline(g["heading"])}</h2>
    <p class="aim">{md_inline(g["aim"])}</p>
{body}
  </div></section>''')

    timeline = []
    for u in updates:
        area_title = md_inline(areas[u["area"]]["title"])
        tag = f' · {u["version"]}' if u.get("version") else ""
        paras = "".join(f"<p>{md_inline(p.strip())}</p>"
                        for p in u["body"].split("\n\n") if p.strip())
        links = []
        if u.get("demo"):
            links.append(f'<a href="{u["demo"]}" target="_blank" rel="noopener">open demo</a>')
        for m in (u.get("media") if isinstance(u.get("media"), list) else []):
            links.append(f'<a href="{m}" target="_blank" rel="noopener">{Path(m).name}</a>')
        linkline = f'<p class="links">{" · ".join(links)}</p>' if links else ""
        timeline.append(f'''    <div class="update">
      <div class="date">{u["date"]} · <a href="#area-{u["area"]}">{area_title}</a>{tag}</div>
      <h3>{md_inline(u["title"])}</h3>
      {paras}{linkline}
    </div>''')

    tpl = (HERE / "templates" / "index.template.html").read_text(encoding="utf-8")
    for key, val in {
        "EYEBROW": html.escape(config["eyebrow"]),
        "TITLE": html.escape(config["title"]),
        "SUBTITLE": html.escape(config["subtitle"]),
        "FOOTER": html.escape(config["footer"]),
        "PW_HASH": config["pw_hash"],
        "NAV": "\n    ".join(nav),
        "OVERVIEW_AIM": md_inline(config["overview_aim"]),
        "OVERVIEW_CHIPS": chips,
        "TAKE_HOMES": "\n      ".join(take_homes),
        "SECTIONS": "\n".join(sections),
        "TIMELINE": "\n".join(timeline),
        "BUILT": date.today().isoformat(),
    }.items():
        tpl = tpl.replace("{{" + key + "}}", val)
    return tpl


# ---------------------------------------------------------------- main

def main():
    config, areas, updates = load_all()
    print(f"ok: {len(areas)} areas, {len(updates)} updates")
    if "--check" in sys.argv:
        return
    SITE.mkdir(exist_ok=True)
    (SITE / "index.html").write_text(build_html(config, areas, updates),
                                     encoding="utf-8", newline="\n")
    for sub in ("media", "demos"):
        src = HERE / sub
        if src.is_dir():
            shutil.copytree(src, SITE / sub, dirs_exist_ok=True)
    print(f"wrote {SITE / 'index.html'}")


if __name__ == "__main__":
    main()
