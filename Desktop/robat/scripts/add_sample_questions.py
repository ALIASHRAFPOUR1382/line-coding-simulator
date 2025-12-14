"""
Script to add sample quiz questions to the database
Run this script to populate the database with sample questions for testing
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import bot modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from bot.database.db_manager import DatabaseManager
from bot.database.migrations import init_database


SAMPLE_QUESTIONS = [
    {
        "question_text": "کدام گزینه زوج مرتبش را به درستی کامل می‌کند؟\n(پایتخت، کشور) <- (؟، ایران)",
        "option_a": "تهران",
        "option_b": "اصفهان",
        "option_c": "آسیا",
        "option_d": "خلیج فارس",
        "correct_answer": "a"
    },
    {
        "question_text": "حاصل جمع اعداد ۱۵ و ۲۵ برابر است با:",
        "option_a": "۳۵",
        "option_b": "۴۰",
        "option_c": "۴۵",
        "option_d": "۵۰",
        "correct_answer": "b"
    },
    {
        "question_text": "کدام یک از گزینه‌های زیر یک عدد اول است؟",
        "option_a": "۴",
        "option_b": "۶",
        "option_c": "۷",
        "option_d": "۸",
        "correct_answer": "c"
    },
    {
        "question_text": "مساحت یک مربع با ضلع ۵ سانتی‌متر برابر است با:",
        "option_a": "۱۰ سانتی‌متر مربع",
        "option_b": "۱۵ سانتی‌متر مربع",
        "option_c": "۲۰ سانتی‌متر مربع",
        "option_d": "۲۵ سانتی‌متر مربع",
        "correct_answer": "d"
    },
    {
        "question_text": "کدام یک از گزینه‌های زیر پایتخت کشور ترکیه است؟",
        "option_a": "استانبول",
        "option_b": "آنکارا",
        "option_c": "ازمیر",
        "option_d": "بورسا",
        "correct_answer": "b"
    },
    {
        "question_text": "حاصل ضرب ۶ × ۷ برابر است با:",
        "option_a": "۳۸",
        "option_b": "۴۰",
        "option_c": "۴۲",
        "option_d": "۴۴",
        "correct_answer": "c"
    },
    {
        "question_text": "کدام یک از گزینه‌های زیر بزرگترین عدد است؟",
        "option_a": "۰.۵",
        "option_b": "۰.۷",
        "option_c": "۰.۳",
        "option_d": "۰.۱",
        "correct_answer": "b"
    },
    {
        "question_text": "محیط یک دایره با شعاع ۷ سانتی‌متر (با π = ۳.۱۴) تقریباً برابر است با:",
        "option_a": "۲۱.۹۸ سانتی‌متر",
        "option_b": "۴۳.۹۶ سانتی‌متر",
        "option_c": "۱۵۳.۸۶ سانتی‌متر مربع",
        "option_d": "۴۹ سانتی‌متر",
        "correct_answer": "b"
    },
    {
        "question_text": "کدام یک از گزینه‌های زیر یک کسر معادل با ۱/۲ است؟",
        "option_a": "۲/۳",
        "option_b": "۳/۶",
        "option_c": "۲/۵",
        "option_d": "۳/۸",
        "correct_answer": "b"
    },
    {
        "question_text": "حاصل تفریق ۱۰۰ - ۴۵ برابر است با:",
        "option_a": "۵۰",
        "option_b": "۵۵",
        "option_c": "۶۰",
        "option_d": "۶۵",
        "correct_answer": "b"
    }
]


async def add_sample_questions():
    """Add sample questions to the database"""
    print("Initializing database...")
    await init_database()
    
    import aiosqlite
    from bot.config import Config
    
    db_path = Config.DATABASE_PATH
    
    print(f"Adding {len(SAMPLE_QUESTIONS)} sample questions...")
    
    async with aiosqlite.connect(db_path) as db:
        for i, question in enumerate(SAMPLE_QUESTIONS, 1):
            try:
                await db.execute("""
                    INSERT INTO quiz_questions 
                    (question_text, option_a, option_b, option_c, option_d, correct_answer)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    question["question_text"],
                    question["option_a"],
                    question["option_b"],
                    question["option_c"],
                    question["option_d"],
                    question["correct_answer"].lower()
                ))
                print(f"Question {i} added successfully")
            except Exception as e:
                print(f"Error adding question {i}: {e}")
        
        await db.commit()
    
    print("\nSample questions added successfully!")
    print("You can now start a quiz using /startquiz command (as admin)")


if __name__ == "__main__":
    asyncio.run(add_sample_questions())

