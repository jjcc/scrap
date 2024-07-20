import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time

def translate(url_to_translate):
    # Set up Firefox options
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.set_preference("print.always_print_silent", True)
    firefox_options.set_preference("print.printer_name", "Microsoft Print to PDF")
    firefox_options.set_preference("dom.disable_beforeunload", True)
    
    # Initialize the Firefox driver
    driver = webdriver.Firefox(options=firefox_options)
    
    # Navigate to Google Translate
    driver.get("https://translate.google.com/?sl=auto&tl=zh-CN&op=translate")
    
    # Wait for the source language input field to be visible
    wait = WebDriverWait(driver, 3)
    
    
    
    websites_span = driver.find_element(By.XPATH, "//span[text()='Websites']")
    websites_span.click()
    #time.sleep(3)
    #url_input = driver.find_element(By.CSS_SELECTOR, "input[type='url']")
    url_input= wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='url']")))
    
    #lang_select = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "VfPpkd-Bz112c-RLmnJb")))
    #lang_select.click()
    
    
    # Enter the URL you want to translate
    url_input.send_keys(url_to_translate)
    
    path_start = "M12 4l-1.41"
    xpath_expression = f"//path[starts-with(@d, '{path_start}')]"
    
    svg_path_element = driver.find_elements(By.XPATH, "//*[local-name()='path' and starts-with(@d, 'M12 4l-1.41')]")
    if len(svg_path_element) > 0:
        svg_path_element0 = svg_path_element[0]
        svg_path_element0.click()
    
    # Wait for the translation to load
    time.sleep(5)
    
    # Switch to the translated page
    driver.switch_to.window(driver.window_handles[-1])
    
    
    # Simulate pressing F9 using JavaScript
    driver.execute_script("window.dispatchEvent(new KeyboardEvent('keydown', {'key': 'F9'}))")
    driver.execute_script("window.dispatchEvent(new KeyboardEvent('keyup', {'key': 'F9'}))")
    
    # # Enable reader view
    # actions = ActionChains(driver)
    
    # # Simulate pressing F9
    # actions.send_keys(Keys.F9).perform()
    
    
    # Wait for the reader view to load
    time.sleep(3)
    
    # Print to PDF
    driver.execute_script("window.print();")
    
    # Wait for the print dialog to appear and complete
    #time.sleep(5)
    
    # Close the browser
    driver.quit()

if __name__ == "__main__":
    #url = "https://dronelife.com/2024/07/08/anti-jamming-drones-enhancing-battlefield-resilience/"
    with open("temp.json") as f:
        sites = json.load(f)
    for collection, urls in sites.items():
        for url in urls:
            translate(url)
