"""
Main application view with tabs
"""
import customtkinter as ctk
from src.config.settings import Config
from src.services.auth_service import AuthService
from src.services.book_service import BookService
from src.views.add_book_view import AddBookView
from src.views.inventory_view import InventoryView
from src.views.chatbot_view import ChatbotView

class MainView:
    def __init__(self, root, auth_service: AuthService):
        self.root = root
        self.auth_service = auth_service
        self.book_service = BookService()
        
        self.root.title(f"{Config.APP_NAME} - {auth_service.get_current_user()}")
        self.root.geometry(f"{Config.APP_WIDTH}x{Config.APP_HEIGHT}")
        self.root.configure(fg_color=Config.COLORS['background'])
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup main interface"""
        # Top bar
        top_bar = ctk.CTkFrame(
            self.root,
            height=60,
            fg_color=Config.COLORS['surface'],
            corner_radius=0
        )
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)
        
        # App title
        title_label = ctk.CTkLabel(
            top_bar,
            text="📚 ChatBook IA",
            font=Config.FONTS['title'],
            text_color=Config.COLORS['primary']
        )
        title_label.pack(side="left", padx=20, pady=10)
        
        # User info
        user_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        user_frame.pack(side="right", padx=20)
        
        user_label = ctk.CTkLabel(
            user_frame,
            text=f"👤 {self.auth_service.get_current_user()}",
            font=Config.FONTS['body'],
            text_color=Config.COLORS['text_secondary']
        )
        user_label.pack(side="left", padx=10)
        
        logout_btn = ctk.CTkButton(
            user_frame,
            text="Déconnexion",
            width=100,
            height=35,
            corner_radius=8,
            fg_color=Config.COLORS['accent_gray'],
            hover_color=Config.COLORS['accent_gray_hover'],
            font=Config.FONTS['body'],
            command=self.logout
        )
        logout_btn.pack(side="left")
        
        # Tab view
        self.tabview = ctk.CTkTabview(
            self.root,
            fg_color=Config.COLORS['surface'],
            segmented_button_fg_color=Config.COLORS['background'],
            segmented_button_selected_color=Config.COLORS['surface'],
            segmented_button_selected_hover_color=Config.COLORS['accent_green']
        )
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create tabs
        self.tabview.add("Ajouter un livre")
        self.tabview.add("Inventaire")
        self.tabview.add("Chatbot IA")
        
        # Initialize views
        self.add_book_view = AddBookView(self.tabview.tab("Ajouter un livre"), self.book_service, self.refresh_inventory)
        self.inventory_view = InventoryView(self.tabview.tab("Inventaire"), self.book_service)
        self.chatbot_view = ChatbotView(self.tabview.tab("Chatbot IA"), self.book_service)
        
        # Load initial data
        self.refresh_inventory()
    
    def refresh_inventory(self):
        """Refresh inventory view"""
        if hasattr(self, 'inventory_view'):
            self.inventory_view.refresh_table()
        if hasattr(self, 'chatbot_view'):
            self.chatbot_view.update_books_data()
    
    def logout(self):
        """Handle logout"""
        self.auth_service.logout()
        # Clear and recreate login view
        for widget in self.root.winfo_children():
            widget.destroy()
        from src.views.login_view import LoginView
        LoginView(self.root)