"""One-file shop with ordinary section links, :target and inline visual fallbacks."""
from build_anivelle import OUT, HOST, DATA, HEADLINES, HERO, SECTIONS, esc

def asset(name): return HOST+name+'.webp'

def el(tag, cls, style, text, attrs=''):
    return f'<{tag} class="{cls}" style="{style}"{attrs}>{text}</{tag}>'

def heading(text, small):
    return el('div','anv-heading','text-align:center;margin:0 auto 26px;max-width:680px',el('div','','font:10px/1.5 Arial,sans-serif;letter-spacing:2px;text-transform:uppercase;color:#a47698;margin-bottom:12px',esc(small))+el('h2','','font:italic 35px/1.2 Georgia,serif;color:#69476f;margin:0','&#10022; '+esc(text)+' &#10022;'))

def divider():
    return el('div','anv-divider','text-align:center;padding:24px 0;color:#b98baa;font:23px Georgia,serif','<span style="display:inline-block;vertical-align:middle;width:25%;height:1px;background:#dfbfd4"></span> &nbsp; &#10023; &nbsp; <span style="display:inline-block;vertical-align:middle;width:25%;height:1px;background:#dfbfd4"></span>',' aria-hidden="true"')

BUTTON='display:inline-block;box-sizing:border-box;padding:12px 18px;margin:5px;border:1px solid #bf8eaf;border-radius:12px;background:#f9e9f5;color:#6c456e;text-decoration:none;font:15px/1.3 Georgia,serif;box-shadow:inset 0 0 0 3px #fff7fb;cursor:pointer'
def link(section,text): return el('a','anv-action',BUTTON,esc(text),f' href="#anv-page-{section}" target="_self"')

def hero(section,subtitle):
    image='boutique-hero' if section=='home' else HERO.get(section,section)+'-hero'
    a,b=('Your','Anime Era') if section=='home' else HEADLINES[section]
    return el('div','anv-hero',f"position:relative;overflow:hidden;min-height:500px;background:#3d2e48 url('{asset(image)}') center 38%/cover no-repeat;color:#fff2fb",el('div','anv-hero-copy','box-sizing:border-box;width:49%;min-height:500px;padding:95px 4% 70px;background:linear-gradient(90deg,#322539e6,#32253900)',el('h1','','font:italic 65px/.98 Georgia,serif;letter-spacing:-2px;margin:0 0 24px;color:#fff1f9',esc(a)+'<br>'+esc(b))+el('p','','font:17px/1.6 Georgia,serif;color:#fff0fa;margin:0;max-width:27ch',esc(subtitle))+el('div','','color:#f3cbdf;margin-top:25px;font:23px Georgia,serif','&#10022; &nbsp; &#10023; &nbsp; &#10022;')))

def home_cards():
    cards=''
    for section,name,image,desc in [('clothing','Celestial Gala','collection-gala','Dreamy layers. A little midnight drama.'),('body','Dreamy Twin Tails','collection-twintails','Soft strands, ribbons, and your signature charm.'),('accessories','Starlit Accessories','collection-starlit','Small details with a whole world of personality.')]:
        cards+=el('div','anv-feature-card','box-sizing:border-box;flex:1 1 240px;overflow:hidden;border:1px solid #d7afcb;border-radius:22px;background:#fff8fd;box-shadow:0 6px 20px #80557618',f'<img src="{asset(image)}" alt="{esc(name)} illustration" width="1536" height="1024" style="display:block;width:100%;height:190px;object-fit:cover">'+el('div','','padding:22px;text-align:center',el('h3','','font:italic 27px/1.15 Georgia,serif;color:#67416c;margin:0 0 12px',name)+el('p','','font:14px/1.6 Georgia,serif;color:#876982;min-height:46px;margin:0 0 12px',desc)+link(section,'View Collection')))
    return el('div','anv-section','padding:32px 4%',heading('Featured Collections','Choose your next chapter')+el('div','anv-feature-grid','display:flex;flex-wrap:wrap;gap:20px',cards))

def gallery():
    items=[('arrival-lunar-dress','Moonlit Silhouettes','Midnight romance','Soft layers with a little midnight drama.'),('arrival-frill-dress','Pearl & Petal','Soft enchantment','Delicate frills and a luminous finish.'),('arrival-cape-set','Wrapped in Starlight','Celestial elegance','Flowing fabric, golden stars, dreamy details.'),('arrival-rose-braids','Ribbon Daydreams','Your signature charm','Romantic strands with a playful twist.'),('arrival-orbit-bow','Little Luxuries','Finishing touches','A golden star. A silk bow. A little magic.')]
    cards=''
    for i,(image,name,tag,desc) in enumerate(items,1):
        art=el('div','anv-edit-art','position:relative;padding:8px 8px 0;background:#eee0ef',f'<img src="{asset(image)}" width="1024" height="1024" alt="{name} illustration" loading="lazy" style="display:block;width:100%;height:auto;border-radius:13px">'+el('span','','position:absolute;top:18px;left:18px;border:1px solid #e5bdd4;border-radius:20px;background:#fff7fb;color:#986b8d;padding:5px 9px;font:10px Arial,sans-serif',f'EDIT / 0{i}'))
        copy=el('div','anv-edit-copy','box-sizing:border-box;padding:22px 17px 24px;text-align:center;min-height:187px;background:#fff8fd',el('div','','font:9px/1.5 Arial,sans-serif;letter-spacing:1.5px;text-transform:uppercase;color:#ad7c9c;margin-bottom:10px',tag)+el('h3','','font:italic 23px/1.15 Georgia,serif;color:#67466d;margin:0 0 12px;min-height:53px',name)+el('p','','font:14px/1.6 Georgia,serif;color:#8a7086;margin:0',desc))
        cards+=el('div','anv-edit-card','box-sizing:border-box;flex:1 1 155px;min-width:0;border:1px solid #d9bbd2;border-radius:20px;overflow:hidden;box-shadow:0 6px 18px #8e5e881a;background:#fff8fd',art+copy)
    return el('div','anv-section anv-edit','padding:32px 4%;background:#fcf5fb',heading('The Celestial Edit','Five details. Endless possibilities.')+el('p','','max-width:650px;margin:0 auto 30px;text-align:center;font:16px/1.7 Georgia,serif;color:#8b6c86','Start with a silhouette you love. Add soft ribbons, luminous layers, or a golden accent. Let every detail tell a little more of your story.')+el('div','anv-edit-grid','display:flex;flex-wrap:wrap;align-items:stretch;justify-content:center;gap:15px',cards)+el('p','','text-align:center;font:italic 16px/1.6 Georgia,serif;color:#a17a96;margin:26px 0 0','&#10023; &nbsp; Curated inspiration for a world that feels like you. &nbsp; &#10023;'))

def couture():
    return el('div','anv-couture',f"margin:0 4%;padding:40px 5%;border:1px solid #c8a2c2;border-radius:24px;background:#49344f url('{asset('atelier-banner')}') center/cover;color:#fff3fc;overflow:hidden",el('div','anv-couture-copy','box-sizing:border-box;max-width:490px;padding:26px;border:1px solid #c99fbc;border-radius:18px;background:#38263ee6;text-align:center',el('div','','font:10px Arial,sans-serif;letter-spacing:2px;text-transform:uppercase;color:#e8bfd8','The art of your signature style')+el('h2','','font:italic 38px/1.1 Georgia,serif;margin:16px 0;color:#fff0fa','Celestial Couture')+el('p','','font:16px/1.7 Georgia,serif;margin:0 0 18px;color:#f2daeb','A curated world of dreamy details<br>for your anime avatar.')+link('clothing','View Clothing')+link('accessories','Style with Accessories')))

def rights_notice():
    rights=DATA['anivelle-shop.html']['rights']; cards=''
    for name,desc in [('Original work, treated with care','Keep Anivelle Studio textures, meshes, designs and assets out of unauthorized copies or redistributions.'),('Check the listing permissions','Derive or edit only where the product listing permits it. Contact the creator when permission is unclear.')]:
        cards+=el('div','anv-rights-card','box-sizing:border-box;flex:1 1 240px;padding:22px;border:1px solid #dec5d8;border-radius:15px;background:#fff9fd',el('div','','font:22px Georgia,serif;color:#b183a3;margin-bottom:12px','&#10023;')+el('h3','','font:italic 22px/1.2 Georgia,serif;color:#725075;margin:0 0 12px',name)+el('p','','font:14px/1.75 Georgia,serif;color:#8d7088;margin:0',desc))
    return el('div','anv-copyright','box-sizing:border-box;margin:0 4% 35px;padding:35px 5%;border:1px solid #caa9c2;border-top:4px solid #b890ad;border-radius:22px;background:#f6edf6;box-shadow:inset 0 0 0 7px #fff9fd,0 8px 25px #6c3f6812',el('div','','text-align:center',el('div','','display:inline-block;width:50px;height:50px;line-height:50px;border:3px double #c69bb8;border-radius:50%;background:#fff9fd;color:#a7779b;font-size:30px;margin-bottom:18px','&#169;')+heading('Copyright & DMCA Warning','Respect the creator. Respect the craft.'))+el('p','','text-align:center;font:italic 23px/1.4 Georgia,serif;color:#785178;margin:0 0 18px','Do not copy or reupload.')+el('p','','max-width:740px;margin:0 auto;font:15px/1.85 Georgia,serif;color:#80657c;text-align:center',esc(rights[1]))+el('div','anv-rights-grid','display:flex;flex-wrap:wrap;gap:18px;margin:26px 0',cards)+el('p','','padding-top:18px;border-top:1px solid #dcc5d6;text-align:center;font:12px/1.8 Arial,sans-serif;color:#9b7f94;margin:0',esc(rights[-1])))

CSS='''
.anv-celestial *{box-sizing:border-box}
.anv-celestial a:focus-visible{outline:3px solid #bc86b1;outline-offset:4px}
.anv-celestial a{cursor:url('CURSOR') 15 13,pointer}
.anv-celestial .anv-nav-box{transition:transform .25s,box-shadow .25s;position:relative;background:linear-gradient(145deg,#fff8fd,#efddf0)!important}
.anv-celestial .anv-nav-box:first-child{background:linear-gradient(145deg,#a270a0,#69496e)!important;color:#fff1fb!important}
.anv-page-marker:target ~ .anv-tab-navigation > a:first-child{background:linear-gradient(145deg,#fff8fd,#efddf0)!important;color:#78527a!important}
.anv-celestial .anv-nav-box:before{content:'';position:absolute;top:5px;left:10px;right:10px;height:1px;background:#fff}
.anv-celestial .anv-nav-box:hover{transform:translateY(-4px);border-color:#efc2de!important;box-shadow:0 0 20px #edc4e65c,inset 0 0 0 3px #fff!important}
.anv-celestial .anv-nav-box:active{transform:translateY(1px) scale(.98)}
.anv-celestial .anv-action{transition:transform .25s,box-shadow .25s}
.anv-celestial .anv-action:hover{transform:translateY(-3px);box-shadow:0 0 0 3px #fff5,0 5px 17px #c18cbb55!important;background:#fff6fd!important}
.anv-celestial .anv-feature-card,.anv-celestial .anv-edit-card,.anv-celestial .anv-detail-card{transition:transform .4s,box-shadow .4s}
.anv-celestial .anv-feature-card:hover,.anv-celestial .anv-edit-card:hover,.anv-celestial .anv-detail-card:hover{transform:translateY(-6px);box-shadow:0 12px 24px #a7729d33!important}
.anv-celestial .anv-edit-art img{transition:transform .6s}
.anv-celestial .anv-edit-card:hover img{transform:scale(1.025)}
.anv-celestial .anv-divider{animation:anv-glow 5s ease-in-out infinite}
@keyframes anv-glow{0%,100%{opacity:.6}50%{opacity:1;text-shadow:0 0 15px #bd8eae}}
.anv-celestial .anv-page-marker{display:block;height:0;overflow:hidden}
.anv-celestial .anv-tab-panel{display:none}
.anv-celestial .anv-panel-home{display:block}
TARGETS
@media(max-width:700px){.anv-celestial .anv-nav-box{flex-basis:calc(33.333% - 8px)!important;padding:13px 6px!important}.anv-celestial .anv-header{flex-wrap:wrap;justify-content:center!important;text-align:center}.anv-celestial .anv-tagline{display:none}.anv-celestial .anv-hero{min-height:400px!important}.anv-celestial .anv-hero-copy{min-height:400px!important;width:65%!important;padding:80px 5% 60px!important}.anv-celestial h1{font-size:45px!important}.anv-celestial .anv-edit-card{flex:0 1 calc(50% - 8px)!important}.anv-celestial .anv-edit-copy{padding:18px 12px!important}.anv-celestial .anv-edit-copy h3{font-size:22px!important}.anv-celestial .anv-couture{padding:18px!important}.anv-celestial .anv-couture-copy{padding:24px 14px!important}.anv-celestial .anv-copyright{padding:30px 6%!important}.anv-celestial .anv-heading h2{font-size:28px!important}}
@media(prefers-reduced-motion:reduce){.anv-celestial *{animation:none!important;transition:none!important}}
'''

def build():
    markers=''.join(f'<span class="anv-page-marker" id="anv-page-{s}"></span>' for s,_,_ in SECTIONS)
    header=el('div','anv-header','display:flex;justify-content:space-between;align-items:center;gap:20px;padding:24px 4%;background:#302639;color:#fff0fa;border-bottom:1px solid #99758f',el('div','','',el('div','','font:italic 37px/1 Georgia,serif;color:#fff0f8','&#10022; AnivelleShop')+el('div','','font:8px/1.5 Arial,sans-serif;letter-spacing:2.5px;margin-top:9px;color:#dec4d8','ANIME AVATAR FASHION BOUTIQUE'))+el('div','anv-tagline','padding:14px 20px;border:1px solid #76596f;border-radius:24px;background:#413047;font:italic 17px Georgia,serif;color:#e9c9e0','Your world. Your style.'))
    icons=['&#10022;','&#8962;','&#9789;','&#9813;','&#10023;','&#9825;','&#10047;','&#10048;','&#9986;','&#9830;']
    nav=el('div','anv-tab-navigation','display:flex;flex-wrap:wrap;gap:10px;padding:20px 4% 24px;background:#302639;border-bottom:4px double #c6a1b9',''.join(el('a','anv-nav-box','display:block;flex:1 1 calc(20% - 10px);box-sizing:border-box;padding:17px 8px;border:1px solid #c8a7bf;border-radius:15px;background:#f5e6f2;box-shadow:inset 0 0 0 3px #fff5fb;text-align:center;text-decoration:none;color:#78527a;font:15px/1.25 Georgia,serif',icon+' &nbsp; '+esc(label),f' href="#anv-page-{section}" target="_self"') for (section,label,_),icon in zip(SECTIONS,icons)))
    panels=[]; targets=''
    for section,label,_ in SECTIONS:
        record=DATA.get('anivelle-'+section+'.html',{})
        subtitle='Original Anime Avatar Fashion for Your Unique Style' if section=='home' else record['av-sub'][0]
        content=hero(section,subtitle)
        if section=='home': content+=divider()+home_cards()
        elif section=='creator-only': content+=el('div','','padding:30px;margin:30px 4%;border:2px solid #b27d9f;border-radius:20px;background:#f8e8f2;text-align:center;color:#754c70',heading('DO NOT BUY','Creator only')+el('p','','font:17px/1.7 Georgia,serif',esc(record['av-warn-sub'][0]))+el('p','','font:15px/1.7 Georgia,serif',esc(record['av-warn-note'][0])))
        else:
            cards=''.join(el('div','anv-detail-card','flex:1 1 240px;padding:26px;border:1px solid #d9bad2;border-radius:20px;background:#fff7fc',el('div','','font:25px Georgia,serif;color:#b589a9;margin-bottom:15px','&#10023;')+el('h3','','font:italic 24px/1.25 Georgia,serif;color:#76527a;margin:0 0 12px',esc(t))+el('p','','font:15px/1.75 Georgia,serif;color:#896b83;margin:0',esc(d))) for t,d in zip(record['av-show-name'],record['av-show-desc']))
            content+=divider()+el('div','anv-section','padding:30px 4%',heading(subtitle,'Inside the collection')+el('p','','max-width:700px;margin:0 auto 25px;text-align:center;font:16px/1.75 Georgia,serif;color:#886980',esc(record['av-sec-text'][0]))+el('div','','display:flex;flex-wrap:wrap;gap:18px',cards))
        panels.append(el('div',f'anv-tab-panel anv-panel-{section}','',content,' role="region" aria-label="'+esc(label)+'"'))
        targets+=f'#anv-page-{section}:target ~ .anv-tab-panels > .anv-tab-panel'+'{display:none}\n'
        targets+=f'#anv-page-{section}:target ~ .anv-tab-panels > .anv-panel-{section}'+'{display:block}\n'
        targets+=f'#anv-page-{section}:target ~ .anv-tab-navigation > a[href="#anv-page-{section}"]'+'{background:linear-gradient(145deg,#a270a0,#69496e)!important;color:#fff1fb!important;border-color:#f1cce3!important;box-shadow:inset 0 0 0 3px #d9b0d04d,0 0 17px #c49abd66!important}\n'
    css=CSS.replace('TARGETS',targets).replace('CURSOR',HOST+'celestial-cursor-link.png')
    footer=el('div','','padding:32px 4%;text-align:center;background:#302639;color:#e3c7db',el('div','','font:italic 30px Georgia,serif','AnivelleShop')+el('p','','font:12px/1.8 Arial,sans-serif;margin:12px 0 0','Original creations for your unique style.<br>&#169; 2026 Anivelle Studio'))
    body=el('div','anv-celestial','box-sizing:border-box;position:relative;max-width:1100px;margin:0 auto;overflow:hidden;background:#fcf5fb;color:#6f5372;font:16px/1.6 Georgia,serif;text-align:left;border:1px solid #d5b9d0',markers+header+nav+el('div','anv-tab-panels','', ''.join(panels))+divider()+gallery()+divider()+couture()+divider()+rights_notice()+footer)
    code='<!-- One file. Ordinary section links and CSS :target. No input, label, or JavaScript. -->\n<style type="text/css">\n'+css+'\n</style>\n'+body+'\n'
    code=code.encode('ascii','xmlcharrefreplace').decode('ascii')
    assert '<input' not in code and '<label' not in code and '<script' not in code
    assert code.count('class="anv-tab-panel ')==10
    assert 'Discover the Look' not in code and 'Explore Collection' not in code
    folder=OUT/'single-file'; folder.mkdir(exist_ok=True)
    for suffix in ('html','txt'): (folder/f'anivelle-imvu-tabs.{suffix}').write_text(code,encoding='ascii')
    (folder/'preview.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AnivelleShop</title><style>body{margin:0;background:#e9dfeb}</style></head><body>'+code+'</body></html>',encoding='ascii')
    (folder/'README.txt').write_text('SINGLE-FILE CELESTIAL SHOP - SECTION LINKS\n\nPaste all of anivelle-imvu-tabs.txt, replacing the entire previous description.\n\nNavbar: ten boxed links. Plain hash anchors with target=_self (stay inside the description frame) replace the radio/label technique that failed in the supplied saved-page screenshots. CSS :target switches the visible panel and active navbar box. Essential card, copyright and navbar styles are inline. The smaller stylesheet is at the START of the code. No scripts, forms, inputs, labels, or product-page URLs.\n\nGallery: five uniform editorial cards. Copyright: solid framed panel and two inset cards. Couture: Clothing and Accessories section links.\n\nThe live IMVU save filter still needs verification: it must retain href fragments, IDs and :target selectors for same-file switching. If the whole stylesheet is removed, all sections remain visible rather than disappearing. No code can restore attributes that the platform deletes. The older simple-link edition is kept separately.\n',encoding='ascii')
    print(f'Built {len(code):,}-byte file: ten hash-link panels, inline visuals, no radio controls.')

if __name__=='__main__': build()
