from scrape_jobs import scrape_jobs, save_to_json

if __name__ == "__main__":
    print("Welcome to Naukri Job Scraper")

    job_role = input("Enter job role (e.g. Python Developer): ").strip()
    location = input("Enter location (e.g. Remote, Delhi): ").strip()
    experience = input("Enter experience in years (e.g. 0,5): ").strip()
    max_pages = int(input("Enter number of pages to scrape (e.g. 3): ").strip())

    jobs = scrape_jobs(role=job_role, location=location, experience=experience, max_pages=max_pages)

    save_to_json(jobs, filename="jobs.json")
