import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
import numpy.polynomial.polynomial as poly

# measured constants
resistor = 47.83 #ohm
big_turns = 500
small_turns = 400
big_radius = .107 #m
area_small = 6.74 #cm
hertz = 164 #hz
voltage = 11.8 #V
u0 = 4.0*np.pi*(10.0**(-7))

#Set up will be "Offset": [], "(mV)": [], "(ms)": [], "(V)": [] where the offset is the key for the (mV), (ms), (V) values
ahh_data = {}
hh_data = {}
one_coil = {}

print(np.sqrt(area_small/np.pi))
"""
# Based off name, each of these can be from the same experiment
for directory in os.listdir(os.path.join("data")):
    print(directory)
    offset = 0
    current_data = {}
    # Split up name to get offset
    if "1coil" in directory:
        directory_parts = directory.split(", ")
        offset_part = directory_parts[1].split("cm")
        offset = float(offset_part[0])
        one_coil[offset] = {"(mV)": [], "(ms)": [], "(V)": []}
        current_data = one_coil
    elif "AHH" in directory:
        directory_parts = directory.split("z")
        offset = float(directory_parts[1])
        ahh_data[offset] = {"(mV)": [], "(ms)": [], "(V)": []}
        current_data = ahh_data
    else:
        # HH is the name
        directory_parts = directory.split(", ")
        offset_part = directory_parts[0].split("z")
        offset = float(offset_part[1])
        hh_data[offset] = {"(mV)": [], "(ms)": [], "(V)": []}
        current_data = hh_data
    # Each of these files is from the same spot
    for data_source in os.listdir(os.path.join("data", directory)):
        with open(os.path.join("data", directory, data_source), "r") as csv_source:
            csv_source.readline()
            headers = csv_source.readline()
            reader = csv.reader(csv_source)
            print(headers)
            for line in reader:
                if line != [] and line != "":
                    current_data[offset]["(mV)"].append(float(line[1]))
                    current_data[offset]["(ms)"].append(float(line[0]))
                    current_data[offset]["(V)"].append(float(line[2]))
#pprint(ahh_data)
#pprint(hh_data)
#pprint(one_coil)


def get_bz(data):
    # Get the average max value from the data points, from getting the max from the different values
    data_max = {}
    data_min = {}
    data_x = []
    data_y  = []
    for key in data:
        offset = key
        data_max[offset] = []
        data_min[offset] = []
        abs_data = np.abs(data[key]["(V)"])
        temp_data = []
        neg_temp_data = []
        for element in abs_data:
            if element > 0.01:
                temp_data.append(element)
            elif element < -0.01:
                neg_temp_data.append(element)
            else:
                if temp_data != []:
                    data_max[offset].append(max(temp_data))
                    temp_data = []
                if neg_temp_data != []:
                    data_min[offset].append(min(neg_temp_data))
                    neg_temp_data = []
        data_max[offset] = np.average(data_max[offset])
        data_min[offset] = np.median(data_min[offset])
        print(data_max)
        print(data_min)
    for key in data_max:
        data_y.append(key)
        data_x.append(data_max[key])

    # Other way
    #data_x = []
    #data_y = []
    #for key in data:
    #    data_x.append(max(data[key]["(mV)"])/1000)
    #    data_y.append(key)
    with open("store1.txt", "a") as storing:
        for element in data_x:
            storing.write(str(element) + "\n")
        storing.write("\n")
        for element in data_y:
            storing.write(str(element) + "\n")
        storing.write("\n")
    return data_x, data_y

def make_graph(data, yaxis, xaxis, title, model_lines):
    # Graph B(z) vs z
    return 0

hh_max, hh_y = get_bz(hh_data)
ahh_max, ahh_y = get_bz(ahh_data)
one_coil_max, one_coil_y = get_bz(one_coil)
"""


def current_t(amplitude, hertz, t):
    #I(t)=I0sin(2πft+φ)
    sine = 2.0*np.pi*hertz*t
    return amplitude*np.sin(sine)


hh_max = []
hh_y = []
ahh_max = []
ahh_y = []
one_coil_max = []
one_coil_y = []

with open("store1.txt") as storing:
    for i in range(0, 14):
        hh_max.append(float(storing.readline().strip()))
    print(storing.readline())
    for j in range(0, 14):
        hh_y.append(float(storing.readline().strip())) #convert to cm
    print(storing.readline())
    for k in range(0, 23):
        ahh_max.append(float(storing.readline().strip()))
    print(storing.readline())
    for l in range(0,23):
        ahh_y.append(float(storing.readline().strip()))
    print(storing.readline())
    for m in range(0, 9):
        one_coil_max.append(float(storing.readline().strip()))
    print(storing.readline())
    for n in range(0,9):
        one_coil_y.append(float(storing.readline().strip()))


def ideal_bz(I, N, R, z):
    # Bz=μ0INR·121+zR2−/2
    value = (u0*I*N) / R
    value *= 0.5*((1+(z/R)**2)**(-1.5))
    return value


def big_b(e, hertz, turns, area):
    denominator = 2.0*np.pi*hertz*turns*area
    value = e / denominator
    return value


def ideal_bz_two(I, N, R, z, L, anti):
    # Bz=μ0INR·121+zR2−/2
    value = u0*I*N / (2*R)
    if anti:
        value *= (((1 + (z / R + L / (2.0 * R)) ** 2) ** (-1.5)) - (1 + (z / R - L / (2.0 * R)) ** 2) ** (-1.5))
    else:
        value *= (((1 + (z / R + L / (2.0 * R)) ** 2) ** (-1.5)) + (1 + (z / R - L / (2.0 * R)) ** 2) ** (-1.5))
    return value

print(ideal_bz_two(11.8/47.83, 400, np.sqrt(area_small/np.pi), z=0.25, L=big_radius, anti=False))

num_points = 100
def create_one_coil():
    numbers = np.linspace(0, 37, num_points, retstep=False)
    output = np.linspace(0, 37, num_points, retstep=False)
    for index, element in enumerate(numbers):
        output[index] = 200 * ideal_bz(11.8/47.83, N=small_turns, R=np.sqrt(area_small/np.pi), z=numbers[index])
    return output


def create_ahh():
    numbers = np.linspace(-37, 37, num_points, retstep=False)
    output = np.linspace(-37, 37, num_points, retstep=False)
    for index, element in enumerate(numbers):
        output[index] = 200 * ideal_bz_two(11.8/47.83, N=small_turns, R=np.sqrt(area_small/np.pi), z=numbers[index], anti=True, L=np.sqrt(3)*big_radius)
    return output


def create_hh():
    numbers = np.linspace(-37, 37, num_points, retstep=False)
    output = np.linspace(-37, 37, num_points, retstep=False)
    for index, element in enumerate(numbers):
        output[index] = 50 * ideal_bz_two(11.8/47.83, N=small_turns, R=np.sqrt(area_small/np.pi), z=element, anti=False, L=big_radius)
    print(output)
    return output

def create_db_dz():
    numbers = np.linspace(-37,37, num_points, retstep=False)
    output = np.linspace(-37, 37, num_points, retstep=False)
    def db_dz(I, N, R):
        value = -48./49.
        value *= np.sqrt(3./7.)
        value *= (u0*I*N)/(R**2)
        return value
    for index, element in enumerate(numbers):
        output[index] = db_dz(11.8/47.83, N=small_turns, R=np.sqrt(area_small/np.pi))
    return output

# B(z)

#z
hh_y_range = np.linspace(-37,stop=37, num=num_points)
ahh_y_range = np.linspace(-37,stop=37, num=num_points)
one_coil_y_range = np.linspace(0,stop=37, num=num_points)

y_new = np.linspace(0, 37, num=len(one_coil_max)*10)

plt.plot(one_coil_y_range, create_one_coil())
plt.plot(one_coil_y, one_coil_max, 'ro')
plt.title("One coil")
plt.ylabel("Voltage (V)")
plt.xlabel("Distance (cm)")


coefs = poly.polyfit(one_coil_y, one_coil_max, 4)
ffit = poly.polyval(y_new, coefs)
print("Coefficients: " + str(coefs))
plt.plot(y_new, ffit)
plt.show()

y_new = np.linspace(-37, 37, num=len(hh_max)*10)


plt.plot(hh_y_range, create_hh())
plt.plot(hh_y, hh_max, 'ro')
plt.title("Helmholtz Coil")
plt.ylabel("Voltage (V)")
plt.xlabel("Distance (cm)")

coefs = poly.polyfit(hh_y, hh_max, 4)
ffit = poly.polyval(y_new, coefs)
print("Coefficients: " + str(coefs))
plt.plot(y_new, ffit)
plt.show()

y_new = np.linspace(-37, 37, num=len(ahh_max)*10)


plt.plot(ahh_y_range, create_db_dz())
plt.plot(ahh_y, ahh_max, 'ro')
plt.title("AntiHelmholtz Coil")
plt.ylabel("Voltage (V)")
plt.xlabel("Distance (cm)")
coefs = poly.polyfit(ahh_y, ahh_max, 4)
ffit = poly.polyval(y_new, coefs)
print("Coefficients: " + str(coefs))
plt.plot(y_new, ffit)

plt.show()
