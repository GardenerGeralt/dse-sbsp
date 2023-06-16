import numpy as np
import scipy.integrate as int
import src.database.utils as sdbu
k = sdbu.read()

CG = [0, 0.6*k["sc height"]]  # assume centre of bus is the origin
Phi = 1367.6  # W/m^2
incidence = 0  # degrees
c = 3*10**8

A_A = 200 # Array Area m^2
A_h = 20 #np.sqrt(A_A)  # m
A_w = 10 #np.sqrt(A_A)  # m
A_x = (k["sc width"]/2)*1.1  # m
A_z = 0  # m

v_avg = 1896  # m/s
t_end = np.round(A_w/v_avg, 4)

M_s = (Phi/c)*A_A*(A_x+A_w/2)
# but with no reference of time

#def TotalM(t):
    #return (Phi/c)*v_avg*t*A_h*(A_x+A_w-v_avg*t)
TM = lambda t: (Phi/c)*v_avg*t*A_h*(A_x+A_w-v_avg*t)
#print(M_s)

x = int.quad(TM, 0, t_end)[0]

T_ts = x/t_end
#print(x)
#print(t_end)
#print(x/t_end)