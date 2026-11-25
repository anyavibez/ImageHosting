"""Preserve the user-supplied default; vary only each page's checked radio."""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
import re
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT if (ROOT/'content.json').exists() else ROOT/'AnivelleShop'
SECTIONS=['home','shop','rooms','clothing','accessories','avatar-poses','body','pets','cutouts','creator-only']

def enhance(default):
    particles='<span class="anv-hover-sparks" aria-hidden="true">'+''.join('<i>&#10022;</i>' if i%2==0 else '<i>&#10023;</i>' for i in range(6))+'</span>'
    # Insert cosmetic spans just inside existing components, preserving every
    # original label, for attribute, input, panel and content block.
    pattern=r'(<(?:label|div)\b[^>]*>)'
    def add(m):
        class_match=re.search(r'\bclass="([^"]*)"',m[1])
        classes=set(class_match[1].split()) if class_match else set()
        if classes & {'anv-collection','anv-spotlight','anv-art-frame'} or ('<label' in m[1] and 'id="anv-tab-label-' in m[1]):
            return m[1]+particles
        return m[1]
    enhanced=re.sub(pattern,add,default)
    effects=(OUT/'source/interaction-effects.css').read_text(encoding='utf-8')
    return enhanced+'\n<style type="text/css">\n'+effects+'\n</style>\n'

def select(code,section):
    code=re.sub(r'(<input\b[^>]*)(\schecked(?:="checked")?)([^>]*>)',r'\1\3',code)
    pattern=r'(<input\b[^>]*\bid="anv-page-'+re.escape(section)+r'"[^>]*)(>)'
    code,n=re.subn(pattern,r'\1 checked="checked"\2',code)
    assert n==1 and code.count('checked="checked"')==1
    return code

class Validator(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.labels=[]; self.checked=[]; self.radios=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='label':self.labels.append(a.get('for'))
        if tag=='input' and a.get('type')=='radio':
            self.radios.append(a['id'])
            if 'checked' in a:self.checked.append(a['id'])

def build():
    source=OUT/'source/default-pasted.html'
    default=source.read_text(encoding='utf-8-sig').strip()
    assert default.count('type="radio"')==10 and '<script' not in default.lower()
    enhanced=enhance(default)
    folder=OUT/'imvu-pages'; folder.mkdir(exist_ok=True)
    previews=folder/'previews'; previews.mkdir(exist_ok=True)
    normalized=None; report={}
    for section in SECTIONS:
        code=select(enhanced,section)
        v=Validator(); v.feed(code)
        assert len(v.ids)==len(set(v.ids))
        assert len(v.radios)==10 and v.checked==['anv-page-'+section]
        assert all(label in v.ids for label in v.labels)
        common=select(code,'home')
        if normalized is None:normalized=common
        assert common==normalized,'Pages must differ ONLY in initially checked tab'
        assert 'anv-hover-particle' in code and 'prefers-reduced-motion' in code
        assert '<script' not in code.lower()
        for ext in ('html','txt'):(folder/f'anivelle-{section}.{ext}').write_text(code,encoding='utf-8')
        preview='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AnivelleShop '+escape(section)+'</title><style>body{margin:0;background:#e9dfeb}</style></head><body>'+code+'</body></html>'
        (previews/f'anivelle-{section}.html').write_text(preview,encoding='utf-8')
        report[section]={'checked':v.checked[0],'sha256':hashlib.sha256(code.encode()).hexdigest()}
    (folder/'README.txt').write_text('YOUR PASTED DEFAULT - TEN COMPLETE IMVU DESCRIPTIONS\n\nEach HTML and TXT contains the same complete layout, all ten panels and the same cosmetic effects. The ONLY difference between editions is the initially checked radio: use the filename matching the product category. shop = Furniture; avatar-poses = Poses.\n\nPaste the entire matching TXT file, replacing all previous code. The navbar retains your supplied label/radio behavior.\n\nEffects: hosted star cursor, six sparkling particles per hovered navbar/card/gallery component, lift, glow, and press feedback. Sparkles are attached to hovered components; they do not follow the exact pointer position. No JavaScript is included. Touch devices do not display hover particles. Reduced-motion preferences disable animation.\n\nThe original pasted code is preserved in source/default-pasted.html. This script does not change its text or styling; it inserts decorative spans and appends cosmetic CSS. Rebuild with python tools/build_anivelle_variants.py.\n\nIMVU must retain the supplied radio/label markup and :checked selectors. Browser verification cannot reproduce the live save filter.\n',encoding='ascii')
    (folder/'validation.json').write_text(json.dumps({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'only_difference':'initially checked radio','pages':report},indent=2)+'\n',encoding='utf-8')
    print('Built and validated ten complete HTML/TXT descriptions; only the checked tab differs.')

if __name__=='__main__':build()
