"""Single-document CSS-only section switching; IMVU save-filter test required."""
from build_anivelle import OUT, HOST, CSS, DATA, CATEGORIES, HEADLINES, HERO, SECTIONS
from build_anivelle import esc, heading, moodboard, editorial, imvu_link_fallback, imvu_symbol_css
from pathlib import Path
import re

def asset(name): return HOST+name+'.webp'

def divider():
    return '<div class="anv-section-divider" aria-hidden="true"><span class="anv-divider-wing"></span><span class="anv-divider-orbit"><span>&#10022;</span></span><span class="anv-divider-wing"></span></div>'

def enhanced_gallery():
    items=[('arrival-lunar-dress','Moonlit Silhouettes','Soft layers with a little midnight drama.'),('arrival-frill-dress','Pearl & Petal','Delicate frills, gentle glow, effortless charm.'),('arrival-cape-set','Wrapped in Starlight','Flowing fabric and celestial finishing touches.'),('arrival-rose-braids','Ribbon Daydreams','Romantic strands with a playful twist.'),('arrival-orbit-bow','Little Luxuries','A golden star. A silk bow. Your signature detail.')]
    cards=''.join(f'<div class="anv-art-frame"><div class="anv-gallery-image"><img src="{asset(image)}" width="1024" height="1024" alt="{esc(title)} illustration" loading="lazy"></div><div class="anv-gallery-caption"><span class="anv-gallery-star" aria-hidden="true">&#10023;</span><h3>{esc(title)}</h3><p>{esc(text)}</p></div></div>' for image,title,text in items)
    return '<div class="anv-section anv-moodboard" id="anv-gallery">'+heading('The Celestial Edit','A little inspiration, a little magic')+'<p class="anv-gallery-copy">Build a look around the details you love: a dreamy silhouette, a ribbon in your hair, a touch of starlight.<br>Mix the soft with the striking. Make the whole story yours.</p><div class="anv-gallery">'+cards+'</div><div class="anv-gallery-note"><span aria-hidden="true">&#10022;</span> An expression of your world, one beautiful detail at a time. <span aria-hidden="true">&#10022;</span></div></div>'

def enhanced_couture():
    return '<div class="anv-editorial anv-couture"><img src="'+asset('atelier-banner')+'" width="1536" height="1024" alt="Celestial couture atelier" loading="lazy"><div class="anv-editorial-copy"><span class="anv-couture-eyebrow">The art of your signature style</span><h2>Celestial Couture</h2><p>A curated world of dreamy details<br>for your anime avatar.</p><p class="anv-couture-note">Silken ribbons. Luminous layers. A little everyday magic.</p><div class="anv-couture-actions"><label for="anv-page-clothing">View Clothing <span aria-hidden="true">&#10023;</span></label><label for="anv-page-accessories">Style with Accessories <span aria-hidden="true">&#10023;</span></label></div></div><span class="anv-couture-spark" aria-hidden="true">&#10022;</span></div>'

def rights_notice():
    rights=DATA['anivelle-shop.html']['rights']
    return '<div class="anv-copyright" id="anv-copyright"><div class="anv-copyright-heading"><span class="anv-copyright-seal" aria-hidden="true">&#169;</span><div><span class="anv-eyebrow">Respect the creator. Respect the craft.</span><h2>Copyright &amp; DMCA Warning</h2></div></div><p class="anv-copyright-lead">Do not copy or reupload.</p><p>'+esc(rights[1])+'</p><div class="anv-rights-points"><div><h3>Original work, treated with care</h3><p>Keep Anivelle Studio textures, meshes, designs and assets out of unauthorized copies or redistributions.</p></div><div><h3>Check the listing permissions</h3><p>Derive or edit only where the product listing permits it. Contact the creator when permission is unclear.</p></div></div><p class="anv-copyright-foot">'+esc(rights[-1])+'</p></div>'

ENHANCEMENTS=r'''
/* All effects are decorative CSS; tab changes remain native label/radio actions. */
.anv-tab-app label{cursor:url('https://raw.githubusercontent.com/anyavibez/ImageHosting/main/AnivelleShop/celestial-v1/assets/celestial-cursor-link.png') 15 13,pointer}
.anv-tab-app .anv-header{background:radial-gradient(ellipse at 100% 0,#82517244,transparent 65%),linear-gradient(110deg,#3c3046,#292334)}
.anv-tab-app .anv-tab-hint{display:flex;align-items:center;gap:11px;padding:11px 17px;border:1px solid #d5a8c13d;border-radius:25px;background:linear-gradient(120deg,#d9a5cb12,#f9deec05);box-shadow:inset 0 1px #ffe5f91a;font:italic 18px/1.35 Georgia,serif;white-space:nowrap}
.anv-tab-app .anv-tab-hint small{display:block;margin-top:4px;text-align:center;font:9px/1.3 Arial,sans-serif;letter-spacing:.22em;text-transform:uppercase;color:#c7abc8}
.anv-tab-app .anv-hint-star{color:#efc4d8;font:21px Georgia,serif;animation:anv-emblem-glow 5s ease-in-out infinite}
.anv-tab-app .anv-hint-star:last-child{animation-delay:-2.5s}
.anv-tab-app .anv-tab-navigation{gap:7px;padding:15px 2%;background:radial-gradient(ellipse at 50% 100%,#7850743b,transparent 70%),#302638;border-bottom:3px double #bf93b3}
.anv-tab-app .anv-tab-navigation label{isolation:isolate;overflow:hidden;display:inline-flex;align-items:center;gap:7px;padding:10px 12px;border:1px solid #a581a244;border-radius:13px 5px 13px 5px;background:linear-gradient(150deg,#f6ceeb08,#ffffff02);box-shadow:inset 0 1px #fff1;transition:transform .25s,border-color .3s,box-shadow .3s,background .3s}
.anv-tab-app .anv-tab-navigation label:before{content:'';position:absolute;inset:0;pointer-events:none;background:linear-gradient(110deg,transparent 32%,#ffe3f726 50%,transparent 68%);transform:translateX(-150%)}
.anv-tab-app .anv-tab-navigation label:hover:before{animation:anv-sheen .8s ease}
.anv-tab-app .anv-tab-navigation label:hover{border-color:#e8bad5;box-shadow:0 4px 17px #e9b0d336,inset 0 0 13px #d8a3cc13;transform:translateY(-3px)}
.anv-tab-app .anv-tab-navigation label:active{transform:translateY(1px) scale(.97)}
.anv-tab-app .anv-nav-glint{color:#e9bed8;font-size:16px;opacity:.55;transition:transform .4s,opacity .4s;text-shadow:0 0 9px #f7c5e3}
.anv-tab-app .anv-tab-navigation label:hover .anv-nav-glint{opacity:1;transform:rotate(45deg)}
.anv-tab-app .anv-section-divider{position:relative;display:flex;align-items:center;justify-content:center;gap:18px;height:58px;margin:7px 4%;pointer-events:none;overflow:hidden}
.anv-tab-app .anv-divider-wing{position:relative;height:1px;width:36%;background:linear-gradient(90deg,transparent,#c899b9 80%,#e8c7d9);overflow:hidden}
.anv-tab-app .anv-divider-wing:last-child{transform:rotate(180deg)}
.anv-tab-app .anv-divider-wing:after{content:'';position:absolute;left:0;top:0;width:35%;height:1px;background:linear-gradient(90deg,transparent,#fff9ff,transparent);animation:anv-divider-light 6s ease-in-out infinite}
.anv-tab-app .anv-divider-orbit{display:grid;place-items:center;position:relative;width:34px;height:34px;border:1px solid #c79db8;border-radius:50%;color:#ac789d;background:#fff6fc9c;box-shadow:0 0 18px #e6c0dc55}
.anv-tab-app .anv-divider-orbit:before{content:'';position:absolute;inset:5px -8px;border:1px solid #d5afc888;border-radius:50%;transform:rotate(-35deg)}
.anv-tab-app .anv-divider-orbit>span{font-size:23px;animation:anv-emblem-glow 6s ease-in-out infinite}
.anv-tab-app .anv-premium-card{min-height:280px;box-shadow:0 0 0 4px #fff4fc,0 0 0 5px #d9afca,0 8px 23px #a16a9e25;transform-style:preserve-3d}
.anv-tab-app .anv-premium-card .anv-collection-label{width:70%;min-height:280px;padding:27px 17px 62px;background:linear-gradient(90deg,#2e213cd6,#30213b3b 95%,transparent)}
.anv-tab-app .anv-premium-card .anv-collection-label h3{font-size:31px;max-width:8ch;line-height:1.07;margin:11px 0 12px}
.anv-tab-app .anv-premium-card .anv-collection-label p{font-size:14px;max-width:19ch;color:#f4dfed}
.anv-tab-app .anv-card-eyebrow{display:block;max-width:20ch;color:#ecc4df;font:10px/1.5 Arial,sans-serif;letter-spacing:.1em;text-transform:uppercase}
.anv-tab-app .anv-card-crown{position:absolute;right:13px;top:12px;font:26px Georgia,serif;color:#ffe3ef;text-shadow:0 0 15px #f5c0dc;z-index:2;transition:transform .5s}
.anv-tab-app .anv-premium-card:hover .anv-card-crown{transform:rotate(90deg) scale(1.1)}
.anv-tab-app .anv-card-action{position:absolute;bottom:19px;left:18px;display:inline-flex;align-items:center;gap:9px;padding:5px 12px;border:1px solid #e7b9d1;border-radius:22px;background:linear-gradient(120deg,#b888ad99,#74557899);font-size:14px;box-shadow:inset 0 1px #ffe6f333;transition:background .3s,box-shadow .3s}
.anv-tab-app .anv-premium-card:hover .anv-card-action{background:#bc8eb5bf;box-shadow:0 0 15px #f3bfd57d}
.anv-tab-app .anv-detail-card{position:relative;isolation:isolate;overflow:hidden;border-radius:18px 7px 18px 7px;background:linear-gradient(145deg,#fffafd,#f2e5f3);box-shadow:inset 0 0 0 4px #fffb,0 4px 13px #9965940b;transition:transform .35s,box-shadow .35s,border-color .35s;padding:25px 22px}
.anv-tab-app .anv-detail-card:after{content:'';position:absolute;inset:0;pointer-events:none;background:linear-gradient(115deg,transparent 30%,#fff8 50%,transparent 70%);transform:translateX(-150%)}
.anv-tab-app .anv-detail-card:hover{transform:translateY(-5px);border-color:#ba86b4;box-shadow:inset 0 0 0 4px #fff9,0 8px 23px #ac77a32b}
.anv-tab-app .anv-detail-card:hover:after{animation:anv-sheen .9s ease}
.anv-tab-app .anv-detail-spark{display:inline-grid;place-items:center;width:33px;height:33px;border:1px solid #cfabc9;border-radius:50%;color:#a26d98;background:#fff7fc;margin-bottom:15px;box-shadow:0 0 13px #e6c6dc50;font-size:21px}
.anv-tab-app .anv-gallery-copy{max-width:76ch;margin:0 auto 28px;line-height:1.7;font-size:16px}
.anv-tab-app .anv-gallery{align-items:flex-start;gap:13px;padding-top:16px;padding-bottom:22px}
.anv-tab-app .anv-art-frame,.anv-tab-app .anv-art-frame:nth-child(3){width:18%;margin-top:0;padding:5px;border-radius:44% 44% 14px 14px;background:linear-gradient(#fff8fd,#f1e3f2);box-shadow:0 7px 17px #93678e24;overflow:hidden}
.anv-tab-app .anv-art-frame:nth-child(2),.anv-tab-app .anv-art-frame:nth-child(4){margin-top:24px}
.anv-tab-app .anv-gallery-image{overflow:hidden;border-radius:48% 48% 9px 9px}
.anv-tab-app .anv-gallery-image img{transition:transform .7s;object-fit:cover}
.anv-tab-app .anv-art-frame:hover img{transform:scale(1.06)}
.anv-tab-app .anv-gallery-caption{padding:12px 9px 18px;text-align:center}
.anv-tab-app .anv-gallery-caption h3{font:italic 18px/1.2 Georgia,serif;margin:6px 0 8px;color:#624267}
.anv-tab-app .anv-gallery-caption p{font:14px/1.55 Georgia,serif;color:#8a6b85}
.anv-tab-app .anv-gallery-star{color:#b483a5;font-size:21px}
.anv-tab-app .anv-gallery-note{text-align:center;max-width:64ch;margin:13px auto 0;color:#91688a;font:italic 16px/1.7 Georgia,serif}
.anv-tab-app .anv-gallery-note>span{color:#b4879e;font-size:16px;padding:0 8px}
.anv-tab-app .anv-couture{min-height:320px;padding:33px 5%;margin:5px 3% 20px;box-shadow:0 0 0 4px #fff5,0 10px 28px #92618d2e}
.anv-tab-app .anv-couture .anv-editorial-copy{position:relative;width:63%}
.anv-tab-app .anv-couture h2{font-size:43px;margin:15px 0}
.anv-tab-app .anv-couture-eyebrow{font:10px/1.5 Arial,sans-serif;letter-spacing:.18em;text-transform:uppercase;color:#f1c9e2}
.anv-tab-app .anv-couture-note{font-style:italic;font-size:14px;color:#ebcde3;margin-top:14px!important}
.anv-tab-app .anv-couture-actions{display:flex;gap:11px;flex-wrap:wrap;justify-content:center;margin-top:21px}
.anv-tab-app .anv-couture-actions label{display:inline-flex;align-items:center;justify-content:center;gap:10px;position:relative;overflow:hidden;min-height:40px;padding:8px 17px;border:1px solid #efcce0;border-radius:21px 8px;background:linear-gradient(120deg,#fff2fbe6,#e8cde3e6);color:#68416b;font:15px/1.4 Georgia,serif;box-shadow:inset 0 0 0 3px #fff4;transition:transform .25s,box-shadow .25s,background .25s}
.anv-tab-app .anv-couture-actions label:hover{transform:translateY(-3px);background:#fff0fa;box-shadow:inset 0 0 0 3px #fff6,0 0 22px #efbddd7d}
.anv-tab-app .anv-couture-actions label:active{transform:translateY(1px)}
.anv-tab-app .anv-couture-spark{position:absolute;right:25px;top:20px;font-size:36px;color:#f4c6df;text-shadow:0 0 22px #f1b9dd;animation:anv-emblem-glow 5s ease-in-out infinite}
.anv-tab-app .anv-copyright{position:relative;padding:33px 4%;margin:0 3% 35px;border:1px solid #cfacc5;border-radius:22px 8px 22px 8px;background:linear-gradient(145deg,#fff8fded,#eddfefed);box-shadow:inset 0 0 0 5px #fff6,0 8px 24px #94659117;color:#715375}
.anv-tab-app .anv-copyright:before{content:'';position:absolute;inset:7px;border:1px solid #e3c9dd;border-radius:16px 5px 16px 5px;pointer-events:none}
.anv-tab-app .anv-copyright-heading{display:flex;align-items:center;gap:18px;margin-bottom:23px}
.anv-tab-app .anv-copyright-heading h2{font-size:31px;color:#603d65}
.anv-tab-app .anv-copyright-heading h2>.anv-heading-star{display:none}
.anv-tab-app .anv-copyright-heading .anv-eyebrow{font-size:10px;margin-bottom:6px}
.anv-tab-app .anv-copyright-seal{display:inline-grid;place-items:center;flex:none;width:55px;height:55px;border:3px double #bb8bae;border-radius:50%;color:#a16e96;background:#fbf0f9;box-shadow:0 0 20px #e6bdd744;font:31px Georgia,serif}
.anv-tab-app .anv-copyright>p{font-size:15px;line-height:1.7;max-width:90ch}
.anv-tab-app .anv-copyright .anv-copyright-lead{font:italic 23px/1.4 Georgia,serif;color:#67406b;margin-bottom:12px}
.anv-tab-app .anv-rights-points{display:flex;gap:15px;margin:24px 0;padding:0}
.anv-tab-app .anv-rights-points>div{flex:1;padding:19px;border:1px solid #dbc0d6;border-radius:13px;background:#fff6fb91}
.anv-tab-app .anv-rights-points h3{font:italic 20px/1.25 Georgia,serif;margin-bottom:10px;color:#69476d}
.anv-tab-app .anv-rights-points p{font-size:14px;line-height:1.6;color:#896d85}
.anv-tab-app .anv-copyright .anv-copyright-foot{font-size:13px;color:#9a7a93;border-top:1px solid #ddc5d9;padding-top:16px}
@keyframes anv-divider-light{0%,15%{transform:translateX(-150%)}65%,100%{transform:translateX(430%)}}
@keyframes anv-emblem-glow{0%,100%{opacity:.6;filter:drop-shadow(0 0 2px #eab2d3);transform:scale(.95)}50%{opacity:1;filter:drop-shadow(0 0 7px #f0bddb);transform:scale(1.1)}}
@media(max-width:850px){.anv-tab-app .anv-tab-hint{font-size:16px;padding:10px 12px}.anv-tab-app .anv-premium-card .anv-collection-label h3{font-size:26px}.anv-tab-app .anv-card-eyebrow{font-size:9px}.anv-tab-app .anv-premium-card .anv-collection-label{width:78%}.anv-tab-app .anv-couture .anv-editorial-copy{width:70%}.anv-tab-app .anv-couture h2{font-size:36px}}
@media(max-width:600px){.anv-tab-app .anv-tab-hint{display:none}.anv-tab-app .anv-tab-navigation{gap:7px;padding:12px 3%}.anv-tab-app .anv-tab-navigation label{padding:8px 9px;font-size:13px;gap:5px}.anv-tab-app .anv-nav-glint{font-size:13px}.anv-tab-app .anv-section-divider{height:44px;gap:13px}.anv-tab-app .anv-premium-card .anv-collection-label{width:65%;min-height:260px}.anv-tab-app .anv-premium-card{min-height:260px}.anv-tab-app .anv-premium-card .anv-collection-label h3{font-size:31px}.anv-tab-app .anv-card-eyebrow{font-size:10px}.anv-tab-app .anv-gallery-copy{font-size:15px;padding:0 2%}.anv-tab-app .anv-art-frame,.anv-tab-app .anv-art-frame:nth-child(3){width:43%;margin-top:0}.anv-tab-app .anv-art-frame:nth-child(2),.anv-tab-app .anv-art-frame:nth-child(4){margin-top:15px}.anv-tab-app .anv-gallery-caption{padding:12px 7px 15px}.anv-tab-app .anv-gallery-caption h3{font-size:20px}.anv-tab-app .anv-gallery-caption p{font-size:14px}.anv-tab-app .anv-gallery-note{font-size:15px}.anv-tab-app .anv-couture{padding:31px 5%;min-height:350px}.anv-tab-app .anv-couture .anv-editorial-copy{width:100%}.anv-tab-app .anv-couture h2{font-size:36px}.anv-tab-app .anv-couture-actions{gap:10px}.anv-tab-app .anv-couture-actions label{padding:9px 13px;font-size:14px}.anv-tab-app .anv-copyright{padding:26px 6%;margin:0 4% 25px}.anv-tab-app .anv-copyright-heading{gap:12px;align-items:flex-start}.anv-tab-app .anv-copyright-heading h2{font-size:26px}.anv-tab-app .anv-copyright-seal{width:43px;height:43px;font-size:25px}.anv-tab-app .anv-rights-points{flex-direction:column}.anv-tab-app .anv-copyright-heading .anv-eyebrow{font-size:9px;letter-spacing:.12em}}
@media(prefers-reduced-motion:reduce){.anv-tab-app *,.anv-tab-app *:before,.anv-tab-app *:after{animation:none!important;transition:none!important}}
'''

def hero(section,title,subtitle):
    image='boutique-hero' if section=='home' else HERO.get(section,section)+'-hero'
    a,b=('Your','Anime Era') if section=='home' else HEADLINES[section]
    return f'<div class="anv-hero"><img class="anv-hero-art" src="{asset(image)}" width="1536" height="1024" alt="Celestial {esc(title)} illustration"><div class="anv-hero-copy"><h1>{esc(a)}<br><em>{esc(b)}</em></h1><p class="anv-hero-sub">{esc(subtitle)}</p><div class="anv-hero-divider"><span>&#10022;</span></div></div><span class="anv-ribbon" aria-hidden="true"></span></div>'

def build():
    radios=''.join(f'<input class="anv-page-radio" type="radio" name="anv-page" id="anv-page-{s}" aria-label="{esc(l)}"'+(' checked="checked"' if s=='home' else '')+'>' for s,l,_ in SECTIONS)
    nav='<div class="anv-tab-navigation" aria-label="Choose a shop section">'+''.join(f'<label id="anv-tab-label-{s}" for="anv-page-{s}"><span class="anv-nav-glint" aria-hidden="true">&#10023;</span>{esc(l)}</label>' for s,l,_ in SECTIONS)+'</div>'
    header='<div class="anv-header"><div class="anv-brand"><span class="anv-brand-mark">&#10022;</span><span><span class="anv-brand-name">AnivelleShop</span><small>Anime Avatar Fashion Boutique</small></span></div><div class="anv-tab-hint"><span class="anv-hint-star" aria-hidden="true">&#10023;</span><span>Your world. Your style.<small>The Celestial Atelier</small></span><span class="anv-hint-star" aria-hidden="true">&#10023;</span></div></div>'
    panels=[]
    for section,label,_ in SECTIONS:
        if section=='home':
            body=hero('home','Boutique','Original Anime Avatar Fashion for Your Unique Style')
            covers=[('clothing','Celestial Gala','collection-gala','Couture daydreams','Luminous layers for your main-character moment.'),('body','Dreamy Twin Tails','collection-twintails','Soft, playful, entirely you','Romantic strands and ribbon-tied possibilities.'),('accessories','Starlit Accessories','collection-starlit','A touch of something magical','Little finishing touches. Lasting personality.')]
            body+=divider()+'<div class="anv-section">'+heading('Featured Collections','Choose your next chapter')+'<div class="anv-collection-grid">'+''.join(f'<label class="anv-collection anv-premium-card" for="anv-page-{target}"><img src="{asset(image)}" width="1536" height="1024" alt="{title}"><span class="anv-card-crown" aria-hidden="true">&#10022;</span><div class="anv-collection-label"><span class="anv-card-eyebrow">{esc(tag)}</span><h3>{title}</h3><p>{esc(desc)}</p><span class="anv-card-action">View Collection <span aria-hidden="true">&#10023;</span></span></div></label>' for target,title,image,tag,desc in covers)+'</div></div>'
        else:
            record=DATA['anivelle-'+section+'.html']
            body=hero(section,label,record['av-sub'][0])
            if section=='creator-only':
                body+='<div class="anv-warning"><h2>DO NOT BUY</h2><h3>'+esc(record['av-warn-sub'][0])+'</h3><p>'+esc(record['av-warn-note'][0])+'</p><strong>Not for sale · Creator only</strong></div>'
            else:
                body+=divider()+'<div class="anv-section">'+heading(record['av-sub'][0],'Inside the collection')+f'<p class="anv-panel-intro">{esc(record["av-sec-text"][0])}</p><div class="anv-spotlight-grid">'+''.join(f'<div class="anv-spotlight anv-detail-card"><span class="anv-detail-spark" aria-hidden="true">&#10023;</span><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t,d in zip(record['av-show-name'],record['av-show-desc']))+'</div></div>'
        panels.append(f'<div class="anv-tab-panel anv-panel-{section}" role="region" aria-labelledby="anv-tab-label-{section}">{body}</div>')
    body='<div class="anv-celestial anv-tab-app" style="background-image:url(\''+asset('celestial-silk')+'\')">'+radios+header+nav+'<div class="anv-tab-panels">'+''.join(panels)+'</div>'+divider()+enhanced_gallery()+divider()+enhanced_couture()+divider()+rights_notice()+'<div class="anv-footer"><div class="anv-brand-name">AnivelleShop</div><p>Original creations for your unique style.</p><div class="anv-footer-bottom"><span>&#169; 2026 Anivelle Studio</span><span>Made for your anime era.</span></div></div></div>'
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
        base+=f'#anv-page-{section}:checked ~ .anv-tab-navigation > label[for="anv-page-{section}"] .anv-nav-glint'+'{opacity:1;color:#fff0f8;transform:rotate(45deg)}\n'
    code='<!-- Single-file CSS tabs. Requires IMVU to retain INPUT, LABEL, and :checked CSS. No JavaScript. -->\n'+imvu_link_fallback(body)+'\n<style type="text/css">\n'+imvu_symbol_css(CSS)+base+ENHANCEMENTS+'\n</style>\n'
    code=code.encode('ascii','xmlcharrefreplace').decode('ascii')
    assert code.count('type="radio"')==10 and code.count('checked="checked"')==1
    assert code.count('class="anv-tab-panel ')==10 and '<script' not in code
    assert 'New Arrivals' not in code and 'Explore Collection' not in code
    assert 'Discover the Look' not in code and 'Open Shop' not in code
    assert 'Copyright &amp; DMCA Warning' in code and 'anv-copyright' in code
    folder=OUT/'single-file'; folder.mkdir(exist_ok=True)
    (folder/'anivelle-imvu-tabs.html').write_text(code,encoding='ascii')
    (folder/'anivelle-imvu-tabs.txt').write_text(code,encoding='ascii')
    preview='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AnivelleShop · Single-file tabs</title><style>body{margin:0;background:#e9deed}</style></head><body>'+code+'</body></html>'
    (folder/'preview.html').write_text(preview,encoding='utf-8')
    (folder/'README.txt').write_text('SINGLE-FILE PAGE SWITCHING\n\nPaste all of anivelle-imvu-tabs.txt into one IMVU description. Clicking a category LABEL changes the selected radio and visible panel in this same document; it does not navigate to another URL. All ten sections are included.\n\nNo JavaScript, no form submission, no product-page URLs are used for the tabs. Images load from GitHub.\n\nIMPORTANT: This is a CSS-only tabs candidate. It requires IMVU to retain INPUT type=radio, LABEL/for attributes, and :checked sibling selectors when saving. Browser operation is verified separately; the live IMVU filter is not verified. If these controls are removed, this technique cannot work there. The previous simple-link edition is preserved.\n\nENHANCED EDITION\nGallery captions, premium cards, glowing navigation, animated star dividers, and Copyright & DMCA Warning are included. The Couture buttons select Clothing and Accessories in this same file. Your world. Your style. is retained with refreshed styling.\n',encoding='ascii')
    print('Built one HTML/TXT file with ten CSS-only panels. IMVU save-filter test still required.')

if __name__=='__main__': build()
