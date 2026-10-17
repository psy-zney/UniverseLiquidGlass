"""Check the encoded final video against its native source, including non-event scenes."""
from pathlib import Path
import json
import subprocess
import numpy as np
import imageio_ffmpeg

HERE=Path(__file__).resolve().parent
VIDEO=HERE.parent
REPO=HERE.parents[2]
original=VIDEO/'renders/native-original.mp4'
edited=REPO/'docs/media/theme-demo.mp4'
timeline=json.loads((VIDEO/'timeline.json').read_text(encoding='utf-8'))
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
def frame(path,seconds):
    raw=subprocess.check_output([ffmpeg,'-v','error','-ss',str(seconds),'-i',str(path),'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','pipe:1'])
    return np.frombuffer(raw,dtype=np.uint8).reshape(900,1600,3).astype(float)

report=[]
for scene in timeline['scenes']:
    t=(scene['start_frame']+scene['end_frame'])/48
    a,b=frame(original,t),frame(edited,t)
    detail=float(np.abs(a[425:830,805:1515]-b[425:830,805:1515]).mean())
    sidebar=float(np.abs(a[:,:292]-b[:,:292]).mean())
    if scene['kind']=='event': assert detail>4,(scene['id'],'Missing close-up',detail)
    else: assert detail<2,(scene['id'],'Unwanted edit in usage scene',detail)
    assert sidebar<2,(scene['id'],'Original sidebar altered',sidebar)
    report.append({'scene':scene['id'],'detail_delta':round(detail,3),'sidebar_delta':round(sidebar,3)})
print(json.dumps(report,indent=2))
print('PASS: close-ups in all nine event scenes; original sidebar and seven usage scenes preserved.')
