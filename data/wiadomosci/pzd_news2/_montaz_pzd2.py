#!/usr/bin/env python3
"""Montaż rolki „Przegląd z ogrodów działkowych" — 0 zł: plansze (Ken Burns) + klon głosu Tomasza + outro; intro doklejane tools/dolacz_intro.py."""
import subprocess, json, pathlib, sys
B = pathlib.Path("/root/rod-ai-studio/data/wiadomosci/pzd_news2")
PL = B/"plansze"; GL = B/"glos/final"; SEG = B/"segmenty"; SEG.mkdir(exist_ok=True)
ORDER = ['N0','N1a','N1b','N2a','N2b','N3','N4a','N4b','N5','N6','N7','N8a','N8b','N9','NK']
PAD = 0.45
def dur(p): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(p)],capture_output=True,text=True).stdout.strip())
segs = []
for i, n in enumerate(ORDER):
    a = GL/f"{n}.wav"; d = dur(a) + PAD; out = SEG/f"{i:02d}_{n}.mp4"
    zoom_in = (i % 2 == 0)
    z = "min(1+0.00022*on,1.09)" if zoom_in else "max(1.09-0.00022*on,1.0)"
    vf = (f"scale=2160:3840,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,format=yuv420p")
    subprocess.run(['ffmpeg','-y','-v','error','-loop','1','-framerate','30','-i',str(PL/f"{n}.png"),'-i',str(a),
        '-filter_complex',f"[0:v]{vf}[v];[1:a]apad=pad_dur={PAD},aresample=48000,aformat=channel_layouts=stereo[a]",
        '-map','[v]','-map','[a]','-t',f"{d:.3f}",'-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k',str(out)],check=True)
    segs.append(out); print(n, f"{d:.1f}s", flush=True)
# outro 4.5 s cisza
out = SEG/"99_OUTRO.mp4"
subprocess.run(['ffmpeg','-y','-v','error','-loop','1','-framerate','30','-i',str(PL/"OUTRO.png"),'-f','lavfi','-i','anullsrc=r=48000:cl=stereo',
    '-filter_complex',"[0:v]scale=1080:1920,format=yuv420p[v]",'-map','[v]','-map','1:a','-t','4.5','-c:v','libx264','-preset','veryfast','-crf','20','-c:a','aac','-b:a','160k',str(out)],check=True)
segs.append(out)
# concat z normalizacja (filter_complex, nigdy demuxer)
inputs=[]; 
for s in segs: inputs += ['-i', str(s)]
fc = "".join(f"[{i}:v]scale=1080:1920,fps=30,format=yuv420p[v{i}];[{i}:a]aresample=48000,aformat=channel_layouts=stereo[a{i}];" for i in range(len(segs)))
fc += "".join(f"[v{i}][a{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=1[v][a]"
body = B/"PZD_NEWS2_body.mp4"
subprocess.run(['ffmpeg','-y','-v','error']+inputs+['-filter_complex',fc,'-map','[v]','-map','[a]','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k',str(body)],check=True)
print("body:", f"{dur(body):.1f}s")
r = subprocess.run(['python3','/root/rod-ai-studio/tools/dolacz_intro.py',str(body),'--wyjscie',str(B/"PZD_NEWS2_v1.mp4")],capture_output=True,text=True)
print(r.stdout[-1500:], r.stderr[-800:])
print("FINAL:", f"{dur(B/'PZD_NEWS2_v1.mp4'):.1f}s")
