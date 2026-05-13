import requests
from bs4 import BeautifulSoup
import sqlite3
import os
from datetime import datetime

# Database path (relative to root)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'instance', 'careerpulse.db')
# Flask creates the instance folder if we use the default config. 
# In app.py I used 'sqlite:///careerpulse.db', which usually goes to root or instance folder.
# Let's check where Flask puts it. By default it's the root if not specified.
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'careerpulse.db')

def scrape_jobs():
    print("Scraping jobs for SQLite database...")
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
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    new_jobs = 0
    for row in job_rows:
        try:
            title = row.find('h2', itemprop='title').text.strip()
            company = row.find('h3', itemprop='name').text.strip()
            link = "https://remoteok.com" + row.find('a', itemprop='url')['href']
            location = "Remote"
            skills = ", ".join([tag.text.strip() for tag in row.find_all('div', class_='tag')])
            
            cursor.execute("INSERT OR IGNORE INTO job (title, company, location, skills, link, date_posted) VALUES (?, ?, ?, ?, ?, ?)",
                           (title, company, location, skills, link, datetime.utcnow()))
            if cursor.rowcount > 0:
                new_jobs += 1
                print(f"Added: {title} @ {company}")
        except Exception as e:
            continue
            
    conn.commit()
    conn.close()
    print(f"Scraping finished. Added {new_jobs} new jobs.")

if __name__ == "__main__":
    scrape_jobs()
