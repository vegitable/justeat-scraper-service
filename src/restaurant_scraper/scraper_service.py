import urllib.request, requests, csv, certifi, logging, time
from http.cookiejar import CookieJar
from random import randint
from bs4 import BeautifulSoup

class JustEatScraper:

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
            time.sleep(8)
            self.scrape_restaurant(f"{self.base_url + slug}/menu")

    def pull_menu_slugs_from_csv(self):
        with open("je_menu_urls.csv", "r") as csvfile:
            slug_reader = csv.reader(csvfile)
            for row in slug_reader:
                self.menu_slugs.append(row[0])

    def scrape_restaurant(self, url):
        print(url)
        self.payload["dishes"] = []
        req = urllib.request.Request(url)
        cj = CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

        header_data = f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{randint(10, 99)}.{randint(1, 9)}.{randint(1000, 9999)}.{randint(10, 99)} Safari/537.36"

        req.add_header("User-Agent", header_data)

        try:
            page = opener.open(req)
        except urllib.error.HTTPError as error:
            print(error.code)
            print(error.read())
            return

        soup = BeautifulSoup(page, "html.parser")
        self._scrape_restaurant_data(soup)
        product_boxes = soup.find_all("div", attrs={"class": "product"})
        if not product_boxes:
            print(soup)
        for product in product_boxes:
            self._scrape_product(product)
        req = requests.post("http://localhost:3000/api/restaurants/create", json=self.payload)
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
        if not name_box:
            print('no data found')
            return
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
