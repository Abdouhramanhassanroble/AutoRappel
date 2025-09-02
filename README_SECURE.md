# AutoRappel - Application de Rappels par Email

## 🚀 Description
AutoRappel est une application FastAPI qui envoie automatiquement des rappels par email. Elle utilise Gmail SMTP pour l'envoi et inclut des fonctionnalités anti-spam.

## 🔒 Sécurité
**⚠️ IMPORTANT :** Cette application ne contient AUCUNE donnée sensible dans le code source. Toutes les informations sensibles (emails, mots de passe) sont stockées dans des variables d'environnement.

## 📋 Prérequis
- Python 3.8+
- Compte Gmail avec authentification à 2 facteurs activée
- Mot de passe d'application Gmail

## 🛠️ Installation

### 1. Cloner le repository
```bash
git clone <votre-repo>
cd AutoRappel
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Configuration
1. **Copier le fichier d'exemple :**
   ```bash
   cp env.example .env
   ```

2. **Éditer le fichier `.env` avec vos vraies données :**
   ```bash
   # Configuration Gmail
   GMAIL_EMAIL=votre_vrai_email@gmail.com
   GMAIL_PASSWORD=votre_vrai_mot_de_passe_application
   
   # Destinataires (séparés par des virgules)
   EMAIL_RECIPIENTS=destinataire1@gmail.com,destinataire2@gmail.com
   
   # Configuration SMTP
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=465
   SMTP_USE_SSL=true
   
   # Nom d'affichage de l'expéditeur
   SENDER_NAME=AutoRappel
   ```

## 🚀 Lancement

### Démarrage de l'application
```bash
python -m uvicorn api.rappel_secure:app --reload --host 0.0.0.0 --port 8000
```

### Accès à l'application
- **URL principale :** http://localhost:8000
- **Documentation API :** http://localhost:8000/docs

## 📧 Endpoints

### 1. **`/`** - Envoi des rappels de travail
- **Méthode :** GET
- **Action :** Envoie un rappel de travail à tous les destinataires

### 2. **`/test-email`** - Test d'envoi d'email
- **Méthode :** GET
- **Action :** Envoie un email de test pour vérifier la délivrabilité

### 3. **`/logs`** - Consultation des logs
- **Méthode :** GET
- **Action :** Affiche tous les logs d'envoi d'emails

### 4. **`/config`** - Configuration actuelle
- **Méthode :** GET
- **Action :** Affiche la configuration (sans données sensibles)

### 5. **`/config/status`** - État de la configuration
- **Méthode :** GET
- **Action :** Vérifie si toutes les variables d'environnement sont configurées

## 🔧 Configuration Gmail

### 1. Activer l'authentification à 2 facteurs
- Aller dans les paramètres Gmail
- Section "Sécurité"
- Activer "Validation en 2 étapes"

### 2. Créer un mot de passe d'application
- Aller dans les paramètres Gmail
- Section "Sécurité"
- "Mots de passe d'application"
- Créer un nouveau mot de passe pour "AutoRappel"

## 📊 Logs et Monitoring

### Fichier de logs
- **Emplacement :** `email_logs.log`
- **Contenu :** Tous les événements d'envoi d'emails
- **Format :** Horodatage + Niveau + Message

### Types de logs
- 🚀 Début d'envoi
- 📧 Configuration de l'expéditeur
- 👥 Liste des destinataires
- 🔌 Connexion SMTP
- 🔐 Authentification
- 📤 Envoi d'email
- ✅ Succès
- ❌ Erreurs détaillées

## 🚨 Dépannage

### Problèmes courants

#### 1. **Erreur d'authentification**
- Vérifier que l'authentification à 2 facteurs est activée
- Vérifier le mot de passe d'application
- Vérifier que l'email est correct

#### 2. **Emails dans les spams**
- Vérifier la configuration des headers
- Ajouter l'expéditeur aux contacts
- Marquer les emails comme "Non spam"

#### 3. **Erreur de connexion SMTP**
- Vérifier la connexion internet
- Vérifier les paramètres SMTP
- Vérifier que le port 465 n'est pas bloqué

## 🔒 Bonnes pratiques de sécurité

1. **Ne jamais commiter le fichier `.env`**
2. **Utiliser des mots de passe d'application, pas le mot de passe principal**
3. **Limiter l'accès aux logs**
4. **Surveiller les tentatives d'envoi**
5. **Utiliser HTTPS en production**

## 📝 Structure des fichiers

```
AutoRappel/
├── api/
│   ├── rappel_secure.py    # Code principal sécurisé
│   └── rappel.py           # Ancien code (ignoré par git)
├── .env                    # Variables d'environnement (ignoré par git)
├── env.example            # Exemple de configuration
├── .gitignore             # Fichiers à ignorer
├── requirements.txt        # Dépendances Python
├── README_SECURE.md       # Ce fichier
└── email_logs.log         # Logs (ignoré par git)
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 🆘 Support

Pour toute question ou problème :
1. Vérifier les logs avec `/logs`
2. Vérifier la configuration avec `/config/status`
3. Consulter la documentation API avec `/docs`
4. Ouvrir une issue sur GitHub
