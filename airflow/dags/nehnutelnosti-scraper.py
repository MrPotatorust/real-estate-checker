from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from bs4 import BeautifulSoup, NavigableString
import requests
from lxml import etree
import re
import pandas as pd
import numpy as np
import time
import json
import logging




default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

my_dag = DAG(
    dag_id = "Nehnutelnosti_scraper",
    default_args=default_args,
    description="Scrapes and converts to dataframe",
    schedule_interval=timedelta(days=1),
)


logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def scraping():


    slovak_cities=['bratislava', 'kosice', 'presov', 'zilina', 'nitra', 'banska-bystrica', 'trnava', 'trencin', 'martin', 'poprad', 'prievidza', 'zvolen', 'povazska-bystrica', 'nove-zamky', 'michalovce', 'spisska-nova-ves', 'komarno', 'levice', 'liptovsky-mikulas', 'humenne', 'bardejov', 'piestany', 'ruzomberok', 'lucenec', 'pezinok', 'topolcany', 'dunajska-streda', 'trebisov', 'cadca', 'dubnica-nad-vahom', 'rimavska-sobota', 'partizanske', 'vranov-nad-toplou', 'sala', 'senec', 'brezno', 'hlohovec', 'nove-mesto-nad-vahom', 'senica', 'malacky', 'snina', 'dolny-kubin', 'roznava', 'puchov', 'ziar-nad-hronom', 'banovce-nad-bebravou', 'stara-lubovna', 'handlova', 'skalica', 'galanta', 'kezmarok', 'sered', 'kysucke-nove-mesto', 'levoca', 'samorin', 'detva', 'stupava', 'sabinov', 'zlate-moravce', 'bytca', 'revuca', 'holic', 'myjava', 'velky-krtis', 'kolarovo', 'nova-dubnica', 'moldava-nad-bodvou', 'stropkov', 'svidnik', 'filakovo', 'sturovo', 'banska-stiavnica', 'surany', 'modra', 'tvrdosin', 'krompachy', 'secovce', 'velke-kapusany', 'stara-tura', 'vrable', 'velky-meder', 'svit', 'krupina', 'namestovo', 'vrutky', 'kralovsky-chlmec', 'hurbanovo', 'hrinova', 'liptovsky-hradok', 'sahy', 'trstena', 'turzovka', 'velky-saris', 'nova-bana', 'tornala', 'spisska-bela', 'zeliezovce', 'krasno-nad-kysucou', 'hnusta', 'lipany', 'nemsova', 'turcianske-teplice', 'svaty-jur', 'sobrance', 'gelnica', 'rajec', 'medzilaborce', 'zarnovica', 'vrbove', 'ilava', 'sladkovicovo', 'gabcikovo', 'poltar', 'dobsina', 'bojnice', 'nesvady', 'sastin-straze', 'gbely', 'sliac', 'kremnica', 'brezova-pod-bradlom', 'strazske', 'novaky', 'medzev', 'turany', 'giraltovce', 'trencianske-teplice', 'leopoldov', 'vysoke-tatry', 'spisske-podhradie', 'hanusovce-nad-toplou', 'tisovec', 'tlmace', 'cierna-nad-tisou', 'spisske-vlachy', 'jelsava', 'podolinec', 'rajecke-teplice', 'spisska-stara-ves', 'modry-kamen', 'dudince']



    def getHtmlDoc(url):

        response = requests.get(url)


        return response.text

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


        
    counter = 1


    logger.info("Started scraping nehnutelnosti.sk")

    sale_rent_text = ""
    house_apartment_text = ""

    # 1 = houses for sale
    # 2 = apartments for sale
    # 3 = houses for rent
    # 4 = apartments for rent

    main_start = time.time()

    for sale_rent_bool in [1, 2, 3, 4]:
        if sale_rent_bool == 1:
            house_apartment_text = "domy"
            sale_rent_text = "predaj"
        elif sale_rent_bool == 2:
            house_apartment_text = "byty"
            sale_rent_text = "predaj"
        elif sale_rent_bool == 3:
            house_apartment_text = "domy"
            sale_rent_text = "prenajom"
        else:
            house_apartment_text = "byty"
            sale_rent_text = "prenajom"
        

        for cities in enumerate(slovak_cities):

                

            url = f"https://www.nehnutelnosti.sk/{cities[1]}/{house_apartment_text}/{sale_rent_text}/?p[page]={counter}"
            logger.info(url)
            logger.info(f"Started scraping {cities[0]+1}, {cities[1]}")

            html_doc = getHtmlDoc(url)
            soup = BeautifulSoup(html_doc, 'lxml')

            start = time.time()

            page_counter=0

            while not soup.find(string="Nenašli sa žiadne výsledky"):

                page_counter +=1

                logger.info(f"Started scraping next page {page_counter}")
                
                for element in soup.find_all('div', {"class": "advertisement-item"}):
                    sq_m = None

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


                    # checks if the price is actually a number
                    if re.match(r'\d+', stripped_prices[0]):
                        index = stripped_prices.find("€")
                        price = stripped_prices[:index]
                        if price == '':
                            price = None
                        else:
                            price = float(stripped_prices[:index].replace(",", "."))
                    else:
                        price = None


                    dict1["title"].append(title)
                    dict1["location_description"].append(location_description)
                    dict1["sq_m"].append(sq_m)
                    dict1["price"].append(price)
                    dict1["link"].append(link)
                    dict1["img"].append(img)
                    dict1["location"].append(cities[0]+1)
                    if sale_rent_bool == 1 or sale_rent_bool == 2:
                        dict1['buy'].append(1)
                    else:
                        dict1['buy'].append(0)
                    if sale_rent_bool == 1 or sale_rent_bool == 3:
                        dict1['house'].append(1)
                    else:
                        dict1['house'].append(0)

                    # print(title)
                    # print(location_description)
                    # print(sq_m)
                    # print(price)
                    # print(link)
                    # print(img)
                    # print(description)


                counter += 1

                changing_url = f"https://www.nehnutelnosti.sk/{cities[1]}/{house_apartment_text}/{sale_rent_text}/?p[page]={counter}"

                html_doc = getHtmlDoc(changing_url)
                soup = BeautifulSoup(html_doc, 'lxml')
                logger.info(changing_url)
            
            end=time.time()
            logger.info(f"Scraping city {cities[1]} took {end-start} seconds")

            counter = 1

    main_end = time.time()

    logger.info(main_end-main_start)

    return dict1


def converting_to_df(ti):
    scraping_dict = ti.xcom_pull(task_ids="scraping")

    logger.info("Converting to dataframe")

    df = pd.DataFrame.from_dict(scraping_dict)

    print(df)

    logger.info("Finished converting to dataframe")


scraping = PythonOperator(
    task_id="scraping",
    python_callable=scraping,
    dag=my_dag,
)

converting_to_df = PythonOperator(
    task_id="converting_to_df",
    python_callable=converting_to_df,
    dag=my_dag,
)

scraping >> converting_to_df