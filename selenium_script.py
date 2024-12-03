from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def linkedin_login(driver, username, password):
    driver.get('https://www.linkedin.com/login')
    time.sleep(2)

    username_input = driver.find_element(By.ID, 'username')
    password_input = driver.find_element(By.ID, 'password')

    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    time.sleep(2)

def fetch_profile_data(driver, profile_url):
    driver.get(profile_url)
    time.sleep(2)

    # Wait for the profile content to load fully
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'text-body-medium')))  # Wait for title element

    # Scroll down in multiple steps to ensure all content loads
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract Name
    name = 'Not Available'
    name_element = soup.find('h1', {'class': 'text-heading-xlarge'})
    if name_element:
        name = name_element.get_text(strip=True)

    # Extract Title (Professional Headline)
    title = 'Not Available'
    title_element = soup.find('div', {'class': 'text-body-medium'})
    if title_element:
        title = title_element.get_text(strip=True)

    # Extract Location
    location = 'Not Available'
    location_element = soup.find('span', {'class': 'text-body-small'})
    if location_element:
        location = location_element.get_text(strip=True)

    # Extract About Section
    about = 'Not Available'
    about_section = soup.find('section', {'id': 'about'})
    if about_section:
        about_text = about_section.find('span', {'class': 'visually-hidden'})
        if about_text:
            about = about_text.get_text(strip=True)

    # Return cleaned data
    return {
        'Name': name,
        'Title': title,
        'Location': location,
        'About': about
    }

def fetch_data_via_selenium(username, password, first_name, last_name):
    search_query = f"{first_name} {last_name} site:linkedin.com"

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    linkedin_login(driver, username, password)

    driver.get("https://www.google.com/")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(search_query)
    search_box.submit()

    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    profile_urls = []

    for element in soup.select('.g'):
        link = element.find('a', href=True)
        if link and "linkedin.com/in" in link['href']:
            profile_urls.append(link['href'])

            if len(profile_urls) == 5:  # Fetch the first 5 relevant profiles
                break

    profile_data = []
    for url in profile_urls:
        data = fetch_profile_data(driver, url)
        profile_data.append(data)

    driver.quit()
    return profile_data

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

if __name__ == "__main__":
    username = 'sanjuhoskal@gmail.com' 
    password = 'Sanju@07072000' 
    first_name = 'Sanjay' 
    last_name = 'P' 

selenium_data = fetch_data_via_selenium(username, password, first_name, last_name)
save_to_csv(selenium_data, 'linkedin_profile_data.csv')