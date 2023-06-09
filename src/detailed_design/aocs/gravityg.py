import numpy as np

import src.database.utils as sdbu
k = sdbu.read()

Ix = k["sc MMOI roll"]
Iy = k["sc MMOI pitch"]
Iz = k["sc MMOI yaw"]

mu = 4.90487 * 10**12  # m^3/ s^2
r_moon = 1737400  # [m]
# Taking the minimum transmission altitude ASSUMPTION (worst case scenario)
R = 7391000 + r_moon  # m

R = [750000 + r_moon , 7391000 + r_moon, 7391000 + r_moon]


# currently assuming worse case scenario;
# maximum angle change per axis:
        # x : laser angle
        # y : inclination of orbit
        # z : laser angle

#theta = [57.1, 60, 70]  # from above and graphs of Daan (07.06.23)
theta = [60, 45, 45]

I = [Iz-Iy, Ix-Iz, Iy-Ix]
T_g = []

def calc_Tg(mu, R, I, theta):
    Tg = ((3*mu/(2*R**3))*np.abs(I)*np.sin(2*np.radians(theta)))
    return Tg

for i in range(3):
    T_g.append(calc_Tg(mu, R[i], I[i], theta[i]))

#print(T_g)