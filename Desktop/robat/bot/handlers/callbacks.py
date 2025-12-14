"""
Callback query handlers
"""

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.services.user_service import UserService
from bot.utils.messages import get_category_confirmation_message
from bot.utils.validators import validate_category

router = Router()
logger = logging.getLogger(__name__)
user_service = UserService()

# Category display names mapping
CATEGORY_NAMES = {
    'student_6': 'دانش‌آموز پایه ششم',
    'student_9': 'دانش‌آموز پایه نهم',
    'parent': 'والدین گرامی',
    'teacher': 'معلم / مشاور'
}


@router.callback_query(F.data.startswith("category_"))
async def handle_category_selection(callback: CallbackQuery):
    """
    Handle user category selection callback
    
    Args:
        callback: Callback query object
    """
    try:
        # Extract category from callback data
        category = callback.data.replace("category_", "")
        
        if not validate_category(category):
            await callback.answer("دسته‌بندی نامعتبر است.", show_alert=True)
            return
        
        # Get or create user
        user = await user_service.get_or_create_user(
            user_id=callback.from_user.id,
            username=callback.from_user.username,
            first_name=callback.from_user.first_name
        )
        
        # Update user category
        success = await user_service.update_user_category(
            user_id=callback.from_user.id,
            category=category
        )
        
        if success:
            # Get category display name
            category_name = CATEGORY_NAMES.get(category, category)
            
            # Send confirmation message with gift
            confirmation_message = get_category_confirmation_message(category_name)
            await callback.message.edit_text(confirmation_message)
            await callback.answer("اطلاعات شما ثبت شد! ✅", show_alert=False)
            logger.info(f"Category {category} set for user {callback.from_user.id}")
        else:
            await callback.answer("خطا در ثبت اطلاعات. لطفاً دوباره تلاش کنید.", show_alert=True)
            
    except Exception as e:
        logger.error(f"Error handling category selection: {e}")
        await callback.answer("خطایی رخ داد. لطفاً دوباره تلاش کنید.", show_alert=True)


