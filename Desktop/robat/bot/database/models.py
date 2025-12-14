"""
Database models and schema definitions
"""

from typing import Optional
from datetime import datetime


class User:
    """User model representing a Telegram user"""
    
    def __init__(
        self,
        user_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        category: Optional[str] = None,
        joined_at: Optional[datetime] = None,
        id: Optional[int] = None
    ):
        self.id = id
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.category = category  # 'student_6', 'student_9', 'parent', 'teacher', None
        self.joined_at = joined_at or datetime.now()


class QuizQuestion:
    """Quiz question model"""
    
    def __init__(
        self,
        question_text: str,
        option_a: str,
        option_b: str,
        option_c: str,
        option_d: str,
        correct_answer: str,
        is_active: bool = True,
        id: Optional[int] = None
    ):
        self.id = id
        self.question_text = question_text
        self.option_a = option_a
        self.option_b = option_b
        self.option_c = option_c
        self.option_d = option_d
        self.correct_answer = correct_answer.lower()  # 'a', 'b', 'c', 'd'
        self.is_active = is_active


class QuizSession:
    """Quiz session model for tracking active quizzes"""
    
    def __init__(
        self,
        week_id: str,
        status: str = 'active',  # 'active', 'ended'
        started_at: Optional[datetime] = None,
        ended_at: Optional[datetime] = None,
        id: Optional[int] = None
    ):
        self.id = id
        self.week_id = week_id
        self.status = status
        self.started_at = started_at or datetime.now()
        self.ended_at = ended_at


class QuizResult:
    """Quiz result model for storing user scores"""
    
    def __init__(
        self,
        user_id: int,
        score: int,
        total_questions: int,
        quiz_week_id: str,
        quiz_date: Optional[datetime] = None,
        id: Optional[int] = None
    ):
        self.id = id
        self.user_id = user_id
        self.score = score
        self.total_questions = total_questions
        self.quiz_week_id = quiz_week_id
        self.quiz_date = quiz_date or datetime.now()


class UserQuizAnswer:
    """Individual user answer for a quiz question"""
    
    def __init__(
        self,
        user_id: int,
        quiz_week_id: str,
        question_id: int,
        user_answer: str,
        answered_at: Optional[datetime] = None,
        id: Optional[int] = None
    ):
        self.id = id
        self.user_id = user_id
        self.quiz_week_id = quiz_week_id
        self.question_id = question_id
        self.user_answer = user_answer.lower()  # 'a', 'b', 'c', 'd'
        self.answered_at = answered_at or datetime.now()


