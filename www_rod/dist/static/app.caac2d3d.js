(() => {
  const root = document.documentElement;
  root.classList.add("js");
  // Motyw: domyslnie JASNY (dekret 03.09: strona ogrodu, nie zasiek); przelacznik zapamietuje wybor
  let savedTheme = null;
  try { savedTheme = localStorage.getItem("rod-theme"); } catch (e) { /* prywatny tryb */ }
  if (savedTheme === "light" || savedTheme === "dark") root.dataset.theme = savedTheme;
  document.querySelector(".theme-toggle")?.addEventListener("click", () => {
    const next = root.dataset.theme === "dark" ? "light" : "dark";
    root.dataset.theme = next;
    try { localStorage.setItem("rod-theme", next); } catch (e) { /* ignoruj */ }
  });
  // Nawigacja na telefonie
  const navToggle = document.querySelector(".nav-toggle");
  const menu = document.querySelector("#menu");
  navToggle?.addEventListener("click", () => {
    const open = navToggle.getAttribute("aria-expanded") === "true";
    navToggle.setAttribute("aria-expanded", String(!open));
    menu?.classList.toggle("is-open", !open);
  });
  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape" || navToggle?.getAttribute("aria-expanded") !== "true") return;
    navToggle.setAttribute("aria-expanded", "false");
    menu?.classList.remove("is-open");
    navToggle.focus();
  });
  const currentPath = location.pathname.replace(/index\.html$/, "");
  menu?.querySelectorAll('a[href^="/"]').forEach((link) => {
    const linkPath = new URL(link.href, location.origin).pathname;
    if (linkPath === currentPath || (linkPath !== "/" && currentPath.startsWith(linkPath))) {
      link.setAttribute("aria-current", "page");
    }
  });
  document.querySelectorAll("[data-year]").forEach((el) => { el.textContent = String(new Date().getFullYear()); });
})();

// Pogoda w ogrodzie — pogoda.json odswiezany na serwerze co 30 min (Open-Meteo, Wozniki)
(async () => {
  const box = document.querySelector('#pogoda-teraz'); if (!box) return;
  const dni = document.querySelector('#pogoda-dni');
  const radar = document.querySelector('#pogoda-radar');
  try {
    const r = await fetch('/pogoda.json', { cache: 'no-store' }); if (!r.ok) throw new Error(r.status);
    const p = await r.json(); const t = p.teraz;
    // TERAZ (domyslnie widoczne) + podpowiedz kliknij
    box.innerHTML = `<div class="ikona">${t.ikona}</div><div class="teraz-tresc"><div class="temp">${t.temp}°C</div><div class="opis">${t.opis}</div>` +
      `<div class="detale">odczuwalna ${t.odczuwalna}° · wilgotność ${t.wilg}% · wiatr ${t.wiatr} km/h${t.opad_mm > 0 ? ' · opad ' + t.opad_mm + ' mm' : ''}</div></div>` +
      `<span class="pogoda-rozwin" aria-hidden="true">Prognoza 8 dni ▾</span>`;
    // PROGNOZA 8 DNI (po kliknieciu)
    dni.innerHTML = p.dni.map(d =>
      `<div class="pogoda-dzien"><div class="d">${d.dzien}</div><div class="dm">${d.dm}</div><div class="i" title="${d.opis}">${d.ikona}</div>` +
      `<div class="t">${d.max}° <span>/ ${d.min}°</span></div><div class="o">${d.opis}</div><div class="o">☔ ${d.szansa}%${d.opad_mm > 0 ? ' · ' + d.opad_mm + ' mm' : ''} · 💨 ${d.wiatr}</div></div>`).join('');
    box.addEventListener('click', () => {
      const otw = box.getAttribute('aria-expanded') === 'true';
      box.setAttribute('aria-expanded', String(!otw)); dni.hidden = otw;
      const et = box.querySelector('.pogoda-rozwin'); if (et) et.textContent = otw ? 'Prognoza 8 dni ▾' : 'Zwiń ▴';
    });
    // (slupki radaru usuniete — radar to teraz mapa Leaflet nizej)
    document.querySelector('#pogoda-stopka').textContent = `Aktualizacja ${p.aktualizacja} · dane Open-Meteo dla Woźnik`;
  } catch (e) { box.innerHTML = '<p class="muted">Prognoza chwilowo niedostępna.</p>'; }
})();

// Formularz kontaktowy: komunikaty po powrocie z /kontakt/wyslij
(() => {
  const q = new URLSearchParams(location.search);
  if (q.get('wyslano')) document.querySelector('#wyslano')?.classList.add('widoczny');
  if (q.get('blad')) document.querySelector('#blad')?.classList.add('widoczny');
})();

// Licznik odwiedzin (bez cookies; z logu serwera, co 5 min)
(async () => {
  const el = document.querySelector('#licznik-odwiedzin') || document.querySelector('#licznik'); if (!el) return;
  try {
    const r = await fetch('/licznik.json', { cache: 'no-store' }); if (!r.ok) return;
    const d = await r.json();
    el.textContent = `Odwiedziny: dziś ${d.dzis_goscie} · łącznie ${d.lacznie_goscie} gości (${d.lacznie_odslony} odsłon) od ${d.od.split('-').reverse().join('.')}`;
  } catch (e) { /* cicho */ }
})();

// Radar opadów — mapa Leaflet z animacją (LibreWXR przez /radar proxy: przeszłość + prognoza 60 min)
(function initRadar() {
  const host = document.querySelector('#radar-mapa');
  if (!host || typeof L === 'undefined') { if (host && typeof L === 'undefined') setTimeout(initRadar, 300); return; }
  const LAT = 50.588, LON = 18.989;
  const mapa = L.map(host, { zoomControl: false, attributionControl: true, dragging: false, scrollWheelZoom: false, doubleClickZoom: false, touchZoom: false, keyboard: false }).setView([LAT, LON], 8);
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 12, attribution: '© OpenStreetMap · radar: RainViewer/LibreWXR' }).addTo(mapa);
  L.circleMarker([LAT, LON], { radius: 5, color: '#2e7d4f', fillColor: '#2e7d4f', fillOpacity: 1, weight: 2 }).addTo(mapa);
  let klatki = [], warstwy = {}, idx = 0, gra = true, timer = null;
  const czasEl = document.querySelector('#radar-czas'), playEl = document.querySelector('#radar-play');
  function warstwaDla(fr) {
    if (warstwy[fr.time]) return warstwy[fr.time];
    const w = L.tileLayer(`/radar/kafel/${fr.time}/256/{z}/{x}/{y}/4/1_0.png`, { opacity: 0, maxZoom: 12, tileSize: 256 });
    w.addTo(mapa); warstwy[fr.time] = w; return w;
  }
  function pokaz(i) {
    if (!klatki.length) return;
    idx = (i + klatki.length) % klatki.length;
    klatki.forEach((fr, k) => { const w = warstwaDla(fr); w.setOpacity(k === idx ? 0.75 : 0); });
    const fr = klatki[idx]; const d = new Date(fr.time * 1000);
    const g = d.getHours().toString().padStart(2, '0') + ':' + d.getMinutes().toString().padStart(2, '0');
    czasEl.textContent = fr.przyszlosc ? `${g} · prognoza` : (k => k)(g);
    czasEl.classList.toggle('prognoza', !!fr.przyszlosc);
  }
  function nastepna() { pokaz(idx + 1); }
  function pętla() { clearInterval(timer); if (gra) timer = setInterval(nastepna, 700); }
  async function wczytaj() {
    try {
      const r = await fetch('/radar/meta', { cache: 'no-store' }); if (!r.ok) throw 0;
      const d = await r.json();
      const past = (d.past || []).slice(-8).map(f => ({ ...f, przyszlosc: false }));
      const now = (d.nowcast || []).map(f => ({ ...f, przyszlosc: true }));
      const nowe = [...past, ...now];
      if (!nowe.length) { host.parentElement.style.display = 'none'; return; }
      klatki = nowe; idx = Math.max(0, past.length - 1); pokaz(idx); pętla();
    } catch (e) { if (host.parentElement) host.parentElement.style.display = 'none'; }
  }
  if (playEl) playEl.addEventListener('click', () => { gra = !gra; playEl.textContent = gra ? '⏸' : '▶'; playEl.setAttribute('aria-label', gra ? 'Pauza' : 'Odtwórz'); pętla(); });
  wczytaj();
  setInterval(wczytaj, 5 * 60 * 1000); // odswiez klatki co 5 min
})();

// Zegar analogowy na logo ROD — same wskazówki (nie zasłaniają napisu)
(function zegarHero() {
  const svg = document.querySelector('#zegar-hero'); if (!svg) return;
  const g = svg.querySelector('.wsk-godz'), m = svg.querySelector('.wsk-min'), s = svg.querySelector('.wsk-sek');
  function tik() {
    const t = new Date();
    const sek = t.getSeconds() + t.getMilliseconds() / 1000;
    const min = t.getMinutes() + sek / 60;
    const godz = (t.getHours() % 12) + min / 60;
    g.style.transform = `rotate(${godz * 30}deg)`;
    m.style.transform = `rotate(${min * 6}deg)`;
    s.style.transform = `rotate(${sek * 6}deg)`;
    requestAnimationFrame(tik);
  }
  const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) { // bez sekundnika, ale ustaw godzinę+minutę raz
    const t = new Date(); g.style.transform = `rotate(${((t.getHours()%12)+t.getMinutes()/60)*30}deg)`; m.style.transform = `rotate(${t.getMinutes()*6}deg)`;
  } else tik();
})();
