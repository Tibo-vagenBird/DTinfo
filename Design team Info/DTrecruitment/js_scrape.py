import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.EdgeOptions()
options.add_argument('--log-level=3')
options.add_argument('--headless')
service = EdgeService(r'D:/myCodeP/Edge_Driver/msedgedriver.exe')
driver = webdriver.Edge(options=options, service=service)

df = pd.read_csv('D:/myCodeP/LearnBasic/output_files/name_time.csv')
urls = df['Recruitment']

def check_buttons(teamname, driver):
    
    try:
        collapsed = driver.find_elements(
            By.XPATH,
            "//button[not(ancestor::header) and not(ancestor::footer)]"
            " | "
            "//*[@aria-expanded='false' and not(ancestor::header) and not(ancestor::footer)]"
            " | "
            "//*[contains(@class,'accordion-item-trigger') and not(ancestor::header) and not(ancestor::footer)]"
            )
        
        button_href = []
        overlay_texts = {}
        div_texts = {}

    except NoSuchElementException:
        return [], {}, {}
    
    for btn in collapsed:
        if btn.is_displayed() and btn.is_enabled():
            # href button
            try:
                hrefs = btn.get_attribute('href')
                if hrefs:
                    btn_name = btn.text.strip()
                    button_href.append(btn_name + hrefs)
                    continue
            except Exception:
                pass

            try:
                btn.click()
                time.sleep(0.5)
                
                # if orbit
                if teamname == 'Orbit':
                    try:
                        header_o, text_o = for_orbit(driver)
                    except Exception:
                        header_o, text_o = None, None

                    if header_o and text_o:
                        div_texts[header_o] = []
                        div_texts[header_o].append(text_o)
                        continue

                # overlay button
                try:
                    header_l, text_l = over_lay_button(driver)
                except Exception:
                    header_l, text_l = None, None

                if header_l and text_l:
                    overlay_texts[header_l] = []
                    overlay_texts[header_l].append(text_l)

            except (ElementClickInterceptedException, TimeoutException):
                continue

    return button_href, overlay_texts, div_texts

def over_lay_button(driver):
    overlay_div = WebDriverWait(driver, 1).until(
        EC.visibility_of_element_located((By.ID, "outer-overlay"))
    )
    elements = overlay_div.find_elements(By.CSS_SELECTOR, "p, a, ul, h1, h2, h3")

    header = ""
    for elt in elements:
        tag = elt.tag_name.lower()

        if tag == "h1":
            h1 = elt.text.strip()
            header = h1
        else:
            text = elt.text.strip()

    driver.execute_script("arguments[0].click();", overlay_div)
    time.sleep(0.5)
    
    return header, text

def for_orbit(driver):
    header = None
    paragraphs = []

    try:
        section = driver.find_element(
            By.CSS_SELECTOR,
            ".py-10.max-w-4xl.mx-auto.text-left.text-gray-700.px-4.sm\\:px-6"
        )
                                      
        try:
            h3_elt = section.find_element(By.TAG_NAME, "h3")
            header = h3_elt.text.strip()
            print(header)
        except NoSuchElementException:
            header = None

        para = section.find_elements(By.CSS_SELECTOR, "p, a, li, span")
        for p in para:
            txt = p.text.strip()
            if txt:
                paragraphs.append(txt)
    except NoSuchElementException:
        return None, []
        
    return header, paragraphs


def extract_visible_text(driver):
    body = driver.find_element(By.TAG_NAME, "body")
    full_text = body.text

    hrefs = []
    a_eles = body.find_elements(By.TAG_NAME, "a")
    for a in a_eles:
        href = a.get_attribute("href")
        try:
            href_tag = a.text.strip()
        except NoSuchElementException:
            href_tag = ""

        hrefs.append(f"{href_tag}: {href}")

    header_text = None
    header_hrefs = []
    try:
        headers = body.find_elements(By.TAG_NAME, "header")
        header_text = " ".join(h.text for h in headers if h.text)

        hrefs = headers.get_attribute("href")
        header_hrefs.append(hrefs)
    except Exception:
        header_text = ""
        header_hrefs = []

    footer_text = ""
    footer_hrefs = []
    try:
        footers = body.find_elements(By.TAG_NAME, "footer")
        footer_text = " ".join(f.text for f in footers if f.text)

        hrefs = footers.get_attribute("href")
        footer_hrefs.append(hrefs)
    except Exception:
        footer_text = ""

    visible_only = full_text
    if header_text:
        visible_only = visible_only.replace(header_text, "")
    if header_hrefs:
        hrefs = list(set(hrefs) - set(header_hrefs))
    if footer_text:
        visible_only = visible_only.replace(footer_text, "")
    if footer_hrefs:
        hrefs = list(set(hrefs) - set(footer_hrefs))
        
    visible_only = visible_only.strip()

    return visible_only, hrefs

    
def main():
    with open('D:/myCodeP/LearnBasic/DTpage_text6.txt', 'w', encoding='utf-8') as f:
        for idx, url in enumerate(urls):
            name = df['Team Name'][idx]
            
            print(f"[+] Loading: {url}")

            try:
                driver.get(url)
            except Exception as e:
                print(f"  -> Failed to load {url}: {e}")
                continue

            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, 'body'))
                )
            except TimeoutException:
                print(f"        -> Timeout waiting for body on {url}")
            
            button_hrefs, overlay_texts, orbit_texts = check_buttons(name, driver)

            visible_only, hrefs = extract_visible_text(driver)

            time.sleep(1)

            f.write(f"=== {name} ===\n")
            f.write(visible_only + "\n")
            for href in button_hrefs:
                f.write(href + "\n")
            f.write(f"{str(overlay_texts)}\n")
            if orbit_texts:
                f.write(f"{str(orbit_texts)}\n")
            if hrefs:
                for href in hrefs:
                    f.write(href + "\n")
            f.write("------------\n\n")


main()

driver.quit()

