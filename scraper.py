from urllib.request import urlopen
from bs4 import BeautifulSoup

class JustEatScraper:

url = "https://www.just-eat.co.uk/area/"

page = urlopen(url)

soup = BeautifulSoup(page, 'html.parser')

name_box = soup.find('h4', attrs={'class': 'name'})

name = name_box.text.strip()

print(name) 

description_box = soup.find('p', attrs={'class':'description'})

description = description_box.text

print(description)

price_box = soup.find('p', attrs={'class':'price'})

price = price_box.text

print(price)