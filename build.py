#!/usr/bin/env python3
"""Builds the Emerald Dating blog into ./docs (served by GitHub Pages at blog.emerald.dating).

Usage: python3 build.py
Posts live in ./posts/*.md with a front matter block:
---
title: Post title
description: One sentence meta description (150 to 160 characters)
date: 2026-10-05
slug: url-slug
keyword: main search phrase
tags: Hinge, Dating apps
---
"""
import os, re, sys, glob, html, json, datetime, shutil
import markdown

SITE = "https://blog.emerald.dating"
MAIN = "https://emerald.dating"
NAME = "Emerald Dating Blog"
# Contact paths (conversion). Leave UPWORK empty to hide the Upwork button.
PHONE = "+14077189695"
PHONE_SHOW = "(407) 718-9695"
SMS_BODY = "Hi David, I read your blog and want more dates. Can we talk?"
BOOK = "https://calendar.app.google/fFkwJPWrZwZmasFW9"
UPWORK = ""
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "docs")


def parse(path):
    raw = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    if not m:
        sys.exit(f"{path}: missing front matter")
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    body = m.group(2).strip()
    for k in ("title", "description", "date", "slug"):
        if not meta.get(k):
            sys.exit(f"{path}: front matter needs '{k}'")
    # House style: never em dashes or double hyphens
    for field, text in [("body", body), ("title", meta["title"]), ("description", meta["description"])]:
        if "—" in text or "--" in text or "–" in text:
            sys.exit(f"{path}: {field} contains an em dash, en dash or double hyphen. Rewrite with commas, periods, colons or parentheses.")
    meta["tags"] = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
    meta["body_md"] = body
    meta["body_html"] = markdown.markdown(body, extensions=["extra", "sane_lists", "toc"])
    words = len(re.findall(r"\w+", body))
    meta["minutes"] = max(3, round(words / 230))
    meta["dt"] = datetime.date.fromisoformat(meta["date"])
    return meta


CSS = """
:root{--forest:#0B241B;--emerald:#1F7A57;--mint:#57C79A;--cream:#F4EFE3;--paper:#F8F6F1;--ink:#12140F;--soft:#4A4E45;--line:rgba(18,20,15,.1);--gold:#C9A961}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Manrope',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--paper);color:var(--ink);-webkit-font-smoothing:antialiased}
a{color:inherit}
.top{background:var(--cream);border-bottom:1px solid var(--line)}
.top .in{max-width:1080px;margin:0 auto;padding:14px 20px;display:flex;align-items:center;justify-content:space-between;gap:12px}
.logo{display:flex;align-items:center;gap:8px;text-decoration:none;font-weight:700;font-size:19px;color:var(--forest)}
.logo .wm span{font-weight:400}
.logo small{font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--emerald);margin-left:6px}
.cta-s{background:var(--forest);color:var(--cream);text-decoration:none;font-weight:700;font-size:14px;padding:10px 16px;border-radius:10px;white-space:nowrap}
.wrap{max-width:740px;margin:0 auto;padding:48px 20px 80px}
.hero{max-width:1080px;margin:0 auto;padding:56px 20px 10px}
.eyebrow{font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--emerald)}
h1{font-family:'Playfair Display',Georgia,serif;font-weight:600;font-size:42px;line-height:1.15;margin-top:12px}
.lede{font-size:18px;line-height:1.6;color:var(--soft);margin-top:14px;max-width:640px}
.grid{max-width:1080px;margin:0 auto;padding:30px 20px 80px;display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px}
.card{display:block;text-decoration:none;background:#fff;border:1px solid var(--line);border-radius:18px;padding:24px;transition:border-color .15s,transform .15s}
.card:hover{border-color:var(--emerald);transform:translateY(-2px)}
.card h2{font-family:'Playfair Display',Georgia,serif;font-size:22px;line-height:1.3;font-weight:600;margin-top:10px}
.card p{font-size:15px;line-height:1.6;color:var(--soft);margin-top:10px}
.meta{font-size:13px;color:var(--soft);font-weight:600}
.post h1{font-size:40px}
.post .meta{margin-top:14px}
.body{margin-top:30px;font-size:17.5px;line-height:1.8;color:#262a22}
.body h2{font-family:'Playfair Display',Georgia,serif;font-size:28px;line-height:1.25;font-weight:600;color:var(--ink);margin:40px 0 12px}
.body h3{font-size:19px;font-weight:800;color:var(--forest);margin:28px 0 8px}
.body p{margin:0 0 18px}
.body ul,.body ol{margin:0 0 20px 22px}
.body li{margin-bottom:8px}
.body a{color:var(--emerald);font-weight:700}
.body strong{color:var(--ink)}
.body blockquote{border-left:3px solid var(--gold);padding:6px 0 6px 18px;margin:0 0 20px;color:var(--soft);font-style:italic}
.body table{width:100%;border-collapse:collapse;margin:0 0 22px;font-size:15px}
.body th,.body td{border:1px solid var(--line);padding:10px 12px;text-align:left}
.body th{background:var(--cream)}
.box{margin-top:44px;background:radial-gradient(90% 120% at 50% 0%,#17463A,var(--forest));color:var(--cream);border-radius:22px;padding:34px 28px;text-align:center}
.box h3{font-family:'Playfair Display',Georgia,serif;font-size:27px;line-height:1.25;font-weight:600}
.box p{font-size:15.5px;line-height:1.65;color:rgba(244,239,227,.82);margin-top:12px}
.box b{color:#fff}
.box a{display:inline-block;margin-top:20px;background:var(--cream);color:var(--forest);text-decoration:none;font-family:'Playfair Display',Georgia,serif;font-weight:600;font-size:18px;padding:15px 30px;border-radius:12px}
.more{margin-top:50px;border-top:1px solid var(--line);padding-top:26px}
.more h4{font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--emerald)}
.more a{display:block;margin-top:12px;font-family:'Playfair Display',Georgia,serif;font-size:19px;text-decoration:none;color:var(--ink)}
.more a:hover{color:var(--emerald)}
.foot{border-top:1px solid var(--line);background:var(--cream)}
.foot .in{max-width:1080px;margin:0 auto;padding:26px 20px;font-size:13px;color:var(--soft);display:flex;flex-wrap:wrap;gap:10px 22px;justify-content:space-between}
.foot a{text-decoration:none;font-weight:700;color:var(--forest)}
.box .btns{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:22px}
.box .btns a{margin-top:0}
.box a.alt{background:transparent;color:var(--cream);border:1px solid rgba(244,239,227,.45)}
.box .tiers{margin-top:18px;font-size:14px;color:rgba(244,239,227,.75)}
.box .proof{margin-top:14px;font-size:13.5px;color:rgba(244,239,227,.7)}
.box .proof a{display:inline;margin:0;padding:0;background:none;color:var(--mint);font-family:inherit;font-size:inherit;font-weight:700;text-decoration:underline}
.mid{margin:30px 0;padding:18px 20px;border:1px solid var(--line);border-left:4px solid var(--emerald);border-radius:12px;background:#fff;font-size:16px;line-height:1.6}
.mid a{color:var(--emerald);font-weight:800}
.bar{display:none}
@media (max-width:640px){.bar{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:20;gap:8px;padding:10px 12px calc(10px + env(safe-area-inset-bottom));background:var(--forest)}
.bar a{flex:1;text-align:center;text-decoration:none;font-weight:800;font-size:15px;padding:13px 8px;border-radius:10px;background:var(--cream);color:var(--forest)}
.bar a.alt{background:transparent;color:var(--cream);border:1px solid rgba(244,239,227,.45)}
body{padding-bottom:76px}.top .cta-s{display:none}}
.pr{max-width:1080px;margin:0 auto;padding:10px 20px 30px;display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
.plan{background:#fff;border:1px solid var(--line);border-radius:18px;padding:24px;display:flex;flex-direction:column}
.plan.hot{border:2px solid var(--emerald);position:relative}
.plan .tag{position:absolute;top:-12px;left:20px;background:var(--emerald);color:#fff;font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;padding:5px 10px;border-radius:20px}
.plan h2{font-family:'Playfair Display',Georgia,serif;font-size:24px;font-weight:600}
.plan .price{font-size:34px;font-weight:800;color:var(--forest);margin-top:8px}
.plan .price small{font-size:15px;font-weight:600;color:var(--soft)}
.plan p{font-size:15px;line-height:1.55;color:var(--soft);margin-top:8px}
.plan ul{margin:14px 0 18px 18px;font-size:14.5px;line-height:1.7;color:#262a22;flex:1}
.plan a{display:block;text-align:center;text-decoration:none;font-weight:800;padding:13px;border-radius:10px;background:var(--forest);color:var(--cream)}
.plan a.alt{background:var(--cream);color:var(--forest)}
.cmp{max-width:740px;margin:10px auto 0;padding:0 20px}
.cmp table{width:100%;border-collapse:collapse;background:#fff;font-size:15px}
.cmp th,.cmp td{border:1px solid var(--line);padding:10px 12px;text-align:left}
.cmp th{background:var(--cream)}
.cmp h2{font-family:'Playfair Display',Georgia,serif;font-size:28px;font-weight:600;margin:30px 0 12px}
.cmp p{font-size:15.5px;line-height:1.65;color:var(--soft);margin-top:12px}
@media (max-width:640px){h1,.post h1{font-size:31px}.body{font-size:17px}.logo small{display:none}}
"""

GEM = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1F7A57" stroke-width="1.8"><path d="M8 2h8l4 5v10l-4 5H8l-4-5V7z"/><path d="M9.5 6h5l2 2.5v7l-2 2.5h-5l-2-2.5v-7z"/></svg>'


def esc(s):
    return html.escape(s, quote=True)


def page(title, desc, canonical, body, extra_head=""):
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}"><meta property="og:site_name" content="{NAME}">
<meta name="twitter:card" content="summary">
<link rel="alternate" type="application/rss+xml" title="{NAME}" href="{SITE}/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600&family=Manrope:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style>
{extra_head}
</head><body>
<header class="top"><div class="in">
<a class="logo" href="{SITE}/">{GEM}<span class="wm">emerald<span>.dating</span></span><small>Blog</small></a>
<a class="cta-s" href="{sms()}">Text David: {PHONE_SHOW}</a>
</div></header>
{body}
<footer class="foot"><div class="in">
<span>© {datetime.date.today().year} Emerald Dating. Done-for-you dating for busy professionals, run by a 100% US-based team.</span>
<span>Text or call David: <a href="{sms()}">{PHONE_SHOW}</a> · <a href="{BOOK}">Book a call</a>{upwork_link(" · ")}</span>
<span><a href="{SITE}/pricing/">Pricing</a> · <a href="{MAIN}/">emerald.dating</a> · <a href="{SITE}/">All articles</a> · <a href="{SITE}/feed.xml">RSS</a></span>
</div></footer>
<nav class="bar"><a href="{sms()}">Text David</a><a class="alt" href="{BOOK}">Book a call</a></nav>
</body></html>
"""


def sms():
    from urllib.parse import quote
    return f"sms:{PHONE}?&amp;body={quote(SMS_BODY)}"


def upwork_link(prefix=""):
    return f'{prefix}<a href="{UPWORK}">Upwork</a>' if UPWORK else ""


def mid_cta(slug):
    return f"""<div class="mid"><b>Rather have this done for you?</b> Text David, the founder, at <a href="{sms()}">{PHONE_SHOW}</a> or <a href="{BOOK}">book a quick call</a>. He answers personally.</div>"""


def with_mid(h, slug):
    parts = h.split("<h2")
    if len(parts) > 4:
        parts[3] = parts[3] + mid_cta(slug)
    return "<h2".join(parts)


def cta(slug):
    up = f'<a class="alt" href="{UPWORK}">Message David on Upwork</a>' if UPWORK else ""
    proof = f'<p class="proof">50+ client reviews on <a href="{UPWORK}">David\'s Upwork profile</a>.</p>' if UPWORK else ""
    return f"""<div class="box">
<h3>Want more dates without the app grind?</h3>
<p>Dating profile management, done for you: we optimize your profile, swipe, message your matches and coordinate the date on Hinge, Bumble and Tinder. You just show up.<br><b>16+ new quality matches in your first 7 days, or your money back.</b></p>
<div class="btns"><a href="{sms()}">Text David: {PHONE_SHOW}</a><a class="alt" href="{BOOK}">Book a call</a>{up}</div>
<p class="tiers">Profile Optimization $99 · Done-for-you plans from $125/week</p>
{proof}</div>"""


def build():
    posts = sorted((parse(p) for p in glob.glob(os.path.join(ROOT, "posts", "*.md"))), key=lambda m: m["dt"], reverse=True)
    today = datetime.date.today()
    posts = [p for p in posts if p["dt"] <= today]
    slugs = [p["slug"] for p in posts]
    if len(slugs) != len(set(slugs)):
        sys.exit("duplicate slug")
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    for i, p in enumerate(posts):
        url = f"{SITE}/{p['slug']}/"
        ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "description": p["description"],
              "datePublished": p["date"], "dateModified": p["date"], "mainEntityOfPage": url,
              "author": {"@type": "Person", "name": "David", "url": MAIN},
              "publisher": {"@type": "Organization", "name": "Emerald Dating", "url": MAIN}}
        if p.get("keyword"):
            ld["keywords"] = p["keyword"]
        others = [o for o in posts if o is not p][:3]
        more = ""
        if others:
            more = '<div class="more"><h4>Keep reading</h4>' + "".join(f'<a href="{SITE}/{o["slug"]}/">{esc(o["title"])}</a>' for o in others) + "</div>"
        body = f"""<main class="wrap post"><article>
<div class="eyebrow">{esc(", ".join(p["tags"]) or "Dating")}</div>
<h1>{esc(p["title"])}</h1>
<div class="meta">By David, founder of Emerald Dating · {p["dt"].strftime("%B %-d, %Y")} · {p["minutes"]} min read</div>
<div class="body">{with_mid(p["body_html"], p["slug"])}</div>
{cta(p["slug"])}
</article>{more}</main>"""
        os.makedirs(os.path.join(OUT, p["slug"]))
        open(os.path.join(OUT, p["slug"], "index.html"), "w", encoding="utf-8").write(
            page(f'{p["title"]} | Emerald Dating', p["description"], url, body,
                 f'<meta property="og:type" content="article"><script type="application/ld+json">{json.dumps(ld)}</script>'))

    cards = "".join(f"""<a class="card" href="{SITE}/{p['slug']}/"><div class="meta">{p['dt'].strftime('%b %-d, %Y')} · {p['minutes']} min read</div>
<h2>{esc(p['title'])}</h2><p>{esc(p['description'])}</p></a>""" for p in posts)
    idx = f"""<section class="hero"><div class="eyebrow">The Emerald Dating Blog</div>
<h1>Dating app advice for busy men</h1>
<p class="lede">Straight answers on Hinge, Bumble and Tinder, better profiles, better messages and more real dates, from the team that runs dating apps for professionals every day.</p></section>
<section class="grid">{cards}</section>"""
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(
        page("Dating App Advice for Busy Men | Emerald Dating Blog",
             "Hinge, Bumble and Tinder advice for busy men: profile tips, opening messages and how to turn matches into real dates.", f"{SITE}/", idx))
    pricing = f"""<section class="hero"><div class="eyebrow">Emerald Dating pricing</div>
<h1>Pick how much of your dating life you want back</h1>
<p class="lede">Dating profile management, done for you. A US-based assistant with a bachelor's degree optimizes your profile, swipes, messages your matches and coordinates the date, so you just show up. <b>16+ new quality matches in your first 7 days, or your money back.</b></p></section>
<section class="pr">
<div class="plan"><h2>Bronze</h2><div class="price">$125<small>/week</small></div><p>We run your apps and book your dates.</p>
<ul><li>Your own US-based assistant</li><li>Profile optimization included</li><li>Daily swiping and messaging</li><li>Dates coordinated onto your calendar</li></ul><a href="{sms()}">Text David to start</a></div>
<div class="plan hot"><span class="tag">Most popular</span><h2>Gold</h2><div class="price">$175<small>/week</small></div><p>More assistant time, more matches, more dates.</p>
<ul><li>Everything in Bronze</li><li>More of your assistant's time every week</li><li>More conversations moved to real dates</li></ul><a href="{sms()}">Text David to start</a></div>
<div class="plan"><h2>Emerald</h2><div class="price">$220<small>/week</small></div><p>Maximum volume, fully hands-off.</p>
<ul><li>Everything in Gold</li><li>The most assistant time we offer</li><li>Highest match and date volume</li></ul><a href="{sms()}">Text David to start</a></div>
</section>
<section class="pr">
<div class="plan"><h2>Profile Optimization</h2><div class="price">$99<small> one time</small></div><p>Fix the profile, then run it yourself.</p>
<ul><li>Best photos picked and ordered</li><li>Prompts and bio rewritten</li><li>App settings tuned</li></ul><a class="alt" href="{sms()}">Text David for the $99 fix</a></div>
<div class="plan"><h2>Dating App OS</h2><div class="price">$49<small>/month</small></div><p>The full playbook if you'd rather do it yourself.</p>
<ul><li>Course and message scripts</li><li>Real profile examples</li><li>Private community</li></ul><a class="alt" href="https://www.skool.com/next-gen-dating-5893">Join on Skool</a></div>
</section>
<section class="cmp"><h2>Pay per week, not per date</h2>
<p>Our clients average 2 to 4 dates a week, capped only by their schedule.</p>
<table><tr><th>Plan</th><th>Per week</th><th>Cost per date at 2 to 4 dates</th></tr>
<tr><td>Bronze</td><td>$125</td><td>$31 to $63</td></tr><tr><td>Gold</td><td>$175</td><td>$44 to $88</td></tr><tr><td>Emerald</td><td>$220</td><td>$55 to $110</td></tr></table>
<p>Typical dating concierges charge thousands up front for about 12 dates in 90 days. Individual results vary. Guarantee conditions apply, see our <a href="{MAIN}/">Terms</a>.</p>
</section>
<main class="wrap" style="padding-top:10px">{cta("pricing")}</main>"""
    os.makedirs(os.path.join(OUT, "pricing"), exist_ok=True)
    open(os.path.join(OUT, "pricing", "index.html"), "w", encoding="utf-8").write(
        page("Pricing: Dating Profile Management | Emerald Dating",
             "Emerald Dating pricing: done-for-you dating profile management from $125/week, Profile Optimization $99, Dating App OS $49/month. 16+ matches in 7 days or money back.",
             f"{SITE}/pricing/", pricing))
    open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(
        page("Page not found | Emerald Dating Blog", "Page not found.", f"{SITE}/",
             f'<main class="wrap"><h1>Page not found</h1><p class="lede"><a href="{SITE}/">Back to all articles</a></p></main>'))

    urls = [f"<url><loc>{SITE}/</loc><lastmod>{posts[0]['date'] if posts else today}</lastmod></url>"]
    urls += [f"<url><loc>{SITE}/pricing/</loc></url>"]
    urls += [f"<url><loc>{SITE}/{p['slug']}/</loc><lastmod>{p['date']}</lastmod></url>" for p in posts]
    open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(urls) + "</urlset>\n")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    items = "".join(f"<item><title>{esc(p['title'])}</title><link>{SITE}/{p['slug']}/</link><guid>{SITE}/{p['slug']}/</guid><pubDate>{p['dt'].strftime('%a, %d %b %Y')} 12:00:00 GMT</pubDate><description>{esc(p['description'])}</description></item>" for p in posts[:20])
    open(os.path.join(OUT, "feed.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>{NAME}</title><link>{SITE}/</link><description>Dating app advice for busy men</description>{items}</channel></rss>\n')
    open(os.path.join(OUT, "CNAME"), "w").write("blog.emerald.dating\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    print(f"built {len(posts)} posts into docs/")


if __name__ == "__main__":
    build()
