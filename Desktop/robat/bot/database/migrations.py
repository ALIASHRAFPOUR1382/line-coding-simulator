"""
Database migration and initialization script
"""

import asyncio
import aiosqlite
from pathlib import Path
from bot.config import Config


async def init_database(db_path: str = None):
    """
    Initialize database with all required tables
    
    Args:
        db_path: Path to SQLite database file. If None, uses Config.DATABASE_PATH
    """
    if db_path is None:
        db_path = Config.DATABASE_PATH
    
    # Ensure directory exists
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    
    async with aiosqlite.connect(db_path) as db:
        # Create users table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id BIGINT UNIQUE NOT NULL,
                username TEXT,
                first_name TEXT,
                category TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create quiz_questions table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS quiz_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_text TEXT NOT NULL,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                correct_answer CHAR(1) NOT NULL,
                is_active BOOLEAN DEFAULT 1
            )
        """)
        
        # Create quiz_sessions table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS quiz_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week_id TEXT UNIQUE NOT NULL,
                status TEXT NOT NULL DEFAULT 'active',
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ended_at TIMESTAMP
            )
        """)
        
        # Create quiz_results table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id BIGINT NOT NULL,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                quiz_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                quiz_week_id TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Create user_quiz_answers table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_quiz_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id BIGINT NOT NULL,
                quiz_week_id TEXT NOT NULL,
                question_id INTEGER NOT NULL,
                user_answer CHAR(1) NOT NULL,
                answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (question_id) REFERENCES quiz_questions(id)
            )
        """)
        
        # Create indexes for better performance
        await db.execute("CREATE INDEX IF NOT EXISTS idx_users_user_id ON users(user_id)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_quiz_results_user_id ON quiz_results(user_id)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_quiz_results_week_id ON quiz_results(quiz_week_id)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_quiz_results_score ON quiz_results(score DESC)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_quiz_questions_active ON quiz_questions(is_active)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_quiz_sessions_status ON quiz_sessions(status)")
        
        await db.commit()
        print(f"Database initialized successfully at {db_path}")


if __name__ == "__main__":
    # Run migration when executed directly
    asyncio.run(init_database())


