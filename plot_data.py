import os
import numpy as np
import matplotlib.pyplot as plt
import csv
import re

for file in os.listdir(os.path.join(".", "SIMIONRUNS", "partTwo")):
    print(file)
    with open(os.path.join(".", "SIMIONRUNS", "partTwo", file), 'r') as data_source:
        for line in data_source:
            print(line)
