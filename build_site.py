#!/usr/bin/env python3
"""Build static HTML pages from copy/*.md and copy/te/*.md. Run from repo root."""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COPY = ROOT / "copy"

NAV_EN = [
    ("index.html", "Home"),
    ("the-name.html", "The name"),
    ("timeline.html", "Timeline"),
    ("ancient.html", "Ancient"),
    ("medieval.html", "Medieval"),
    ("independence.html", "To Independence"),
    ("places.html", "Places"),
    ("sources.html", "Sources"),
]

NAV_TE = [
    ("index.html", "\u0c38\u0c4d\u0c35\u0c3e\u0c17\u0c24\u0c02"),
    ("the-name.html", "\u0c2a\u0c47\u0c30\u0c41"),
    ("timeline.html", "\u0c15\u0c3e\u0c32\u0c15\u0c4d\u0c30\u0c2e\u0c02"),
    ("ancient.html", "\u0c2a\u0c4d\u0c30\u0c3e\u0c1a\u0c40\u0c28\u0c2e\u0c48\u0c28\u0c26\u0c3f"),
    ("medieval.html", "\u0c2e\u0c27\u0c4d\u0c2f\u0c2f\u0c41\u0c17\u0c02"),
    ("independence.html", "\u0c38\u0c4d\u0c35\u0c3e\u0c24\u0c02\u0c24\u0c4d\u0c30\u0c4d\u0c2f\u0c3e\u0c28\u0c3f\u0c15\u0c3f"),
    ("places.html", "\u0c2a\u0c4d\u0c30\u0c26\u0c47\u0c36\u0c3e\u0c32\u0c41"),
    ("sources.html", "\u0c2e\u0c42\u0c32\u0c3e\u0c32\u0c41"),
]

PAGES_EN = {
    "index.md": {
        "out": "index.html",
        "title": "Kumturu \u2014 a public history of Guntur, India",
        "description": "A public history of Guntur, a city in Andhra Pradesh, India. The name Kumturu, 669 CE, and the story of this river country to 15 August 1947.",
        "h1": "Welcome to Kumturu",
    },
    "the-name.md": {
        "out": "the-name.html",
        "title": "The name \u2014 Kumturu, Guntur, India",
        "description": "Kumturu, 669 CE, is the earliest known epigraphical mention of Guntur, India. Then Gomturu / Gonturu, Gunturu, and Guntur.",
        "h1": "The name: Kumturu \u2192 Gomturu \u2192 Gunturu \u2192 Guntur",
    },
    "timeline.md": {
        "out": "timeline.html",
        "title": "Timeline \u2014 Kumturu, Guntur, India",
        "description": "Dated claims for Guntur, Andhra Pradesh, India, from palaeolithic tools to the morning of 15 August 1947.",
        "h1": "Timeline",
    },
    "ancient.md": {
        "out": "ancient.html",
        "title": "Ancient Guntur, India \u2014 Kumturu",
        "description": "The Krishna tract in Andhra Pradesh, India: Bhattiprolu, Amaravati, Chebrolu, the Ikshvakus, Undavalli, and the first writing of Kumturu.",
        "h1": "Ancient Guntur",
    },
    "medieval.md": {
        "out": "medieval.html",
        "title": "Medieval Guntur, India \u2014 Kumturu",
        "description": "Velanadu, Palnadu, the Kakatiyas, Kondavidu, Krishnadevaraya on 23 June 1515, and Golconda to 1687, in historic Guntur, India.",
        "h1": "Medieval Guntur",
    },
    "independence.md": {
        "out": "independence.html",
        "title": "To Independence \u2014 Kumturu, Guntur, India",
        "description": "Circars, the French headquarters, the Company, the district, and the walk to 15 August 1947 in Guntur, India.",
        "h1": "To Independence",
    },
    "places.md": {
        "out": "places.html",
        "title": "Places \u2014 Kumturu, Guntur, India",
        "description": "Short cards for Bhattiprolu, Amaravati, Chebrolu, Undavalli, Nagarjunakonda, Palnadu, Kondavidu, and Guntur town, India.",
        "h1": "Places",
    },
    "sources.md": {
        "out": "sources.html",
        "title": "Sources \u2014 Kumturu, Guntur, India",
        "description": "Books, stones, gazetteers, and the 2026 ASI reading of the Pune plates behind this public history of Guntur, India.",
        "h1": "Sources",
    },
}

PAGES_TE = {
    "index.md": {
        "out": "te/index.html",
        "title": "Kumturu \u2014 \u0c17\u0c41\u0c02\u0c1f\u0c42\u0c30\u0c41, India",
        "description": "A public history of Guntur, a city in Andhra Pradesh, India, in Telugu. The name Kumturu, 669 CE, and the story of this river country to 15 August 1947.",
        "h1": "\u0c38\u0c4d\u0c35\u0c3e\u0c17\u0c24\u0c02 Kumturu",
    },
    "the-name.md": {
        "out": "te/the-name.html",
        "title": "\u0c2a\u0c47\u0c30\u0c41 \u2014 Kumturu, \u0c17\u0c41\u0c02\u0c1f\u0c42\u0c30\u0c41, India",
        "description": "Kumturu, 669 CE, is the earliest known epigraphical mention of Guntur, India. Then Gomturu / Gonturu, Gunturu, and Guntur.",
        "h1": "\u0c2a\u0c47\u0c30\u0c41: Kumturu \u2192 Gomturu \u2192 Gunturu \u2192 \u0c17\u0c41\u0c02\u0c1f\u0c42\u0c30\u0c41",
    },
    "timeline.md": {
        "out": "te/timeline.html",
        "title": "\u0c15\u0c3e\u0c32\u0c15\u0c4d\u0c30\u0c2e\u0c02 \u2014 Kumturu, \u0c17\u0c41\u0c02\u0c1f\u0c42\u0c30\u0c41, India",
        "description": "Dated claims for Guntur, Andhra Pradesh, India, from palaeolithic tools to the morning of 15 August 1947.",
        "h1": "\u0c15\u0c3e\u0c32\u0c15\u0c4d\u0c30\u0c2e\u0c02",
    },
    "ancient.md": {
        "out": "te/ancient.html",
        "title": "\u0c2a\u0c4d\u0c30\u0c3e\u0c1a\u0c40\u0c28 \u0c17\u0c41\u0c02\u0c1f\u0c42\u0c30\u0c41, India \u2014 Kumturu",
        "description": "The Krishna tract in Andhra Pradesh, India: Bhattiprolu, Amaravati, Chebrolu, the Ikshvakus, Undavalli, and the first writing of Kumturu.",
        "h1": "\u0c2a\u0c4d\u0c30\u0c3e\u0c1a\u0c40\u0c28 \u0c17\u0c41\u0c02\u0c1f\u0c42\u0c30\u0c41",
    },
    "medieval.md": {
        "out": "te/medieval.html",
        "title": "\u0c2e\u0c27\u0c4d\u0c2f\u0c2f\u0c41\u0c17 \u0c17\u0c41\u0c02\u0c1f\u0c42\u0c30\u0c41, India \u2014 Kumturu",
        "description": "Velanadu, Palnadu, the Kakatiyas, Kondavidu, Krishnadevaraya on 23 June 1515, and Golconda to 1687, in historic Guntur, India.",
        "h1": "\u0c2e\u0c27\u0c4d\u0c2f\u0c2f\u0c41\u0c17 \u0c17\u0c41\u0c02\u0c1f\u0c42\u0c30\u0c41",
    },
    "independence.md": {
        "out": "te/independence.html",
        "title": "\u0c38\u0c4d\u0c35\u0c3e\u0c24\u0c02\u0c24\u0c4d\u0c30\u0c4d\u0c2f\u0c3e\u0c28\u0c3f\u0c15\u0c3f \u2014 Kumturu, \u0c17\u0c41\u0c02\u0c1f\u0c42\u0c30\u0c41, India",
        "description": "Circars, the French headquarters, the Company, the district, and the walk to 15 August 1947 in Guntur, India.",
        "h1": "\u0c38\u0c4d\u0c35\u0c3e\u0c24\u0c02\u0c24\u0c4d\u0c30\u0c4d\u0c2f\u0c3e\u0c28\u0c3f\u0c15\u0c3f",
    },
    "places.md": {
        "out": "te/places.html",
        "title": "\u0c2a\u0c4d\u0c30\u0c26\u0c47\u0c36\u0c3e\u0c32\u0c41 \u2014 Kumturu, \u0c17\u0c41\u0c02\u0c1f\u0c42\u0c30\u0c41, India",
        "description": "Short cards for Bhattiprolu, Amaravati, Chebrolu, Undavalli, Nagarjunakonda, Palnadu, Kondavidu, and Guntur town, India.",
        "h1": "\u0c2a\u0c4d\u0c30\u0c26\u0c47\u0c36\u0c3e\u0c32\u0c41",
    },
    "sources.md": {
        "out": "te/sources.html",
        "title": "\u0c2e\u0c42\u0c32\u0c3e\u0c32\u0c41 \u2014 Kumturu, \u0c17\u0c41\u0c02\u0c1f\u0c42\u0c30\u0c41, India",
        "description": "Books, stones, gazetteers, and the 2026 ASI reading of the Pune plates behind this public history of Guntur, India.",
        "h1": "\u0c2e\u0c42\u0c32\u0c3e\u0c32\u0c41",
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

STILL_CAPTION = "An impression of river-country life, not an archive film."
BRAND_TAG = "A public history of Guntur, India"
LOCATOR_EN = "Guntur, Andhra Pradesh, India. South bank of the Krishna."
LOCATOR_TE = "\u0c17\u0c41\u0c02\u0c1f\u0c42\u0c30\u0c41, Andhra Pradesh, India. South bank of the Krishna."

STILLS = {
    "village": ("media/01-village-road.png", "Bullock carts on a village road beside a tank and palms, a rocky hill beyond, in the Krishna country of Guntur, India."),
    "vengi": ("media/02-vengi-court.png", "An impression of an Eastern Chalukya court at Vengi."),
    "kondavidu": ("media/03-kondavidu.png", "An impression of the Kondavidu hill forts west of Guntur, India."),
    "krishna": ("media/04-krishna-country.png", "An impression of Krishna-country river land on the south bank, Guntur, India."),
    "bhattiprolu": ("media/05-bhattiprolu.png", "Brick stupa at Bhattiprolu among palms and paddy at low sun."),
    "tenali": ("media/06-tenali-1942.png", "An impression of Tenali in 1942."),
}

FILM_HEADINGS = {
    "Bhattiprolu and king Kuberaka": "bhattiprolu",
    "Bhattiprolu \u0c2e\u0c30\u0c3f\u0c2f\u0c41 \u0c30\u0c3e\u0c1c\u0c41 Kuberaka": "bhattiprolu",
    "The Eastern Chalukyas, and the first writing of the name": "vengi",
    "\u0c24\u0c42\u0c30\u0c4d\u0c2a\u0c41 Chalukyas, \u0c2e\u0c30\u0c3f\u0c2f\u0c41 \u0c2a\u0c47\u0c30\u0c41 \u0c2f\u0c4a\u0c15\u0c4d\u0c15 \u0c2e\u0c4a\u0c26\u0c1f\u0c3f \u0c30\u0c1a\u0c28": "vengi",
    "The Reddis and Kondavidu": "kondavidu",
    "\u0c30\u0c46\u0c21\u0c4d\u0c21\u0c40\u0c32\u0c41 \u0c2e\u0c30\u0c3f\u0c2f\u0c41 Kondavidu": "kondavidu",
    "Tenali, 12 August 1942": "tenali",
}


def inline(text: str) -> str:
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


def film_band(key: str, extra_class: str = "", prefix: str = "") -> str:
    src, alt = STILLS[key]
    cls = "film-band" + (f" {extra_class}" if extra_class else "")
    return f"""<figure class="{cls}">
  <div class="film-frame">
    <img src="{prefix}{src}" alt="{html.escape(alt, quote=True)}" width="1536" height="1024">
  </div>
  <figcaption>{STILL_CAPTION}</figcaption>
</figure>"""


def plates(prefix: str = "") -> str:
    return f"""<div class="plates">
<figure class="plate">
  <img src="{prefix}media/plates-seal.jpg" alt="Circular metal seal of the Pune plates: a crescent above a line of raised script and a lotus below, on a plain field." width="800" height="800">
  <figcaption>Circular seal of the three-leaf charter: lotus, crescent, and the legend <em>Sri Vishamasiddhi</em>. News photograph of a privately held plate (Ameet Lomte, Pune), read by ASI Director (Epigraphy) K. Munirathnam Reddy. Not an excavation of this site, and not a published plate edition.</figcaption>
</figure>
<figure class="plate">
  <img src="{prefix}media/plates-leaf.jpg" alt="A rectangular copper leaf with five lines of incised Telugu-Kannada script and a circular binding hole at the left." width="1200" height="800">
  <figcaption>A copper leaf of the same privately held set. A line is marked in the source photograph. Held by Ameet Lomte, Pune; reading by ASI Director (Epigraphy) K. Munirathnam Reddy. News / social-media photograph, August 2026.</figcaption>
</figure>
<figure class="plate">
  <img src="{prefix}media/plates-set.jpg" alt="A copper plate on a ring, with five lines of script and one passage underlined in the source photograph." width="1200" height="800">
  <figcaption>The bound set: leaves on a ring, one line underlined in the source post. Privately held plates (Ameet Lomte, Pune), read by ASI Director (Epigraphy) K. Munirathnam Reddy. These photographs are not a published edition of the inner grant.</figcaption>
</figure>
</div>"""


def coins(prefix: str = "") -> str:
    credit = "Sada coins: Vaddamanu excavations (BACRI) and British Museum; photographs as published by Shailendra Bhandare, 2016."
    return f"""<div class="coins">
<figure class="plate">
  <img src="{prefix}media/coin-maha-sada.jpg" alt="Lead coin of Maha Sada, obverse and reverse, from the Vaddamanu excavations." width="346" height="185">
  <figcaption>Maha Sada. Lead. Vaddamanu excavations (BACRI).</figcaption>
</figure>
<figure class="plate">
  <img src="{prefix}media/coin-siri-sada.jpg" alt="Lead coin of Siri Sada, obverse and reverse." width="347" height="182">
  <figcaption>Siri Sada. Lead. Photograph as published by Shailendra Bhandare, 2016.</figcaption>
</figure>
<figure class="plate">
  <img src="{prefix}media/coin-asaka-sada.jpg" alt="Lead coin of Asaka Sada, obverse and reverse, British Museum." width="345" height="162">
  <figcaption>Asaka Sada. Lead. British Museum.</figcaption>
</figure>
<p class="note coin-credit">{html.escape(credit)}</p>
</div>"""


def render_blocks(md: str, page_key: str, prefix: str = "") -> str:
    lines = md.splitlines()
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
                    html_rows.append(f'<th scope="row">{inline(row[0])}</th>')
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
            fig = "\n".join(block)
            if prefix:
                fig = fig.replace('src="media/', f'src="{prefix}media/')
            out.append(fig)
            continue

        if stripped.startswith("## "):
            flush_paras(para)
            title = stripped[3:]
            h2_count += 1
            if page_key == "index.md" and h2_count == 2:
                out.append(film_band("village", "breakout", prefix))
            if page_key == "index.md" and h2_count == 3:
                out.append(film_band("krishna", "breakout", prefix))
            still_key = FILM_HEADINGS.get(title)
            if still_key:
                out.append(film_band(still_key, "breakout", prefix))
            hid = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
            if not hid:
                hid = f"section-{h2_count}"
            out.append(f'<h2 id="{html.escape(hid, quote=True)}">{inline(title)}</h2>')
            i += 1
            continue

        if stripped.startswith("### "):
            flush_paras(para)
            title = stripped[4:]
            hid = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
            if not hid:
                hid = "section"
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


def lang_switch(leaf: str, lang: str) -> str:
    if lang == "te":
        en_href = f"../{leaf}"
        te_href = leaf
        en_cur, te_cur = "", ' aria-current="true"'
    else:
        en_href = leaf
        te_href = f"te/{leaf}"
        en_cur, te_cur = ' aria-current="true"', ""
    return f"""<nav class="lang-switch" aria-label="Language">
      <a href="{en_href}" lang="en" hreflang="en" data-set-lang="en"{en_cur}>EN</a>
      <span aria-hidden="true">|</span>
      <a href="{te_href}" lang="te" hreflang="te" data-set-lang="te"{te_cur}>\u0c24\u0c46\u0c32\u0c41\u0c17\u0c41</a>
    </nav>"""


def header(current_leaf: str, lang: str) -> str:
    nav_items = NAV_TE if lang == "te" else NAV_EN
    items = []
    for href, label in nav_items:
        cur = ' aria-current="page"' if href == current_leaf else ""
        items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    nav = "\n          ".join(items)
    return f"""<header class="masthead">
  <div class="masthead-inner">
    <div class="masthead-top">
      <div class="brand">
        <a class="brand-name" href="index.html">Kumturu</a>
        <span class="brand-tag">{BRAND_TAG}</span>
      </div>
      {lang_switch(current_leaf, lang)}
    </div>
    <nav aria-label="Site">
      <ul class="site-nav">
          {nav}
      </ul>
    </nav>
  </div>
</header>"""


def footer(current_leaf: str, lang: str) -> str:
    nav_items = NAV_TE if lang == "te" else NAV_EN
    items = []
    for href, label in nav_items:
        cur = ' aria-current="page"' if href == current_leaf else ""
        items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    nav = "\n        ".join(items)
    return f"""<footer class="colophon">
  <div class="colophon-inner">
    <nav aria-label="Footer">
      <ul class="foot-nav">
        {nav}
      </ul>
    </nav>
    <p>The story stops on the morning of 15 August 1947. Andhra State, 1953, is beyond this site.</p>
    <p>kumturu.com \u00b7 kumuturu.com \u00b7 A public history of Guntur, India. Nothing here is invented.</p>
  </div>
</footer>"""


def lang_script() -> str:
    return """  <script>
    (function () {
      var KEY = "kumturu-lang";
      var here = document.documentElement.lang === "te" ? "te" : "en";
      document.querySelectorAll("[data-set-lang]").forEach(function (a) {
        a.addEventListener("click", function () {
          try { localStorage.setItem(KEY, a.getAttribute("data-set-lang")); } catch (e) {}
        });
      });
      try {
        var pref = localStorage.getItem(KEY);
        if (pref && (pref === "en" || pref === "te") && pref !== here) {
          var dest = document.querySelector('[data-set-lang="' + pref + '"]');
          if (dest) {
            var href = dest.getAttribute("href");
            if (href && !sessionStorage.getItem("kumturu-lang-applied")) {
              sessionStorage.setItem("kumturu-lang-applied", "1");
              location.replace(href);
            }
          }
        }
      } catch (e) {}
    })();
  </script>"""


def page_shell(meta: dict, body: str, extra_class: str = "", lang: str = "en") -> str:
    current = meta["out"]
    leaf = Path(current).name
    prefix = "../" if lang == "te" else ""
    wrap_cls = "wrap wide" if extra_class else "wrap"
    css = f"{prefix}site.css"
    if leaf == "index.html":
        if lang == "te":
            canon = "te/"
            h1 = meta["h1"]
            locator = LOCATOR_TE
        else:
            canon = ""
            h1 = "Welcome to Kumturu"
            locator = LOCATOR_EN
        hero = f"""<header class="hero">
      <p class="kicker">Kumturu \u00b7 669 CE</p>
      <h1>{html.escape(h1)}</h1>
      <p class="locator">{html.escape(locator)}</p>
      <p class="chain">Kumturu \u2192 Gomturu / Gonturu \u2192 Gunturu \u2192 Guntur</p>
    </header>"""
    else:
        canon = current if not current.endswith("index.html") else ("te/" if lang == "te" else "")
        hero = f"""<header class="hero">
      <h1 class="page-title">{html.escape(meta["h1"])}</h1>
    </header>"""

    en_close = "<p>Welcome. The name is old. The river is older. The people were here before either was written down.</p>"
    te_close = "<p>\u0c38\u0c4d\u0c35\u0c3e\u0c17\u0c24\u0c02. \u0c2a\u0c47\u0c30\u0c41 \u0c2a\u0c3e\u0c24\u0c26\u0c3f. \u0c28\u0c26\u0c3f \u0c2a\u0c3e\u0c24\u0c26\u0c3f. \u0c0f\u0c26\u0c48\u0c28\u0c3e \u0c35\u0c4d\u0c30\u0c3e\u0c2f\u0c2c\u0c21\u0c1f\u0c3e\u0c28\u0c3f\u0c15\u0c3f \u0c2e\u0c41\u0c02\u0c26\u0c41 \u0c2a\u0c4d\u0c30\u0c1c\u0c32\u0c41 \u0c07\u0c15\u0c4d\u0c15\u0c21 \u0c09\u0c28\u0c4d\u0c28\u0c3e\u0c30\u0c41.</p>"
    if leaf == "index.html":
        body = body.replace(en_close, '<p class="closing">Welcome. The name is old. The river is older. The people were here before either was written down.</p>')
        body = body.replace(te_close, '<p class="closing">\u0c38\u0c4d\u0c35\u0c3e\u0c17\u0c24\u0c02. \u0c2a\u0c47\u0c30\u0c41 \u0c2a\u0c3e\u0c24\u0c26\u0c3f. \u0c28\u0c26\u0c3f \u0c2a\u0c3e\u0c24\u0c26\u0c3f. \u0c0f\u0c26\u0c48\u0c28\u0c3e \u0c35\u0c4d\u0c30\u0c3e\u0c2f\u0c2c\u0c21\u0c1f\u0c3e\u0c28\u0c3f\u0c15\u0c3f \u0c2e\u0c41\u0c02\u0c26\u0c41 \u0c2a\u0c4d\u0c30\u0c1c\u0c32\u0c41 \u0c07\u0c15\u0c4d\u0c15\u0c21 \u0c09\u0c28\u0c4d\u0c28\u0c3e\u0c30\u0c41.</p>')

    alt_en = f"https://kumturu.com/{'' if leaf == 'index.html' else leaf}"
    alt_te = f"https://kumturu.com/te/{'' if leaf == 'index.html' else leaf}"

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(meta["title"])}</title>
  <meta name="description" content="{html.escape(meta["description"])}">
  <link rel="canonical" href="https://kumturu.com/{canon}">
  <link rel="alternate" hreflang="en" href="{alt_en}">
  <link rel="alternate" hreflang="te" href="{alt_te}">
  <link rel="stylesheet" href="{css}">
</head>
<body>
  <a class="skip" href="#content">Skip to the history</a>
  {header(leaf, lang)}
  <main id="content" class="{wrap_cls}">
    {hero}
    <div class="prose">
{body}
    </div>
  </main>
  {footer(leaf, lang)}
{lang_script()}
</body>
</html>
"""


def build_lang(pages: dict, copy_dir: Path, lang: str) -> None:
    prefix = "../" if lang == "te" else ""
    for md_name, meta in pages.items():
        raw = (copy_dir / md_name).read_text(encoding="utf-8")
        body = render_blocks(raw, md_name, prefix)
        extra = ""
        if md_name == "the-name.md":
            extra = "wide"
            for marker in (
                "The name, the king, the year, and the seal are what the 2026 briefing placed in public view.</p>",
                "\u0c2a\u0c47\u0c30\u0c41, \u0c30\u0c3e\u0c1c\u0c41, \u0c38\u0c02\u0c35\u0c24\u0c4d\u0c38\u0c30\u0c02 \u0c2e\u0c30\u0c3f\u0c2f\u0c41 \u0c2e\u0c41\u0c26\u0c4d\u0c30 2026 \u0c2c\u0c4d\u0c30\u0c40\u0c2b\u0c3f\u0c02\u0c17\u0c4d \u0c2a\u0c4d\u0c30\u0c1c\u0c32 \u0c26\u0c43\u0c37\u0c4d\u0c1f\u0c3f\u0c32\u0c4b \u0c09\u0c02\u0c1a\u0c3f\u0c02\u0c26\u0c3f.</p>",
            ):
                if marker in body:
                    body = body.replace(marker, marker + "\n" + plates(prefix), 1)
                    break
        if md_name == "ancient.md":
            inserted = False
            for marker in (
                "yielded coins with legends ending in <em>-Sada</em>.</p>",
                "<em>-Sada</em> \u0c24\u0c4b \u0c2e\u0c41\u0c17\u0c3f\u0c38\u0c47 \u0c2a\u0c41\u0c30\u0c3e\u0c23\u0c3e\u0c32\u0c24\u0c4b \u0c28\u0c3e\u0c23\u0c47\u0c32\u0c41 \u0c32\u0c2d\u0c3f\u0c02\u0c1a\u0c3e\u0c2f\u0c3f.</p>",
            ):
                if marker in body:
                    body = body.replace(marker, marker + "\n" + coins(prefix), 1)
                    inserted = True
                    break
            if not inserted:
                raise SystemExit(f"coin marker missing for {lang} ancient")
        if md_name == "places.md":
            body = wrap_places(body)
            extra = "wide"
        if md_name == "timeline.md":
            extra = "wide"
        if md_name == "sources.md":
            extra = "wide"
        html_out = page_shell(meta, body, extra, lang)
        dest = ROOT / meta["out"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html_out, encoding="utf-8")
        print("wrote", dest.relative_to(ROOT))


def main() -> None:
    build_lang(PAGES_EN, COPY, "en")
    build_lang(PAGES_TE, COPY / "te", "te")


if __name__ == "__main__":
    main()
