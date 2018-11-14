from selenium import webdriver
import csv
from constants import LONDON_POSTCODES


browser = webdriver.Firefox()
slugs = []


def pull_all_slugs():
    for code in LONDON_POSTCODES:
        browser.implicitly_wait(3)
        browser.get('https://www.just-eat.co.uk/')
        browser.find_element_by_id('postcode').clear()
        browser.find_element_by_id('postcode').send_keys(code + '0AA')
        browser.find_element_by_class_name('o-btn--primary').click()
        slugs.append(_url_to_slug(browser))
    browser.close()


def write_slugs_to_csv():
    with open('/Users/muzzialdean/Muzzi/web_scraper/csv/je_postcode_slugs.csv', 'w+') as csvfile:
        slug_writer = csv.writer(csvfile)
        for slug in slugs:
            if '-' in slug:
                slug_writer.writerow([slug])


def _url_to_slug(browser):
    return browser.current_url.split('/')[-1]


def main():
    pull_all_slugs()
    write_slugs_to_csv()


if __name__ == '__main__':
    main()
