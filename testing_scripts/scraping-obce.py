from lxml import etree
from bs4 import BeautifulSoup, NavigableString
import re
import requests
import json

def getHtmlDoc(url):

    response = requests.get(url)

    return response.text

htmldoc = getHtmlDoc("https://sk.wikipedia.org/wiki/Zoznam_slovensk%C3%BDch_obc%C3%AD_a_vojensk%C3%BDch_obvodov")

soup = BeautifulSoup(htmldoc, "lxml")

table = soup.find(class_="wikitable")

all_cities = []

for row in table.find("tbody"):
    if type(row) is NavigableString:
        continue
    cur = (row.find_all("td")[0:1])

    if cur:
        all_cities.append(cur[0].text.strip())



with open("./testing_scripts/sample.json", "w", encoding="utf8") as file:
    file.write(json.dumps(all_cities, ensure_ascii=False, indent=4))