"""
Chatbot service using Google Gemini AI
"""
import json
from typing import List, Dict, Any
from src.models.book import Book
from src.utils.constants import Messages
from src.config.settings import Config

class ChatbotService:
    """Handle AI chatbot logic"""
    
    def __init__(self):
        self.books_data: List[Book] = []
        self.gemini_available = False
        self._init_gemini()
    
    def _init_gemini(self):
        """Initialize Gemini AI"""
        try:
            import warnings
            warnings.filterwarnings("ignore", category=FutureWarning)
            import google.generativeai as genai

            
            if Config.GEMINI_API_KEY:
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
                self.gemini_available = True
            else:
                print("No Gemini API key found")
        except Exception as e:
            print(f"Gemini initialization failed: {e}")
            self.gemini_available = False
    
    def update_books_data(self, books: List[Book]):
        """Update books data for context"""
        self.books_data = books
    
    def _format_books_context(self) -> str:
        """Format books data for AI context"""
        if not self.books_data:
            return "Aucun livre dans la bibliothèque pour le moment."
        
        context_lines = []
        for book in self.books_data[:50]:  # Limit to 50 books for context
            context_lines.append(
                f"- ID:{book.id} | {book.title} par {book.author} | "
                f"Catégorie:{book.category} | {book.get_status_display()}"
            )
        
        return "\n".join(context_lines)
    
    def _get_basic_response(self, question: str) -> str:
        """Fallback basic response when AI is unavailable"""
        question_lower = question.lower()
        
        # Check by ID
        if "id" in question_lower:
            for word in question.split():
                if word.isdigit():
                    for book in self.books_data:
                        if book.id == word:
                            return (f"Oui, le livre avec l'ID {book.id} existe.\n"
                                   f"Titre : {book.title}\n"
                                   f"Auteur : {book.author}\n"
                                   f"Statut : {book.get_status_display()}")
                    return f"Non, aucun livre avec l'ID {word} n'a été trouvé."
        
        # Check availability
        if any(word in question_lower for word in ["disponible", "existe", "est-ce que"]):
            # Look for book titles in question
            for book in self.books_data:
                if book.title.lower() in question_lower:
                    return (f"{book.title} par {book.author}\n"
                           f"Statut : {book.get_status_display()}")
        
        # Author search
        for book in self.books_data:
            if book.author.lower() in question_lower:
                author_books = [b for b in self.books_data if b.author.lower() == book.author.lower()]
                response = f"Œuvres de {book.author} :\n"
                for b in author_books:
                    response += f"- {b.title} : {b.get_status_display()}\n"
                return response
        
        # Recommendations
        if any(word in question_lower for word in ["recommande", "suggère", "conseille"]):
            available = [b for b in self.books_data if b.status == 'disponible']
            if available:
                response = "Voici mes recommandations :\n"
                for book in available[:3]:
                    response += f"- {book.title} par {book.author}\n"
                return response
            return "Désolé, aucun livre n'est disponible pour le moment."
        
        if self.books_data:
            return (f"Je peux vous aider à trouver des livres ! Notre bibliothèque contient "
                   f"{len(self.books_data)} livres. Posez-moi une question comme :\n"
                   f"- 'Est-ce que le livre avec l'ID 101 existe ?'\n"
                   f"- 'Le Petit Prince est-il disponible ?'\n"
                   f"- 'Recommande-moi un roman'")
        
        return "La bibliothèque est vide pour le moment. Ajoutez des livres pour que je puisse vous aider !"
    
    def get_response(self, question: str) -> str:
        """Get AI response for user question"""
        if not question or not question.strip():
            return "Veuillez poser une question."
        
        # Update context with current books
        context = self._format_books_context()
        
        # Use Gemini if available
        if self.gemini_available:
            try:
                prompt = f"""{Messages.SYSTEM_PROMPT.format(books_data=context)}

        Question de l'utilisateur: {question}

        Réponds de manière naturelle et utile en français:"""
                
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                print(f"Gemini error: {e}")
                return self._get_basic_response(question)
        
        # Fallback to basic response
        return self._get_basic_response(question)