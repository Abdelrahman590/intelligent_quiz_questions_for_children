from transformers import pipeline
from deep_translator import GoogleTranslator
import json
import time
import re

def enhance_question_quality(input_file, output_file):
   
    def get_paraphraser():
        try:
            return pipeline(
                "text2text-generation",
                model="humarin/chatgpt_paraphraser_on_T5_base",
                device=0, 
                max_length=60
            )
        except Exception as e:
            print(f" خطأ في تحميل النموذج: {e}")
            return None
    
    def paraphrase_question(paraphraser, question, num_versions=3):
        
        if not paraphraser:
            return [question] * (num_versions + 1)
            
        versions = [question]
        num_candidates = num_versions * 2
        
        try:
            paraphrases = paraphraser(
                f"paraphrase: {question}",
                num_return_sequences=min(num_candidates, 5), 
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

    # 2. تحسين الترجمة
    def translate_for_children(text, context="education"):
        try:
            if len(text.split()) > 3:
                prefixed_text = f"{text}"
            else:
                prefixed_text = text
                
            translated = GoogleTranslator(source='auto', target='ar').translate(prefixed_text)
            
            corrections = {
                "رسائل": "حروف",
                "جمل": "جُمل",
                "ه": "هـ",
                "أ": "ا",
                "رسالة": "حرف"
            }
            
            for wrong, correct in corrections.items():
                translated = translated.replace(wrong, correct)
                
            return translated
        except Exception as e:
            print(f"⚠️ خطأ في الترجمة: {e}")
            return text

    #  تبسيط اللغة
    def simplify_for_children(text):
        simplifications = {
            "أي": "ما",
            "التي": "اللي",
            "تستطيع": "تقدر",
            "يستطيع": "يقدر",
            "المرأة": "الست",
            "الرجل": "الراجل",
            "الطفل": "الولد",
            "كلمة": "كلمه",
            "حرف": "حرف"
        }
        
        for complex_word, simple_word in simplifications.items():
            text = text.replace(complex_word, simple_word)
        
        return text

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        paraphraser_model = get_paraphraser()
        
        for i, item in enumerate(data):
            item['versions'] = paraphrase_question(paraphraser_model, item['question'])
            
            item['versions_ar'] = [simplify_for_children(translate_for_children(v)) 
                                   for v in item['versions']]
            
            item['choices_ar'] = [simplify_for_children(translate_for_children(c)) 
                                  for c in item['choices']]
            
            item['answer_ar'] = simplify_for_children(translate_for_children(item['answer']))
            
            item['category_ar'] = simplify_for_children(translate_for_children(item['category']))
            
            print(f"✅ تم تحسين السؤال {i+1}/{len(data)}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"🎉 تم حفظ الأسئلة المحسنة في {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ خطأ جسيم في المعالجة: {e}")
        return False

if __name__ == "__main__":
    input_path = "D:\\company\\En_questions.json"
    output_path = "D:\\company\\enhanced_questions2.json"
    
    enhance_question_quality(input_path, output_path)