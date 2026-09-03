const q = new URLSearchParams(location.search);
    if (q.get('blad')) { document.getElementById('blad').style.display = 'block'; }
    if (q.get('login')) { document.getElementById('login').value = q.get('login'); }
