import asyncio, json
from playwright.async_api import async_playwright
Z={'zrzut_oplaty_pzd.png':'http://pzd.pl/artykuly/29962/188/STANOWISKO-KRAJOWEJ-KOMISJI-REWIZYJNEJ-POLSKIEGO-ZWIaZKU-DZIAlKOWCoW-z-dnia-26-sierpnia-2026-r-w-sprawie-projektu-ustawy-o-zmianie-ustawy-o-gospodarowaniu-nieruchomosciami-rolnymi-Skarbu-Panstwa-oraz-ustawy-o-gospodarce-nieruchomosciami.html',
   'zrzut_oplaty_farmer.png':'https://www.farmer.pl/prawo/przepisy-i-regulacje/o-1200-zl-rosnie-oplata-za-dzialki-nadchodza-nowe-stawki,183862.html',
   'zrzut_dziki.png':'https://www.rodw.pl/wydarzenia.htm',
   'zrzut_pozar.png':'https://walczon.pl/pozar-smietnika-w-rod-ikar-w-miroslawcu-gornym-interwencja-osp-miroslawiec/',
   'zrzut_dotacje.png':'http://pzd.pl/artykuly/29969/188/Krajowy-Zarzad-PZD-przyznal-fundusze-na-inwestycje-i-remonty-w-ROD.html',
   'zrzut_brama.png':'https://rodrelaksszczaki.pl/otwieranie-bramy-nr-4-telefonem-przypomnienie/',
   'zrzut_ruda.png':'https://rudaslaska.com.pl/artykuly/artykul/rod-im-ks-jana-dzierzona-swietowal-110-lecie-to-miejsce-tworzyly-pokolenia-rudzkich-dzialkowcow',
   'zrzut_siedlce.png':'https://siedlce.pl/aktualnosci/2026/09-2026/piknik-w-rod-zlote-piaski/show',
   'zrzut_dzialkowiec.png':'http://pzd.pl/artykuly/29971/188/Czytajcie-Dzialkowca.html',
   'zrzut_klimat.png':'http://pzd.pl/artykuly/29963/188/STANOWISKO-KRAJOWEJ-KOMISJI-REWIZYJNEJ-POLSKIEGO-ZWIaZKU-DZIAlKOWCoW-z-dnia-26-sierpnia-2026-r-w-sprawie-raportu-strategicznego-Polskiego-Zwiazku-Dzialkowcow-Rodzinne-ogrody-dzialkowe-w-polityce-klimatycznej-panstwa.html'}
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); ok={}
        for fn,u in Z.items():
            try:
                pg=await b.new_page(viewport={'width':1080,'height':1400},device_scale_factor=2)
                await pg.goto(u,wait_until='domcontentloaded',timeout=60000); await pg.wait_for_timeout(2500)
                # zamknij cookie-bannery
                for sel in ('button:has-text("Akceptuj")','button:has-text("Zgadzam")','button:has-text("Zaakceptuj")','button:has-text("Accept")','#onetrust-accept-btn-handler'):
                    try: await pg.click(sel,timeout=1500); break
                    except Exception: pass
                await pg.evaluate("window.scrollTo(0,150)"); await pg.wait_for_timeout(500)
                await pg.screenshot(path=fn,full_page=False); ok[fn]=u; await pg.close(); print('OK',fn)
            except Exception as e: print('FAIL',fn,str(e)[:70])
        await b.close()
    json.dump(ok,open('manifest_zrzuty.json','w'),indent=1,ensure_ascii=False)
asyncio.run(main())
