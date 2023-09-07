from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def wait_and_get_element(driver: WebElement, by: By, value: str, timeout=10) -> WebElement:
    """Wait for an element to be show in html and return it.

    Args:
        driver (WebElement): The driver to use.
        by (By): by id, name, tag_name, ...
        value (str): name of the element.
        timeout (int, optional): timeout of waiting. Defaults to 10.

    Returns:
        WebElement: The element.
    """
    wait = WebDriverWait(driver, timeout)
    wait.until(EC.presence_of_element_located((by, value)))
    return driver.find_element(by, value)


def wait_until_clickable(driver: WebElement, by: By, value: str, timeout=10) -> WebElement:
    """Wait for an element to be clickable and return it.

    Args:
        driver (WebElement): The driver to use.
        by (By): by id, name, tag_name, ...
        value (str): name of the element.
        timeout (int, optional): timeout of waiting. Defaults to 10.

    Returns:
        WebElement: The element.
    """
    wait = WebDriverWait(driver, timeout)
    wait.until(EC.element_to_be_clickable((by, value)))
    return driver.find_element(by, value)


def get_element_if_exists(element: webdriver.WebKitGTK, by: str, value: str) -> WebElement:
    """Get an element if it exists.

    Args:
        element (webdriver.WebKitGTK): The element to search in.
        by (str): by id, name, tag_name, ...
        value (str): name of the element.
    
    Returns:
        WebElement: The element if it exists, None otherwise.
    """
    try:
        return element.find_element(by, value)
    except NoSuchElementException:
        return None
