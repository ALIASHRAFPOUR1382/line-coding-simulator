"""
Message templates for bot responses
"""

from bot.config import Config


def get_welcome_message(channel_name: str = "کانال تیزهوشان") -> str:
    """
    Get welcome message for new channel members
    
    Args:
        channel_name: Name of the channel
        
    Returns:
        Welcome message text
    """
    return f"""سلام! 👋 به خانواده بزرگ «{channel_name}» خوش اومدی.

اینجا مسیر موفقیت تو در آزمون تیزهوشان رو هموار می‌کنیم.

برای اینکه بتونیم بهترین و مرتبط‌ترین محتوا رو بهت نمایش بدیم، لطفاً دسته‌بندی خودت رو انتخاب کن:"""


def get_category_confirmation_message(category_name: str) -> str:
    """
    Get confirmation message after category selection
    
    Args:
        category_name: Display name of selected category
        
    Returns:
        Confirmation message with gift link
    """
    return f"""عالی! اطلاعات شما با موفقیت ثبت شد. از این به بعد محتوای ویژه‌ای برای شما ارسال می‌شود.

🎁 هدیه خوشامدگویی ما به شما:

«چک‌لیست ۲۰ موردی آمادگی برای آزمون تیزهوشان در یک هفته آخر»

برای دانلود روی لینک زیر کلیک کن:

{Config.WELCOME_GIFT_LINK}

به خانواده ما خوش آمدی! 🚀"""


def get_quiz_announcement_message(channel_name: str = "کانال تیزهوشان") -> str:
    """
    Get quiz announcement message for channel
    
    Args:
        channel_name: Name of the channel
        
    Returns:
        Quiz announcement message
    """
    return f"""🚀 کوئیز هفتگی «{channel_name}» شروع شد!

آماده‌ای تا دانش خودت رو محک بزنی؟

۱۰ سوال هیجان‌انگیز در انتظار توئه.

برای شروع، روی دکمه زیر کلیک کن! 👇"""


def get_quiz_question_message(question_number: int, total_questions: int, question_text: str) -> str:
    """
    Format quiz question message
    
    Args:
        question_number: Current question number
        total_questions: Total number of questions
        question_text: Question text
        
    Returns:
        Formatted question message
    """
    return f"""سوال {question_number} از {total_questions}:

{question_text}"""


def get_quiz_completion_message(score: int, total_questions: int) -> str:
    """
    Get quiz completion message with score
    
    Args:
        score: User's score
        total_questions: Total number of questions
        
    Returns:
        Completion message
    """
    return f"""🏁 آزمون شما به پایان رسید!

نمره شما از {total_questions}: {score}

برای دیدن نتایج کامل و برندگان، کانال را دنبال کن.

موفق باشی! 🌟"""


def get_quiz_winners_message(week_id: str, winners: list, channel_name: str = "کانال تیزهوشان") -> str:
    """
    Format quiz winners announcement message
    
    Args:
        week_id: Quiz week identifier
        winners: List of tuples (user_id, score, username, first_name)
        channel_name: Name of the channel
        
    Returns:
        Formatted winners message
    """
    message = f"""🏆 نتایج کوئیز هفته «{channel_name}» اعلام شد!

از همه شرکت‌کنندگان عزیز سپاسگزاریم.

تبریک به ۳ نفر برتر این هفته که بالاترین نمرات رو کسب کردن:

"""
    
    medals = ["🥇", "🥈", "🥉"]
    positions = ["مقام اول", "مقام دوم", "مقام سوم"]
    
    for i, (user_id, score, username, first_name) in enumerate(winners[:3]):
        medal = medals[i] if i < len(medals) else "🏅"
        position = positions[i] if i < len(positions) else f"مقام {i+1}"
        
        # Format user display name
        if username:
            user_display = f"@{username}"
        elif first_name:
            user_display = first_name
        else:
            user_display = f"کاربر {user_id}"
        
        message += f"{medal} {position}: {user_display} با نمره {score}\n"
    
    message += "\nقهرمانان برای دریافت جایزه خود با ادمین کانال در ارتباط باشید.\n\nتا هفته بعد! 👋"
    
    return message


def get_start_command_message() -> str:
    """
    Get message for /start command
    
    Returns:
        Start command message
    """
    return """سلام! 👋

به ربات مدیریت کانال تیزهوشان خوش آمدی.

این ربات برای مدیریت و تعامل با اعضای کانال طراحی شده است.

اگر عضو کانال هستی، پیام‌های ویژه‌ای برای تو ارسال می‌شه!"""


def get_admin_help_message() -> str:
    """
    Get admin help message with available commands
    
    Returns:
        Admin help message
    """
    return """دستورات مدیریتی:

/startquiz - شروع کوئیز هفتگی جدید
/endquiz - پایان کوئیز و اعلام برندگان
/broadcast <پیام> - ارسال پیام به تمام کاربران

برای استفاده از دستورات، لطفاً دستور را به همراه پارامترهای لازم ارسال کنید."""


