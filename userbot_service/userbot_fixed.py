"""
UserBot Service - النسخة المصححة
تم إصلاح مشكلة وضع التوجيه: فصل منطق requires_copy_mode عن forward_mode
"""

import logging
import asyncio
import json
import time
from typing import Dict, List, Optional, Any
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument, MessageMediaWebPage
from telethon.errors import FloodWaitError, ChatAdminRequiredError, UserBannedInChannelError
from database import get_database

logger = logging.getLogger(__name__)

class UserBotService:
    def __init__(self):
        self.db = get_database()
        self.clients = {}  # {user_id: client}
        self.album_collectors = {}  # {user_id: AlbumCollector}
        
    async def process_message(self, event, user_id: int, client: TelegramClient):
        """معالجة الرسالة مع إصلاح منطق وضع التوجيه"""
        try:
            source_chat_id = event.chat_id
            
            # الحصول على المهام المطابقة
            matching_tasks = self.get_matching_tasks(source_chat_id, user_id)
            if not matching_tasks:
                return
            
            # معالجة الوسائط مرة واحدة
            processed_media = None
            processed_filename = None
            original_text = event.message.text or ""
            
            if event.message.media:
                try:
                    # معالجة الوسائط (watermark, etc.)
                    processed_media, processed_filename = await self._process_media(event.message.media, user_id)
                except Exception as e:
                    logger.error(f"❌ خطأ في معالجة الوسائط: {e}")
                    processed_media = event.message.media
                    processed_filename = None
            
            # توجيه الرسالة لجميع المهام المطابقة
            for i, task in enumerate(matching_tasks):
                try:
                    target_chat_id = str(task['target_chat_id']).strip()
                    task_name = task.get('task_name', f"مهمة {task['id']}")
                    
                    # فحص الفلاتر المتقدمة
                    should_block, should_remove_buttons, should_remove_forward = await self._check_message_advanced_filters(
                        task['id'], event.message
                    )
                    
                    if should_block:
                        logger.info(f"🚫 الرسالة محظورة بواسطة فلاتر متقدمة للمهمة {task_name}")
                        continue
                    
                    # الحصول على وضع التوجيه وإعدادات التوجيه
                    forward_mode = task.get('forward_mode', 'forward')
                    forwarding_settings = self.get_forwarding_settings(task['id'])
                    split_album_enabled = forwarding_settings.get('split_album_enabled', False)
                    mode_text = "نسخ" if forward_mode == 'copy' else "توجيه"
                    
                    # تطبيق فلتر الرسائل المُوجهة
                    if should_remove_forward:
                        forward_mode = 'copy'  # إجبار النسخ لإزالة علامة التوجيه
                        mode_text = "نسخ (بدون علامة التوجيه)"
                        logger.info(f"📋 تم تحويل إلى وضع النسخ لإزالة علامة التوجيه")
                    
                    logger.info(f"🔄 بدء {mode_text} رسالة من {source_chat_id} إلى {target_chat_id} (المهمة: {task_name})")
                    
                    # فحص وضع النشر
                    publishing_mode = forwarding_settings.get('publishing_mode', 'auto')
                    if publishing_mode == 'manual':
                        logger.info(f"⏸️ وضع النشر اليدوي - إرسال الرسالة للمراجعة (المهمة: {task_name})")
                        await self._handle_manual_approval(event.message, task, user_id, client)
                        continue
                    
                    # تطبيق فاصل الإرسال
                    if i > 0:
                        await self._apply_sending_interval(task['id'])
                    
                    # إرسال الرسالة بناءً على وضع التوجيه
                    await self._send_message_with_correct_mode(
                        event, task, user_id, client, target_chat_id,
                        forward_mode, forwarding_settings, processed_media, processed_filename
                    )
                    
                except Exception as forward_error:
                    task_name = task.get('task_name', f"مهمة {task['id']}")
                    logger.error(f"❌ فشل في توجيه الرسالة (المهمة: {task_name}) للمستخدم {user_id}")
                    logger.error(f"💥 تفاصيل الخطأ: {str(forward_error)}")
                    
        except Exception as e:
            logger.error(f"خطأ في معالج الرسائل للمستخدم {user_id}: {e}")
    
    async def _send_message_with_correct_mode(self, event, task, user_id, client, target_chat_id,
                                            forward_mode, forwarding_settings, processed_media, processed_filename):
        """إرسال الرسالة بالوضع الصحيح - إصلاح منطق التوجيه"""
        try:
            # الحصول على إعدادات الرسالة
            message_settings = self.get_message_settings(task['id'])
            
            # تطبيق تنظيف النص والاستبدالات
            original_text = event.message.text or ""
            cleaned_text = self.apply_text_cleaning(original_text, task['id']) if original_text else original_text
            modified_text = self.apply_text_replacements(task['id'], cleaned_text) if cleaned_text else cleaned_text
            
            # تطبيق الترجمة (فقط في وضع النسخ)
            if forward_mode == 'copy':
                translated_text = await self.apply_translation(task['id'], modified_text) if modified_text else modified_text
                if modified_text != translated_text and modified_text:
                    logger.info(f"🌐 تم تطبيق الترجمة في وضع النسخ: '{modified_text}' → '{translated_text}'")
            else:
                translated_text = modified_text  # تجاهل الترجمة في وضع التوجيه
                logger.info(f"⏭️ تم تجاهل الترجمة في وضع التوجيه - إرسال الرسالة كما هي")
            
            # تطبيق تنسيق النص
            formatted_text = self.apply_text_formatting(translated_text, message_settings) if translated_text else translated_text
            
            # تطبيق الترويسة والتذييل
            final_text = self.apply_message_formatting(formatted_text, message_settings)
            
            # فحص ما إذا كان يحتاج إلى وضع النسخ بسبب التنسيق
            requires_copy_mode = (
                original_text != modified_text or  # تم تطبيق استبدالات النص
                modified_text != translated_text or  # تم تطبيق الترجمة
                translated_text != formatted_text or  # تم تطبيق تنسيق النص
                message_settings['header_enabled'] or  # الترويسة مفعلة
                message_settings['footer_enabled'] or  # التذييل مفعل
                message_settings['inline_buttons_enabled']  # الأزرار الإنلاين مفعلة
            )
            
            # تسجيل التغييرات إذا تم تعديل النص
            if original_text != final_text and original_text:
                logger.info(f"🔄 تم تطبيق تنسيق الرسالة: '{original_text}' → '{final_text}'")
            
            # تحديد الأزرار المراد استخدامها
            inline_buttons = None
            original_reply_markup = None
            
            # الحفاظ على الأزرار الأصلية إذا كان فلتر الأزرار معطل
            if not should_remove_buttons and event.message.reply_markup:
                original_reply_markup = event.message.reply_markup
                logger.info(f"🔘 الحفاظ على الأزرار الأصلية - فلتر الأزرار الشفافة معطل للمهمة {task['id']}")
            
            # بناء الأزرار الإنلاين المخصصة إذا كانت مفعلة
            if message_settings['inline_buttons_enabled'] and not should_remove_buttons:
                inline_buttons = self.build_inline_buttons(task['id'])
                if inline_buttons:
                    logger.info(f"🔘 تم بناء {len(inline_buttons)} صف من الأزرار الإنلاين المخصصة للمهمة {task['id']}")
            
            # ===== منطق الإرسال المصحح =====
            
            # تحديد الوضع النهائي للإرسال
            final_send_mode = self._determine_final_send_mode(forward_mode, requires_copy_mode)
            
            logger.info(f"📤 إرسال الرسالة بالوضع: {final_send_mode} (الأصلي: {forward_mode}, يتطلب نسخ: {requires_copy_mode})")
            
            # إرسال الرسالة بالوضع المحدد
            if final_send_mode == 'copy':
                await self._send_as_copy(
                    event, client, target_chat_id, final_text, forwarding_settings,
                    processed_media, processed_filename, original_reply_markup, inline_buttons
                )
            else:  # forward mode
                await self._send_as_forward(
                    event, client, target_chat_id, forwarding_settings
                )
                
        except Exception as e:
            logger.error(f"❌ خطأ في إرسال الرسالة: {e}")
            raise e
    
    def _determine_final_send_mode(self, forward_mode: str, requires_copy_mode: bool) -> str:
        """تحديد الوضع النهائي للإرسال - إصلاح منطق التوجيه"""
        if forward_mode == 'copy':
            # وضع النسخ - دائماً نسخ
            return 'copy'
        elif forward_mode == 'forward':
            if requires_copy_mode:
                # وضع التوجيه مع تنسيق - إجبار النسخ
                logger.info(f"🔄 إجبار النسخ في وضع التوجيه بسبب التنسيق")
                return 'copy'
            else:
                # وضع التوجيه بدون تنسيق - توجيه عادي
                return 'forward'
        else:
            # افتراضي - توجيه
            return 'forward'
    
    async def _send_as_copy(self, event, client, target_chat_id, final_text, forwarding_settings,
                          processed_media, processed_filename, original_reply_markup, inline_buttons):
        """إرسال الرسالة كنسخ"""
        try:
            target_entity = int(target_chat_id) if not target_chat_id.startswith('@') else target_chat_id
            
            if event.message.media:
                # رسالة وسائط
                await self._send_media_as_copy(
                    event, client, target_entity, final_text, forwarding_settings,
                    processed_media, processed_filename, original_reply_markup, inline_buttons
                )
            elif event.message.text or final_text:
                # رسالة نصية
                await self._send_text_as_copy(
                    client, target_entity, final_text, forwarding_settings,
                    original_reply_markup, inline_buttons
                )
            else:
                # أنواع أخرى - توجيه
                await client.forward_messages(
                    target_entity,
                    event.message,
                    silent=forwarding_settings['silent_notifications']
                )
                
        except Exception as e:
            logger.error(f"❌ خطأ في إرسال النسخ: {e}")
            raise e
    
    async def _send_as_forward(self, event, client, target_chat_id, forwarding_settings):
        """إرسال الرسالة كتوجيه"""
        try:
            target_entity = int(target_chat_id) if not target_chat_id.startswith('@') else target_chat_id
            
            # توجيه عادي
            forwarded_msg = await client.forward_messages(
                target_entity,
                event.message,
                silent=forwarding_settings['silent_notifications']
            )
            
            logger.info(f"✅ تم التوجيه بنجاح إلى {target_chat_id}")
            return forwarded_msg
            
        except Exception as e:
            logger.error(f"❌ خطأ في التوجيه: {e}")
            raise e
    
    async def _send_media_as_copy(self, event, client, target_entity, final_text, forwarding_settings,
                                processed_media, processed_filename, original_reply_markup, inline_buttons):
        """إرسال الوسائط كنسخ"""
        try:
            # فحص نوع الوسائط
            if isinstance(event.message.media, MessageMediaWebPage):
                # صفحة ويب - إرسال كنص
                message_text = final_text or event.message.text or "رسالة"
                processed_text, spoiler_entities = self._process_spoiler_entities(message_text)
                
                if spoiler_entities:
                    await client.send_message(
                        target_entity,
                        processed_text,
                        link_preview=forwarding_settings['link_preview_enabled'],
                        silent=forwarding_settings['silent_notifications'],
                        formatting_entities=spoiler_entities,
                        buttons=original_reply_markup or inline_buttons,
                    )
                else:
                    await client.send_message(
                        target_entity,
                        processed_text,
                        link_preview=forwarding_settings['link_preview_enabled'],
                        silent=forwarding_settings['silent_notifications'],
                        parse_mode='HTML',
                        buttons=original_reply_markup or inline_buttons,
                    )
            else:
                # وسائط عادية
                caption_text = final_text
                text_cleaning_settings = self.db.get_text_cleaning_settings(task['id'])
                if text_cleaning_settings and text_cleaning_settings.get('remove_caption', False):
                    caption_text = None
                    logger.info(f"🗑️ تم حذف التسمية التوضيحية للمهمة {task['id']}")
                
                # إرسال الوسائط
                media_to_send = processed_media if processed_media else event.message.media
                filename_to_send = processed_filename if processed_filename else "media_file.jpg"
                
                from send_file_helper import TelethonFileSender
                await TelethonFileSender.send_file_with_name(
                    client,
                    target_entity,
                    media_to_send,
                    filename_to_send,
                    caption=caption_text,
                    silent=forwarding_settings['silent_notifications'],
                    parse_mode='HTML' if caption_text else None,
                    force_document=False,
                    buttons=original_reply_markup or inline_buttons,
                )
                
        except Exception as e:
            logger.error(f"❌ خطأ في إرسال الوسائط كنسخ: {e}")
            raise e
    
    async def _send_text_as_copy(self, client, target_entity, final_text, forwarding_settings,
                               original_reply_markup, inline_buttons):
        """إرسال النص كنسخ"""
        try:
            message_text = final_text or "رسالة"
            processed_text, spoiler_entities = self._process_spoiler_entities(message_text)
            
            if spoiler_entities:
                await client.send_message(
                    target_entity,
                    processed_text,
                    link_preview=forwarding_settings['link_preview_enabled'],
                    silent=forwarding_settings['silent_notifications'],
                    formatting_entities=spoiler_entities,
                    buttons=original_reply_markup or inline_buttons,
                )
            else:
                await client.send_message(
                    target_entity,
                    processed_text,
                    link_preview=forwarding_settings['link_preview_enabled'],
                    silent=forwarding_settings['silent_notifications'],
                    parse_mode='HTML',
                    buttons=original_reply_markup or inline_buttons,
                )
                
        except Exception as e:
            logger.error(f"❌ خطأ في إرسال النص كنسخ: {e}")
            raise e
    
    # باقي الدوال المساعدة (مختصرة)
    def get_matching_tasks(self, source_chat_id, user_id):
        """الحصول على المهام المطابقة"""
        return self.db.get_active_tasks_for_source(str(source_chat_id), user_id)
    
    def get_forwarding_settings(self, task_id):
        """الحصول على إعدادات التوجيه"""
        return self.db.get_forwarding_settings(task_id)
    
    def get_message_settings(self, task_id):
        """الحصول على إعدادات الرسالة"""
        return self.db.get_message_settings(task_id)
    
    async def _check_message_advanced_filters(self, task_id, message):
        """فحص الفلاتر المتقدمة"""
        # تنفيذ فحص الفلاتر
        return False, False, False
    
    def apply_text_cleaning(self, text, task_id):
        """تطبيق تنظيف النص"""
        return text
    
    def apply_text_replacements(self, task_id, text):
        """تطبيق استبدالات النص"""
        return text
    
    async def apply_translation(self, task_id, text):
        """تطبيق الترجمة"""
        return text
    
    def apply_text_formatting(self, text, message_settings):
        """تطبيق تنسيق النص"""
        return text
    
    def apply_message_formatting(self, text, message_settings):
        """تطبيق تنسيق الرسالة"""
        return text
    
    def build_inline_buttons(self, task_id):
        """بناء الأزرار الإنلاين"""
        return None
    
    def _process_spoiler_entities(self, text):
        """معالجة كيانات الإخفاء"""
        return text, None
    
    async def _process_media(self, media, user_id):
        """معالجة الوسائط"""
        return media, "media_file.jpg"
    
    async def _apply_sending_interval(self, task_id):
        """تطبيق فاصل الإرسال"""
        pass
    
    async def _handle_manual_approval(self, message, task, user_id, client):
        """معالجة الموافقة اليدوية"""
        pass

# إنشاء مثيل عام
userbot_instance = UserBotService()