"""
Quiz handlers with FSM for quiz flow
"""

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.services.quiz_service import QuizService
from bot.utils.messages import (
    get_quiz_question_message,
    get_quiz_completion_message
)
from bot.keyboards.inline import get_quiz_answer_keyboard
from bot.utils.validators import validate_answer_choice

router = Router()
logger = logging.getLogger(__name__)
quiz_service = QuizService()


class QuizStates(StatesGroup):
    """FSM states for quiz flow"""
    waiting_for_answer = State()
    quiz_in_progress = State()


@router.callback_query(F.data == "start_quiz_user")
async def start_quiz_for_user(callback: CallbackQuery, state: FSMContext):
    """
    Start quiz for a user when they click start button
    
    Args:
        callback: Callback query object
        state: FSM context
    """
    try:
        user_id = callback.from_user.id
        
        # Get active quiz session
        session = await quiz_service.get_active_session()
        if not session:
            await callback.answer("در حال حاضر کوئیز فعالی وجود ندارد.", show_alert=True)
            return
        
        # Check if user has already completed this quiz
        if await quiz_service.user_has_completed_quiz(user_id, session.week_id):
            await callback.answer("شما قبلاً در این کوئیز شرکت کرده‌اید.", show_alert=True)
            return
        
        # Get all questions
        questions = await quiz_service.get_active_questions()
        if not questions:
            await callback.answer("سوالی برای نمایش وجود ندارد.", show_alert=True)
            return
        
        # Initialize quiz state
        await state.set_state(QuizStates.quiz_in_progress)
        await state.update_data(
            quiz_week_id=session.week_id,
            questions=questions,
            current_question_index=0,
            answers={}
        )
        
        # Send first question
        await send_question(callback.message, state, questions[0], 0, len(questions))
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error starting quiz for user: {e}")
        await callback.answer("خطایی در شروع کوئیز رخ داد.", show_alert=True)


async def send_question(
    message: Message,
    state: FSMContext,
    question,
    question_index: int,
    total_questions: int
):
    """
    Send a quiz question to user
    
    Args:
        message: Message object to edit or send
        state: FSM context
        question: QuizQuestion object
        question_index: Current question index (0-based)
        total_questions: Total number of questions
    """
    question_text = f"""{question.question_text}

گزینه الف: {question.option_a}
گزینه ب: {question.option_b}
گزینه ج: {question.option_c}
گزینه د: {question.option_d}"""
    
    message_text = get_quiz_question_message(
        question_number=question_index + 1,
        total_questions=total_questions,
        question_text=question_text
    )
    
    keyboard = get_quiz_answer_keyboard(question.id)
    
    if question_index == 0:
        # First question - send new message
        await message.answer(message_text, reply_markup=keyboard)
    else:
        # Subsequent questions - edit previous message
        try:
            await message.edit_text(message_text, reply_markup=keyboard)
        except Exception:
            # If edit fails, send new message
            await message.answer(message_text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("quiz_answer_"), QuizStates.quiz_in_progress)
async def handle_quiz_answer(callback: CallbackQuery, state: FSMContext):
    """
    Handle user's answer to a quiz question
    
    Args:
        callback: Callback query object
        state: FSM context
    """
    try:
        # Parse callback data: quiz_answer_{question_id}_{answer}
        parts = callback.data.split("_")
        if len(parts) < 4:
            await callback.answer("پاسخ نامعتبر است.", show_alert=True)
            return
        
        question_id = int(parts[2])
        answer = parts[3]
        
        if not validate_answer_choice(answer):
            await callback.answer("پاسخ نامعتبر است.", show_alert=True)
            return
        
        # Get state data
        data = await state.get_data()
        quiz_week_id = data.get("quiz_week_id")
        questions = data.get("questions")
        current_index = data.get("current_question_index", 0)
        answers = data.get("answers", {})
        
        if not quiz_week_id or not questions:
            await callback.answer("خطا در دریافت اطلاعات کوئیز.", show_alert=True)
            return
        
        # Save answer
        await quiz_service.save_user_answer(
            user_id=callback.from_user.id,
            quiz_week_id=quiz_week_id,
            question_id=question_id,
            answer=answer
        )
        
        # Store answer in state
        answers[question_id] = answer
        await state.update_data(answers=answers)
        
        # Move to next question
        next_index = current_index + 1
        
        if next_index < len(questions):
            # Send next question
            await state.update_data(current_question_index=next_index)
            next_question = questions[next_index]
            await send_question(
                callback.message,
                state,
                next_question,
                next_index,
                len(questions)
            )
            await callback.answer("پاسخ شما ثبت شد. ✅")
        else:
            # Quiz completed - calculate score
            await callback.answer("در حال محاسبه نتیجه...", show_alert=False)
            
            # Calculate and save score
            result = await quiz_service.calculate_and_save_score(
                user_id=callback.from_user.id,
                quiz_week_id=quiz_week_id
            )
            
            if result:
                # Send completion message
                completion_message = get_quiz_completion_message(
                    score=result.score,
                    total_questions=result.total_questions
                )
                await callback.message.edit_text(completion_message)
            else:
                await callback.message.edit_text(
                    "خطا در محاسبه نتیجه. لطفاً با ادمین تماس بگیرید."
                )
            
            # Clear state
            await state.clear()
            logger.info(f"Quiz completed for user {callback.from_user.id}")
        
    except Exception as e:
        logger.error(f"Error handling quiz answer: {e}")
        await callback.answer("خطایی در ثبت پاسخ رخ داد.", show_alert=True)


