from selenium import webdriver
import csv


class MenuSlugGenerator:

    browser = webdriver.Firefox()
    base_url = 'https://www.just-eat.co.uk/area/'
    area_slugs = []
    menu_slugs = []

    def pull_area_slugs_from_csv(self):
        with open('just_eat_slugs.csv', 'r') as csvfile:
            slug_reader = csv.reader(csvfile)
            for row in slug_reader:
                self.area_slugs.append(row[0])

    def pull_all_menu_slugs(self):
        for slug in self.area_slugs:
            current_url = self.base_url + slug
            self.browser.implicitly_wait(2)
            self._pull_menu_slugs_for_current_page(current_url)
        self.browser.close()

    def _pull_menu_slugs_for_current_page(self, url):
        self.browser.get(url)
        num_restaurants = len(self.browser.find_elements_by_class_name('c-restaurant__logo'))
        for i in range(0, num_restaurants):
            self.browser.find_elements_by_class_name('c-restaurant__logo')[i].click()
            self._write_slug_to_csv(self.browser.current_url.split('/')[-2])
            print(f"{i + 1} out of {num_restaurants} on url({url} written to csv file.")
            self.browser.get(url)
    
    def _write_slug_to_csv(self, content):
        with open('je_menu_urls.csv', 'a') as csvfile:
            slug_writer = csv.writer(csvfile)
            slug_writer.writerow([content])
    

gen = MenuSlugGenerator()
gen.pull_area_slugs_from_csv()
gen.pull_all_menu_slugs()