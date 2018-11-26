from selenium.common.exceptions import NoSuchElementException
import csv
from constants import BROWSER, POSTCODE_CSV, MENU_CSV, JUSTEAT_URL


area_slugs = []
menu_slugs = []


def pull_area_slugs_from_csv():
    with open(POSTCODE_CSV, 'r') as csvfile:
        slug_reader = csv.reader(csvfile)
        for row in slug_reader:
            area_slugs.append(row[0])


def pull_all_menu_slugs():
    for slug in area_slugs:
        current_url = JUSTEAT_URL + 'area/' + slug
        BROWSER.implicitly_wait(2)
        _pull_menu_slugs_for_current_page(current_url)
    BROWSER.close()


def _pull_menu_slugs_for_current_page(url):
    BROWSER.get(url)
    num_restaurants = len(BROWSER.find_elements_by_class_name('c-restaurant__logo'))
    print(num_restaurants)
    for i in range(0, num_restaurants):
        _check_for_popup(BROWSER)
        try:
            BROWSER.find_elements_by_class_name('c-restaurant__logo')[i].click()
            _write_slug_to_csv(BROWSER.current_url.split('/')[-2])
            print(f"{i + 1} out of {num_restaurants} on url({url}) written to csv file.")
            BROWSER.get(url)
        except IndexError:
            pass


def _write_slug_to_csv(content):
    if content != 'area':
        with open(MENU_CSV, 'a') as csvfile:
            slug_writer = csv.writer(csvfile)
            slug_writer.writerow([content])


def _check_for_popup(browser):
    try:
        browser.find_element_by_xpath("//button[@class='o-btn o-btn--primary o-btn--block' and contains(text(), 'All Restaurants')]").click()
    except NoSuchElementException:
        pass



def main():
    pull_area_slugs_from_csv()
    pull_all_menu_slugs()


if __name__ == '__main__':
    main()
