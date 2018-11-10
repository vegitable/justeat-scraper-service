import urllib.request
import requests
from bs4 import BeautifulSoup
import certifi
import csv

class JustEatScraper:

    header_data = ["User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"]
    menu_slugs = []
    base_url = "https://www.just-eat.co.uk/"
    payload = {
        "name": None,
        "postcode": None,
        "coords": [1, 2],
        "rating": None,
        "dishes": [],
    }


    def scrape_all_restaurants(self):
        self.pull_menu_slugs_from_csv()
        for slug in self.menu_slugs:
            self.scrape_restaurant(f"{self.base_url + slug}/menu")

    def pull_menu_slugs_from_csv(self):
        with open("je_menu_urls.csv", "r") as csvfile:
            slug_reader = csv.reader(csvfile)
            for row in slug_reader:
                self.menu_slugs.append(row[0])

    def scrape_restaurant(self, url):
        req = urllib.request.Request(url)
        req.add_header(self.header_data[0], self.header_data[1])
        page = urllib.request.urlopen(req)
        soup = BeautifulSoup(page, "html.parser")
        self._scrape_restaurant_data(soup)
        product_boxes = soup.find_all("div", attrs={"class": "product"})
        for product in product_boxes:
            self._scrape_product(product)
        req = requests.post("https://scraper-data-service.herokuapp.com/api/restaurants/create", json=self.payload)
        print(req.status_code)

    def _scrape_product(self, product):
        name_box = product.find("h4", attrs={"class": "name"})
        description_box = product.find("p", attrs={"class":"description"})
        price_box = product.find("p", attrs={"class":"price"})
        name = name_box.text.strip() if name_box else None
        description = description_box.text if description_box else None
        price = price_box.text if price_box else None
        item = {
            "name": name,
            "description": description,
            "price": price,
        }
        self.payload["dishes"].append(item)

    def _scrape_restaurant_data(self, soup):
        name_box = soup.find("h1", attrs={"class": "name"})
        name = name_box.text.strip()
        address_box = soup.find("p", attrs={"class": "address"})
        address = address_box.text.strip()
        city_box = soup.find(id="city")
        city = city_box.text.strip()
        postcode_box = soup.find(id="postcode")
        postcode = postcode_box.text.strip()

        parent_image_box = soup.find("p", attrs={"class": "rating"})
        image_box = parent_image_box.contents[1]
        rating = image_box.get("alt", "")
        self.payload["name"] = name
        self.payload["postcode"] = postcode
        self.payload["rating"] = 10

scraper = JustEatScraper()
scraper.scrape_all_restaurants()
