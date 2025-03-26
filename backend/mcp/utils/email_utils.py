# Keyhole_Automation_Platform\backend\mcp\utils\email_utils.py

import os
import smtplib
import ssl
import traceback
from email.message import EmailMessage
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "mail.keyholesolution.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "security@keyholesolution.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# Token-related secrets
SECRET_KEY = os.getenv("EMAIL_TOKEN_SECRET", "super-secret-key")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


def send_email(to_email: str, subject: str, body: str) -> bool:
    from_email = os.getenv("EMAIL_FROM")
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    
    # ✅ Move this check inside the function
    if os.getenv("IS_TESTING", "false").lower() == "true":
        print(f"📧 [MOCKED] Email sent to {to_email}")
        return True

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(body)

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        print(f"📧 Email sent to {to_email}")
        return True
    except Exception as e:
        print("❌ Failed to send email:")
        traceback.print_exc()
        return False


def generate_email_token(email: str) -> str:
    """Generate a time-limited token for verifying email."""
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt="email-confirm")


def confirm_email_token(token: str, expiration=3600) -> str | None:
    """Confirm token and return email if valid."""
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(token, salt="email-confirm", max_age=expiration)
        return email
    except Exception:
        return None
