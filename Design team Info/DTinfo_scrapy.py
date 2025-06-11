import requests
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from bs4 import BeautifulSoup
'''
url = "https://experience.apsc.ubc.ca/sites/default/files/styles/hero_focal_point_2600/public/2023-06/UBC-AgroBot-2-scaled.jpg?h=7eabb7da&itok=K9EnzJKe"
response = requests.get(url, timeout=10)

filepath = "D:/myCodeP/LearnBasic/tryDown_pic1.jpg"

if not os.path.exists(filepath):
    with open(filepath, 'wb') as f:
        f.write(response.content)
    print("download")
else:
    print("has been downloaded")
'''

options = webdriver.EdgeOptions()
options.add_argument('--log-level=3')
options.add_argument('--headless')

service = EdgeService(r'D:\myCodeP\Edge_Driver\msedgedriver.exe')

driver = webdriver.Edge(service=service, options=options)


def basicScrapy():
    driver.get('https://experience.apsc.ubc.ca/student-groups/engineering-design-teams-list')

    time.sleep(3)

    # get all <a> tags inside <article> card
    team_elements = driver.find_elements(By.CSS_SELECTOR, 'article a.no-underline.link-expand')
    team_links = [link.get_attribute('href') for link in team_elements]

    file_path = 'D:/myCodeP/LearnBasic/design_team_info.txt'

    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:

            for href in team_links:
                driver.get(href)
                time.sleep(2)

                html = driver.page_source
                soup2 = BeautifulSoup(html, 'lxml')

                title_div = soup2.find('div',class_="w-screen md--w-auto md--mb-molecule-2 md---mx-organism-4 relative")
                team_name_h1 = title_div.find('h1', class_='mt-4')
                team_name = team_name_h1.find('span').text.strip()
                team_catagories = title_div.find('h3',class_='h4 uppercase mt-8 md--mt-10').text.strip()

                file.write(f'{team_name}\n')
                print(team_name)
                file.write(f'{team_catagories}\n')

                body_div = soup2.find('div', class_='node__content clearfix flow-root')
                body_elements = body_div.find_all(['ul','p'])
                time_div = body_elements[-1].find_all('span')
                for time_info in time_div:
                    file.write(time_info.text.strip() + '\n')
            
                teamWeb_a = soup2.find('a', class_='link-button h4 flex p-6 mt-8 border border-neutral-200 items-center justify-between no-underline')
                teamWeb = teamWeb_a.get('href')
                file.write(teamWeb + '\n')

                file.write(f'\n')

import re

def is_url(line):
    url_pattern = re.compile(
        r'^(https?|ftp):\/\/'                  # http://, https://, or ftp://
        r'(\S+\.\S+)'                          # at least one dot (domain)
        r'(\S*)$', re.IGNORECASE)             # rest of the URL (optional)
    return re.match(url_pattern, line.strip()) is not None

web_url = []

def extract_teamweb_link():
    with open('D:/myCodeP/LearnBasic/design_team_info.txt', 'r') as file:
        for line in file:
            if is_url(line):
                web_url.append(line)
    print(web_url[1:10])

def to_recuitment():

    extract_teamweb_link()

    for team_url in web_url:
        driver.get(team_url)
        time.sleep(2)

        html = driver.page_source
        soup2 = BeautifulSoup(html, 'lxml')

        href = soup2.find('a', class_='')

        print(f'success')

to_recuitment()




