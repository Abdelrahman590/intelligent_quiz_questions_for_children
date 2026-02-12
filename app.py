import json
from googletrans import Translator
original_questions = [
    {
        "question": "لf Ahmed has 3 balls and gives 2 to Mohamed, how many does he have left؟",
        "options": {"A": "3 كرات", "B": "كرة واحدة", "C": "5 كرات", "D": "2 كرات"},
        "answer": "B"
    },
    {
        "question": "مريم راحت المدرسة الساعة 8 وخرجت الساعة 2، كانت موجودة كام ساعة؟",
        "options": {"A": "6 ساعات", "B": "4 ساعات", "C": "10 ساعات", "D": "8 ساعات"},
        "answer": "A"
    },
    {
        "question": "الشمس بتطلع منين؟",
        "options": {"A": "الغرب", "B": "الشرق", "C": "الشمال", "D": "الجنوب"},
        "answer": "B"
    },
    {
        "question": "لو عندك تفاحة وموزة وبرتقالة، وكلت الموزة… إيه اللي فاضل؟",
        "options": {"A": "تفاحة وبصلة", "B": "تفاحة وبرتقالة", "C": "موزة وبرتقالة", "D": "موزة وتفاحة"},
        "answer": "B"
    },
    {
        "question": "لو لون السماء أخضر… هل ده طبيعي؟",
        "options": {"A": "أيوة", "B": "لأ", "C": "ممكن", "D": "في بعض الأحيان"},
        "answer": "B"
    },
]

# دالة للترجمة
def translate_text(text, src='ar', dest='en'):
    translator = Translator()
    return translator.translate(text, src=src, dest=dest).text

# دالة لإعادة الصياغة باستخدام نموذج بديل (افتراضي)
def manual_paraphrase_ar(question):
    """إعادة صياغة يدوية للأسئلة الشائعة"""
    paraphrases = {
        "لو أحمد عنده 3 كرات، وإدى محمد كرتين، يبقى معاه كام؟": [
            "أحمد كان معه 3 كرات ثم أعطى محمد كرتين، فكم بقي معه؟",
            "بعد إعطاء أحمد كرتين لمحمد من أصل 3 كرات كان يملكها، كم كرة تبقى؟"
        ],
        "مريم راحت المدرسة الساعة 8 وخرجت الساعة 2، كانت موجودة كام ساعة؟": [
            "إذا دخلت مريم المدرسة عند 8 صباحًا وغادرت عند 2 ظهرًا، فكم ساعة قضت؟",
            "من الساعة 8 إلى 2 ظهرًا، كم تبلغ المدة الزمنية؟"
        ],
        # أضف باقي الأسئلة هنا بنفس الطريقة
    }
    return paraphrases.get(question, [question + " (نسخة بديلة)"])

# توليد نسخ بديلة
def generate_alt_versions(questions):
    result = []
    for i, q in enumerate(questions):
        arabic_question = q["question"]
        
        # إعادة الصياغة اليدوية
        versions = [arabic_question] + manual_paraphrase_ar(arabic_question)
        
        result.append({
            "id": i+1,
            "original": arabic_question,
            "versions": versions,
            "options": q["options"],
            "answer": q["answer"]
        })
        
        # طباعة النتائج
        print(f"\n🟦 السؤال الأصلي {i+1}: {arabic_question}")
        for j, v in enumerate(versions[1:], 1):
            print(f"🔹 النسخة {j}: {v}")
    
    return result

# تشغيل الدالة
questions_with_alts = generate_alt_versions(original_questions)

# حفظ النتائج في ملف
with open('questions_versions.json', 'w', encoding='utf-8') as f:
    json.dump(questions_with_alts, f, ensure_ascii=False, indent=4)