"""
Login view
"""
import tkinter as tk
import customtkinter as ctk
from src.config.settings import Config
from src.services.auth_service import AuthService
from src.utils.constants import Messages

class LoginView:
    def __init__(self, root):
        self.root = root
        self.auth_service = AuthService()
        self._is_logging_in = False
        self.setup_ui()

    
    def setup_ui(self):
        """Setup login interface"""
        self.root.title(f"{Config.APP_NAME} - Connexion")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.configure(fg_color=Config.COLORS['background'])
        
        # Main container
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(expand=True, fill="both", padx=40, pady=40)
        
        # Title
        title = ctk.CTkLabel(
            main_frame,
            text="📚 ChatBook IA",
            font=Config.FONTS['title'],
            text_color=Config.COLORS['primary']
        )
        title.pack(pady=(0, 10))
        
        subtitle = ctk.CTkLabel(
            main_frame,
            text="Bibliothèque Intelligente",
            font=Config.FONTS['subtitle'],
            text_color=Config.COLORS['text_secondary']
        )
        subtitle.pack(pady=(0, 30))
        
        # Login Card
        card = ctk.CTkFrame(
            main_frame,
            fg_color=Config.COLORS['surface'],
            corner_radius=16
        )
        card.pack(fill="both", expand=True)
        
        # Email field
        email_label = ctk.CTkLabel(
            card,
            text="Email",
            font=Config.FONTS['body_bold'],
            text_color=Config.COLORS['text_secondary']
        )
        email_label.pack(anchor="w", padx=24, pady=(24, 5))
        
        self.email_entry = ctk.CTkEntry(
            card,
            placeholder_text="nadhem@gmail.com",
            height=44,
            corner_radius=8,
            border_color=Config.COLORS['border']
        )
        self.email_entry.pack(fill="x", padx=24, pady=(0, 15))
        self.email_entry.insert(0, "nadhem@gmail.com")
        
        # Password field
        pwd_label = ctk.CTkLabel(
            card,
            text="Mot de passe",
            font=Config.FONTS['body_bold'],
            text_color=Config.COLORS['text_secondary']
        )
        pwd_label.pack(anchor="w", padx=24, pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(
            card,
            placeholder_text="••••••••",
            height=44,
            corner_radius=8,
            border_color=Config.COLORS['border'],
            show="*"
        )
        self.password_entry.pack(fill="x", padx=24, pady=(0, 15))
        self.password_entry.insert(0, "123456789")
        
        # Login button
        self.login_btn = ctk.CTkButton(
            card,
            text="Se connecter",
            height=44,
            corner_radius=8,
            fg_color=Config.COLORS['accent_green'],
            hover_color=Config.COLORS['accent_green_hover'],
            font=Config.FONTS['button'],
            command=self.login
        )
        self.login_btn.pack(fill="x", padx=24, pady=(10, 24))
        
        # Bind Enter key (avoid double execution)
        self._enter_binding_id = self.root.bind('<Return>', self._on_enter)

        
        # Error label
        self.error_label = None
    
    def show_error(self, message):
        """Show error message"""
        if self.error_label:
            self.error_label.destroy()
        
        self.error_label = ctk.CTkLabel(
            self.root,
            text=message,
            text_color=Config.COLORS['error'],
            font=Config.FONTS['small']
        )
        self.error_label.pack(pady=(0, 20))
        self.root.after(3000, lambda: self.error_label.destroy() if self.error_label else None)
    
    def _on_enter(self, _event=None):
        # Prevent double execution (Enter + button click)
        if self._is_logging_in:
            return
        self.login()

    def login(self):
        """Handle login"""
        if self._is_logging_in:
            return
        self._is_logging_in = True
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        
        if self.auth_service.login(email, password):
            # Clear current window
            for widget in self.root.winfo_children():
                widget.destroy()
            # Import here to avoid circular import
            from src.views.main_view import MainView
            # Show main view
            MainView(self.root, self.auth_service)
        else:
            self.show_error(Messages.LOGIN_FAILED)