from scraper_sqlite import scrape_jobs
from mailer_sqlite import run_mailer

def main():
    print("--- SQLite Daily Automation ---")
    scrape_jobs()
    run_mailer()
    print("--- Done ---")

if __name__ == "__main__":
    main()
