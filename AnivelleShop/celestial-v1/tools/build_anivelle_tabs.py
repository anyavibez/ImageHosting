"""Single-document CSS-only section switching; IMVU save-filter test required."""
from build_anivelle import OUT, HOST, CSS, DATA, CATEGORIES, HEADLINES, HERO, SECTIONS
from build_anivelle import esc, heading, moodboard, editorial, imvu_link_fallback, imvu_symbol_css
from pathlib import Path
import re

def asset(name): return HOST+name+'.webp'

def hero(section,title,subtitle):
    image='boutique-hero' if section=='home' else HERO.get(section,section)+'-hero'
    a,b=('Your','Anime Era') if section=='home' else HEADLINES[section]
    return f'<div class="anv-hero"><img class="anv-hero-art" src="{asset(image)}" width="1536" height="1024" alt="Celestial {esc(title)} illustration"><div class="anv-hero-copy"><h1>{esc(a)}<br><em>{esc(b)}</em></h1><p class="anv-hero-sub">{esc(subtitle)}</p><div class="anv-hero-divider"><span>&#10022;</span></div></div><span class="anv-ribbon" aria-hidden="true"></span></div>'

def build():
    radios=''.join(f'<input class="anv-page-radio" type="radio" name="anv-page" id="anv-page-{s}" aria-label="{esc(l)}"'+(' checked="checked"' if s=='home' else '')+'>' for s,l,_ in SECTIONS)
    nav='<div class="anv-tab-navigation" aria-label="Choose a shop section">'+''.join(f'<label id="anv-tab-label-{s}" for="anv-page-{s}">{esc(l)}</label>' for s,l,_ in SECTIONS)+'</div>'
    header='<div class="anv-header"><div class="anv-brand"><span class="anv-brand-mark">&#10022;</span><span><span class="anv-brand-name">AnivelleShop</span><small>Anime Avatar Fashion Boutique</small></span></div><span class="anv-tab-hint">Your world. Your style.</span></div>'
    panels=[]
    for section,label,_ in SECTIONS:
        if section=='home':
            body=hero('home','Boutique','Original Anime Avatar Fashion for Your Unique Style')
            covers=[('clothing','Celestial Gala','collection-gala'),('body','Dreamy Twin Tails','collection-twintails'),('accessories','Starlit Accessories','collection-starlit')]
            body+='<div class="anv-section">'+heading('Featured Collections')+'<div class="anv-collection-grid">'+''.join(f'<label class="anv-collection" for="anv-page-{target}"><img src="{asset(image)}" width="1536" height="1024" alt="{title}"><div class="anv-collection-label"><h3>{title}</h3><p>Open this collection</p></div></label>' for target,title,image in covers)+'</div></div>'
        else:
            record=DATA['anivelle-'+section+'.html']
            body=hero(section,label,record['av-sub'][0])
            if section=='creator-only':
                body+='<div class="anv-warning"><h2>DO NOT BUY</h2><h3>'+esc(record['av-warn-sub'][0])+'</h3><p>'+esc(record['av-warn-note'][0])+'</p><strong>Not for sale · Creator only</strong></div>'
            else:
                body+='<div class="anv-section">'+heading(record['av-sub'][0])+f'<p class="anv-panel-intro">{esc(record["av-sec-text"][0])}</p><div class="anv-spotlight-grid">'+''.join(f'<div class="anv-spotlight"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t,d in zip(record['av-show-name'],record['av-show-desc']))+'</div></div>'
        panels.append(f'<div class="anv-tab-panel anv-panel-{section}" role="region" aria-labelledby="anv-tab-label-{section}">{body}</div>')
    body='<div class="anv-celestial anv-tab-app" style="background-image:url(\''+asset('celestial-silk')+'\')">'+radios+header+nav+'<div class="anv-tab-panels">'+''.join(panels)+'</div>'+moodboard(asset)+editorial(asset)+'<div class="anv-footer"><div class="anv-brand-name">AnivelleShop</div><p>Original creations for your unique style.</p></div></div>'
    base='''
.anv-tab-app .anv-page-radio{position:absolute;left:0;top:0;width:1px;height:1px;opacity:0;overflow:hidden;clip:rect(0,0,0,0)}
.anv-tab-app .anv-tab-navigation{display:flex;flex-wrap:wrap;justify-content:center;gap:6px;padding:13px 2%;background:#352a3e;border-bottom:1px solid #d8acc9;color:#fff0fa}
.anv-tab-app .anv-tab-navigation label{position:relative;padding:9px 13px;border:1px solid transparent;border-radius:10px;cursor:pointer;font:15px/1.4 Georgia,serif;transition:background .3s,box-shadow .3s,transform .3s}
.anv-tab-app .anv-tab-navigation label:hover{background:#92688b77;transform:translateY(-2px);box-shadow:0 0 16px #e0a8d650}
.anv-tab-app .anv-tab-panel{display:none}
.anv-tab-app .anv-tab-hint{font:italic 17px Georgia,serif;color:#f0ccdf}
.anv-tab-app .anv-panel-intro{max-width:75ch;margin:0 auto 25px;color:#755675;text-align:center}
.anv-tab-app label.anv-collection{cursor:pointer}
.anv-tab-app .anv-hero-divider span{color:#ffe0ef;position:absolute;left:45%;top:-14px}
@media(max-width:600px){.anv-tab-app .anv-tab-navigation label{font-size:13px;padding:8px 10px}.anv-tab-app .anv-tab-hint{display:none}}
'''
    for section,_,_ in SECTIONS:
        base+=f'#anv-page-{section}:checked ~ .anv-tab-panels > .anv-panel-{section}'+'{display:block}\n'
        base+=f'#anv-page-{section}:checked ~ .anv-tab-navigation > label[for="anv-page-{section}"]'+'{background:#a7799d66;border-color:#e8b8d3;color:#ffe6f4;box-shadow:0 0 15px #e6b0d750}\n'
        base+=f'#anv-page-{section}:focus-visible ~ .anv-tab-navigation > label[for="anv-page-{section}"]'+'{outline:2px solid #ffdeef;outline-offset:3px}\n'
    code='<!-- Single-file CSS tabs. Requires IMVU to retain INPUT, LABEL, and :checked CSS. No JavaScript. -->\n'+imvu_link_fallback(body)+'\n<style type="text/css">\n'+imvu_symbol_css(CSS)+base+'\n</style>\n'
    code=code.encode('ascii','xmlcharrefreplace').decode('ascii')
    assert code.count('type="radio"')==10 and code.count('checked="checked"')==1
    assert code.count('class="anv-tab-panel ')==10 and '<script' not in code
    assert 'New Arrivals' not in code and 'Explore Collection' not in code
    folder=OUT/'single-file'; folder.mkdir(exist_ok=True)
    (folder/'anivelle-imvu-tabs.html').write_text(code,encoding='ascii')
    (folder/'anivelle-imvu-tabs.txt').write_text(code,encoding='ascii')
    preview='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AnivelleShop · Single-file tabs</title><style>body{margin:0;background:#e9deed}</style></head><body>'+code+'</body></html>'
    (folder/'preview.html').write_text(preview,encoding='utf-8')
    (folder/'README.txt').write_text('SINGLE-FILE PAGE SWITCHING\n\nPaste all of anivelle-imvu-tabs.txt into one IMVU description. Clicking a category LABEL changes the selected radio and visible panel in this same document; it does not navigate to another URL. All ten sections are included.\n\nNo JavaScript, no form submission, no product-page URLs are used for the tabs. Images load from GitHub.\n\nIMPORTANT: This is a CSS-only tabs candidate. It requires IMVU to retain INPUT type=radio, LABEL/for attributes, and :checked sibling selectors when saving. Browser operation is verified separately; the live IMVU filter is not verified. If these controls are removed, this technique cannot work there. The previous simple-link edition is preserved.\n',encoding='ascii')
    print('Built one HTML/TXT file with ten CSS-only panels. IMVU save-filter test still required.')

if __name__=='__main__': build()
