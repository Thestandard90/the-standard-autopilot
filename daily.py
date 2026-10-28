#!/usr/bin/env python3
"""Deterministic daily video producer. No paid API or account access required."""
import datetime,json,subprocess,sys,os,html
from pathlib import Path
ROOT=Path(__file__).parent
scripts=json.loads((ROOT/'scripts.json').read_text())
index=int(os.getenv('VIDEO_INDEX', str((datetime.date.today()-datetime.date(2026,10,28)).days)))%len(scripts)
video=scripts[index]
subprocess.run([sys.executable,str(ROOT/'build.py'),'--slug',video['slug']],check=True)
site=ROOT/'site';site.mkdir(exist_ok=True)
path=ROOT/'videos'/(video['slug']+'.mp4')
(site/'daily.mp4').write_bytes(path.read_bytes())
(site/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>The Standard media</title><h1>The Standard: daily media</h1><video controls width="360" src="daily.mp4"></video>',encoding='utf-8')
(site/'caption.txt').write_text(video['caption']+'\n',encoding='utf-8')
print('Selected:',video['slug'],'output:',path)
