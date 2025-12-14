"""
Configuration management for the bot
"""

import os
from dotenv import load_dotenv
from typing import List

# Load environment variables from .env file
load_dotenv()


class Config:
    """Bot configuration class"""
    
    # Telegram Bot Configuration
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    
    # Admin Configuration
    ADMIN_IDS: List[int] = [
        int(admin_id.strip())
        for admin_id in os.getenv("ADMIN_IDS", "").split(",")
        if admin_id.strip().isdigit()
    ]
    
    # Channel Configuration
    CHANNEL_ID: str = os.getenv("CHANNEL_ID", "")
    
    # Welcome Gift Configuration
    WELCOME_GIFT_LINK: str = os.getenv("WELCOME_GIFT_LINK", "")
    
    # Database Configuration
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "bot.db")
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate that all required configuration is present
        
        Returns:
            True if all required config is present, False otherwise
        """
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is required but not set in environment variables")
        
        if not cls.ADMIN_IDS:
            raise ValueError("ADMIN_IDS is required but not set in environment variables")
        
        if not cls.CHANNEL_ID:
            raise ValueError("CHANNEL_ID is required but not set in environment variables")
        
        if not cls.WELCOME_GIFT_LINK:
            raise ValueError("WELCOME_GIFT_LINK is required but not set in environment variables")
        
        return True
    
    @classmethod
    def is_admin(cls, user_id: int) -> bool:
        """
        Check if a user is an admin
        
        Args:
            user_id: Telegram user ID to check
            
        Returns:
            True if user is admin, False otherwise
        """
        return user_id in cls.ADMIN_IDS


