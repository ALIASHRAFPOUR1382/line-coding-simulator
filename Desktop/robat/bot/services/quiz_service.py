"""
Quiz service for quiz logic and scoring
"""

import logging
from typing import List, Optional
from datetime import datetime
from bot.database.db_manager import DatabaseManager
from bot.database.models import QuizQuestion, QuizSession, QuizResult

logger = logging.getLogger(__name__)


class QuizService:
    """Service for quiz-related operations"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
    
    async def get_active_questions(self) -> List[QuizQuestion]:
        """
        Get all active quiz questions
        
        Returns:
            List of active quiz questions
        """
        return await self.db_manager.get_active_quiz_questions()
    
    async def get_question_by_id(self, question_id: int) -> Optional[QuizQuestion]:
        """
        Get quiz question by ID
        
        Args:
            question_id: Question ID
            
        Returns:
            QuizQuestion or None if not found
        """
        return await self.db_manager.get_quiz_question_by_id(question_id)
    
    async def create_quiz_session(self) -> QuizSession:
        """
        Create a new quiz session
        
        Returns:
            Created QuizSession
        """
        # Generate week_id based on current date
        week_id = f"week_{datetime.now().strftime('%Y_%W')}"
        
        # Check if session already exists
        existing = await self.db_manager.get_quiz_session_by_week_id(week_id)
        if existing:
            return existing
        
        return await self.db_manager.create_quiz_session(week_id)
    
    async def get_active_session(self) -> Optional[QuizSession]:
        """
        Get currently active quiz session
        
        Returns:
            Active QuizSession or None
        """
        return await self.db_manager.get_active_quiz_session()
    
    async def end_quiz_session(self, week_id: str) -> bool:
        """
        End a quiz session
        
        Args:
            week_id: Week ID of the session to end
            
        Returns:
            True if successful, False otherwise
        """
        return await self.db_manager.end_quiz_session(week_id)
    
    async def save_user_answer(
        self,
        user_id: int,
        quiz_week_id: str,
        question_id: int,
        answer: str
    ) -> bool:
        """
        Save user's answer to a question
        
        Args:
            user_id: Telegram user ID
            quiz_week_id: Quiz week ID
            question_id: Question ID
            answer: User's answer (a, b, c, or d)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            await self.db_manager.save_user_answer(
                user_id=user_id,
                quiz_week_id=quiz_week_id,
                question_id=question_id,
                user_answer=answer
            )
            return True
        except Exception as e:
            logger.error(f"Error saving user answer: {e}")
            return False
    
    async def calculate_and_save_score(
        self,
        user_id: int,
        quiz_week_id: str
    ) -> Optional[QuizResult]:
        """
        Calculate user's score for a quiz and save it
        
        Args:
            user_id: Telegram user ID
            quiz_week_id: Quiz week ID
            
        Returns:
            QuizResult or None if calculation failed
        """
        try:
            # Get all user answers for this quiz
            user_answers = await self.db_manager.get_user_answers_for_quiz(
                user_id=user_id,
                quiz_week_id=quiz_week_id
            )
            
            if not user_answers:
                logger.warning(f"No answers found for user {user_id} in quiz {quiz_week_id}")
                return None
            
            # Get all questions for this quiz
            questions = await self.db_manager.get_active_quiz_questions()
            
            # Create a dictionary of question_id -> correct_answer
            correct_answers = {q.id: q.correct_answer for q in questions}
            
            # Calculate score
            score = 0
            total_questions = len(questions)
            
            for answer in user_answers:
                correct_answer = correct_answers.get(answer.question_id)
                if correct_answer and answer.user_answer.lower() == correct_answer.lower():
                    score += 1
            
            # Save result
            result = await self.db_manager.save_quiz_result(
                user_id=user_id,
                score=score,
                total_questions=total_questions,
                quiz_week_id=quiz_week_id
            )
            
            logger.info(f"Score calculated for user {user_id}: {score}/{total_questions}")
            return result
            
        except Exception as e:
            logger.error(f"Error calculating score: {e}")
            return None
    
    async def get_top_winners(self, quiz_week_id: str, limit: int = 3) -> List[tuple]:
        """
        Get top winners for a quiz
        
        Args:
            quiz_week_id: Quiz week ID
            limit: Number of top winners to return
            
        Returns:
            List of tuples (user_id, score, username, first_name)
        """
        return await self.db_manager.get_top_quiz_results(quiz_week_id, limit)
    
    async def user_has_completed_quiz(self, user_id: int, quiz_week_id: str) -> bool:
        """
        Check if user has already completed a quiz
        
        Args:
            user_id: Telegram user ID
            quiz_week_id: Quiz week ID
            
        Returns:
            True if user has completed, False otherwise
        """
        return await self.db_manager.user_has_completed_quiz(user_id, quiz_week_id)


