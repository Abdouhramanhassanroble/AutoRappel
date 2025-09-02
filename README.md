# 🚀 AutoRappel - API de Rappels par Email

Une API FastAPI sécurisée pour envoyer automatiquement des rappels par email avec protection anti-spam avancée.

## ✨ Fonctionnalités

- 📧 **Envoi d'emails sécurisé** via Gmail SMTP
- 🛡️ **Protection anti-spam** avec rate limiting et validation
- 📊 **Monitoring et logs** détaillés
- 🔒 **Sécurité renforcée** avec variables d'environnement
- 🐳 **Déploiement Docker** prêt à l'emploi
- 📱 **API REST** complète avec documentation automatique

## 🚀 Démarrage Rapide

### 1. Configuration
```bash
# Cloner le projet
git clone <votre-repo>
cd AutoRappel

# Copier le fichier de configuration
cp env.example .env

# Éditer .env avec vos données Gmail
nano .env
```

### 2. Installation
```bash
# Installer les dépendances
pip install -r requirements.txt

# OU utiliser le script de démarrage
./start.sh
```

### 3. Lancement
```bash
# Méthode simple
python main.py

# OU avec uvicorn directement
uvicorn api.rappel_secure:app --reload --host 0.0.0.0 --port 8000
```

## 🔧 Configuration

### Variables d'environnement (.env)

```bash
# Configuration Gmail
GMAIL_EMAIL=votre_email@gmail.com
GMAIL_PASSWORD=votre_mot_de_passe_application

# Destinataires (séparés par des virgules)
EMAIL_RECIPIENTS=destinataire1@gmail.com,destinataire2@gmail.com

# Configuration SMTP
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SMTP_USE_SSL=true

# Nom d'affichage de l'expéditeur
SENDER_NAME=AutoRappel

# Protection anti-spam
MAX_EMAILS_PER_HOUR=50

# Configuration du serveur
HOST=0.0.0.0
PORT=8000
RELOAD=true
```

### Configuration Gmail

1. **Activer l'authentification à 2 facteurs**
2. **Créer un mot de passe d'application** pour "AutoRappel"
3. **Utiliser ce mot de passe** dans la variable `GMAIL_PASSWORD`

## 📡 Endpoints API

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Envoie un rappel de travail |
| `/test-email` | GET | Envoie un email de test |
| `/health` | GET | Vérification de santé |
| `/config` | GET | Configuration actuelle |
| `/config/status` | GET | État de la configuration |
| `/stats` | GET | Statistiques d'envoi |
| `/logs` | GET | Consultation des logs |
| `/docs` | GET | Documentation Swagger |

## 🛡️ Protection Anti-Spam

### Rate Limiting
- **10 requêtes par minute** par adresse IP
- **50 emails maximum par heure** au total
- **Validation d'email** stricte

### Headers Anti-Spam
- Message-ID unique
- Headers de priorité normale
- Informations de désabonnement
- Formatage HTML/text optimisé

## 🐳 Déploiement Docker

### Avec Docker Compose
```bash
# Démarrer l'application
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter
docker-compose down
```

### Avec Docker seul
```bash
# Construire l'image
docker build -t autorappel .

# Lancer le conteneur
docker run -p 8000:8000 --env-file .env autorappel
```

## 🧪 Tests

### Test des endpoints
```bash
# Lancer l'application
python main.py

# Dans un autre terminal, tester
python test_app.py
```

### Test manuel
```bash
# Test de santé
curl http://localhost:8000/health

# Test d'envoi d'email
curl http://localhost:8000/test-email

# Voir la configuration
curl http://localhost:8000/config
```

## 📊 Monitoring

### Logs
- **Fichier :** `email_logs.log`
- **Format :** Horodatage + Niveau + Message
- **Endpoint :** `/logs`

### Statistiques
- **Endpoint :** `/stats`
- **Métriques :** Emails/heure, limites, statut

### Santé
- **Endpoint :** `/health`
- **Vérifications :** Statut, version, timestamp

## 🚨 Dépannage

### Problèmes courants

#### Erreur d'authentification SMTP
```bash
# Vérifier la configuration
curl http://localhost:8000/config/status

# Vérifier les logs
curl http://localhost:8000/logs
```

#### Emails dans les spams
- Ajouter l'expéditeur aux contacts
- Vérifier la configuration des headers
- Marquer comme "Non spam"

#### Rate limit dépassé
- Attendre la fin de la fenêtre (1 minute)
- Vérifier les statistiques : `/stats`

## 🔒 Sécurité

- ✅ **Aucune donnée sensible** dans le code
- ✅ **Variables d'environnement** pour la configuration
- ✅ **Rate limiting** par IP
- ✅ **Validation d'email** stricte
- ✅ **Limites d'envoi** par heure
- ✅ **Logs détaillés** pour l'audit

## 📁 Structure du Projet

```
AutoRappel/
├── api/
│   └── rappel_secure.py    # Code principal sécurisé
├── .env                    # Configuration (ignoré par git)
├── env.example            # Exemple de configuration
├── .gitignore             # Fichiers à ignorer
├── requirements.txt        # Dépendances Python
├── main.py                # Lanceur principal
├── start.sh               # Script de démarrage
├── test_app.py            # Script de test
├── docker-compose.yml     # Configuration Docker
├── Dockerfile             # Image Docker
├── README.md              # Ce fichier
└── README_SECURE.md       # Documentation détaillée
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT.

## 🆘 Support

- 📚 **Documentation API :** http://localhost:8000/docs
- 🔍 **Logs :** http://localhost:8000/logs
- 📊 **Statut :** http://localhost:8000/health
- 🐛 **Issues :** Ouvrir une issue sur GitHub

---

**🎯 AutoRappel est maintenant prêt à envoyer vos rappels !**
