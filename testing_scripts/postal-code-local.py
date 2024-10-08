import json
import re
import numpy as np
import pandas as pd

cur = "040 01"
text = "STARÉ MESTO - KOMENSKÉHO SUPER 3 IZBOVÝ TEHLOVÝ BYT 120 M2".lower()


lines_with_code = []



with open("./testing_scripts/SK.txt", "r", encoding="utf8") as file:
    lines = file.readlines()
    for line in lines:
        if cur in line:
            lines_with_code.append(line)


transformed_lines = []

for line in lines_with_code:
    stripped_line = line[10:]
    transformed_line = stripped_line[:re.search(r'\t', stripped_line).start()]
    if transformed_line in text:
        print("sigma")
    transformed_lines.append(transformed_line)


print(transformed_lines)
print(text)