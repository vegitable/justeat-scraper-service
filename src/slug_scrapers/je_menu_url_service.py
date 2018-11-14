from selenium import webdriver
import csv


browser = webdriver.Firefox()
base_url = 'https://www.just-eat.co.uk/area/'
area_slugs = []
menu_slugs = []


def pull_area_slugs_from_csv():
    with open('/Users/muzzialdean/Muzzi/web_scraper/csv/je_postcode_slugs.csv', 'r') as csvfile:
        slug_reader = csv.reader(csvfile)
        for row in slug_reader:
            area_slugs.append(row[0])


def pull_all_menu_slugs():
    for slug in area_slugs:
        current_url = base_url + slug
        browser.implicitly_wait(2)
        _pull_menu_slugs_for_current_page(current_url)
    browser.close()


def _pull_menu_slugs_for_current_page(url):
    browser.get(url)
    num_restaurants = len(browser.find_elements_by_class_name('c-restaurant__logo'))
    for i in range(0, num_restaurants):
        browser.find_elements_by_class_name('c-restaurant__logo')[i].click()
        _write_slug_to_csv(browser.current_url.split('/')[-2])
        print(f"{i + 1} out of {num_restaurants} on url({url}) written to csv file.")
        browser.get(url)


def _write_slug_to_csv(content):
    with open('/Users/muzzialdean/Muzzi/web_scraper/csv/je_menu_slugs.csv', 'a') as csvfile:
        slug_writer = csv.writer(csvfile)
        slug_writer.writerow([content])


def main():
    pull_area_slugs_from_csv()
    pull_all_menu_slugs()


if __name__ == '__main__':
    main()
