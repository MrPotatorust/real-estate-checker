import requests
from bs4 import BeautifulSoup
from lxml import etree

def getHtmlDoc(url):
    response = requests.get(url)


    return response.text




def get_city(postal_code):
    response = getHtmlDoc(f"https://www.geonames.org/postalcode-search.html?q={postal_code.replace(" ", "+")}&country=SK")
    soup = BeautifulSoup(response, "lxml")
    result = soup.find_all("td")[9:10][0]

    return result

print(get_city("049 16"))