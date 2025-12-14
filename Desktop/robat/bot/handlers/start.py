"""
Start command handler
"""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from bot.utils.messages import get_start_command_message

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    """
    Handle /start command
    
    Args:
        message: Telegram message object
    """
    await message.answer(get_start_command_message())


