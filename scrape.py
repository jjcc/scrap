from datetime import datetime
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
'''
The first step: to collect the urls from general search
'''


def search_and_collect_urls(engine_url, search_terms,lang = 'en'):
    # Set up the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    results = {}
    
    for term in search_terms:
        # Navigate to Google

        target_url = f"{engine_url}search?q={term}&hl={lang}"
        #driver.get(engine_url)
        driver.get(target_url)
        
        ## Find the search box and enter the search term
        #search_box = WebDriverWait(driver, 10).until(
        #    EC.presence_of_element_located((By.NAME, "q"))
        #)
        #search_box.send_keys(term)
        #search_box.send_keys(Keys.RETURN)
        
        # Wait for the results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search"))
        )
        
        # Collect the URLs
        result_links = driver.find_elements(By.CSS_SELECTOR, "div.g div.yuRUbf a")
        urls = [link.get_attribute("href") for link in result_links]
        
        results[term] = urls
        
        # Wait a bit to avoid overwhelming Google
        time.sleep(2)
    
    driver.quit()
    return results


def search_by_keywords( topic,lang = 'en'):
    from helper.common import kw2b_en, kw2b_fr, kw2b_jp, kw2b_ge
    from helper.common import news

    kw_list = {"en":kw2b_en, "fr":kw2b_fr,"ge":kw2b_ge,"jp":kw2b_jp }
    if topic not in ['news','think_tank']:
        print("The topic is not supported")
        return
    if topic == 'news':
        topic =  news.get(lang)

    kw2b = kw_list.get(lang)
    list_kw =[k.strip() for k in  kw2b.split(",")]
    # for now, just add topic at the end of a search tearm
    search_terms = [k + f" {topic}" for k in list_kw]

    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d_%H-%M-%S")

    engines = {'en':'https://www.google.com/','fr':'https://www.google.fr/', 'jp':'https://www.google.jp/','ge':'https://www.google.ge/'}
    engine = engines.get(lang)

    results = search_and_collect_urls(engine, search_terms, lang)

    with open(f"data/search_results_{topic}_{lang}_{now_str}.json", "w") as f:
        json.dump(results, f, indent=4)
    
    # Print the results
    for term, urls in results.items():
        print(f"Search term: {term}")
        for url in urls:
            print(f"  - {url}")
        print()

def search_by_different_topic_lang():
    for topic in ['news']:
        lang = ['en','jp','fr','ge']
        for l in lang:
            search_by_keywords( topic, lang=l)


def search_simple(engine_url, term, lang):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    target_url = f"{engine_url}search?q={term}&hl={lang}"
    driver.get(target_url)
    time.sleep(2)

if __name__ == "__main__":
    search_by_different_topic_lang()
    #search_by_keywords("news")
    #search_by_keywords("'think tank'")
    #search_simple("https://www.google.com/","無人水上艦艇ニュース","ja")