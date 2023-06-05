import link_budget
import numpy as np
import matplotlib.pyplot as plt
#Note to self: we use X-band (8.5GHz) and a 35m diameter gs antenna at 20 (or 2000 like the adsee assignments
# #,just use TAR = 749/880

T_orb = 26.93 #hr
P_gs = 700 #2000
L_trans = 0.8
L_rec = 0.7
f_dl = 8.5 #GHz
TAR = 749/880
D_gs = 15
e_t = 0.1
R_up = 8e6 #bits/s
stored_data = 8e9 # bits

t_contact = T_orb/2*3600 #s/orbit
SNR_req = 1 #dB, assuming turbocoded at 1e-6 BER
#print(stored_data/t_contact)
def design_antenna(margin_req):
    possible_P = []
    possible_D = []
    for power in range(1, 10):
        for diameter in np.arange(0.1, 10, 0.01):
            lb = link_budget.LinkBudget(power, P_gs, L_trans, L_rec, f_dl, TAR, diameter, D_gs, e_t, R_up,
                                        stored_data, t_contact, SNR_req)
            if lb.margin_up >= margin_req and lb.margin_down >=margin_req:
                possible_P.append(power)
                possible_D.append(diameter)
    D_sc = min(possible_D)
    P_sc = possible_P[possible_D.index(D_sc)]
    return D_sc, P_sc

print(design_antenna(6))