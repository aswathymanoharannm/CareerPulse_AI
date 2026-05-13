import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'careerpulse.db')
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

def send_alert(to_email, name, jobs):
    if not jobs: return
    
    msg = MIMEMultipart()
    msg['From'] = f"CareerPulse AI <{SMTP_USER}>"
    msg['To'] = to_email
    msg['Subject'] = f"Job Alerts for {name}"
    
    html = f"<h2>Hello {name},</h2><p>Here are matching jobs for your skills:</p>"
    for job in jobs:
        html += f"<p><b>{job[1]}</b> at {job[2]}<br><a href='{job[3]}'>Apply Now</a></p><hr>"
    
    msg.attach(MIMEText(html, 'html'))
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        print(f"Sent to {to_email}")
    except Exception as e:
        print(f"Error: {e}")

def run_mailer():
    if not SMTP_USER:
        print("No SMTP credentials. Skipping mailer.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, email, skills FROM student")
    students = cursor.fetchall()
    
    cursor.execute("SELECT id, title, company, link, skills FROM job ORDER BY date_posted DESC LIMIT 10")
    recent_jobs = cursor.fetchall()
    
    for student in students:
        s_name, s_email, s_skills = student
        s_skills_list = [s.strip().lower() for s in (s_skills or "").split(',')]
        
        matching = []
        for job in recent_jobs:
            j_skills = job[4].lower()
            if not s_skills_list or any(skill in j_skills for skill in s_skills_list):
                matching.append(job)
        
        if matching:
            send_alert(s_email, s_name, matching[:5])
            
    conn.close()

if __name__ == "__main__":
    run_mailer()
