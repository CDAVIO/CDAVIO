#!/usr/bin/env python3
"""Render the animated SVG cards shown in the profile README.

Reads data/contributions.json, writes cards/*.svg.
STATIC=1 renders every card at its final frame (for screenshots).

Refresh the contribution data first with:
    python3 scripts/render_cards.py --fetch
"""
from html import escape
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))
from icons import SOCIAL  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CARDS = ROOT / "cards"
STATIC = os.environ.get("STATIC") == "1"

# Brand
BG0, BG1, BG2 = "#0c0418", "#1c0b36", "#2a0f52"
VIOLET, LAVENDER, YELLOW, WHITE, MUTED = "#6d28d9", "#c4b5fd", "#ffd905", "#ffffff", "#a99ccc"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

BASE_CSS = f"""
.s {{ font-family: {SANS}; }}
.m {{ font-family: {MONO}; }}
.rise {{ animation: rise .7s cubic-bezier(.2,.8,.2,1) both; }}
.fade {{ animation: fade .6s ease both; }}
.pop  {{ animation: pop .45s cubic-bezier(.3,1.6,.5,1) both; transform-box: fill-box; transform-origin: center; }}
@keyframes rise {{ from {{ opacity: 0; transform: translateY(18px); }} to {{ opacity: 1; transform: none; }} }}
@keyframes fade {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
@keyframes pop  {{ from {{ opacity: 0; transform: scale(.2); }} to {{ opacity: 1; transform: none; }} }}
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
"""
if STATIC:
    BASE_CSS += "* { animation: none !important; }"


def delay(seconds):
    return f'style="animation-delay:{seconds:.2f}s"'


def background(w, h, glow_x=.5):
    return f"""
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{BG0}"/><stop offset=".6" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/>
    </linearGradient>
    <radialGradient id="glow" cx="{glow_x}" cy=".45" r=".55">
      <stop offset="0" stop-color="{VIOLET}" stop-opacity=".45"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="frame"><rect width="{w}" height="{h}" rx="22"/></clipPath>
  </defs>
  <g clip-path="url(#frame)">
    <rect width="{w}" height="{h}" fill="url(#bg)"/>
    <rect width="{w}" height="{h}" fill="url(#glow)"/>"""


def svg(w, h, label, body, extra_css=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">
<style>{BASE_CSS}{extra_css}</style>
{body}
</svg>
"""


# ---------------------------------------------------------------- hero

def hero():
    """Centred name card over animated purple water (the avatar already shows the face)."""
    w, h, mid = 1200, 380, 600

    chips = ["Game dev", "Web & SaaS", "AI & Python", "Trading"]
    widths = [22 + len(label) * 10.2 for label in chips]
    x = mid - (sum(widths) + 12 * (len(chips) - 1)) / 2
    chip_svg = []
    for i, (label, cw) in enumerate(zip(chips, widths)):
        chip_svg.append(
            f'<g class="pop" {delay(1.0 + i * .12)}><rect x="{x:.0f}" y="262" width="{cw:.0f}" height="38" rx="19" '
            f'fill="#ffffff" fill-opacity=".07" stroke="{LAVENDER}" stroke-opacity=".45"/>'
            f'<text class="s" x="{x + cw / 2:.0f}" y="287" text-anchor="middle" font-size="17" font-weight="600" fill="{WHITE}">{escape(label)}</text></g>'
        )
        x += cw + 12

    shine = "" if STATIC else '<animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1.6 0;1.6 0" keyTimes="0;.45;1" dur="4.5s" begin="1.4s" repeatCount="indefinite"/>'

    def wave(fill, d, dur, reverse=False):
        move = "" if STATIC else (f'<animateTransform attributeName="transform" type="translate" from="{"-1200" if reverse else "0"} 0" '
                                  f'to="{"0" if reverse else "-1200"} 0" dur="{dur}s" repeatCount="indefinite"/>')
        return f'<path fill="url(#{fill})" d="{d}">{move}</path>'

    body = background(w, h, glow_x=.5) + f"""
    <defs>
      <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stop-color="{WHITE}"/><stop offset=".42" stop-color="{WHITE}"/>
        <stop offset=".5" stop-color="{YELLOW}"/><stop offset=".58" stop-color="{WHITE}"/><stop offset="1" stop-color="{WHITE}"/>
        {shine}
      </linearGradient>
      <linearGradient id="w1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8b5cf6" stop-opacity=".45"/><stop offset="1" stop-color="#4c1d95" stop-opacity=".12"/></linearGradient>
      <linearGradient id="w2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".6"/><stop offset="1" stop-color="#2e1065" stop-opacity=".4"/></linearGradient>
      <linearGradient id="w3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3b0f7a"/><stop offset="1" stop-color="{BG0}"/></linearGradient>
    </defs>

    <!-- copy -->
    <text class="s rise" {delay(.2)} x="{mid}" y="148" text-anchor="middle" font-size="84" font-weight="800" fill="{WHITE}" letter-spacing="-2">Cristea <tspan fill="url(#shine)">David</tspan></text>
    <text class="s rise" {delay(.45)} x="{mid}" y="202" text-anchor="middle" font-size="27" font-weight="600" fill="{LAVENDER}">Deaf · Founder of <tspan fill="{WHITE}">CDAV.</tspan><tspan fill="{YELLOW}">IO</tspan></text>
    <text class="s rise" {delay(.65)} x="{mid}" y="240" text-anchor="middle" font-size="27" font-weight="600" fill="{WHITE}">Building a trading <tspan fill="{YELLOW}">super intelligence</tspan></text>
    {''.join(chip_svg)}

    <!-- water: each path holds two identical 1200px periods and slides by one -->
    {wave("w1", "M0 336 C150 318 300 318 450 336 S750 354 900 336 S1050 318 1200 336 C1350 318 1500 318 1650 336 S1950 354 2100 336 S2250 318 2400 336 V380 H0Z", 16)}
    {wave("w2", "M0 350 C200 334 400 366 600 350 S1000 334 1200 350 C1400 334 1600 366 1800 350 S2200 334 2400 350 V380 H0Z", 12, reverse=True)}
    {wave("w3", "M0 364 C150 356 300 372 450 364 S750 356 900 364 S1050 372 1200 364 C1350 356 1500 372 1650 364 S1950 356 2100 364 S2250 372 2400 364 V380 H0Z", 9)}
  </g>"""
    return svg(w, h, "Cristea David. Deaf, founder of CDAV.IO, building a trading super intelligence", body)


# ------------------------------------------------------------ activity

def activity():
    data = json.loads((DATA / "contributions.json").read_text())
    days = data["days"]
    total = data["total"]
    active = sum(1 for d in days if d["count"])
    best = max(days, key=lambda d: d["count"])
    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] else 0
        longest = max(longest, run)

    w, h = 1200, 330
    cell, gap = 16, 4
    first = dt.date.fromisoformat(days[0]["date"])
    lead = (first.weekday() + 1) % 7        # GitHub weeks start on Sunday
    gx, gy = (w - 53 * (cell + gap) + gap) / 2, 150

    peak = max(1, best["count"])
    def colour(n):
        if n == 0:
            return "#24113f"
        f = n / peak
        return "#5b21b6" if f < .25 else VIOLET if f < .5 else "#8b5cf6" if f < .85 else YELLOW

    cells, months, last_month = [], [], None
    for i, d in enumerate(days):
        k = i + lead
        col, row = divmod(k, 7)
        x, y = gx + col * (cell + gap), gy + row * (cell + gap)
        cells.append(f'<rect class="pop" {delay(.5 + col * .018)} x="{x:.0f}" y="{y}" width="{cell}" height="{cell}" rx="4" fill="{colour(d["count"])}"/>')
        date = dt.date.fromisoformat(d["date"])
        if row == 0 and date.month != last_month and date.day <= 7:
            months.append(f'<text class="m" x="{x:.0f}" y="{gy - 10}" font-size="13" fill="{MUTED}">{date.strftime("%b")}</text>')
            last_month = date.month

    # count-up: one text per value, each shown briefly; the plain text is the final frame
    steps = 16
    count_up = ""
    if not STATIC:
        frames = [round(total * (i / steps) ** .6) for i in range(steps)]
        count_up = "".join(
            f'<text class="s" x="64" y="92" font-size="56" font-weight="800" fill="{WHITE}" opacity="0">{n}'
            f'<set attributeName="opacity" to="1" begin="{.3 + i * .05:.2f}s" dur=".05s"/></text>'
            for i, n in enumerate(frames)
        )
    final_total = (f'<text class="s" x="64" y="92" font-size="56" font-weight="800" fill="{WHITE}"'
                   + ("" if STATIC else ' opacity="0"><set attributeName="opacity" to="1" begin="1.1s" fill="freeze"/') + f'>{total}</text>')

    stats = [("ACTIVE DAYS", active), ("LONGEST STREAK", f"{longest} d"), ("BEST DAY", best["count"])]
    stat_svg = "".join(
        f'<g class="rise" {delay(.4 + i * .12)}><text class="m" x="{760 + i * 150}" y="62" font-size="12" fill="{MUTED}" letter-spacing="1.5">{label}</text>'
        f'<text class="s" x="{760 + i * 150}" y="92" font-size="30" font-weight="800" fill="{YELLOW if i == 2 else WHITE}">{value}</text></g>'
        for i, (label, value) in enumerate(stats)
    )

    body = background(w, h, glow_x=.15) + f"""
    {count_up}{final_total}
    <text class="m rise" {delay(.2)} x="66" y="122" font-size="15" fill="{LAVENDER}" letter-spacing="1">contributions in the last year</text>
    {stat_svg}
    {''.join(months)}
    {''.join(cells)}
  </g>"""
    return svg(w, h, f"{total} contributions in the last year", body)


# --------------------------------------------------------------- tiles

SILVER = "#d6d6e4"   # white-grey for small labels
GREY = "#a3a3b8"

# Icons sit on a 56x56 grid and are filled with the glossy white gradient "gloss".
ICON_GAME = (
    '<path fill="url(#gloss)" fill-rule="evenodd" d="M17 13h22a13 13 0 0 1 12.6 9.8l3.6 14.4a7 7 0 0 1-12.2 6.1L37.5 37h-19l-5.5 6.3a7 7 0 0 1-12.2-6.1l3.6-14.4A13 13 0 0 1 17 13z'
    'M15 22.5h4v4.5h4.5v4H19V35.5h-4V31h-4.5v-4H15z'
    'M38 23.5a2.8 2.8 0 1 0 0 .01zM44.5 29a2.8 2.8 0 1 0 0 .01zM38 34.5a2.8 2.8 0 1 0 0 .01zM31.5 29a2.8 2.8 0 1 0 0 .01z"/>'
)
ICON_CODE = (
    '<g fill="none" stroke="url(#glossLine)" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M18 16L6 28l12 12"/><path d="M38 16l12 12-12 12"/><path d="M32 11l-8 34"/></g>'
)
ICON_CHART = (
    '<g fill="url(#gloss)">'
    '<rect x="8" y="30" width="7" height="16" rx="2"/><rect x="10.5" y="25" width="2" height="25" rx="1"/>'
    '<rect x="21" y="24" width="7" height="18" rx="2"/><rect x="23.5" y="19" width="2" height="28" rx="1"/>'
    '<rect x="34" y="14" width="7" height="20" rx="2"/><rect x="36.5" y="9" width="2" height="30" rx="1"/></g>'
    '<path d="M6 44L20 33l12 4 18-22" fill="none" stroke="url(#glossLine)" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>'
    '<path d="M42 14h9v9" fill="none" stroke="url(#glossLine)" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>'
)

TILES = [
    ("games", "GAMES", "Game dev", "From prototype to playable build", ICON_GAME),
    ("apps", "APPS & SAAS", "macOS · Windows · iOS", "Native apps, desktop software, web", ICON_CODE),
    ("trading", "TRADING", "Nasdaq · BTC · ETH", None, ICON_CHART),
]


def tile(i, key, kicker, title, line, icon):
    w, h = 400, 260
    css = """
.swing { animation: swing .9s cubic-bezier(.2,1.4,.4,1) both; transform-origin: 50% 100%; transform-box: view-box; }
@keyframes swing { from { opacity: 0; transform: translateY(70px) rotate(-6deg); } to { opacity: 1; transform: none; } }
.nudge { animation: nudge 1.6s ease-in-out infinite; transform-box: fill-box; }
@keyframes nudge { 0%,100% { transform: none; } 50% { transform: translateX(6px); } }
"""
    if STATIC:
        css += "* { animation: none !important; }"
    start = 1.2 + i * .2
    shine = "" if STATIC else f'<animate attributeName="x" values="-240;640;640" keyTimes="0;.35;1" dur="5s" begin="{start + .4:.1f}s" repeatCount="indefinite"/>'
    glint = "" if STATIC else f'<animate attributeName="x" values="-30;80;80" keyTimes="0;.3;1" dur="4s" begin="{start:.1f}s" repeatCount="indefinite"/>'

    if line is None:   # trading: the super intelligence is still loading
        dots = "" if STATIC else "".join(
            f'<tspan>.<animate attributeName="opacity" values="{v}" keyTimes="0;.25;.5;.75;1" dur="1.6s" repeatCount="indefinite"/></tspan>'
            for v in ("0;1;1;1;1", "0;0;1;1;1", "0;0;0;1;1"))
        bar = "" if STATIC else '<animate attributeName="width" values="0;220;220" keyTimes="0;.85;1" dur="5s" repeatCount="indefinite"/>'
        detail = f"""
    <text class="s" x="36" y="200" font-size="17" fill="{GREY}">Super intelligence <tspan fill="{WHITE}" font-weight="700">loading</tspan>{dots if dots else "..."}</text>
    <rect x="36" y="214" width="220" height="6" rx="3" fill="#ffffff" fill-opacity=".1"/>
    <rect x="36" y="214" width="{140 if STATIC else 0}" height="6" rx="3" fill="url(#barFill)">{bar}</rect>"""
    else:
        detail = f'<text class="s" x="36" y="204" font-size="17" fill="{GREY}">{escape(line)}</text>'

    body = f"""
  <defs>
    <linearGradient id="tbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/></linearGradient>
    <linearGradient id="tshine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="badge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8b5cf6"/><stop offset="1" stop-color="#4c1d95"/></linearGradient>
    <linearGradient id="gloss" gradientUnits="userSpaceOnUse" x1="0" y1="6" x2="0" y2="50">
      <stop offset="0" stop-color="#ffffff"/><stop offset=".55" stop-color="#ececf4"/><stop offset="1" stop-color="#b9b9cc"/>
    </linearGradient>
    <linearGradient id="glossLine" gradientUnits="userSpaceOnUse" x1="0" y1="6" x2="0" y2="50">
      <stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#c3c3d4"/>
    </linearGradient>
    <linearGradient id="glint" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".45"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="barFill" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{VIOLET}"/><stop offset="1" stop-color="#ffffff"/></linearGradient>
    <clipPath id="tc"><rect x="6" y="6" width="{w - 12}" height="{h - 12}" rx="20"/></clipPath>
    <clipPath id="bc"><rect x="30" y="30" width="72" height="72" rx="18"/></clipPath>
  </defs>
  <g class="swing" {delay(.2 + i * .18)}>
    <rect x="6" y="6" width="{w - 12}" height="{h - 12}" rx="20" fill="url(#tbg)" stroke="{VIOLET}" stroke-opacity=".8" stroke-width="1.5"/>
    <g clip-path="url(#tc)">
      <rect x="-240" y="0" width="200" height="{h}" fill="url(#tshine)" transform="skewX(-18)">{shine}</rect>
    </g>

    <!-- app-style badge: purple tile, glossy white icon, a glint sweeping across -->
    <rect x="30" y="30" width="72" height="72" rx="18" fill="url(#badge)"/>
    <rect x="30" y="30" width="72" height="36" rx="18" fill="#ffffff" fill-opacity=".1"/>
    <g transform="translate(38 38)">{icon}</g>
    <g clip-path="url(#bc)"><rect x="-30" y="20" width="22" height="100" fill="url(#glint)" transform="skewX(-20)">{glint}</rect></g>

    <text class="m" x="36" y="134" font-size="14" font-weight="700" fill="{SILVER}" letter-spacing="3">{escape(kicker)}</text>
    <text class="s" x="34" y="172" font-size="29" font-weight="800" fill="{WHITE}">{escape(title)}</text>
    {detail}
    <text class="s nudge" x="{w - 58}" y="214" font-size="26" font-weight="800" fill="{SILVER}">→</text>
  </g>"""
    return svg(w, h, f"{kicker}: {title}", body, css)


# ------------------------------------------------------------- buttons

GLOSS_DEFS = """
    <linearGradient id="bbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2a0f52"/><stop offset="1" stop-color="#1c0b36"/></linearGradient>
    <linearGradient id="gw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".55" stop-color="#ececf4"/><stop offset="1" stop-color="#b9b9cc"/></linearGradient>
    <linearGradient id="hl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity=".16"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient>"""


def icon_button(key):
    """Square, icon-only link button: purple glass with a glossy white icon."""
    vb, inner = SOCIAL[key]
    size, pad = 64, 18
    body = f"""
  <defs>{GLOSS_DEFS}</defs>
  <rect x=".75" y=".75" width="{size - 1.5}" height="{size - 1.5}" rx="16" fill="url(#bbg)" stroke="{VIOLET}" stroke-width="1.5"/>
  <rect x="2" y="2" width="{size - 4}" height="{size / 2 - 2}" rx="14" fill="url(#hl)"/>
  <svg x="{pad}" y="{pad}" width="{size - 2 * pad}" height="{size - 2 * pad}" viewBox="{vb}" fill="url(#gw)">{inner}</svg>"""
    return svg(size, size, key, body)


def repos_button():
    w, h = 330, 56
    body = f"""
  <defs>{GLOSS_DEFS}</defs>
  <rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="16" fill="url(#bbg)" stroke="{VIOLET}" stroke-width="1.5"/>
  <rect x="2" y="2" width="{w - 4}" height="{h / 2 - 2}" rx="14" fill="url(#hl)"/>
  <g transform="translate(22 16)" fill="none" stroke="url(#gw)" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
    <path d="M3 3.5A2.5 2.5 0 0 1 5.5 1H21v18H5.5A2.5 2.5 0 0 0 3 21.5z"/><path d="M3 21.5A2.5 2.5 0 0 0 5.5 24H21v-5"/><path d="M8 6h8"/>
  </g>
  <text class="s" x="60" y="34" fill="{WHITE}" font-size="15" font-weight="700" letter-spacing="2">VIEW REPOSITORIES</text>
  <text class="s" x="294" y="35" fill="#d6d6e4" font-size="18" font-weight="800">→</text>"""
    return svg(w, h, "View my repositories", body)


# ---------------------------------------------------------------- main

def fetch():
    query = 'query{user(login:"CDAVIO"){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}'
    raw = subprocess.run(["gh", "api", "graphql", "-f", f"query={query}"], check=True, capture_output=True, text=True).stdout
    cal = json.loads(raw)["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = [{"date": d["date"], "count": d["contributionCount"]} for w in cal["weeks"] for d in w["contributionDays"]]
    (DATA / "contributions.json").write_text(json.dumps({"total": cal["totalContributions"], "days": days}, indent=0))


def main():
    if "--fetch" in sys.argv:
        fetch()
    CARDS.mkdir(exist_ok=True)
    (CARDS / "hero.svg").write_text(hero())
    (CARDS / "activity.svg").write_text(activity())
    for i, t in enumerate(TILES):
        (CARDS / f"tile-{t[0]}.svg").write_text(tile(i, *t))
    for key in SOCIAL:
        (CARDS / f"icon-{key}.svg").write_text(icon_button(key))
    (CARDS / "btn-repos.svg").write_text(repos_button())
    print("rendered", ", ".join(sorted(p.name for p in CARDS.glob("*.svg"))))


if __name__ == "__main__":
    main()
