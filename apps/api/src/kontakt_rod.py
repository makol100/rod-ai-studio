"""Formularz kontaktowy strony ROD (dekret 03.09): POST /kontakt/wyslij → zapis + Telegram do zarzadu + e-mail na rodwozniki@gmail.com (gdy skonfigurowany SMTP)."""
import json, os, time, re, smtplib, ssl, sys
from email.message import EmailMessage
from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
router = APIRouter()
KATALOG = "/root/rod-ai-studio/data/kontakt"
ADRES_ROD = "rodwozniki@gmail.com"
def _sekret(nazwa):
    for p in ("/root/rod-ai-studio/data/.secrets/smtp.env",):
        try:
            for l in open(p, encoding="utf-8"):
                if l.startswith(nazwa + "="): return l.split("=", 1)[1].strip().strip('"\'')
        except Exception: pass
    return None
def _telegram(tekst):
    try:
        import urllib.request, urllib.parse
        tok = czat = None
        for l in open("/root/rod-ai-studio/data/.secrets/hans.env", encoding="utf-8"):
            k, _, v = l.strip().partition("=")
            if k == "HANS_BOT_TOKEN": tok = v.strip()
            if k == "HANS_CHAT_ID": czat = v.strip()
        r = urllib.request.urlopen(f"https://api.telegram.org/bot{tok}/sendMessage", data=urllib.parse.urlencode({"chat_id": czat, "text": tekst[:3900]}).encode(), timeout=20)
        print("kontakt: telegram", r.status)
    except Exception as e: print("kontakt: telegram nie poszedl:", e)
def _email(temat, tresc, odpowiedz_do):
    haslo = _sekret("GMAIL_APP_PASSWORD"); user = _sekret("GMAIL_USER") or ADRES_ROD
    if not haslo: return False
    m = EmailMessage(); m["From"] = user; m["To"] = ADRES_ROD; m["Subject"] = temat
    if odpowiedz_do: m["Reply-To"] = odpowiedz_do
    m.set_content(tresc)
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as s:
        s.starttls(context=ssl.create_default_context()); s.login(user, haslo); s.send_message(m)
    return True
@router.post("/kontakt/wyslij")
def kontakt_wyslij(req: Request, imie: str = Form(""), email: str = Form(""), tresc: str = Form(""), zgoda: str = Form(""), www: str = Form("")):
    if www.strip():  # honeypot — boty wypelniaja ukryte pole
        return RedirectResponse("/kontakt/?wyslano=1", status_code=303)
    imie, email, tresc = imie.strip()[:120], email.strip()[:200], tresc.strip()[:4000]
    if not tresc or not zgoda or (email and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email)):
        return RedirectResponse("/kontakt/?blad=1", status_code=303)
    os.makedirs(KATALOG, exist_ok=True)
    rek = {"ts": time.time(), "imie": imie, "email": email, "tresc": tresc, "ip": req.headers.get("x-forwarded-for", "").split(",")[0].strip()}
    with open(os.path.join(KATALOG, time.strftime("%Y%m%d_%H%M%S") + ".json"), "w", encoding="utf-8") as f: json.dump(rek, f, ensure_ascii=False, indent=1)
    tekst = f"Wiadomosc ze strony rodwozniki.pl\nOd: {imie or '(bez imienia)'} <{email or 'bez e-maila'}>\n\n{tresc}"
    _telegram("📬 " + tekst)
    try: mail_ok = _email(f"[rodwozniki.pl] Wiadomość od {imie or 'anonim'}", tekst, email or None)
    except Exception as e: print("kontakt: e-mail nie poszedl:", e); mail_ok = False
    return RedirectResponse("/kontakt/?wyslano=1", status_code=303)
