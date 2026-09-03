import {VideoRTC} from '/video-rtc.js?v=1fd3b652';

const cameras = {
  parking_wjazd: 'Wjazd na parking',
  parking_wejscie: 'Wejście na parking',
  parking_smietnik: 'Altana śmietnikowa',
};

const host = document.querySelector('#player-host');
const shell = document.querySelector('#video-shell');
const cameraTitle = document.querySelector('#camera-title');
const liveStatus = document.querySelector('#live-status');
const liveLabel = document.querySelector('#live-label');
const lastFrameText = document.querySelector('#last-frame');
const signalMessage = document.querySelector('#signal-message');
const fullscreenButton = document.querySelector('#fullscreen-button');
const privacyDialog = document.querySelector('#privacy-dialog');

let activePlayer = null;
let activeCamera = null;
let lastFrameAt = 0;
let healthTimer = 0;

if (!customElements.get('video-rtc')) {
  customElements.define('video-rtc', VideoRTC);
}

function setStatus(state, label) {
  liveStatus.dataset.state = state;
  liveLabel.textContent = label;
}

function formatTime(timestamp) {
  return new Intl.DateTimeFormat('pl-PL', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  }).format(timestamp);
}

function markFrame() {
  lastFrameAt = Date.now();
  setStatus('live', 'Na żywo');
  signalMessage.hidden = true;
  lastFrameText.textContent = `Ostatni obraz: ${formatTime(lastFrameAt)}`;
}

function observeVideoFrames(player) {
  const attach = () => {
    if (player !== activePlayer) return;
    const video = player.querySelector('video');
    if (!video) {
      requestAnimationFrame(attach);
      return;
    }

    video.muted = true;
    video.setAttribute('aria-label', cameras[activeCamera]);

    if ('requestVideoFrameCallback' in video) {
      const onFrame = () => {
        if (player !== activePlayer) return;
        markFrame();
        video.requestVideoFrameCallback(onFrame);
      };
      video.requestVideoFrameCallback(onFrame);
    } else {
      video.addEventListener('timeupdate', markFrame);
      video.addEventListener('loadeddata', markFrame);
    }
  };

  requestAnimationFrame(attach);
}

function startHealthCheck() {
  clearInterval(healthTimer);
  healthTimer = window.setInterval(() => {
    if (!lastFrameAt) return;
    if (Date.now() - lastFrameAt > 25_000) {
      setStatus('offline', 'Brak sygnału');
      signalMessage.hidden = false;
    }
  }, 1_000);
}

function selectCamera(name) {
  if (!Object.hasOwn(cameras, name) || name === activeCamera) return;

  if (activePlayer) {
    activePlayer.ondisconnect();
    activePlayer.remove();
  }

  activeCamera = name;
  lastFrameAt = 0;
  cameraTitle.textContent = cameras[name];
  lastFrameText.textContent = 'Ostatni obraz: czekam na sygnał';
  signalMessage.hidden = true;
  setStatus('loading', 'Łączenie');

  document.querySelectorAll('[data-camera]').forEach((button) => {
    const isActive = button.dataset.camera === name;
    button.classList.toggle('is-active', isActive);
    button.setAttribute('aria-pressed', String(isActive));
  });

  const player = document.createElement('video-rtc');
  player.mode = 'mse';
  player.media = 'video';
  player.visibilityCheck = false;      // nie zrywaj przy chwilowym ukryciu
  player.background = true;            // trzymaj polaczenie w tle
  player.pliveThreshold = 10;         // duzy bufor, plynnie mimo porcji co ~4 s z chmury
  player.src = `/api/ws?src=${encodeURIComponent(name)}`;
  activePlayer = player;
  host.replaceChildren(player);
  // bufor + lagodne doganianie: gdy narosnie zaleglosc, przyspiesz odtwarzanie zamiast skakac/restartowac
  player.addEventListener('loadeddata', () => {
    const v = player.querySelector('video'); if (!v) return;
    v.playsInline = true; v.playbackRate = 1.0;
    // predkosc i bufor obsluguje wlasny video-rtc.js (spokojny)
  });
  observeVideoFrames(player);
  startHealthCheck();
}

document.querySelectorAll('[data-camera]').forEach((button) => {
  button.addEventListener('click', () => selectCamera(button.dataset.camera));
});

fullscreenButton.addEventListener('click', async () => {
  if (document.fullscreenElement) {
    await document.exitFullscreen();
    return;
  }
  if (shell.requestFullscreen) await shell.requestFullscreen();
  else if (shell.webkitRequestFullscreen) shell.webkitRequestFullscreen();
});

for (const id of ['privacy-button', 'privacy-footer-button']) {
  document.querySelector(`#${id}`).addEventListener('click', () => privacyDialog.showModal());
}

document.querySelector('#privacy-close').addEventListener('click', () => privacyDialog.close());
privacyDialog.addEventListener('click', (event) => {
  if (event.target === privacyDialog) privacyDialog.close();
});

selectCamera('parking_wjazd');


// Kto oglada teraz (widzowie.json odswiezany na serwerze co 5 s)
const widzowieText = document.querySelector('#widzowie');
async function odswiezWidzow() {
  try {
    const r = await fetch('/widzowie.json', { cache: 'no-store' });
    if (!r.ok) return;
    const d = await r.json();
    if (!d.kamery) return;
    const czesci = d.kamery.filter(k => k.widzow > 0).map(k => `${k.kamera}: ${k.widzow}${k.kto && k.kto.length ? ' (' + k.kto.join(', ') + ')' : ''}`);
    widzowieText.textContent = 'Oglądają teraz: ' + (d.razem ? `${d.razem} — ${czesci.join(' · ')}` : 'nikt') + ` · ${d.ts}`;
  } catch (e) { /* cicho */ }
}
odswiezWidzow();
window.setInterval(odswiezWidzow, 5000);
