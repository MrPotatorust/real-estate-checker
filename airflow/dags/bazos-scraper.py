from bs4 import BeautifulSoup, NavigableString
import requests
from lxml import etree
import re
import pandas as pd
import numpy as np
import time
import json
import logging




logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def getHtmlDoc(url):

    response = requests.get(url)


    return response.text



html_doc = getHtmlDoc("https://reality.bazos.sk/")
soup = BeautifulSoup(html_doc, "lxml")
counter = 0


while not soup.find(string="Stránka nenájdená"):



    counter += 20
    html_doc = getHtmlDoc(f"https://reality.bazos.sk/{counter}/")
    soup = BeautifulSoup(html_doc, "lxml")