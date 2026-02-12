# Architecture & Design

## System Architecture

```
┌─────────────────────────────────────────┐
│        Input Data (JSON)                │
│  - English Questions                     │
│  - Arabic Questions                      │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│   Question Processing Pipeline          │
├─────────────────────────────────────────┤
│ 1. Load & Parse JSON                    │
│ 2. Initialize NLP Models                │
│ 3. Iterate Questions                    │
└────────────┬────────────────────────────┘
             │
             ├─► Paraphrasing    (T5 Model)
             │   - num_beams=5
             │   - temp=0.7
             │   - repetition_penalty=2.5
             │
             ├─► Translation     (NLLB-200)
             │   - Smart context detection
             │   - Letter mapping for single chars
             │
             └─► Simplification
                 - Arabic vocab replacement
                 - Egyptian dialect adaptation
             │
             ▼
┌─────────────────────────────────────────┐
│    Enhanced Output (JSON)               │
│  - Original question                    │
│  - 3 paraphrased versions              │
│  - Arabic versions (all)                │
│  - Simplified choices & answers         │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│   Display & Interaction (Streamlit)     │
│   - Web UI with RTL support             │
│   - Quiz presentation                   │
│   - Score tracking                      │
└─────────────────────────────────────────┘
```

## Component Architecture

### 1. Module Structure

```
Application Layer
├── deploy.py          (Streamlit UI)
├── qiz_app.py         (Processing Pipeline)
└── app.py             (Legacy Entry Point)

NLP Processing Layer
├── paraphrasing.py    (T5-based paraphrasing)
├── Arabic_model/
│   └── AR_para.py     (Arabic-specific processing)
└── comp_parapharsing.ipynb (Interactive notebook)

Utilities Layer
├── extract.py         (Data extraction)
├── remove.py          (Data cleaning)
├── update_model.py    (Model management)
└── battary_book.py    (State persistence)

Data Layer
├── *_questions.json   (Input/Output data)
├── enhanced_*.json    (Processed outputs)
└── error.json         (Error logging)
```

### 2. Data Flow Diagram

```
INPUT: En_questions.json
│
├─ Question: "What is 2+2?"
│  Choices: ["3", "4", "5", "6"]
│  Answer: "B"
│
▼
PARAPHRASING (T5)
│
├─ "What does 2 plus 2 equal?"
├─ "Calculate: 2 + 2 = ?"
├─ "How much is 2 added to 2?"
│
▼
TRANSLATION (NLLB)
│
├─ "ما هو 2 + 2؟"
├─ "اطرح النتيجة: 2 + 2 = ؟"
├─ "كام ناتج 2 جمع 2؟"
│
▼
SIMPLIFICATION (Rule-based)
│
├─ "إيه هو 2 ضايف 2؟"
├─ "أظهر الحل: 2 ضايف 2 = إيه؟"
├─ "كام لما نجمع 2 مع 2؟"
│
▼
OUTPUT: enhanced_questions_final.json
{
  "question": "What is 2+2?",
  "versions": [...],
  "versions_ar": [...],
  "choices_ar": [...],
  ...
}
```

## Process Details

### Enhancement Pipeline

```python
def enhance_question_quality(input_file, output_file):
    # 1. Load Data
    data = load_json(input_file)  # JSON parsing

    # 2. Initialize Models
    paraphraser = get_paraphraser()  # T5 model load
    translator = NLLB()              # Translation model

    # 3. Process Each Question
    for item in data:
        # Step A: Paraphrase
        versions = paraphrase_question(paraphraser, item['question'])

        # Step B: Translate
        versions_ar = [translate(v) for v in versions]

        # Step C: Simplify
        versions_simplified = [simplify(v) for v in versions_ar]

        # Step D: Store Results
        item['versions'] = versions
        item['versions_ar'] = versions_simplified
        item['choices_ar'] = [simplify(translate(c)) for c in item['choices']]

    # 4. Save Output
    save_json(data, output_file)
```

### Paraphrasing Configuration

```python
pipeline(
    "text2text-generation",
    model="humarin/chatgpt_paraphraser_on_T5_base",
    device=0,           # GPU device ID
    max_length=60
)

# Generation parameters:
paraphraser(
    f"paraphrase: {question}",
    num_return_sequences=6,     # Generate 6 candidates
    num_beams=5,                # Beam search width
    temperature=0.7,            # Diversity control
    repetition_penalty=2.5      # Reduce repetition
)
```

### Translation Smart Detection

```python
def context_aware_translate(text):
    """Route translation based on text type"""

    if single_letter(text):
        # Direct mapping: "A" → "أ"
        return letter_map[text]

    elif single_word(text):
        # Word translation: "cat" → "قطة"
        return translate_word(text)

    else:
        # Sentence paraphrasing + translation
        return nllb_translate(text)
```

### Simplification Rules

```python
simplifications = {
    "التي": "اللي",          # Complex → Colloquial
    "تستطيع": "تقدر",       # Formal → Casual
    "الطفل": "الولد",       # Generic → Egyptian
    "كلمة": "كلمه",         # Formal → Phonetic
    ...
}

# Applied sequentially to all Arabic output
```

## Model Specifications

### T5-Paraphraser

| Property          | Value                                    |
| ----------------- | ---------------------------------------- |
| Model Name        | `humarin/chatgpt_paraphraser_on_T5_base` |
| Base Model        | Google T5                                |
| Parameters        | ~220M                                    |
| Input Max Tokens  | 256                                      |
| Output Max Tokens | 60                                       |
| GPU Memory        | ~1.5GB                                   |
| Inference Time    | 2-5s per question                        |

### NLLB-200

| Property       | Value                              |
| -------------- | ---------------------------------- |
| Model Name     | `facebook/nllb-200-distilled-600M` |
| Languages      | 200+                               |
| Variant        | Distilled (smaller)                |
| Parameters     | ~600M                              |
| GPU Memory     | ~2.5GB                             |
| Inference Time | 0.5-1s per text                    |

## Error Handling Strategy

```
Question Processing
    │
    ├─ Try: Paraphrase with T5
    │   └─ Fail? Return original + duplicates
    │
    ├─ Try: Translate with NLLB
    │   └─ Fail? Fallback to GoogleTranslate
    │
    ├─ Try: Simplify with rules
    │   └─ Fail? Return as-is
    │
    └─ Catch: Log error, continue with next
```

## Memory Management

### GPU Memory Allocation

```
Startup:
├─ T5 Model Load:      1.5 GB
├─ NLLB Model Load:    2.5 GB
├─ Tokenizers Cache:   0.5 GB
└─ Runtime Buffer:     1.0 GB
Total Peak:            5.5 GB
```

### Data Structure Memory

```
For 1000 questions:
├─ Original JSON:      ~800 KB
├─ Paraphrases:        ~6 MB (3 versions each)
├─ Translations:       ~8 MB (Arabic)
└─ Final Output:       ~15 MB
```

## Performance Optimization

### Batch Processing

- Process all questions in single model session
- Reuse loaded tokenizers
- Avoid redundant model reloads

### Caching Strategy

- Cache downloaded models in `~/.cache/huggingface/`
- Cache tokenizer vocabularies
- Reuse translation results

### Device Selection

- GPU (device=0): 10x faster, requires NVIDIA
- CPU (device=-1): Slower, always available

## Extension Points

### Add New Language

```python
# In context_aware_translate()
elif target_language == "fr":
    return NLLB_translate(text, src="eng", tgt="fra")
```

### Add New Simplification Rules

```python
# In simplify_for_children()
simplifications.update({
    "complex_word": "simple_word",
    ...
})
```

### Add New Model

```python
# In get_paraphraser()
if model_type == "gpt2":
    return pipeline("text-generation", model="gpt2")
```

## Testing Strategy

### Unit Tests (per function)

```bash
python -m pytest tests/test_paraphrase.py
python -m pytest tests/test_translate.py
```

### Integration Tests

```bash
python -m pytest tests/test_pipeline.py
```

### Performance Tests

```bash
python tests/benchmark.py
```

## Deployment Strategy

### Development

```
- Local Python
- CPU inference
- Single-threaded
```

### Production (Planned)

```
- Docker containerization
- GPU server deployment
- Multi-worker processing
- Redis caching
- PostgreSQL database
```

## Dependencies Graph

```
Streamlit
  ├─ Pillow (Image)
  └─ Session State

Transformers
  ├─ PyTorch
  ├─ Tokenizers
  └─ Hugging Face Hub

Deep-Translator
  ├─ Google Translate
  └─ Network IO

App
  ├─ JSON (stdlib)
  ├─ Time (stdlib)
  └─ Re (stdlib)
```

---

For detailed code documentation, see `README.md`.
