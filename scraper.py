import urllib.request
from bs4 import BeautifulSoup
import certifi
import csv

class JustEatScraper:

    header_data = ['User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36']
    restaurants = []
    menu_slugs = []

    def pull_menu_slugs_from_csv(self):
        with open('je_menu_urls.csv', 'r') as csvfile:
            slug_reader = csv.reader(csvfile)
            for row in slug_reader:
                self.menu_slugs.append(row[0])

    def scrape_restaurant(self, url):
        req = urllib.request.Request(url)
        req.add_header(self.header_data[0], self.header_data[1])
        page = urllib.request.urlopen(req)
        soup = BeautifulSoup(page, 'html.parser')
        name_box = soup.find('h4', attrs={'class': 'name'})
        name = name_box.text.strip()
        description_box = soup.find('p', attrs={'class':'description'})
        description = description_box.text
        price_box = soup.find('p', attrs={'class':'price'})
        price = price_box.text
        restaurant = {
            'name': name,
            'description': description,
            'price': price,
        }
        self.restaurants.append(restaurant)

scraper = JustEatScraper()
scraper.pull_menu_slugs_from_csv()
url = "https://www.just-eat.co.uk/restaurants-Mario-Pizza-E14/menu"
scraper.scrape_restaurant(url)
print(scraper.restaurants)
