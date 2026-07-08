

## ZAMKNIETE (08.07.2026, 13:30) — odtwarzanie rolek w panelu
Przycisk odtwarzania (trojkat) w naglowku KAZDEJ karty rolki ze statusem "gotowa" (obok kosza). Klik -> karta sie rozwija (jesli nie byla) + wstrzykuje <video controls autoplay playsinline src="/reels/{id}/video"> w gornej czesci rbody. Powtorny klik usuwa element wideo (zatrzymuje odtwarzanie, bo element znika z DOM, nie tylko sie chowa).

Zweryfikowane: GET /reels/{id}/video zwraca video/mp4 (200), Range requests dzialaja (206 - przewijanie w video dziala plynnie), endpoint uzywa istniejacej logiki wyszukiwania folderu (ta sama co w innych miejscach: sprawdza final_napisy_muzyka.mp4 / final_with_music.mp4 / final.mp4 w tej kolejnosci).
