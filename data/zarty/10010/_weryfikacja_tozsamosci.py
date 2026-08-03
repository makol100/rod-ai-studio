
#!/app/venv/bin/python
import os
import shutil
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from insightface.app import FaceAnalysis

PYTHON = "/app/venv/bin/python"
FFMPEG = "/usr/bin/ffmpeg"
ROOT = Path("/root/rod-ai-studio")
EPISODE = ROOT / "data/zarty/10010"
FRAMES_ROOT = Path("/tmp/10010_identity_check")
LIBRARY_REFERENCE = ROOT / "assets/zarty/karty/bohater_noc.jpg"

CLIPS = {
    "k04": EPISODE / "klip_k06_niemy.mp4",
    "k06": EPISODE / "klip_k06_niemy.mp4",
}

ACCEPTED_FRAMES = {
    "k04": EPISODE / "kadry/k04.jpg",
    "k06": EPISODE / "kadry/k06.jpg",
}

# Próg pomocniczy zgodny z używaną bramką.
# Decyzję opieramy przede wszystkim na podobieństwie do zaakceptowanego kadru.
FRAME_THRESHOLD = 0.35


def require_file(path: Path) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"Brak pliku: {path}")


def extract_frames(video: Path, output_dir: Path) -> list[Path]:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    pattern = output_dir / "kl_%03d.jpg"
    command = [
        FFMPEG,
        "-hide_banner",
        "-loglevel", "error",
        "-y",
        "-i", str(video),
        "-vf", "fps=1",
        "-q:v", "2",
        str(pattern),
    ]
    subprocess.run(command, check=True)

    frames = sorted(output_dir.glob("kl_*.jpg"))
    if not frames:
        raise RuntimeError(f"FFmpeg nie wyciągnął klatek z {video}")
    return frames


def largest_face(app: FaceAnalysis, image_path: Path):
    image = cv2.imread(str(image_path))
    if image is None:
        raise RuntimeError(f"Nie można odczytać obrazu: {image_path}")

    faces = app.get(image)
    if not faces:
        return None

    return max(
        faces,
        key=lambda face: (
            float(face.bbox[2] - face.bbox[0])
            * float(face.bbox[3] - face.bbox[1])
        ),
    )


def normalized_embedding(face, image_path: Path) -> np.ndarray:
    if face is None:
        raise RuntimeError(f"Nie wykryto twarzy w referencji: {image_path}")

    embedding = np.asarray(face.embedding, dtype=np.float32)
    norm = float(np.linalg.norm(embedding))
    if norm == 0:
        raise RuntimeError(f"Zerowy embedding twarzy: {image_path}")
    return embedding / norm


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))


def verdict(similarities: list[float | None]) -> tuple[str, str]:
    detected = [value for value in similarities if value is not None]
    if not detected:
        return "NIE ROZSTRZYGNIĘTO", "w żadnej klatce nie wykryto twarzy"

    passed = sum(value >= FRAME_THRESHOLD for value in detected)
    ratio = passed / len(detected)
    median = float(np.median(detected))
    minimum = min(detected)

    # Pojedyncza trudna klatka nie przesądza o zmianie osoby.
    # Wymagamy, aby większość wykrytych twarzy trzymała zaakceptowany kadr.
    if ratio >= 0.60 and median >= FRAME_THRESHOLD:
        reason = (
            f"{passed}/{len(detected)} wykrytych twarzy ma sim >= "
            f"{FRAME_THRESHOLD:.2f}; mediana={median:.2f}, min={minimum:.2f}"
        )
        return "WIERNY KADROWI", reason

    reason = (
        f"tylko {passed}/{len(detected)} wykrytych twarzy ma sim >= "
        f"{FRAME_THRESHOLD:.2f}; mediana={median:.2f}, min={minimum:.2f}"
    )
    return "OBCA TWARZ / SILNY DRYF W KLIPIE", reason


def main() -> int:
    if Path(sys.executable).resolve() != Path(PYTHON).resolve():
        print(
            f"UWAGA: zalecany interpreter to {PYTHON}; "
            f"uruchomiono {sys.executable}",
            file=sys.stderr,
        )

    require_file(Path(FFMPEG))
    require_file(LIBRARY_REFERENCE)
    for path in list(CLIPS.values()) + list(ACCEPTED_FRAMES.values()):
        require_file(path)

    # Buffalo_l może użyć GPU, jeżeli provider CUDA jest dostępny;
    # CPU pozostaje bezpiecznym fallbackiem.
    app = FaceAnalysis(
        name="buffalo_l",
        providers=["CUDAExecutionProvider", "CPUExecutionProvider"],
    )
    app.prepare(ctx_id=0, det_size=(640, 640))

    library_embedding = normalized_embedding(
        largest_face(app, LIBRARY_REFERENCE),
        LIBRARY_REFERENCE,
    )

    for shot in ("k04", "k06"):
        accepted_path = ACCEPTED_FRAMES[shot]
        accepted_embedding = normalized_embedding(
            largest_face(app, accepted_path),
            accepted_path,
        )

        accepted_vs_library = cosine(
            accepted_embedding,
            library_embedding,
        )

        frames = extract_frames(
            CLIPS[shot],
            FRAMES_ROOT / shot,
        )

        print()
        print("=" * 82)
        print(f"{shot}: {CLIPS[shot]}")
        print(f"Zaakceptowany kadr: {accepted_path}")
        print(f"Biblioteka:          {LIBRARY_REFERENCE}")
        print(
            "Kadr vs biblioteka:  "
            f"{accepted_vs_library:.3f}"
        )
        print("-" * 82)
        print(
            f"{'czas':>6}  {'plik':<14}  "
            f"{'vs kadr':>9}  {'vs biblioteka':>15}  status"
        )
        print("-" * 82)

        sims_to_frame: list[float | None] = []

        for second, frame_path in enumerate(frames):
            face = largest_face(app, frame_path)

            if face is None:
                sims_to_frame.append(None)
                print(
                    f"{second:5d}s  {frame_path.name:<14}  "
                    f"{'BRAK':>9}  {'BRAK':>15}  brak wykrytej twarzy"
                )
                continue

            embedding = normalized_embedding(face, frame_path)
            sim_frame = cosine(embedding, accepted_embedding)
            sim_library = cosine(embedding, library_embedding)
            sims_to_frame.append(sim_frame)

            status = (
                "zgodna z kadrem"
                if sim_frame >= FRAME_THRESHOLD
                else "poniżej progu kadru"
            )
            print(
                f"{second:5d}s  {frame_path.name:<14}  "
                f"{sim_frame:9.3f}  {sim_library:15.3f}  {status}"
            )

        label, reason = verdict(sims_to_frame)
        print("-" * 82)
        print(f"WERDYKT {shot}: {label}")
        print(f"UZASADNIENIE: {reason}")

    print()
    print(f"Klatki tymczasowe zapisano wyłącznie w: {FRAMES_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
