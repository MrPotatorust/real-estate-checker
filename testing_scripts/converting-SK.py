import json
import re
import numpy as np
import pandas as pd

cur = "974 01"

lines_with_code = []



with open("./testing_scripts/SK.txt", "r", encoding="utf8") as file:
    lines = file.readlines()
    for line in lines:
        if cur in line:
            lines_with_code.append(line)


print(lines_with_code)