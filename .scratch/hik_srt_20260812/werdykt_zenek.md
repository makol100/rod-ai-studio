POTWIERDZONE

1. Dokument Hik-Connect „Share a Single Device” mówi: „if you select Live View and Remote Playback, the recipient will have the permissions to view live video and play back the video footage”. Zatem shared user może mieć Live View, ale tylko gdy właściciel nadał to uprawnienie.

2. session.go opisuje kolejność: „P2P_SETUP ...”, „PLAY_REQUEST ...”, następnie „wait for the SRT data session”. Timeout pada, gdy getDataSessionID() pozostaje 0. DataSessionID jest ustawiane w handleConnectionControl po odebraniu pakietu SRT z initSeq albo conclusion. contactP2PServers po 10 sekundach bez punchCh robi fallback holePunch i mimo tego zwraca nil. Błąd nie dowodzi więc udanego hole-punch; dowodzi tylko, że nie odebrano kontroli SRT ustanawiającej data session.

3. client.go parsuje tylko account, password, serial, channel, subtype, start i end. verification code nie ma parametru URL. PROTOCOL.md mówi: „This path assumes unencrypted media and does not carry that schedule.” Kod nie obsługuje szyfrowanego verification-code media.

4. PROTOCOL.md mówi: „The media path is always direct, hole-punched P2P” oraz „There is no TCP media-relay fallback in this implementation.” Relayed jest tylko PLAY_REQUEST control; media relay/TURN/VTM nie istnieje.

HIPOTEZY

Najpierw sprawdzić Live View w oficjalnej aplikacji na koncie Tomasza i jedną próbę poświadczeniami właściciela. Trzy identyczne awarie shared wskazują na wariant shared/permission bardziej niż zły kanał, ale kod bez logowania etapów tego nie rozstrzyga. Równolegle tcpdump rozstrzygnie, czy wraca 0x0C00/SRT.

NIE WIEM

Nie wiem bez capture, czy dochodzi 0x0B03, 0x0C00 albo PLAY_REQUEST jest odrzucany. Nie wiem, czy właściciel nadał Tomaszowi Live View i czy stream encryption jest włączone.

Zenek
