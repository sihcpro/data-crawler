import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from constants import SITE
from helper import get_element_if_exists, wait_and_get_element, wait_until_clickable


def init_chrome_driver() -> webdriver.Chrome:
    """
    Initialize a Chrome webdriver.

    Returns:
        webdriver.Chrome: The Selenium webdriver.
    """
    driver = webdriver.Chrome()
    driver.maximize_window()
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
        driver (webdriver.WebKitGTK): The Selenium webdriver.

    Returns:
        dict: The search results.
    """
    wait_and_get_element(driver, By.ID, "xboxholder")
    search_result = wait_and_get_element(driver, By.TAG_NAME, "b")
    if not search_result or "no results" in search_result.text:
        return []

    search_table = wait_and_get_element(driver, By.ID, "CFIResultList")
    results = search_table.find_elements(By.TAG_NAME, "tr")[1:]
    return results


def is_have_left_right_section(element: WebElement) -> bool:
    try:
        element.find_element(By.CLASS_NAME, "left")
        return True
    except NoSuchElementException:
        return False


def get_attachment_info_from_activity(element: WebElement) -> list[dict]:
    content = element.find_element(By.ID, "WzBoDyI")
    documents = content.find_elements(By.TAG_NAME, "table")
    results = []
    for document in documents:
        tabs = document.find_elements(By.TAG_NAME, "td")
        title, date = tabs[0].text, tabs[1].text
        href = get_element_if_exists(tabs[0], By.TAG_NAME, "a").get_attribute("href")
        result = {"title": title, "date": date, "href": href}
        results.append(result)
    return results


def get_file_activities(driver: webdriver.WebKitGTK, element: WebElement) -> list[dict]:
    table = element.find_element(By.CLASS_NAME, "rectext")
    table_data = table.find_elements(By.TAG_NAME, "tr")[1:]
    results = []
    for row in table_data:
        tabs = row.find_elements(By.TAG_NAME, "td")
        date, activity = tabs[0].text, tabs[1].text
        attachment_img = get_element_if_exists(tabs[2], By.TAG_NAME, "img")
        attachments = []
        if attachment_img:
            attachment_img.click()
            wait_until_clickable(driver, By.ID, "WzClOsE")
            element = wait_and_get_element(driver, By.ID, "WzBoDy")
            attachments = get_attachment_info_from_activity(element)
            driver.find_element(By.ID, "WzClOsE").click()

        result = {"date": date, "activity": activity, "attachments": attachments}
        results.append(result)
    return results


def get_section_data(
    driver: webdriver.WebKitGTK, element: WebElement
) -> tuple[str, str]:
    POSSIBLE_TITLE = ["reclabel"]
    POSSIBLE_VALUE = ["recvalue", "rectext"]

    title, value = None, None
    for possible_title in POSSIBLE_TITLE:
        title = get_element_if_exists(element, By.CLASS_NAME, possible_title)
        if title:
            title = title.text
            break

    if title == "File Activities":
        value = get_file_activities(driver, element)
        return title, value

    for possible_value in POSSIBLE_VALUE:
        value = get_element_if_exists(element, By.CLASS_NAME, possible_value)
        if value:
            value = value.text
            break
    return title, value


def generate_section_data(
    driver: webdriver.WebKitGTK, element: WebElement
) -> tuple[str, str, int]:
    fields = element.find_elements(By.CLASS_NAME, "section")
    for i, field in enumerate(fields):
        if is_have_left_right_section(field):
            title, value = get_section_data(
                driver, field.find_element(By.CLASS_NAME, "left")
            )
            yield title, value, i

            title, value = get_section_data(
                driver, field.find_element(By.CLASS_NAME, "right")
            )
            yield title, value, i
        else:
            title, value = get_section_data(driver, field)
            yield title, value, i


def get_primary_data(driver: webdriver.WebKitGTK) -> dict:
    MANDATORY_FIELDS = {"Title"}
    council_file = driver.find_element(By.CLASS_NAME, "cfheader").text.replace(
        "Council File: ", ""
    )

    main_content = driver.find_element(By.ID, "CFI_MainContent")
    xbox_content = main_content.find_element(By.ID, "xboxholder")
    result = {"Council File": council_file}
    data = []
    for title, value, row_number in generate_section_data(driver, xbox_content):
        if not title:
            continue

        if title in MANDATORY_FIELDS:
            result[title] = value
        else:
            section_data = {"title": title, "value": value, "row_number": row_number}
            data.append(section_data)
    result["Data"] = data

    return result


def get_online_documents(driver: webdriver.WebKitGTK) -> dict:
    content = driver.find_element(By.ID, "CFI_OnlineDocsContent")
    table = content.find_elements(By.ID, "inscrolltbl")[1]
    table_data = table.find_elements(By.TAG_NAME, "tr")
    results = []
    for row in table_data:
        tabs = row.find_elements(By.TAG_NAME, "td")
        title, date = tabs[0].text, tabs[1].text
        href = get_element_if_exists(tabs[0], By.TAG_NAME, "a").get_attribute("href")
        result = {"title": title, "date": date, "href": href}
        results.append(result)
    return results


def get_vote_information(driver: webdriver.WebKitGTK) -> dict:
    content = driver.find_element(By.ID, "CFI_VotesContent")
    tables = content.find_elements(By.ID, "inscrolltbl")

    if len(tables) == 0:
        return {}

    aggregated_data = tables[0].find_elements(By.TAG_NAME, "tr")
    member_data = tables[1].find_elements(By.TAG_NAME, "tr")[1:]

    results = {}
    for row in aggregated_data:
        tabs = row.find_elements(By.TAG_NAME, "td")
        title, value = tabs[0].text, tabs[1].text
        results[title] = value
    member_votes = []
    for row in member_data:
        tabs = row.find_elements(By.TAG_NAME, "td")
        name, cd, vote = tabs[0].text, tabs[1].text, tabs[2].text
        member_vote = {"name": name, "cd": cd, "vote": vote}
        member_votes.append(member_vote)
    results["Member Information"] = member_votes
    return results


def get_data_from_data_page(driver: webdriver.WebKitGTK) -> dict:
    primary_data = get_primary_data(driver)
    online_documents = get_online_documents(driver)
    vote_information = get_vote_information(driver)
    return {
        **primary_data,
        "Online Documents": online_documents,
        "Vote Information": vote_information,
    }


def get_data_from_search_record(
    driver: webdriver.WebKitGTK, element: WebElement
) -> dict:
    """Get the data from a search record. by open a new tab

    Args:
        driver (webdriver.WebKitGTK): The Selenium webdriver.
        element (WebElement): The search record.

    Returns:
        dict: The data inside the search record.
    """
    href = element.find_element(By.TAG_NAME, "a").get_attribute("href")
    driver.execute_script(f"window.open('{href}');")
    driver.switch_to.window(driver.window_handles[1])
    data = get_data_from_data_page(driver)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return data


def main(num_of_result: int = 0) -> None:
    """
    The main function.

    Args:
        num_of_result (int, optional): The number of result to get.
            Less then 0 if you want to get all results. Defaults to 0.
    """
    num_of_result -= 1
    driver = init_chrome_driver()
    search_word(driver, "test")
    results = get_search_results(driver)
    data = []
    for i, result in enumerate(results):
        page_data = get_data_from_search_record(driver, result)
        data.append(page_data)
        if i == num_of_result:
            break
    json_object = json.dumps(data, indent=2)
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)
    driver.close()


if __name__ == "__main__":
    main(5)
