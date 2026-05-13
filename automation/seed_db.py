from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client.careerpulse

def seed():
    print("Seeding database with sample jobs...")
    jobs = [
        {
            "title": "Senior AI Research Engineer",
            "company": "DeepMind",
            "link": "https://example.com/job1",
            "location": "London, UK",
            "skills": ["Python", "PyTorch", "Machine Learning", "NLP"],
            "posted_date": datetime.utcnow().isoformat()
        },
        {
            "title": "Data Scientist - Generative AI",
            "company": "OpenAI",
            "link": "https://example.com/job2",
            "location": "San Francisco, CA",
            "skills": ["LLMs", "Python", "RLHF", "Data Analysis"],
            "posted_date": datetime.utcnow().isoformat()
        },
        {
            "title": "MLOps Engineer",
            "company": "NVIDIA",
            "link": "https://example.com/job3",
            "location": "Remote",
            "skills": ["Docker", "Kubernetes", "AWS", "Python"],
            "posted_date": datetime.utcnow().isoformat()
        },
        {
            "title": "Junior Data Analyst",
            "company": "CareerPulse AI",
            "link": "https://example.com/job4",
            "location": "India",
            "skills": ["SQL", "Excel", "Tableau", "Python"],
            "posted_date": datetime.utcnow().isoformat()
        }
    ]
    
    db.jobs.delete_many({}) # Clear existing
    db.jobs.insert_many(jobs)
    print(f"Successfully seeded {len(jobs)} sample jobs.")

if __name__ == "__main__":
    seed()
