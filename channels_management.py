#!/usr/bin/env python3
"""
دوال إدارة القنوات
"""

import json
import logging
from datetime import datetime
from telethon import Button

logger = logging.getLogger(__name__)

class ChannelsManagement:
	"""إدارة القنوات"""
	
	def __init__(self, bot):
		self.bot = bot
		self.db = bot.db

	async def show_channels_menu(self, event):
		"""Show channels management menu"""
		user_id = event.sender_id
		
		# Check if user is authenticated
		if not self.db.is_user_authenticated(user_id):
			await self.bot.edit_or_send_message(event, "❌ يجب تسجيل الدخول أولاً لإدارة القنوات")
			return

		# Get channels count
		channels = self.db.get_user_channels(user_id)
		channels_count = len(channels)
		admin_channels = len([c for c in channels if c.get('is_admin', False)])
		member_channels = channels_count - admin_channels

		buttons = [
			[Button.inline("➕ إضافة قناة", b"add_channel")],
			[Button.inline("📋 قائمة القنوات", b"list_channels")],
			[Button.inline("📤 إضافة عدة قنوات", b"add_multiple_channels")],
			[Button.inline("🔙 رجوع لإدارة المهام", b"manage_tasks")]
		]

		message_text = (
			f"📺 إدارة القنوات\n\n"
			f"📊 الإحصائيات:\n"
			f"• إجمالي القنوات: {channels_count}\n"
			f"• قنوات مشرف: {admin_channels}\n"
			f"• قنوات عضو: {member_channels}\n\n"
			f"💡 الميزات:\n"
			f"• إضافة قناة واحدة أو عدة قنوات دفعة واحدة\n"
			f"• عرض قائمة القنوات مع الصلاحيات\n"
			f"• استخدام القنوات كمصادر أو أهداف في المهام\n"
			f"• عرض أسماء القنوات بدلاً من الأرقام\n\n"
			f"اختر إجراء:"
		)
		
		await self.bot.edit_or_send_message(event, message_text, buttons=buttons)

	async def start_add_channel(self, event):
		"""Start adding a single channel"""
		user_id = event.sender_id

		# Check if user is authenticated
		if not self.db.is_user_authenticated(user_id):
			await self.bot.edit_or_send_message(event, "❌ يجب تسجيل الدخول أولاً لإضافة قنوات")
			return

		# Set conversation state
		self.db.set_conversation_state(user_id, 'waiting_channel_link', json.dumps({}))

		buttons = [
			[Button.inline("❌ إلغاء", b"manage_channels")]
		]

		message_text = (
			"➕ إضافة قناة جديدة\n\n"
			"📋 **الخطوة 1: إرسال رابط القناة**\n\n"
			"أرسل رابط القناة التي تريد إضافتها:\n\n"
			"• رابط القناة: (مثال: https://t.me/channel_name)\n"
			"• أو معرف القناة: (مثال: @channel_name)\n"
			"• أو رقم القناة: (مثال: -1001234567890)\n\n"
			"💡 ملاحظة: يجب أن تكون عضو في القناة أو مشرف عليها"
		)
		
		await self.bot.edit_or_send_message(event, message_text, buttons=buttons)

	async def start_add_multiple_channels(self, event):
		"""Start adding multiple channels"""
		user_id = event.sender_id

		# Check if user is authenticated
		if not self.db.is_user_authenticated(user_id):
			await self.bot.edit_or_send_message(event, "❌ يجب تسجيل الدخول أولاً لإضافة قنوات")
			return

		# Set conversation state
		self.db.set_conversation_state(user_id, 'waiting_multiple_channels', json.dumps({'channels': []}))

		buttons = [
			[Button.inline("✅ إنهاء الإضافة", b"finish_add_channels")],
			[Button.inline("❌ إلغاء", b"manage_channels")]
		]

		message_text = (
			"📤 إضافة عدة قنوات دفعة واحدة\n\n"
			"📋 **الخطوة 1: إرسال روابط القنوات**\n\n"
			"أرسل روابط القنوات واحداً تلو الآخر:\n\n"
			"• رابط القناة: (مثال: https://t.me/channel_name)\n"
			"• أو معرف القناة: (مثال: @channel_name)\n"
			"• أو رقم القناة: (مثال: -1001234567890)\n\n"
			"💡 ملاحظات:\n"
			"• أرسل رابط واحد في كل رسالة\n"
			"• اضغط 'إنهاء الإضافة' عند الانتهاء\n"
			"• يجب أن تكون عضو في القنوات أو مشرف عليها"
		)
		
		await self.bot.edit_or_send_message(event, message_text, buttons=buttons)

	async def list_channels(self, event):
		"""List user channels"""
		user_id = event.sender_id

		# Check if user is authenticated
		if not self.db.is_user_authenticated(user_id):
			await self.bot.edit_or_send_message(event, "❌ يجب تسجيل الدخول أولاً لعرض القنوات")
			return

		channels = self.db.get_user_channels(user_id)

		if not channels:
			buttons = [
				[Button.inline("➕ إضافة قناة", b"add_channel")],
				[Button.inline("🔙 رجوع لإدارة القنوات", b"manage_channels")]
			]

			message_text = (
				"📋 قائمة القنوات\n\n"
				"❌ لا توجد قنوات مضافة حالياً\n\n"
				"أضف قنواتك الأولى للبدء!"
			)
			
			await self.bot.edit_or_send_message(event, message_text, buttons=buttons)
			return

		# Build channels list
		message = "📋 قائمة القنوات:\n\n"
		buttons = []

		for i, channel in enumerate(channels[:10], 1):  # Show max 10 channels
			channel_id = channel.get('chat_id', 'غير محدد')
			channel_name = channel.get('chat_name', f'قناة {channel_id}')
			is_admin = channel.get('is_admin', False)
			status_icon = "👑" if is_admin else "👤"
			status_text = "مشرف" if is_admin else "عضو"

			message += (
				f"{i}. {status_icon} **{channel_name}**\n"
				f"   📊 الصلاحية: {status_text}\n"
				f"   🆔 المعرف: `{channel_id}`\n\n"
			)

			# Add action buttons for each channel
			buttons.append([
				Button.inline(f"🗑️ حذف {i}", f"delete_channel_{channel_id}".encode()),
				Button.inline(f"✏️ تعديل {i}", f"edit_channel_{channel_id}".encode())
			])

		# Add navigation buttons
		if len(channels) > 10:
			message += f"\n📄 عرض 1-10 من {len(channels)} قناة"
			buttons.append([Button.inline("📄 الصفحة التالية", b"channels_next_page")])

		buttons.extend([
			[Button.inline("➕ إضافة قناة", b"add_channel")],
			[Button.inline("🔙 رجوع لإدارة القنوات", b"manage_channels")]
		])

		await self.bot.edit_or_send_message(event, message, buttons=buttons)

	async def delete_channel(self, event, channel_id):
		"""Delete a specific channel"""
		user_id = event.sender_id
		
		try:
			# Get channel info before deletion
			channel = self.db.get_channel_info(channel_id, user_id)
			if not channel:
				await event.answer("❌ القناة غير موجودة")
				return

			channel_name = channel.get('chat_name', f'قناة {channel_id}')
			
			# Delete channel
			success = self.db.delete_channel(channel_id, user_id)
			
			if success:
				await event.answer(f"✅ تم حذف القناة: {channel_name}")
				# Refresh channels list
				await self.list_channels(event)
			else:
				await event.answer("❌ فشل في حذف القناة")
				
		except Exception as e:
			logger.error(f"❌ خطأ في حذف القناة: {e}")
			await event.answer("❌ حدث خطأ في حذف القناة")

	async def edit_channel(self, event, channel_id):
		"""Edit channel information"""
		user_id = event.sender_id
		
		try:
			# Get channel info
			channel = self.db.get_channel_info(channel_id, user_id)
			if not channel:
				await event.answer("❌ القناة غير موجودة")
				return

			channel_name = channel.get('chat_name', f'قناة {channel_id}')
			is_admin = channel.get('is_admin', False)
			status_icon = "👑" if is_admin else "👤"
			status_text = "مشرف" if is_admin else "عضو"

			buttons = [
				[Button.inline("🔄 تحديث المعلومات", f"refresh_channel_{channel_id}".encode())],
				[Button.inline("🗑️ حذف القناة", f"delete_channel_{channel_id}".encode())],
				[Button.inline("🔙 رجوع لقائمة القنوات", b"list_channels")]
			]

			message_text = (
				f"✏️ تعديل القناة\n\n"
				f"📺 **{channel_name}**\n"
				f"📊 الصلاحية: {status_icon} {status_text}\n"
				f"🆔 المعرف: `{channel_id}`\n\n"
				f"اختر إجراء:"
			)

			await self.bot.edit_or_send_message(event, message_text, buttons=buttons)
				
		except Exception as e:
			logger.error(f"❌ خطأ في تعديل القناة: {e}")
			await event.answer("❌ حدث خطأ في تعديل القناة")

	async def refresh_channel_info(self, event, channel_id):
		"""Refresh channel information from Telegram"""
		user_id = event.sender_id
		
		try:
			# Get updated channel info from Telegram
			from userbot_service.userbot import userbot_instance
			
			if user_id not in userbot_instance.clients:
				await event.answer("❌ UserBot غير متصل. يرجى إعادة تسجيل الدخول")
				return

			client = userbot_instance.clients[user_id]
			
			# Try to get channel info
			try:
				chat = await client.get_entity(int(channel_id))
				new_name = getattr(chat, 'title', None) or getattr(chat, 'username', None) or str(channel_id)
				
				# Update channel info in database
				success = self.db.update_channel_info(channel_id, user_id, {
					'chat_name': new_name,
					'username': getattr(chat, 'username', None),
					'updated_at': datetime.now().isoformat()
				})
				
				if success:
					await event.answer(f"✅ تم تحديث معلومات القناة: {new_name}")
					# Refresh channel edit page
					await self.edit_channel(event, channel_id)
				else:
					await event.answer("❌ فشل في تحديث معلومات القناة")
					
			except Exception as e:
				logger.error(f"❌ خطأ في الحصول على معلومات القناة من Telegram: {e}")
				await event.answer("❌ لا يمكن الوصول للقناة. تأكد من أنك عضو فيها")
				
		except Exception as e:
			logger.error(f"❌ خطأ في تحديث معلومات القناة: {e}")
			await event.answer("❌ حدث خطأ في تحديث معلومات القناة")

	async def finish_add_channels(self, event):
		"""Finish adding multiple channels"""
		user_id = event.sender_id
		
		try:
			# Get current state (tuple)
			state_tuple = self.db.get_conversation_state(user_id)
			if not state_tuple:
				await event.answer("❌ لا توجد عملية إضافة قنوات نشطة")
				return

			state, data_str = state_tuple
			if state != 'waiting_multiple_channels':
				await event.answer("❌ لا توجد عملية إضافة قنوات نشطة")
				return

			try:
				data_json = json.loads(data_str) if data_str else {}
			except Exception:
				data_json = {}

			channels = data_json.get('channels', [])
			
			if not channels:
				await event.answer("❌ لم يتم إضافة أي قنوات")
				# Clear state and return to channels menu
				self.db.clear_conversation_state(user_id)
				await self.show_channels_menu(event)
				return

			# Clear state
			self.db.clear_conversation_state(user_id)
			
			# Show summary
			buttons = [
				[Button.inline("📋 عرض القنوات", b"list_channels")],
				[Button.inline("➕ إضافة المزيد", b"add_channel")],
				[Button.inline("🔙 رجوع لإدارة القنوات", b"manage_channels")]
			]

			message_text = (
				f"✅ تم إضافة {len(channels)} قناة بنجاح!\n\n"
				f"📋 القنوات المضافة:\n"
			)
			
			for i, channel in enumerate(channels[:5], 1):  # Show first 5
				channel_name = channel.get('chat_name', f"قناة {channel.get('chat_id')}")
				message_text += f"{i}. {channel_name}\n"
			
			if len(channels) > 5:
				message_text += f"... و {len(channels) - 5} قناة أخرى\n"
			
			message_text += "\nاختر إجراء:"

			await self.bot.edit_or_send_message(event, message_text, buttons=buttons)
				
		except Exception as e:
			logger.error(f"❌ خطأ في إنهاء إضافة القنوات: {e}")
			await event.answer("❌ حدث خطأ في إنهاء إضافة القنوات")

	async def process_channel_link(self, event, channel_link):
		"""Process channel link and add to database"""
		user_id = event.sender_id
		
		try:
			# Get UserBot client
			from userbot_service.userbot import userbot_instance
			
			if user_id not in userbot_instance.clients:
				await event.answer("❌ UserBot غير متصل. يرجى إعادة تسجيل الدخول")
				return False

			client = userbot_instance.clients[user_id]
			
			# Parse channel link
			channel_id = None
			channel_name = None
			username = None
			
			try:
				# Try to get entity from link
				chat = await client.get_entity(channel_link)
				channel_id = chat.id
				channel_name = getattr(chat, 'title', None) or getattr(chat, 'username', None) or str(channel_id)
				username = getattr(chat, 'username', None)
				
				# Check if user is member/admin
				participant = await client.get_participants(chat, filter='all')
				user_participant = None
				
				for p in participant:
					if p.id == user_id:
						user_participant = p
						break
				
				if not user_participant:
					await event.answer("❌ يجب أن تكون عضو في القناة أو مشرف عليها")
					return False
				
				is_admin = getattr(user_participant, 'admin_rights', None) is not None
				
			except Exception as e:
				logger.error(f"❌ خطأ في الحصول على معلومات القناة: {e}")
				await event.answer("❌ لا يمكن الوصول للقناة. تأكد من صحة الرابط وأنك عضو فيها")
				return False
			
			# Add channel to database
			success = self.db.add_channel(user_id, channel_id, channel_name, username, is_admin)
			
			if success:
				status_text = "مشرف" if is_admin else "عضو"
				await event.answer(f"✅ تم إضافة القناة: {channel_name} ({status_text})")
				return {
					'chat_id': channel_id,
					'chat_name': channel_name,
					'username': username,
					'is_admin': is_admin
				}
			else:
				await event.answer("❌ فشل في إضافة القناة. قد تكون مضافة مسبقاً")
				return False
				
		except Exception as e:
			logger.error(f"❌ خطأ في معالجة رابط القناة: {e}")
			await event.answer("❌ حدث خطأ في معالجة رابط القناة")
			return False

	async def show_channel_selection(self, event, task_id, selection_type):
		"""Show channel selection for sources/targets with multi-select"""
		user_id = event.sender_id

		# Normalize selection key and back button
		selection_key = 'source' if selection_type in ('source', 'مصدر') else 'target'
		back_button = f"manage_sources_{task_id}" if selection_key == 'source' else f"manage_targets_{task_id}"

		# Check if user is authenticated
		if not self.db.is_user_authenticated(user_id):
			await event.answer("❌ يجب تسجيل الدخول أولاً")
			return

		channels = self.db.get_user_channels(user_id)

		if not channels:
			buttons = [
				[Button.inline("➕ إضافة قناة", b"add_channel")],
				[Button.inline("🔙 رجوع", back_button.encode())]
			]

			message_text = (
				f"📺 اختيار {selection_type}\n\n"
				f"❌ لا توجد قنوات مضافة حالياً\n\n"
				f"أضف قنواتك أولاً لاستخدامها ك{selection_type}"
			)
			
			await self.bot.edit_or_send_message(event, message_text, buttons=buttons)
			return

		# Build channel selection list
		message = f"📺 اختر {selection_type}:\n\n"
		buttons = []

		for i, channel in enumerate(channels, 1):
			channel_id = channel.get('chat_id', 'غير محدد')
			channel_name = channel.get('chat_name', f'قناة {channel_id}')
			is_admin = channel.get('is_admin', False)
			status_icon = "👑" if is_admin else "👤"

			message += f"{i}. {status_icon} {channel_name}\n"
			buttons.append([
				Button.inline(
					f"اختيار {i}",
					f"toggle_select_channel_{selection_key}_{channel_id}_{task_id}".encode()
				)
			])

		# Add action and navigation buttons
		buttons.append([Button.inline("✅ تأكيد الاختيار", f"confirm_selected_channels_{selection_key}_{task_id}".encode())])
		buttons.append([Button.inline("🔄 مسح الاختيار", f"clear_selected_channels_{selection_key}_{task_id}".encode())])
		buttons.append([Button.inline("🔙 رجوع", back_button.encode())])

		await self.bot.edit_or_send_message(event, message, buttons=buttons)