import numpy as np
import src.database.utils as sdbu
k = sdbu.read()

################################################################### Solar Pressure
from srp import Ts, cp
from srp import Phi, As, q, CG
k_total = 1.2*1.5*1.25

#axis = 0  # 0 for torque around z, 1 for torque around x
incidence = 0.0  # degree
T_s = []
for i in [1, 0]:
    T_s.append(np.sum(Ts(Phi, As, q, cp, CG, incidence, i)))
T_s.insert(1, 0.0)
# Torque around x  |  y  |  z
print("SP Torque around x, y, z:", T_s)

################################################################### Gravity Gradient

from gravityg import calc_Tg
from gravityg import mu, R, I, theta

T_g = []
for i in range(len(theta)):
    T_g.append(calc_Tg(mu, R[i], I[i], theta[i]))
print("GG Torque around x, y, z:", T_g)

################################################################### Thermal Shock
from thermalg import T_ts
T_ts = [0,0,T_ts]
print("TS Torque around x, y, z:", T_ts)

################################################################### Internal Torques

m_payload = 72  # kg
r_payload = 1.2  # m from CG
acc_payload = 1.649*10**(-6)  # rad/s^2

T_payload = m_payload*r_payload*acc_payload

T_int = np.full(3, T_payload)
#################################################################

T_total = np.sum([T_s, T_g, T_ts, T_int], axis=0)
T_design = np.max(T_total)*k_total
print("Total Distrubance Torques around x, y, z", T_total)
print()
print("Design Torque [Nm]", T_design)
