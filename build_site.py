#!/usr/bin/env python3
"""Build static HTML pages from copy/*.md. Run from repo root."""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COPY = ROOT / "copy"

NAV = [
    ("index.html", "Home", "nav.home"),
    ("the-name.html", "The name", "nav.name"),
    ("timeline.html", "Timeline", "nav.timeline"),
    ("ancient.html", "Ancient", "nav.ancient"),
    ("medieval.html", "Medieval", "nav.medieval"),
    ("independence.html", "To Independence", "nav.independence"),
    ("places.html", "Places", "nav.places"),
    ("sources.html", "Sources", "nav.sources"),
]

PAGES = {
    "index.md": {
        "out": "index.html",
        "title": "Kumturu — a public history of Guntur",
        "description": "A public history of Guntur for Guntur people. The name Kumturu, 669 CE, and the story of this river country to 15 August 1947.",
        "h1": "Welcome to Kumturu",
    },
    "the-name.md": {
        "out": "the-name.html",
        "title": "The name — Kumturu",
        "description": "Kumturu, 669 CE, is the earliest known epigraphical mention of Guntur. Then Gomturu / Gonturu, Gunturu, and Guntur.",
        "h1": "The name: Kumturu → Gomturu → Gunturu → Guntur",
    },
    "timeline.md": {
        "out": "timeline.html",
        "title": "Timeline — Kumturu",
        "description": "Dated claims for Guntur, from palaeolithic tools to the morning of 15 August 1947.",
        "h1": "Timeline",
    },
    "ancient.md": {
        "out": "ancient.html",
        "title": "Ancient Guntur — Kumturu",
        "description": "The Krishna tract, Bhattiprolu, Amaravati, Chebrolu, the Ikshvakus, Undavalli, and the first writing of Kumturu.",
        "h1": "Ancient Guntur",
    },
    "medieval.md": {
        "out": "medieval.html",
        "title": "Medieval Guntur — Kumturu",
        "description": "Velanadu, Palnadu, the Kakatiyas, Kondavidu, Krishnadevaraya on 23 June 1515, and Golconda to 1687.",
        "h1": "Medieval Guntur",
    },
    "independence.md": {
        "out": "independence.html",
        "title": "To Independence — Kumturu",
        "description": "Circars, the French headquarters, the Company, the district, and the walk to 15 August 1947.",
        "h1": "To Independence",
    },
    "places.md": {
        "out": "places.html",
        "title": "Places — Kumturu",
        "description": "Short cards for Bhattiprolu, Amaravati, Chebrolu, Undavalli, Nagarjunakonda, Palnadu, Kondavidu, and Guntur town.",
        "h1": "Places",
    },
    "sources.md": {
        "out": "sources.html",
        "title": "Sources — Kumturu",
        "description": "Books, stones, gazetteers, and the 2026 ASI reading of the Pune plates behind this public history of Guntur.",
        "h1": "Sources",
    },
}

MD_LINKS = {
    "the-name.md": "the-name.html",
    "timeline.md": "timeline.html",
    "ancient.md": "ancient.html",
    "medieval.md": "medieval.html",
    "independence.md": "independence.html",
    "places.md": "places.html",
    "sources.md": "sources.html",
}

VIDEO_CAPTION = "An impression of river-country life, not an archive film."


def inline(text: str) -> str:
    # Protect links first
    links: list[str] = []

    def store_link(m: re.Match) -> str:
        label, href = m.group(1), m.group(2)
        href = MD_LINKS.get(href, href)
        links.append(
            f'<a href="{html.escape(href, quote=True)}">{inline_simple(label)}</a>'
        )
        return f"\x00L{len(links) - 1}\x00"

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", store_link, text)

    urls: list[str] = []

    def store_url(m: re.Match) -> str:
        url = m.group(0)
        urls.append(f'<a href="{html.escape(url, quote=True)}">{html.escape(url)}</a>')
        return f"\x00U{len(urls) - 1}\x00"

    text = re.sub(r"https?://[^\s<>]+", store_url, text)
    text = inline_simple(text)
    text = re.sub(r"\x00L(\d+)\x00", lambda m: links[int(m.group(1))], text)
    text = re.sub(r"\x00U(\d+)\x00", lambda m: urls[int(m.group(1))], text)
    return text


def inline_simple(text: str) -> str:
    parts: list[str] = []
    pos = 0
    pattern = re.compile(r"\*\*\*(.+?)\*\*\*|\*\*(.+?)\*\*|\*(.+?)\*|`([^`]+)`")
    for m in pattern.finditer(text):
        parts.append(html.escape(text[pos : m.start()]))
        if m.group(1) is not None:
            parts.append(f"<strong><em>{html.escape(m.group(1))}</em></strong>")
        elif m.group(2) is not None:
            parts.append(f"<strong>{html.escape(m.group(2))}</strong>")
        elif m.group(3) is not None:
            parts.append(f"<em>{html.escape(m.group(3))}</em>")
        else:
            parts.append(f"<code>{html.escape(m.group(4))}</code>")
        pos = m.end()
    parts.append(html.escape(text[pos:]))
    return "".join(parts)


def split_table_row(line: str) -> list[str]:
    line = line.strip().strip("|")
    return [c.strip() for c in line.split("|")]


def is_sep(row: list[str]) -> bool:
    return all(re.fullmatch(r":?-{3,}:?", c or "") for c in row)


def film_band(src: str, extra_class: str = "") -> str:
    cls = "film-band" + (f" {extra_class}" if extra_class else "")
    return f"""<figure class="{cls}">
  <div class="film-frame">
    <video muted loop playsinline autoplay preload="metadata" disablepictureinpicture>
      <source src="{src}" type="video/mp4">
    </video>
  </div>
  <figcaption>{VIDEO_CAPTION}</figcaption>
</figure>"""


PLATES = """<div class="plates">
<figure class="plate">
  <img src="media/plates-seal.jpg" alt="Circular metal seal of the Pune plates: a crescent above a line of raised script and a lotus below, on a weathered copper face." width="800" height="800">
  <figcaption>Circular seal of the three-leaf charter: lotus, crescent, and the legend <em>Sri Vishamasiddhi</em>. News photograph of a privately held plate (Ameet Lomte, Pune), read by ASI Director (Epigraphy) K. Munirathnam Reddy. Not an excavation of this site, and not a published plate edition.</figcaption>
</figure>
<figure class="plate">
  <img src="media/plates-leaf.jpg" alt="A rectangular copper leaf with five lines of incised Telugu-Kannada script and a circular binding hole at the left." width="1200" height="800">
  <figcaption>A copper leaf of the same privately held set. A line is marked in the source photograph. Held by Ameet Lomte, Pune; reading by ASI Director (Epigraphy) K. Munirathnam Reddy. News / social-media photograph, August 2026.</figcaption>
</figure>
<figure class="plate">
  <img src="media/plates-set.jpg" alt="A copper plate on a ring, with five lines of script and one passage underlined in the source photograph." width="1200" height="800">
  <figcaption>The bound set: leaves on a ring, one line underlined in the source post. Privately held plates (Ameet Lomte, Pune), read by ASI Director (Epigraphy) K. Munirathnam Reddy. These photographs are not a published edition of the inner grant.</figcaption>
</figure>
</div>"""


def render_blocks(md: str, page_key: str) -> str:
    lines = md.splitlines()
    # drop first ATX title
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    while lines and not lines[0].strip():
        lines = lines[1:]

    out: list[str] = []
    i = 0
    n = len(lines)
    h2_count = 0

    def flush_paras(buf: list[str]) -> None:
        if buf:
            out.append("<p>" + inline(" ".join(buf)) + "</p>")
            buf.clear()

    para: list[str] = []

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("|") and i + 1 < n and stripped.count("|") >= 2:
            flush_paras(para)
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(split_table_row(lines[i]))
                i += 1
            if len(rows) >= 2 and is_sep(rows[1]):
                header, body = rows[0], rows[2:]
            else:
                header, body = [], rows
            empty_header = header and all(not c for c in header)
            classes = []
            if page_key == "timeline.md":
                classes.append("timeline")
            if empty_header or page_key == "the-name.md":
                classes.append("facts")
            cls = f' class="{" ".join(classes)}"' if classes else ""
            html_rows = ['<div class="table-wrap">', f"<table{cls}>"]
            if header and not empty_header:
                html_rows.append("<thead><tr>")
                html_rows.extend(f"<th>{inline(c)}</th>" for c in header)
                html_rows.append("</tr></thead>")
            html_rows.append("<tbody>")
            for row in body:
                html_rows.append("<tr>")
                if empty_header or (page_key == "the-name.md" and len(row) == 2):
                    html_rows.append(f"<th scope=\"row\">{inline(row[0])}</th>")
                    html_rows.extend(f"<td>{inline(c)}</td>" for c in row[1:])
                else:
                    html_rows.extend(f"<td>{inline(c)}</td>" for c in row)
                html_rows.append("</tr>")
            html_rows.append("</tbody></table></div>")
            out.append("".join(html_rows))
            continue

        if stripped.startswith("<figure"):
            flush_paras(para)
            block = [line]
            i += 1
            while i < n and "</figure>" not in block[-1]:
                block.append(lines[i])
                i += 1
            out.append("\n".join(block))
            continue

        if stripped.startswith("## "):
            flush_paras(para)
            title = stripped[3:]
            h2_count += 1
            if page_key == "index.md" and h2_count == 2:
                out.append(film_band("media/01-village-road.mp4", "breakout"))
            if page_key == "index.md" and h2_count == 3:
                out.append(film_band("media/04-krishna-country.mp4", "breakout"))
            if page_key == "ancient.md" and title == "The Eastern Chalukyas, and the first writing of the name":
                out.append(film_band("media/02-vengi-court.mp4", "breakout"))
            if page_key == "medieval.md" and title == "The Reddis and Kondavidu":
                out.append(film_band("media/03-kondavidu.mp4", "breakout"))
            hid = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
            out.append(f'<h2 id="{html.escape(hid, quote=True)}">{inline(title)}</h2>')
            i += 1
            continue

        if stripped.startswith("### "):
            flush_paras(para)
            title = stripped[4:]
            hid = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
            out.append(f'<h3 id="{html.escape(hid, quote=True)}">{inline(title)}</h3>')
            i += 1
            continue

        if stripped.startswith("- "):
            flush_paras(para)
            items = []
            while i < n and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:])
                i += 1
            cls = "page-list" if page_key == "index.md" else "biblio" if page_key == "sources.md" else ""
            attr = f' class="{cls}"' if cls else ""
            out.append(f"<ul{attr}>")
            out.extend(f"<li>{inline(item)}</li>" for item in items)
            out.append("</ul>")
            continue

        if not stripped:
            flush_paras(para)
            i += 1
            continue

        para.append(stripped)
        i += 1

    flush_paras(para)
    return "\n".join(out)


def wrap_places(body: str) -> str:
    # Turn each h2 + following block into a card; keep the intro paragraph outside.
    parts = re.split(r'(<h2 id="[^"]+">)', body, maxsplit=1)
    if len(parts) < 3:
        return body
    intro, rest_start, rest = parts[0], parts[1], parts[2]
    rest = rest_start + rest
    chunks = re.split(r'(<h2 id="[^"]+">.*?</h2>)', rest)
    cards = []
    i = 1
    while i < len(chunks):
        heading = chunks[i]
        content = chunks[i + 1] if i + 1 < len(chunks) else ""
        cards.append(f'<article class="place-card">{heading}{content}</article>')
        i += 2
    return intro + '<div class="places">' + "".join(cards) + "</div>"


def header(current: str) -> str:
    items = []
    for href, label, key in NAV:
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'<li><a href="{href}"{cur} data-i18n="{key}">{label}</a></li>')
    nav = "\n          ".join(items)
    return f"""<header class="masthead">
  <div class="masthead-inner">
    <div class="brand">
      <a class="brand-name" href="index.html">Kumturu</a>
      <span class="brand-tag" data-i18n="brand.tag">A public history of Guntur</span>
    </div>
    <nav aria-label="Site">
      <ul class="site-nav">
          {nav}
      </ul>
    </nav>
    <div class="lang-toggle" role="group" aria-label="Language">
      <button type="button" class="lang-btn is-current" data-lang="en" aria-pressed="true">English</button>
      <button type="button" class="lang-btn" data-lang="te" aria-pressed="false" title="Telugu not yet available" aria-description="Telugu not yet available">తెలుగు</button>
    </div>
    <p class="lang-note" hidden>Telugu is being written. This site is in English for now.</p>
  </div>
</header>"""


def footer(current: str) -> str:
    items = []
    for href, label, key in NAV:
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'<li><a href="{href}"{cur} data-i18n="{key}">{label}</a></li>')
    nav = "\n        ".join(items)
    return f"""<footer class="colophon">
  <div class="colophon-inner">
    <nav aria-label="Footer">
      <ul class="foot-nav">
        {nav}
      </ul>
    </nav>
    <p data-i18n="footer.stop">The story stops on the morning of 15 August 1947. Andhra State, 1953, is beyond this site.</p>
    <p data-i18n="footer.credit">kumturu.com · kumuturu.com · Written for Guntur people. Nothing here is invented.</p>
  </div>
</footer>"""


def page_shell(meta: dict, body: str, extra_class: str = "") -> str:
    current = meta["out"]
    wrap_cls = "wrap wide" if extra_class else "wrap"
    hero = ""
    if current == "index.html":
        hero = """<header class="hero">
      <p class="kicker">Kumturu · 669 CE</p>
      <h1>Welcome to Kumturu</h1>
      <p class="chain">Kumturu → Gomturu / Gonturu → Gunturu → Guntur</p>
    </header>"""
        # body already starts after the dropped h1; first paras are the welcome
    else:
        hero = f"""<header class="hero">
      <h1 class="page-title">{html.escape(meta["h1"])}</h1>
    </header>"""

    # closing italic on home: last paragraph after the list
    if current == "index.html":
        body = body.replace(
            "<p>Welcome. The name is old. The river is older. The people were here before either was written down.</p>",
            '<p class="closing">Welcome. The name is old. The river is older. The people were here before either was written down.</p>',
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(meta["title"])}</title>
  <meta name="description" content="{html.escape(meta["description"])}">
  <link rel="canonical" href="https://kumturu.com/{'' if current == 'index.html' else current}">
  <link rel="stylesheet" href="site.css">
</head>
<body>
  <a class="skip" href="#content" data-i18n="skip">Skip to the history</a>
  {header(current)}
  <main id="content" class="{wrap_cls}">
    {hero}
    <div class="prose">
{body}
    </div>
  </main>
  {footer(current)}
  <script src="js/i18n.js"></script>
  <script>
    document.querySelectorAll(".film-frame video").forEach(function (video) {{
      var hide = function () {{ video.classList.remove("is-ready"); }};
      video.addEventListener("loadeddata", function () {{
        if (video.readyState >= 2 && video.videoWidth) video.classList.add("is-ready");
      }});
      video.addEventListener("error", hide);
      video.querySelectorAll("source").forEach(function (source) {{
        source.addEventListener("error", hide);
      }});
      var play = video.play();
      if (play && play.catch) play.catch(function () {{}});
    }});
  </script>
</body>
</html>
"""


def main() -> None:
    for md_name, meta in PAGES.items():
        raw = (COPY / md_name).read_text(encoding="utf-8")
        body = render_blocks(raw, md_name)
        extra = ""
        if md_name == "the-name.md":
            extra = "wide"
            marker = "The name, the king, the year, and the seal are what the 2026 briefing placed in public view.</p>"
            if marker in body:
                body = body.replace(marker, marker + "\n" + PLATES, 1)
        if md_name == "places.md":
            body = wrap_places(body)
            extra = "wide"
        if md_name == "timeline.md":
            extra = "wide"
        if md_name == "sources.md":
            extra = "wide"
        html_out = page_shell(meta, body, extra)
        dest = ROOT / meta["out"]
        dest.write_text(html_out, encoding="utf-8")
        print("wrote", dest.name)


if __name__ == "__main__":
    main()
