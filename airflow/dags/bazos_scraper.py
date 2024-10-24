from bs4 import BeautifulSoup, NavigableString
import requests
from lxml import etree
import re
import pandas as pd
import numpy as np
import time
import json
import logging

from custom_functions import getHtmlDoc





logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

dict1 = {
        "title": [],
        "price": [],
        "sq_m": [],
        "img": [],
        "link": [],
        "location": [],
        "postal_code":[],
        'rentable': [],
        'property_type': [],
        'site':[]
    }



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
        description = element.find(class_="popis").text
        img = element.find("img").get("src")

        price = element.find(class_='inzeratycena').text.replace(' ', '')[:-1]

        if re.match(r'\d+', price[0]):
            price = float(price)
        else:
            price = None

        
        element_loc = element.find(class_="inzeratylok").text.replace("\r", "").replace("\n", "")
        first_num = re.search(r'\d', element_loc)
        if element_loc[:first_num.start()] not in slovak_cities:
            postal_code = element_loc[first_num.start():]
            city = element_loc[:first_num.start()]

        
        
        dict1['title'].append(title)
        dict1["location"].append(city)
        dict1["sq_m"].append(None)
        dict1['price'].append(price)
        dict1['link'].append(f"https://reality.bazos.sk{link}")
        dict1['img'].append(img)
        dict1['postal_code'].append(postal_code)
        dict1["rentable"].append(None)
        dict1["property_type"].append(None)
        dict1["site"].append(2)

        print(price)
        print(description.replace("\r", "").replace("\n", ""))
        print(postal_code)
        print(img)
        print(city)
        print(title)
        print(f"https://reality.bazos.sk{link}")
        print(2)
        print("--------------------------")

    counter += 20
    html_doc = getHtmlDoc(f"https://reality.bazos.sk/{counter}/")
    soup = BeautifulSoup(html_doc, "lxml")
    print(f"scraped page {counter}")

