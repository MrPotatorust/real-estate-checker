import requests
from bs4 import BeautifulSoup, NavigableString
from lxml import etree
import re


slovak_to_english = {
    'á': 'a', 'ä': 'a', 'č': 'c', 'ď': 'd', 'é': 'e', 'í': 'i', 'ĺ': 'l', 'ľ': 'l',
    'ň': 'n', 'ó': 'o', 'ô': 'o', 'ŕ': 'r', 'š': 's', 'ť': 't', 'ú': 'u', 'ý': 'y', 'ž': 'z',
    'Á': 'A', 'Ä': 'A', 'Č': 'C', 'Ď': 'D', 'É': 'E', 'Í': 'I', 'Ĺ': 'L', 'Ľ': 'L',
    'Ň': 'N', 'Ó': 'O', 'Ô': 'O', 'Ŕ': 'R', 'Š': 'S', 'Ť': 'T', 'Ú': 'U', 'Ý': 'Y', 'Ž': 'Z', ' ': '-'
}

smthing = [
    'Bánovce nad Bebravou',
    'Banská Bystrica',
    'Banská Štiavnica',
    'Bardejov',
    'Bratislava',
    'Brezno',
    'Bytča',
    'Čadca',
    'Česká republika',
    'Detva',
    'Dolný Kubín',
    'Dunajská Streda',
    'Galanta',
    'Gelnica',
    'Hlohovec',
    'Humenné',
    'Hurbanovo',
    'Ilava',
    'Kežmarok',
    'Komárno',
    'Košice',
    'Košice-okolie',
    'Krupina',
    'Kysucké Nové Mesto',
    'Levice',
    'Levoča',
    'Liptovský Mikuláš',
    'Lučenec',
    'Malacky',
    'Martin',
    'Medzilaborce',
    'Michalovce',
    'Myjava',
    'Námestovo',
    'Nitra',
    'Nové Mesto n.Váhom',
    'Nové Zámky',
    'Partizánske',
    'Pezinok',
    'Piešťany',
    'Poltár',
    'Poprad',
    'Považská Bystrica',
    'Prešov',
    'Prievidza',
    'Púchov',
    'Revúca',
    'Rimavská Sobota',
    'Rožňava',
    'Ružomberok',
    'Sabinov',
    'Senec',
    'Senica',
    'Skalica',
    'Snina',
    'Sobrance',
    'Spišská Nová Ves',
    'Stará Ľubovňa',
    'Stropkov',
    'Štúrovo',
    'Svidník',
    'Šaľa',
    'Topoľčany',
    'Trebišov',
    'Trenčín',
    'Trnava',
    'Turčianske Teplice',
    'Tvrdošín',
    'Veľký Krtíš',
    'Vranov nad Topľou',
    'Zahraničie',
    'Zlaté Moravce',
    'Zvolen',
    'Žarnovica',
    'Žiar nad Hronom',
    'Žilina'
]

def convert_slovak_to_english(text):
    return ''.join(slovak_to_english.get(char, char) for char in text)


def getHtmlDoc(url):

    response = requests.get(url)

    return response.text

htmldoc = getHtmlDoc("https://sk.wikipedia.org/wiki/Zoznam_miest_na_Slovensku")

soup = BeautifulSoup(htmldoc, "lxml")

table = soup.find(class_="mw-datatable")

myarr = []

for row in table.find("tbody"):
    if type(row) is NavigableString:
        continue
    cur = row.find_all("td")[2:3]

    if cur:
        myarr.append(convert_slovak_to_english(cur[0].text.strip()).lower())
    

print(sorted(myarr))
print(len(myarr))
print(len(smthing))
# import logging
# import re
# import requests
# from bs4 import BeautifulSoup, NavigableString
# from lxml import etree
# import time
# import json


# logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
# logger = logging.getLogger(__name__)



# def getHtmlDoc(url):

#     response = requests.get(url)


#     return response.text


# soup = BeautifulSoup(getHtmlDoc("https://www.nehnutelnosti.sk/bratislava/byty/prenajom/?p[page]=3"), "lxml")

# for element in soup.find_all('div', {"class": "advertisement-item"}):

#     img = element.find_all(class_="position-relative")[1:2][0].find("data-img").get("data-src")

#     description = element.find(class_="truncate-text").text.strip().replace("\n", "").replace("\r", "")

#     title_el = element.find(class_= "advertisement-item--content__title d-block text-truncate", href=True)
#     link = title_el.get('href')
#     title = title_el.text


#     stripped_prices = element.find(class_="advertisement-item--content__price").text.replace(" ", "").strip()

#     sq_m_el = element.find_all(class_="advertisement-item--content__info")

#     for i in sq_m_el:
#         i = i.text.strip()
#         sq_m_index = i.find("•")

#         if sq_m_index != -1:
#             sq_m = float(i[sq_m_index+2:-3].replace(",", "."))
#         else:
#             location_description = i


#     # checks if the price is actually a number
#     if re.match(r'\d+', stripped_prices[0]):
#         index = stripped_prices.find("€")
#         price = stripped_prices[:index]
#         if price == '':
#             price = None
#         else:
#             price = float(stripped_prices[:index].replace(",", "."))
#     else:
#         price = None


#     print(title)
#     print(location_description)
#     print(sq_m)
#     print(price)
#     print(link)
#     print(img)
#     print(description)
