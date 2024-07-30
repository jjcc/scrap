from io import BytesIO
import json
import re
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
from selenium.webdriver.common.print_page_options import PrintOptions
import base64
from selenium.webdriver.firefox.options import Options

'''
This is the  step for collecting sites
'''

firefox_options = Options()
firefox_options.set_preference("print.always_print_silent", True)
firefox_options.set_preference("print.printer_name", "Microsoft Print to PDF")
firefox_options.set_preference("print.print_to_file", True)
firefox_options.set_preference("print.print_to_filename", "output/output_new.pdf")


def search_and_capture_screenshots(search_terms, urls_by_term=None,lang = 'en'):
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #urls_by_term = json.load(open("data/search_results_2024-07-10_22-01-02.json"))
    #urls_by_term = json.load(open("data/search_results_think-tank_2024-07-16_02-07-52.json"))
    # Initialize the Firefox WebDriver with options
    driver = webdriver.Firefox(options=firefox_options)

    keep = {}
    for term, urls in urls_by_term.items():
        keep[term] = []
    #for term in search_terms:
    #    keep[term] = []
        # Create a folder for the search term
        #folder_name = term.replace(" ", "_")
        #os.makedirs(f"img/{folder_name}", exist_ok=True)
        urls = urls_by_term[term]
        # Visit each URL and take a screenshot
        for i, url in enumerate(urls):
            if 'translate' in url and 'google' in url:
                pattern = r'&u=(.*?)(?:&|$)'
                match = re.search(pattern, url)
                
                if match:
                    extracted_url = match.group(1)
                    url = extracted_url
                else:
                    print(f"Could not extract URL from {url}")
                    continue
            if 'wikipedia' in url:
                continue
            if '2024' not in url:
                continue


            try:
                reader_mode_url = f"about:reader?url={url}"
                driver.get(reader_mode_url)
                # Wait for the page to load
                wait = WebDriverWait(driver, 10)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                time.sleep(5)
                print_options = PrintOptions()
                pdf = driver.print_page(print_options=print_options)
                output_dir = "output/news"
                output_file = f"{output_dir}/{lang}_{term}_{i}.pdf"
                with open(output_file, 'wb') as file:
                   file.write(base64.b64decode(pdf))


                
                # Wait for the page to load and PDF to be generated
                time.sleep(10)
                #driver.get(url)
                #time.sleep(2)  # Wait for page to load
                
                # Prompt user for input
                #user_input = input(f"Keep this URL? ({url}) [y/n]: ").lower()
                #if user_input != "y":
                #    print(f"Skipping {url}")
                #    continue
                keep[term].append(url)

                # Take screenshot
                #screenshot = driver.get_screenshot_as_png()
                
                ## Save and resize screenshot
                #img = Image.open(BytesIO(screenshot))
                #img.thumbnail((900, 900))  # Resize to thumbnail
                ## get last part of URL
                #url_parts = url.split("/")
                #last_part = url_parts[-1] if url_parts[-1] else url_parts[-2]

                #img_file = f"img/{folder_name}/scr_{last_part}_{i}.png"
                #img.save(img_file, "PNG")
                
            except Exception as e:
                print(f"Error capturing screenshot for {url}: {e}")

        with open(f"output/news/{lang}_{term}.json", "w") as f:
            json.dump(keep, f, indent=4)
        time.sleep(2)  # Wait between searches
    
    driver.quit()

# Example usage
if __name__ == "__main__":
    from helper.common import kw2b_en, kw2b_fr, kw2b_jp, kw2b_ge, news
    kw_list = {"en":kw2b_en, "fr":kw2b_fr,"ge":kw2b_ge,"jp":kw2b_jp }
    kw2b = kw2b_en
    list_kw =[k.strip() for k in  kw2b.split(",")]
    #search_terms = [k + " news" for k in list_kw]
    #search_terms = [k + " 'think tank'" for k in list_kw]
    for dirpath, dirnames, filenames in os.walk("input"):

        for filename in filenames:
            if not filename.endswith(".json"):
                continue
            segs = filename.split("_")
            topic = segs[2]
            lang = segs[3]
            kw2b = kw_list.get(lang)
            news_lang = news.get(lang)
            if topic != news_lang:
                print("The topic is not supported")
                continue
            list_kw =[k.strip() for k in  kw2b.split(",")]
            search_terms = [k + f" {news_lang}" for k in list_kw]
            filewithpath = os.path.join(dirpath, filename)

            urls_by_term = json.load(open(os.path.join(dirpath, filename)))

            #print(f"lang: {lang}")
            #with open(os.path.join(dirpath, filename)) as f:
            #    search_terms = f.read().splitlines()
            if lang == 'ge':
                continue
            search_and_capture_screenshots(search_terms, urls_by_term,lang)


            #search_and_capture_screenshots(search_terms)