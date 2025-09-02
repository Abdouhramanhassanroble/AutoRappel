#!/bin/bash

echo "🚀 Démarrage d'AutoRappel..."
echo "================================"

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérifier si le fichier .env existe
if [ ! -f ".env" ]; then
    echo "⚠️  Fichier .env non trouvé !"
    echo "📝 Copiez env.example vers .env et configurez vos données :"
    echo "   cp env.example .env"
    echo "   # Puis éditez .env avec vos vraies données"
    exit 1
fi

# Installer les dépendances si nécessaire
echo "📦 Installation des dépendances..."
pip3 install -r requirements.txt

# Démarrer l'application
echo "🌐 Lancement de l'application..."
echo "📡 URL: http://localhost:8000"
echo "📚 Documentation: http://localhost:8000/docs"
echo "🔄 Appuyez sur Ctrl+C pour arrêter"
echo "================================"

python3 main.py
