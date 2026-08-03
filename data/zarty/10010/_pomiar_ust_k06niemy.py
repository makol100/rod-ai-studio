
#!/app/venv/bin/python
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import cv2
import numpy as np
from insightface.app import FaceAnalysis


PYTHON = Path("/app/venv/bin/python")
FFMPEG = Path("/usr/bin/ffmpeg")
VIDEO = Path(
    "/root/rod-ai-studio/data/zarty/10010/klip_k06_niemy.mp4"
)

SAMPLE_FPS = 2.0
DET_SIZE = (640, 640)

# Progi startowe do bramki konserwatywnej:
# - CLOSED_LEVEL: ponad 2,2% wysokości twarzy uznajemy za zauważalne otwarcie;
# - MOTION_RANGE: zmiana o co najmniej 0,8% wysokości twarzy oznacza pracę ust;
# - OPEN_FRACTION: co najmniej 25% próbek zauważalnie otwartych.
# Należy je skalibrować na kilku poprawnych i błędnych klipach z tej serii.
CLOSED_LEVEL = 0.022
MOTION_RANGE = 0.008
OPEN_FRACTION = 0.25
MAX_MISSING_FRACTION = 0.25

# Kontur ust w schemacie InsightFace 106.
# Trzy pary biegną przez centralną część górnej i dolnej wargi.
LIP_PAIRS = ((54, 70), (55, 69), (56, 68))


def fail(message: str) -> None:
    print(f"BŁĄD: {message}", file=sys.stderr)
    raise SystemExit(2)


def find_model_root() -> Path:
    """Znajdź już zainstalowany buffalo_l bez pobierania i zapisu poza /tmp."""
    roots = (
        Path("/root/.insightface"),
        Path("/app/.insightface"),
        Path("/app/models/insightface"),
    )
    for root in roots:
        model_dir = root / "models" / "buffalo_l"
        if (
            model_dir.is_dir()
            and (model_dir / "det_10g.onnx").is_file()
            and (model_dir / "2d106det.onnx").is_file()
        ):
            return root

    fail(
        "nie znaleziono lokalnego buffalo_l z det_10g.onnx i "
        "2d106det.onnx w oczekiwanych katalogach; skrypt celowo "
        "nie pobiera modelu poza /tmp"
    )


def extract_frames(output_dir: Path) -> list[Path]:
    pattern = output_dir / "frame_%05d.png"
    command = [
        str(FFMPEG),
        "-hide_banner",
        "-loglevel", "error",
        "-nostdin",
        "-y",
        "-i", str(VIDEO),
        "-vf", f"fps={SAMPLE_FPS:g}",
        "-vsync", "0",
        str(pattern),
    ]
    subprocess.run(command, check=True)
    return sorted(output_dir.glob("frame_*.png"))


def choose_visible_face(faces):
    """W tym klipie widoczna postać to największa wykryta twarz."""
    return max(
        faces,
        key=lambda face: float(
            max(0.0, face.bbox[2] - face.bbox[0])
            * max(0.0, face.bbox[3] - face.bbox[1])
        ),
    )


def normalized_mouth_opening(face) -> float:
    landmarks = getattr(face, "landmark_2d_106", None)
    if landmarks is None or np.asarray(landmarks).shape != (106, 2):
        raise RuntimeError("model nie zwrócił landmark_2d_106 o kształcie 106x2")

    points = np.asarray(landmarks, dtype=np.float32)
    face_height = float(face.bbox[3] - face.bbox[1])
    if face_height <= 0:
        raise RuntimeError("niepoprawna wysokość bbox twarzy")

    distances = [
        float(np.linalg.norm(points[upper] - points[lower]))
        for upper, lower in LIP_PAIRS
    ]
    return float(np.median(distances) / face_height)


def main() -> None:
    if Path(sys.executable).resolve() != PYTHON.resolve():
        print(
            f"UWAGA: zalecany interpreter to {PYTHON}; "
            f"obecnie: {sys.executable}",
            file=sys.stderr,
        )
    if not FFMPEG.is_file():
        fail(f"brak ffmpeg: {FFMPEG}")
    if not VIDEO.is_file():
        fail(f"brak klipu: {VIDEO}")

    model_root = find_model_root()
    app = FaceAnalysis(
        name="buffalo_l",
        root=str(model_root),
        allowed_modules=["detection", "landmark_2d_106"],
        providers=["CPUExecutionProvider"],
    )
    app.prepare(ctx_id=-1, det_size=DET_SIZE, det_thresh=0.35)

    tmp_dir = Path(tempfile.mkdtemp(prefix="k06_mouth_", dir="/tmp"))
    measurements: list[float] = []
    rows: list[tuple[float, float | None]] = []

    try:
        frames = extract_frames(tmp_dir)
        if not frames:
            fail("ffmpeg nie wyodrębnił żadnych klatek")

        for index, frame_path in enumerate(frames):
            timestamp = index / SAMPLE_FPS
            frame = cv2.imread(str(frame_path), cv2.IMREAD_COLOR)
            if frame is None:
                rows.append((timestamp, None))
                continue

            faces = app.get(frame)
            if not faces:
                rows.append((timestamp, None))
                continue

            face = choose_visible_face(faces)
            opening = normalized_mouth_opening(face)
            measurements.append(opening)
            rows.append((timestamp, opening))

        print("czas_s | rozwarcie_norm")
        print("-------+----------------")
        for timestamp, opening in rows:
            value = "BRAK_TWARZY" if opening is None else f"{opening:.5f}"
            print(f"{timestamp:6.2f} | {value}")

        missing_fraction = 1.0 - len(measurements) / len(rows)
        if missing_fraction > MAX_MISSING_FRACTION:
            print(
                f"\nWERDYKT: NIEWIARYGODNY POMIAR "
                f"(brak twarzy w {missing_fraction:.1%} próbek)"
            )
            raise SystemExit(3)

        if len(measurements) < 3:
            fail("za mało poprawnych pomiarów do werdyktu")

        values = np.asarray(measurements, dtype=np.float32)
        q10, median, q90 = np.percentile(values, [10, 50, 90])
        motion = float(q90 - q10)
        open_fraction = float(np.mean(values > CLOSED_LEVEL))

        # Ruch artykulacyjny albo częste wyraźne otwarcie uruchamia bramkę.
        mouth_working = (
            motion >= MOTION_RANGE
            or open_fraction >= OPEN_FRACTION
        )

        print()
        print(
            f"statystyki: mediana={median:.5f}, "
            f"q10={q10:.5f}, q90={q90:.5f}, "
            f"zakres_q90-q10={motion:.5f}, "
            f"udział_otwartych={open_fraction:.1%}"
        )
        print(
            "WERDYKT: "
            + ("USTA PRACUJĄ (mówi)" if mouth_working else "USTA ZAMKNIĘTE")
        )

        raise SystemExit(1 if mouth_working else 0)

    finally:
        # Wszystkie klatki tymczasowe powstały wyłącznie w /tmp.
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
