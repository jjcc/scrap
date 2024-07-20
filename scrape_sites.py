from io import BytesIO
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import os
import time
'''
This is the  step for collecting sites
'''

def search_and_capture_screenshots(search_terms):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #urls_by_term = json.load(open("data/search_results_2024-07-10_22-01-02.json"))
    urls_by_term = json.load(open("data/search_results_think-tank_2024-07-16_02-07-52.json"))

    keep = {}
    for term in search_terms:
        keep[term] = []
        # Create a folder for the search term
        folder_name = term.replace(" ", "_")
        os.makedirs(f"img/{folder_name}", exist_ok=True)
        urls = urls_by_term[term]
        

        # Visit each URL and take a screenshot
        for i, url in enumerate(urls):
            try:
                driver.get(url)
                time.sleep(2)  # Wait for page to load
                
                                # Prompt user for input
                user_input = input(f"Keep this URL? ({url}) [y/n]: ").lower()
                if user_input != "y":
                    print(f"Skipping {url}")
                    continue
                keep[term].append(url)
                # Take screenshot
                screenshot = driver.get_screenshot_as_png()
                
                # Save and resize screenshot
                img = Image.open(BytesIO(screenshot))
                img.thumbnail((900, 900))  # Resize to thumbnail
                # get last part of URL
                url_parts = url.split("/")
                last_part = url_parts[-1] if url_parts[-1] else url_parts[-2]

                img_file = f"img/{folder_name}/scr_{last_part}_{i}.png"
                img.save(img_file, "PNG")
                
            except Exception as e:
                print(f"Error capturing screenshot for {url}: {e}")
        
        time.sleep(2)  # Wait between searches
    
    driver.quit()

# Example usage
if __name__ == "__main__":
    from helper.common import kw2b_en
    kw2b = kw2b_en
    list_kw =[k.strip() for k in  kw2b.split(",")]
    #search_terms = [k + " news" for k in list_kw]
    search_terms = [k + " 'think tank'" for k in list_kw]
    search_and_capture_screenshots(search_terms)