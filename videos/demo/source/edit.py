"""Add tracked event close-ups to the native recording, preserving full-window context."""
from pathlib import Path
import argparse
import json
import sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
sys.path.insert(0,str(REPO/'src'))
from cosmic_events import SCHEDULE

parser=argparse.ArgumentParser()
parser.add_argument('--input',type=Path,default=HERE.parent/'renders/native-original.mp4')
parser.add_argument('--output',type=Path,default=REPO/'docs/media/theme-demo.mp4')
parser.add_argument('--font',type=Path,help='Optional TrueType font for the detail label')
args=parser.parse_args()
timeline=json.loads((HERE.parent/'timeline.json').read_text(encoding='utf-8'))
reader=imageio_ffmpeg.read_frames(str(args.input))
meta=next(reader)
width,height=meta['size']
if (width,height)!=(1600,900) or meta['fps']!=timeline['fps']:
    raise ValueError('Edit expects the native 1600x900 / 24 fps capture')
font=ImageFont.truetype(str(args.font),18) if args.font else ImageFont.load_default(size=18)
args.output.parent.mkdir(parents=True,exist_ok=True)
writer=imageio_ffmpeg.write_frames(str(args.output),(width,height),fps=meta['fps'],codec='libx264',quality=None,
    output_params=['-crf','19','-preset','fast','-movflags','+faststart'],macro_block_size=1)
writer.send(None)
events={e[0]:e for e in SCHEDULE}
count=0
try:
    for frame,raw in enumerate(reader):
        scene=next(s for s in timeline['scenes'] if s['start_frame']<=frame<s['end_frame'])
        canvas=Image.frombytes('RGB',(width,height),raw)
        if scene['kind']=='event':
            p=(frame-scene['start_frame'])/(scene['end_frame']-scene['start_frame']-1)
            # Fade in only when the source has entered the sidebar; follow its vertical path.
            visibility=max(0,min(1,(p-.23)/.09,(.77-p)/.09))
            if visibility>0:
                entry=events[scene['event']]
                sprite_height=entry[5][1]
                center_y=(height-sprite_height)*(entry[3]+(entry[4]-entry[3])*p)/100+sprite_height/2
                crop_height=150
                top=max(74,min(height-55-crop_height,center_y-crop_height/2))
                closeup=canvas.crop((0,round(top),292,round(top)+crop_height)).resize((684,351),Image.Resampling.LANCZOS)
                panel=Image.new('RGB',(710,405),'#07090c')
                draw=ImageDraw.Draw(panel)
                draw.rounded_rectangle((0,0,709,404),radius=14,outline='#717b89',width=1)
                draw.text((16,12),scene['title'].upper()+'  /  2.3x',font=font,fill='#e3e7ed')
                panel.paste(closeup,(13,40))
                overlay=canvas.copy();overlay.paste(panel,(805,425))
                canvas=Image.blend(canvas,overlay,visibility*visibility*(3-2*visibility))
        writer.send(np.asarray(canvas,dtype=np.uint8).tobytes())
        count+=1
        if frame%240==0: print(f'Edited {frame}/{timeline["duration_frames"]}',flush=True)
        if frame==450:
            canvas.save(HERE.parent/'renders/zoom-hole.png')
            canvas.save(REPO/'docs/media/preview.png')
        if frame in [114,534,618,858]: canvas.save(HERE.parent/'renders'/f'edited-{frame}.png')
finally:
    reader.close();writer.close()
if count!=timeline['duration_frames']: raise RuntimeError(f'Incomplete video: {count} frames')
print('Edited event close-ups:',args.output,count,'frames',flush=True)
