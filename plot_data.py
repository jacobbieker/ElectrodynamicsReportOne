import os
import numpy as np
import matplotlib.pyplot as plt
import csv
import re
from pprint import pprint


def determine_t_over_u(kinetic_energy, charge, potential_lens):
    return kinetic_energy/(charge * potential_lens)


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
                if "Event" in element and "Crossed Y" in element:
                    temp = element.split("(")
                    data[counter][inner_counter]["Event"] = "Crossed Y = 0"
                if "Mass(" in element:
                    temp = element.split("(")
                    data[counter][inner_counter]["Mass"] = temp[1]
                if "X(" in element:
                    temp = element.split("(")
                    data[counter][inner_counter]["X"] = temp[1]
                if "Y(" in element:
                    temp = element.split("(")
                    data[counter][inner_counter]["Y"] = temp[1]
                if "Event(Ion Created)" in element:
                    temp = element.split("(")
                    data[counter][inner_counter]["Event"] = "Created"
    pprint(data)


three_data = {}
start_data = []
cross_y_data = []
three_data['1'] = {'Focal': {}, 'Start': {}}
three_data['2'] = {'Focal': {}, 'Start': {}}
three_data['3'] = {'Focal': {}, 'Start': {}}
three_data['4'] = {'Focal': {}, 'Start': {}}
three_data['5'] = {'Focal': {}, 'Start': {}}
three_data['6'] = {'Focal': {}, 'Start': {}}
three_data['7'] = {'Focal': {}, 'Start': {}}
three_data['8'] = {'Focal': {}, 'Start': {}}
three_data['9'] = {'Focal': {}, 'Start': {}}
three_data['10'] = {'Focal': {}, 'Start': {}}
three_data['11'] = {'Focal': {}, 'Start': {}}
three_data['12'] = {'Focal': {}, 'Start': {}}
three_data['13'] = {'Focal': {}, 'Start': {}}
three_data['14'] = {'Focal': {}, 'Start': {}}
three_data['15'] = {'Focal': {}, 'Start': {}}
three_data['16'] = {'Focal': {}, 'Start': {}}
three_data['17'] = {'Focal': {}, 'Start': {}}
three_data['18'] = {'Focal': {}, 'Start': {}}
three_data['19'] = {'Focal': {}, 'Start': {}}
three_data['20'] = {'Focal': {}, 'Start': {}}
three_data['21'] = {'Focal': {}, 'Start': {}}
three_data['22'] = {'Focal': {}, 'Start': {}}
three_data['23'] = {'Focal': {}, 'Start': {}}
three_data['24'] = {'Focal': {}, 'Start': {}}
three_data['25'] = {'Focal': {}, 'Start': {}}
three_data['1'] = {'Focal': {}, 'Start': {}}

for file in os.listdir(os.path.join(".", "SIMIONRUNS", "partThree")):
    print(file)
    with open(os.path.join(".", "SIMIONRUNS", "partThree", file), 'r') as data_source:
        reader = csv.DictReader(data_source, delimiter=",")
        # Get info from title
        for row in reader:
            if row["Events"] == '2048':
                three_data[row["Ion N"]]['Focal'] = {"X": float(row["X"]), "Charge": float(row["Charge"]), "KE": float(row["KE"])}
            elif row["Events"] == '1':
                three_data[row["Ion N"]]['Start'] = {"Y": float(row["Y"]), "Charge": float(row["Charge"]), "KE": float(row["KE"])}
            print(row)
pprint(three_data)



def plot_data(data, title, xaxis, yaxis):
    plt.plot(data[0], data[1], 'ro')
    plt.ylabel(yaxis)
    plt.xlabel(xaxis)
    plt.title(title)
    plt.show()

#Assumign start at 28mm into the grid, the first 14mm long section, then 6mm between each section

# Plot r_0 vs F/L
# To get F, subtract 28 + 14 + 6 + 7 from length, so 54mm total
r_0_vs_F_L_data = [[],[]]
del three_data['13']
for key in three_data:
    r_0_vs_F_L_data[0].append(float(three_data[key]['Start']['Y']))
    r_0_vs_F_L_data[1].append((float(three_data[key]['Focal']['X']) - 54.0)/14.0)

plot_data(r_0_vs_F_L_data, "f/L vs. T/tau*U", "T/tau*U", "f/L")