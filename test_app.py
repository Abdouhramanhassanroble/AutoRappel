#!/usr/bin/env python3
"""
Script de test pour AutoRappel
"""

import requests
import time
import json

BASE_URL = "http://localhost:8000"

def test_endpoints():
    """Teste tous les endpoints de l'API"""
    
    print("🧪 Test des endpoints AutoRappel")
    print("=" * 40)
    
    # Test de santé
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ /health - Status: {response.status_code}")
        print(f"   Réponse: {response.json()}")
    except Exception as e:
        print(f"❌ /health - Erreur: {e}")
    
    print()
    
    # Test de configuration
    try:
        response = requests.get(f"{BASE_URL}/config")
        print(f"✅ /config - Status: {response.status_code}")
        config = response.json()
        print(f"   Expéditeur: {config.get('expediteur', 'N/A')}")
        print(f"   Destinataires: {config.get('destinataires_count', 'N/A')}")
        print(f"   SMTP: {config.get('serveur_smtp', 'N/A')}")
    except Exception as e:
        print(f"❌ /config - Erreur: {e}")
    
    print()
    
    # Test du statut de configuration
    try:
        response = requests.get(f"{BASE_URL}/config/status")
        print(f"✅ /config/status - Status: {response.status_code}")
        status = response.json()
        print(f"   Configuration OK: {status.get('config_ok', 'N/A')}")
        if not status.get('config_ok'):
            print(f"   Variables manquantes: {status.get('missing_variables', [])}")
    except Exception as e:
        print(f"❌ /config/status - Erreur: {e}")
    
    print()
    
    # Test des statistiques
    try:
        response = requests.get(f"{BASE_URL}/stats")
        print(f"✅ /stats - Status: {response.status_code}")
        stats = response.json()
        print(f"   Emails/heure: {stats.get('emails_envoyes_heure', 'N/A')}")
        print(f"   Limite: {stats.get('limite_emails_heure', 'N/A')}")
    except Exception as e:
        print(f"❌ /stats - Erreur: {e}")
    
    print()
    
    # Test des logs
    try:
        response = requests.get(f"{BASE_URL}/logs")
        print(f"✅ /logs - Status: {response.status_code}")
        logs = response.json()
        if logs.get('logs'):
            print(f"   Logs disponibles: {len(logs['logs'])} caractères")
        else:
            print("   Aucun log disponible")
    except Exception as e:
        print(f"❌ /logs - Erreur: {e}")
    
    print()
    print("=" * 40)
    print("🎯 Tests terminés !")
    print()
    print("💡 Pour tester l'envoi d'emails:")
    print("   1. Assurez-vous que l'application est lancée")
    print("   2. Configurez votre fichier .env")
    print("   3. Testez avec: curl http://localhost:8000/test-email")

if __name__ == "__main__":
    test_endpoints()
