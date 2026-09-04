(function(){
if(window.__filmOkno)return; window.__filmOkno=1;
function pelny(el){var s=el.style; s.position='fixed'; s.top='0'; s.right='0'; s.bottom='0'; s.left='0';}
function zamknij(ok){var v=ok.querySelector('video'); if(v){v.pause(); v.removeAttribute('src'); v.load();}
  var f=ok.querySelector('iframe'); if(f){f.src='about:blank'; f.remove();}
  ok.remove(); document.body.style.overflow='';}
function ramka(){
  var ok=document.createElement('div'); pelny(ok);
  var s=ok.style; s.background='rgba(10,14,10,.94)'; s.zIndex='9999';
  s.display='flex'; s.alignItems='center'; s.justifyContent='center';
  var x=document.createElement('button'); x.textContent='\u2715'; x.setAttribute('aria-label','Zamknij');
  var xs=x.style; xs.position='fixed'; xs.top='12px'; xs.right='12px'; xs.width='48px'; xs.height='48px';
  xs.fontSize='24px'; xs.lineHeight='48px'; xs.border='2px solid rgba(255,255,255,.7)'; xs.borderRadius='50%';
  xs.background='rgba(0,0,0,.45)'; xs.color='#fff'; xs.cursor='pointer'; xs.padding='0'; xs.zIndex='10000';
  x.addEventListener('click',function(){zamknij(ok);});
  ok.addEventListener('click',function(e){if(e.target===ok)zamknij(ok);});
  document.addEventListener('keydown',function esc(e){if(e.key==='Escape'){zamknij(ok);document.removeEventListener('keydown',esc);}});
  ok.appendChild(x); return ok;
}
function otworzMp4(src,poster){
  var ok=ramka(); var v=document.createElement('video');
  v.controls=true; v.setAttribute('playsinline',''); v.preload='metadata';
  if(poster)v.poster=poster; v.src=src;
  var vs=v.style; vs.maxHeight='92vh'; vs.maxWidth='96vw'; vs.borderRadius='10px'; vs.background='#000';
  ok.insertBefore(v,ok.firstChild); document.body.appendChild(ok); document.body.style.overflow='hidden';
  var p=v.play(); if(p&&p.catch)p.catch(function(){});
}
function otworzYt(id,pion){
  var ok=ramka(); var f=document.createElement('iframe');
  f.src='https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0&modestbranding=1&playsinline=1';
  f.setAttribute('allow','accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture');
  f.setAttribute('allowfullscreen',''); f.setAttribute('title','Film');
  var W=window.innerWidth, H=window.innerHeight, w, h;
  if(pion){h=Math.floor(H*0.92); w=Math.floor(h*9/16); if(w>W*0.96){w=Math.floor(W*0.96); h=Math.floor(w*16/9);}}
  else{w=Math.floor(W*0.96); h=Math.floor(w*9/16); if(h>H*0.92){h=Math.floor(H*0.92); w=Math.floor(h*16/9);}}
  var fs=f.style; fs.width=w+'px'; fs.height=h+'px'; fs.border='0'; fs.borderRadius='10px'; fs.background='#000';
  ok.insertBefore(f,ok.firstChild); document.body.appendChild(ok); document.body.style.overflow='hidden';
}
document.addEventListener('click',function(e){
  var t=e.target; while(t&&t!==document&&!(t.getAttribute&&(t.getAttribute('data-wideo')||t.getAttribute('data-yt'))))t=t.parentNode;
  if(!t||t===document)return; e.preventDefault();
  var yt=t.getAttribute('data-yt');
  if(yt)otworzYt(yt,t.getAttribute('data-pion')==='1');
  else otworzMp4(t.getAttribute('data-wideo'),t.getAttribute('data-mini')||'');
});
})();