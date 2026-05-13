import sqlite3
import os
from datetime import datetime

# Database path in the instance folder
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'instance', 'careerpulse.db')

def seed():
    print(f"Seeding SQLite database at {DB_PATH}...")
    if not os.path.exists(DB_PATH):
        print("Database file not found! Make sure to run app.py first.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Add some jobs
    jobs = [
        ("AI Software Engineer", "TechNova", "Remote", "Python, TensorFlow, PyTorch", "https://example.com/a1", datetime.utcnow().isoformat()),
        ("Data Scientist", "OpenData", "New York", "SQL, R, Python, Tableau", "https://example.com/a2", datetime.utcnow().isoformat()),
        ("MLOps Specialist", "CloudSystems", "Remote", "Docker, Kubernetes, AWS, Python", "https://example.com/a3", datetime.utcnow().isoformat())
    ]
    
    cursor.executemany("INSERT OR IGNORE INTO job (title, company, location, skills, link, date_posted) VALUES (?, ?, ?, ?, ?, ?)", jobs)
    
    conn.commit()
    conn.close()
    print("Seeding complete.")

if __name__ == "__main__":
    seed()
