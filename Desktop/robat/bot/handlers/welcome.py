"""
Welcome handler for new channel members
"""

import logging
from aiogram import Router, F
from aiogram.types import Message, ChatMemberUpdated
from aiogram.filters import ChatMemberUpdatedFilter
from aiogram.enums import ChatMemberStatus

from bot.database.db_manager import DatabaseManager
from bot.utils.messages import get_welcome_message
from bot.keyboards.inline import get_category_selection_keyboard

router = Router()
logger = logging.getLogger(__name__)
db_manager = DatabaseManager()


@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=ChatMemberStatus.MEMBER))
async def on_new_member(event: ChatMemberUpdated):
    """
    Handle new member joining the channel
    
    Args:
        event: Chat member update event
    """
    try:
        new_member = event.new_chat_member.user
        
        # Skip if the new member is the bot itself
        if new_member.is_bot:
            return
        
        # Get channel information
        chat = event.chat
        
        # Create or update user in database
        await db_manager.create_user(
            user_id=new_member.id,
            username=new_member.username,
            first_name=new_member.first_name
        )
        
        # Send welcome message with category selection
        welcome_text = get_welcome_message()
        keyboard = get_category_selection_keyboard()
        
        # Try to send private message to user
        try:
            await event.bot.send_message(
                chat_id=new_member.id,
                text=welcome_text,
                reply_markup=keyboard
            )
            logger.info(f"Welcome message sent to user {new_member.id}")
        except Exception as e:
            logger.warning(f"Could not send private message to user {new_member.id}: {e}")
            # If private message fails, we'll handle it via callback when user interacts with bot
            
    except Exception as e:
        logger.error(f"Error handling new member: {e}")

