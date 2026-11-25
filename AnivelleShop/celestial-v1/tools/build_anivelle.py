"""Build the celestial website and self-contained IMVU HTML from preserved content."""
from pathlib import Path
from html import escape
from urllib.parse import urlparse, parse_qs
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT if (ROOT / 'content.json').exists() else ROOT / 'AnivelleShop'
HOST = 'https://raw.githubusercontent.com/anyavibez/ImageHosting/main/AnivelleShop/celestial-v1/assets/'
DATA = json.loads((OUT / 'content.json').read_text(encoding='utf-8'))
CSS = (OUT / 'celestial.css').read_text(encoding='utf-8')
CATEGORIES = [
    ('shop','Furniture','furniture','Furniture for your dream space.','107'),
    ('rooms','Rooms','rooms','A little world of your own.','107'),
    ('clothing','Clothing','clothing','Dress for your anime era.','106'),
    ('accessories','Accessories','accessories','The finishing touch of magic.','3117'),
    ('avatar-poses','Poses','poses','Every angle, a little story.','108'),
    ('body','Body','body','Make your avatar your own.','3114'),
    ('pets','Pets','pets','Your cutest little companion.','425'),
    ('cutouts','Cutouts','cutouts','Bring your creative world to life.','3110'),
]
HEADLINES = {
    'shop':('Your anime','era.'), 'rooms':('Rooms made','of dreams.'),
    'clothing':('A little','main-character magic.'),
    'accessories':('Written in','the little details.'),
    'avatar-poses':('Make every','moment yours.'),
    'body':('Beautifully,','uniquely you.'),
    'pets':('Little friends.','Big magic.'),
    'cutouts':('Imagine it.','Make it magic.'),
    'creator-only':('Behind the','atelier doors.'),
}
HERO = {'shop':'home','avatar-poses':'poses','creator-only':'creator'}
CATALOG = DATA['anivelle-shop.html']['original_links'][0]['href']
ALL = DATA['anivelle-shop.html']['original_links'][1]['href']

def esc(s): return escape(str(s), quote=True)
def ext(url): return f'href="{esc(url)}" target="_blank" rel="noopener noreferrer"'
def cat_url(cat):
    for link in DATA['anivelle-shop.html']['original_links']:
        if parse_qs(urlparse(link['href']).query).get('cat') == [cat]: return link['href']
    return ALL
def page_url(slug, home=False): return f'pages/anivelle-{slug}.html' if home else f'anivelle-{slug}.html'
def button(label, url): return f'<a class="anv-button" {ext(url)}>{esc(label)}</a>'
def heading(title, eyebrow='', sub=''):
    return f'<div class="anv-section-head"><span class="anv-eyebrow">{esc(eyebrow)}</span><h2>{esc(title)}</h2>{f"<p>{esc(sub)}</p>" if sub else ""}</div>'
def brand(url):
    return f'<a class="anv-brand" href="{esc(url)}" aria-label="AnivelleShop home"><span class="anv-brand-mark" aria-hidden="true">✦</span><span><span class="anv-brand-name">AnivelleShop</span><small>The Celestial Atelier</small></span></a>'
def sparkles():
    return '<span class="anv-sparkles" aria-hidden="true">'+''.join(f'<i>{s}</i>' for s in '✦✧✦✧✦✧')+'</span>'

def collections(slug, asset, embed, home):
    selected = ['clothing','accessories','rooms'] if slug in ('shop','creator-only') else ['shop','clothing','accessories']
    selected = [s for s in selected if s != slug]
    if len(selected)<3: selected.append('pets' if slug!='pets' else 'rooms')
    cards = []
    for item in selected:
        key,label,tile,desc,cat = next(c for c in CATEGORIES if c[0]==item)
        link = ext(cat_url(cat)) if embed else f'href="{page_url(key,home)}"'
        cards.append(f'<a class="anv-collection" {link}><img src="{asset(tile+"-tile")}" width="1024" height="1024" alt="Celestial {label.lower()} collection artwork" loading="lazy" decoding="async"><div class="anv-collection-label"><h3>{esc(label)}</h3><p>{esc(desc)}</p></div></a>')
    return '<section class="anv-section" id="anv-collections">'+heading('Featured collections','Discover your next favourite')+'<div class="anv-collection-grid">'+''.join(cards)+'</div></section>'

def catalog_links(record):
    unique={}
    for link in record['original_links']:
        unique.setdefault(link['href'],re.sub(r'^[^A-Za-z]+','',link['text']))
    return '<details class="anv-rights"><summary>Browse the IMVU catalogue</summary><nav class="anv-chips" aria-label="IMVU catalogue links" style="margin-top:18px">'+''.join(f'<a class="anv-chip" {ext(url)}>{esc(label)}</a>' for url,label in unique.items())+'</nav></details>'

def render(slug, record, embed=False, home=False):
    prefix='assets/' if home else '../assets/'
    asset=lambda name: esc((HOST if embed else prefix)+name+'.webp')
    home_link = CATALOG if embed else ('index.html' if home else '../index.html')
    creator_link = CATALOG if embed else page_url('creator-only',home)
    current=next((c for c in CATEGORIES if c[0]==slug),None)
    category_url=cat_url(current[4]) if current else CATALOG
    title_a,title_b=HEADLINES[slug]
    hero=HERO.get(slug,slug)+'-hero'
    title=record['av-sub'][0]
    top=f'''<div class="anv-celestial" id="anv-top">
<header class="anv-header">{brand(home_link)}<nav class="anv-topnav" aria-label="Main navigation"><a href="{esc(home_link)}">Home</a><a href="#anv-collections">Collections</a><a {ext(ALL)}>New arrivals</a><a class="anv-bag" {ext(CATALOG)} aria-label="Open Anivelle Studio on IMVU"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 7h14l1 14H4L5 7Z M8 8V6a4 4 0 0 1 8 0v2"/></svg></a></nav></header>
<section class="anv-hero" aria-label="{esc(title)}">
<img class="anv-hero-art" src="{asset(hero)}" width="1536" height="1024" alt="Original blonde anime heroine in the celestial {esc('creator workshop' if not current else current[1].lower()+' atelier')}" fetchpriority="high" decoding="async">
{sparkles()}<div class="anv-hero-copy"><span class="anv-eyebrow">Anivelle Studio · IMVU Creator</span><h1>{esc(title_a)}<br><em>{esc(title_b)}</em></h1><p class="anv-hero-sub">{esc(title)}<br>Original creations for your IMVU world.</p><div class="anv-hero-divider" aria-hidden="true"></div>{button('Explore '+current[1].lower(),category_url) if current else '<a class="anv-button" href="#anv-creator-note">Read creator note</a>'}<br><a class="anv-text-link" href="#anv-collections">Discover the collections</a></div><span class="anv-ribbon" aria-hidden="true"></span></section>
<nav class="anv-categories" aria-label="Shop collections">'''
    for key,label,_,_,cat in CATEGORIES:
        link=ext(cat_url(cat)) if embed else f'href="{page_url(key,home)}"'
        top+=f'<a {link}{" aria-current=\"page\"" if key==slug else ""}>{label}</a>'
    top+='</nav>'
    if slug=='creator-only':
        body=f'''<section class="anv-warning" id="anv-creator-note"><span class="anv-eyebrow">Please read before buying</span><h2>{esc(record['av-warn-title'][0])}</h2><h3>{esc(record['av-warn-sub'][0])}</h3><p>{esc(record['av-warn-note'][0])}</p><strong>Not for sale · Creator only</strong></section>
<section class="anv-intro"><div><span class="anv-eyebrow">A personal piece</span><h2>{esc(record['av-co-item-name'][0])}</h2><p>{esc(record['av-co-item-desc'][0])}</p><p>{esc(record['av-sec-text'][0])}</p></div><div class="anv-intro-art"><img src="{asset('accessories-tile')}" width="1024" height="1024" alt="Illustrative celestial ribbon and jewelry still life" loading="lazy"></div></section>
<section class="anv-section">{heading('Three simple rules','Inside the atelier')}<div class="anv-perks">{''.join('<div class="anv-perk">'+esc(s.lstrip('✔ ').strip())+'</div>' for s in record['av-mini'])}</div></section>'''
        body+=collections(slug,asset,embed,home)
    else:
        body=collections(slug,asset,embed,home)
        body+=f'''<section class="anv-intro" id="anv-atelier"><div><span class="anv-eyebrow">Welcome to the atelier</span><h2>{esc(record['av-sec-title'][0].replace('Welcome to the ', '').replace('Welcome to ', '').rstrip('!'))}</h2><p>{esc(record['av-sec-text'][0])}</p>{button('Browse on IMVU',category_url)}<div class="anv-note">A little celestial magic. Entirely your style.</div></div><div class="anv-intro-art"><img src="{asset(current[2]+'-tile')}" width="1024" height="1024" alt="Celestial {esc(current[1].lower())} editorial illustration" loading="lazy" decoding="async"></div></section>'''
        body+='<section class="anv-section">'+heading('Signature pieces','The collection')+'<div class="anv-spotlight-grid">'
        body+=''.join(f'<article class="anv-spotlight"><h3>{esc(name)}</h3><p>{esc(desc)}</p></article>' for name,desc in zip(record['av-show-name'],record['av-show-desc']))+'</div></section>'
        body+='<section class="anv-night">'+heading('Crafted for collectors','The experience')+'<div class="anv-benefit-grid">'
        body+=''.join(f'<article class="anv-benefit"><span class="anv-benefit-icon" aria-hidden="true">{["✧","♡","✦","◇","❀","☾"][i]}</span><h3>{esc(name)}</h3><p>{esc(desc)}</p></article>' for i,(name,desc) in enumerate(zip(record['av-card-title'],record['av-card-text'])))+'</div></section>'
        body+='<section class="anv-section">'+heading(record['av-sec-title'][3],'Made for your world')+'<div class="anv-list-grid">'
        body+=''.join(f'<article class="anv-list-card"><h3>{["Atelier selection","Signature collection"][i%2]}</h3><ul>'+''.join('<li>'+esc(s)+'</li>' for s in group)+'</ul></article>' for i,group in enumerate(record['lists']))+'</div>'
        body+=f'<h3 class="anv-style-title">{esc(record["av-sec-title"][4])}</h3><div class="anv-chips">'+''.join('<span class="anv-chip">'+esc(s)+'</span>' for s in record['styles'])+'</div></section>'
        body+='<section class="anv-section">'+heading(record['av-sec-title'][-1],'The little details')+'<div class="anv-perks">'+''.join('<div class="anv-perk">'+esc(s.lstrip('✔ ').strip())+'</div>' for s in record['av-mini'])+'</div></section>'
    body+=f'''<section class="anv-editorial"><img src="{asset('atelier-banner')}" width="1536" height="1024" alt="Dreamy lavender celestial fashion atelier" loading="lazy" decoding="async"><div class="anv-editorial-copy"><h2>Celestial by design.</h2><p>A world of beautiful details, dreamy spaces and looks that feel like you.</p>{button('Visit the IMVU shop',CATALOG)}</div></section>'''
    body+=catalog_links(record)
    body+='<details class="anv-rights" open><summary>Copyright &amp; DMCA Warning</summary>'+''.join('<p>'+esc(s)+'</p>' for s in record['rights'])+'</details>'
    foot=f'''<footer class="anv-footer"><div>{brand(home_link)}<p>{esc(record['av-gfoot-sub'][0])}</p></div><nav aria-label="Footer navigation"><a href="#anv-top">Back to top</a><a {ext(CATALOG)}>IMVU shop</a><a href="{esc(creator_link)}">{'Creator catalogue' if embed else 'Creator note'}</a></nav><div class="anv-footer-bottom"><span>© 2026 Anivelle Studio · AnivelleShop</span><span>IMVU Creator · The Celestial Atelier</span></div></footer></div>'''
    return top+body+foot

def document(body, title, home=False):
    prefix='' if home else '../'
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#302538"><meta name="description" content="Explore {esc(title)} by Anivelle Studio. The Celestial Atelier for your IMVU world."><title>{esc(title)} · AnivelleShop</title><link rel="stylesheet" href="{prefix}celestial.css"><style>html{{scroll-behavior:smooth}}body{{margin:0;padding:24px;background:#e9deed}}@media(max-width:650px){{body{{padding:0}}}}@media(prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}</style></head><body>{body}</body></html>'''

def build():
    (OUT/'pages').mkdir(exist_ok=True); (OUT/'embeds').mkdir(exist_ok=True)
    for name,record in DATA.items():
        slug=name.removeprefix('anivelle-').removesuffix('.html')
        snippet='<style>\n'+CSS+'\n</style>\n'+render(slug,record,embed=True)
        (OUT/'embeds'/name).write_text(snippet,encoding='utf-8')
        (OUT/'embeds'/name.replace('.html','.txt')).write_text(snippet,encoding='utf-8')
        (OUT/'pages'/name).write_text(document(render(slug,record),record['av-sub'][0]),encoding='utf-8')
    record=DATA['anivelle-shop.html']
    (OUT/'index.html').write_text(document(render('shop',record,home=True),'The Celestial Atelier',home=True),encoding='utf-8')
    print('Built nine standalone pages, nine HTML + TXT embeds, and the shop index.')

if __name__=='__main__': build()
