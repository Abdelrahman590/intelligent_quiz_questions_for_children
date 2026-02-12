from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import json
import re
import os
os.environ['HF_HOME'] = 'D:/huggingface_cache'


# تحميل نموذج إعادة الصياغة
def get_paraphraser():
    try:
        return pipeline(
            "text2text-generation",
            model="humarin/chatgpt_paraphraser_on_T5_base",
            device=0,
            max_length=60
        )
    except Exception as e:
        print(f"⚠️ خطأ في تحميل نموذج إعادة الصياغة: {e}")
        return None

# تحميل نموذج الترجمة السياقية (NLLB)
nllb_model_name = "facebook/nllb-200-distilled-600M"
nllb_tokenizer = AutoTokenizer.from_pretrained(nllb_model_name)
nllb_model = AutoModelForSeq2SeqLM.from_pretrained(nllb_model_name)

# ترجمة ذكية باستخدام NLLB
def smart_translate(text, src_lang="eng_Latn", tgt_lang="arb_Arab"):
    try:
        inputs = nllb_tokenizer(text, return_tensors="pt", src_lang=src_lang)
        translated_tokens = nllb_model.generate(
            **inputs,
            forced_bos_token_id=nllb_tokenizer.lang_code_to_id[tgt_lang],
            max_length=60
        )
        return nllb_tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
    except Exception as e:
        print(f"⚠️ خطأ في NLLB: {e}")
        return text

# تصنيف النص
def classify_text(text):
    if re.fullmatch(r'[A-Za-z]', text.strip()):
        return "letter"
    elif len(text.strip().split()) == 1:
        return "word"
    else:
        return "sentence"

# ترجمة ذكية بناءً على نوع النص
def context_aware_translate(text):
    text_type = classify_text(text)
    if text_type == "letter":
        return {
            "A": "أ", "B": "ب", "C": "ج", "D": "د", "E": "هـ",
            "F": "ف", "G": "ج", "H": "هـ", "I": "ي", "J": "ج",
            "K": "ك", "L": "ل", "M": "م", "N": "ن", "O": "و",
            "P": "ب", "Q": "ق", "R": "ر", "S": "س", "T": "ت",
            "U": "ع", "V": "ف", "W": "و", "X": "إكس", "Y": "ي", "Z": "ز"
        }.get(text.upper(), text)
    else:
        return smart_translate(text)

# تبسيط لغوي للأطفال
def simplify_for_children(text):
    simplifications = {
        "التي": "اللي",
        "تستطيع": "تقدر",
        "يستطيع": "يقدر",
        "ذلك": "ده",
        "تلك": "دي",
        "الطفل": "الولد",
        "الطفلة": "البنت",
        "رسالة": "حرف",
        "جملة": "جُمله",
        "أي": "إيه",
        "ما هي": "إيه هي",
        "ما هو": "إيه هو"
    }
    for k, v in simplifications.items():
        text = text.replace(k, v)
    return text

# إعادة صياغة السؤال
def paraphrase_question(paraphraser, question, num_versions=3):
    if not paraphraser:
        return [question] * (num_versions + 1)
    versions = [question]
    try:
        paraphrases = paraphraser(
            f"paraphrase: {question}",
            num_return_sequences=min(num_versions * 2, 5),
            num_beams=5,
            temperature=0.7,
            repetition_penalty=2.5
        )
        unique_paraphrases = set()
        for p in paraphrases:
            text = p['generated_text'].strip()
            if (
                text.lower() != question.lower() and
                len(text.split()) > 3 and
                '?' in text
            ):
                unique_paraphrases.add(text)
        versions.extend(list(unique_paraphrases)[:num_versions])
        return versions
    except Exception as e:
        print(f"⚠️ خطأ في إعادة الصياغة: {e}")
        return [question] * (num_versions + 1)

# المعالجة الكاملة
def enhance_question_quality(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        paraphraser_model = get_paraphraser()

        for i, item in enumerate(data):
            item['versions'] = paraphrase_question(paraphraser_model, item['question'])

            item['versions_ar'] = [
                simplify_for_children(context_aware_translate(v))
                for v in item['versions']
            ]

            item['choices_ar'] = [
                simplify_for_children(context_aware_translate(c))
                for c in item['choices']
            ]

            item['answer_ar'] = simplify_for_children(context_aware_translate(item['answer']))

            item['category_ar'] = simplify_for_children(context_aware_translate(
                item['category'] if item['category'] else "عام"
            ))

            print(f"✅ تم تحسين السؤال {i+1}/{len(data)}")

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"🎉 تم حفظ النتائج في: {output_file}")
        return True

    except Exception as e:
        print(f"❌ خطأ أثناء المعالجة: {e}")
        return False

# التشغيل
if __name__ == "__main__":
    input_path = "D:\\company\\En_questions.json"
    output_path = "D:\\company\\enhanced_questions_final.json"
    enhance_question_quality(input_path, output_path)
