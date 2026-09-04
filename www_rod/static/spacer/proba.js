// Spacer 360 (D-0311): pełne ładowanie z paskiem postępu na starcie,
// potem płynne chodzenie bez doładowywania; nawigacja: strzałki + podwójny klik/tap wszędzie.
var SCENY = {
  parking: { tytul: 'Parking',    url: '/static/spacer/parking.jpg',
             sasiedzi: [{ scena: 'plac', yaw: 118 }],
             strzalki: [{ pitch: -4, yaw: 118, sceneId: 'plac', text: 'Plac zabaw', targetYaw: 95 }] },
  plac:    { tytul: 'Plac zabaw', url: '/static/spacer/plac.jpg',
             sasiedzi: [{ scena: 'parking', yaw: 95 }],
             strzalki: [{ pitch: -4, yaw: 95, sceneId: 'parking', text: 'Parking', targetYaw: 118 }] }
};
var PIERWSZA = 'parking';
var viewer = null;

// ===== 1. Ładowanie całości z paskiem postępu =====
function wczytajWszystko() {
  var klucze = Object.keys(SCENY);
  var pobrane = {}, razem = 0, odebrane = 0, rozmiary = {};

  function pokaz() {
    var pr = razem > 0 ? Math.min(99, Math.round(odebrane / razem * 100)) : 0;
    document.getElementById('pasek-w').style.width = pr + '%';
    document.getElementById('procent').textContent = pr + '%';
  }

  // najpierw rozmiary (HEAD), żeby pasek liczył bajty całości
  return Promise.all(klucze.map(function (k) {
    return fetch(SCENY[k].url, { method: 'HEAD' }).then(function (r) {
      rozmiary[k] = parseInt(r.headers.get('Content-Length') || '0', 10);
    }).catch(function () { rozmiary[k] = 0; });
  })).then(function () {
    razem = klucze.reduce(function (s, k) { return s + rozmiary[k]; }, 0);
    return Promise.all(klucze.map(function (k) {
      return fetch(SCENY[k].url).then(function (r) {
        var reader = r.body.getReader(), czesci = [];
        function czytaj() {
          return reader.read().then(function (x) {
            if (x.done) return;
            czesci.push(x.value); odebrane += x.value.length; pokaz();
            return czytaj();
          });
        }
        return czytaj().then(function () {
          pobrane[k] = URL.createObjectURL(new Blob(czesci, { type: 'image/jpeg' }));
        });
      });
    }));
  }).then(function () {
    document.getElementById('pasek-w').style.width = '100%';
    document.getElementById('procent').textContent = '100%';
    return pobrane;
  });
}

// ===== 2. Start spaceru po załadowaniu =====
function start(pobrane) {
  var sceny = {};
  Object.keys(SCENY).forEach(function (k) {
    sceny[k] = {
      title: SCENY[k].tytul, type: 'equirectangular', panorama: pobrane[k],
      hotSpots: SCENY[k].strzalki.map(function (s) {
        return { pitch: s.pitch, yaw: s.yaw, type: 'scene', cssClass: 'strzalka',
                 text: s.text, sceneId: s.sceneId, targetYaw: s.targetYaw, targetPitch: 0 };
      })
    };
  });
  viewer = pannellum.viewer('panorama', {
    default: { firstScene: PIERWSZA, autoLoad: true, sceneFadeDuration: 700, hfov: 100, ignoreGPanoXMP: true },
    scenes: sceny
  });
  window.viewer = viewer;
  var l = document.getElementById('ladowanie');
  l.style.opacity = '0';
  setTimeout(function () { l.remove(); }, 600);
  nawigacja();
}

// ===== 3. Podwójny klik / podwójne tapnięcie — wszędzie =====
var ostatniSkok = 0;
function idz(px, py) {
  var teraz = Date.now();
  if (teraz - ostatniSkok < 800 || !viewer) return; // ochrona przed podwójnym odpaleniem
  var c = viewer.mouseEventToCoords({ clientX: px, clientY: py });
  var yaw = c[1], lista = SCENY[viewer.getScene()].sasiedzi, naj = null, najd = 181;
  lista.forEach(function (s) {
    var d = Math.abs((((yaw - s.yaw) % 360) + 540) % 360 - 180);
    if (d < najd) { najd = d; naj = s; }
  });
  if (naj && najd <= 90) { ostatniSkok = teraz; viewer.loadScene(naj.scena); }
}
function nawigacja() {
  var el = document.getElementById('panorama');
  var lt = 0, lx = 0, ly = 0, sx = 0, sy = 0, ruch = false;
  el.addEventListener('pointerdown', function (e) { sx = e.clientX; sy = e.clientY; ruch = false; }, true);
  el.addEventListener('pointermove', function (e) {
    if (Math.abs(e.clientX - sx) > 12 || Math.abs(e.clientY - sy) > 12) ruch = true;
  }, true);
  el.addEventListener('pointerup', function (e) {
    if (ruch) { lt = 0; return; } // to było przeciąganie, nie tapnięcie
    var t = Date.now();
    if (t - lt < 500 && Math.abs(e.clientX - lx) < 60 && Math.abs(e.clientY - ly) < 60) {
      lt = 0; idz(e.clientX, e.clientY);
    } else { lt = t; lx = e.clientX; ly = e.clientY; }
  }, true);
  el.addEventListener('dblclick', function (e) { idz(e.clientX, e.clientY); }, true);
}

wczytajWszystko().then(start).catch(function (e) {
  document.getElementById('procent').textContent = 'Błąd ładowania: ' + e;
});
