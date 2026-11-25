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
        super().__init__(); self.ids=[]; self.links=[]; self.images=[]; self.headings=0; self.stack=[]
        self.feed(html)
        assert not self.stack, f'Unclosed HTML elements: {self.stack}'
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag=='a':
            self.links.append(a.get('href',''))
            assert a.get('href'), 'Empty link'
            if a.get('target')=='_blank': assert 'noopener' in a.get('rel',''), 'Missing rel=noopener'
        if tag=='img':
            assert a.get('alt'), 'Image missing meaningful alternative text'
            self.images.append(a['src'])
        if tag=='h1': self.headings+=1
        if tag not in {'img','br','hr','meta','link','input','source','wbr','area','base','embed','param','track','col'}: self.stack.append(tag)
    def handle_endtag(self, tag):
        assert self.stack and self.stack[-1]==tag, f'Mismatched closing {tag}; open {self.stack[-4:]}'
        self.stack.pop()

def validate():
    data=json.loads((OUT/'content.json').read_text(encoding='utf-8'))
    manifest=json.loads((OUT/'asset-manifest.json').read_text(encoding='utf-8'))
    assert len(manifest['assets'])==18
    used=set(); pages=list((OUT/'pages').glob('*.html'))+[OUT/'index.html']
    assert len(pages)==10
    for file in pages:
        text=file.read_text(encoding='utf-8'); p=Page(text)
        assert p.headings==1, f'{file.name}: expected one h1'
        assert len(p.ids)==len(set(p.ids)), f'{file.name}: duplicate IDs'
        assert '<script' not in text, 'Shop must work without scripts'
        assert not re.search(r'devil|pentagram|Pirata One|dlx-cursor|av-fire|2b\.png',text,re.I)
        for ref in p.images+p.links:
            if ref.startswith('#'): assert ref[1:] in p.ids, f'Invalid anchor {ref}'
            elif not urlparse(ref).scheme: assert (file.parent/ref).resolve().is_file(), f'Missing local file {ref} from {file}'
        for src in p.images: used.add(Path(src).name)
    for name,record in data.items():
        html=(OUT/'embeds'/name).read_text(encoding='utf-8'); p=Page(html)
        assert p.headings==1
        assert (OUT/'embeds'/name.replace('.html','.txt')).read_text(encoding='utf-8')==html
        for original in record['original_links']:
            assert original['href'] in p.links, f'Lost original catalogue URL: {original["text"]}'
        for key in ['av-show-name','av-show-desc','av-card-title','av-card-text','av-warn-note','av-co-item-desc']:
            for content in record[key]: assert content in unescape(html), f'Lost content {content}'
        assert all(src.startswith('https://raw.githubusercontent.com/anyavibez/ImageHosting/main/AnivelleShop/celestial-v1/assets/') for src in p.images)
        if 'creator-only' in name:
            assert 'DO NOT BUY' in html and 'Not for sale' in html
            assert 'Read creator note' in html and 'Explore creator' not in html
    for asset in manifest['assets']:
        file=OUT/asset['file']
        assert hashlib.sha256(file.read_bytes()).hexdigest()==asset['sha256']
        assert file.name in used, f'Unused generated asset {file.name}'
    css=(OUT/'celestial.css').read_text(encoding='utf-8')
    assert 'prefers-reduced-motion' in css and '@container(max-width:600px)' in css
    summary={'standalone_pages':10,'shop_pages':9,'IMVU_HTML_embeds':9,'IMVU_TXT_embeds':9,'generated_assets':18,'all_assets_used':True,'original_catalogue_links_preserved':True,'existing_page_content_preserved':True,'html_nesting':'valid','local_links':'valid','reduced_motion':'supported'}
    (OUT/'validation.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': validate()
