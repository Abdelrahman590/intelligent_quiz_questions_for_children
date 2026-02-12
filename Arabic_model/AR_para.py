from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import json

# استخدام النموذج البديل لإعادة صياغة الأسئلة
model_name = "salti/arabic-t5-small-question-paraphrasing"

try:
    # تهيئة النموذج
    print(f"⚙️ جاري تحميل النموذج {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # استخدام GPU إذا متاح
    
    paraphraser = pipeline(
        "text2text-generation", 
        model=model, 
        tokenizer=tokenizer
    )

    print("✅ تم تحميل النموذج بنجاح!")

    def generate_paraphrases(question, num_versions=2):
        """توليد إعادة صياغات للسؤال مع الحفاظ على الأصل"""
        paraphrases = paraphraser(
            question,
            max_new_tokens=80,
            num_return_sequences=num_versions,
            num_beams=5,
            repetition_penalty=2.0,
            temperature=0.7  # تنويع الإخراج
        )
        return [p['generated_text'] for p in paraphrases]

    # معالجة الملف
    input_file = "D:\\company\\arabic_questions.json"
    print(f"📂 جاري قراءة الملف: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    print(f"🔁 بدء معالجة {len(questions)} سؤال...")

    for i, item in enumerate(questions, 1):
        original = item.get('question_ar') or item.get('السؤال')  # دعم المفتاحين
        try:
            versions = [original] + generate_paraphrases(original, num_versions=2)
            item['versions_ar'] = versions
            print(f"[{i}/{len(questions)}] ✓ تمت إعادة صياغة: {original}")
        except Exception as e:
            print(f"[{i}/{len(questions)}] ✗ خطأ في: {original} - {str(e)}")
            item['versions_ar'] = [original]

    # حفظ النتائج
    output_file = 'enhanced_questions1.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

    print(f"💾 تم الانتهاء! النتائج محفوظة في {output_file}")
    print(f"• عدد الأسئلة المعالجة: {len(questions)}")
    print(f"• إجمالي النسخ المتاحة: {sum(len(item['versions_ar']) for item in questions)}")

except Exception as e:
    print(f"❌ حدث خطأ جسيم: {str(e)}")
    print("الحلول المقترحة:")
    print("1. تأكد من اتصالك بالإنترنت")
    print("2. قم بتحديث المكتبات: pip install --upgrade transformers torch")
    print("3. جرب استخدام GPU إذا كان متاحًا")
    print("4. تحقق من صحة مسار الملفات")
