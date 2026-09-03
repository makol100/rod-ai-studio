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
  document.querySelectorAll("[data-year]").forEach((el) => { el.textContent = String(new Date().getFullYear()); });
})();

// Pogoda w ogrodzie — pogoda.json odswiezany na serwerze co 30 min (Open-Meteo, Wozniki)
(async () => {
  const box = document.querySelector('#pogoda-teraz'); if (!box) return;
  try {
    const r = await fetch('/pogoda.json', { cache: 'no-store' }); if (!r.ok) throw new Error(r.status);
    const p = await r.json(); const t = p.teraz;
    box.innerHTML = `<div class="ikona">${t.ikona}</div><div><div class="temp">${t.temp}°C</div><div class="opis">${t.opis}</div></div>` +
      `<div class="detale">odczuwalna ${t.odczuwalna}°C · wilgotność ${t.wilg}% · wiatr ${t.wiatr} km/h (porywy ${t.porywy})${t.opad_mm > 0 ? ' · opad ' + t.opad_mm + ' mm' : ''}</div>`;
    document.querySelector('#pogoda-dni').innerHTML = p.dni.map(d =>
      `<div class="pogoda-dzien"><div class="d">${d.dzien}</div><div class="dm">${d.dm}</div><div class="i" title="${d.opis}">${d.ikona}</div>` +
      `<div class="t">${d.max}° <span>/ ${d.min}°</span></div><div class="o">${d.opis}</div><div class="o">☔ ${d.szansa}%${d.opad_mm > 0 ? ' · ' + d.opad_mm + ' mm' : ''} · 💨 ${d.wiatr}</div></div>`).join('');
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
  const el = document.querySelector('#licznik'); if (!el) return;
  try {
    const r = await fetch('/licznik.json', { cache: 'no-store' }); if (!r.ok) return;
    const d = await r.json();
    el.textContent = `Odwiedziny: dziś ${d.dzis_goscie} · łącznie ${d.lacznie_goscie} gości (${d.lacznie_odslony} odsłon) od ${d.od.split('-').reverse().join('.')}`;
  } catch (e) { /* cicho */ }
})();
