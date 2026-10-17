from math import atan2, cos, sin, hypot, sqrt, pi
from random import Random
from urllib.parse import unquote
import re


def inner_svg(data_url, x, y, width, height):
    text=unquote(data_url[len('url("data:image/svg+xml,'):-2])
    view=re.search(r'viewBox="([^"]+)"',text).group(1)
    body=text[text.index('>')+1:text.rindex('</svg>')]
    return f'<svg x="{x}" y="{y}" width="{width}" height="{height}" viewBox="{view}">{body}</svg>'


def make_event_assets(base, svg_url):
    rng=Random(73121)
    events={}

    def illuminated(name, color, intensity, body, dark=False):
        veil='<radialGradient id="veil"><stop stop-color="#000102" stop-opacity=".93"/><stop offset=".3" stop-color="#000102" stop-opacity=".45"/><stop offset="1" stop-color="#000102" stop-opacity="0"/></radialGradient>' if dark else ''
        halo=f'''<defs><radialGradient id="event-light"><stop stop-color="{color}" stop-opacity="{intensity}"/><stop offset=".16" stop-color="{color}" stop-opacity="{intensity*.65:.3f}"/><stop offset=".4" stop-color="{color}" stop-opacity="{intensity*.23:.3f}"/><stop offset=".75" stop-color="{color}" stop-opacity="{intensity*.035:.3f}"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>{veil}</defs>
          <ellipse cx="180" cy="130" rx="176" ry="124" fill="url(#event-light)"/>'''
        if dark: halo+='<ellipse cx="180" cy="130" rx="79" ry="69" fill="url(#veil)"/>'
        events[name]=svg_url(halo+body,'0 0 360 260')

    # Lensed star images move with the dark core, replacing the local unwarped field.
    lens=[]
    for i in range(43):
        sx,sy=rng.uniform(-58,58),rng.uniform(-43,43)
        r=hypot(sx,sy)
        if r<3 or r>61: continue
        angle=atan2(sy,sx)
        image_r=.5*(r+sqrt(r*r+4*22**2))
        x=180+image_r*cos(angle);y=130+image_r*sin(angle)
        lens.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{rng.uniform(.3,.7):.2f}" fill="#edf1f5" opacity=".55"/>')
        if r<27:
            a=angle-.12; b=angle+.12
            inner=.5*(sqrt(r*r+4*22**2)-r)
            x1=180-inner*cos(a);y1=130-inner*sin(a)
            x2=180-inner*cos(b);y2=130-inner*sin(b)
            lens.append(f'<path d="M{x1:.2f} {y1:.2f} A{inner:.2f} {inner:.2f} 0 0 1 {x2:.2f} {y2:.2f}" fill="none" stroke="#f7e8d5" stroke-width=".55" opacity=".48"/>')
    illuminated('HOLE','#e5cfaf',.25,''.join(lens)+inner_svg(base['HOLE'],103,77,154,106),True)
    illuminated('PLANET','#dce6ed',.065,inner_svg(base['PLANET'],132,82,96,96))
    illuminated('GALAXY','#ece5d6',.12,inner_svg(base['GALAXY'],98,79,164,102))
    illuminated('COMET','#f1f4f7',.2,inner_svg(base['COMET'],68,65,128,80))

    def star(color, radius, corona, rays=0):
        pieces=[f'''<defs><radialGradient id="corona"><stop stop-color="#fff" stop-opacity=".95"/><stop offset=".12" stop-color="{color}" stop-opacity=".85"/><stop offset=".35" stop-color="{color}" stop-opacity=".25"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient></defs>
          <circle cx="180" cy="130" r="{corona}" fill="url(#corona)"/>
          <circle cx="180" cy="130" r="{radius}" fill="#fffaf3"/>''']
        for i in range(rays):
            a=i*pi/rays
            dx=cos(a)*corona*.9;dy=sin(a)*corona*.9
            pieces.append(f'<path d="M{180-dx:.2f} {130-dy:.2f}L{180+dx:.2f} {130+dy:.2f}" stroke="{color}" stroke-width=".45" opacity=".2"/>')
        return ''.join(pieces)

    illuminated('STAR','#fff0d2',.19,star('#fff0d2',4.2,30,4))
    illuminated('WHITE_DWARF','#f2f6ff',.22,star('#e6f1ff',2.8,23,2))
    illuminated('BLUE_STAR','#85c6ff',.2,star('#8fcfff',5.0,38,5))
    neutron='''<defs><linearGradient id="jet" x1="-86" y1="0" x2="86" y2="0" gradientUnits="userSpaceOnUse"><stop stop-color="#b5dfff" stop-opacity="0"/><stop offset=".45" stop-color="#b5dfff" stop-opacity=".75"/><stop offset=".5" stop-color="#fff"/><stop offset=".55" stop-color="#b5dfff" stop-opacity=".75"/><stop offset="1" stop-color="#b5dfff" stop-opacity="0"/></linearGradient></defs>
      <g transform="translate(180 130) rotate(-43)"><path d="M-86 0H86" stroke="url(#jet)" stroke-width="4" opacity=".13"/><path d="M-86 0H86" stroke="url(#jet)" stroke-width=".85"/></g>'''
    illuminated('NEUTRON','#c8e4ff',.19,neutron+star('#d9eeff',3.1,24))

    clouds=[]
    for i in range(30):
        x=92+i*5.8+rng.uniform(-9,9)
        y=130+sin(i*.21)*28+rng.uniform(-17,17)
        clouds.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rng.uniform(19,43):.1f}" ry="{rng.uniform(13,28):.1f}" fill="url(#cloud-light)" opacity="{rng.uniform(.24,.65):.2f}"/>')
    nebula='''<defs><radialGradient id="cloud-light"><stop stop-color="#c7d8dd" stop-opacity=".24"/><stop offset=".4" stop-color="#83a5b4" stop-opacity=".12"/><stop offset="1" stop-color="#a8bac4" stop-opacity="0"/></radialGradient>
      <filter id="wisps"><feTurbulence type="fractalNoise" baseFrequency=".021 .029" numOctaves="3" seed="8" result="noise"/><feColorMatrix in="noise" type="luminanceToAlpha" result="alpha"/><feComposite in="SourceGraphic" in2="alpha" operator="in"/></filter></defs>
      <g filter="url(#wisps)">'''+''.join(clouds)+'''</g>
      <path d="M98 147Q143 100 179 132T270 126Q226 159 188 145T98 147" fill="#010204" opacity=".18"/>
      <circle cx="172" cy="128" r="1.2" fill="#fff" opacity=".8"/><circle cx="213" cy="145" r=".8" fill="#eef3f8"/>'''
    illuminated('NEBULA','#b2cbd5',.11,nebula)
    return events


SCHEDULE=[
    # name, start/end seconds, sidebar y start/end, sidebar size, top size
    ('COMET',1,3.5,30,72,(300,217),(166,120)),
    ('STAR',5,10,42,35,(300,217),(170,123)),
    ('PLANET',12,18,64,55,(280,202),(174,126)),
    ('WHITE_DWARF',20,25,28,40,(300,217),(166,120)),
    ('HOLE',27,34,65,52,(320,231),(188,136)),
    ('NEUTRON',36,42,46,58,(320,231),(194,140)),
    ('NEBULA',44,51,70,64,(340,246),(240,173)),
    ('BLUE_STAR',53,59,39,50,(320,231),(178,129)),
    ('GALAXY',61,68,76,69,(320,231),(208,150)),
]
TOTAL=70


def make_timeline(events, top=False, edge=False):
    sizes=[e[6 if top else 5] for e in SCHEDULE]
    initial=[]; final=[]
    for e,(width,height) in zip(SCHEDULE,sizes):
        y0=y1=50 if top else None
        if not top: y0,y1=e[3],e[4]
        start_y=end_y=f'calc(4px - {height/2:g}px)' if edge else None
        if not edge: start_y,end_y=f'{y0}%',f'{y1}%'
        initial.append(f'-{width+10}px {start_y}')
        final.append(f'calc(100% + {width+10}px) {end_y}')
    states=[]
    for t in sorted({0,TOTAL,*[e[1] for e in SCHEDULE],*[e[2] for e in SCHEDULE]}):
        positions=[final[i] if t>=e[2] else initial[i] for i,e in enumerate(SCHEDULE)]
        states.append(f'  {t/TOTAL*100:.6f}% {{ background-position: '+', '.join(positions)+'; }')
    name='cosmos-top-edge' if edge else ('cosmos-top-events' if top else 'cosmos-visitors')
    keyframes='@keyframes '+name+' {\n'+'\n'.join(states)+'\n}\n'
    images=',\n    '.join(events[e[0]] for e in SCHEDULE)
    css_sizes=', '.join(f'{w}px {h}px' for w,h in sizes)
    positions=', '.join(initial)
    if edge:
        return f'''/* Native compact mode can hide its toolbar. Its exposed frame still receives light.
 * Paint on the parent background so page surfaces naturally occlude every sprite. */
#zen-appcontent-wrapper {{
  background-image: var(--cosmos-top-event-images) !important;
  background-size: {css_sizes} !important;
  background-repeat: no-repeat !important;
  background-position: {positions};
  animation: cosmos-top-edge 84s linear -16s infinite !important;
}}
'''+keyframes
    if top:
        return f'''/* Ambient events on the top bar remain independent of the loading indicator. */
:root {{ --cosmos-top-event-images: {images}; }}
#zen-appcontent-navbar-wrapper {{
  isolation: isolate !important;
  background-color: #010203 !important;
  background-image: var(--cosmos-top-event-images) !important;
  background-size: {css_sizes} !important;
  background-repeat: no-repeat !important;
  background-position: {positions};
  animation: cosmos-top-events 84s linear -16s infinite !important;
}}
'''+keyframes+make_timeline(events,top=True,edge=True)
    return {'EVENT_IMAGES':images,'EVENT_SIZES':css_sizes,'EVENT_POSITIONS':positions,'EVENT_KEYFRAMES':keyframes}
