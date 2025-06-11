import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

target_keywords = ['recruitment', 'join us', 'join', 'apply']
special_keywords = ['more']

def is_relative_link(href):
    parsed = urlparse(href)
    return not parsed.scheme or not parsed.netloc

def static_scrape(url):
    found_links = []

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')

        print(f"\nLinks from {url}")

        for link in soup.find_all('a'):
            href = link.get('href')
            link_text = link.get_text(strip=True)

            if any(kw in link_text.lower() for kw in target_keywords):
                if href and is_relative_link(href):
                        full_link = urljoin(url, href)
                        found_links.append(full_link)
                elif href:
                        found_links.append(href)

        return found_links[0]
                
    
    except Exception as e:
        print(f"Error on {url}: {e}")

df = pd.read_csv('D:/myCodeP/LearnBasic/name_time.csv')
web_link = df['Links']
exist_re = df['Recruitment']

for idx, link in enumerate(df['Links']):
    recruitment_link = static_scrape(link)
    df.at[idx, 'Recruitment'] = recruitment_link

df.to_csv('D:/myCodeP/LearnBasic/name_time_static.csv', index=False)