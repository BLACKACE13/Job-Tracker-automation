from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json


def scrape_jobs(role="python developer", max_pages=5):
    options = Options()
    #options.add_argument("--headless=new")  # New headless mode (quieter)
    options.add_argument("--disable-logging")
    options.add_argument("--log-level=3")  # Suppress most logs

    driver = webdriver.Chrome(service=Service(), options=options)
    driver.get("https://www.naukri.com/")

    search = driver.find_element(By.CLASS_NAME, "suggestor-input")
    search.send_keys(role)
    search.send_keys(Keys.RETURN)

    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "srp-jobtuple-wrapper")))
        time.sleep(2)
    except:
        print("No job listings found.")
        driver.quit()
        return []

    jobs = []
    page = 1

    while True:
        #print(f"Scraping page {page}...")
        jobcards = driver.find_elements(By.CSS_SELECTOR, "div.cust-job-tuple")

        for job in jobcards:
            try:
                title_elem = job.find_element(By.CSS_SELECTOR, "a.title")
                title = title_elem.text.strip()
                link = title_elem.get_attribute("href")
            except:
                title, link = "N/A", "N/A"

            try:
                company = job.find_element(By.CSS_SELECTOR, "a.comp-name").text.strip()
            except:
                company = "N/A"

            try:
                location = job.find_element(By.CSS_SELECTOR, "span.locWdth").text.strip()
            except:
                location = "N/A"

            try:
                posted = job.find_element(By.CSS_SELECTOR, "span.job-post-day").text.strip()
            except:
                posted = "N/A"

            jobs.append([title, company, location, posted, link])

        if page >= max_pages:
            break

        try:
            next_btn = driver.find_element(By.XPATH, "//a[span[text()='Next'] and contains(@class, 'btn-secondary')]")
            next_btn.click()
            time.sleep(3)
            page += 1
        except NoSuchElementException:
            break

    driver.quit()
    return jobs

def save_to_json(jobs, filename="jobs.json"):
    job_dicts = [
        {"title": j[0], "company": j[1], "location": j[2], "posted": j[3], "link": j[4]}
        for j in jobs
    ]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(job_dicts, f, indent=4, ensure_ascii=False)
    print(f"{len(job_dicts)} jobs saved to {filename}")
