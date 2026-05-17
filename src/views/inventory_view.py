"""
Inventory view with search and actions
"""
import customtkinter as ctk
from tkinter import ttk, messagebox, simpledialog
from src.config.settings import Config
from src.models.book import Book
from src.services.book_service import BookService

class InventoryView:
    def __init__(self, parent, book_service: BookService):
        self.parent = parent
        self.book_service = book_service
        self.setup_ui()
    
    def setup_ui(self):
        """Setup inventory interface"""
        self.parent.configure(fg_color=Config.COLORS['surface'])
        
        # Main container
        main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Search bar with action buttons
        search_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 20))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Rechercher par titre, auteur ou ID...",
            height=44,
            corner_radius=8,
            border_color=Config.COLORS['border'],
            font=Config.FONTS['body']
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.search_btn = ctk.CTkButton(
            search_frame,
            text="Rechercher",
            height=44,
            width=120,
            corner_radius=8,
            fg_color=Config.COLORS['accent_green'],
            hover_color=Config.COLORS['accent_green_hover'],
            font=Config.FONTS['button'],
            command=self.search_books
        )
        self.search_btn.pack(side="left", padx=(0, 10))
        
        self.refresh_btn = ctk.CTkButton(
            search_frame,
            text="⟳ Actualiser",
            height=44,
            width=120,
            corner_radius=8,
            fg_color=Config.COLORS['accent_gray'],
            hover_color=Config.COLORS['accent_gray_hover'],
            font=Config.FONTS['button'],
            command=self.refresh_table
        )
        self.refresh_btn.pack(side="left")
        
        # Action buttons bar
        action_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        action_frame.pack(fill="x", pady=(0, 20))
        
        # Helper function to safely get colors with fallbacks
        def get_color(color_key, fallback='primary'):
            return Config.COLORS.get(color_key, Config.COLORS.get(fallback, '#1E293B'))
        
        # Edit button
        self.edit_btn = ctk.CTkButton(
            action_frame,
            text="✏️ Modifier",
            height=40,
            width=130,
            corner_radius=8,
            fg_color=get_color('accent_blue', 'primary'),
            hover_color=get_color('accent_blue_hover', 'primary_hover'),
            font=Config.FONTS['button'],
            command=self.edit_selected
        )
        self.edit_btn.pack(side="left", padx=(0, 10))
        
        # Delete button
        self.delete_btn = ctk.CTkButton(
            action_frame,
            text="🗑️ Supprimer",
            height=40,
            width=130,
            corner_radius=8,
            fg_color=get_color('accent_red', 'error'),
            hover_color=get_color('accent_red_hover', 'error'),
            font=Config.FONTS['button'],
            command=self.delete_selected
        )
        self.delete_btn.pack(side="left", padx=(0, 10))
        
        # Status button
        self.status_btn = ctk.CTkButton(
            action_frame,
            text="📊 Changer Statut",
            height=40,
            width=150,
            corner_radius=8,
            fg_color=get_color('accent_orange', 'warning'),
            hover_color=get_color('accent_orange_hover', 'warning'),
            font=Config.FONTS['button'],
            command=self.change_status
        )
        self.status_btn.pack(side="left")
        
        # Statistics frame
        self.stats_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        self.stats_frame.pack(fill="x", pady=(0, 20))
        self.update_statistics()
        
        # Treeview for books
        tree_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        tree_frame.pack(fill="both", expand=True)
        
        # Create scrollbars
        scroll_y = ttk.Scrollbar(tree_frame, orient="vertical")
        scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Configure style for Treeview
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Inventory.Treeview",
            font=('Segoe UI', 11),
            rowheight=35,
            background='white',
            fieldbackground='white',
            foreground='#2C3E50'
        )
        style.configure(
            "Inventory.Treeview.Heading",
            font=('Segoe UI', 11, 'bold'),
            background=Config.COLORS['primary'],
            foreground='white',
            relief='flat'
        )
        style.map('Inventory.Treeview.Heading',
                  background=[('active', Config.COLORS.get('primary_hover', Config.COLORS['primary']))])
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'Titre', 'Auteur', 'Catégorie', 'Année', 'Quantité', 'Statut'),
            show='headings',
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            style="Inventory.Treeview"
        )
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # Define columns with icons
        self.tree.heading('ID', text='🆔 ID', command=lambda: self.sort_by('id'))
        self.tree.heading('Titre', text='📚 Titre', command=lambda: self.sort_by('title'))
        self.tree.heading('Auteur', text='✍️ Auteur', command=lambda: self.sort_by('author'))
        self.tree.heading('Catégorie', text='📑 Catégorie', command=lambda: self.sort_by('category'))
        self.tree.heading('Année', text='📅 Année', command=lambda: self.sort_by('year'))
        self.tree.heading('Quantité', text='🔢 Qté', command=lambda: self.sort_by('quantity'))
        self.tree.heading('Statut', text='✅ Statut', command=lambda: self.sort_by('status'))
        
        # Set column widths
        self.tree.column('ID', width=70, minwidth=70)
        self.tree.column('Titre', width=300, minwidth=200)
        self.tree.column('Auteur', width=200, minwidth=150)
        self.tree.column('Catégorie', width=150, minwidth=100)
        self.tree.column('Année', width=80, minwidth=80)
        self.tree.column('Quantité', width=80, minwidth=80)
        self.tree.column('Statut', width=200, minwidth=150)
        
        # Pack treeview
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scroll_y.pack(side="right", fill="y", pady=10)
        scroll_x.pack(side="bottom", fill="x", padx=10)
        
        # Bind events
        self.tree.bind('<Double-Button-1>', self.edit_book)
        self.tree.bind('<Delete>', lambda e: self.delete_selected())
        self.tree.bind('<Control-e>', lambda e: self.edit_selected())
        self.tree.bind('<Control-d>', lambda e: self.delete_selected())
        
        # Right-click context menu
        import tkinter as tk
        self.context_menu = tk.Menu(self.tree, tearoff=0)
        self.context_menu.add_command(label="✏️ Modifier", command=self.edit_selected, accelerator="Ctrl+E")
        self.context_menu.add_command(label="🗑️ Supprimer", command=self.delete_selected, accelerator="Del")
        self.context_menu.add_separator()
        self.context_menu.add_command(label="📊 Changer Statut", command=self.change_status)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="⟳ Actualiser", command=self.refresh_table, accelerator="F5")
        
        self.tree.bind('<Button-3>', self.show_context_menu)
        
        # Bind keyboard shortcuts
        self.parent.bind('<Control-e>', lambda e: self.edit_selected())
        self.parent.bind('<Control-d>', lambda e: self.delete_selected())
        self.parent.bind('<F5>', lambda e: self.refresh_table())
        
        # Load initial data
        self.refresh_table()
    
    def update_statistics(self):
        """Update statistics display"""
        # Clear existing
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        stats = self.book_service.get_statistics()
        
        # Create stat cards
        stat_configs = [
            ("📚 Total Livres", stats['total_books'], Config.COLORS['primary']),
            ("✅ Disponibles", stats['available_books'], Config.COLORS['accent_green']),
            ("📖 Empruntés", stats['borrowed_books'], Config.COLORS.get('accent_orange', Config.COLORS['warning'])),
            ("🔒 Réservés", stats['reserved_books'], Config.COLORS.get('accent_red', Config.COLORS['error'])),
            ("📊 Total Exemplaires", stats['total_copies'], Config.COLORS.get('accent_blue', Config.COLORS['primary']))
        ]
        
        for i, (label, value, color) in enumerate(stat_configs):
            card = ctk.CTkFrame(self.stats_frame, corner_radius=8, border_width=1, border_color=Config.COLORS['border'])
            card.pack(side="left", fill="both", expand=True, padx=5, pady=5)
            
            ctk.CTkLabel(
                card,
                text=str(value),
                font=('Segoe UI', 24, 'bold'),
                text_color=color
            ).pack(pady=(10, 0))
            
            ctk.CTkLabel(
                card,
                text=label,
                font=Config.FONTS['small'],
                text_color=Config.COLORS['text_secondary']
            ).pack(pady=(0, 10))
    
    def refresh_table(self):
        """Refresh the book table"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add books
        books = self.book_service.get_all_books()
        for book in books:
            self.tree.insert('', 'end', iid=book.id, values=(
                book.id, 
                book.title, 
                book.author, 
                book.category,
                book.year, 
                book.quantity, 
                book.get_status_display()
            ))
        
        self.update_statistics()
    
    def search_books(self):
        """Search books"""
        query = self.search_entry.get().strip()
        
        if not query:
            self.refresh_table()
            return
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add search results
        books = self.book_service.search_books(query)
        for book in books:
            self.tree.insert('', 'end', iid=book.id, values=(
                book.id, book.title, book.author, book.category,
                book.year, book.quantity, book.get_status_display()
            ))
    
    def edit_book(self, event):
        """Edit selected book"""
        self.edit_selected()
    
    def edit_selected(self):
        """Edit selected book"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un livre à modifier")
            return
        
        book_id = selection[0]
        book = self.book_service.get_book_by_id(book_id)
        
        if not book:
            messagebox.showerror("Erreur", "Livre non trouvé")
            return
        
        # Create edit dialog
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title(f"✏️ Modifier - {book.title}")
        dialog.geometry("550x650")
        dialog.configure(fg_color=Config.COLORS['surface'])
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (550 // 2)
        y = (dialog.winfo_screenheight() // 2) - (650 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Form fields with better layout
        main_form = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        main_form.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Title
        ctk.CTkLabel(main_form, text="📚 Titre *", font=Config.FONTS['body_bold']).pack(anchor="w", pady=(0, 5))
        title_entry = ctk.CTkEntry(main_form, height=40, corner_radius=8, font=Config.FONTS['body'])
        title_entry.pack(fill="x", pady=(0, 15))
        title_entry.insert(0, book.title)
        
        # Author
        ctk.CTkLabel(main_form, text="✍️ Auteur *", font=Config.FONTS['body_bold']).pack(anchor="w", pady=(0, 5))
        author_entry = ctk.CTkEntry(main_form, height=40, corner_radius=8, font=Config.FONTS['body'])
        author_entry.pack(fill="x", pady=(0, 15))
        author_entry.insert(0, book.author)
        
        # Category
        categories = Config.CATEGORIES if hasattr(Config, 'CATEGORIES') and Config.CATEGORIES else [
            "Roman", "Science-Fiction", "Fantasy", "Policier", "Thriller", 
            "Science", "Histoire", "Informatique", "Philosophie"
        ]
        ctk.CTkLabel(main_form, text="📑 Catégorie *", font=Config.FONTS['body_bold']).pack(anchor="w", pady=(0, 5))
        category_var = ctk.StringVar(value=book.category)
        category_menu = ctk.CTkOptionMenu(
            main_form, 
            values=categories, 
            variable=category_var, 
            height=40, 
            corner_radius=8,
            font=Config.FONTS['body']
        )
        category_menu.pack(fill="x", pady=(0, 15))
        
        # Year
        ctk.CTkLabel(main_form, text="📅 Année *", font=Config.FONTS['body_bold']).pack(anchor="w", pady=(0, 5))
        year_entry = ctk.CTkEntry(main_form, height=40, corner_radius=8, font=Config.FONTS['body'])
        year_entry.pack(fill="x", pady=(0, 15))
        year_entry.insert(0, str(book.year))
        
        # Quantity
        ctk.CTkLabel(main_form, text="🔢 Quantité *", font=Config.FONTS['body_bold']).pack(anchor="w", pady=(0, 5))
        quantity_entry = ctk.CTkEntry(main_form, height=40, corner_radius=8, font=Config.FONTS['body'])
        quantity_entry.pack(fill="x", pady=(0, 15))
        quantity_entry.insert(0, str(book.quantity))
        
        # Status
        ctk.CTkLabel(main_form, text="✅ Statut", font=Config.FONTS['body_bold']).pack(anchor="w", pady=(0, 5))
        status_var = ctk.StringVar(value=book.status)
        status_menu = ctk.CTkOptionMenu(
            main_form, 
            values=['disponible', 'emprunté', 'réservé'], 
            variable=status_var, 
            height=40, 
            corner_radius=8,
            font=Config.FONTS['body']
        )
        status_menu.pack(fill="x", pady=(0, 20))
        
        # Button frame
        button_frame = ctk.CTkFrame(main_form, fg_color="transparent")
        button_frame.pack(fill="x", pady=(10, 0))
        
        def save_changes():
            try:
                # Validation
                title = title_entry.get().strip()
                author = author_entry.get().strip()
                
                if not title or not author:
                    messagebox.showerror("Erreur", "Le titre et l'auteur sont requis")
                    return
                
                year = int(year_entry.get().strip())
                if year < 1450 or year > 2026:
                    messagebox.showerror("Erreur", "Année invalide (1450-2026)")
                    return
                
                quantity = int(quantity_entry.get().strip())
                if quantity < 0:
                    messagebox.showerror("Erreur", "La quantité doit être positive")
                    return
                
                updated_book = Book(
                    id=book.id,
                    title=title,
                    author=author,
                    category=category_var.get(),
                    year=year,
                    quantity=quantity,
                    status=status_var.get()
                )
                
                success, message = self.book_service.update_book(book.id, updated_book)
                
                if success:
                    messagebox.showinfo("✅ Succès", message)
                    self.refresh_table()
                    dialog.destroy()
                else:
                    messagebox.showerror("❌ Erreur", message)
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides")
        
        save_btn = ctk.CTkButton(
            button_frame, 
            text="💾 Enregistrer les modifications", 
            height=44, 
            corner_radius=8,
            fg_color=Config.COLORS['accent_green'], 
            hover_color=Config.COLORS['accent_green_hover'],
            font=Config.FONTS['button'],
            command=save_changes
        )
        save_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        cancel_btn = ctk.CTkButton(
            button_frame, 
            text="❌ Annuler", 
            height=44, 
            corner_radius=8,
            fg_color=Config.COLORS['accent_gray'], 
            hover_color=Config.COLORS['accent_gray_hover'],
            font=Config.FONTS['button'],
            command=dialog.destroy
        )
        cancel_btn.pack(side="left", fill="x", expand=True)
    
    def delete_selected(self):
        """Delete selected book"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un livre à supprimer")
            return
        
        book_id = selection[0]
        book = self.book_service.get_book_by_id(book_id)
        
        if not book:
            messagebox.showerror("Erreur", "Livre non trouvé")
            return
        
        # Confirmation dialog with details
        confirm = messagebox.askyesno(
            "Confirmation de suppression", 
            f"⚠️ Êtes-vous sûr de vouloir supprimer le livre suivant ?\n\n"
            f"📚 Titre: {book.title}\n"
            f"✍️ Auteur: {book.author}\n"
            f"🆔 ID: {book.id}\n\n"
            f"Cette action est irréversible !",
            icon='warning'
        )
        
        if confirm:
            success, message = self.book_service.delete_book(book_id)
            if success:
                messagebox.showinfo("✅ Succès", message)
                self.refresh_table()
            else:
                messagebox.showerror("❌ Erreur", message)
    
    def change_status(self):
        """Change status of selected book"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un livre")
            return
        
        book_id = selection[0]
        book = self.book_service.get_book_by_id(book_id)
        
        if not book:
            messagebox.showerror("Erreur", "Livre non trouvé")
            return
        
        # Create status change dialog
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title(f"📊 Changer le statut - {book.title}")
        dialog.geometry("400x350")
        dialog.configure(fg_color=Config.COLORS['surface'])
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (350 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Content
        main_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        ctk.CTkLabel(
            main_frame, 
            text=f"Livre: {book.title}", 
            font=Config.FONTS.get('title_small', ('Segoe UI', 18, 'bold')),
            text_color=Config.COLORS['primary']
        ).pack(pady=(0, 10))
        
        ctk.CTkLabel(
            main_frame, 
            text=f"Auteur: {book.author}", 
            font=Config.FONTS['body']
        ).pack(pady=(0, 20))
        
        ctk.CTkLabel(
            main_frame, 
            text="Nouveau statut:", 
            font=Config.FONTS['body_bold']
        ).pack(anchor="w", pady=(0, 5))
        
        status_var = ctk.StringVar(value=book.status)
        status_menu = ctk.CTkOptionMenu(
            main_frame,
            values=['disponible', 'emprunté', 'réservé'],
            variable=status_var,
            height=40,
            corner_radius=8,
            font=Config.FONTS['body']
        )
        status_menu.pack(fill="x", pady=(0, 20))
        
        def apply_status_change():
            updated_book = Book(
                id=book.id,
                title=book.title,
                author=book.author,
                category=book.category,
                year=book.year,
                quantity=book.quantity,
                status=status_var.get()
            )
            
            success, message = self.book_service.update_book(book.id, updated_book)
            
            if success:
                messagebox.showinfo("✅ Succès", message)
                self.refresh_table()
                dialog.destroy()
            else:
                messagebox.showerror("❌ Erreur", message)
        
        apply_btn = ctk.CTkButton(
            main_frame,
            text="✅ Appliquer le changement",
            height=44,
            corner_radius=8,
            fg_color=Config.COLORS['accent_green'],
            hover_color=Config.COLORS['accent_green_hover'],
            font=Config.FONTS['button'],
            command=apply_status_change
        )
        apply_btn.pack(fill="x", pady=(10, 10))
        
        cancel_btn = ctk.CTkButton(
            main_frame,
            text="❌ Annuler",
            height=40,
            corner_radius=8,
            fg_color=Config.COLORS['accent_gray'],
            hover_color=Config.COLORS['accent_gray_hover'],
            font=Config.FONTS['button'],
            command=dialog.destroy
        )
        cancel_btn.pack(fill="x")
    
    def show_context_menu(self, event):
        """Show context menu"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def sort_by(self, column):
        """Sort table by column"""
        items = [(self.tree.set(item, column), item) for item in self.tree.get_children('')]
        items.sort()
        
        for index, (val, item) in enumerate(items):
            self.tree.move(item, '', index)