#!/usr/bin/env python3
"""Generate original cinematic 9:16 marketing videos with Pillow + FFmpeg; no API keys."""
import argparse, json, math, subprocess, random, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT=Path(__file__).resolve().parent
W,H=720,1280
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
if not Path(BOLD).exists():
    BOLD=FONT

def font(size,bold=False):return ImageFont.truetype(BOLD if bold else FONT,size)

def backgrounds(seed,scene):
    random.seed(seed*91+scene)
    img=Image.new('RGB',(W,H)); p=img.load()
    # Atmospheric twilight: navy, almost black, faint amber on skyline
    for y in range(H):
        horizon=H*.61
        glow=math.exp(-((y-horizon)/(H*.21))**2)
        for x in range(W):
            h=math.exp(-((x-W*.62)/(W*.78))**2)
            noise=random.randint(-3,3)
            p[x,y]=(int(7+15*glow*h+noise),int(12+13*glow*h+noise),int(19+11*glow+noise))
    d=ImageDraw.Draw(img,'RGBA')
    # faint architecture/horizon and rain streaks
    for j in range(35):
        x=random.randrange(W); y=random.randrange(70,H-170)
        d.line([(x,y),(x-5,y+random.randint(24,120))],fill=(169,181,193,random.randrange(6,20)),width=1)
    # layered mountainous geometry
    d.polygon([(0,910),(100,840),(215,940),(350,780),(490,935),(640,840),(720,895),(720,H),(0,H)],fill=(13,20,27,205))
    d.polygon([(0,1070),(130,930),(240,1010),(440,875),(610,985),(720,910),(720,H),(0,H)],fill=(5,10,14,245))
    # lone human as abstract silhouette at bottom, original illustration
    cx=360 + [-65,55,-15,50][scene%4]; cy=1035
    d.ellipse((cx-26,cy-120,cx+26,cy-68),fill=(2,6,9,255))
    d.polygon([(cx-39,cy-69),(cx+39,cy-69),(cx+54,cy+82),(cx-54,cy+82)],fill=(2,6,9,255))
    d.polygon([(cx-45,cy+60),(cx-5,cy+55),(cx-17,cy+235),(cx-48,cy+235)],fill=(2,6,9,255))
    d.polygon([(cx+4,cy+55),(cx+43,cy+60),(cx+50,cy+235),(cx+17,cy+235)],fill=(2,6,9,255))
    # film-style vignette
    vign=Image.new('L',(W,H)); vp=vign.load()
    for y in range(H):
        for x in range(W):
            rr=((x-W/2)/(W*.85))**2+((y-H*.45)/(H*.75))**2
            vp[x,y]=min(180,int(rr*145))
    img=Image.composite(Image.new('RGB',(W,H),(1,3,6)),img,vign)
    return img

def wrap_text(text,draw,f,max_width):
    words=text.split(); lines=[]; cur=''
    for word in words:
        test=(cur+' '+word).strip()
        if draw.textbbox((0,0),test,font=f)[2]>max_width and cur:
            lines.append(cur);cur=word
        else:cur=test
    if cur:lines.append(cur)
    return lines

def scene_png(text,scene,seed,out):
    img=backgrounds(seed,scene).convert('RGBA');d=ImageDraw.Draw(img,'RGBA')
    d.rectangle((0,0,W,H),fill=(0,0,0,42))
    d.line((55,175,115,175),fill=(196,166,116,230),width=4)
    d.text((55,200),'THE STANDARD',font=font(22,True),fill=(231,229,220,240),stroke_width=0)
    d.text((55,238),'90 DAYS TO REBUILD YOURSELF',font=font(15),fill=(179,178,170,210))
    upper=text.upper()
    f=font(57,True)
    lines=wrap_text(upper,d,f,605)
    while len(lines)>5:
        f=font(f.size-3,True);lines=wrap_text(upper,d,f,605)
    heights=[d.textbbox((0,0),l,font=f)[3] for l in lines]
    line_height=f.size+16
    top=430-(len(lines)-3)*29
    for i,line in enumerate(lines):
        y=top+i*line_height
        # soft shadow
        d.text((55+2,y+3),line,font=f,fill=(0,0,0,160),stroke_width=0)
        d.text((55,y),line,font=f,fill=(242,237,224,255))
    d.line((55,1080,665,1080),fill=(185,157,112,140),width=2)
    if scene==3:
        d.text((55,1103),'LINK IN BIO  /  $59  /  LIFETIME ACCESS',font=font(20,True),fill=(207,181,134,255))
    else:
        d.text((55,1103),'DISCIPLINE  /  FOCUS  /  SELF-RESPECT',font=font(17),fill=(199,196,185,210))
    img.convert('RGB').save(out,quality=95)

def run(cmd): subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)

def build(video,output):
    tmp=ROOT/'_frames'/video['slug'];tmp.mkdir(parents=True,exist_ok=True)
    clips=[]
    for i,segment in enumerate(video['frames']):
        png=tmp/f'scene_{i:02d}.png'; scene_png(segment,i,video['seed'],png)
        duration=float(video.get('seconds_per_scene',4.5))
        outfile=tmp/f'clip_{i:02d}.mp4'
        # modest movement via slow zoom; no external assets
        filt=f"zoompan=z='min(zoom+0.0007,1.09)':d=1:s=720x1280:fps=24,format=yuv420p"
        run(['ffmpeg','-y','-loop','1','-framerate','24','-i',str(png),'-vf',filt,'-t',str(duration),'-r','24','-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p',str(outfile)])
        clips.append(outfile)
    concat=tmp/'concat.txt';concat.write_text(''.join("file '"+str(c.resolve())+"'\n" for c in clips))
    noaudio=tmp/'noaudio.mp4'
    run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy',str(noaudio)])
    # Original synthetic dark ambient soundtrack. Avoid any copyrighted audio.
    total=len(clips)*float(video.get('seconds_per_scene',4.5))
    sound=f"0.055*sin(2*PI*55*t)+0.028*sin(2*PI*82.41*t)+0.018*sin(2*PI*110*t)"
    # use sine generators with low gain + fades
    run(['ffmpeg','-y','-i',str(noaudio),'-f','lavfi','-i','sine=frequency=55:sample_rate=44100', '-f','lavfi','-i','sine=frequency=82.41:sample_rate=44100', '-filter_complex',f'[1:a]volume=0.08[a1];[2:a]volume=0.04[a2];[a1][a2]amix=inputs=2:duration=longest,afade=t=in:st=0:d=1.5,afade=t=out:st={max(0,total-1.5)}:d=1.5[a]', '-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','96k','-t',str(total),'-movflags','+faststart',str(output)])

def main():
    a=argparse.ArgumentParser();a.add_argument('--all',action='store_true');a.add_argument('--slug');args=a.parse_args()
    scripts=json.loads((ROOT/'scripts.json').read_text())
    vids=scripts if args.all else [next((x for x in scripts if x['slug']==args.slug),scripts[0])]
    out=ROOT/'videos';out.mkdir(exist_ok=True)
    for v in vids:
        path=out/(v['slug']+'.mp4'); print('Rendering',path,flush=True);build(v,path)
if __name__=='__main__':main()
