import csv
from constants import LONDON_POSTCODES, BROWSER, POSTCODE_CSV


slugs = []


def pull_all_slugs():
    for code in LONDON_POSTCODES:
        BROWSER.implicitly_wait(3)
        BROWSER.get('https://www.just-eat.co.uk/')
        BROWSER.find_element_by_id('postcode').clear()
        BROWSER.find_element_by_id('postcode').send_keys(code + '0AA')
        BROWSER.find_element_by_class_name('o-btn--primary').click()
        slugs.append(_url_to_slug(BROWSER))
    BROWSER.close()


def write_slugs_to_csv():
    with open(POSTCODE_CSV, 'w+') as csvfile:
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
