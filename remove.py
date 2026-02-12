import os
import shutil

def clean_huggingface_cache():
    # الكاش الافتراضي القديم
    default_cache = os.path.expanduser("~/.cache/huggingface")

    # الكاش الجديد
    new_cache = "D:/huggingface_cache"

    print("🧹 جاري تنظيف كاش HuggingFace القديم...")

    try:
        if os.path.exists(default_cache):
            shutil.rmtree(default_cache)
            print(f"✅ تم حذف الكاش القديم: {default_cache}")
        else:
            print("ℹ️ لا يوجد كاش قديم لحذفه.")
    except Exception as e:
        print(f"❌ فشل حذف الكاش القديم: {e}")
        return

    print("\n📁 جاري إعداد الكاش الجديد...")
    try:
        os.makedirs(new_cache, exist_ok=True)
        os.environ['HF_HOME'] = new_cache
        print(f"✅ تم إعداد الكاش الجديد في: {new_cache}")
    except Exception as e:
        print(f"❌ فشل إعداد الكاش الجديد: {e}")
        return

    print("\n🚀 كل حاجة جاهزة! شغّل سكربت الترجمة دلوقتي وهيشتغل بدون مشاكل 💪")

if __name__ == "__main__":
    clean_huggingface_cache()
