from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up Firefox options to enable Marionette
firefox_options = webdriver.FirefoxOptions()
firefox_options.set_preference('devtools.chrome.enabled', True)
firefox_options.set_preference('devtools.debugger.remote-enabled', True)

# Initialize the Firefox WebDriver with options
driver = webdriver.Firefox(options=firefox_options)

try:
    # Navigate to the specific URL
    url = "https://dronelife.com/2024/07/08/anti-jamming-drones-enhancing-battlefield-resilience/"
    driver.get(url)

    # Wait for the page to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Switch to Marionette context
    driver.execute_script("window.focus();")
    original_context = driver.context
    driver.context = 'chrome'

    # Try to find all elements in the chrome context
    try:
        # Find all elements
        all_elements = driver.find_elements(By.XPATH, "//*")
        
        print(f"Found {len(all_elements)} elements in the chrome context")
        
        # Print details of elements that might be related to reader mode
        for element in all_elements:
            try:
                element_id = element.get_attribute('id')
                element_class = element.get_attribute('class')
                element_tag = element.tag_name
                print(f"### text: {element.text} ###")
                if 'reader' in str(element_id).lower() or 'reader' in str(element_class).lower():
                    print(f"Potential reader mode element: Tag: {element_tag}, ID: {element_id}, Class: {element_class}")
            except:
                pass  # Ignore elements that can't be inspected

    except Exception as e:
        print(f"Failed to find elements in chrome context: {e}")

    # Switch back to content context
    driver.context = original_context

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Keep the browser open for a few seconds so you can see the result
    time.sleep(10)
    # Close the browser
    driver.quit()
