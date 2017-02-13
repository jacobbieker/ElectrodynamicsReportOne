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
plotting_two_data = [[],[],[],[],[],[],[],[],[], []]
plotting_t_over_u = [[],[],[],[],[],[],[],[],[], []]
for file in os.listdir(os.path.join(".", "SIMIONRUNS", "partTwo")):
    print(file)
    with open(os.path.join(".", "SIMIONRUNS", "partTwo", file), 'r') as data_source:
        # Get info from title
        counter += 1
        list_name = file.split("_")
        data[counter] = {"KE": float(list_name[1].split("E")[1]), "POT": list_name[2], "L": list_name[3], "Q": float(list_name[4].split("Q")[1])}
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
                    data[counter][inner_counter]["Ion"] = int(temp[1])
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

# Get the delimited data
two_delimited_data = {}
two_delimited_data['1'] = {'Focal': {}, 'Start': {}}
two_delimited_data['2'] = {'Focal': {}, 'Start': {}}
two_delimited_data['3'] = {'Focal': {}, 'Start': {}}
two_delimited_data['4'] = {'Focal': {}, 'Start': {}}
two_delimited_data['5'] = {'Focal': {}, 'Start': {}}
two_delimited_data['6'] = {'Focal': {}, 'Start': {}}
two_delimited_data['7'] = {'Focal': {}, 'Start': {}}
two_delimited_data['8'] = {'Focal': {}, 'Start': {}}
two_delimited_data['9'] = {'Focal': {}, 'Start': {}}
two_delimited_data['10'] = {'Focal': {}, 'Start': {}}
two_delimited_data['11'] = {'Focal': {}, 'Start': {}}
two_delimited_data['12'] = {'Focal': {}, 'Start': {}}
two_delimited_data['13'] = {'Focal': {}, 'Start': {}}
two_delimited_data['14'] = {'Focal': {}, 'Start': {}}
two_delimited_data['15'] = {'Focal': {}, 'Start': {}}
two_delimited_data['16'] = {'Focal': {}, 'Start': {}}
two_delimited_data['17'] = {'Focal': {}, 'Start': {}}
two_delimited_data['18'] = {'Focal': {}, 'Start': {}}
two_delimited_data['19'] = {'Focal': {}, 'Start': {}}
two_delimited_data['20'] = {'Focal': {}, 'Start': {}}
two_delimited_data['21'] = {'Focal': {}, 'Start': {}}
two_delimited_data['22'] = {'Focal': {}, 'Start': {}}
two_delimited_data['23'] = {'Focal': {}, 'Start': {}}
two_delimited_data['24'] = {'Focal': {}, 'Start': {}}
two_delimited_data['25'] = {'Focal': {}, 'Start': {}}

for file in os.listdir(os.path.join(".", "SIMIONRUNS", "delimitedTwo")):
    print(file)
    with open(os.path.join(".", "SIMIONRUNS", "delimitedTwo", file), 'r') as data_source:
        two_delimited_data['13'] = {'Focal': {}, 'Start': {}}
        # Get info from title
        counter += 1
        list_name = file.split("_")
        data[counter] = {"KE": float(list_name[1].split("E")[1]), "POT": list_name[2], "L": list_name[3], "Q": float(list_name[4].split("Q")[1])}
        inner_counter = 0
        reader = csv.DictReader(data_source, delimiter=",")
        # Get info from title
        for row in reader:
            if row["Events"] == '2048':
                two_delimited_data[row["Ion N"]]['Focal'] = {"X": float(row["X"]), "Charge": float(row["Charge"]), "KE": float(row["KE"])}
            elif row["Events"] == '1':
                two_delimited_data[row["Ion N"]]['Start'] = {"Y": float(row["Y"]), "Charge": float(row["Charge"]), "KE": float(row["KE"])}

    # now add in data from the delimited stuff, hoepfully some points line up
    del two_delimited_data['13']
    for key in two_delimited_data:
        if -8 <= int(two_delimited_data[key]['Start']['Y']) <= 9:
            spot = -1
            if int(two_delimited_data[key]['Start']['Y']) == -8:
                spot = 1
            elif int(two_delimited_data[key]['Start']['Y']) == -6:
                spot = 2
            elif int(two_delimited_data[key]['Start']['Y']) == -4:
                spot = 3
            elif int(two_delimited_data[key]['Start']['Y']) == -2:
                spot = 4
            elif int(two_delimited_data[key]['Start']['Y']) == 2:
                spot = 6
            elif int(two_delimited_data[key]['Start']['Y']) == 4:
                spot = 7
            elif int(two_delimited_data[key]['Start']['Y']) == 6:
                spot = 8
            elif int(two_delimited_data[key]['Start']['Y']) == 8:
                spot = 9
            if spot != -1:
                plotting_two_data[spot].append((float(two_delimited_data[key]['Focal']['X']) - 54.0)/14.0)
                plotting_t_over_u[spot].append(-1.0 * determine_t_over_u(two_delimited_data[key]['Start']["KE"], two_delimited_data[key]['Start']["Charge"], 10.0))


# Convert data from above to get what we need: where the Y axis was crossed, already have KE, Charge, Potential from filename
# Need to get data only from every ion that has the same start position, so 9 tries per file
# If Ion = 1 it starts at the same place each time, so don't need to check that, only where crossed Y axis
for key in data:
    current_ion = 1
    for key2 in data[key]:
        if isinstance(data[key][key2], dict):
            if "Ion" in data[key][key2].keys() and "Event" in data[key][key2].keys():
                if data[key][key2]["Ion"] == current_ion:
                    plotting_two_data[current_ion].append((float(data[key][key2]["X"].split(" ")[0]) - 54.0)/14.0)
                    plotting_t_over_u[current_ion].append(determine_t_over_u(data[key]["KE"], data[key]["Q"], 10.0))
                current_ion += 1


print(plotting_two_data)
print(plotting_t_over_u)




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


# sort the data
reorder = sorted(range(len(plotting_two_data)), key = lambda ii: plotting_t_over_u[1][ii])
yd = [plotting_two_data[1][ii] for ii in reorder]
xd = [plotting_t_over_u[1][ii] for ii in reorder]

# make the scatter plot
plt.scatter(xd, yd, s=30, alpha=0.15, marker='o')

# determine best fit line
par = np.polyfit(xd, yd, 1, full=True)

slope=par[0][0]
intercept=par[0][1]
xl = [min(xd), max(xd)]
yl = [slope*xx + intercept  for xx in xl]

# coefficient of determination, plot text
variance = np.var(yd)
residuals = np.var([(slope*xx + intercept - yy)  for xx,yy in zip(xd,yd)])
Rsqr = np.round(1-residuals/variance, decimals=2)
plt.text(.9*max(xd)+.1*min(xd),.9*max(yd)+.1*min(yd),'$R^2 = %0.2f$'% Rsqr, fontsize=30)

plt.ylabel("f/L")
plt.xlabel("T/q*U")
plt.title("f/L vs. T/q*U")

# error bounds
yerr = [abs(slope*xx + intercept - yy)  for xx,yy in zip(xd,yd)]
par = np.polyfit(xd, yerr, 2, full=True)

yerrUpper = [(xx*slope+intercept)+(par[0][0]*xx**2 + par[0][1]*xx + par[0][2]) for xx,yy in zip(xd,yd)]
yerrLower = [(xx*slope+intercept)-(par[0][0]*xx**2 + par[0][1]*xx + par[0][2]) for xx,yy in zip(xd,yd)]

plt.plot(xl, yl, '-r')
plt.plot(xd, yerrLower, '--r')
plt.plot(xd, yerrUpper, '--r')
plt.show()

import numpy.polynomial.polynomial as poly

x_new = np.linspace(xd[0], xd[-1], num=len(xd)*10)

coefs = poly.polyfit(xd[0:len(xd)-1], yd[0:len(yd)-1], 2)
ffit = poly.polyval(x_new, coefs)
print("Coefficients: " + str(coefs))
plt.plot(x_new, ffit)
plt.plot(xd, yd, 'o')
plt.ylabel("f/L")
plt.xlabel("T/q*U")
plt.title("f/L vs. T/q*U")
plt.show()


for index2, data_list in enumerate(plotting_two_data):
    plt.plot(plotting_t_over_u[1], plotting_two_data[1], 'ro')
plt.ylabel("f/L")
plt.xlabel("T/q*U")
plt.title("f/L vs. T/q*U")
plt.show()

plot_data(r_0_vs_F_L_data, "r_0 vs f/L", "r_0", "f/L")



##################################3
"""
ONTO THE OTHER THINGY
"""
one_source_data = {}
y_data_energy = []
e_data_energy = []
for file in os.listdir(os.path.join(".", "SIMIONRUNS", "partOne")):
    print(file)
    with open(os.path.join(".", "SIMIONRUNS", "partOne", file), 'r') as data_source:
        reader = csv.DictReader(data_source, delimiter=",")
        for line in reader:
            y_data_energy.append(float(line["Y"]))
            e_data_energy.append(float(line["E"]))
            print(line)

y_new = np.linspace(y_data_energy[0], y_data_energy[-1], num=len(xd)*10)

coefs = poly.polyfit(y_data_energy, e_data_energy, 2)
ffit = poly.polyval(y_new, coefs)
print("Coefficients: " + str(coefs))
plt.plot(y_new, ffit)

plt.plot(y_data_energy, e_data_energy, 'o')
plt.ylabel("E")
plt.xlabel("Y")
plt.title("E vs. Y")
plt.show()
