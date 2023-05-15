# -*- coding: utf-8 -*-
"""
Created on Thu May 11 10:51:58 2023

@author: daans
"""
from math import pi, sqrt, sin, cos, asin, tan, atan2
import numpy as np


## Definitions ##
# Functions
def viewtime(e, theta_v):
    E = 2 * atan2(sqrt((1 - e)) * tan(theta_v / 2), sqrt(1 + e))
    if E < 0:
        E0 = 2 * atan2(sqrt((1 - e)) * tan(pi / 2), sqrt(1 + e))
        E = 2 * E0 + E
    M = E - e * sin(E)
    t = M / (2 * pi) * T
    t_v = T - 2 * t
    return t, t_v


def viewaltitude(t, T):
    t_array = np.arange(round(t), (round(T - t) + 100), 100)
    h_array = []
    for i in t_array:
        #print(i / T)
        M = i / T * 2 * pi
        E = 0
        E_new = 0.1
        counter = 0
        while abs(E_new - E) > 0.001:
            E = E_new
            E_new = E - (E - e * sin(E) - M) / (1 - e * cos(E))
            counter = counter + 1
            if counter > 1000:
                break
        theta = 2 * atan2(tan(E_new / 2), sqrt((1 - e) / (1 + e)))
        h_array.append(a * (1 - e ** 2) / (1 + e * np.cos(theta)) - R)
    h_v = np.average(h_array)
    return h_v


def eclipsetime(a, e, R, T):
    phi = asin(R / a)
    t_e = phi / pi * T
    return t_e


# Moon constants
R = 1737.4  # [km]
mu = 4.90486959 * 10 ** 3  # [km^3/s^2]

# Orbital parameters
i = pi / 2  # [rad]
e = 0.45  # [-]
h_peri = 750  # [km]
a = (R + h_peri) / (1 - e)  # [km]
# h_apo = 750                                         #[km]
# a = (R + h_apo)/(1 + e)                             #[km]

# General calculations
T = 2 * pi * sqrt(a ** 3 / mu)  # [s]
h_peri = a * (1 - e) - R  # [km]
h_apo = a * (1 + e) - R  # [km]
l = a * (1 - e ** 2)
b = sqrt(a * l)
x = a * e - R
y = b * sqrt(1 - (x / a) ** 2)
theta_v = pi - atan2(y, R)

# View time
t, t_v = viewtime(e, theta_v)  # [s]

# View altitude
h_v = viewaltitude(t, T)

# Eclipse time
t_e = eclipsetime(a, e, R, T)  # [s]

print("Eccentricity: " + str(e))
print("Semi-major axis: " + str(round(a, 2)) + " km")
print("Pericenter altitude: " + str(round(h_peri, 2)) + " km")
print("Apocenter altitude: " + str(round(h_apo, 2)) + " km")
print("Orbital period: " + str(round(T / 3600, 3)) + " hrs")
print("Time in view: " + str(round(t_v / 3600, 3)) + " hrs")
print("Percentage in view: " + str(round(t_v / T * 100, 2)) + " %")
print("Average altitude while in view: " + str(round(h_v, 2)) + " km")
print("Time in eclipse: " + str(round(t_e / 3600, 3)) + " hrs")
print("Percentage in eclipse: " + str(round(t_e / T * 100, 2)) + " %")

