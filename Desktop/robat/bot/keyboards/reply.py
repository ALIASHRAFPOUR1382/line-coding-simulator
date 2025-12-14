"""
Reply keyboard builders (if needed in future)
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """
    Create main menu reply keyboard (for future use)
    
    Returns:
        ReplyKeyboardMarkup with main menu options
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 وضعیت من")],
            [KeyboardButton(text="📚 منابع آموزشی")]
        ],
        resize_keyboard=True
    )
    return keyboard


