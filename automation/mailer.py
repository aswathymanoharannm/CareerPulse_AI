import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Config
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client.careerpulse

def send_email(to_email, student_name, matching_jobs):
    if not matching_jobs:
        return

    msg = MIMEMultipart()
    msg['From'] = f"CareerPulse AI <{SMTP_USER}>"
    msg['To'] = to_email
    msg['Subject'] = f"Daily Job Alerts for {student_name} - CareerPulse AI"

    # Create HTML content
    job_list_html = ""
    for job in matching_jobs:
        job_list_html += f"""
        <div style="margin-bottom: 20px; padding: 15px; border: 1px solid #e2e8f0; border-radius: 12px;">
            <h3 style="margin: 0; color: #6366f1;">{job['title']}</h3>
            <p style="margin: 5px 0; font-weight: bold;">{job['company']} | {job['location']}</p>
            <p style="margin: 5px 0; font-size: 0.9em; color: #64748b;">Skills: {", ".join(job['skills'])}</p>
            <a href="{job['link']}" style="display: inline-block; margin-top: 10px; padding: 8px 16px; background-color: #6366f1; color: white; text-decoration: none; border-radius: 8px; font-weight: bold;">Apply Now</a>
        </div>
        """

    html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #1e293b; line-height: 1.6;">
            <h2 style="color: #0f172a;">Hello {student_name},</h2>
            <p>Here are your personalized job recommendations for today based on your skills.</p>
            <div style="margin-top: 30px;">
                {job_list_html}
            </div>
            <p style="margin-top: 40px; font-size: 0.8em; color: #94a3b8;">
                You are receiving this email because you are enrolled in CareerPulse AI Placement Assistance.
            </p>
        </body>
    </html>
    """

    msg.attach(MIMEText(html, 'html'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

def run_mailer():
    print("Starting email automation...")
    students = list(db.students.find())
    recent_jobs = list(db.jobs.find().sort("posted_date", -1).limit(20))
    
    for student in students:
        # Simple skill matching
        student_skills = [s.lower() for s in student.get('skills', [])]
        matching_jobs = []
        
        for job in recent_jobs:
            job_skills = [s.lower() for s in job.get('skills', [])]
            # If student has no skills, send top jobs, otherwise match
            if not student_skills or any(skill in job_skills for skill in student_skills):
                matching_jobs.append(job)
        
        if matching_jobs:
            send_email(student['email'], student['name'], matching_jobs[:5]) # Send top 5

if __name__ == "__main__":
    if not SMTP_USER or not SMTP_PASS:
        print("SMTP credentials not found. Skipping mailer.")
    else:
        run_mailer()
