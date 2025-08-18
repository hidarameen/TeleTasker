"""
Simple Telegram Bot using Telethon
Handles bot API and user API functionality
"""
import logging
import asyncio
from telethon import TelegramClient, events
from telethon.tl.custom import Button
from telethon.sessions import StringSession
from database import get_database
from userbot_service.userbot import userbot_instance
from bot_package.config import BOT_TOKEN, API_ID, API_HASH
import json
import time
import os
from datetime import datetime
from channels_management import ChannelsManagement

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class SimpleTelegramBot:
    def __init__(self):
        # استخدام مصنع قاعدة البيانات
        self.db = get_database()
        
        # معلومات قاعدة البيانات
        from database import DatabaseFactory
        self.db_info = DatabaseFactory.get_database_info()
        
        logger.info(f"🗄️ تم تهيئة قاعدة البيانات: {self.db_info['name']}")
        
        self.bot = None
        self.conversation_states = {}
        self.user_states = {}  # For handling user input states
        self.user_messages = {}  # Track user messages for editing: {user_id: {message_id, chat_id, timestamp}}
        
        # تهيئة مدير وضع النشر
        from .publishing_mode_manager import PublishingModeManager
        self.publishing_manager = PublishingModeManager(self)
        # تهيئة إدارة القنوات
        self.channels_mgmt = ChannelsManagement(self)

    def set_user_state(self, user_id, state, data=None):
        """Set user conversation state"""
        self.user_states[user_id] = {'state': state, 'data': data or {}}
    
    def get_user_state(self, user_id):
        """Get user conversation state"""
        return self.user_states.get(user_id, {}).get('state', None)
        
    def get_user_data(self, user_id):
        """Get user conversation data"""
        return self.user_states.get(user_id, {}).get('data', {})
    
    def clear_user_state(self, user_id):
        """Clear user conversation state"""
        self.user_states.pop(user_id, None)

    def track_user_message(self, user_id, message_id, chat_id):
        """Track a message sent to user for potential editing"""
        self.user_messages[user_id] = {
            'message_id': message_id,
            'chat_id': chat_id,
            'timestamp': time.time()
        }

    def get_user_message(self, user_id):
        """Get the last message sent to user"""
        return self.user_messages.get(user_id)

    def clear_user_message(self, user_id):
        """Clear tracked message for user"""
        self.user_messages.pop(user_id, None)

    async def delete_previous_message(self, user_id):
        """Delete the previous tracked message for user"""
        if user_id in self.user_messages:
            try:
                msg_info = self.user_messages[user_id]
                await self.bot.delete_messages(msg_info['chat_id'], msg_info['message_id'])
            except Exception:
                pass