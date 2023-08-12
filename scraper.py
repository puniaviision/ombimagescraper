import requests
from bs4 import BeautifulSoup
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chrome_driver_path = '/Users/punia/Desktop/Folders/chromedriver-mac-arm64/chromedriver'

service = Service(chrome_driver_path)

driver = webdriver.Chrome(service=service)

url = "https://ordiscan.com/collection/omb"
driver.get(url)

time.sleep(5)

div_elements = driver.find_elements(By.CSS_SELECTOR, 'div[style*="background-image"]')

last_len = 0
while True:
    # Scroll down
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Wait for new images to load
    time.sleep(5)
    
    # Collect the new set of image URLs
    div_elements = driver.find_elements(By.CSS_SELECTOR, 'div[style*="background-image"]')
    new_file_urls = [div.get_attribute('style').split('"')[1] for div in div_elements]
    
    # Check if there are new images
    if len(new_file_urls) == last_len:
        break
    
    # Update the file URLs
    file_urls = new_file_urls
    last_len = len(file_urls)

print(file_urls)

driver.quit()

output_folder = "ordinals"
os.makedirs(output_folder, exist_ok=True)

for idx, file_url in enumerate(file_urls):
    file_name = f"image_{idx}.jpeg"
    file_path = os.path.join(output_folder, file_name)
    response = requests.get(file_url, stream=True)
    print("Downloading image", idx)

    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
    else:
        print(f"Failed to download {file_url}")

print("Download complete!")
