from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup


def use_selenium(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--log-level=3")  
    chrome_options.add_argument("--disable-logging") 
    chrome_options.add_argument("--silent")  

    service = Service(log_path="/dev/null")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)
    html = driver.page_source
    driver.quit()

    return BeautifulSoup(html, 'html.parser')

def use_requests(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(f'Page "{url}" not found: {response}')