"""
Add book view with form
"""
import customtkinter as ctk
from tkinter import ttk, messagebox
from src.config.settings import Config
from src.models.book import Book
from src.services.book_service import BookService
from src.utils.constants import Messages

class AddBookView:
    def __init__(self, parent, book_service: BookService, refresh_callback):
        self.parent = parent
        self.book_service = book_service
        self.refresh_callback = refresh_callback
        self.setup_ui()
    
    def setup_ui(self):
        """Setup add book interface"""
        self.parent.configure(fg_color=Config.COLORS['surface'])
        
        # Main container with scrollable frame for better UX
        self.main_container = ctk.CTkScrollableFrame(
            self.parent, 
            fg_color="transparent"
        )
        self.main_container.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Title with icon effect
        title_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(
            title_frame,
            text="📚 Ajouter un nouveau livre",
            font=Config.FONTS['title'],
            text_color=Config.COLORS['primary']
        )
        title.pack(anchor="w")
        
        # Subtitle
        subtitle = ctk.CTkLabel(
            title_frame,
            text="Remplissez les informations ci-dessous pour ajouter un livre à la bibliothèque",
            font=Config.FONTS['body'],
            text_color=Config.COLORS['text_secondary']
        )
        subtitle.pack(anchor="w", pady=(5, 0))
        
        # Form container with card effect
        form_frame = ctk.CTkFrame(
            self.main_container, 
            fg_color=Config.COLORS['surface'],
            corner_radius=15,
            border_width=1,
            border_color=Config.COLORS['border']
        )
        form_frame.pack(fill="x", pady=20)
        
        # Form inner padding
        form_inner = ctk.CTkFrame(form_frame, fg_color="transparent")
        form_inner.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Two column layout with responsive design
        columns_frame = ctk.CTkFrame(form_inner, fg_color="transparent")
        columns_frame.pack(fill="both", expand=True)
        
        # Configure grid for responsive layout
        columns_frame.grid_columnconfigure(0, weight=1)
        columns_frame.grid_columnconfigure(1, weight=1)
        
        # Left column
        left_col = ctk.CTkFrame(columns_frame, fg_color="transparent")
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        
        # Right column
        right_col = ctk.CTkFrame(columns_frame, fg_color="transparent")
        right_col.grid(row=0, column=1, sticky="nsew", padx=(15, 0))
        
        # Left column fields
        self.create_field(left_col, "Titre", 0, required=True)
        self.create_field(left_col, "Auteur", 1, required=True)
        
        # Right column fields
        self.create_year_field(right_col, "Année", 0, required=True)
        self.create_quantity_field(right_col, "Quantité", 1, required=True)
        
        # Category field with improved dropdown
        self.create_category_field(right_col, "Catégorie", 2, required=True)
        
        # Buttons section
        button_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        button_frame.pack(fill="x", pady=30)
        
        # Button container for centering
        button_container = ctk.CTkFrame(button_frame, fg_color="transparent")
        button_container.pack()
        
        # Add button with icon
        self.add_btn = ctk.CTkButton(
            button_container,
            text="➕ Ajouter le livre",
            height=48,
            width=200,
            corner_radius=12,
            fg_color=Config.COLORS['accent_green'],
            hover_color=Config.COLORS['accent_green_hover'],
            font=Config.FONTS['button'],
            command=self.add_book
        )
        self.add_btn.pack(side="left", padx=(0, 15))
        
        # Reset button with icon
        self.reset_btn = ctk.CTkButton(
            button_container,
            text="🔄 Réinitialiser",
            height=48,
            width=180,
            corner_radius=12,
            fg_color=Config.COLORS['accent_gray'],
            hover_color=Config.COLORS['accent_gray_hover'],
            font=Config.FONTS['button'],
            command=self.reset_form
        )
        self.reset_btn.pack(side="left")
        
        # Preview section
        preview_frame = ctk.CTkFrame(self.main_container, corner_radius=15)
        preview_frame.pack(fill="both", expand=True, pady=20)
        
        # Preview header with icon
        preview_header = ctk.CTkFrame(preview_frame, fg_color="transparent")
        preview_header.pack(fill="x", padx=20, pady=(20, 10))
        
        preview_icon = ctk.CTkLabel(
            preview_header,
            text="📖",
            font=("Segoe UI", 20),
            text_color=Config.COLORS['primary']
        )
        preview_icon.pack(side="left", padx=(0, 10))
        
        preview_label = ctk.CTkLabel(
            preview_header,
            text="Aperçu des livres récents",
            font=Config.FONTS['body_bold'],
            text_color=Config.COLORS['text_secondary']
        )
        preview_label.pack(side="left")
        
        # Treeview container with better styling
        tree_container = ctk.CTkFrame(preview_frame, fg_color="transparent")
        tree_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Create custom style for Treeview
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Custom.Treeview",
            font=('Segoe UI', 11),
            rowheight=35,
            background='white',
            fieldbackground='white',
            foreground='#2C3E50'
        )
        style.configure(
            "Custom.Treeview.Heading",
            font=('Segoe UI', 11, 'bold'),
            background=Config.COLORS['primary'],
            foreground='white',
            relief='flat'
        )
        style.map('Custom.Treeview.Heading',
                  background=[('active', Config.COLORS['primary_hover'])])
        
        # Treeview for preview
        self.tree = ttk.Treeview(
            tree_container,
            columns=('Titre', 'Auteur', 'Catégorie', 'Année', 'Quantité', 'Statut'),
            show='headings',
            height=6,
            style="Custom.Treeview"
        )
        
        # Configure columns
        self.tree.heading('Titre', text='📚 Titre')
        self.tree.heading('Auteur', text='✍️ Auteur')
        self.tree.heading('Catégorie', text='📑 Catégorie')
        self.tree.heading('Année', text='📅 Année')
        self.tree.heading('Quantité', text='🔢 Quantité')
        self.tree.heading('Statut', text='✅ Statut')
        
        self.tree.column('Titre', width=250, minwidth=150)
        self.tree.column('Auteur', width=200, minwidth=120)
        self.tree.column('Catégorie', width=150, minwidth=100)
        self.tree.column('Année', width=100, minwidth=80)
        self.tree.column('Quantité', width=100, minwidth=80)
        self.tree.column('Statut', width=120, minwidth=100)
        
        # Scrollbar with custom styling
        scrollbar = ttk.Scrollbar(
            tree_container, 
            orient="vertical", 
            command=self.tree.yview,
            style="Vertical.TScrollbar"
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Initial preview update
        self.update_preview()
        
        # Set initial focus to title field
        self.title_entry.focus()
    
    def create_field(self, parent, label, row, required=False):
        """Create form field with improved styling"""
        # Label frame for better visual grouping
        label_text = f"{label} {'*' if required else ''}"
        lbl = ctk.CTkLabel(
            parent,
            text=label_text,
            font=Config.FONTS['body_bold'],
            text_color=Config.COLORS['text_secondary']
        )
        lbl.grid(row=row*2, column=0, sticky="w", padx=(0, 10), pady=(10, 5))
        
        entry = ctk.CTkEntry(
            parent,
            height=44,
            corner_radius=10,
            border_color=Config.COLORS['border'],
            border_width=1,
            font=Config.FONTS['body']
        )
        entry.grid(row=row*2+1, column=0, sticky="ew", pady=(0, 15))
        
        parent.grid_columnconfigure(0, weight=1)
        
        # Store reference
        if label == "Titre":
            self.title_entry = entry
        elif label == "Auteur":
            self.author_entry = entry
        
        return entry
    
    def create_year_field(self, parent, label, row, required=False):
        """Create year field with validation"""
        label_text = f"{label} {'*' if required else ''}"
        lbl = ctk.CTkLabel(
            parent,
            text=label_text,
            font=Config.FONTS['body_bold'],
            text_color=Config.COLORS['text_secondary']
        )
        lbl.grid(row=row*2, column=0, sticky="w", padx=(0, 10), pady=(10, 5))
        
        self.year_entry = ctk.CTkEntry(
            parent,
            height=44,
            corner_radius=10,
            border_color=Config.COLORS['border'],
            border_width=1,
            placeholder_text="ex: 2024",
            font=Config.FONTS['body']
        )
        self.year_entry.grid(row=row*2+1, column=0, sticky="ew", pady=(0, 15))
        
        parent.grid_columnconfigure(0, weight=1)
    
    def create_quantity_field(self, parent, label, row, required=False):
        """Create quantity field with validation"""
        label_text = f"{label} {'*' if required else ''}"
        lbl = ctk.CTkLabel(
            parent,
            text=label_text,
            font=Config.FONTS['body_bold'],
            text_color=Config.COLORS['text_secondary']
        )
        lbl.grid(row=row*2, column=0, sticky="w", padx=(0, 10), pady=(10, 5))
        
        self.quantity_entry = ctk.CTkEntry(
            parent,
            height=44,
            corner_radius=10,
            border_color=Config.COLORS['border'],
            border_width=1,
            placeholder_text="ex: 5",
            font=Config.FONTS['body']
        )
        self.quantity_entry.grid(row=row*2+1, column=0, sticky="ew", pady=(0, 15))
        
        parent.grid_columnconfigure(0, weight=1)
    
    def create_category_field(self, parent, label, row, required=False):
        """Create category dropdown with better styling"""
        label_text = f"{label} {'*' if required else ''}"
        lbl = ctk.CTkLabel(
            parent,
            text=label_text,
            font=Config.FONTS['body_bold'],
            text_color=Config.COLORS['text_secondary']
        )
        lbl.grid(row=row*2, column=0, sticky="w", padx=(0, 10), pady=(10, 5))
        
        # Get categories from Config or use the comprehensive list
        categories_from_config = Config.CATEGORIES if hasattr(Config, 'CATEGORIES') and Config.CATEGORIES else []
        
        # Comprehensive category list (from your image)
        default_categories = [
            "Roman",
            "Science-Fiction",
            "Fantasy", 
            "Policier",
            "Thriller",
            "Science",
            "Histoire",
            "Informatique",
            "Philosophie"
        ]
        
        # Use config categories if available, otherwise use default list
        categories = categories_from_config if categories_from_config else default_categories
        
        # Set default value - make sure it's a string, not a list
        default_value = categories[0] if categories else "Roman"
        self.category_var = ctk.StringVar(value=default_value)
        
        # Create the option menu with proper configuration
        self.category_menu = ctk.CTkOptionMenu(
            parent,
            values=categories,
            variable=self.category_var,
            height=44,
            width=300,  # Fixed width for better visibility
            corner_radius=10,
            fg_color="white",
            text_color="#2C3E50",  # Dark text for visibility
            button_color=Config.COLORS['accent_gray'],
            button_hover_color=Config.COLORS['accent_gray_hover'],
            font=Config.FONTS['body'],
            dropdown_font=Config.FONTS['body']
        )
        self.category_menu.grid(row=row*2+1, column=0, sticky="ew", pady=(0, 15))
        
        parent.grid_columnconfigure(0, weight=1)
    
    def add_book(self):
        """Add book to database with auto-generated ID"""
        try:
            # Validate required fields
            title = self.title_entry.get().strip()
            author = self.author_entry.get().strip()
            year_str = self.year_entry.get().strip()
            quantity_str = self.quantity_entry.get().strip()
            category = self.category_var.get()
            
            # Comprehensive validation
            if not title:
                messagebox.showerror("Erreur", "Le titre est requis")
                self.title_entry.focus()
                return
            
            if not author:
                messagebox.showerror("Erreur", "L'auteur est requis")
                self.author_entry.focus()
                return
            
            if not year_str:
                messagebox.showerror("Erreur", "L'année est requise")
                self.year_entry.focus()
                return
            
            if not quantity_str:
                messagebox.showerror("Erreur", "La quantité est requise")
                self.quantity_entry.focus()
                return
            
            # Validate category
            if not category or category.strip() == "":
                messagebox.showerror("Erreur", "Veuillez sélectionner une catégorie")
                return
            
            # Validate year
            try:
                year = int(year_str)
                if year < 1450 or year > 2026:
                    messagebox.showerror("Erreur", "L'année doit être entre 1450 et 2026")
                    self.year_entry.focus()
                    return
            except ValueError:
                messagebox.showerror("Erreur", "L'année doit être un nombre valide")
                self.year_entry.focus()
                return
            
            # Validate quantity
            try:
                quantity = int(quantity_str)
                if quantity < 0:
                    messagebox.showerror("Erreur", "La quantité doit être positive")
                    self.quantity_entry.focus()
                    return
            except ValueError:
                messagebox.showerror("Erreur", "La quantité doit être un nombre valide")
                self.quantity_entry.focus()
                return
            
            # Generate auto-increment ID
            auto_id = self.book_service.generate_next_id()
            
            # Create book object without manual ID
            book = Book(
                id=auto_id,
                title=title,
                author=author,
                category=category,
                year=year,
                quantity=quantity,
                status="disponible"
            )
            
            success, message = self.book_service.add_book(book)
            
            if success:
                messagebox.showinfo("✅ Succès", f"Livre '{title}' ajouté avec succès !\nID: {auto_id}\nCatégorie: {category}")
                self.reset_form()
                self.refresh_callback()
                self.update_preview()
            else:
                messagebox.showerror("❌ Erreur", message)
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur inattendue s'est produite:\n{str(e)}")
    
    def reset_form(self):
        """Reset form fields with animation effect"""
        # Clear all entries
        self.title_entry.delete(0, 'end')
        self.author_entry.delete(0, 'end')
        self.year_entry.delete(0, 'end')
        self.quantity_entry.delete(0, 'end')
        
        # Reset category to default
        categories_from_config = Config.CATEGORIES if hasattr(Config, 'CATEGORIES') and Config.CATEGORIES else []
        default_categories = [
            "Roman",
            "Science-Fiction",
            "Fantasy", 
            "Policier",
            "Thriller",
            "Science",
            "Histoire",
            "Informatique",
            "Philosophie"
        ]
        categories = categories_from_config if categories_from_config else default_categories
        default_value = categories[0] if categories else "Roman"
        
        # Explicitly set the category variable
        self.category_var.set(default_value)
        
        # Force update the option menu display
        if hasattr(self, 'category_menu'):
            self.category_menu.set(default_value)
        
        # Set focus to title field for quick entry
        self.title_entry.focus()
        
        # Visual feedback
        self.reset_btn.configure(fg_color=Config.COLORS['accent_gray'])
        self.parent.after(200, lambda: self.reset_btn.configure(fg_color=Config.COLORS['accent_gray']))
    
    def update_preview(self):
        """Update preview table with recent books"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get all books and show last 6
        books = self.book_service.get_all_books()
        
        if not books:
            # Show empty state
            self.tree.insert('', 'end', values=(
                "Aucun livre", "", "", "", "", ""
            ))
            return
        
        # Show last 6 books
        for book in reversed(books[-6:]):
            # Status icon mapping
            status_icon = {
                'disponible': '✅ Disponible',
                'emprunté': '📖 Emprunté',
                'réservé': '🔒 Réservé'
            }.get(book.status, book.status.capitalize())
            
            self.tree.insert('', 'end', values=(
                book.title[:35] + ('...' if len(book.title) > 35 else ''),
                book.author[:25] + ('...' if len(book.author) > 25 else ''),
                book.category,
                book.year,
                book.quantity,
                status_icon
            ))