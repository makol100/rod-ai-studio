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
    // RADAR OPADOW — 12h w przod (slupki opadu + szansa%)
    if (radar && Array.isArray(p.godziny) && p.godziny.length) {
      const maxOpad = Math.max(0.5, ...p.godziny.map(g => g.opad_mm));
      const jestOpad = p.godziny.some(g => g.opad_mm > 0 || g.szansa >= 30);
      radar.innerHTML =
        `<div class="radar-tytul">Radar opadów · 12 h${jestOpad ? '' : ' · sucho'}</div>` +
        `<div class="radar-slupki">` + p.godziny.map(g => {
          const h = Math.round((g.opad_mm / maxOpad) * 100);
          const kolor = g.szansa >= 60 ? 'mokro' : (g.szansa >= 30 ? 'mzawka' : 'sucho');
          return `<div class="radar-godz" title="${g.godz} · ${g.opad_mm} mm · ${g.szansa}%"><div class="radar-bar ${kolor}" style="height:${Math.max(4,h)}%"></div><div class="radar-g">${g.godz.slice(0,2)}</div></div>`;
        }).join('') + `</div>` +
        `<div class="radar-legenda"><span><i class="mokro"></i>deszcz</span><span><i class="mzawka"></i>mżawka</span><span><i class="sucho"></i>sucho</span></div>`;
    }
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
