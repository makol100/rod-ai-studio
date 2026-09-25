# Rolka mieczyki+dalie+zimowit — narracja Scrimba Explain (guide0vibul08t) + zdjecia na PELNY EKRAN (uklad pH v3, D-0586)
import subprocess,re,json
FPS=30; W,H=1080,1920; GAP=0.30
SEG=['pop/x','all/3','all/5','all/7','pop/7','all/b','all/d','all/f','all/h','pop/g','all/l']   # v2: S1,S5,S10 podmienione (D-0595)   # kolejnosc scen 1..11 (sprawdzona transkrypcja Gemini 2.5 + 3.8)
dur=[float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'explain/{s}.webm'],capture_output=True,text=True).stdout) for s in SEG]
FOTO=[['C_M1_mieczyk','C_M1b_mieczyk'],['M2_zolkniece'],['M3c_bulwa','M3b_bulwy'],['M4_suszenie'],['C_D5_dalia'],['D6_mroz','D6b_karpa'],['D7_piwnica'],['C_Z8_zimowit'],['C_Z9_liscie'],['C_Z10_preciki'],['C_Z8b_zimowit']]
NAG=['MIECZYKI — WYKOP JESIENIĄ']*4+['DALIE — DOPIERO PO MROZIE']*3+['UWAGA: ZIMOWIT JESIENNY TRUJE']*4
LEK=[b.split('LEKTOR:',1)[1].strip() for b in open('scenes.txt',encoding='utf-8').read().split('SCENA ')[1:]]
assert len(LEK)==11
# audio: segmenty + przerwy
cmd=['ffmpeg','-v','error','-y']; fc=''; k=0
for i,s in enumerate(SEG):
    cmd+=['-i',f'explain/{s}.webm']
for i in range(11):
    pad = GAP if i<10 else 0.8
    fc+=f'[{i}:a]aresample=48000,apad=pad_dur={pad}[a{i}];'
fc+=''.join(f'[a{i}]' for i in range(11))+'concat=n=11:v=0:a=1,loudnorm=I=-16:TP=-1.5,aresample=48000[a]'
subprocess.run(cmd+['-filter_complex',fc,'-map','[a]','-ac','2','-c:a','pcm_s16le','narracja.wav'],check=True)
# obraz
lst=open('klipy.txt','w'); t0=0.0; starts=[]; n=0
for i in range(11):
    D=dur[i]+(GAP if i<10 else 0.8); starts.append(t0)
    fot=FOTO[i]; part=D/len(fot)
    for j,f in enumerate(fot):
        fr=int(round(part*FPS)); out=f'klip_{n:02d}.mp4'; n+=1
        dx = 1 if n%2 else -1
        # cover 110%, potem przesuw w poziomie max 160 px i lekki w pionie
        vf=(f"scale='if(gt(a,{W}/{H}),-2,{int(W*1.1)})':'if(gt(a,{W}/{H}),{int(H*1.1)},-2)':flags=lanczos,"
            f"crop={W}:{H}:x='(iw-ow)/2+{dx}*min((iw-ow)/2,80)*(2*n/{fr}-1)':y='(ih-oh)/2+{-dx}*min((ih-oh)/2,40)*(2*n/{fr}-1)',format=yuv420p")
        subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-framerate',str(FPS),'-i',f'foto/{f}.jpg','-vf',vf,'-frames:v',str(fr),'-c:v','libx264','-crf','18',out],check=True)
        lst.write(f"file '{out}'\n")
    t0+=D
lst.close()
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','klipy.txt','-c','copy','obraz.mp4'],check=True)
# napisy
def ts(t): h=int(t//3600); m=int(t%3600//60); s=t%60; return f"{h}:{m:02d}:{s:05.2f}"
ev=[]; i=0
while i<11:
    j=i
    while j+1<11 and NAG[j+1]==NAG[i]: j+=1
    end=starts[j]+dur[j]+(GAP if j<10 else 0.8)
    ev.append(f"Dialogue: 0,{ts(starts[i])},{ts(end-0.05)},Gora,,0,0,0,,{{\\fad(150,150)}}{NAG[i]}"); i=j+1
for i,txt in enumerate(LEK):
    slowa=txt.split(); chunks=[]; cur=[]
    for w in slowa:
        cur.append(w); L=len(' '.join(cur))
        if L>=26 or (w.endswith(('.',',',':','?','!','—')) and L>=14): chunks.append(' '.join(cur)); cur=[]
    if cur: chunks.append(' '.join(cur))
    tot=sum(len(c)+3 for c in chunks); t=starts[i]+0.10
    for c in chunks:
        dd=(dur[i]-0.15)*(len(c)+3)/tot
        ev.append(f"Dialogue: 0,{ts(t)},{ts(t+dd-0.03)},Dol,,0,0,0,,{c}"); t+=dd
TOTAL=t0
head=open('/root/rod-ai-studio/data/scrimba/pelny.ass',encoding='utf-8').read().split('[Events]')[0]
ev.append(f"Dialogue: 0,{ts(0)},{ts(TOTAL)},Marka,,0,0,0,,Mieczyki · dalie · zimowit · rodwozniki.pl")
open('mdz.ass','w',encoding='utf-8').write(head+'[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'+'\n'.join(ev)+'\n')
nap=' '.join(e.split(',,',1)[1] for e in ev if ',Dol,' in e).split(); zn=' '.join(LEK).split()
print('NAPISY==SCENARIUSZ:',nap==zn,len(nap),len(zn),'| czas',round(TOTAL,2),'| klipow',n)
subprocess.run(['ffmpeg','-v','error','-y','-i','obraz.mp4','-i','narracja.wav','-vf','ass=mdz.ass','-c:v','libx264','-crf','21','-preset','medium','-pix_fmt','yuv420p','-g','60','-keyint_min','60','-sc_threshold','0','-c:a','aac','-b:a','160k','-ar','48000','-ac','2','-shortest','-movflags','+faststart','mdz_rolka_v2.mp4'],check=True)
print(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration,size','-of','csv=p=0','mdz_rolka_v2.mp4'],capture_output=True,text=True).stdout)
