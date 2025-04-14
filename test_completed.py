import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.controllers.app_controller import AppController

def main():
    """Run the application"""
    print("=== Iniciando Aplicación ===")
    
    app = AppController()
    app.run()

if __name__ == "__main__":
    main()