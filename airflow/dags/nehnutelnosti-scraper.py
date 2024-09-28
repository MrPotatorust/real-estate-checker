from bs4 import BeautifulSoup, NavigableString
import requests
from lxml import etree
import re
import pandas as pd
import numpy as np


slovak_cities=['bratislava', 'kosice', 'presov', 'zilina', 'nitra', 'banska-bystrica', 'trnava', 'trencin', 'martin', 'poprad', 'prievidza', 'zvolen', 'povazska-bystrica', 'nove-zamky', 'michalovce', 'spisska-nova-ves', 'komarno', 'levice', 'liptovsky-mikulas', 'humenne', 'bardejov', 'piestany', 'ruzomberok', 'lucenec', 'pezinok', 'topolcany', 'dunajska-streda', 'trebisov', 'cadca', 'dubnica-nad-vahom', 'rimavska-sobota', 'partizanske', 'vranov-nad-toplou', 'sala', 'senec', 'brezno', 'hlohovec', 'nove-mesto-nad-vahom', 'senica', 'malacky', 'snina', 'dolny-kubin', 'roznava', 'puchov', 'ziar-nad-hronom', 'banovce-nad-bebravou', 'stara-lubovna', 'handlova', 'skalica', 'galanta', 'kezmarok', 'sered', 'kysucke-nove-mesto', 'levoca', 'samorin', 'detva', 'stupava', 'sabinov', 'zlate-moravce', 'bytca', 'revuca', 'holic', 'myjava', 'velky-krtis', 'kolarovo', 'nova-dubnica', 'moldava-nad-bodvou', 'stropkov', 'svidnik', 'filakovo', 'sturovo', 'banska-stiavnica', 'surany', 'modra', 'tvrdosin', 'krompachy', 'secovce', 'velke-kapusany', 'stara-tura', 'vrable', 'velky-meder', 'svit', 'krupina', 'namestovo', 'vrutky', 'kralovsky-chlmec', 'hurbanovo', 'hrinova', 'liptovsky-hradok', 'sahy', 'trstena', 'turzovka', 'velky-saris', 'nova-bana', 'tornala', 'spisska-bela', 'zeliezovce', 'krasno-nad-kysucou', 'hnusta', 'lipany', 'nemsova', 'turcianske-teplice', 'svaty-jur', 'sobrance', 'gelnica', 'rajec', 'medzilaborce', 'zarnovica', 'vrbove', 'ilava', 'sladkovicovo', 'gabcikovo', 'poltar', 'dobsina', 'bojnice', 'nesvady', 'sastin-straze', 'gbely', 'sliac', 'kremnica', 'brezova-pod-bradlom', 'strazske', 'novaky', 'medzev', 'turany', 'giraltovce', 'trencianske-teplice', 'leopoldov', 'vysoke-tatry', 'spisske-podhradie', 'hanusovce-nad-toplou', 'tisovec', 'tlmace', 'cierna-nad-tisou', 'spisske-vlachy', 'jelsava', 'podolinec', 'rajecke-teplice', 'spisska-stara-ves', 'modry-kamen', 'dudince']



def getHtmlDoc(url):

    response = requests.get(url)


    return response.text

dict1 = {
    "title": [],
    "price": [],
    "sq_m": [],
    "imgs": [],
    "link": [],
    "location": [],
    "location_description": []
}



html_doc = getHtmlDoc("https://www.nehnutelnosti.sk/banska-bystrica/predaj/?p[page]=1")
    

soup = BeautifulSoup(html_doc, 'html.parser')


# for i in soup.find_all('div', {"class": "advertisement-item--content__price col-auto pl-0 pl-md-3 pr-0 text-right mt-2 mt-md-0 align-self-end"}):
#     stripped_i = i.text.replace(" ", "").strip()
#     if stripped_i[0] != "C":
#         index = stripped_i.find("€")
#         price = stripped_i[:index]
#         price_per_m = stripped_i[index+1:-4]

#         print(f"price: {price}, price_per_m: {price_per_m}")


for element in soup.find_all('div', {"class": "advertisement-item"}):

    img = element.find_all(class_="position-relative")[1:2][0].find("data-img").get("data-src")

    description = element.find(class_="truncate-text").text.strip().replace("\n", "").replace("\r", "")

    title_el = element.find(class_= "advertisement-item--content__title d-block text-truncate", href=True)
    link = title_el.get('href')
    title = title_el.text


    stripped_prices = element.find(class_="advertisement-item--content__price").text.replace(" ", "").strip()

    sq_m_el = element.find_all(class_="advertisement-item--content__info")

    for i in sq_m_el:
        i = i.text.strip()
        sq_m_index = i.find("•")

        if sq_m_index != -1:
            sq_m = float(i[sq_m_index+2:-3].replace(",", "."))
        else:
            location_description = i


    # the "C" is because there can be "Cena dohodou" intead of a number 
    if stripped_prices[0] != "C":
        index = stripped_prices.find("€")
        price = stripped_prices[:index]
        if price == '':
            price = None
        else:
            price = float(stripped_prices[:index])


    print(title)
    print(location_description)
    print(sq_m)
    print(price)
    print(link)
    print(img)
    print(description)