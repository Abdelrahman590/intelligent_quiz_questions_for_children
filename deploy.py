# child_quiz_app_deploy.py
import streamlit as st
import json
import random
from PIL import Image

# ---------- CONFIG ----------
st.set_page_config(page_title="اختبار الانتباه للأطفال", layout="centered")
st.markdown("""
    <style>
        body, .stButton > button {
            font-family: 'Cairo', sans-serif;
            direction: rtl;
        }
        .question {
            font-size: 22px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- HEADER IMAGE ----------
image = Image.open("child_avatar.jpg")  # ضع صورة باسم child_avatar.jpg في نفس المجلد
st.image(image, caption=" اختبار الانتباه للأطفال", use_container_width=True)

# ---------- LOAD QUESTIONS ----------
@st.cache_data
def load_questions():
    with open("enhanced_questions.json", "r", encoding="utf-8") as f:
        return json.load(f)

all_questions = load_questions()

# فلترة الأسئلة الخاصة بالفهم والاتجاه
comprehension_questions = [q for q in all_questions if q.get("category_ar") == "فهـم"]
direction_questions = [q for q in all_questions if q.get("category_ar") == "الاتجاهـ"]

# اختيار 10 من كل فئة بشكل عشوائي
selected_comprehension = random.sample(comprehension_questions, min(10, len(comprehension_questions)))
selected_direction = random.sample(direction_questions, min(10, len(direction_questions)))
selected_questions = selected_comprehension + selected_direction
random.shuffle(selected_questions)

# ---------- SESSION STATE ----------
if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.finished = False
    st.session_state.try_again = False
    st.session_state.questions = selected_questions

# ---------- MAIN QUIZ ----------
if not st.session_state.finished:
    q = st.session_state.questions[st.session_state.index]
    current_q_text = q['versions_ar'][1] if st.session_state.try_again and len(q['versions_ar']) > 1 else q['versions_ar'][0]

    st.markdown(f"<div class='question'>سؤال {st.session_state.index + 1}: {current_q_text}</div>", unsafe_allow_html=True)

    for idx, choice in enumerate(q['choices_ar']):
        key = f"btn-{st.session_state.index}-{idx}"
        if st.button(f"{chr(65+idx)}) {choice}", key=key):
            if choice == q['answer_ar']:
                st.success(" إجابة صحيحة!")
                st.session_state.score += 1
            else:
                st.error(f" خطأ! الإجابة الصحيحة: {q['answer_ar']}")
            st.session_state.index += 1
            if st.session_state.index >= len(st.session_state.questions):
                st.session_state.finished = True
            st.rerun()

# ---------- RESULTS ----------
if st.session_state.finished:
    st.markdown("---")
    st.subheader(" النتيجة النهائية")
    st.write(f"الدرجة: {st.session_state.score} من {len(st.session_state.questions)}")

    if st.session_state.score == len(st.session_state.questions):
        st.success(" ممتاز! تركيزك عالي جدًا.")
    elif st.session_state.score >= len(st.session_state.questions) * 0.6:
        st.info(" جيد! بس محتاج شوية تركيز.")
    else:
        st.warning(" محتاج تدريب أكتر على الانتباه.")
        st.info("📘 تم تجهيز نسخة من الأسئلة بصياغة مختلفة لك")

    if st.button(" حاول تاني بصياغة مختلفة"):
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.finished = False
        st.session_state.try_again = True
        st.session_state.questions = selected_questions
        st.rerun()

    st.download_button(
        label=" تحميل النتيجة",
        data=f"نتيجتك: {st.session_state.score} من {len(st.session_state.questions)}",
        file_name="attention_score.txt",
        mime="text/plain"
    )

    if st.button(" إعادة الاختبار من الأول"):
        selected_comprehension = random.sample(comprehension_questions, min(10, len(comprehension_questions)))
        selected_direction = random.sample(direction_questions, min(10, len(direction_questions)))
        selected_questions = selected_comprehension + selected_direction
        random.shuffle(selected_questions)
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.finished = False
        st.session_state.try_again = False
        st.session_state.questions = selected_questions
        st.rerun()

# ---------- IGNORE UNUSED MODEL IMPORT ----------
