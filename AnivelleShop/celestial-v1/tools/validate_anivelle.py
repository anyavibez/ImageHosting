"""Check actual delivery files, embedded links, content preservation, and asset integrity."""
from pathlib import Path
from html.parser import HTMLParser
from html import unescape
from urllib.parse import urlparse
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT if (ROOT/'content.json').exists() else ROOT/'AnivelleShop'

class Page(HTMLParser):
    def __init__(self, html):
        super().__init__(); self.ids=[]; self.links=[]; self.images=[]; self.headings=0; self.stack=[]; self.sections={}; self.active=[]; self.section_context={}; self.link_attributes=[]; self.artwork_in_links=0
        self.feed(html)
        assert not self.stack, f'Unclosed HTML elements: {self.stack}'
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        for cls in a.get('class','').split():
            if cls.startswith('active-'): self.active.append(cls[7:])
            if cls.startswith('anv-link-') and cls[9:] in {'home','shop','rooms','clothing','accessories','avatar-poses','body','pets','cutouts','creator-only'}:
                if tag=='a': self.sections[cls[9:]]=a.get('href')
                else: self.section_context[len(self.stack)]=cls[9:]
        if 'id' in a: self.ids.append(a['id'])
        if tag=='a':
            self.link_attributes.append(a)
            if self.section_context: self.sections[self.section_context[max(self.section_context)]]=a.get('href')
            self.links.append(a.get('href',''))
            assert a.get('href'), 'Empty link'
            if a.get('target')=='_blank': assert 'noopener' in a.get('rel',''), 'Missing rel=noopener'
        if tag=='img':
            if 'a' in self.stack: self.artwork_in_links+=1
            assert a.get('alt'), 'Image missing meaningful alternative text'
            self.images.append(a['src'])
        if tag=='h1': self.headings+=1
        if tag not in {'img','br','hr','meta','link','input','source','wbr','area','base','embed','param','track','col'}: self.stack.append(tag)
    def handle_endtag(self, tag):
        assert self.stack and self.stack[-1]==tag, f'Mismatched closing {tag}; open {self.stack[-4:]}'
        self.stack.pop()
        self.section_context.pop(len(self.stack),None)

def validate():
    data=json.loads((OUT/'content.json').read_text(encoding='utf-8'))
    manifest=json.loads((OUT/'asset-manifest.json').read_text(encoding='utf-8'))
    assert len(manifest['assets'])==28
    used=set(); pages=list((OUT/'pages').glob('*.html'))+[OUT/'index.html']
    assert len(pages)==10
    for file in pages:
        text=file.read_text(encoding='utf-8'); p=Page(text)
        assert p.headings==1, f'{file.name}: expected one h1'
        assert len(p.ids)==len(set(p.ids)), f'{file.name}: duplicate IDs'
        assert '<script' not in text, 'Shop must work without scripts'
        assert 'anv-arrival-grid' in text and 'anv-card-flourish' in text
        assert 'anv-arrivals' in p.ids
        section='home' if file.name=='index.html' else file.stem.removeprefix('anivelle-')
        assert p.active==[section], f'Incorrect active section in {file.name}'
        assert len(p.sections)==10
        for target,url in p.sections.items():
            linked=(file.parent/url).resolve()
            assert linked.is_file(), f'Broken navbar target {url}'
            dest=Page(linked.read_text(encoding='utf-8'))
            assert dest.active==[target], f'{section} nav opens wrong active section {target}'
        assert not re.search(r'devil|pentagram|Pirata One|dlx-cursor|av-fire|2b\.png',text,re.I)
        for ref in p.images+p.links:
            if ref.startswith('#'): assert ref[1:] in p.ids, f'Invalid anchor {ref}'
            elif not urlparse(ref).scheme: assert (file.parent/ref).resolve().is_file(), f'Missing local file {ref} from {file}'
        for src in p.images+re.findall(r"url\('([^']+)'\)",text): used.add(Path(src).name)
    common=(OUT/'common'/'anivelle-common.html').read_text(encoding='ascii')
    for name in [*data,'anivelle-home.html']:
        section=name.removeprefix('anivelle-').removesuffix('.html')
        html=(OUT/'embeds'/name).read_text(encoding='utf-8'); p=Page(html)
        assert p.headings==1
        assert html.isascii(), 'IMVU snippet must use ASCII with numeric HTML entities'
        assert p.artwork_in_links==0, 'IMVU artwork must not be nested inside links'
        assert not re.search(r'\\272[67]',html), 'IMVU CSS must not contain backslash star escapes'
        assert all(set(a)=={'href','target'} and a['target']=='_top' for a in p.link_attributes), 'IMVU links must use only plain href and target attributes'
        filtered=re.sub(r'<a\b[^>]*>.*?</a>','',html,flags=re.S).replace('\\','')
        fp=Page(filtered)
        assert len(fp.images)==len(p.images), 'Images must survive removal of link blocks'
        for label in ['AnivelleShop','Clothing','Accessories','Lunar Waltz Dress','Starlit','New Arrivals']:
            assert label in unescape(filtered), f'Visible label lost if links are removed: {label}'
        assert '2726' not in filtered and '2727' not in filtered
        assert not re.search(r'<(?:svg|script|iframe|form|input|button|header|footer|nav|section|article|details|summary)\b',html,re.I)
        assert (OUT/'embeds'/name.replace('.html','.txt')).read_text(encoding='utf-8')==html
        assert p.active==[section] and len(p.sections)==10
        assert html.replace('class="anv-celestial active-'+section+'"','class="anv-celestial active-home"',1)==common, 'Fragments must differ ONLY in the active class'
        for url in p.sections.values(): assert url.startswith('https://www.imvu.com/shop/web_search.php?') and 'keywords=anivellestudio' in url
        assert all(src.startswith('https://raw.githubusercontent.com/anyavibez/ImageHosting/main/AnivelleShop/celestial-v1/assets/') for src in p.images)
        if 'creator-only' in name:
            assert 'DO NOT BUY' in html and 'Not for sale' in html
            assert 'anv-creator-message' in html and 'Explore creator' not in html
    for asset in manifest['assets']:
        file=OUT/asset['file']
        assert hashlib.sha256(file.read_bytes()).hexdigest()==asset['sha256']
        # Earlier collection art remains available in the asset bundle for reuse.
    css=(OUT/'celestial.css').read_text(encoding='utf-8')
    assert 'prefers-reduced-motion' in css and '@media(max-width:600px)' in css
    assert '@container' not in css and 'cqw' not in css and '@import' not in css
    home=(OUT/'embeds'/'anivelle-home.html').read_text(encoding='ascii')
    hp=Page(home)
    assert hp.headings==1 and 'anv-arrivals' in hp.ids and '<svg' not in home
    assert len(list((OUT/'embeds').glob('*.html')))==10
    assert len(used)==11
    summary={'standalone_pages':10,'IMVU_HTML_embeds':10,'IMVU_TXT_embeds':10,'generated_assets_available':28,'shared_layout_assets':len(used),'same_layout_all_pages':True,'only_active_class_differs':True,'navbar_destinations':'all 100 local section links verified','active_sections':'all 10 verified','html_nesting':'valid','local_links':'valid','symbols':'ASCII HTML entities','scripts_svg_forms':'none','reduced_motion':'supported'}
    (OUT/'validation.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': validate()
