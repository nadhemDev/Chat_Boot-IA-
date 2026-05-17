"""
Database manager for CSV operations
"""
import os
from typing import List, Dict, Any, Optional
from src.database.csv_handler import CSVHandler
from src.models.book import Book
from src.models.user import User
from src.config.settings import Config
from src.utils.constants import Messages

class DatabaseManager:
    """Manage database operations"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize database files"""
        # Initialize books.csv
        CSVHandler.ensure_file_exists(Config.BOOKS_FILE, Messages.CSV_BOOKS_HEADERS)
        
        # Initialize users.csv with default admin
        CSVHandler.ensure_file_exists(Config.USERS_FILE, Messages.CSV_USERS_HEADERS)
        
        # Add default user if no users exist
        users = CSVHandler.read_all(Config.USERS_FILE)
        if not users:
            default_user = {'email': 'nadhem@gmail.com', 'password': '123456789'}
            CSVHandler.append(Config.USERS_FILE, default_user, Messages.CSV_USERS_HEADERS)
    
    # Book operations
    def get_all_books(self) -> List[Book]:
        """Get all books"""
        data = CSVHandler.read_all(Config.BOOKS_FILE)
        return [Book.from_dict(record) for record in data]
    
    def get_book_by_id(self, book_id: str) -> Optional[Book]:
        """Get book by ID"""
        record = CSVHandler.find_by_id(Config.BOOKS_FILE, book_id)
        return Book.from_dict(record) if record else None
    
    def add_book(self, book: Book) -> bool:
        """Add a new book"""
        try:
            # Check if ID already exists
            existing = self.get_book_by_id(book.id)
            if existing:
                return False
            
            CSVHandler.append(Config.BOOKS_FILE, book.to_dict(), Messages.CSV_BOOKS_HEADERS)
            return True
        except Exception as e:
            print(f"Error adding book: {e}")
            return False
    
    def update_book(self, book_id: str, updated_book: Book) -> bool:
        """Update an existing book"""
        return CSVHandler.update(Config.BOOKS_FILE, book_id, updated_book.to_dict())
    
    def delete_book(self, book_id: str) -> bool:
        """Delete a book"""
        return CSVHandler.delete(Config.BOOKS_FILE, book_id)
    
    def search_books(self, query: str) -> List[Book]:
        """Search books by title, author, or ID"""
        books = self.get_all_books()
        query_lower = query.lower()
        
        results = []
        for book in books:
            if (query_lower in book.title.lower() or 
                query_lower in book.author.lower() or 
                query_lower == book.id):
                results.append(book)
        
        return results
    
    def get_books_by_category(self, category: str) -> List[Book]:
        """Get books by category"""
        books = self.get_all_books()
        return [b for b in books if b.category.lower() == category.lower()]
    
    def get_books_by_author(self, author: str) -> List[Book]:
        """Get books by author"""
        books = self.get_all_books()
        return [b for b in books if author.lower() in b.author.lower()]
    
    # User operations
    def authenticate_user(self, email: str, password: str) -> bool:
        """Authenticate user"""
        users = CSVHandler.read_all(Config.USERS_FILE)
        for user in users:
            if user.get('email') == email and user.get('password') == password:
                return True
        return False
    
    def add_sample_books(self):
        """Add sample books for testing"""
        books = self.get_all_books()
        if not books:
            sample_books = [
                Book('101', 'Le Petit Prince', 'Antoine de Saint-Exupéry', 'Roman', 1943, 3, 'disponible'),
                Book('102', 'Les Misérables', 'Victor Hugo', 'Roman', 1862, 2, 'emprunté', 'Jean Dupont', '2026-03-15'),
                Book('103', 'Notre-Dame de Paris', 'Victor Hugo', 'Roman', 1831, 2, 'disponible'),
                Book('104', 'Orgueil et Préjugés', 'Jane Austen', 'Roman', 1813, 1, 'disponible'),
                Book('105', 'Jane Eyre', 'Charlotte Brontë', 'Roman', 1847, 2, 'disponible'),
                Book('106', 'Les Contemplations', 'Victor Hugo', 'Poésie', 1856, 1, 'disponible'),
                Book('107', 'Introduction à Python', 'Guido van Rossum', 'Informatique', 2020, 5, 'disponible'),
                Book('108', 'Histoire de France', 'Jules Michelet', 'Histoire', 1855, 1, 'réservé', 'Marie Martin', '2026-03-20'),
            ]
            for book in sample_books:
                self.add_book(book)