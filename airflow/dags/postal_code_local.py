import json
import re
import numpy as np
import pandas as pd

cur = "040 01"
text = "STARÉ MESTO - KOMENSKÉHO SUPER 3 IZBOVÝ TEHLOVÝ BYT 120 M2."

slovak_to_english = {
    'á': 'a', 'ä': 'a', 'č': 'c', 'ď': 'd', 'é': 'e', 'í': 'i', 'ĺ': 'l', 'ľ': 'l',
    'ň': 'n', 'ó': 'o', 'ô': 'o', 'ŕ': 'r', 'š': 's', 'ť': 't', 'ú': 'u', 'ý': 'y', 'ž': 'z',
    'Á': 'A', 'Ä': 'A', 'Č': 'C', 'Ď': 'D', 'É': 'E', 'Í': 'I', 'Ĺ': 'L', 'Ľ': 'L',
    'Ň': 'N', 'Ó': 'O', 'Ô': 'O', 'Ŕ': 'R', 'Š': 'S', 'Ť': 'T', 'Ú': 'U', 'Ý': 'Y', 'Ž': 'Z', ' ': '-'
}


def convert_slovak_to_english(text):
    return ''.join(slovak_to_english.get(char, char) for char in text)


def getPreciseLocation(postal_code, text, slovak_to_english=slovak_to_english):


    lines_with_code = []

    with open("./airflow/dags/SK.txt", "r", encoding="utf8") as file:
        lines = file.readlines()
        for line in lines:
            if cur in line:
                lines_with_code.append(line)

    for line in lines_with_code:
        stripped_line = line[10:]
        transformed_line = stripped_line[:re.search(r'\t', stripped_line).start()]
        saved_line = transformed_line
        transformed_line = transformed_line.lower().split("-")
        if len(transformed_line) > 1:
            transformed_line = transformed_line[1]
        else:
            transformed_line = transformed_line[0]

        
        if convert_slovak_to_english(transformed_line) in convert_slovak_to_english(text.lower()):
            return saved_line

    # print(repr(text.lower()))

    # for name in transformed_lines:
    #     if name in text.lower():
    #         print("what the sigma")

    # print(text.lower())
    # print(transformed_lines)



print(getPreciseLocation(cur, text))