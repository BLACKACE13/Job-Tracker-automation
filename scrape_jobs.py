from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import time
import json

def save_to_json(jobs, filename="jobs.json"):
    job_dicts = [
        {"title": j[0], "company": j[1], "location": j[2], "posted": j[3], "link": j[4]}
        for j in jobs
    ]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(job_dicts, f, indent=4, ensure_ascii=False)
    print(f"{len(job_dicts)} jobs founded")
    print(f"Saved to {filename}")


driver= webdriver.Chrome()
driver.get("https://www.naukri.com/")

title = driver.title
print(title) # gets the title

search = driver.find_element(By.CLASS_NAME,"suggestor-input")
search.send_keys("Python developer")
search.send_keys(Keys.RETURN)

try:
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "srp-jobtuple-wrapper"))) #finds job listing.
    
    time.sleep(2)

except:
    print("No job listing found.")

jobs=[]

while True:
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

    try:
        # Try to locate the "Next" button by text and class
        next_btn = driver.find_element(By.XPATH, "//a[span[text()='Next'] and contains(@class, 'btn-secondary')]")
        next_btn.click()
        time.sleep(3)  # wait for next page to load
    except NoSuchElementException:
        print("No more pages found.")
        break
    
    jobs.append([title, company, location, posted, link])

save_to_json(jobs)

driver.close()
driver.quit()