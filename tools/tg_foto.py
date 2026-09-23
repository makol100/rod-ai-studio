#!/usr/bin/env python3
"""Wyslij zdjecie/obraz Tomaszowi na Telegram NATYCHMIAST (dekret 23.09.2026, D-0522). Uzycie: tg_foto.py <plik> "<podpis>"  — dla calej zalogi."""
import sys, urllib.request, uuid, json, os
sys.path.insert(0, "/root/rod-ai-studio/tools")
import hans_ucho as h
def wyslij(plik, podpis=""):
    tok, czat = h._wczytaj_token_hansa(); b = uuid.uuid4().hex
    def fld(n, v): return f'--{b}\r\nContent-Disposition: form-data; name="{n}"\r\n\r\n{v}\r\n'.encode()
    data = fld("chat_id", str(czat)) + fld("caption", podpis[:1000])
    ext = os.path.splitext(plik)[1].lower(); mime = "image/png" if ext == ".png" else "image/jpeg"
    data += f'--{b}\r\nContent-Disposition: form-data; name="photo"; filename="{os.path.basename(plik)}"\r\nContent-Type: {mime}\r\n\r\n'.encode() + open(plik, "rb").read() + f"\r\n--{b}--\r\n".encode()
    r = urllib.request.Request(f"https://api.telegram.org/bot{tok}/sendPhoto", data=data, headers={"Content-Type": f"multipart/form-data; boundary={b}"})
    return json.load(urllib.request.urlopen(r, timeout=60)).get("ok")
if __name__ == "__main__":
    print("na Telegram:", wyslij(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else ""))
