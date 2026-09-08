#!/usr/bin/env python3
"""Zamazuje (pikseluje) WSZYSTKIE osoby na zdjęciach/wideo — YOLOv8n (COCO klasa 0 = person), CPU.
Użycie: python3 tools/zamaz_ludzi.py WEJ [WEJ...] --do KATALOG  (jpg/png/mp4). Ramka powiększona o 15%, dla wideo pamięć 12 klatek (zanik nie odsłania)."""
import sys, argparse, subprocess
from pathlib import Path
import cv2, numpy as np
from ultralytics import YOLO
ap=argparse.ArgumentParser(); ap.add_argument('wej',nargs='+'); ap.add_argument('--do',required=True); ap.add_argument('--conf',type=float,default=0.25)
A=ap.parse_args(); cel=Path(A.do); cel.mkdir(parents=True,exist_ok=True)
model=YOLO('yolov8n.pt')
def boxy(img):
    r=model.predict(img,classes=[0],conf=A.conf,imgsz=960,verbose=False)[0]
    out=[]
    for b in r.boxes.xyxy.cpu().numpy():
        x1,y1,x2,y2=b; w,h=x2-x1,y2-y1; m=0.15
        out.append([max(0,x1-w*m),max(0,y1-h*m),min(img.shape[1],x2+w*m),min(img.shape[0],y2+h*m)])
    return out
def zamaz(img,bx):
    for x1,y1,x2,y2 in bx:
        x1,y1,x2,y2=map(int,(x1,y1,x2,y2))
        if x2-x1<4 or y2-y1<4: continue
        roi=img[y1:y2,x1:x2]; k=max(6,(x2-x1)//14)
        mal=cv2.resize(roi,(max(1,(x2-x1)//k),max(1,(y2-y1)//k)),interpolation=cv2.INTER_LINEAR)
        img[y1:y2,x1:x2]=cv2.resize(mal,(x2-x1,y2-y1),interpolation=cv2.INTER_NEAREST)
    return img
for w in A.wej:
    p=Path(w)
    if p.suffix.lower() in ('.jpg','.jpeg','.png'):
        img=cv2.imread(str(p)); bx=boxy(img); img=zamaz(img,bx)
        cv2.imwrite(str(cel/p.name),img,[cv2.IMWRITE_JPEG_QUALITY,86]); print(p.name,'osob:',len(bx))
    else:
        cap=cv2.VideoCapture(str(p)); fps=cap.get(cv2.CAP_PROP_FPS); W=int(cap.get(3)); H=int(cap.get(4)); n=int(cap.get(7))
        tmp=str(cel/('_tmp_'+p.stem+'.mp4')); out=cv2.VideoWriter(tmp,cv2.VideoWriter_fourcc(*'mp4v'),fps,(W,H))
        pamiec=[]; i=0; maxo=0
        while True:
            ok,fr=cap.read()
            if not ok: break
            bx=boxy(fr) if i%2==0 else []
            pamiec.append(bx); pamiec=pamiec[-12:]
            wszystkie=[b for lst in pamiec for b in lst]; maxo=max(maxo,len(bx))
            out.write(zamaz(fr,wszystkie)); i+=1
        cap.release(); out.release()
        fin=str(cel/p.name)
        subprocess.run(['ffmpeg','-v','error','-y','-i',tmp,'-i',str(p),'-map','0:v','-map','1:a?','-c:v','libx264','-crf','24','-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart','-c:a','aac','-b:a','96k',fin],check=True)
        Path(tmp).unlink(); print(p.name,'klatek:',i,'max osob w klatce:',maxo)
