from bs4 import BeautifulSoup, NavigableString
import requests
from lxml import etree
import re
import pandas as pd
import numpy as np
import time
import json
import logging

from postal_code_local import getPreciseLocation




logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)



dict1 = {
    "title": [],
    "price": [],
    "sq_m": [],
    "img": [],
    "link": [],
    "location": [],
    "location_description": [],
    "buy": [],
    "house": []
}

def getHtmlDoc(url):
    response = requests.get(url)


    return response.text


slovak_cities = []


html_doc = getHtmlDoc("https://reality.bazos.sk/")
soup = BeautifulSoup(html_doc, "lxml")
counter = 0


while not soup.find(string="Stránka nenájdená"):
    elements = soup.find_all(class_="inzeraty")

    for element in elements:
        title_el = element.find(class_="nadpis")
        title = title_el.text
        link = title_el.find("a").get("href")

        
        element_loc = element.find(class_="inzeratylok").text.replace("\r", "").replace("\n", "")
        first_num = re.search(r'\d', element_loc)
        if element_loc[:first_num.start()] not in slovak_cities:
            slovak_cities.append(element_loc[:first_num.start()])
            postal_code = element_loc[first_num.start():]
            city = element_loc[:first_num.start()]

        
        description = element.find(class_="popis").text
        img = element.find("img").get("src")
        
        #print(img)
        print(description)
        print(postal_code)
        print(city)
        print(getPreciseLocation(postal_code, f"{description} {title}"))
        print("--------------------------")
        # print(title)
        # print(f"https://reality.bazos.sk{link}")

    break
    counter += 20
    html_doc = getHtmlDoc(f"https://reality.bazos.sk/{counter}/")
    soup = BeautifulSoup(html_doc, "lxml")
    print(f"scraped page {counter}")


