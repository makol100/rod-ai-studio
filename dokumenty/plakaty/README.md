# Plakaty i grafiki informacyjne ROD Woźniki

Plakaty A4 dla działkowców — źródła HTML + gotowe PDF/PNG.

## Plakat: wyłączenie wewnętrznej sieci działkowej (30.11.2026)

Dekret Tomasza 20.09.2026: plakat A4, pastelowy, na białym tle, z graficznymi dodatkami
w stylu ogrodowym/PZD, informujący działkowców o terminie **30 listopada 2026 r.**
(sprawdzone: listopad ma 30 dni, 30.11.2026 to poniedziałek — ostatni dzień miesiąca),
w którym zostanie wyłączona wewnętrzna sieć działkowa.

- źródło: `wylaczenie_sieci_30-11-2026.html` (render: Chromium headless → PDF A4)
- assety: logo ROD (`assets/branding/rod_logo_kolo.png`) i znak ISO 7010 W012
  (`dokumenty/elektryk/assets/znak_elektryk.svg`) — te same co w oświadczeniach elektryka

### Jak wyrenderować

```bash
# w katalogu z html + logo_rod.png + znak_elektryk.svg obok
node -e "const{chromium}=require('playwright');(async()=>{const b=await chromium.launch();
const p=await b.newPage();await p.goto('file://'+process.cwd()+'/wylaczenie_sieci_30-11-2026.html',{waitUntil:'networkidle'});
await p.waitForTimeout(1500);await p.pdf({path:'plakat.pdf',format:'A4',printBackground:true,pageRanges:'1'});await b.close()})()"
```

### Pułapka (kosztowała kilka podejść)

Elementy tła wystające poza krawędź strony (dekoracyjne koła z ujemnym `top`/`right`)
powodują w druku Chromium **shrink-to-fit** — cała zawartość zjeżdża w skali ~0,9
i na dole zostaje biały pas. Lekarstwo: trzymać całą dekorację w kontenerze
`.tlo { position:absolute; inset:0; overflow:hidden }`, nigdy luzem w `body`.
Po każdej zmianie sprawdzać render z PDF (`pdftoppm`), nie screenshotem przeglądarki —
screenshot ma inną wysokość viewportu i kłamie.

### Status

PDF i PNG wystawione Tomaszowi 20.09.2026. **Nie publikować** na stronie ani FB
bez jego wyraźnego „publikuj".
