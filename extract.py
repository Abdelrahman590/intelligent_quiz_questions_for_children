import pdfplumber
from pyarabic import araby

def extract_and_clean_arabic(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        # تنظيف النص
        text = araby.strip_diacritics(text)
        text = text.replace('ى', 'ي').replace('ة', 'ه')
        
        print("✅ تم استخراج النص بنجاح!")
        print(f"📄 عدد الأحرف: {len(text)}")
        print("📝 أول 200 حرف:")
        print(text[:200])
        
        return text
    
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return None

# استخدام الكود
if __name__ == "__main__":
    # ضع مسار الـ PDF هنا
    pdf_path = "D:\\rag_bot_book\\98 (2).pdf"  # غير اسم الملف هنا
    
    text = extract_and_clean_arabic(pdf_path)
    
    if text:
        # حفظ النص في ملف
        with open("extracted_text.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print("💾 تم حفظ النص في ملف extracted_text.txt")