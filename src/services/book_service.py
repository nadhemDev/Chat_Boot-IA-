"""
Book service for business logic
"""
from typing import List, Optional, Tuple
from src.models.book import Book
from src.database.db_manager import DatabaseManager

class BookService:
    """Handle book business logic"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def get_all_books(self) -> List[Book]:
        """Get all books"""
        return self.db.get_all_books()
    
    def get_book_by_id(self, book_id: str) -> Optional[Book]:
        """Get book by ID"""
        return self.db.get_book_by_id(book_id)
    
    def add_book(self, book: Book) -> Tuple[bool, str]:
        """Add a new book with validation"""
        # Validation
        if not book.title or not book.author or not book.category:
            return False, "Tous les champs sont requis"
        
        if book.year < 1450 or book.year > 2026:
            return False, "Année invalide (1450-2026)"
        
        if book.quantity < 0:
            return False, "La quantité doit être positive"
        
        # Check for duplicate ID (should not happen with auto-increment)
        existing = self.db.get_book_by_id(book.id)
        if existing:
            # Generate new ID if collision occurs
            new_id = self.generate_next_id()
            book.id = new_id
        
        if self.db.add_book(book):
            return True, "Livre ajouté avec succès"
        return False, "Erreur lors de l'ajout"
    
    def update_book(self, book_id: str, book: Book) -> Tuple[bool, str]:
        """Update a book with validation"""
        existing = self.db.get_book_by_id(book_id)
        if not existing:
            return False, "Livre non trouvé"
        
        # Keep original ID
        book.id = book_id
        
        if self.db.update_book(book_id, book):
            return True, "Livre modifié avec succès"
        return False, "Erreur lors de la modification"
    
    def delete_book(self, book_id: str) -> Tuple[bool, str]:
        """Delete a book"""
        existing = self.db.get_book_by_id(book_id)
        if not existing:
            return False, "Livre non trouvé"
        
        if self.db.delete_book(book_id):
            return True, "Livre supprimé avec succès"
        return False, "Erreur lors de la suppression"
    
    def search_books(self, query: str) -> List[Book]:
        """Search books"""
        if not query:
            return self.get_all_books()
        return self.db.search_books(query)
    
    def generate_next_id(self) -> str:
        """Generate next available ID (auto-increment)"""
        books = self.get_all_books()
        if not books:
            return "101"
        
        max_id = 100
        for book in books:
            try:
                book_id = int(book.id)
                if book_id > max_id:
                    max_id = book_id
            except ValueError:
                continue
        
        return str(max_id + 1)
    
    def get_statistics(self) -> dict:
        """Get library statistics"""
        books = self.get_all_books()
        total_books = len(books)
        available_books = sum(1 for b in books if b.status == 'disponible')
        borrowed_books = sum(1 for b in books if b.status == 'emprunté')
        reserved_books = sum(1 for b in books if b.status == 'réservé')
        total_copies = sum(b.quantity for b in books)
        
        return {
            'total_books': total_books,
            'available_books': available_books,
            'borrowed_books': borrowed_books,
            'reserved_books': reserved_books,
            'total_copies': total_copies
        }