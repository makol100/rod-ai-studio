import sys
sys.path.insert(0, '/app')
from src.zarty_produkcja import ASS_HEADER, KOLORY_ASS

def czas(s):
    h = int(s // 3600); m = int(s % 3600 // 60); sec = s % 60
    return f"{h}:{m:02d}:{sec:05.2f}"

B = '/root/rod-ai-studio/data/zarty/10004'
kt = KOLORY_ASS.get('TOMASZ', '&H00FFFFFF')
kj = KOLORY_ASS.get('JÓZEK', KOLORY_ASS.get('JOZEK', '&H00FFFFFF'))
km = KOLORY_ASS.get('MIECZYSŁAW', KOLORY_ASS.get('MIECZYSLAW', '&H00FFFFFF'))

pliki = {
 'napisy_g01.ass': [
  (0.4, 4.8, kt, 'TOMASZ: Znowu mi ktoś jabłka podżera! Idę i złapię go za jajca!')],
 'napisy_g02a.ass': [
  (0.4, 5.4, kt, 'TOMASZ: Ktoś ty?! Pytam, ktoś ty?!')],
 'napisy_g02b.ass': [
  (0.2, 1.3, kj, 'JÓZEK: Józek......'),
  (1.3, 2.5, kt, 'TOMASZ: Jaki Józek?!'),
  (2.5, 5.6, km, 'MIECZYSŁAW: Józek... ten niemowa!')],
}
for nazwa, linie in pliki.items():
    tresc = ''.join(
        f"Dialogue: 0,{czas(a)},{czas(b)},Default,,0,0,0,,{{\\c{k}}}{t}\n"
        for a, b, k, t in linie)
    open(f'{B}/{nazwa}', 'w', encoding='utf-8').write(ASS_HEADER + tresc)
    print(nazwa, 'OK')
