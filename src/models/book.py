"""
Book model class
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Book:
    """Book entity model"""
    id: str
    title: str
    author: str
    category: str
    year: int
    quantity: int
    status: str = "disponible"
    borrower: Optional[str] = None
    return_date: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert book to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'category': self.category,
            'year': str(self.year),
            'quantity': str(self.quantity),
            'status': self.status,
            'borrower': self.borrower or '',
            'return_date': self.return_date or ''
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Book':
        """Create book from dictionary"""
        return cls(
            id=data.get('id', ''),
            title=data.get('title', ''),
            author=data.get('author', ''),
            category=data.get('category', ''),
            year=int(data.get('year', 0)),
            quantity=int(data.get('quantity', 0)),
            status=data.get('status', 'disponible'),
            borrower=data.get('borrower') or None,
            return_date=data.get('return_date') or None
        )
    
    def get_status_display(self) -> str:
        """Get formatted status"""
        if self.status == 'disponible':
            return f"✅ Disponible ({self.quantity} exemplaire(s))"
        elif self.status == 'emprunté':
            return f"📖 Emprunté (retour: {self.return_date or 'N/A'})"
        else:
            return f"🔒 Réservé"