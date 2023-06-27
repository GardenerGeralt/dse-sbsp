import numpy as np
import pandas as pd
from orbit_func import deg2rad

# General constants
R_M = 1737.4                # [km]
mu_M = 4.9048696 * 10 ** 3  # [km^3/s^2]
J2_M = 2.0330530 * 10 ** -4 # [-]
declination = deg2rad(6.68) # [rad]
lim_up = 20000              # [km]
lim_down = 500              # [km]
lim_trans = 14150           # [km]

# Orbital params
#Input
SMA = 8934.369696969698
ECC = 0.7437844582105605
INC = 2.115021720825856
# INC = np.pi - 2.115021720825856
AOP = deg2rad(90)
RAAN = deg2rad(0)  # [rad]
orbpar = [SMA, ECC, INC, RAAN, AOP]

#Average
# SMA = 8930.43325472
# ECC = 0.7084912
# INC = np.pi - deg2rad(123.25662458)
# AOP = deg2rad(90.0150212)
# RAAN = deg2rad(0)  # [rad]
# orbpar = [SMA, ECC, INC, RAAN, AOP]


#Orbit optimisation LLFO
# SMA_range = np.linspace(R_M + lim_down, R_M + lim_up, 100)
# INC_range, ECC_range = deg2rad(np.loadtxt('LowFrozenLunarOrbit.csv', delimiter=',')[:, 0]), np.loadtxt(
#         'LowFrozenLunarOrbit.csv', delimiter=',')[:, 1]

#Orbit optimisation ELFO
# SMA_range = np.linspace(R_M + lim_down, R_M + lim_up, 100)
# INC_range = deg2rad(np.linspace(110, 140.75, 100))
# ECC_range = np.sqrt(1 - 5/3*np.cos(INC_range)**2)

#GMAT min-max
# SMA_range, INC_range, ECC_range, AOP_range = np.loadtxt('GMATmin-max.csv', delimiter=',')[:, 0], \
#                                              deg2rad(np.loadtxt('GMATmin-max.csv', delimiter=',')[:, 1]), \
#                                              np.loadtxt('GMATmin-max.csv', delimiter=',')[:, 2], \
#                                              deg2rad(np.loadtxt('GMATmin-max.csv', delimiter=',')[:, 3])
#
# SMA, ECC, INC, AOP = [8951.272930978732, 0.7428835420016632, 0.94545446795, 1.4096673278382614]
# RAAN = 0
# orbpar = [SMA, ECC, INC, RAAN, AOP]

#################  Oscillations min-max  #######################
# path = r'{}'.format("oscillation.csv")
# df = pd.read_csv(path,delim_whitespace=True,header=None)
# SMA_range = np.array(df[:][1][1:])
# ECC_range = np.array(df[:][2][1:])
# INC_range = deg2rad(np.array(df[:][3][1:]))
# AOP_range = deg2rad(np.array(df[:][5][1:]))
#
# for i in range(len(SMA_range)):
#     SMA_range[i] = float(SMA_range[i])
#     ECC_range[i] = float(ECC_range[i])
#     INC_range[i] = float(np.pi - INC_range[i])
#     AOP_range[i] = float(AOP_range[i])
# RAAN = 0
# orbpar = [SMA_range[0], ECC_range[0], np.pi - INC_range[0], RAAN, AOP_range[0]]
# orbpar = [SMA_range[0], 0.2, np.pi - deg2rad(75), RAAN, AOP_range[0]]
###############################################################

# Satellite params
n_sat = 133

# Transmitter-receiver params
trans_angle = deg2rad(68.2)
pointing_acc = 6.5 * 10**-6     #[rad]

# Resolution
res_t = 10000
#res_e = 5
res_e = 36
#res_e = 1


