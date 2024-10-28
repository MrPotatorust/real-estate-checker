from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base_hook import BaseHook

from bs4 import BeautifulSoup, NavigableString
import requests
from lxml import etree
import re
import pandas as pd
import numpy as np
import time
import json
import logging

from sqlalchemy import create_engine, text, Column, String, Integer, CHAR, Boolean, Float, DateTime, null
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from custom_functions import convert_to_postal_code, getHtmlDoc




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
    # schedule_interval=timedelta(days=1),
    schedule_interval=None
)


logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)



Base = declarative_base()

class Advertisement(Base):
    __tablename__ = "property_listings_nehnutelnosti"

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    title = Column(String)
    price = Column(Float, nullable=True)
    sq_m = Column(Float, nullable=True)
    img = Column(String)
    link = Column(String)
    location = Column(String)
    postal_code = Column(String)
    rentable = Column(Boolean, nullable=True)
    property_type = Column(String, nullable=True)
    site = Column(Integer)
    datetime = Column(DateTime)

    def __init__(self, title, price, sq_m, img, link, location, postal_code, 
                rentable, property_type, site, datetime, id=None):
        self.id = id
        self.title = title
        self.price = price
        self.sq_m = sq_m
        self.img = img
        self.link = link
        self.location = location
        self.postal_code = postal_code
        self.rentable = rentable
        self.property_type = property_type
        self.site = site
        self.datetime = datetime

    def __repr__(self):
        return (f"Advertisement(id={self.id}, title='{self.title}', "
                f"location='{self.location}', sq_m={self.sq_m}, "
                f"price={self.price}, link='{self.link}', img='{self.img}', "
                f"postal_code='{self.postal_code}', rentable={self.rentable}, "
                f"property_type='{self.property_type}', site={self.site}, "
                f"datetime='{self.datetime}')")


conn_vars = BaseHook.get_connection('staging_db')
engine = create_engine(f'postgresql://{conn_vars.login}:{conn_vars.password}@{conn_vars.host}:{conn_vars.port}/{conn_vars.schema}', echo=True)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()



def scraping():


    # slovak_cities=['bratislava', 'kosice', 'presov', 'zilina', 'nitra', 'banska-bystrica', 'trnava', 'trencin', 'martin', 'poprad', 'prievidza', 'zvolen', 'povazska-bystrica', 'nove-zamky', 'michalovce', 'spisska-nova-ves', 'komarno', 'levice', 'liptovsky-mikulas', 'humenne', 'bardejov', 'piestany', 'ruzomberok', 'lucenec', 'pezinok', 'topolcany', 'dunajska-streda', 'trebisov', 'cadca', 'dubnica-nad-vahom', 'rimavska-sobota', 'partizanske', 'vranov-nad-toplou', 'sala', 'senec', 'brezno', 'hlohovec', 'nove-mesto-nad-vahom', 'senica', 'malacky', 'snina', 'dolny-kubin', 'roznava', 'puchov', 'ziar-nad-hronom', 'banovce-nad-bebravou', 'stara-lubovna', 'handlova', 'skalica', 'galanta', 'kezmarok', 'sered', 'kysucke-nove-mesto', 'levoca', 'samorin', 'detva', 'stupava', 'sabinov', 'zlate-moravce', 'bytca', 'revuca', 'holic', 'myjava', 'velky-krtis', 'kolarovo', 'nova-dubnica', 'moldava-nad-bodvou', 'stropkov', 'svidnik', 'filakovo', 'sturovo', 'banska-stiavnica', 'surany', 'modra', 'tvrdosin', 'krompachy', 'secovce', 'velke-kapusany', 'stara-tura', 'vrable', 'velky-meder', 'svit', 'krupina', 'namestovo', 'vrutky', 'kralovsky-chlmec', 'hurbanovo', 'hrinova', 'liptovsky-hradok', 'sahy', 'trstena', 'turzovka', 'velky-saris', 'nova-bana', 'tornala', 'spisska-bela', 'zeliezovce', 'krasno-nad-kysucou', 'hnusta', 'lipany', 'nemsova', 'turcianske-teplice', 'svaty-jur', 'sobrance', 'gelnica', 'rajec', 'medzilaborce', 'zarnovica', 'vrbove', 'ilava', 'sladkovicovo', 'gabcikovo', 'poltar', 'dobsina', 'bojnice', 'nesvady', 'sastin-straze', 'gbely', 'sliac', 'kremnica', 'brezova-pod-bradlom', 'strazske', 'novaky', 'medzev', 'turany', 'giraltovce', 'trencianske-teplice', 'leopoldov', 'vysoke-tatry', 'spisske-podhradie', 'hanusovce-nad-toplou', 'tisovec', 'tlmace', 'cierna-nad-tisou', 'spisske-vlachy', 'jelsava', 'podolinec', 'rajecke-teplice', 'spisska-stara-ves', 'modry-kamen', 'dudince']

    # dict1 = {
    #     "title": [],
    #     "price": [],
    #     "sq_m": [],
    #     "img": [],
    #     "link": [],
    #     "location": [],
    #     "postal_code":[],
    #     'rentable': [],
    #     'property_type': [],
    #     'site':[]
    # }



    logger.info("Started scraping nehnutelnosti.sk")

    main_start = time.time()
    cur_time = datetime.utcnow()

    page_counter = 0
        

    while not page_counter or not soup.find(string="Nenašli sa žiadne výsledky"):
        start = time.time()
        page_counter +=1

        url = f"https://www.nehnutelnosti.sk/vyhladavanie/?p[page]={page_counter}"
        logger.info(url)
        logger.info(f"Started scraping page {page_counter}")

        html_doc = getHtmlDoc(url)
        soup = BeautifulSoup(html_doc, 'lxml')


        
        for element in soup.find_all('div', {"class": "advertisement-item"}):
            sq_m = None

            img = element.find_all(class_="position-relative")[1:2][0].find("data-img").get("data-src")

            description = element.find(class_="truncate-text").text.strip().replace("\n", "").replace("\r", "")

            title_el = element.find(class_= "advertisement-item--content__title d-block text-truncate", href=True)
            link = title_el.get('href')
            title = title_el.text


            stripped_prices = element.find(class_="advertisement-item--content__price").text.replace(" ", "").strip()
            if 'mes.' in stripped_prices:
                rentable = True
            else:
                rentable = False
            sq_m_el = element.find_all(class_="advertisement-item--content__info")

            for i in sq_m_el:
                i = i.text.strip()
                sq_m_index = i.find("•")
                comma_check = i.find(',')

                if sq_m_index != -1:
                    sq_m = float(i[sq_m_index+2:-3].replace(",", "."))
                    property_type = i[:sq_m_index].strip()
                elif comma_check != -1:
                    location = i
                else:
                    property_type = i[:sq_m_index+1].strip()


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


            postal_code = convert_to_postal_code(location)


            # dict1["title"].append(title)
            # dict1["location"].append(location)
            # dict1["sq_m"].append(sq_m)
            # dict1["price"].append(price)
            # dict1["link"].append(link)
            # dict1["img"].append(img)
            # dict1['postal_code'].append(postal_code)
            # dict1['rentable'].append(rentable)
            # dict1['property_type'].append(property_type)
            # dict1['site'].append(1)

            advertisement = Advertisement(title=title, price=price, sq_m=null(), img=img, link=link, location=location, postal_code=postal_code, rentable=null(), property_type=null(), site=1, datetime=cur_time)

            # print(title)
            # print(location)
            # print(sq_m)
            # print(price)
            # print(link)
            # print(img)
            # print(postal_code)
            # print(description)
            # print(rentable)
            # print(property_type)
            # print('---------------------')
            


            session.add(advertisement)
            
        end=time.time()

        logger.info(f"Scraped page took {end-start}")


    main_end = time.time()

    logger.info(main_end-main_start)

    session.commit()




scraping = PythonOperator(
    task_id="scraping",
    python_callable=scraping,
    dag=my_dag,
)


scraping