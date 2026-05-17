"""
Authentication service
"""
from src.database.db_manager import DatabaseManager

class AuthService:
    """Handle authentication logic"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.current_user = None
    
    def login(self, email: str, password: str) -> bool:
        """Authenticate user"""
        if self.db.authenticate_user(email, password):
            self.current_user = email
            return True
        return False
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.current_user is not None
    
    def get_current_user(self) -> str:
        """Get current user email"""
        return self.current_user if self.current_user else ""