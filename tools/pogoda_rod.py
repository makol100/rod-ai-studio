#!/usr/bin/env python3
"""Pogoda dla strony ROD (Wozniki 50.588,18.989, Open-Meteo — to samo zrodlo co Barometr): teraz + 7 dni -> pogoda.json (dist + wolumen Caddy)."""
import json, urllib.request, urllib.parse, datetime, os, sys
LAT, LON = 50.588, 18.989
WMO = {0:("Słonecznie","☀️"),1:("Przeważnie słonecznie","🌤️"),2:("Częściowe zachmurzenie","⛅"),3:("Pochmurno","☁️"),45:("Mgła","🌫️"),48:("Mgła osadzająca szadź","🌫️"),
 51:("Lekka mżawka","🌦️"),53:("Mżawka","🌦️"),55:("Gęsta mżawka","🌧️"),56:("Marznąca mżawka","🌧️"),57:("Marznąca mżawka","🌧️"),61:("Lekki deszcz","🌦️"),63:("Deszcz","🌧️"),65:("Ulewa","🌧️"),
 66:("Marznący deszcz","🌧️"),67:("Marznący deszcz","🌧️"),71:("Lekki śnieg","🌨️"),73:("Śnieg","🌨️"),75:("Intensywny śnieg","❄️"),77:("Ziarna śniegu","🌨️"),80:("Przelotny deszcz","🌦️"),81:("Przelotne opady","🌧️"),
 82:("Gwałtowne opady","⛈️"),85:("Przelotny śnieg","🌨️"),86:("Śnieżyca","❄️"),95:("Burza","⛈️"),96:("Burza z gradem","⛈️"),99:("Burza z gradem","⛈️")}
DNI = ["pon.","wt.","śr.","czw.","pt.","sob.","niedz."]
def main():
    q = urllib.parse.urlencode({"latitude":LAT,"longitude":LON,"timezone":"Europe/Warsaw","forecast_days":8,
        "current":"temperature_2m,apparent_temperature,relative_humidity_2m,precipitation,weather_code,wind_speed_10m,wind_gusts_10m",
        "hourly":"precipitation,precipitation_probability,weather_code,temperature_2m",
        "daily":"weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,sunrise,sunset,uv_index_max"})
    d = json.load(urllib.request.urlopen("https://api.open-meteo.com/v1/forecast?"+q, timeout=30))
    c = d["current"]; op = WMO.get(c["weather_code"], ("—","🌡️"))
    teraz = {"temp":round(c["temperature_2m"]),"odczuwalna":round(c["apparent_temperature"]),"wilg":c["relative_humidity_2m"],"opad_mm":c["precipitation"],
             "wiatr":round(c["wind_speed_10m"]),"porywy":round(c["wind_gusts_10m"]),"opis":op[0],"ikona":op[1],"czas":c["time"][11:16]}
    dni=[]
    dd=d["daily"]
    for i,data in enumerate(dd["time"]):
        dt=datetime.date.fromisoformat(data); o=WMO.get(dd["weather_code"][i],("—","🌡️"))
        dni.append({"data":data,"dzien":"dziś" if i==0 else ("jutro" if i==1 else DNI[dt.weekday()]),"dm":f"{dt.day}.{dt.month:02d}","max":round(dd["temperature_2m_max"][i]),"min":round(dd["temperature_2m_min"][i]),
                    "opad_mm":round(dd["precipitation_sum"][i],1),"szansa":dd["precipitation_probability_max"][i],"wiatr":round(dd["wind_speed_10m_max"][i]),"opis":o[0],"ikona":o[1],
                    "wschod":dd["sunrise"][i][11:16],"zachod":dd["sunset"][i][11:16],"uv":round(dd["uv_index_max"][i] or 0)})
    # radar/prognoza godzinowa opadow: 12h w przod od teraz
    godziny=[]
    try:
        h=d["hourly"]; teraz_iso=c["time"][:13]  # do godziny
        start=next((k for k,t in enumerate(h["time"]) if t[:13]>=teraz_iso), 0)
        for k in range(start, min(start+12, len(h["time"]))):
            oh=WMO.get(h["weather_code"][k],("—","🌡️"))
            godziny.append({"godz":h["time"][k][11:16],"opad_mm":round(h["precipitation"][k],1),"szansa":h["precipitation_probability"][k] or 0,"temp":round(h["temperature_2m"][k]),"ikona":oh[1]})
    except Exception as e:
        print("hourly",e,file=sys.stderr)
    out={"miejsce":"Woźniki","aktualizacja":datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2))).strftime("%d.%m %H:%M"),"teraz":teraz,"dni":dni[:8],"godziny":godziny,"zrodlo":"Open-Meteo"}
    for p in ("/root/rod-ai-studio/www_rod/dist/pogoda.json","/var/lib/docker/volumes/caddy_mcp_data/_data/www_rod/pogoda.json"):
        try:
            os.makedirs(os.path.dirname(p),exist_ok=True); open(p+".tmp","w",encoding="utf-8").write(json.dumps(out,ensure_ascii=False)); os.chmod(p+".tmp",0o644); os.replace(p+".tmp",p)
        except Exception as e: print("zapis",p,e,file=sys.stderr)
    print(f"pogoda OK: teraz {teraz['temp']}°C {teraz['opis']}, dni={len(dni)}")
if __name__=="__main__": main()
