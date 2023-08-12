import requests
from bs4 import BeautifulSoup
import os

url = "https://ordiscan.com/collection/omb" # Replace with the URL you want to scrape
response = requests.get(url)

if response.status_code == 200:
    html_content = response.text
else:
    print("Failed to fetch the webpage")
    exit()

soup = BeautifulSoup(html_content, 'html.parser')

file_urls = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.jpeg')]

output_folder = "ordinals"
os.makedirs(output_folder, exist_ok=True)

for file_url in file_urls:
    file_name = os.path.basename(file_url)
    file_path = os.path.join(output_folder, file_name)
    response = requests.get(file_url, stream=True)

    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
    else:
        print(f"Failed to download {file_url}")