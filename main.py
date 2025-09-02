#!/usr/bin/env python3
"""
Lanceur principal pour AutoRappel - Version avec .env
"""

import os
import sys
import uvicorn
from pathlib import Path

# IMPORTANT: Charger le .env AVANT d'importer l'app
from dotenv import load_dotenv

# Charger le fichier .env
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Ajouter le répertoire racine au path
sys.path.append(str(Path(__file__).parent))

def main():
    """Démarrer l'application FastAPI"""
    try:
        # Render fournit la variable PORT automatiquement, sinon 8000
        port = int(os.environ.get("PORT", 8000))
        host = "0.0.0.0"
        
        # Debug: Afficher les variables chargées
        print(f"🚀 Démarrage d'AutoRappel sur {host}:{port}")
        print(f"📧 Email configuré: {os.environ.get('GMAIL_EMAIL', 'Non configuré')}")
        
        recipients = os.environ.get('EMAIL_RECIPIENTS', '')
        recipient_count = len(recipients.split(',')) if recipients else 0
        print(f"📬 Destinataires: {recipient_count}")
        
        if not os.environ.get('GMAIL_EMAIL'):
            print("⚠️  ATTENTION: Variables d'environnement non chargées!")
            print(f"📁 Cherche .env dans: {env_path}")
            print(f"📁 .env existe: {env_path.exists()}")
        
        # Démarrage du serveur
        uvicorn.run(
            "api.rappel_secure:app",
            host=host,
            port=port,
            reload=os.environ.get("RELOAD", "false").lower() == "true",
            log_level="info",
            access_log=True
        )
        
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()