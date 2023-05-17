import numpy as np
import csv
from MatEnergy import MatEE

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

S_Ex = (S_S_CH4+S_B_CH4) * MatEE["methane"] + (S_B_O2+S_S_O2) * MatEE["oxygen"]
print("Starship", S_Ex)

# Falcon Heavy

F_O2 = (287.4 + 75.2)*1000  # kg
F_CH4 = (123.5 + 32.3)*1000  # kg

F_Ex = F_O2 * MatEE["oxygen"] + F_CH4 * MatEE["methane"]
print("Falcon", F_Ex)

# Centaur [PASS]



# H3

H_PBD =
H_O2 =
H_CH4 =

H_Ex = (H_O2 * MatEE['oxygen']) + (H_CH4 * MatEE["methane"]) + (H_PBD * MatEE["PBD"])
print("H3", H_Ex)
