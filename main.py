from scrape_jobs import scrape_jobs, save_to_json

if __name__ == "__main__":
    job_role = str(input("Job Title: "))
    max_pages = 3  # increase/decrease based on filters

    jobs = scrape_jobs(role=job_role, max_pages=max_pages)
    save_to_json(jobs, filename="jobs.json")

