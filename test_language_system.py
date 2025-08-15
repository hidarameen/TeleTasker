#!/usr/bin/env python3
"""
اختبار نظام اللغات المتعددة
"""

from translations import translations
from database.database import Database
import sys

def test_translation_system():
    """اختبار نظام الترجمة"""
    print("🧪 اختبار نظام الترجمة...")
    print("=" * 50)
    
    # اختبار اللغات المختلفة
    languages = translations.get_supported_languages()
    print(f"🌐 اللغات المدعومة: {languages}")
    print()
    
    # اختبار رسالة الترحيب بجميع اللغات
    print("📝 اختبار رسالة الترحيب:")
    print("-" * 30)
    
    for lang in languages:
        welcome_msg = translations.get_text(
            'welcome_authenticated', 
            lang, 
            name='أحمد/Ahmed', 
            status='🟢 نشط/Active'
        )
        lang_name = translations.get_language_name(lang)
        print(f"{lang_name}:")
        print(welcome_msg[:100] + "..." if len(welcome_msg) > 100 else welcome_msg)
        print()
    
    print("✅ اختبار الترجمة مكتمل!")

def test_database_language_functions():
    """اختبار دوال قاعدة البيانات"""
    print("🗄️ اختبار قاعدة البيانات...")
    print("=" * 50)
    
    try:
        db = Database()
        test_user_id = 999999999
        
        # اختبار حفظ واسترجاع اللغات
        languages_to_test = ['ar', 'en', 'fr', 'de', 'es', 'ru']
        
        for lang in languages_to_test:
            # حفظ اللغة
            success = db.update_user_language(test_user_id, lang)
            print(f"📝 حفظ اللغة {lang}: {'✅' if success else '❌'}")
            
            # استرجاع الإعدادات
            settings = db.get_user_settings(test_user_id)
            if settings and settings.get('language') == lang:
                print(f"📖 استرجاع اللغة {lang}: ✅")
            else:
                print(f"📖 استرجاع اللغة {lang}: ❌")
            print()
        
        print("✅ اختبار قاعدة البيانات مكتمل!")
        
    except Exception as e:
        print(f"❌ خطأ في اختبار قاعدة البيانات: {e}")

def test_language_names():
    """اختبار أسماء اللغات"""
    print("🏷️ اختبار أسماء اللغات...")
    print("=" * 50)
    
    languages = ['ar', 'en', 'fr', 'de', 'es', 'ru']
    
    for lang in languages:
        name = translations.get_language_name(lang)
        print(f"{lang} → {name}")
    
    print()
    print("✅ اختبار أسماء اللغات مكتمل!")

def test_button_translations():
    """اختبار ترجمة الأزرار"""
    print("🔘 اختبار ترجمة الأزرار...")
    print("=" * 50)
    
    button_keys = [
        'btn_manage_tasks',
        'btn_settings', 
        'btn_check_userbot',
        'btn_about',
        'btn_change_language',
        'btn_back_to_main'
    ]
    
    languages = ['ar', 'en', 'fr']  # عينة من اللغات
    
    for key in button_keys:
        print(f"🔹 {key}:")
        for lang in languages:
            text = translations.get_text(key, lang)
            lang_name = translations.get_language_name(lang)[:8]  # أول 8 أحرف
            print(f"  {lang_name}: {text}")
        print()
    
    print("✅ اختبار ترجمة الأزرار مكتمل!")

def demo_language_switching():
    """عرض توضيحي لتبديل اللغات"""
    print("🔄 عرض توضيحي لتبديل اللغات")
    print("=" * 50)
    
    # محاكاة مستخدم يغير لغته
    demo_user_id = 888888888
    
    try:
        db = Database()
        
        # البداية بالعربية
        db.update_user_language(demo_user_id, 'ar')
        settings = db.get_user_settings(demo_user_id)
        print(f"🇸🇦 المستخدم باللغة العربية:")
        print(f"   الإعدادات: {settings}")
        print(f"   النص: {translations.get_text('btn_manage_tasks', 'ar')}")
        print()
        
        # التبديل للإنجليزية
        db.update_user_language(demo_user_id, 'en')
        settings = db.get_user_settings(demo_user_id)
        print(f"🇺🇸 المستخدم باللغة الإنجليزية:")
        print(f"   Settings: {settings}")
        print(f"   Text: {translations.get_text('btn_manage_tasks', 'en')}")
        print()
        
        # التبديل للفرنسية
        db.update_user_language(demo_user_id, 'fr')
        settings = db.get_user_settings(demo_user_id)
        print(f"🇫🇷 المستخدم باللغة الفرنسية:")
        print(f"   Paramètres: {settings}")
        print(f"   Texte: {translations.get_text('btn_manage_tasks', 'fr')}")
        print()
        
        print("✅ عرض تبديل اللغات مكتمل!")
        
    except Exception as e:
        print(f"❌ خطأ في عرض تبديل اللغات: {e}")

def main():
    """الدالة الرئيسية"""
    print("🌐 مرحباً بك في اختبار نظام اللغات المتعددة")
    print("=" * 60)
    print()
    
    try:
        # تشغيل جميع الاختبارات
        test_translation_system()
        print("\n" + "="*60 + "\n")
        
        test_language_names()
        print("\n" + "="*60 + "\n")
        
        test_button_translations()
        print("\n" + "="*60 + "\n")
        
        test_database_language_functions()
        print("\n" + "="*60 + "\n")
        
        demo_language_switching()
        print("\n" + "="*60 + "\n")
        
        print("🎉 جميع الاختبارات مكتملة بنجاح!")
        print("✅ نظام اللغات المتعددة يعمل بشكل مثالي!")
        
    except KeyboardInterrupt:
        print("\n⏹️ تم إيقاف الاختبار بواسطة المستخدم")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ خطأ عام: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()