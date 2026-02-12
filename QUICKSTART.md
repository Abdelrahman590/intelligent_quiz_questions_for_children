# Quick Start Guide

Get the Children's Intelligence Test Application running in 5 minutes.

## Prerequisites

- Python 3.8+
- pip, git
- 4GB+ RAM
- Optional: NVIDIA GPU for faster processing

## Installation (5 minutes)

### Step 1: Setup Environment

```bash
# Navigate to project directory
cd d:\company

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### Step 2: Install Dependencies

```bash
pip install transformers torch deep-translator streamlit googletrans Pillow
```

Or with requirements file:

```bash
pip install -r requirements.txt
```

### Step 3: Run Application

**Option A: Web Quiz Interface**

```bash
streamlit run deploy.py
```

Opens at `http://localhost:8501`

**Option B: Process Questions**

```bash
python qiz_app.py
```

**Option C: Jupyter Notebook**

```bash
jupyter notebook comp_parapharsing.ipynb
```

## First Run Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] JSON data files present
- [ ] `child_avatar.jpg` in root directory
- [ ] Model downloads complete (auto on first run)

## Common Commands

```bash
# Enhancement pipeline
python qiz_app.py

# Arabic model processing
python Arabic_model/AR_para.py

# Launch interactive app
streamlit run deploy.py

# Extract/clean data
python extract.py
python remove.py

# Update models
python update_model.py
```

## Next Steps

1. ✅ Check `EN_questions.json` for input format
2. ✅ Run enhancement: `python qiz_app.py`
3. ✅ Launch app: `streamlit run deploy.py`
4. ✅ View output in `enhanced_questions_final.json`

## Troubleshooting

**GPU not detected?**

```python
# Edit qiz_app.py, change: device=0 → device=-1
```

**Out of memory?**

```bash
# Close other applications, or use CPU
```

**Models not downloading?**

```bash
pip install --upgrade transformers
```

See `README.md` for detailed documentation.
