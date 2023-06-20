import numpy as np
import matplotlib.pyplot as plt

def atmos_eff(R, h, theta_array):
    d_array = np.sqrt(R**2 + (h + R)**2 - 2*R*(h + R)*np.cos(theta_array))
    eff_array =  h*np.ones(shape=np.shape(d_array)) / d_array
    eff = np.average(eff_array)
    return eff

def inc_eff(R, h, theta_array):
    length_array = np.sqrt(R**2 + (h + R)**2 - 2*R*(h + R)*np.cos(np.abs(theta_array)))
    phi_array = np.arcsin(np.sin(np.abs(theta_array))*(h + R) / length_array)
    eff_array = np.cos(phi_array)
    eff = np.average(eff_array)
    return eff

R = 6378                        #[km]
h = 35786                       #[km]
power = 100                     #[kW]
n_sat = 1000                     #[-]
spacing = 50                    #[km]

theta_spacing = 2*np.arcsin((spacing/2)/(R + h))

sat_array = np.linspace(1,n_sat,n_sat)
distance = []
incidence = []
total = []
power_array = []

for n in sat_array:
    theta_array = []
    for i in range(int(n)):
        theta_array.append(-(n - 1)/2*theta_spacing + i*theta_spacing)
    theta_array = np.array(theta_array)
    distance_i = atmos_eff(R, h, theta_array)
    incidence_i = inc_eff(R, h, theta_array)
    total_i = distance_i * incidence_i
    distance.append(distance_i)
    incidence.append(incidence_i)
    total.append(total_i)
    power_array.append(n*power*total_i)

plt.plot(sat_array,total)
plt.show()

