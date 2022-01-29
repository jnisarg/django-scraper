import time
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from .models import NewsItem


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("- incognito")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    # options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(
        executable_path="./chromedriver", options=options)

    return driver


def load_infinite_scroll(driver, number_of_pagedowns=50):
    elem = driver.find_element(By.TAG_NAME, "body")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(3.0)
    while number_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        number_of_pagedowns -= 1
    return None


def scrape_dev_to(url):
    driver = get_driver()
    driver.get(url)
    timeout = 10
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".crayons-story"),)
        )
    except TimeoutException:
        print("Timed out waiting for page to load")
        driver.quit()

    try:
        load_infinite_scroll(driver)
        articles = driver.find_elements(By.CSS_SELECTOR, ".crayons-story")
        for article in articles:
            result = article.find_element(By.CSS_SELECTOR,
                                          ".crayons-story__title > a")
            article_title = result.text
            article_link = result.get_attribute("href")

            time = article.find_element(By.TAG_NAME, "time").text

            today = datetime.date.today()
            yesterday = today - datetime.timedelta(days=1)

            article_date = datetime.datetime.strptime(
                " ".join(time.split()[:2]), "%b %d")
            article_date = article_date.replace(year=today.year).date()

            if yesterday <= article_date:
                NewsItem.objects.get_or_create(
                    source="dev.to",
                    link=article_link,
                    title=article_title,
                    publish_date=article_date,
                )
    except Exception as error:
        print(error)  # TODO: send mail to admin
