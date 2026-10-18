"""Prepare a review bundle without publishing or claiming a Zen Mods listing."""
from pathlib import Path
import json
import shutil

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'zen-mod'
OUT.mkdir(exist_ok=True)
name='Universe Liquid Glass'
description='Deep black cosmic sidebar, liquid glass tabs and nine illuminated celestial events.'
assert len(name)<25 and len(description)<100
style=ROOT/'theme/userChrome.css'
shutil.copyfile(style,OUT/'chrome.css')
metadata={
    'name':name,'description':description,'version':json.loads((ROOT/'theme.json').read_text(encoding='utf-8'))['version'],'author':'psy-zney',
    'homepage':'https://github.com/psy-zney/UniverseLiquidGlass',
    'type':'css','style':'chrome.css','readme':'readme.md','image':'preview.png',
    'preferences':{},'submissionStatus':'not_submitted',
    'officialRepository':'https://github.com/zen-browser/theme-store',
    'lastVerified':'2026-10-18','officialRepositoryArchived':True,
    'notes':[
        'This file is review-bundle metadata, not an official store-assigned theme record.',
        'The official repository is archived; issue/PR submissions cannot be created there.',
        'The style exceeds the GitHub issue-body limit; the legacy inline form cannot carry the complete CSS.',
        'Website content rules in theme/userContent.css are optional manual-install extras and are not included in chrome.css.',
        'The official store requires CC BY-NC-SA 4.0 for submitted themes. This project remains MIT; no store license change is made by preparing this bundle.'
    ]
}
(OUT/'submission.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
print(f'Review bundle prepared: {name} ({len(name)} characters), description {len(description)} characters, CSS {style.stat().st_size:,} bytes')
