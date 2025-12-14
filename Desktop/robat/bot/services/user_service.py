"""
User service for user management operations
"""

import logging
from typing import Optional
from bot.database.db_manager import DatabaseManager
from bot.database.models import User

logger = logging.getLogger(__name__)


class UserService:
    """Service for user-related operations"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
    
    async def get_or_create_user(
        self,
        user_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None
    ) -> User:
        """
        Get existing user or create new one
        
        Args:
            user_id: Telegram user ID
            username: Telegram username
            first_name: User's first name
            
        Returns:
            User object
        """
        user = await self.db_manager.get_user_by_id(user_id)
        if not user:
            user = await self.db_manager.create_user(
                user_id=user_id,
                username=username,
                first_name=first_name
            )
        return user
    
    async def update_user_category(self, user_id: int, category: str) -> bool:
        """
        Update user category
        
        Args:
            user_id: Telegram user ID
            category: Category to set
            
        Returns:
            True if successful, False otherwise
        """
        return await self.db_manager.update_user_category(user_id, category)
    
    async def get_user(self, user_id: int) -> Optional[User]:
        """
        Get user by ID
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            User object or None if not found
        """
        return await self.db_manager.get_user_by_id(user_id)


