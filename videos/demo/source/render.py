"""Capture actual Zen chrome into a silent video using a dedicated Marionette profile.

python render.py --profile /absolute/path/to/isolated-profile
Never use a personal profile. Install imageio-ffmpeg before rendering.
"""
from pathlib import Path
import argparse
import base64
import json
import subprocess
import sys
import time
from marionette_capture import Marionette

HERE=Path(__file__).resolve().parent
VIDEO=HERE.parent
REPO=VIDEO.parent.parent
sys.path.insert(0,str(REPO/'src'))
from cosmic_events import SCHEDULE,TOTAL
parser=argparse.ArgumentParser()
parser.add_argument('--profile',required=True,help='Exact isolated profile to permit capturing')
parser.add_argument('--frames',type=int,help='Optional short preview render')
parser.add_argument('--output',type=Path,default=VIDEO/'renders/native-original.mp4')
args=parser.parse_args()
import imageio_ffmpeg
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
timeline=json.loads((VIDEO/'timeline.json').read_text(encoding='utf-8'))
fps=timeline['fps']
client=Marionette()

def js(code,*params):
    result=client.command('WebDriver:ExecuteScript',{'script':code,'args':list(params),'newSandbox':False,'sandbox':'default'})
    return result.get('value',result)

def content(chapter):
    client.command('Marionette:SetContext',{'value':'content'})
    try: js('for(const [id,text] of Object.entries(arguments[0])){const el=document.getElementById(id);if(el)el.textContent=text;}return true;',chapter)
    finally: client.command('Marionette:SetContext',{'value':'chrome'})

def screenshot():
    result=client.command('WebDriver:TakeScreenshot',{'id':None,'full':True,'hash':False})
    return base64.b64decode(result.get('value',result))

encoder=None
try:
    client.command('WebDriver:NewSession',{'capabilities':{'alwaysMatch':{'acceptInsecureCerts':True}}})
    client.command('Marionette:SetContext',{'value':'chrome'})
    profile=js("return Services.dirsvc.get('ProfD',Ci.nsIFile).path;")
    if Path(profile).resolve()!=Path(args.profile).resolve(): raise RuntimeError('Refusing to capture a different profile')
    client.command('WebDriver:SetWindowRect',{'width':1600,'height':900})
    css=(REPO/'theme/userChrome.css').read_text(encoding='utf-8')
    setup=js('''const w=Services.wm.getMostRecentWindow('navigator:browser'),d=w.document;
      if(w.__demoSheet)w.windowUtils.removeSheetUsingURIString(w.__demoSheet,w.windowUtils.USER_SHEET);
      w.__demoSheet='data:text/css;charset=utf-8,'+encodeURIComponent(arguments[0]);
      w.windowUtils.loadSheetUsingURIString(w.__demoSheet,w.windowUtils.USER_SHEET);
      Services.prefs.setBoolPref('zen.library.enabled',true);
      const lib=d.querySelector('zen-library');if(lib.hasAttribute('open'))lib.constructor.close();
      const extra='#navigator-toolbox{width:292px!important;min-width:292px!important;max-width:292px!important}:root{--zen-sidebar-width:292px!important}';
      w.windowUtils.loadSheetUsingURIString('data:text/css,'+encodeURIComponent(extra),w.windowUtils.USER_SHEET);
      const old=[...w.gBrowser.tabs],first=w.gBrowser.selectedTab;
      first.linkedBrowser.loadURI(Services.io.newURI(arguments[1][0]),{triggeringPrincipal:Services.scriptSecurityManager.getSystemPrincipal()});
      w.__demoTabs=[first,...arguments[1].slice(1).map(uri=>w.gBrowser.addTab(uri,{triggeringPrincipal:Services.scriptSecurityManager.getSystemPrincipal()}))];
      for(const tab of old)if(tab!==first)w.gBrowser.removeTab(tab,{animate:false});
      w.gBrowser.selectedTab=first;
      return {width:w.innerWidth,height:w.innerHeight};''',css,[(HERE/(name+'.html')).as_uri() for name in ['overview','reading','workspace']])
    print('Native Zen capture:',setup,flush=True)
    time.sleep(2)
    js((HERE/'library-fixture.js').read_text(encoding='utf-8'))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    (VIDEO/'renders').mkdir(exist_ok=True)
    log=(VIDEO/'renders/ffmpeg.log').open('w',encoding='utf-8')
    encoder=subprocess.Popen([ffmpeg,'-y','-f','image2pipe','-vcodec','png','-r',str(fps),'-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(args.output)],stdin=subprocess.PIPE,stderr=log)
    frames=min(args.frames or timeline['duration_frames'],timeline['duration_frames'])
    previous=None
    for frame in range(frames):
        scene=next(s for s in timeline['scenes'] if s['start_frame']<=frame<s['end_frame'])
        if scene['id']!=previous:
            previous=scene['id']
            selected=js('''const w=Services.wm.getMostRecentWindow('navigator:browser'),d=w.document;
              const lib=d.querySelector('zen-library');if(lib.hasAttribute('open'))lib.constructor.close();
              w.__demoTabs.forEach(t=>t.removeAttribute('busy'));
              w.__demoTabs[arguments[0]].click();return w.gBrowser.selectedTab===w.__demoTabs[arguments[0]];''',scene['tab'])
            if not selected: raise RuntimeError('Native tab click did not select expected tab')
            time.sleep(.08)
            if scene['kind']=='event':
                content({'eyebrow':'CELESTIAL EVENT','title':scene['title'],'description':scene['description'],'event':'Native CSS + SVG · Sidebar and top frame','note':'The glow follows the source. Controls and web content stay above the scene.'})
            elif scene['kind']=='loading':
                content({'eyebrow':'LOADING STATE','title':'Light follows loading.','description':'The selected tab gets a moving highlight while its page is busy. It stops when loading finishes.','event':'Only the active loading tab','note':'The capture toggles the native busy state; no network request is needed.'})
            elif scene['kind']=='downloads':
                js("Services.wm.getMostRecentWindow('navigator:browser').document.querySelector('zen-library').constructor.toggle('downloads');return true;")
                time.sleep(.4)
            elif scene['kind']=='install':
                content({'eyebrow':'MAKE IT YOURS','title':'Your universe awaits.','description':'Download the release, close Zen, then run install.cmd. Reopen Zen and enjoy the view.','event':'github.com/psy-zney/UniverseLiquidGlass','c1':'01  Download','s1':'Get UniverseLiquidGlass-v1.0.0.zip from Releases and extract it.','c2':'02  Install','s2':'Close Zen completely. Run install.cmd; existing CSS is backed up.','c3':'03  Restart Zen','s3':'Use the dark appearance and an expanded vertical sidebar.','note':'Manual installation and profile selection are documented in the README.'})
            print('Scene',scene['id'],f'{frame}/{frames}',flush=True)
        progress=(frame-scene['start_frame'])/max(1,scene['end_frame']-scene['start_frame']-1)
        if scene['kind']=='event':
            entry=next(e for e in SCHEDULE if e[0]==scene['event'])
            cosmic=entry[1]+(entry[2]-entry[1])*progress
        else: cosmic=(frame/fps)%TOTAL
        busy=scene['kind']=='loading' and progress<.8
        js('''const w=Services.wm.getMostRecentWindow('navigator:browser'),d=w.document;
          const tab=w.gBrowser.selectedTab;
          if(arguments[2])tab.setAttribute('busy','true');else tab.removeAttribute('busy');
          for(const a of d.getAnimations()) {
            const name=a.animationName||'';
            if(!name.startsWith('cosmos-'))continue;
            a.pause();a.currentTime=['cosmos-visitors','cosmos-source-pulse'].includes(name)?arguments[0]:
              ['cosmos-top-events','cosmos-top-edge'].includes(name)?arguments[0]/70*84-16000:arguments[1];
          }
          return true;''',cosmic*1000,frame/fps*1000,busy)
        png=screenshot();encoder.stdin.write(png)
        if frame==scene['start_frame']+(scene['end_frame']-scene['start_frame'])//2:
            (VIDEO/'renders'/f"{scene['id']}.png").write_bytes(png)
            if scene['id']=='hole': (REPO/'docs/media/preview.png').write_bytes(png)
        if frame%fps==0: print(f'Captured {frame}/{frames}',flush=True)
    encoder.stdin.close()
    if encoder.wait()!=0: raise RuntimeError('FFmpeg failed; inspect renders/ffmpeg.log')
    encoder=None
    print('Rendered',args.output,frames/fps,'seconds',flush=True)
finally:
    if encoder:
        try: encoder.stdin.close()
        except Exception: pass
        encoder.wait()
    try: client.command('WebDriver:DeleteSession')
    finally: client.sock.close()
