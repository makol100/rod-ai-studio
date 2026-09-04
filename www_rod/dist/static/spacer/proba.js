// Spacer 360 — nawigacja stylu Street View: podwójne kliknięcie/tapnięcie w kierunku ruchu (D-0308)
var sasiedzi = {
  parking: [{ scena: 'plac', yaw: 118 }],
  plac:    [{ scena: 'parking', yaw: 95 }]
};

var viewer = pannellum.viewer('panorama', {
  default: { firstScene: 'parking', autoLoad: true, sceneFadeDuration: 700, hfov: 100 },
  scenes: {
    parking: { title: 'Parking', type: 'equirectangular', panorama: '/static/spacer/parking.jpg' },
    plac:    { title: 'Plac zabaw', type: 'equirectangular', panorama: '/static/spacer/plac.jpg' }
  }
});

// podgrzewanie sąsiadów — jak w Google: dogrywamy w tle następne sfery
function podgrzej() {
  (sasiedzi[viewer.getScene()] || []).forEach(function (s) {
    var i = new Image(); i.src = '/static/spacer/' + s.scena + '.jpg';
  });
}
viewer.on('load', podgrzej);

function idz(px, py) {
  var c = viewer.mouseEventToCoords({ clientX: px, clientY: py });
  var yaw = c[1];
  var lista = sasiedzi[viewer.getScene()] || [];
  var naj = null, najd = 181;
  lista.forEach(function (s) {
    var d = Math.abs((((yaw - s.yaw) % 360) + 540) % 360 - 180);
    if (d < najd) { najd = d; naj = s; }
  });
  if (naj && najd <= 90) viewer.loadScene(naj.scena);
}

var pan = document.getElementById('panorama');
pan.addEventListener('dblclick', function (e) { idz(e.clientX, e.clientY); });

// własne wykrywanie podwójnego tapnięcia (telefony nie zawsze dają dblclick)
var ostT = 0, ostX = 0, ostY = 0;
pan.addEventListener('touchend', function (e) {
  if (e.changedTouches.length !== 1) return;
  var t = Date.now(), x = e.changedTouches[0].clientX, y = e.changedTouches[0].clientY;
  if (t - ostT < 350 && Math.abs(x - ostX) < 40 && Math.abs(y - ostY) < 40) {
    idz(x, y); ostT = 0;
  } else { ostT = t; ostX = x; ostY = y; }
});
