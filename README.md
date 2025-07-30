# 🧠 Job Scraper with Filters using Selenium

This project is a Python-based job scraper that uses Selenium to automate job search on [Naukri.com](https://www.naukri.com). It allows filtering jobs by **role**, **location**, **posted date**, and **experience (years)**.

---

## Features

This script helps you automate job searches on portals like `Naukri.com` by allowing you to enter a job role and optionally apply filters like **location, posted date, and minimum experience**. It navigates through all job listing pages, collects details like **job title, company, location, posted date, and job link**, and saves everything to a `jobs.json file`.

---

## Requirements

- Python 3.7+
- Google Chrome
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) (should match your browser version)
- Selenium

```bash
pip install selenium
```
## How to Use

1. Clone or download this repo.
2. Make sure `chromedriver` is installed and added to your system PATH.
3. Run the script:
``` bash
python main.py
```
4. Enter the following input when prompted:

- Job role (e.g., `python developer`)
- Location (e.g., `Remote, Delhi, Mumbai`) – auto-filled from suggestions
- Minimum experience (`0-20 years`)
- Number of pages scrapped (`max 5`)

5. Jobs will be saved to `jobs.json`.


### Notes
- The location input uses the auto-suggest input box on the Naukri homepage.

- Experience slider might default to a high value if not set carefully — verify the slider logic if needed.

- If a location string doesn’t exactly match a checkbox label, the auto-suggest will still help match similar ones.

## License
This project is for educational/demo purposes only. Please respect the terms of service of any website you scrape.