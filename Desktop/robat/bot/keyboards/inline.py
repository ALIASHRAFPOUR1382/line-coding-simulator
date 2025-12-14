"""
Inline keyboard builders
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_category_selection_keyboard() -> InlineKeyboardMarkup:
    """
    Create inline keyboard for user category selection
    
    Returns:
        InlineKeyboardMarkup with category options
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🎒 دانش‌آموز پایه ششم",
                callback_data="category_student_6"
            )
        ],
        [
            InlineKeyboardButton(
                text="🎓 دانش‌آموز پایه نهم",
                callback_data="category_student_9"
            )
        ],
        [
            InlineKeyboardButton(
                text="👨‍👩‍👧‍👦 والدین گرامی",
                callback_data="category_parent"
            )
        ],
        [
            InlineKeyboardButton(
                text="👩‍🏫 معلم / مشاور",
                callback_data="category_teacher"
            )
        ]
    ])
    return keyboard


def get_quiz_start_keyboard() -> InlineKeyboardMarkup:
    """
    Create inline keyboard for starting quiz
    
    Returns:
        InlineKeyboardMarkup with start quiz button
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="شروع آزمون",
                callback_data="start_quiz_user"
            )
        ]
    ])
    return keyboard


def get_quiz_answer_keyboard(question_id: int) -> InlineKeyboardMarkup:
    """
    Create inline keyboard for quiz question answers
    
    Args:
        question_id: ID of the current question
        
    Returns:
        InlineKeyboardMarkup with answer options
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="گزینه الف",
                callback_data=f"quiz_answer_{question_id}_a"
            ),
            InlineKeyboardButton(
                text="گزینه ب",
                callback_data=f"quiz_answer_{question_id}_b"
            )
        ],
        [
            InlineKeyboardButton(
                text="گزینه ج",
                callback_data=f"quiz_answer_{question_id}_c"
            ),
            InlineKeyboardButton(
                text="گزینه د",
                callback_data=f"quiz_answer_{question_id}_d"
            )
        ]
    ])
    return keyboard


