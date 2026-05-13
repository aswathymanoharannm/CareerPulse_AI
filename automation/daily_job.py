from scraper import scrape_remote_ok
from mailer import run_mailer

def main():
    print("--- CareerPulse AI Daily Automation Start ---")
    
    # 1. Scrape Jobs
    scrape_remote_ok()
    
    # 2. Send Emails
    run_mailer()
    
    print("--- CareerPulse AI Daily Automation End ---")

if __name__ == "__main__":
    main()
