from selenium import webdriver
import csv


class SlugGenerator:

    e_london_postcodes = [f"E{n}" for n in range(1, 21)]
    n_london_postcodes = [f"N{n}" for n in range(1, 23)]
    w_london_postcodes = [f"SE{n}" for n in range(1, 15)]
    nw_london_postcodes = [f"NW{n}" for n in range(1, 12)]
    se_london_postcodes = [f"SE{n}" for n in range(1, 29)]
    sw_london_postcodes = [f"SW{n}" for n in range(1, 21)]
    total_london_postcodes = (
        e_london_postcodes +
        n_london_postcodes +
        w_london_postcodes +
        nw_london_postcodes +
        se_london_postcodes +
        sw_london_postcodes
    )
    browser = webdriver.Firefox()
    slugs = []

    def pull_all_slugs(self):
        for code in self.total_london_postcodes:
            self.browser.implicitly_wait(3)
            self.browser.get('https://www.just-eat.co.uk/')
            self.browser.find_element_by_id('postcode').clear()
            self.browser.find_element_by_id('postcode').send_keys(code + '0AA')
            self.browser.find_element_by_class_name('o-btn--primary').click()
            self.slugs.append(self._url_to_slug(self.browser))
        self.browser.close()

    def write_slugs_to_csv(self):
        with open('just_eat_slugs.csv', 'w+') as csvfile:
            slug_writer = csv.writer(csvfile)
            for slug in self.slugs:
                if '-' in slug:
                    slug_writer.writerow([slug])
    
    def _url_to_slug(self, browser):
        return browser.current_url.split('/')[-1]

gen = SlugGenerator()
gen.pull_all_slugs()
gen.write_slugs_to_csv()