"""
Chatbot view with AI conversation
"""
import customtkinter as ctk
from tkinter import messagebox
from src.config.settings import Config
from src.services.book_service import BookService
from src.services.chatbot_service import ChatbotService
import threading

class ChatbotView:
    def __init__(self, parent, book_service: BookService):
        self.parent = parent
        self.book_service = book_service
        self.chatbot = ChatbotService()
        self.setup_ui()
        self.update_books_data()
    
    def setup_ui(self):
        """Setup chatbot interface"""
        self.parent.configure(fg_color=Config.COLORS['surface'])
        
        # Main container
        main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            main_frame,
            text="🤖 Assistant IA ChatBook",
            font=Config.FONTS['title'],
            text_color=Config.COLORS['primary']
        )
        title.pack(anchor="w", pady=(0, 10))
        
        subtitle = ctk.CTkLabel(
            main_frame,
            text="Posez vos questions sur la bibliothèque en langage naturel",
            font=Config.FONTS['subtitle'],
            text_color=Config.COLORS['text_secondary']
        )
        subtitle.pack(anchor="w", pady=(0, 20))
        
        # Gemini status indicator
        status_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        status_frame.pack(fill="x", pady=(0, 15))
        
        if self.chatbot.gemini_available:
            status_text = "✅ Mode IA avancé (Gemini) - Actif"
            status_color = Config.COLORS['accent_green']
        else:
            status_text = "⚠️ Mode standard - API Gemini non configurée"
            status_color = Config.COLORS['warning']
        
        self.status_badge = ctk.CTkLabel(
            status_frame,
            text=status_text,
            font=Config.FONTS['small'],
            text_color=status_color,
            fg_color=Config.COLORS['background'],
            corner_radius=10,
            padx=10,
            pady=5
        )
        self.status_badge.pack(side="left")
        
        # Suggested questions
        suggestions_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        suggestions_frame.pack(fill="x", pady=(0, 20))
        
        suggestions_label = ctk.CTkLabel(
            suggestions_frame,
            text="💡 Questions suggérées:",
            font=Config.FONTS['body_bold'],
            text_color=Config.COLORS['text_secondary']
        )
        suggestions_label.pack(anchor="w", pady=(0, 10))
        
        suggestions_buttons_frame = ctk.CTkFrame(suggestions_frame, fg_color="transparent")
        suggestions_buttons_frame.pack(fill="x")
        
        suggestions = [
            ("🔍 Livre avec ID 101", "Livre avec ID 101"),
            ("✅ Disponibilité des livres", "Quels livres sont disponibles ?"),
            ("📖 Livres de Victor Hugo", "Livres de Victor Hugo"),
            ("💡 Recommande un livre", "Recommande-moi un livre à lire"),
            ("📊 Statistiques", "Statistiques de la bibliothèque")
        ]
        
        for i, (display, query) in enumerate(suggestions):
            chip = ctk.CTkButton(
                suggestions_buttons_frame,
                text=display,
                height=35,
                corner_radius=20,
                fg_color="white",
                text_color=Config.COLORS['primary'],
                border_color=Config.COLORS['border'],
                border_width=1,
                hover_color=Config.COLORS['background'],
                font=Config.FONTS['body'],
                command=lambda q=query: self.ask_question(q)
            )
            chip.pack(side="left", padx=5, pady=5)
        
        # Chat display area
        chat_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        chat_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Text widget for conversation
        self.chat_display = ctk.CTkTextbox(
            chat_frame,
            font=('Segoe UI', 12),
            wrap='word',
            corner_radius=12,
            fg_color="white"
        )
        self.chat_display.pack(fill="both", expand=True, padx=10, pady=10)
        self.chat_display.configure(state="disabled")
        
        # Input area
        input_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        input_frame.pack(fill="x")
        
        self.input_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Posez votre question ici... (ex: 'Livres de Victor Hugo' ou 'Livre 101 est disponible ?')",
            height=50,
            corner_radius=25,
            border_color=Config.COLORS['border'],
            font=Config.FONTS['body']
        )
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.send_btn = ctk.CTkButton(
            input_frame,
            text="📤 Envoyer",
            height=50,
            width=120,
            corner_radius=25,
            fg_color=Config.COLORS['accent_green'],
            hover_color=Config.COLORS['accent_green_hover'],
            font=Config.FONTS['button'],
            command=self.send_message
        )
        self.send_btn.pack(side="right")
        
        # Clear chat button
        self.clear_btn = ctk.CTkButton(
            input_frame,
            text="🗑️ Effacer",
            height=50,
            width=100,
            corner_radius=25,
            fg_color=Config.COLORS['accent_gray'],
            hover_color=Config.COLORS['accent_gray_hover'],
            font=Config.FONTS['button'],
            command=self.clear_chat
        )
        self.clear_btn.pack(side="right", padx=(0, 10))
        
        # Bind Enter key
        self.input_entry.bind('<Return>', lambda e: self.send_message())
        
        # Welcome message
        self.add_welcome_message()
    
    def add_welcome_message(self):
        """Add welcome message to chat"""
        welcome_text = """Bonjour ! 👋

Je suis votre **assistant bibliothécaire intelligent**. Je peux vous aider à :

📚 **Rechercher des livres** par titre, auteur ou ID
✅ **Vérifier la disponibilité** d'un livre
💡 **Obtenir des recommandations** personnalisées
📊 **Consulter les statistiques** de la bibliothèque

**Exemples de questions :**
• "Livre avec ID 101 existe ?"
• "Quels livres de Victor Hugo avons-nous ?"
• "Les Misérables est-il disponible ?"
• "Recommande-moi un bon roman"
• "Combien de livres sont disponibles ?"

Comment puis-je vous aider aujourd'hui ? 🎯"""
        
        self.add_message("🤖 Assistant", welcome_text)
    
    def update_books_data(self):
        """Update books data in chatbot"""
        books = self.book_service.get_all_books()
        self.chatbot.update_books_data(books)
    
    def add_message(self, sender: str, message: str):
        """Add message to chat display"""
        self.chat_display.configure(state="normal")
        
        # Format message
        if sender == "🤖 Assistant":
            self.chat_display.insert("end", f"\n{sender}\n", "assistant")
            self.chat_display.insert("end", f"{'─' * 55}\n", "separator")
            self.chat_display.insert("end", f"{message}\n\n", "assistant_text")
        else:
            self.chat_display.insert("end", f"\n{sender}\n", "user")
            self.chat_display.insert("end", f"{'─' * 55}\n", "separator")
            self.chat_display.insert("end", f"{message}\n\n", "user_text")
        
        # Configure tags
        self.chat_display.tag_config("assistant", foreground=Config.COLORS['accent_green'], font=('Segoe UI', 13, 'bold'))
        self.chat_display.tag_config("user", foreground=Config.COLORS['primary'], font=('Segoe UI', 13, 'bold'))
        self.chat_display.tag_config("separator", foreground=Config.COLORS['border'])
        self.chat_display.tag_config("assistant_text", foreground=Config.COLORS['text_primary'], font=('Segoe UI', 12))
        self.chat_display.tag_config("user_text", foreground=Config.COLORS['text_secondary'], font=('Segoe UI', 12))
        
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")
    
    def send_message(self):
        """Send user message and get response"""
        question = self.input_entry.get().strip()
        
        if not question:
            messagebox.showwarning("Attention", "Veuillez entrer une question")
            return
        
        # Clear input
        self.input_entry.delete(0, 'end')
        
        # Update books data before answering
        self.update_books_data()
        
        # Add user message
        self.add_message("👤 Vous", question)
        
        # Disable send button during processing
        self.send_btn.configure(state="disabled", text="⏳ Réflexion...")
        self.parent.update()
        
        # Use threading to prevent UI freeze
        def process_response():
            try:
                # Get AI response
                response = self.chatbot.get_response(question)
                self.parent.after(0, lambda: self.add_message("🤖 Assistant", response))
            except Exception as e:
                error_msg = f"Désolé, une erreur s'est produite : {str(e)}"
                self.parent.after(0, lambda: self.add_message("🤖 Assistant", error_msg))
            finally:
                # Re-enable send button
                self.parent.after(0, lambda: self.send_btn.configure(state="normal", text="📤 Envoyer"))
        
        # Start processing in background thread
        thread = threading.Thread(target=process_response)
        thread.daemon = True
        thread.start()
    
    def ask_question(self, question: str):
        """Ask predefined question"""
        self.input_entry.delete(0, 'end')
        self.input_entry.insert(0, question)
        self.send_message()
    
    def clear_chat(self):
        """Clear chat display"""
        if messagebox.askyesno("Confirmation", "Voulez-vous effacer toute la conversation ?"):
            self.chat_display.configure(state="normal")
            self.chat_display.delete("1.0", "end")
            self.chat_display.configure(state="disabled")
            self.add_welcome_message()