"""
Application constants and messages
"""

class Messages:
    # Success Messages
    BOOK_ADDED = "✅ Livre ajouté avec succès !"
    BOOK_UPDATED = "✅ Livre modifié avec succès !"
    BOOK_DELETED = "✅ Livre supprimé avec succès !"
    LOGIN_SUCCESS = "✅ Connexion réussie !"
    
    # Error Messages
    LOGIN_FAILED = "❌ Email ou mot de passe incorrect"
    BOOK_NOT_FOUND = "❌ Livre non trouvé"
    INVALID_YEAR = "❌ Année invalide (doit être entre 1450 et 2026)"
    INVALID_QUANTITY = "❌ Quantité invalide (doit être un nombre positif)"
    EMPTY_FIELDS = "❌ Veuillez remplir tous les champs"
    GEMINI_ERROR = "⚠️ Service IA temporairement indisponible. Utilisation du mode basique."
    
    # Chatbot Prompts
    SYSTEM_PROMPT = """Tu es un assistant bibliothécaire professionnel pour ChatBook IA. 
    Tu dois répondre aux questions sur les livres disponibles dans notre catalogue.
    Sois courtois, précis et utile. Réponds en français.
    Utilise les données suivantes pour répondre: {books_data}
    
    Règles:
    - Si un livre est demandé par ID, vérifie son existence et donne ses détails
    - Pour les questions de disponibilité, précise le statut exact
    - Pour les recommandations, propose 2-3 livres pertinents
    - Si un auteur est mentionné, liste tous ses livres disponibles
    """
    
    # CSV Headers
    CSV_BOOKS_HEADERS = ['id', 'title', 'author', 'category', 'year', 'quantity', 'status', 'borrower', 'return_date']
    CSV_USERS_HEADERS = ['email', 'password']