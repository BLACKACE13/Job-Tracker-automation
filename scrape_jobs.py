from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import time
import json


def scrape_jobs(role="python developer", location="remote", experience="0", max_pages=5):
    options = Options()
    #options.add_argument("--headless=new")  # New headless mode (quieter)
    options.add_argument("--disable-logging")
    options.add_argument("--log-level=3")  # Suppress most logs

    driver = webdriver.Chrome(service=Service(), options=options)
    driver.get("https://www.naukri.com/")

    wait = WebDriverWait(driver, 10)
    role_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "suggestor-input")))
    role_input.send_keys(role)

    # Set location (the second input — use a better locator if needed)
    location_inputs = driver.find_elements(By.CLASS_NAME, "suggestor-input")
    if len(location_inputs) > 1:
        location_input = location_inputs[1]  # second input is for location
        location_input.clear()
        location_input.send_keys(location)
        time.sleep(2)
        location_input.send_keys(Keys.ARROW_DOWN)
        location_input.send_keys(Keys.RETURN)

    # Start search
    role_input.send_keys(Keys.RETURN)

    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "srp-jobtuple-wrapper")))
        time.sleep(2)
    except:
        print("No job listings found.")
        driver.quit()
        return []
    
    #experience filter
    try:
        slider = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "handle")))
        actions = ActionChains(driver)
        offset = 225 - (int(experience) * 10)
        actions.click_and_hold(slider).move_by_offset(-offset, 0).release().perform()
        time.sleep(2)
    except Exception as e:
        print("Could not set experience slider:", e)
    
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
