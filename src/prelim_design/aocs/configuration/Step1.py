import numpy as np
import csv

import numpy as np
import matplotlib.pyplot as plt


#not necessary
def pdf(x):
    mean = np.mean(x)
    std = np.std(x)
    y_out = 1 / (std * np.sqrt(2 * np.pi)) * np.exp(- (x - mean) ** 2 / (2 * std ** 2))
    return y_out

x = np.arange(0.0, 0.9, 0.001)


# Mass distribution of the power subsystem
mean = 0.20     # %
std = 0.072047116  # %
y1 = 1 / (std * np.sqrt(2 * np.pi)) * np.exp(- (x - mean) ** 2 / (2 * std ** 2))
z1 = 130


# Mass distribution of the thermal subsystem
mean = 0.04   # %
std = 0.017052266  # %
y2 = 1 / (std * np.sqrt(2 * np.pi)) * np.exp(- (x - mean) ** 2 / (2 * std ** 2))
z2 = 170


# Mass distribution of the Payload subsystem
mean = 0.26   # %
std = 0.16920960  # %
y3 = 1 / (std * np.sqrt(2 * np.pi)) * np.exp(- (x - mean) ** 2 / (2 * std ** 2))
z3 = 390


# Mass distribution of the TTC subsystem
mean = 0.04   # %
std = 0.01917310  # %
y4 = 1 / (std * np.sqrt(2 * np.pi)) * np.exp(- (x - mean) ** 2 / (2 * std ** 2))
z4 = 240




# Plotting the bell-shaped curve
plt.figure(figsize=(6, 6))
plt.plot(x, y1, color='black', label= "Power" )
plt.plot(x, y2, color='blue', label= "Thermal")
plt.plot(x, y3, color='red', label= "Payload")
plt.plot(x, y4, color='brown', label= "TTC")
plt.scatter( 0.13, y1[z1], marker = 'o', s = 25, color = 'red')
plt.scatter( 0.17, y2[z2], marker = 'o', s = 25, color = 'pink')
plt.scatter( 0.39, y3[z3], marker = 'o', s = 25, color = 'yellow')
plt.scatter( 0.24, y4[z4], marker = 'o', s = 25, color = 'orange')

plt.legend(["Power", "Thermal", "Payload", "TTC"], loc='upper right')

plt.show()