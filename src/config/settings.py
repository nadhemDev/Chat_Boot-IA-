"""
Application configuration settings
"""
import os
import csv
from dotenv import load_dotenv

load_dotenv()

class Config:
    # App Settings
    APP_NAME = "ChatBook IA"
    APP_VERSION = "1.0.0"
    APP_WIDTH = 1200
    APP_HEIGHT = 700
    
    # Colors (Design System)
    COLORS = {
        'background': '#F8FAFC',
        'surface': '#FFFFFF',
        'primary': '#1E293B',
        'primary_light': '#334155',
        'primary_hover': '#334155',
        'accent_green': '#10B981',
        'accent_green_hover': '#059669',
        'accent_blue': '#3B82F6',
        'accent_blue_hover': '#2563EB',
        'accent_red': '#EF4444',
        'accent_red_hover': '#DC2626',
        'accent_orange': '#F59E0B',
        'accent_orange_hover': '#D97706',
        'accent_gray': '#64748B',
        'accent_gray_hover': '#475569',
        'border': '#E2E8F0',
        'text_primary': '#1E293B',
        'text_secondary': '#64748B',
        'error': '#EF4444',
        'warning': '#F59E0B',
        'success': '#10B981'
    }
    
    # Fonts
    FONTS = {
        'title': ('Segoe UI', 32, 'bold'),
        'title_small': ('Segoe UI', 18, 'bold'),
        'subtitle': ('Segoe UI', 14),
        'body': ('Segoe UI', 12),
        'body_bold': ('Segoe UI', 12, 'bold'),
        'small': ('Segoe UI', 10),
        'button': ('Segoe UI', 13, 'bold')
    }
    
    # CSV Files
    DATA_DIR = "data"
    BOOKS_FILE = "data/books.csv"
    USERS_FILE = "data/users.csv"
    
    # Gemini API
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    GEMINI_MODEL = 'gemini-pro'
    
    # Validation Rules
    BOOK_FIELDS = ['id', 'title', 'author', 'category', 'year', 'quantity', 'status', 'borrower', 'return_date']
    
    # Enhanced Categories with emojis for better display
    CATEGORIES = [
        '📖 Roman',
        '🚀 Science-Fiction',
        '🐉 Fantasy',
        '🔍 Policier',
        '😱 Thriller',
        '🔬 Science',
        '📜 Histoire',
        '💻 Informatique',
        '🧠 Philosophie',
        '📝 Poésie',
        '🎭 Théâtre',
        '👤 Biographie',
        '📚 Essai',
        '🎨 Bande Dessinée',
        '🧸 Jeunesse',
        '🎨 Art',
        '🍳 Cuisine',
        '✈️ Voyage',
        '⚽ Sport',
        '📖 Autre'
    ]
    
    @classmethod
    def ensure_data_dir(cls):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(cls.DATA_DIR):
            os.makedirs(cls.DATA_DIR)
            print(f"✓ Created data directory: {cls.DATA_DIR}")
            return True
        return False
    
    @classmethod
    def ensure_books_file(cls):
        """Create books CSV file with headers if it doesn't exist"""
        if not os.path.exists(cls.BOOKS_FILE):
            try:
                with open(cls.BOOKS_FILE, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(cls.BOOK_FIELDS)
                print(f"✓ Created books file: {cls.BOOKS_FILE}")
                return True
            except Exception as e:
                print(f"⚠️ Error creating books file: {e}")
                return False
        return False
    
    @classmethod
    def ensure_users_file(cls):
        """Create users CSV file with headers and default admin if it doesn't exist"""
        if not os.path.exists(cls.USERS_FILE):
            try:
                with open(cls.USERS_FILE, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['username', 'password'])
                    # Add default admin user
                    writer.writerow(['admin', 'admin123'])
                    writer.writerow(['user', 'user123'])
                print(f"✓ Created users file with default accounts: {cls.USERS_FILE}")
                print("  Default accounts: admin/admin123, user/user123")
                return True
            except Exception as e:
                print(f"⚠️ Error creating users file: {e}")
                return False
        return False
    
    @classmethod
    def initialize_data_files(cls):
        """Initialize all data files"""
        print("\n📁 Initializing data files...")
        cls.ensure_data_dir()
        cls.ensure_books_file()
        cls.ensure_users_file()
        print("✅ Data files initialized\n")
    
    @classmethod
    def get_sample_books(cls):
        """Return sample books for initial database population"""
        return [
            {
                'id': '101',
                'title': 'Les Misérables',
                'author': 'Victor Hugo',
                'category': '📖 Roman',
                'year': '1862',
                'quantity': '3',
                'status': 'disponible',
                'borrower': '',
                'return_date': ''
            },
            {
                'id': '102',
                'title': 'Le Petit Prince',
                'author': 'Antoine de Saint-Exupéry',
                'category': '🧸 Jeunesse',
                'year': '1943',
                'quantity': '5',
                'status': 'disponible',
                'borrower': '',
                'return_date': ''
            },
            {
                'id': '103',
                'title': '1984',
                'author': 'George Orwell',
                'category': '🚀 Science-Fiction',
                'year': '1949',
                'quantity': '2',
                'status': 'disponible',
                'borrower': '',
                'return_date': ''
            },
            {
                'id': '104',
                'title': 'Le Comte de Monte-Cristo',
                'author': 'Alexandre Dumas',
                'category': '📖 Roman',
                'year': '1844',
                'quantity': '2',
                'status': 'emprunté',
                'borrower': 'user',
                'return_date': '2024-12-15'
            },
            {
                'id': '105',
                'title': 'Vingt mille lieues sous les mers',
                'author': 'Jules Verne',
                'category': '🚀 Science-Fiction',
                'year': '1870',
                'quantity': '1',
                'status': 'disponible',
                'borrower': '',
                'return_date': ''
            },
            {
                'id': '106',
                'title': 'Notre-Dame de Paris',
                'author': 'Victor Hugo',
                'category': '📖 Roman',
                'year': '1831',
                'quantity': '2',
                'status': 'disponible',
                'borrower': '',
                'return_date': ''
            },
            {
                'id': '107',
                'title': 'L\'Étranger',
                'author': 'Albert Camus',
                'category': '🧠 Philosophie',
                'year': '1942',
                'quantity': '1',
                'status': 'réservé',
                'borrower': 'admin',
                'return_date': ''
            },
            {
                'id': '108',
                'title': 'Germinal',
                'author': 'Émile Zola',
                'category': '📖 Roman',
                'year': '1885',
                'quantity': '2',
                'status': 'disponible',
                'borrower': '',
                'return_date': ''
            },
            {
                'id': '109',
                'title': 'Introduction à l\'algorithmique',
                'author': 'Thomas H. Cormen',
                'category': '💻 Informatique',
                'year': '2009',
                'quantity': '1',
                'status': 'disponible',
                'borrower': '',
                'return_date': ''
            },
            {
                'id': '110',
                'title': 'Sapiens',
                'author': 'Yuval Noah Harari',
                'category': '📜 Histoire',
                'year': '2015',
                'quantity': '3',
                'status': 'disponible',
                'borrower': '',
                'return_date': ''
            }
        ]
    
    @classmethod
    def validate_year(cls, year):
        """Validate if year is within acceptable range"""
        try:
            year_int = int(year)
            return 1450 <= year_int <= 2026
        except (ValueError, TypeError):
            return False
    
    @classmethod
    def validate_quantity(cls, quantity):
        """Validate if quantity is positive"""
        try:
            quantity_int = int(quantity)
            return quantity_int >= 0
        except (ValueError, TypeError):
            return False
    
    @classmethod
    def get_status_options(cls):
        """Return available status options"""
        return ['disponible', 'emprunté', 'réservé']
    
    @classmethod
    def get_status_display(cls, status):
        """Return formatted status with emoji"""
        status_map = {
            'disponible': '✅ Disponible',
            'emprunté': '📖 Emprunté',
            'réservé': '🔒 Réservé'
        }
        return status_map.get(status, status.capitalize())
    
    @classmethod
    def get_category_emoji(cls, category):
        """Extract emoji from category name"""
        # Categories already have emojis at the beginning
        if category and len(category) > 0:
            # Return first character if it's an emoji (simple check)
            first_char = category[0]
            if first_char in ['📖', '🚀', '🐉', '🔍', '😱', '🔬', '📜', '💻', '🧠', 
                             '📝', '🎭', '👤', '📚', '🎨', '🧸', '🍳', '✈️', '⚽']:
                return first_char
        return '📚'  # Default book emoji
    
    @classmethod
    def get_category_without_emoji(cls, category):
        """Remove emoji from category name"""
        # Remove emoji if present (assuming emoji is first character)
        if category and len(category) > 2 and category[0] in ['📖', '🚀', '🐉', '🔍', '😱', '🔬', '📜', '💻', '🧠', 
                                                               '📝', '🎭', '👤', '📚', '🎨', '🧸', '🍳', '✈️', '⚽']:
            return category[2:]  # Skip emoji and space
        return category