from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base_hook import BaseHook

from bs4 import BeautifulSoup, NavigableString
import requests
from lxml import etree
import re
from sqlalchemy import create_engine, text, Column, String, Integer, CHAR, Boolean, Float, DateTime, null
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import numpy as np
import time
import json
import logging

from custom_functions import getHtmlDoc


Base = declarative_base()

class Advertisement(Base):
    __tablename__ = "property_listings_bazos"

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
    dag_id = "Bazos_scraper",
    default_args=default_args,
    description="Scrapes and converts to dataframe",
    #schedule_interval=timedelta(days=1),
    schedule=None,
)


logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def scraping(Advertisement = Advertisement, session = session):

    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    logger = logging.getLogger(__name__)


    cur_time = datetime.utcnow()

    # dict1 = {
    #         "title": [],
    #         "price": [],
    #         "sq_m": [],
    #         "img": [],
    #         "link": [],
    #         "location": [],
    #         "postal_code":[],
    #         'rentable': [],
    #         'property_type': [],
    #         'site':[]
    #     }




    start = time.time()

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
                price = null()

            
            element_loc = element.find(class_="inzeratylok").text.replace("\r", "").replace("\n", "")
            first_num = re.search(r'\d', element_loc)
            if element_loc[:first_num.start()]:
                postal_code = element_loc[first_num.start():]
                city = element_loc[:first_num.start()]

            
            
            # dict1['title'].append(title)
            # dict1["location"].append(city)
            # dict1["sq_m"].append(None)
            # dict1['price'].append(price)
            # dict1['link'].append(f"https://reality.bazos.sk{link}")
            # dict1['img'].append(img)
            # dict1['postal_code'].append(postal_code)
            # dict1["rentable"].append(None)
            # dict1["property_type"].append(None)
            # dict1["site"].append(2)

            advertisement = Advertisement(title=title, price=price, sq_m=null(), img=img, link=link, location=city, postal_code=postal_code, rentable=null(), property_type=null(), site=2, datetime=cur_time)

            session.add(advertisement)

            # print(price)
            # print(description.replace("\r", "").replace("\n", ""))
            # print(postal_code)
            # print(img)
            # print(city)
            # print(title)
            # print(f"https://reality.bazos.sk{link}")
            # print(2)
            # print("--------------------------")

        counter += 20
        html_doc = getHtmlDoc(f"https://reality.bazos.sk/{counter}/")
        soup = BeautifulSoup(html_doc, "lxml")
        logger.info(f"scraped page {counter}")


    end = time.time()

    logger.info(f"Took: {end-start} seconds")

    session.commit()



scraping = PythonOperator(
    task_id="scraping",
    python_callable=scraping,
    dag=my_dag,
)


scraping 