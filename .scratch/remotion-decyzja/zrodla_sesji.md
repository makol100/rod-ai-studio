# Ślady z sesji

## Stan VPS — wynik poleceń

node v22.23.1
npm 10.9.8
12 CPU
Mem total 22Gi, used 8.6Gi, free 1.5Gi, available 14Gi
Swap 0B
Chromium, chromium-browser i google-chrome: command not found.

## Oficjalna dokumentacja Remotion odczytana przez web

Remotion fundamentals: React component receives the current frame and renders content to a canvas.
Animation is driven by useCurrentFrame(); helpers include interpolate() and spring().

renderMedia(): default concurrency is half of the available CPU threads. A browser executable is
automatically detected and downloaded if unavailable. Default chrome mode is headless-shell.
The renderer uses FFmpeg. disallowParallelEncoding makes rendering more memory-efficient but slower.
mediaCacheSizeInBytes defaults to half available system memory; the OffthreadVideo cache likewise
defaults to half the available system memory.

Pricing page: free license for individuals and companies up to 3 people. For collaborations and
companies of 4+ people, Automators pricing is $0.01 per render with $100/month minimum; Creators is
$25/month per seat.

Terminology used in the report: H.264, TypeScript, GiB, RAM-u.

## Filtry dostępne w lokalnym ffmpeg — wynik `ffmpeg -filters`

ass, drawtext, geq, overlay, xfade, zoompan, showspectrum, showwaves.
