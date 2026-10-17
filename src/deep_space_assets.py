from math import sin, cos, pi, hypot
from random import Random


def make_assets(svg_url, rng):
    # Tiny neutral stars on an almost black sky. Bright accents are a separate layer.
    stars=[]
    for _ in range(260):
        x,y=rng.uniform(3,417),rng.uniform(3,1297)
        r=rng.choices([.34,.5,.72,1.05],weights=[48,32,17,3])[0]
        color=rng.choice(['#c6c9cf','#e1e3e7','#ffffff','#d7d2ca'])
        stars.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{color}" opacity="{rng.uniform(.13,.5):.2f}"/>')
    sky=svg_url('''<defs><radialGradient id="dust"><stop stop-color="#777d87" stop-opacity=".045"/><stop offset="1" stop-color="#060708" stop-opacity="0"/></radialGradient></defs>
      <rect width="420" height="1300" fill="#010203"/>
      <ellipse cx="360" cy="380" rx="270" ry="370" fill="url(#dust)"/>
      <ellipse cx="40" cy="1030" rx="230" ry="360" fill="url(#dust)" opacity=".6"/>'''+''.join(stars))

    # As in the portfolio loader: compact white cores, a tight halo, staggered twinkle.
    images=[];positions=[];sizes=[]
    spark_rng=Random(20261017)
    points=[]
    for i in range(21):
        group='abc'[i%3]
        while True:
            x,y=spark_rng.uniform(4,96),spark_rng.uniform(8,94)
            if all(hypot((x-px)*2.4,(y-py)*10)>25 for px,py in points):
                break
        points.append((x,y))
        size=spark_rng.choices([3.5,4,4.5,5,6,7],weights=[22,28,20,15,10,5])[0]
        images.append(f'radial-gradient(circle, rgb(255 255 255 / var(--cosmos-spark-{group})) 0 17%, rgb(245 247 250 / calc(var(--cosmos-spark-{group}) * .22)) 36%, transparent 69%)')
        positions.append(f'{x:.1f}% {y:.1f}%')
        sizes.append(f'{size}px {size}px')

    # A closed accretion disc and photon ring; the opaque core occludes their center.
    disc=[]
    for i in range(10):
        rx=50-i*1.8;ry=12.5-i*.38
        disc.append(f'<ellipse rx="{rx:.1f}" ry="{ry:.2f}" fill="none" stroke="url(#disc)" stroke-width="{.45 if i%3 else .8}" opacity="{.14+i*.025:.2f}"/>')
    hole=svg_url('''<defs>
      <radialGradient id="halo"><stop stop-color="#d4cbbc" stop-opacity=".16"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
      <radialGradient id="rim"><stop offset=".6" stop-color="#090a0b" stop-opacity="0"/><stop offset=".86" stop-color="#e7ddce" stop-opacity=".3"/><stop offset="1" stop-color="#c5ccd2" stop-opacity="0"/></radialGradient>
      <linearGradient id="disc"><stop stop-color="#a1a7ae" stop-opacity=".15"/><stop offset=".42" stop-color="#f0e3cf"/><stop offset=".65" stop-color="#e8e9ea"/><stop offset="1" stop-color="#a1a7ae" stop-opacity=".15"/></linearGradient>
      </defs><ellipse cx="70" cy="48" rx="64" ry="40" fill="url(#halo)"/>
      <g transform="translate(70 48) rotate(-19)">'''+''.join(disc)+'''
      <circle r="22" fill="url(#rim)"/><circle r="15.5" fill="#000102"/>
      <circle r="16.1" fill="none" stroke="#fff1db" stroke-opacity=".82" stroke-width=".65"/>
      <circle r="17.2" fill="none" stroke="#dce0e5" stroke-opacity=".22" stroke-width=".45"/>
      </g>''','0 0 140 96')

    # A textured, ringless moon avoids the overlapping orbit outlines in the old version.
    craters=[]
    for _ in range(35):
        x,y=rng.uniform(-29,29),rng.uniform(-29,29)
        r=rng.uniform(.8,4)
        if hypot(x,y)+r>30: continue
        craters.append(f'<circle cx="{54+x:.2f}" cy="{54+y:.2f}" r="{r:.2f}" fill="#30363c" opacity=".23"/><path d="M{54+x-r*.7:.2f} {54+y:.2f}a{r*.75:.2f} {r*.75:.2f} 0 0 1 {r:.2f} {-r*.65:.2f}" fill="none" stroke="#f4f2e9" stroke-width=".55" opacity=".26"/>')
    planet=svg_url('''<defs><radialGradient id="moon" cx="28%" cy="24%"><stop stop-color="#e7e5de"/><stop offset=".4" stop-color="#a4a6a7"/><stop offset=".76" stop-color="#52585e"/><stop offset="1" stop-color="#090c10"/></radialGradient>
      <linearGradient id="night"><stop offset=".35" stop-color="#000" stop-opacity="0"/><stop offset=".74" stop-color="#010204" stop-opacity=".22"/><stop offset="1" stop-color="#000102" stop-opacity=".95"/></linearGradient><clipPath id="limb"><circle cx="54" cy="54" r="31"/></clipPath></defs>
      <circle cx="54" cy="54" r="31" fill="url(#moon)"/>
      <g clip-path="url(#limb)"><path d="M20 44Q40 24 72 38T91 55M20 62Q55 42 86 63" fill="none" stroke="#e0ded7" stroke-width="4" opacity=".08"/>'''+''.join(craters)+'''
      <circle cx="54" cy="54" r="31" fill="url(#night)"/></g>
      <circle cx="54" cy="54" r="31" fill="none" stroke="#e6e9ee" stroke-width=".5" stroke-opacity=".25"/>''','0 0 108 108')

    # A sampled spiral made from dust points, with no open orbit paths.
    dust=[]
    for i in range(680):
        t=rng.uniform(.18,5.3);r=(t/5.3)**1.25*65
        angle=t*1.55+(i%3)*2*pi/3
        x=r*cos(angle)+rng.gauss(0,2)
        y=(r*sin(angle)+rng.gauss(0,2))*.35
        size=rng.uniform(.15,.6)
        dust.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{size:.2f}" fill="{rng.choice(["#fff2da","#e5e8ed","#b5bcc6"])}" opacity="{rng.uniform(.18,.64):.2f}"/>')
    galaxy=svg_url('''<defs><radialGradient id="gal"><stop stop-color="#fff7e8" stop-opacity=".95"/><stop offset=".07" stop-color="#e2ddd5" stop-opacity=".7"/><stop offset=".24" stop-color="#c7cbd1" stop-opacity=".22"/><stop offset=".7" stop-color="#a2aab5" stop-opacity=".035"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient></defs>
      <g transform="translate(80 50) rotate(-25)"><ellipse rx="73" ry="29" fill="url(#gal)"/>'''+''.join(dust)+'''<ellipse rx="2.1" ry="1.1" fill="#fff9ed" opacity=".85"/></g>''','0 0 160 100')

    comet=svg_url('''<defs><linearGradient id="tail" x1="8" y1="5" x2="112" y2="65" gradientUnits="userSpaceOnUse"><stop stop-color="#fff" stop-opacity="0"/><stop offset=".6" stop-color="#e7ebf0" stop-opacity=".25"/><stop offset="1" stop-color="#fff"/></linearGradient><radialGradient id="head"><stop stop-color="#fff" stop-opacity=".6"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient></defs>
      <path d="M8 5L112 65" stroke="url(#tail)" stroke-width="3.3" opacity=".2"/>
      <path d="M8 5L112 65" stroke="url(#tail)" stroke-width=".85"/>
      <circle cx="112" cy="65" r="6" fill="url(#head)"/>
      <circle cx="112" cy="65" r="1.45" fill="#fff"/>
      <circle cx="95" cy="55" r=".5" fill="#fff" opacity=".7"/>
      <circle cx="84" cy="48" r=".4" fill="#fff" opacity=".4"/>''','0 0 128 80')
    return {'SKY':sky,'HOLE':hole,'PLANET':planet,'GALAXY':galaxy,'COMET':comet,
            'SPARK_IMAGES':',\n    '.join(images),'SPARK_POSITIONS':', '.join(positions),'SPARK_SIZES':', '.join(sizes)}
