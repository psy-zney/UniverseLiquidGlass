"""Build standalone CSS from local, deterministic SVG/CSS sources. Python 3.10+."""
from pathlib import Path
from random import Random
from urllib.parse import quote
import re
import sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'src'))
COLORS = {
    '#685ed1':'#36586c', '#303e90':'#1d3246', '#101735':'#0a1320',
    '#35a5be':'#3f7689', '#215a8b':'#213b4d', '#081122':'#080f17',
    '#171a36':'#0c151e', '#070d1b':'#05090e', '#e4d2ff':'#dce7ef',
    '#5c72b0':'#46647a', '#839ed5':'#6d8a9d', '#b5b4df':'#a6bbc9',
    '#b8b9de':'#a6bcc9', '#aab7ff':'#b0c9d9', '#6089ce':'#668b9d',
    '#0c1424':'#090f16', '#16243b':'#111c28', '#233957':'#1c2d3d',
    '#0a1222':'#060b11', '#080f1d':'#060b10', '#192b43':'#142331',
    '#29435f':'#243b4c', '#101b2e':'#0d1722', '#1e314c':'#182a38',
    '#172941':'#12222f', '#294968':'#233d4d', '#20364f':'#1b3040',
    '#132239':'#0f1c29', '#1f3651':'#1b3040', '#101c30':'#0c1721',
    '#14243a':'#101f2b', '#0d1729':'#0a131c', '#514881':'#2d4b5a',
    '#3a2c61':'#233c4b', '#1c4761':'#1c3645', '#172039':'#101d2a',
    '#101726':'#0b141e', '#91b9f044':'#93b5c833', '#32496d22':'#344d6022',
    '#a19be735':'#87a4b322', '#709bc34d':'#6b8c9f4d',
    '#a194d977':'#8098aa66', '#71bfcf66':'#82bac366',
}
DEEP_COLORS = {
    '#05090e':'#010203', '#090a0f':'#020304', '#10151d':'#060809',
    '#1b2735':'#101315', '#090f16':'#050607', '#111c28':'#0b0d10',
    '#1c2d3d':'#1b1e22', '#060b11':'#030405', '#060b10':'#030405',
    '#142331':'#101215', '#243b4c':'#24282e', '#0d1722':'#090b0e',
    '#182a38':'#171a1e', '#12222f':'#111417', '#233d4d':'#24292e',
    '#1b3040':'#1c2025', '#0f1c29':'#0c0f12', '#0c1721':'#080a0d',
    '#101f2b':'#101317', '#0a131c':'#07090c', '#233c4b':'#191d22',
    '#1c3645':'#151a1e', '#101d2a':'#0b0e11', '#0b141e':'#080a0d',
    '#93b5c833':'#d5dbe31f', '#344d6022':'#87929e14', '#87a4b322':'#c7cfd91a',
    '#6b8c9f4d':'#b8bec526', '#8098aa66':'#c9cfd633', '#82bac366':'#b9c0c92e',
    '#719dc866':'#b8bec526', '#c5e4ffbb':'#d9dee7aa', '#b9ddff88':'#d4dce677',
    '#b0d8ffbb':'#d6dce2bb', '#6eabed30':'#aebcc822', '#8fbfff22':'#c0cbd522',
    '#d4e9ff35':'#d4dbe535', '#c5e7ff':'#e2e6eb', '#b9c9df':'#bbc1c9',
    '#bdcde1':'#c0c5cd', '#dceaff':'#e1e5eb', '#f5f7ff':'#f5f6f8',
    '#7395cf30':'#a4b0be20', '#294969':'#303940', '#182b44':'#14191f',
    '#101923':'#0b0e12', '#0d141d':'#06080b', '#162230':'#11161b',
    '#1b2938':'#141a20', '#25374a':'#20272e', '#293d52':'#242b33',
    '#1c304b':'#191d23', '#9bb8d2':'#b9c0c7', '#b6dcff':'#e6e9ee',
    '#88b8ee77':'#cad1d877', '#94caff88':'#dae0e688',
    '#0c1729':'#0b0e12',
}


def black_palette(text):
    for old, new in COLORS.items():
        text = text.replace(old, new)
    for old,new in DEEP_COLORS.items():
        text=text.replace(old,new)
    for old,new in {
        'rgba(17,31,51,.84)':'rgba(10,12,15,.9)',
        'rgba(14, 24, 42, 0.78)':'rgba(7,9,12,.84)',
        'rgba(30, 44, 68, 0.86)':'rgba(17,20,24,.9)',
        'rgba(34, 48, 75, 0.88)':'rgba(22,25,30,.92)',
        'rgba(25,42,65,.84)':'rgba(21,24,28,.88)',
    }.items(): text=text.replace(old,new)
    return text


def svg_url(body, view='0 0 420 1300'):
    svg = black_palette(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}">{body}</svg>')
    return 'url("data:image/svg+xml,' + quote(svg, safe='') + '")'



from deep_space_assets import make_assets
from cosmic_events import make_event_assets,make_timeline
assets=make_assets(svg_url,Random(101726))
events=make_event_assets(assets,svg_url)
assets.update(make_timeline(events))
sidebar=(ROOT/'src/sidebar.css').read_text(encoding='utf-8')
for key,value in assets.items(): sidebar=sidebar.replace('__'+key+'__',value)
base=(ROOT/'src/browser-base.css').read_text(encoding='utf-8')
ui=(ROOT/'src/ui.css').read_text(encoding='utf-8').replace('__TOP_EVENT_CSS__',make_timeline(events,top=True))
css=base.replace('__SIDEBAR__',sidebar)+ui
css=black_palette(re.sub(r'\n{4,}','\n\n',css))
if re.search(r'__[A-Z_]+__',css): raise RuntimeError('Unresolved CSS template')
(ROOT/'theme').mkdir(exist_ok=True)
(ROOT/'theme/userChrome.css').write_text(css,encoding='utf-8')
(ROOT/'theme/userContent.css').write_text((ROOT/'src/content.css').read_text(encoding='utf-8'),encoding='utf-8')
print('Built theme/userChrome.css and theme/userContent.css')
