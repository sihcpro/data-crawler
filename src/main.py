from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from constants import SITE


def init_chrome_driver() -> webdriver.Chrome:
    """
    Initialize a Chrome webdriver.

    Returns:
        webdriver.Chrome: The Chrome webdriver.
    """
    driver = webdriver.Chrome()
    return driver

def search_word(driver: webdriver.WebKitGTK, word: str):
    """
    Search for a word on the City Clerk Connect website.

    Args:
        word (str): The word to search for.
    """
    driver.get(SITE)
    search_bar = driver.find_element(By.ID, "basicsearch")
    search_bar.clear()
    search_bar.send_keys(word)
    search_bar.send_keys(Keys.RETURN)

def get_search_results(driver: webdriver.WebKitGTK) -> list:
    """
    Get the search results from the City Clerk Connect website.

    Args:
        driver (webdriver.WebKitGTK): The Chrome webdriver.

    Returns:
        dict: The search results.
    """
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.ID, 'xboxholder')))
    xboxholder = driver.find_element(By.ID, "xboxholder")
    wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'b')))
    if "no results" in xboxholder.find_element(By.TAG_NAME, "b").text:
        return []

    wait.until(EC.element_to_be_clickable((By.ID, 'CFIResultList')))
    search_table = driver.find_element(By.ID, "CFIResultList")
    results = search_table.find_elements(By.TAG_NAME, "tr")[1:]
    return results


def get_data_from_data_page(driver: webdriver.WebKitGTK) -> dict:
    driver
    return {}


def get_data_from_element(driver: webdriver.WebKitGTK, element: WebElement):
    href = element.find_element(By.TAG_NAME, "a").get_attribute("href")
    driver.execute_script(f"window.open('{href}');")
    driver.switch_to.window(driver.window_handles[1])    
    data = get_data_from_data_page(driver)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return data

def main() -> None:
    """
    The main function.
    """
    driver = init_chrome_driver()
    search_word(driver, "test")
    results = get_search_results(driver)
    for result in results:
        get_data_from_element(driver, result)
        break
    input("Press enter to exit...")
    driver.close()


if __name__ == "__main__":
    main()
