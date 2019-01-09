from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import csv
import psycopg2
import sys

sys.path.append("..")

from constants import POSTCODE_CSV, JUSTEAT_URL

area_slugs = []
menu_slugs = []
BROWSER = webdriver.Firefox()
conn = psycopg2.connect(host="localhost", database="justeat_scraper")
cur = conn.cursor()


def pull_area_slugs_from_csv():
    with open(POSTCODE_CSV, "r") as csvfile:
        slug_reader = csv.reader(csvfile)
        for row in slug_reader:
            area_slugs.append(row[0])


def pull_all_menu_slugs():
    for i, slug in enumerate(area_slugs):
        current_url = JUSTEAT_URL + "area/" + slug
        print(f"Scraping {current_url}. {i+1}/{len(area_slugs)}")
        BROWSER.implicitly_wait(2)
        _pull_menu_slugs_for_current_page(current_url)
    BROWSER.close()


def _pull_menu_slugs_for_current_page(url):
    BROWSER.get(url)
    num_restaurants = len(BROWSER.find_elements_by_class_name("c-listing-item"))
    print(f"{num_restaurants} restaurants on page.")
    for i in range(0, num_restaurants):
        _check_for_popup(BROWSER)
        try:
            BROWSER.find_elements_by_class_name("c-listing-item")[i].click()
            slug = BROWSER.current_url.split("/")[-2]
            _save_to_db(slug)
            print(
                f"'{slug}' written to database: {num_restaurants - (i + 1)} left to scrape on {url}."
            )
            BROWSER.get(url)
        except IndexError:
            pass


def _save_to_db(content):
    cur.execute("select exists(select 1 from menu_slugs where slug=(%s))", (content,))
    row_exists = cur.fetchone()
    if not row_exists[0]:
        cur.execute("INSERT INTO menu_slugs(slug) VALUES (%s);", (content,))
        conn.commit()


def _check_for_popup(browser):
    try:
        browser.find_element_by_xpath(
            "//button[@class='o-btn o-btn--primary o-btn--block' and contains(text(), 'All Restaurants')]"
        ).click()
    except NoSuchElementException:
        pass


def main():
    pull_area_slugs_from_csv()
    pull_all_menu_slugs()


if __name__ == "__main__":
    main()
