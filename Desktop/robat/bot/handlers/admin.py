"""
Admin command handlers
"""

import logging
import re
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from datetime import datetime

from bot.config import Config
from bot.services.quiz_service import QuizService
from bot.services.broadcast_service import BroadcastService
from bot.utils.messages import (
    get_quiz_announcement_message,
    get_quiz_winners_message,
    get_admin_help_message
)
from bot.keyboards.inline import get_quiz_start_keyboard

router = Router()
logger = logging.getLogger(__name__)
quiz_service = QuizService()
broadcast_service = BroadcastService()


def is_admin(user_id: int) -> bool:
    """
    Check if user is an admin
    
    Args:
        user_id: Telegram user ID
        
    Returns:
        True if admin, False otherwise
    """
    return Config.is_admin(user_id)


@router.message(Command("startquiz"))
async def cmd_start_quiz(message: Message):
    """
    Handle /startquiz command - Start a new quiz session
    
    Args:
        message: Telegram message object
    """
    if not is_admin(message.from_user.id):
        await message.answer("شما دسترسی به این دستور را ندارید.")
        return
    
    try:
        # Check if there's already an active quiz
        active_session = await quiz_service.get_active_session()
        if active_session:
            await message.answer(
                f"یک کوئیز فعال وجود دارد (Week ID: {active_session.week_id}).\n"
                "لطفاً ابتدا کوئیز قبلی را با دستور /endquiz پایان دهید."
            )
            return
        
        # Get active questions
        questions = await quiz_service.get_active_questions()
        if not questions:
            await message.answer(
                "هیچ سوال فعالی در پایگاه داده وجود ندارد.\n"
                "لطفاً ابتدا سوالات را اضافه کنید."
            )
            return
        
        # Create new quiz session
        session = await quiz_service.create_quiz_session()
        
        # Send announcement to channel
        announcement_text = get_quiz_announcement_message()
        keyboard = get_quiz_start_keyboard()
        
        try:
            await message.bot.send_message(
                chat_id=Config.CHANNEL_ID,
                text=announcement_text,
                reply_markup=keyboard
            )
            await message.answer(
                f"✅ کوئیز هفتگی با موفقیت شروع شد!\n"
                f"Week ID: {session.week_id}\n"
                f"تعداد سوالات: {len(questions)}\n"
                f"اعلان در کانال ارسال شد."
            )
            logger.info(f"Quiz started by admin {message.from_user.id}, Week ID: {session.week_id}")
        except Exception as e:
            logger.error(f"Error sending announcement to channel: {e}")
            await message.answer(
                f"❌ خطا در ارسال اعلان به کانال: {e}\n"
                f"کوئیز ایجاد شد اما اعلان ارسال نشد."
            )
            
    except Exception as e:
        logger.error(f"Error starting quiz: {e}")
        await message.answer(f"خطا در شروع کوئیز: {e}")


@router.message(Command("endquiz"))
async def cmd_end_quiz(message: Message):
    """
    Handle /endquiz command - End quiz and announce winners
    
    Args:
        message: Telegram message object
    """
    if not is_admin(message.from_user.id):
        await message.answer("شما دسترسی به این دستور را ندارید.")
        return
    
    try:
        # Get active quiz session
        session = await quiz_service.get_active_session()
        if not session:
            await message.answer("هیچ کوئیز فعالی وجود ندارد.")
            return
        
        # End the session
        success = await quiz_service.end_quiz_session(session.week_id)
        if not success:
            await message.answer("خطا در پایان دادن به کوئیز.")
            return
        
        # Get top winners
        winners = await quiz_service.get_top_winners(session.week_id, limit=3)
        
        if not winners:
            await message.answer(
                f"کوئیز با موفقیت پایان یافت.\n"
                f"هیچ شرکت‌کننده‌ای وجود نداشت."
            )
            return
        
        # Format winners message
        winners_message = get_quiz_winners_message(
            week_id=session.week_id,
            winners=winners
        )
        
        # Send winners announcement to channel
        try:
            await message.bot.send_message(
                chat_id=Config.CHANNEL_ID,
                text=winners_message
            )
            await message.answer(
                f"✅ کوئیز با موفقیت پایان یافت و برندگان اعلام شدند.\n"
                f"Week ID: {session.week_id}\n"
                f"تعداد برندگان: {len(winners)}"
            )
            logger.info(f"Quiz ended by admin {message.from_user.id}, Week ID: {session.week_id}")
        except Exception as e:
            logger.error(f"Error sending winners announcement: {e}")
            await message.answer(
                f"❌ خطا در ارسال اعلان برندگان به کانال: {e}\n"
                f"کوئیز پایان یافت اما اعلان ارسال نشد."
            )
            
    except Exception as e:
        logger.error(f"Error ending quiz: {e}")
        await message.answer(f"خطا در پایان دادن به کوئیز: {e}")


@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message):
    """
    Handle /broadcast command - Send message to all users
    
    Args:
        message: Telegram message object
    """
    if not is_admin(message.from_user.id):
        await message.answer("شما دسترسی به این دستور را ندارید.")
        return
    
    # Extract message text (everything after /broadcast)
    command_text = message.text or message.caption or ""
    parts = command_text.split(maxsplit=1)
    
    if len(parts) < 2:
        await message.answer(
            "لطفاً پیام خود را بعد از دستور /broadcast بنویسید.\n"
            "مثال: /broadcast این یک پیام همگانی است."
        )
        return
    
    broadcast_text = parts[1]
    
    try:
        # Send confirmation
        await message.answer("در حال ارسال پیام به تمام کاربران...")
        
        # Broadcast message
        result = await broadcast_service.broadcast_message(
            bot=message.bot,
            message_text=broadcast_text
        )
        
        await message.answer(
            f"✅ ارسال پیام همگانی انجام شد:\n"
            f"موفق: {result['success']}\n"
            f"ناموفق: {result['failure']}\n"
            f"کل: {result['total']}"
        )
        logger.info(
            f"Broadcast sent by admin {message.from_user.id}: "
            f"{result['success']} successful, {result['failure']} failed"
        )
        
    except Exception as e:
        logger.error(f"Error broadcasting message: {e}")
        await message.answer(f"خطا در ارسال پیام همگانی: {e}")


@router.message(Command("adminhelp"))
async def cmd_admin_help(message: Message):
    """
    Handle /adminhelp command - Show admin help
    
    Args:
        message: Telegram message object
    """
    if not is_admin(message.from_user.id):
        await message.answer("شما دسترسی به این دستور را ندارید.")
        return
    
    await message.answer(get_admin_help_message())


