#!/bin/bash
set -e
python3 -m venv /opt/xtts
/opt/xtts/bin/pip install -q --upgrade pip
/opt/xtts/bin/pip install --index-url https://download.pytorch.org/whl/cpu torch==2.11.0 torchaudio==2.11.0 || /opt/xtts/bin/pip install --index-url https://download.pytorch.org/whl/cpu torch torchaudio
/opt/xtts/bin/pip install coqui-tts
/opt/xtts/bin/python -c "import torch, torchaudio; print('PARA OK:', torch.__version__, torchaudio.__version__)"
