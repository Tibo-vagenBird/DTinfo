import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin, urlparse

def is_relative_link(href):
    parsed = urlparse(href)
    return not parsed.scheme or not parsed.netloc

# Setup Edge driver
options = webdriver.EdgeOptions()
options.add_argument('--log-level=3')
options.add_argument('--headless')
service = EdgeService(r'D:\myCodeP\Edge_Driver\msedgedriver.exe')
driver = webdriver.Edge(options=options, service=service)

# Load data
df = pd.read_csv('D:/myCodeP/LearnBasic/name_time.csv')
urls = df['Links']
recruitment = []

def get_recruitment_link():
    target_keywords = ['recruitment', 'join us', 'join', 'apply']
    special_keywords = ['more']

    for url in urls:
        found_link = []

        try:
            driver.get(url)
            time.sleep(3)
            print(f'🟢 Page loaded: {url}')

            links = driver.find_elements(By.TAG_NAME, 'a')
            txt_elements = driver.find_elements(By.CSS_SELECTOR, 'button, p, span')

            for txt in txt_elements:
                text = txt.text.strip()

                if any(skw in text.lower() for skw in special_keywords):
                    try:
                        button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), '{text}')]"))
                        )
                        button.click()
                        print(f"✅ Clicked: '{text}'")
                        time.sleep(3)
                        links = driver.find_elements(By.TAG_NAME, 'a')  # refresh
                    except Exception as click_err:
                        print(f"⚠️ Couldn't click '{text}': {click_err}")

            for link in links:
                href = link.get_attribute('href')
                link_text = link.text.strip().lower()

                if any(kw in link_text for kw in target_keywords):
                    if href and is_relative_link(href):
                        full_link = urljoin(url, href)
                        found_link.append(full_link)
                    elif href:
                        found_link.append(href)

            recruitment.append(found_link[0] if found_link else '')
            print(f"🔗 Recruitment link found: {recruitment[-1]}")

        except Exception as e:
            print(f'❌ Error on {url}: {e}')
            #recruitment.append('')

    df['Recruitment'] = recruitment
    df.to_csv('D:/myCodeP/LearnBasic/name_time.csv', index=False)
    print("✅ Recruitment links saved to CSV.")

get_recruitment_link()
driver.quit()

def read_all_recuitment_pages():
    join_links = df['Recruiment']

    for link in join_links:
        driver.get(link)
        time.sleep(3)

        html = driver.page_source
        soup2 = BeautifulSoup(html, 'lxml')

        soup2


get_recruitment_link()



