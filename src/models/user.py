"""
User model class
"""
from dataclasses import dataclass

@dataclass
class User:
    """User entity model"""
    email: str
    password: str
    
    def to_dict(self) -> dict:
        """Convert user to dictionary"""
        return {
            'email': self.email,
            'password': self.password
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create user from dictionary"""
        return cls(
            email=data.get('email', ''),
            password=data.get('password', '')
        )