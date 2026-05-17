#!/usr/bin/env python3
"""
ChatBook IA - Bibliothèque Intelligente
Main application entry point
"""
import sys
import os
import subprocess
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Try to import customtkinter, show helpful error if not installed
try:
    import customtkinter as ctk
except ImportError:
    print("=" * 60)
    print("ERROR: CustomTkinter is not installed!")
    print("=" * 60)
    print("\nPlease install the required packages:")
    print("  pip install customtkinter Pillow python-dotenv")
    print("\nFor AI features (optional):")
    print("  pip install google-generativeai")
    print("\nThen run the application again.")
    print("=" * 60)
    
    # Ask if user wants to install dependencies automatically
    try:
        response = input("\nDo you want to install dependencies automatically? (y/n): ")
        if response.lower() == 'y':
            print("\nInstalling dependencies...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", 
                                 "customtkinter", "Pillow", "python-dotenv"])
            print("\n✅ Dependencies installed successfully!")
            print("Please run the application again.")
        else:
            print("\nPlease install dependencies manually and run again.")
    except:
        pass
    
    input("\nPress Enter to exit...")
    sys.exit(1)

from src.config.settings import Config
from src.database.db_manager import DatabaseManager
from src.views.login_view import LoginView

def setup_application():
    """Setup application before launch"""
    print("=" * 50)
    print("🚀 ChatBook IA - Starting Application")
    print("=" * 50)
    
    try:
        # Ensure data directory exists
        Config.ensure_data_dir()
        print("✓ Data directory initialized")
        
        # Initialize database
        db = DatabaseManager()
        print("✓ Database initialized")
        
        # Add sample books if needed
        db.add_sample_books()
        print("✓ Sample books loaded")
        
        print("=" * 50)
        print("✅ Application ready!")
        print("=" * 50)
        
    except Exception as e:
        print(f"⚠️ Warning: {e}")
        print("The application may still work, but some features might be limited.")
    
    # Configure CustomTkinter with modern settings
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    
    # Set global scaling for better readability (Windows)
    try:
        ctk.set_widget_scaling(1.0)
        ctk.set_window_scaling(1.0)
    except:
        pass

def check_dependencies():
    """Check if all required dependencies are installed"""
    missing_packages = []
    
    # Check for optional AI package
    try:
        import google.generativeai
        print("✓ Gemini AI package found")
    except ImportError:
        print("⚠️ Gemini AI package not installed (optional for AI features)")
        print("  Install with: pip install google-generativeai")
    
    # Check for Pillow
    try:
        import PIL
        print("✓ Pillow package found")
    except ImportError:
        missing_packages.append("Pillow")
    
    return missing_packages

def create_desktop_shortcut():
    """Create desktop shortcut (Windows only)"""
    if sys.platform == "win32":
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            path = os.path.join(desktop, "ChatBook IA.lnk")
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = f'"{os.path.abspath(__file__)}"'
            shortcut.WorkingDirectory = os.path.dirname(os.path.abspath(__file__))
            shortcut.IconLocation = sys.executable
            shortcut.save()
            
            print("✓ Desktop shortcut created")
        except:
            pass

def main():
    """Main application entry point"""
    # Print banner
    print("""
    ╔══════════════════════════════════════════╗
    ║     📚 ChatBook IA - Bibliothèque       ║
    ║         Intelligence Artificielle        ║
    ╚══════════════════════════════════════════╝
    """)
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"\n⚠️ Missing packages: {', '.join(missing)}")
        print("Install with: pip install " + " ".join(missing))
    
    # Setup application
    setup_application()
    
    # Create desktop shortcut (optional)
    try:
        create_desktop_shortcut()
    except:
        pass
    
    # Create root window with modern styling
    root = ctk.CTk()
    root.title(Config.APP_NAME)
    
    # Set window size
    window_width = Config.APP_WIDTH
    window_height = Config.APP_HEIGHT
    
    # Set minimum window size
    root.minsize(900, 600)
    
    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Calculate position to center window
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    
    # Set window geometry
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Set window icon (if available)
    try:
        icon_path = Path(__file__).parent / "assets" / "icon.ico"
        if icon_path.exists():
            root.iconbitmap(str(icon_path))
    except:
        pass
    
    # Configure root window grid for responsiveness
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    # Set protocol for window close
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    
    # Launch login view
    try:
        login_view = LoginView(root)
    except Exception as e:
        print(f"❌ Error loading login view: {e}")
        # Show error dialog
        from tkinter import messagebox
        messagebox.showerror(
            "Erreur de démarrage",
            f"Une erreur s'est produite lors du démarrage de l'application:\n\n{str(e)}\n\n"
            "Veuillez vérifier votre installation et réessayer."
        )
        sys.exit(1)
    
    # Start main loop
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n\n👋 Application fermée par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        sys.exit(1)

def on_closing(root):
    """Handle window closing event"""
    from tkinter import messagebox
    
    # Ask for confirmation
    if messagebox.askyesno("Quitter", "Êtes-vous sûr de vouloir quitter ChatBook IA ?"):
        print("\n👋 Au revoir ! Merci d'avoir utilisé ChatBook IA")
        root.destroy()
        sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)