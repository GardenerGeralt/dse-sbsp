import numpy as np

import src.database.utils as sdbu
k = sdbu.read()
#from structures import cg
#from payload import array width, array height, array area
#from thermal import reflectance factor

  # coordinates will be given as [x, z] as the y disturbance is neglected



CG = [0, 0.3*k["sc height"]]  # assume centre of bus is the origin
Phi = 1367.6  # W/m^2
incidence = 0  # degrees

A_A = 200  # Array Area m^2
A_h = 20 #np.sqrt(A_A)
A_w = 10 #np.sqrt(A_A)
A_x = (k["sc width"]/2)*1.1
A_z = 0

B_h = k["sc height"]
B_w = k["sc width"]
B_A = B_w*B_h  # Bus Area m^2

As = np.array([A_A, A_A, B_A])

A_q = 0.8
B_q = 0.8
q = np.array([A_q, A_q, B_q])
def calc_cp(A_width, A_height, x_dist, z_dist):  # calculate the centre of pressure
    cp = np.array([np.sign(x_dist)*A_width / 2 + x_dist, np.sign(z_dist)*A_height / 2 + z_dist])
    return cp


cp = calc_cp(A_w, A_h, A_x, A_z), calc_cp(A_w, A_h, -A_x, A_z), np.array([0, 0])  #ass. sc cp at the center of its area

def Ts(Phi, As, q, cp, cg, inc, axis):
    c = 3*10**8  # m/s
    Ts = []
    for i in range(len(As)):
        Ts.append((Phi/c) * As[i] * (1+q[i])*(cg[axis]-cp[i][axis])*np.cos(inc))
    return Ts

#axis = 0
#print(Ts(Phi, As, q, cp, CG, 0, axis))