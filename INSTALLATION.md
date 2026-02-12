# Installation & Setup Guide

Detailed setup instructions for the Children's Intelligence Test Application.

## System Requirements

| Requirement | Minimum           | Recommended   |
| ----------- | ----------------- | ------------- |
| Python      | 3.8               | 3.10+         |
| RAM         | 4GB               | 8GB+          |
| Storage     | 10GB              | 20GB+         |
| GPU         | None              | NVIDIA (6GB+) |
| OS          | Windows/Linux/Mac | Linux Server  |

## Installation Methods

## Method 1: Standard Installation (Recommended)

### 1.1 Clone Repository

```bash
cd d:\company
```

### 1.2 Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 1.3 Install Dependencies

```bash
# From requirements.txt
pip install -r requirements.txt

# Or individual packages
pip install transformers torch deep-translator streamlit
```

### 1.4 Verify Installation

```bash
python -c "import torch; print('PyTorch:', torch.__version__)"
python -c "import transformers; print('Transformers:', transformers.__version__)"
python -c "import streamlit; print('Streamlit:', streamlit.__version__)"
```

## Method 2: GPU Installation (NVIDIA)

### 2.1 Prerequisites

- NVIDIA GPU (RTX series recommended)
- NVIDIA Driver 520+ installed
- CUDA Toolkit 11.8+
- cuDNN 8.6+

### 2.2 Install CUDA-enabled PyTorch

```bash
# Check your CUDA version
nvidia-smi

# Install compatible PyTorch (replace 11.8 with your CUDA version)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verify GPU availability
python -c "import torch; print('GPU Available:', torch.cuda.is_available())"
```

### 2.3 Install Remaining Dependencies

```bash
pip install -r requirements.txt
```

## Method 3: Docker Installation

### 3.1 Build Docker Image

```bash
docker build -t children-quiz-app .
```

### 3.2 Run Container

```bash
docker run -it -p 8501:8501 children-quiz-app
```

### Dockerfile Example

```dockerfile
FROM pytorch/pytorch:2.1.1-cuda12.1-runtime-ubuntu22.04

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "deploy.py", "--server.port=8501"]
```

## Configuration

### Environment Variables

Create `.env` file:

```bash
# Model Configuration
MODEL_DEVICE=0          # GPU ID (0) or -1 for CPU
MAX_QUESTIONS=1000      # Batch size limit
MODEL_PRECISION=fp16    # fp32 or fp16 for GPU

# Application Configuration
LOG_LEVEL=INFO          # DEBUG, INFO, WARNING, ERROR
DATA_DIR=./data         # Data directory path
CACHE_DIR=~/.models     # Model cache directory

# Translation Service
TRANSLATOR=nllb         # nllb or googletrans
ENABLE_CACHING=true     # Cache translations
```

### Model Configuration

Edit in `qiz_app.py`:

```python
# Device selection
device = 0      # GPU device ID
# device = -1   # Use CPU instead

# Model parameters
MAX_LENGTH = 60         # Output token limit
NUM_BEAMS = 5           # Beam search width
TEMPERATURE = 0.7       # Diversity control
REPETITION_PENALTY = 2.5
```

## Troubleshooting Installation

### Issue: ModuleNotFoundError

```bash
# Solution 1: Reinstall package
pip install --upgrade transformers

# Solution 2: Check virtual environment
which python  # Linux/Mac
where python  # Windows
```

### Issue: CUDA Version Mismatch

```bash
# Check CUDA compatibility
nvidia-smi
python -c "import torch; print(torch.version.cuda)"

# Install specific PyTorch version
pip install torch==2.1.1 torchvision==0.16.1 -f https://download.pytorch.org/whl/torch_stable.html
```

### Issue: Out of Memory

```bash
# Reduce batch size in config
MAX_QUESTIONS = 100  # Smaller batches

# Use CPU instead of GPU
MODEL_DEVICE = -1

# Reduce model precision
MODEL_PRECISION = "int8"  # Quantization
```

### Issue: Model Download Failures

```bash
# Manual model download
from transformers import AutoTokenizer, AutoModel
AutoTokenizer.from_pretrained("humarin/chatgpt_paraphraser_on_T5_base")

# Set cache directory
export HF_HOME=~/.cache/huggingface
```

### Issue: Streamlit Port Conflicts

```bash
# Run on different port
streamlit run deploy.py --server.port=8502
```

## Post-Installation Verification

### Test 1: Python Imports

```bash
python -c "
from transformers import pipeline
from deep_translator import GoogleTranslator
import streamlit as st
import torch
import json
print('✅ All imports successful')
"
```

### Test 2: Model Loading

```bash
python -c "
from transformers import pipeline
print('Loading model...')
p = pipeline('text2text-generation', model='humarin/chatgpt_paraphraser_on_T5_base')
print('✅ Model loaded successfully')
"
```

### Test 3: Sample Question Processing

```bash
python qiz_app.py
```

### Test 4: Web Interface

```bash
streamlit run deploy.py
# Should open http://localhost:8501
```

## Development Setup

### Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

### Contents of requirements-dev.txt

```
# Testing
pytest>=7.4.0
pytest-cov>=4.1.0

# Code Quality
black>=23.0.0
flake8>=6.0.0
pylint>=2.17.0

# Documentation
sphinx>=7.0.0
sphinx-rtd-theme>=1.3.0

# Jupyter
jupyter>=1.0.0
ipykernel>=6.25.0
```

### Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install

# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
```

## System Optimization

### Windows Optimization

```batch
# Increase virtual memory
SET PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512

# Run batch file before starting
@echo off
set PYTORCH_ENABLE_MPS_FALLBACK=1
python script.py
```

### Linux Optimization

```bash
# Check available memory
free -h

# Increase swap if needed
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### macOS Optimization

```bash
# For Apple Silicon Macs
pip install torch torchvision torchaudio

# Enable MPS (Metal Performance Shaders)
export PYTORCH_ENABLE_MPS_FALLBACK=1
```

## Multi-Environment Setup

### Development Environment

```bash
python -m venv dev-venv
source dev-venv/bin/activate  # Linux/Mac
pip install -r requirements.txt -r requirements-dev.txt
```

### Production Environment

```bash
python -m venv prod-venv
source prod-venv/bin/activate  # Linux/Mac
pip install -r requirements.txt --no-dev
```

### Testing Environment

```bash
python -m venv test-venv
source test-venv/bin/activate
pip install -r requirements.txt pytest pytest-cov
```

## Upgrade Instructions

### Upgrade All Dependencies

```bash
pip install --upgrade -r requirements.txt
```

### Upgrade Specific Package

```bash
pip install --upgrade transformers

# Verify compatibility
python -c "import torch, transformers; print(f'PyTorch: {torch.__version__}, Transformers: {transformers.__version__}')"
```

## Uninstallation

### Complete Removal

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rmdir venv  # Windows
rm -rf venv  # Linux/Mac

# Clean pip cache
pip cache purge
```

## Support

For installation issues:

1. Check Python version: `python --version`
2. Verify internet connection for model downloads
3. Check available disk space: 15GB+ needed
4. Run verification tests above
5. Check GPU status: `nvidia-smi`

See `QUICKSTART.md` for quick installation.
See `README.md` for complete documentation.
