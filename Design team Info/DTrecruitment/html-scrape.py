import httpx, asyncio, time, random
import requests
import pandas as pd
from bs4 import BeautifulSoup

df = pd.read_csv("D:/myCodeP/LearnBasic/output_files/name_time.csv")
links = df["Recruitment"]
team_name = df["Team Name"]

HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0")
}

async def fetch(url, retries=3, cooldown=(1, 3)):
    for i in range(retries):
        try:
            async with httpx.AsyncClient(timeout=15, headers=HEADERS) as client:
                r = await client.get(url)
                r.raise_for_status()
                return r.text
        except httpx.HTTPError:
            if i == retries - 1:
                return None
            await asyncio.sleep(random.uniform(*cooldown))

async def scrape_all():
    with open('D:/myCodeP/LearnBasic/DTpage_text4.txt', 'w', encoding='utf-8') as file:
        for idx, link in enumerate(links):
            name = team_name[idx]
            if isinstance(link, str) and link.strip():
                html = await fetch(link)
                if html:
                    soup = BeautifulSoup(html, 'html.parser')
                    text = soup.get_text(separator='\n', strip=True)
                    if "You need to enable JavaScript to run this app." in text:
                        print(name +" "+ link)
                        file.write(name + "\n\n")
                    else:
                        file.write(name + '\n')
                        file.write(text)
            file.write('\n-----------------------------\n')

asyncio.run(scrape_all())

