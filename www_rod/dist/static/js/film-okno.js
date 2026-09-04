(function(){
if(window.__filmOkno)return; window.__filmOkno=1;
function zamknij(ok){var v=ok.querySelector('video'); if(v){v.pause(); v.removeAttribute('src'); v.load();} ok.remove(); document.body.style.overflow='';}
function otworz(src,poster){
  var ok=document.createElement('div');
  var s=ok.style; s.position='fixed'; s.inset='0'; s.background='rgba(10,14,10,.94)'; s.zIndex='9999';
  s.display='flex'; s.alignItems='center'; s.justifyContent='center';
  var v=document.createElement('video');
  v.controls=true; v.setAttribute('playsinline',''); v.preload='metadata';
  if(poster)v.poster=poster; v.src=src;
  var vs=v.style; vs.maxHeight='92vh'; vs.maxWidth='96vw'; vs.borderRadius='10px'; vs.background='#000';
  var x=document.createElement('button');
  x.textContent='\u2715'; x.setAttribute('aria-label','Zamknij');
  var xs=x.style; xs.position='fixed'; xs.top='12px'; xs.right='12px'; xs.width='48px'; xs.height='48px';
  xs.fontSize='24px'; xs.lineHeight='48px'; xs.border='2px solid rgba(255,255,255,.7)'; xs.borderRadius='50%';
  xs.background='rgba(0,0,0,.45)'; xs.color='#fff'; xs.cursor='pointer'; xs.padding='0';
  x.addEventListener('click',function(){zamknij(ok);});
  ok.addEventListener('click',function(e){if(e.target===ok)zamknij(ok);});
  document.addEventListener('keydown',function esc(e){if(e.key==='Escape'){zamknij(ok);document.removeEventListener('keydown',esc);}});
  ok.appendChild(v); ok.appendChild(x); document.body.appendChild(ok);
  document.body.style.overflow='hidden';
  var p=v.play(); if(p&&p.catch)p.catch(function(){});
}
document.addEventListener('click',function(e){
  var a=e.target.closest?e.target.closest('a.wideo-karta[data-wideo]'):null;
  if(!a)return; e.preventDefault();
  otworz(a.getAttribute('data-wideo'),a.getAttribute('data-mini')||'');
});
})();