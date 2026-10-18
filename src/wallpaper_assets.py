"""Deterministic, local-only wide star field; personal desktop images stay in profiles."""
from random import Random

def make_wallpaper_assets(svg_url):
    rng=Random(20261018)
    stars=[]
    for i in range(200):
        x,y=rng.uniform(4,1916),rng.uniform(4,1076)
        size=rng.choices([.4,.65,.9,1.3],weights=[40,34,22,4])[0]
        stars.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size}" fill="#f3f5fa" opacity="{rng.uniform(.14,.6):.2f}"/>')
    points=''.join(stars)
    return {
        'AMBIENT_STARS':svg_url(points,'0 0 1920 1080'),
        'DEFAULT_WALLPAPER':svg_url('''<defs><radialGradient id="mist"><stop stop-color="#89959f" stop-opacity=".17"/><stop offset=".4" stop-color="#596877" stop-opacity=".08"/><stop offset="1" stop-color="#030405" stop-opacity="0"/></radialGradient></defs>
        <rect width="1920" height="1080" fill="#020304"/><ellipse cx="1300" cy="650" rx="900" ry="370" fill="url(#mist)" transform="rotate(-24 1300 650)"/>'''+points,'0 0 1920 1080')
    }
