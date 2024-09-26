from bs4 import BeautifulSoup
import requests
from lxml import etree
import re

def getHtmlDoc(url):

    response = requests.get(url)


    return response.text


html_doc = getHtmlDoc("https://www.nehnutelnosti.sk/zilina/domy/predaj/")

soup = BeautifulSoup(html_doc, 'lxml')

# for i in soup.find_all('div', {"class": "advertisement-item--content__price col-auto pl-0 pl-md-3 pr-0 text-right mt-2 mt-md-0 align-self-end"}):
#     stripped_i = i.text.replace(" ", "").strip()
#     if stripped_i[0] != "C":
#         index = stripped_i.find("€")
#         price = stripped_i[:index]
#         price_per_m = stripped_i[index+1:-4]

#         print(f"price: {price}, price_per_m: {price_per_m}")


for element in soup.find_all('div', {"class": "advertisement-item"}):
    title = element.find(class_= "advertisement-item--content__title d-block text-truncate").text
    imgs = []
    for img in element.find_all("img"):
        imgs.append(img['src'])

    stripped_prices = element.find(class_="advertisement-item--content__price").text.replace(" ", "").strip()

    if stripped_prices[0] != "C":
        index = stripped_prices.find("€")
        price = stripped_prices[:index]
        price_per_m = stripped_prices[index+1:-8].replace(",", ".")
        if price == '':
            price = None
        else:
            price = float(stripped_prices[:index])
        if price_per_m == '':
            price_per_m = None
        else:
            price_per_m = float(stripped_prices[index+1:-8].replace(",", "."))

    print(title)
    print(price, price_per_m)
    print(imgs)