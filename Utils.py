import re
from ast import literal_eval

def load_data(data_file):
    data = []
    with open(data_file, "r") as file:
        for line in file:
            data_sample = literal_eval(line)
            data.append(data_sample)

    return data
