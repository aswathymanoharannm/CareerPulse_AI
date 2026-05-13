import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client.careerpulse
job_collection = db.jobs

def scrape_remote_ok():
    print("Scraping RemoteOK for AI/Data jobs...")
    url = "https://remoteok.com/remote-ai-jobs"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch jobs: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    job_rows = soup.find_all('tr', class_='job')
    
    new_jobs_count = 0
    
    for row in job_rows:
        try:
            title = row.find('h2', itemprop='title').text.strip()
            company = row.find('h3', itemprop='name').text.strip()
            link = "https://remoteok.com" + row.find('a', itemprop='url')['href']
            location = "Remote"
            
            # Extract tags as skills
            tags = [tag.text.strip() for tag in row.find_all('div', class_='tag')]
            
            # Check for duplicates
            if job_collection.find_one({"link": link}):
                continue
                
            job_data = {
                "title": title,
                "company": company,
                "link": link,
                "location": location,
                "skills": tags,
                "posted_date": datetime.utcnow().isoformat()
            }
            
            job_collection.insert_one(job_data)
            new_jobs_count += 1
            print(f"Added: {title} at {company}")
            
        except Exception as e:
            print(f"Error parsing row: {e}")
            
    print(f"Scraping completed. Added {new_jobs_count} new jobs.")

if __name__ == "__main__":
    scrape_remote_ok()
