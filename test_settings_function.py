#!/usr/bin/env python3
"""
اختبار مخصص لدالة الإعدادات
لتشخيص أي مشاكل في الترجمة
"""

import asyncio
import sys
from database.database import Database
from translations import translations

# إعداد التسجيل
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestBot:
    """نسخة اختبار من البوت"""
    
    def __init__(self):
        self.db = Database()
        
    def get_user_language(self, user_id):
        """الحصول على لغة المستخدم"""
        try:
            user_settings = self.db.get_user_settings(user_id)
            if user_settings and user_settings.get('language'):
                return user_settings['language']
            
            # إنشاء إعدادات افتراضية
            self.db.update_user_language(user_id, 'ar')
            return 'ar'
        except Exception as e:
            logger.error(f"خطأ في الحصول على لغة المستخدم {user_id}: {e}")
            return 'ar'

    def get_text(self, key, user_id, **kwargs):
        """الحصول على النص المترجم"""
        user_language = self.get_user_language(user_id)
        # إزالة أي تضارب في المعاملات
        kwargs.pop('language', None)
        return translations.get_text(key, user_language, **kwargs)

class MockEvent:
    """محاكاة event للاختبار"""
    
    def __init__(self, user_id):
        self.sender_id = user_id
        
    async def edit(self, text, buttons=None):
        """محاكاة تعديل الرسالة"""
        print("=" * 60)
        print("📝 تم تعديل الرسالة بنجاح:")
        print("=" * 60)
        print(text)
        print("=" * 60)
        if buttons:
            print(f"🔘 عدد الأزرار: {len(buttons)} صف")
            for i, row in enumerate(buttons):
                print(f"   الصف {i+1}: {len(row)} زر")
        print("=" * 60)
        
    async def respond(self, text, buttons=None):
        """محاكاة الرد على الرسالة"""
        print("📤 تم إرسال رد:")
        print(text)

async def test_settings_function():
    """اختبار دالة الإعدادات"""
    print("🧪 اختبار دالة الإعدادات...")
    print("=" * 60)
    
    try:
        # إنشاء البوت والحدث
        bot = TestBot()
        test_user_id = 888888888
        
        # تعيين لغة المستخدم للاختبار
        languages_to_test = ['ar', 'en', 'fr']
        
        for lang in languages_to_test:
            print(f"\n🌐 اختبار باللغة: {lang}")
            print("-" * 40)
            
            # تعيين اللغة
            bot.db.update_user_language(test_user_id, lang)
            
            # إنشاء حدث وهمي
            event = MockEvent(test_user_id)
            
            # اختبار دالة الإعدادات
            await test_show_settings(bot, event)
            
        print("\n✅ اكتمل اختبار جميع اللغات بنجاح!")
        
    except Exception as e:
        print(f"\n❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

async def test_show_settings(bot, event):
    """اختبار دالة show_settings"""
    try:
        user_id = event.sender_id
        print(f"👤 معرف المستخدم: {user_id}")
        
        # الحصول على إعدادات المستخدم
        user_settings = bot.db.get_user_settings(user_id)
        print(f"📋 إعدادات المستخدم: {user_settings}")
        
        # اختبار ترجمة الأزرار
        print("🔘 اختبار ترجمة الأزرار:")
        button_keys = [
            'btn_change_language',
            'btn_change_timezone', 
            'btn_check_userbot',
            'btn_relogin',
            'btn_delete_all_tasks',
            'btn_back_to_main'
        ]
        
        buttons = []
        for key in button_keys:
            try:
                text = bot.get_text(key, user_id)
                buttons.append([f"Button: {text}"])
                print(f"   ✓ {key}: {text}")
            except Exception as e:
                print(f"   ❌ {key}: خطأ - {e}")
                raise
        
        # الحصول على لغة المستخدم بأمان
        if user_settings and user_settings.get('language'):
            user_language = user_settings['language']
        else:
            user_language = 'ar'
            bot.db.update_user_language(user_id, 'ar')
            
        language_name = translations.get_language_name(user_language)
        timezone_name = user_settings.get('timezone', 'Asia/Riyadh') if user_settings else 'Asia/Riyadh'

        print(f"🌐 لغة المستخدم: {user_language}")
        print(f"🏷️ اسم اللغة: {language_name}")
        print(f"🕐 المنطقة الزمنية: {timezone_name}")

        # اختبار نص الإعدادات
        print("📝 اختبار نص settings_title:")
        try:
            settings_text = bot.get_text("settings_title", user_id, 
                                       language_name=language_name, 
                                       timezone=timezone_name)
            print(f"   ✓ تم إنشاء النص بنجاح")
        except Exception as e:
            print(f"   ❌ خطأ في إنشاء النص: {e}")
            raise
        
        # محاكاة تعديل الرسالة
        await event.edit(settings_text, buttons=buttons)
        print("✅ تم اختبار دالة الإعدادات بنجاح!")
        
    except Exception as e:
        print(f"❌ خطأ في اختبار دالة الإعدادات: {e}")
        import traceback
        traceback.print_exc()
        raise

def test_individual_components():
    """اختبار المكونات الفردية"""
    print("\n🔧 اختبار المكونات الفردية...")
    print("=" * 60)
    
    try:
        # اختبار نظام الترجمة
        print("1️⃣ اختبار نظام الترجمة:")
        supported_langs = translations.get_supported_languages()
        print(f"   اللغات المدعومة: {supported_langs}")
        
        for lang in supported_langs[:3]:  # اختبار أول 3 لغات
            name = translations.get_language_name(lang)
            print(f"   {lang} → {name}")
        
        # اختبار قاعدة البيانات
        print("\n2️⃣ اختبار قاعدة البيانات:")
        db = Database()
        test_user = 777777777
        
        success = db.update_user_language(test_user, 'en')
        print(f"   تحديث اللغة: {'✓' if success else '✗'}")
        
        settings = db.get_user_settings(test_user)
        print(f"   استرجاع الإعدادات: {settings}")
        
        # اختبار الترجمة مع المعاملات
        print("\n3️⃣ اختبار الترجمة مع المعاملات:")
        test_text = translations.get_text('settings_title', 'ar', 
                                        language_name='العربية', 
                                        timezone='Asia/Riyadh')
        print(f"   النص المُنشأ: {test_text[:50]}...")
        
        print("\n✅ جميع المكونات الفردية تعمل بشكل صحيح!")
        return True
        
    except Exception as e:
        print(f"\n❌ خطأ في اختبار المكونات: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """الدالة الرئيسية"""
    print("🌐 اختبار شامل لنظام الإعدادات والترجمة")
    print("=" * 60)
    
    try:
        # اختبار المكونات الفردية أولاً
        if not test_individual_components():
            print("❌ فشل في اختبار المكونات الفردية!")
            return
        
        # اختبار دالة الإعدادات
        success = await test_settings_function()
        
        if success:
            print("\n🎉 نجح جميع الاختبارات!")
            print("✅ دالة الإعدادات تعمل بشكل مثالي!")
            print("\n💡 إذا كان لا يزال هناك خطأ في البوت الفعلي:")
            print("   1. تأكد من تشغيل البوت بآخر إصدار")
            print("   2. تحقق من سجلات الأخطاء (logs)")
            print("   3. أعد تشغيل البوت")
        else:
            print("\n❌ فشل في بعض الاختبارات!")
            
    except KeyboardInterrupt:
        print("\n⏹️ تم إيقاف الاختبار بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ عام في الاختبار: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())