import numpy as np
import csv
from MatEnergy import MatEE


methane = int(MatEE['methane'])
oxygen = int(MatEE["oxygen"])
hydrogen = int(MatEE["hydrogen"])

# Launchers to be considered:

#|   Starship (S)    |   Falcon Heavy (F)   |   Centaur  (C)  |   H3 (H) |

# Starship

# Booster
S_B_O2 = 2800000  # kg
S_B_CH4 = 800000  # kg
Ratio = S_B_O2/(S_B_O2+S_B_CH4)

#Starship
S_S_Prop = 3600000  # kg
S_S_O2 = Ratio * S_S_Prop
S_S_CH4 = (1-Ratio) * S_S_Prop

S_Ex = (S_S_CH4+S_B_CH4) * methane + (S_B_O2+S_S_O2) * oxygen
# per kg capabilities
S_cap = 100000  # kg

S_Ex_kg = S_Ex/S_cap
print("Starship", S_Ex_kg)


# Falcon Heavy

F_O2 = (287.4 + 75.2)*1000  # kg
F_CH4 = (123.5 + 32.3)*1000  # kg

F_Ex = F_O2 * oxygen + F_CH4 * methane


# per kg capabilities
F_cap = 26700  # kg

F_Ex_kg = F_Ex/F_cap
print("Falcon", F_Ex_kg)

# Centaur [PASS]



# H3

#main stage + 2nd stage
#H_PBD =
H_prop = 248000  # kg

H_H2 = (H_prop) * (2.02/34.02)
H_O2 = (H_prop) * (32/34.02)

H_Ex = (H_H2 * hydrogen) + (H_O2 * oxygen)  # + (H_PBD * MatEE["PBD"])


# per kg capabilities
H_cap = 11900  # kg

H_Ex_kg = H_Ex/H_cap
print("H3", H_Ex_kg)