"""
Broadcast service for sending messages to all users
"""

import logging
from typing import List
from aiogram import Bot
from bot.database.db_manager import DatabaseManager

logger = logging.getLogger(__name__)


class BroadcastService:
    """Service for broadcasting messages to all users"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
    
    async def broadcast_message(self, bot: Bot, message_text: str) -> dict:
        """
        Broadcast a message to all registered users
        
        Args:
            bot: Bot instance
            message_text: Message text to broadcast
            
        Returns:
            Dictionary with success and failure counts
        """
        users = await self.db_manager.get_all_users()
        success_count = 0
        failure_count = 0
        
        for user in users:
            try:
                await bot.send_message(
                    chat_id=user.user_id,
                    text=message_text
                )
                success_count += 1
                logger.info(f"Broadcast message sent to user {user.user_id}")
            except Exception as e:
                failure_count += 1
                logger.warning(f"Failed to send broadcast to user {user.user_id}: {e}")
        
        return {
            "success": success_count,
            "failure": failure_count,
            "total": len(users)
        }


