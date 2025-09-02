#!/usr/bin/env python3
"""
AutoRappel - Lanceur principal de l'application
"""

import uvicorn
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

if __name__ == "__main__":
    # Configuration du serveur
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    print("🚀 Démarrage d'AutoRappel...")
    print(f"📡 Serveur accessible sur: http://{host}:{port}")
    print(f"📚 Documentation API: http://{host}:{port}/docs")
    print(f"🔄 Mode reload: {'Activé' if reload else 'Désactivé'}")
    print("=" * 50)
    
    # Lancer le serveur
    uvicorn.run(
        "api.rappel_secure:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
