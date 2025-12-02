import subprocess
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Start Flask app
flask_process = subprocess.Popen(['python', 'main.py'], cwd=os.getcwd())
time.sleep(5)  # Wait for Flask to start

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)

# Base URL
base_url = "http://127.0.0.1:5000"

# Marketplace pages
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
        time.sleep(3)
        driver.save_screenshot(f"screenshots/{page_name}.png")
        print(f"Screenshot saved: {page_name}.png")
        
finally:
    driver.quit()
    flask_process.terminate()