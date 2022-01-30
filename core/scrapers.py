import time
import datetime
import requests

from bs4 import BeautifulSoup

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

            article_author = article.find_element(
                By.CSS_SELECTOR, ".profile-preview-card > button").text

            time = article.find_element(By.TAG_NAME, "time").text

            today = datetime.date.today()
            yesterday = today - datetime.timedelta(days=1)

            article_date = datetime.datetime.strptime(
                " ".join(time.split()[:2]), "%b %d")
            article_date = article_date.replace(year=today.year).date()

            if yesterday <= article_date:
                NewsItem.objects.get_or_create(
                    source="dev.to",
                    author=article_author,
                    link=article_link,
                    title=article_title,
                    publish_date=article_date,
                )
    except Exception as error:
        print(error)  # TODO: send mail to admin


def scrape_hn(crawl_delay=30):
    page = 1
    scrape_count = 0
    while True:
        try:
            url = f"https://news.ycombinator.com/news?p={page}"

            res = requests.get(url)

            if res.status_code != 200:
                break

            soup = BeautifulSoup(res.text, "html.parser")

            links = soup.select(".athing")
            subtexts = soup.select(".subtext")

            if not links:
                break

            for idx, item in enumerate(links):
                title = item.select(".titlelink")
                author = subtexts[idx].select(".hnuser")
                dt = subtexts[idx].select(".age")
                source = item.select(".sitestr")

                if all([title, author, dt]):
                    article_title = title[0].text
                    article_link = title[0].get("href")
                    article_author = author[0].text
                    article_publish_date = datetime.datetime.strptime(
                        dt[0].get("title"), "%Y-%m-%dT%H:%M:%S").date()
                    article_source = source[0].text if source else "news.ycombinator.com"
                else:
                    continue

                _, created = NewsItem.objects.get_or_create(
                    source=article_source,
                    author=article_author,
                    link=article_link,
                    title=article_title,
                    publish_date=article_publish_date,
                )

                if created:
                    scrape_count += 1

            page += 1
            # time.sleep(crawl_delay)  # crawl_delay

        except Exception as error:
            print(error)  # TODO: send mail to admin
            break

    print(f"{scrape_count} new articles scraped.")
