# child_attention_versions.py
from transformers import pipeline
import json

# ---------- LOAD PARAPHRASER MODEL ----------
def load_paraphraser():
    return pipeline("text2text-generation", model="salti/arabic-t5-small-question-paraphrasing") #Vamsi/T5_Paraphrase_Paws

paraphraser = load_paraphraser()

# ---------- ATTENTION QUESTIONS (with logical thinking) ----------
original_questions = [
    {
        "question": "فيه ولد اسمه كريم عنده 4 أقلام، وقع منهم 2 على الأرض، وبعد كده اشترى 3 جداد، دلوقتي معاه كام قلم؟",
        "options": {"A": "4", "B": "5", "C": "7", "D": "6"},
        "answer": "C"
    },
    {
        "question": "لو رسمنا مربع جوه دايرة، إيه الشكل اللي حوالين التاني؟",
        "options": {"A": "المربع حوالين الدايرة", "B": "الدايرة حوالين المربع", "C": "الاتنين نفس الحجم", "D": "مش ممكن يحصل كده"},
        "answer": "B"
    },
    {
        "question": "فيه 3 أطفال واقفين في طابور: سامي قدام كريم، وكريم قدام مازن. مين في النص؟",
        "options": {"A": "سامي", "B": "كريم", "C": "مازن", "D": "كلهم جنب بعض"},
        "answer": "B"
    },
    {
        "question": "ولد عنده 5 كرات، كل واحدة بلون مختلف: أحمر، أزرق، أصفر، أخضر، برتقالي. لو شال الكرة اللي لونها في النص، هيفضل كام لون؟",
        "options": {"A": "4", "B": "3", "C": "2", "D": "5"},
        "answer": "A"
    },
    {
        "question": "مازن بيحب يلعب 10 دقايق ويرتاح 5 دقايق. لو بدأ الساعة 2:00، يبقى هيرتاح إمتى؟",
        "options": {"A": "2:10", "B": "2:05", "C": "2:15", "D": "2:20"},
        "answer": "A"
    }
    # أكمل باقي الأسئلة بنفس النمط لو تحب
]

# ---------- GENERATE MULTIPLE VERSIONS PER QUESTION ----------
def generate_multi_versions(questions, num_versions=3):
    extended_questions = []
    for q in questions:
        versions = []
        # Add original question
        versions.append(q["question"])

        # Generate paraphrased versions
        generated = paraphraser("paraphrase: " + q["question"], max_length=60, num_return_sequences=num_versions - 1)
        for alt in generated:
            versions.append(alt['generated_text'])

        q_copy = q.copy()
        q_copy["versions"] = versions
        extended_questions.append(q_copy)
    return extended_questions

questions_with_versions = generate_multi_versions(original_questions, num_versions=3)

# ---------- SAVE TO JSON WITH UTF-8 ENCODING ----------
with open("questions_with_versions.json", "w", encoding="utf-8") as f:
    json.dump(questions_with_versions, f, ensure_ascii=False, indent=2)

# ---------- DEBUG OUTPUT ----------
for i, q in enumerate(questions_with_versions):
    print(f"\nQuestoin {i+1}:")
    for v_idx, version in enumerate(q["versions"], start=1):
        print(f"  نسخة {v_idx}: {version}")
