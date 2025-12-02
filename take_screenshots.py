from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)

# Base URL
base_url = "http://127.0.0.1:5000"

# Marketplace pages to screenshot
pages = {
    "market": "/market",
    "marketpage": "/marketpage", 
    "emergencyfood": "/emergencyfood",
    "essentials": "/essentials",
    "medicals": "/medicals",
    "cart": "/cart"
}

try:
    for page_name, route in pages.items():
        driver.get(base_url + route)
        time.sleep(2)  # Wait for page to load
        driver.save_screenshot(f"screenshots/{page_name}.png")
        print(f"Screenshot saved: {page_name}.png")
        
finally:
    driver.quit()