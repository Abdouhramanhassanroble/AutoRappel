from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr, formatdate
import uuid
from datetime import datetime, timedelta
import logging
import os
import re
from dotenv import load_dotenv
from typing import Dict, List
import time

# Charger les variables d'environnement
load_dotenv()

# Configuration des logs adaptée pour Vercel
def setup_logging():
    """Configure les logs selon l'environnement"""
    if os.getenv("VERCEL_ENV"):  # Environnement Vercel
        # En Vercel, on utilise seulement les logs de sortie
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )
    else:
        # Environnement local avec fichier de log
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('email_logs.log'),
                logging.StreamHandler()
            ]
        )

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AutoRappel API",
    description="API sécurisée pour l'envoi de rappels par email avec protection anti-spam",
    version="1.0.0"
)

# Middleware CORS pour la sécurité
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, restreindre aux domaines autorisés
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Système de rate limiting adapté pour Vercel
class RateLimiter:
    def __init__(self):
        self.requests: Dict[str, List[float]] = {}
        self.max_requests = 10  # Max 10 requêtes par minute
        self.window = 60  # Fenêtre de 60 secondes
    
    def is_allowed(self, client_ip: str) -> bool:
        now = time.time()
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        
        # Nettoyer les anciennes requêtes
        self.requests[client_ip] = [req_time for req_time in self.requests[client_ip] 
                                   if now - req_time < self.window]
        
        # Vérifier la limite
        if len(self.requests[client_ip]) >= self.max_requests:
            return False
        
        # Ajouter la nouvelle requête
        self.requests[client_ip].append(now)
        return True

rate_limiter = RateLimiter()

# Validation d'email
def validate_email(email: str) -> bool:
    """Valide le format d'un email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Middleware de rate limiting
async def check_rate_limit(request: Request):
    client_ip = request.client.host
    if not rate_limiter.is_allowed(client_ip):
        logger.warning(f"🚫 Rate limit dépassé pour {client_ip}")
        raise HTTPException(
            status_code=429, 
            detail="Trop de requêtes. Veuillez attendre avant de réessayer."
        )
    return True

# Configuration depuis les variables d'environnement
def get_config():
    """Récupère la configuration depuis les variables d'environnement"""
    config = {
        "gmail_email": os.getenv("GMAIL_EMAIL", "votre_email@gmail.com"),
        "gmail_password": os.getenv("GMAIL_PASSWORD", "votre_mot_de_passe"),
        "recipients": os.getenv("EMAIL_RECIPIENTS", "destinataire@gmail.com").split(","),
        "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        "smtp_port": int(os.getenv("SMTP_PORT", "465")),
        "smtp_use_ssl": os.getenv("SMTP_USE_SSL", "true").lower() == "true",
        "sender_name": os.getenv("SENDER_NAME", "AutoRappel"),
        "max_emails_per_hour": int(os.getenv("MAX_EMAILS_PER_HOUR", "50"))
    }
    
    # Validation de la configuration
    if config["gmail_email"] == "votre_email@gmail.com":
        logger.warning("⚠️ Configuration par défaut détectée. Vérifiez votre fichier .env")
    
    return config

# Compteur d'emails pour la protection anti-spam
email_counter = {"count": 0, "reset_time": datetime.now()}

def check_email_limit() -> bool:
    """Vérifie la limite d'emails par heure"""
    now = datetime.now()
    if now - email_counter["reset_time"] > timedelta(hours=1):
        email_counter["count"] = 0
        email_counter["reset_time"] = now
    
    if email_counter["count"] >= get_config()["max_emails_per_hour"]:
        logger.warning("🚫 Limite d'emails par heure atteinte")
        return False
    
    email_counter["count"] += 1
    return True

# Fonction pour envoyer le mail
def send_email(subject, body, to_emails):
    config = get_config()
    
    # Vérifier la limite d'emails
    if not check_email_limit():
        raise HTTPException(
            status_code=429,
            detail="Limite d'emails par heure atteinte. Veuillez attendre."
        )
    
    from_email = config["gmail_email"]
    from_name = config["sender_name"]
    password = config["gmail_password"]

    logger.info(f"🚀 Début de l'envoi d'email - Sujet: {subject}")
    logger.info(f"📧 Expéditeur: {from_email}")
    logger.info(f"👥 Destinataires: {to_emails}")

    for to_email in to_emails:
        # Validation de l'email
        if not validate_email(to_email):
            logger.error(f"❌ Format d'email invalide: {to_email}")
            continue
            
        logger.info(f"📤 Préparation de l'email pour: {to_email}")
        
        try:
            # Créer un message multipart
            msg = MIMEMultipart('alternative')
            
            # Headers essentiels pour éviter le spam
            msg["Subject"] = subject
            msg["From"] = formataddr((from_name, from_email))
            msg["To"] = to_email
            msg["Date"] = formatdate(localtime=True)
            msg["Message-ID"] = f"<{uuid.uuid4()}@autorappel.com>"
            msg["Reply-To"] = from_email
            msg["X-Mailer"] = "AutoRappel/1.0"
            msg["X-Priority"] = "3"  # Priorité normale
            msg["X-MSMail-Priority"] = "Normal"
            msg["Importance"] = "Normal"
            
            logger.info(f"✅ Headers configurés pour {to_email}")
            
            # Corps du message en HTML et texte
            text_body = body
            html_body = f"""
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                        <h2 style="color: #007bff; margin-top: 0;">🚀 AutoRappel</h2>
                        <p style="margin: 0; font-size: 16px;">{body}</p>
                    </div>
                    <div style="text-align: center; color: #6c757d; font-size: 12px;">
                        <p>Cet email a été envoyé automatiquement par AutoRappel</p>
                        <p>Envoyé le {datetime.now().strftime('%d/%m/%Y à %H:%M')}</p>
                        <p>Pour vous désabonner, contactez l'administrateur</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Ajouter les parties texte et HTML
            text_part = MIMEText(text_body, 'plain', 'utf-8')
            html_part = MIMEText(html_body, 'html', 'utf-8')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            logger.info(f"✅ Contenu de l'email préparé pour {to_email}")
            
            # Connexion au serveur SMTP
            logger.info(f"🔌 Tentative de connexion à {config['smtp_server']}:{config['smtp_port']}")
            
            if config["smtp_use_ssl"]:
                with smtplib.SMTP_SSL(config["smtp_server"], config["smtp_port"]) as server:
                    logger.info(f"✅ Connexion SMTP SSL établie")
                    
                    # Authentification
                    logger.info(f"🔐 Tentative d'authentification avec {from_email}")
                    server.login(from_email, password)
                    logger.info(f"✅ Authentification réussie")
                    
                    # Envoi de l'email
                    logger.info(f"📤 Envoi de l'email à {to_email}")
                    server.send_message(msg)
                    logger.info(f"✅ Email envoyé avec succès à {to_email}")
            else:
                with smtplib.SMTP(config["smtp_server"], config["smtp_port"]) as server:
                    logger.info(f"✅ Connexion SMTP établie")
                    server.starttls()
                    
                    # Authentification
                    logger.info(f"🔐 Tentative d'authentification avec {from_email}")
                    server.login(from_email, password)
                    logger.info(f"✅ Authentification réussie")
                    
                    # Envoi de l'email
                    logger.info(f"📤 Envoi de l'email à {to_email}")
                    server.send_message(msg)
                    logger.info(f"✅ Email envoyé avec succès à {to_email}")
                
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"❌ Erreur d'authentification SMTP: {str(e)}")
            logger.error(f"Vérifiez le mot de passe d'application pour {from_email}")
            raise HTTPException(
                status_code=500,
                detail="Erreur d'authentification SMTP. Vérifiez la configuration."
            )
        except smtplib.SMTPRecipientsRefused as e:
            logger.error(f"❌ Destinataire refusé {to_email}: {str(e)}")
        except smtplib.SMTPSenderRefused as e:
            logger.error(f"❌ Expéditeur refusé {from_email}: {str(e)}")
        except smtplib.SMTPDataError as e:
            logger.error(f"❌ Erreur de données SMTP: {str(e)}")
        except smtplib.SMTPConnectError as e:
            logger.error(f"❌ Erreur de connexion SMTP: {str(e)}")
        except smtplib.SMTPHeloError as e:
            logger.error(f"❌ Erreur HELO SMTP: {str(e)}")
        except Exception as e:
            logger.error(f"❌ Erreur inattendue lors de l'envoi à {to_email}: {str(e)}")
            logger.error(f"Type d'erreur: {type(e).__name__}")
    
    logger.info(f"🏁 Fin du processus d'envoi d'emails")

# Endpoint pour les rappels
@app.get("/", dependencies=[Depends(check_rate_limit)])
def main():
    logger.info("🌐 Endpoint / appelé - Envoi des rappels de travail")
    config = get_config()
    send_email(
        "Rappel travail",
        "N'oubliez pas de travailler maintenant ! 💪",
        config["recipients"]
    )
    logger.info("✅ Rappels de travail envoyés")
    return {"message": "Mails envoyés à tous les destinataires !"}

# Endpoint pour tester l'envoi
@app.get("/test-email", dependencies=[Depends(check_rate_limit)])
def test_email():
    logger.info("🧪 Endpoint /test-email appelé - Test d'envoi d'email")
    config = get_config()
    send_email(
        "Test AutoRappel",
        "Ceci est un email de test pour vérifier la délivrabilité.",
        config["recipients"]
    )
    logger.info("✅ Email de test envoyé")
    return {"message": "Email de test envoyé !"}

# Endpoint pour voir les logs
@app.get("/logs")
def view_logs():
    try:
        with open('email_logs.log', 'r') as f:
            logs = f.read()
        return {"logs": logs}
    except FileNotFoundError:
        return {"logs": "Aucun fichier de log trouvé"}

# Endpoint pour vérifier la configuration (sans données sensibles)
@app.get("/config")
def check_config():
    config = get_config()
    return {
        "expediteur": config["gmail_email"],
        "destinataires_count": len(config["recipients"]),
        "serveur_smtp": f"{config['smtp_server']}:{config['smtp_port']}",
        "ssl_actif": config["smtp_use_ssl"],
        "max_emails_par_heure": config["max_emails_per_hour"],
        "status": "Configuration chargée"
    }

# Endpoint pour vérifier l'état de la configuration
@app.get("/config/status")
def config_status():
    config = get_config()
    missing_vars = []
    
    if config["gmail_email"] == "votre_email@gmail.com":
        missing_vars.append("GMAIL_EMAIL")
    if config["gmail_password"] == "votre_mot_de_passe":
        missing_vars.append("GMAIL_PASSWORD")
    if config["recipients"] == ["destinataire@gmail.com"]:
        missing_vars.append("EMAIL_RECIPIENTS")
    
    return {
        "config_ok": len(missing_vars) == 0,
        "missing_variables": missing_vars,
        "message": "Configuration complète" if len(missing_vars) == 0 else f"Variables manquantes: {', '.join(missing_vars)}"
    }

# Endpoint pour vérifier les statistiques
@app.get("/stats")
def get_stats():
    return {
        "emails_envoyes_heure": email_counter["count"],
        "limite_emails_heure": get_config()["max_emails_per_hour"],
        "reset_prochain": (email_counter["reset_time"] + timedelta(hours=1)).strftime("%H:%M:%S"),
        "status": "Actif"
    }

# Endpoint de santé
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }
