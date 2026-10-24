"""Generate the static multilingual website. Run with Python 3; no dependencies."""
from pathlib import Path
from html import escape as e
import json
B=Path(__file__).resolve().parent
D=json.loads((B/'content.json').read_text())
BASE='https://shiba6v.github.io/plcalc-page/'
SERVER='https://6pfbzewa5i.execute-api.ap-northeast-1.amazonaws.com/prod'
def path(lang):return '' if lang=='en' else lang+'/'
def title(lang):return 'Photo Lock Calculator 〜秘密の写真庫〜' if lang=='ja' else 'Photo Lock Calculator'
def url(lang):return BASE+path(lang)
for lang,t in D.items():
 assert len(t)==22,(lang,len(t))
 pre='' if lang=='en' else '../'
 dest=B/path(lang);dest.mkdir(exist_ok=True)
 alts='\n'.join(f'<link rel="alternate" hreflang="{k}" href="{url(k)}">' for k in D)
 links=''.join(f'<a href="{pre+path(k)}" lang="{k}" hreflang="{k}"'+(' aria-current="page"' if k==lang else '')+f'>{e(v[0])}</a>' for k,v in D.items())
 cards=''.join(f'<article><span class="number">0{i+1}</span><h3>{e(t[5+i*2])}</h3><p>{e(t[6+i*2])}</p></article>' for i in range(3))
 steps=''.join(f'<li><span>{i+1:02}</span><p>{e(t[12+i])}</p></li>' for i in range(3))
 store='https://apps.apple.com/'+('jp/' if lang=='ja' else '')+'app/id6821909230'
 schema={'@context':'https://schema.org','@type':'SoftwareApplication','name':title(lang),'alternateName':'plcalc','applicationCategory':'UtilitiesApplication','operatingSystem':'iOS 17.0 or later; iPadOS 17.0 or later','url':url(lang),'downloadUrl':store,'description':t[2],'image':BASE+'assets/icon.jpg','inLanguage':lang,'author':{'@type':'Person','name':'KEISUKE SHIBATA'}}
 headline='写真やファイルを<br>パスコードで保管。' if lang=='ja' else e(t[1])
 html=f'''<!doctype html>
<html lang="{lang}" dir="{'rtl' if lang=='ar' else 'ltr'}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title(lang))} | {e(t[1])}</title>
<meta name="description" content="{e(t[2],quote=True)}">
<link rel="canonical" href="{url(lang)}">
{alts}
<link rel="alternate" hreflang="x-default" href="{BASE}">
<meta property="og:type" content="website"><meta property="og:title" content="{e(title(lang),quote=True)}"><meta property="og:description" content="{e(t[2],quote=True)}"><meta property="og:url" content="{url(lang)}"><meta property="og:image" content="{BASE}assets/icon.jpg"><meta name="twitter:card" content="summary">
<meta name="theme-color" content="#10100f">
<link rel="icon" href="{pre}assets/icon.jpg"><link rel="stylesheet" href="{pre}site.css">
<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">{e(t[4])} ↓</a>
<header><a class="brand" href="{pre+path(lang)}"><img src="{pre}assets/icon.jpg" width="40" height="40" alt=""><span>{e(title(lang))}</span></a><details class="language"><summary>◎ <span lang="{lang}">{e(t[0])}</span> <span aria-hidden="true">⌄</span></summary><nav aria-label="Language">{links}</nav></details></header>
<main id="main">
<section class="hero">
<div class="hero-copy"><p class="eyebrow" dir="ltr">iPhone & iPad · plcalc</p><h1>{headline}</h1><p class="intro">{e(t[2])}</p><a class="cta" href="{store}">{e(t[3])}<span aria-hidden="true">↗</span></a><p class="compat" dir="ltr">iOS 17+ · iPadOS 17+</p></div>
<div class="screens"><div class="halo"></div><img class="phone secondary" src="{pre}assets/{lang}-calculator.webp" width="640" height="1392" alt="{e(t[14],quote=True)}" decoding="async"><img class="phone primary" src="{pre}assets/{lang}-gallery.webp" width="640" height="1392" alt="{e(t[7],quote=True)}" fetchpriority="high"></div>
</section>
<section class="features"><div class="section-heading"><p class="eyebrow" dir="ltr">PHOTO LOCK CALCULATOR</p><h2>{e(t[4])}</h2></div><div class="feature-grid">{cards}</div></section>
<section class="walkthrough"><div class="wifi-screen"><img src="{pre}assets/{lang}-wifi.webp" width="640" height="1392" alt="{e(t[9],quote=True)}" loading="lazy" decoding="async"></div><div class="instructions"><p class="eyebrow" dir="ltr">01 / 02 / 03</p><h2>{e(t[11])}</h2><ol>{steps}</ol><a class="text-link" href="{store}">{e(t[3])} ↗</a></div></section>
<section class="notes"><h2>{e(t[15])}</h2><p>{e(t[16])}</p><p>{e(t[17])}</p><a class="text-link" href="{SERVER}/support" hreflang="ja">{e(t[18])} ↗</a></section>
<section class="last"><img src="{pre}assets/icon.jpg" width="64" height="64" alt="" loading="lazy"><h2 dir="auto">{e(title(lang))}</h2><a class="cta" href="{store}">{e(t[3])}<span aria-hidden="true">↗</span></a></section>
</main>
<footer><nav aria-label="{e(t[18],quote=True)}"><a href="{SERVER}/support" hreflang="ja">{e(t[18])}</a><a href="{SERVER}/privacy" hreflang="ja">{e(t[19])}</a><a href="{SERVER}/terms" hreflang="ja">{e(t[20])}</a></nav><p>{e(t[21])}</p><p dir="ltr">© 2026 KEISUKE SHIBATA · Photo Lock Calculator</p></footer>
</body></html>'''
 (dest/'index.html').write_text(html)
sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
for lang in D:
 sitemap+=f'<url><loc>{url(lang)}</loc>'
 sitemap+=''.join(f'<xhtml:link rel="alternate" hreflang="{k}" href="{url(k)}"/>' for k in D)
 sitemap+=f'<xhtml:link rel="alternate" hreflang="x-default" href="{BASE}"/></url>\n'
(B/'sitemap.xml').write_text(sitemap+'</urlset>\n')
(B/'.nojekyll').touch()
print(f'Generated {len(D)} languages and sitemap.xml')
