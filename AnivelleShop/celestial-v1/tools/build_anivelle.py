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
CSS = (OUT / 'celestial.css').read_text(encoding='utf-8-sig')
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
    'shop':('Dream','Interiors'), 'rooms':('Your','Dream Escape'),
    'clothing':('Celestial','Couture'), 'accessories':('Starlit','Accessories'),
    'avatar-poses':('Strike a','Little Magic'), 'body':('Your','Signature Look'),
    'pets':('Little','Moon Companions'), 'cutouts':('Dream.','Create. Shine.'),
    'creator-only':('Inside','The Atelier'),
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
    return f'<a class="anv-brand" href="{esc(url)}" aria-label="AnivelleShop home"><span class="anv-brand-mark" aria-hidden="true">&#10022;</span><span><span class="anv-brand-name">AnivelleShop</span><small>Anime Avatar Fashion Boutique</small></span></a>'
def sparkles():
    return '<span class="anv-sparkles" aria-hidden="true">'+''.join(f'<i>{s}</i>' for s in '✦✧✦✧✦✧')+'</span>'

def collections(slug, asset, embed, home):
    selected = [
        ('clothing','Celestial<br>Gala','Starry elegance for your avatar.','collection-gala','106'),
        ('body','Dreamy<br>Twin Tails','A little magic in every strand.','collection-twintails','3114'),
        ('accessories','Starlit<br>Accessories','The finishing touch for your look.','collection-starlit','3117'),
    ]
    cards = []
    for key,label,desc,tile,cat in selected:
        link = ext(cat_url(cat)) if embed else f'href="{page_url(key,home)}"'
        cards.append(f'<a class="anv-collection" {link}><img src="{asset(tile)}" width="1536" height="1024" alt="{esc(label.replace("<br>"," "))} collection illustration" loading="lazy" decoding="async"><span class="anv-card-flourish" aria-hidden="true">&#10087;</span><div class="anv-collection-label"><h3>{label}</h3><p>{esc(desc)}</p><span class="anv-round-star" aria-hidden="true">&#10023;</span></div></a>')
    return '<div class="anv-section anv-featured" id="anv-collections">'+heading('Featured Collections')+'<div class="anv-collection-grid">'+''.join(cards)+'</div></div>'

def arrivals(asset):
    items=[('Lunar Waltz Dress','arrival-lunar-dress','106'),('Starlight Frill Dress','arrival-frill-dress','106'),('Celestial Cape Set','arrival-cape-set','106'),('Rose Star Braids','arrival-rose-braids','3114'),('Orbit Ribbon Clip','arrival-orbit-bow','3117')]
    cards=[]
    for name,image,cat in items:
        cards.append(f'<a class="anv-arrival" {ext(cat_url(cat))}><div class="anv-arrival-art"><img src="{asset(image)}" width="1024" height="1024" alt="{esc(name)} style illustration" loading="lazy" decoding="async"><span class="anv-heart" aria-hidden="true">&#9825;</span></div><h3>{esc(name)}</h3><span class="anv-arrival-tag">Style Preview</span><span class="anv-arrival-link">Browse on IMVU</span></a>')
    return '<div class="anv-section anv-arrivals" id="anv-arrivals">'+heading('New Arrivals')+'<div class="anv-arrival-grid">'+''.join(cards)+'</div><p class="anv-arrival-note">Celestial style inspiration · Explore the latest Anivelle Studio listings on IMVU.</p></div>'

def editorial(asset):
    return f'<div class="anv-editorial"><img src="{asset("atelier-banner")}" width="1536" height="1024" alt="Dreamy lavender celestial fashion atelier" loading="lazy" decoding="async"><div class="anv-editorial-copy"><h2>Celestial Couture</h2><p>A curated world of dreamy details<br>for your anime avatar.</p>{button("Discover the Look",CATALOG)}</div><span class="anv-editorial-flourish" aria-hidden="true">&#10022;</span></div>'

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
    title_a,title_b=('Your','Anime Era') if home else HEADLINES[slug]
    hero='boutique-hero' if home else HERO.get(slug,slug)+'-hero'
    title='Original Anime Avatar Fashion<br>for Your Unique Style' if home else esc(record['av-sub'][0])+'<br>Original creations for your IMVU world.'
    top=f'''<div class="anv-celestial" id="anv-top" style="background-image:url('{asset('celestial-silk')}')">
<header class="anv-header">{brand(home_link)}<nav class="anv-topnav" aria-label="Main navigation"><a href="{esc(home_link)}">Home</a><a href="#anv-collections">Collections</a><a href="#anv-arrivals">New Arrivals</a><a class="anv-search" {ext(CATALOG)} aria-label="Search Anivelle Studio on IMVU"><span aria-hidden="true"></span></a><a class="anv-bag" {ext(CATALOG)} aria-label="Open Anivelle Studio on IMVU"><span aria-hidden="true"></span></a></nav><span class="anv-header-ribbon" aria-hidden="true"></span></header>
<section class="anv-hero" aria-label="{esc('AnivelleShop Boutique' if home else record['av-sub'][0])}">
<img class="anv-hero-art" src="{asset(hero)}" width="1536" height="1024" alt="Original blonde anime heroine in the celestial {esc('creator workshop' if not current else current[1].lower()+' atelier')}" fetchpriority="high" decoding="async">
{sparkles()}<div class="anv-hero-copy"><h1>{esc(title_a)}<br><em>{esc(title_b)}</em></h1><p class="anv-hero-sub">{title}</p><div class="anv-hero-divider" aria-hidden="true"></div>{'<a class="anv-button" href="#anv-collections">Explore Collection</a>' if home else button('Explore '+current[1].lower(),category_url) if current else '<a class="anv-button" href="#anv-creator-note">Read creator note</a>'}</div><span class="anv-ribbon" aria-hidden="true"></span></section>'''
    category_nav='<nav class="anv-categories" aria-label="Shop collections">'
    for key,label,_,_,cat in CATEGORIES:
        link=ext(cat_url(cat)) if embed else f'href="{page_url(key,home)}"'
        category_nav+=f'<a {link}{" aria-current=\"page\"" if key==slug and not home else ""}>{label}</a>'
    category_nav+='</nav>'
    if home:
        body=collections(slug,asset,embed,home)+arrivals(asset)+editorial(asset)+category_nav
    elif slug=='creator-only':
        body=f'''<section class="anv-warning" id="anv-creator-note"><span class="anv-eyebrow">Please read before buying</span><h2>{esc(record['av-warn-title'][0])}</h2><h3>{esc(record['av-warn-sub'][0])}</h3><p>{esc(record['av-warn-note'][0])}</p><strong>Not for sale · Creator only</strong></section>
<section class="anv-intro"><div><span class="anv-eyebrow">A personal piece</span><h2>{esc(record['av-co-item-name'][0])}</h2><p>{esc(record['av-co-item-desc'][0])}</p><p>{esc(record['av-sec-text'][0])}</p></div><div class="anv-intro-art"><img src="{asset('accessories-tile')}" width="1024" height="1024" alt="Illustrative celestial ribbon and jewelry still life" loading="lazy"></div></section>
<section class="anv-section">{heading('Three simple rules','Inside the atelier')}<div class="anv-perks">{''.join('<div class="anv-perk">'+esc(s.lstrip('✔ ').strip())+'</div>' for s in record['av-mini'])}</div></section>'''
        body+=collections(slug,asset,embed,home)+arrivals(asset)+editorial(asset)+category_nav
    else:
        body=collections(slug,asset,embed,home)+arrivals(asset)+editorial(asset)+category_nav
        body+=f'''<section class="anv-intro" id="anv-atelier"><div><span class="anv-eyebrow">Welcome to the atelier</span><h2>{esc(record['av-sec-title'][0].replace('Welcome to the ', '').replace('Welcome to ', '').rstrip('!'))}</h2><p>{esc(record['av-sec-text'][0])}</p>{button('Browse on IMVU',category_url)}<div class="anv-note">A little celestial magic. Entirely your style.</div></div><div class="anv-intro-art"><img src="{asset(current[2]+'-tile')}" width="1024" height="1024" alt="Celestial {esc(current[1].lower())} editorial illustration" loading="lazy" decoding="async"></div></section>'''
        body+='<section class="anv-section">'+heading('Signature pieces','The collection')+'<div class="anv-spotlight-grid">'
        body+=''.join(f'<article class="anv-spotlight"><h3>{esc(name)}</h3><p>{esc(desc)}</p></article>' for name,desc in zip(record['av-show-name'],record['av-show-desc']))+'</div></section>'
        body+='<section class="anv-night">'+heading('Crafted for collectors','The experience')+'<div class="anv-benefit-grid">'
        body+=''.join(f'<article class="anv-benefit"><span class="anv-benefit-icon" aria-hidden="true">{["✧","♡","✦","◇","❀","☾"][i]}</span><h3>{esc(name)}</h3><p>{esc(desc)}</p></article>' for i,(name,desc) in enumerate(zip(record['av-card-title'],record['av-card-text'])))+'</div></section>'
        body+='<section class="anv-section">'+heading(record['av-sec-title'][3],'Made for your world')+'<div class="anv-list-grid">'
        body+=''.join(f'<article class="anv-list-card"><h3>{["Atelier selection","Signature collection"][i%2]}</h3><ul>'+''.join('<li>'+esc(s)+'</li>' for s in group)+'</ul></article>' for i,group in enumerate(record['lists']))+'</div>'
        body+=f'<h3 class="anv-style-title">{esc(record["av-sec-title"][4])}</h3><div class="anv-chips">'+''.join('<span class="anv-chip">'+esc(s)+'</span>' for s in record['styles'])+'</div></section>'
        body+='<section class="anv-section">'+heading(record['av-sec-title'][-1],'The little details')+'<div class="anv-perks">'+''.join('<div class="anv-perk">'+esc(s.lstrip('✔ ').strip())+'</div>' for s in record['av-mini'])+'</div></section>'
    if not home:
        body+=catalog_links(record)
        body+='<div class="anv-rights"><h3>Copyright &amp; DMCA Warning</h3>'+''.join('<p>'+esc(s)+'</p>' for s in record['rights'])+'</div>'
    foot=f'''<footer class="anv-footer"><div>{brand(home_link)}<p>{esc(record['av-gfoot-sub'][0])}</p></div><nav class="anv-footer-nav" aria-label="Footer navigation"><a href="#anv-top">Back to top</a><a {ext(CATALOG)}>IMVU shop</a><a href="{esc(creator_link)}">{'Creator catalogue' if embed else 'Creator note'}</a></nav><div class="anv-footer-bottom"><span>© 2026 Anivelle Studio · AnivelleShop</span><span>IMVU Creator · The Celestial Atelier</span></div></footer></div>'''
    html=top+body+foot
    if embed:
        # Keep paste-ready fragments to simple legacy-friendly HTML elements.
        html=re.sub(r'<(/?)(?:header|nav|section|article|footer|details)\b',r'<\1div',html)
        html=re.sub(r'<(/?)summary\b',r'<\1h3',html)
    return html

def document(body, title, home=False):
    prefix='' if home else '../'
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#302538"><meta name="description" content="Explore {esc(title)} by Anivelle Studio. The Celestial Atelier for your IMVU world."><title>{esc(title)} · AnivelleShop</title><link rel="stylesheet" href="{prefix}celestial.css"><style>html{{scroll-behavior:smooth}}body{{margin:0;padding:24px;background:#e9deed}}@media(max-width:650px){{body{{padding:0}}}}@media(prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}</style></head><body>{body}</body></html>'''

def build():
    (OUT/'pages').mkdir(exist_ok=True); (OUT/'embeds').mkdir(exist_ok=True)
    for name,record in DATA.items():
        slug=name.removeprefix('anivelle-').removesuffix('.html')
        snippet='<style type="text/css">\n'+CSS+'\n</style>\n'+render(slug,record,embed=True)
        snippet=snippet.encode('ascii','xmlcharrefreplace').decode('ascii')
        (OUT/'embeds'/name).write_text(snippet,encoding='utf-8')
        (OUT/'embeds'/name.replace('.html','.txt')).write_text(snippet,encoding='utf-8')
        (OUT/'pages'/name).write_text(document(render(slug,record),record['av-sub'][0]),encoding='utf-8')
    record=DATA['anivelle-shop.html']
    (OUT/'index.html').write_text(document(render('shop',record,home=True),'The Celestial Atelier',home=True),encoding='utf-8')
    snippet=('<style type="text/css">\n'+CSS+'\n</style>\n'+render('shop',record,embed=True,home=True)).encode('ascii','xmlcharrefreplace').decode('ascii')
    (OUT/'embeds'/'anivelle-home.html').write_text(snippet,encoding='ascii')
    (OUT/'embeds'/'anivelle-home.txt').write_text(snippet,encoding='ascii')
    print('Built ten styled pages and ten matching IMVU HTML + TXT fragments.')

if __name__=='__main__': build()
