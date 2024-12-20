import json
import re
import numpy as np
import pandas as pd
import requests

from sqlalchemy import create_engine, text, Column, String, Integer, CHAR, Boolean, Float, DateTime, null, Text
from sqlalchemy.ext.declarative import declarative_base

cur = "040 01"
text = "STARÉ MESTO - KOMENSKÉHO SUPER 3 IZBOVÝ TEHLOVÝ BYT 120 M2."


replace = {
    ' I - ':'-',
    ' II - ':'-',
    ' III - ':'-',
    ' IV - ':'-',
    ' V - ':'-',
    ' VI - ':'-',
    ' VII - ':'-',
    ' VIII - ':'-',
    ' IX - ':'-',
    ' X - ':'-'
}

def getHtmlDoc(url):
    response = requests.get(url)


    return response.text


def convert_to_postal_code(location):

    if location.count(",") > 1:
        comma_locations=[]
        for index, char in enumerate(location):
            if char == ',':
                comma_locations.append(index)
        lookup_location = location[comma_locations[-2]+2:comma_locations[-1]]
    else:
        lookup_location = location[:location.index(",")]

    if '-' in lookup_location:
        for word, initial in replace.items():
            lookup_location = lookup_location.replace(word, initial)

    
    with open('./dags/SK.txt', 'r', encoding='utf8' ) as file:
        lines = file.readlines()
        for line in lines:
            stripped_line = line[10:]
            line_city = stripped_line[:stripped_line.find('\t')]
            if line_city == lookup_location:
                return line[3:9]

        


#print(convert_to_postal_code("Veľká Lomnica, Kamenná ul., Vysoké Tatry, okres Poprad"))

# slovak_to_english = {
#     'á': 'a', 'ä': 'a', 'č': 'c', 'ď': 'd', 'é': 'e', 'í': 'i', 'ĺ': 'l', 'ľ': 'l',
#     'ň': 'n', 'ó': 'o', 'ô': 'o', 'ŕ': 'r', 'š': 's', 'ť': 't', 'ú': 'u', 'ý': 'y', 'ž': 'z',
#     'Á': 'A', 'Ä': 'A', 'Č': 'C', 'Ď': 'D', 'É': 'E', 'Í': 'I', 'Ĺ': 'L', 'Ľ': 'L',
#     'Ň': 'N', 'Ó': 'O', 'Ô': 'O', 'Ŕ': 'R', 'Š': 'S', 'Ť': 'T', 'Ú': 'U', 'Ý': 'Y', 'Ž': 'Z', ' ': '-'
# }


# def convert_slovak_to_english(text):
#     return ''.join(slovak_to_english.get(char, char) for char in text)


# def getPreciseLocation(postal_code, text, slovak_to_english=slovak_to_english):


#     lines_with_code = []

#     with open("./airflow/dags/SK.txt", "r", encoding="utf8") as file:
#         lines = file.readlines()
#         for line in lines:
#             if cur in line:
#                 lines_with_code.append(line)

#     for line in lines_with_code:
#         stripped_line = line[10:]
#         transformed_line = stripped_line[:re.search(r'\t', stripped_line).start()]
#         saved_line = transformed_line
#         transformed_line = transformed_line.lower().split("-")
#         if len(transformed_line) > 1:
#             transformed_line = transformed_line[1]
#         else:
#             transformed_line = transformed_line[0]

        
#         if convert_slovak_to_english(transformed_line) in convert_slovak_to_english(text.lower()):
#             return saved_line



# # print(getPreciseLocation(cur, text))

# def num_to_postal_code():
#     unique_codes = []

#     with open("./airflow/dags/SK.txt", "r", encoding="utf8") as file:
#         lines = file.readlines()
#         for line in lines:
#             cur = line[3:9]
#             if cur not in unique_codes:
#                 unique_codes.append(cur)
        
#         df = pd.DataFrame(unique_codes)
#         df.to_json('./airflow/dags/num_to_postal_code.json', indent=4)
#         #dd = pd.read_json('./airflow/dags/postal_code_to_num.json')
#         # print(dd.head())


# def postal_code_to_num():
#     unique_codes = {}
#     counter = 0

#     with open("./airflow/dags/SK.txt", "r", encoding="utf8") as file:
#         lines = file.readlines()
#         for line in lines:
#             cur = line[3:9]
#             if cur not in unique_codes:
#                 unique_codes[cur] = str(counter)
#                 counter += 1

#     print(unique_codes)       
#     with open("./airflow/dags/postal_code_to_num.json", 'w') as file:
#         json.dump(unique_codes, file)


# # FILE CREATE FUNCTIONS EXECUTE
# # postal_code_to_num()
# # num_to_postal_code()