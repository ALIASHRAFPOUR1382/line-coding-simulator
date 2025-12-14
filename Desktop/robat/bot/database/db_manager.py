"""
Async database manager for all database operations
"""

import aiosqlite
from typing import Optional, List, Tuple
from datetime import datetime
from bot.config import Config
from bot.database.models import (
    User, QuizQuestion, QuizSession, QuizResult, UserQuizAnswer
)


class DatabaseManager:
    """Async database manager for SQLite operations"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Config.DATABASE_PATH
    
    async def get_connection(self):
        """Get async database connection"""
        return await aiosqlite.connect(self.db_path)
    
    @staticmethod
    def _parse_datetime(dt_str: str) -> Optional[datetime]:
        """
        Safely parse datetime string from SQLite
        
        Args:
            dt_str: Datetime string from database
            
        Returns:
            Parsed datetime or None if parsing fails
        """
        if not dt_str:
            return None
        
        try:
            # Try ISO format first
            return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            try:
                # Try SQLite format
                return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
            except (ValueError, AttributeError):
                try:
                    # Try with microseconds
                    return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S.%f')
                except (ValueError, AttributeError):
                    return None
    
    # User operations
    async def create_user(
        self,
        user_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None
    ) -> User:
        """Create a new user in the database"""
        db = await self.get_connection()
        async with db:
            try:
                await db.execute("""
                    INSERT INTO users (user_id, username, first_name)
                    VALUES (?, ?, ?)
                """, (user_id, username, first_name))
                await db.commit()
                return await self.get_user_by_id(user_id)
            except aiosqlite.IntegrityError:
                # User already exists, return existing user
                return await self.get_user_by_id(user_id)
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by Telegram user_id"""
        db = await self.get_connection()
        async with db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM users WHERE user_id = ?", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return User(
                        id=row['id'],
                        user_id=row['user_id'],
                        username=row['username'],
                        first_name=row['first_name'],
                        category=row['category'],
                        joined_at=DatabaseManager._parse_datetime(row['joined_at'])
                    )
                return None
    
    async def update_user_category(self, user_id: int, category: str) -> bool:
        """Update user category"""
        db = await self.get_connection()
        async with db:
            cursor = await db.execute(
                "UPDATE users SET category = ? WHERE user_id = ?",
                (category, user_id)
            )
            await db.commit()
            return cursor.rowcount > 0
    
    async def get_all_users(self) -> List[User]:
        """Get all registered users"""
        db = await self.get_connection()
        async with db:
            db.row_factory = aiosqlite.Row
            users = []
            async with db.execute("SELECT * FROM users") as cursor:
                async for row in cursor:
                    users.append(User(
                        id=row['id'],
                        user_id=row['user_id'],
                        username=row['username'],
                        first_name=row['first_name'],
                        category=row['category'],
                        joined_at=DatabaseManager._parse_datetime(row['joined_at'])
                    ))
            return users
    
    # Quiz question operations
    async def create_quiz_question(
        self,
        question_text: str,
        option_a: str,
        option_b: str,
        option_c: str,
        option_d: str,
        correct_answer: str
    ) -> QuizQuestion:
        """Create a new quiz question"""
        db = await self.get_connection()
        async with db:
            cursor = await db.execute("""
                INSERT INTO quiz_questions 
                (question_text, option_a, option_b, option_c, option_d, correct_answer)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (question_text, option_a, option_b, option_c, option_d, correct_answer.lower()))
            await db.commit()
            question_id = cursor.lastrowid
            return QuizQuestion(
                id=question_id,
                question_text=question_text,
                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,
                correct_answer=correct_answer.lower()
            )
    
    async def get_active_quiz_questions(self) -> List[QuizQuestion]:
        """Get all active quiz questions"""
        db = await self.get_connection()
        async with db:
            db.row_factory = aiosqlite.Row
            questions = []
            async with db.execute(
                "SELECT * FROM quiz_questions WHERE is_active = 1 ORDER BY id"
            ) as cursor:
                async for row in cursor:
                    questions.append(QuizQuestion(
                        id=row['id'],
                        question_text=row['question_text'],
                        option_a=row['option_a'],
                        option_b=row['option_b'],
                        option_c=row['option_c'],
                        option_d=row['option_d'],
                        correct_answer=row['correct_answer'],
                        is_active=bool(row['is_active'])
                    ))
            return questions
    
    async def get_quiz_question_by_id(self, question_id: int) -> Optional[QuizQuestion]:
        """Get quiz question by ID"""
        db = await self.get_connection()
        async with db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM quiz_questions WHERE id = ?", (question_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return QuizQuestion(
                        id=row['id'],
                        question_text=row['question_text'],
                        option_a=row['option_a'],
                        option_b=row['option_b'],
                        option_c=row['option_c'],
                        option_d=row['option_d'],
                        correct_answer=row['correct_answer'],
                        is_active=bool(row['is_active'])
                    )
                return None
    
    # Quiz session operations
    async def create_quiz_session(self, week_id: str) -> QuizSession:
        """Create a new quiz session"""
        db = await self.get_connection()
        async with db:
            await db.execute("""
                INSERT INTO quiz_sessions (week_id, status, started_at)
                VALUES (?, 'active', ?)
            """, (week_id, datetime.now().isoformat()))
            await db.commit()
            return await self.get_quiz_session_by_week_id(week_id)
    
    async def get_quiz_session_by_week_id(self, week_id: str) -> Optional[QuizSession]:
        """Get quiz session by week_id"""
        db = await self.get_connection()
        async with db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM quiz_sessions WHERE week_id = ?", (week_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return QuizSession(
                        id=row['id'],
                        week_id=row['week_id'],
                        status=row['status'],
                        started_at=DatabaseManager._parse_datetime(row['started_at']),
                        ended_at=DatabaseManager._parse_datetime(row['ended_at'])
                    )
                return None
    
    async def get_active_quiz_session(self) -> Optional[QuizSession]:
        """Get currently active quiz session"""
        db = await self.get_connection()
        async with db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM quiz_sessions WHERE status = 'active' ORDER BY started_at DESC LIMIT 1"
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return QuizSession(
                        id=row['id'],
                        week_id=row['week_id'],
                        status=row['status'],
                        started_at=DatabaseManager._parse_datetime(row['started_at']),
                        ended_at=DatabaseManager._parse_datetime(row['ended_at'])
                    )
                return None
    
    async def end_quiz_session(self, week_id: str) -> bool:
        """End a quiz session"""
        db = await self.get_connection()
        async with db:
            cursor = await db.execute("""
                UPDATE quiz_sessions 
                SET status = 'ended', ended_at = ?
                WHERE week_id = ?
            """, (datetime.now().isoformat(), week_id))
            await db.commit()
            return cursor.rowcount > 0
    
    # Quiz result operations
    async def save_quiz_result(
        self,
        user_id: int,
        score: int,
        total_questions: int,
        quiz_week_id: str
    ) -> QuizResult:
        """Save quiz result for a user"""
        db = await self.get_connection()
        async with db:
            await db.execute("""
                INSERT INTO quiz_results 
                (user_id, score, total_questions, quiz_week_id, quiz_date)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, score, total_questions, quiz_week_id, datetime.now().isoformat()))
            await db.commit()
            return QuizResult(
                user_id=user_id,
                score=score,
                total_questions=total_questions,
                quiz_week_id=quiz_week_id
            )
    
    async def get_top_quiz_results(
        self,
        quiz_week_id: str,
        limit: int = 3
    ) -> List[Tuple[int, int, Optional[str], Optional[str]]]:
        """
        Get top quiz results for a specific week
        
        Returns:
            List of tuples: (user_id, score, username, first_name)
        """
        db = await self.get_connection()
        async with db:
            db.row_factory = aiosqlite.Row
            results = []
            async with db.execute("""
                SELECT qr.user_id, qr.score, u.username, u.first_name
                FROM quiz_results qr
                LEFT JOIN users u ON qr.user_id = u.user_id
                WHERE qr.quiz_week_id = ?
                ORDER BY qr.score DESC, qr.quiz_date ASC
                LIMIT ?
            """, (quiz_week_id, limit)) as cursor:
                async for row in cursor:
                    results.append((
                        row['user_id'],
                        row['score'],
                        row['username'],
                        row['first_name']
                    ))
            return results
    
    async def user_has_completed_quiz(self, user_id: int, quiz_week_id: str) -> bool:
        """Check if user has already completed a quiz"""
        db = await self.get_connection()
        async with db:
            async with db.execute("""
                SELECT COUNT(*) as count FROM quiz_results
                WHERE user_id = ? AND quiz_week_id = ?
            """, (user_id, quiz_week_id)) as cursor:
                row = await cursor.fetchone()
                return row[0] > 0 if row else False
    
    # User quiz answer operations
    async def save_user_answer(
        self,
        user_id: int,
        quiz_week_id: str,
        question_id: int,
        user_answer: str
    ) -> UserQuizAnswer:
        """Save user's answer to a quiz question"""
        db = await self.get_connection()
        async with db:
            await db.execute("""
                INSERT INTO user_quiz_answers 
                (user_id, quiz_week_id, question_id, user_answer, answered_at)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, quiz_week_id, question_id, user_answer.lower(), datetime.now().isoformat()))
            await db.commit()
            return UserQuizAnswer(
                user_id=user_id,
                quiz_week_id=quiz_week_id,
                question_id=question_id,
                user_answer=user_answer.lower()
            )
    
    async def get_user_answers_for_quiz(
        self,
        user_id: int,
        quiz_week_id: str
    ) -> List[UserQuizAnswer]:
        """Get all answers for a user in a specific quiz"""
        db = await self.get_connection()
        async with db:
            db.row_factory = aiosqlite.Row
            answers = []
            async with db.execute("""
                SELECT * FROM user_quiz_answers
                WHERE user_id = ? AND quiz_week_id = ?
                ORDER BY question_id
            """, (user_id, quiz_week_id)) as cursor:
                async for row in cursor:
                    answers.append(UserQuizAnswer(
                        id=row['id'],
                        user_id=row['user_id'],
                        quiz_week_id=row['quiz_week_id'],
                        question_id=row['question_id'],
                        user_answer=row['user_answer'],
                        answered_at=DatabaseManager._parse_datetime(row['answered_at'])
                    ))
            return answers

