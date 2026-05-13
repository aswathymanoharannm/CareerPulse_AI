import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

def test_mail():
    print(f"Connecting to {SMTP_SERVER}:{SMTP_PORT}...")
    print(f"User: {SMTP_USER}")
    
    if not SMTP_USER or not SMTP_PASS:
        print("Error: SMTP_USER or SMTP_PASS not set in .env")
        return

    msg = MIMEText("This is a test email from CareerPulse AI.")
    msg['Subject'] = "Test Email"
    msg['From'] = SMTP_USER
    msg['To'] = SMTP_USER  # Send to self for testing

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.set_debuglevel(1) # Enable debug output
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        print("Success: Test email sent!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    test_mail()
