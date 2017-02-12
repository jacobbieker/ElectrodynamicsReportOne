import os
import numpy as np
import matplotlib.pyplot as plt
import csv
import re
from pprint import pprint

data = {}
counter = 0
for file in os.listdir(os.path.join(".", "SIMIONRUNS", "partTwo")):
    print(file)
    with open(os.path.join(".", "SIMIONRUNS", "partTwo", file), 'r') as data_source:
        # Get info from title
        counter += 1
        list_name = file.split("_")
        data[counter] = {"KE": list_name[1], "POT": list_name[2], "L": list_name[3], "Q": list_name[4]}
        inner_counter = 0
        for line in data_source:
            #TODO Get Information on charge, Start position, when Y axis crossed, mass, and Kinetic energy
            split_line = line.split(")")
            # Now for all the if statements, cuz I don't get regex
            for index, element in enumerate(split_line):
                print(element)
                if "Ion(" in element and "Event" not in element:
                    inner_counter += 1
                    data[counter][inner_counter] = {}
                    temp = element.split("(")
                    data[counter][inner_counter]["Ion"] = temp[1]
                elif "Event" in element and "Crossed Y" in element:
                    temp = element.split("(")
                    data[counter][inner_counter]["Event"] = "Crossed Y = 0"
                elif "Mass(" in element:
                    temp = element.split("(")
                    data[counter][inner_counter]["Mass"] = temp[1]
                elif "X(" in element:
                    temp = element.split("(")
                    data[counter][inner_counter]["X"] = temp[1]
                elif "Y(" in element:
                    temp = element.split("(")
                    data[counter][inner_counter]["Y"] = temp[1]
                elif "Event(Ion Created)" in element:
                    temp = element.split("(")
                    data[counter][inner_counter]["Event"] = "Created"
        pprint(data)
