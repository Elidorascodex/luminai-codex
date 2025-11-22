Post-Training Quantization (PTQ) experiment scaffold

This folder contains a minimal smoke-test scaffold to help you run a quick
PTQ experiment locally. It's intentionally conservative: it won't overwrite
models or attempt heavy downloads. Use it as a starting point for
PTQ/QAT exploration.

Files:
- `requirements-ptq.txt` - Python packages useful for PTQ experiments.
- `ptq_experiment.py` - Lightweight script that checks environment, optionally
  loads a model, and runs a simple PTQ conversion flow if the required
  dependencies are installed.

How to use:
1. Create and activate a Python virtualenv: python -m venv .venv && .\.venv\Scripts\Activate.ps1
2. pip install -r tools/quant/requirements-ptq.txt
3. Run: python tools/quant/ptq_experiment.py --help

Notes:
- This is a scaffold. Replace the model I/O and quantizer with the toolchain
  you prefer (transformers + bitsandbytes, or a TPU/XLA toolchain, etc.).
