"""
Input validation utilities
"""

from typing import Optional


def validate_answer_choice(answer: str) -> bool:
    """
    Validate that answer is a valid choice (a, b, c, d)
    
    Args:
        answer: Answer string to validate
        
    Returns:
        True if valid, False otherwise
    """
    return answer.lower() in ['a', 'b', 'c', 'd']


def validate_category(category: str) -> bool:
    """
    Validate that category is a valid user category
    
    Args:
        category: Category string to validate
        
    Returns:
        True if valid, False otherwise
    """
    valid_categories = ['student_6', 'student_9', 'parent', 'teacher']
    return category in valid_categories


def sanitize_username(username: Optional[str]) -> Optional[str]:
    """
    Sanitize Telegram username
    
    Args:
        username: Username to sanitize
        
    Returns:
        Sanitized username or None
    """
    if not username:
        return None
    
    # Remove @ if present
    username = username.lstrip('@')
    
    # Basic validation: alphanumeric and underscores only
    if username.replace('_', '').isalnum():
        return username
    
    return None


def format_user_display_name(user_id: int, username: Optional[str] = None, first_name: Optional[str] = None) -> str:
    """
    Format user display name for messages
    
    Args:
        user_id: Telegram user ID
        username: Telegram username
        first_name: User's first name
        
    Returns:
        Formatted display name
    """
    if username:
        return f"@{username}"
    elif first_name:
        return first_name
    else:
        return f"کاربر {user_id}"


