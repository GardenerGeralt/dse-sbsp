import link_budget
import numpy as np
#Note to self: we use X-band (8.5GHz) and a 35m diameter gs antenna at 20kW (or 2000 like the adsee assignments
        #,just use TAR = 749/880
        #Asssume each storage element = 8 bytes ->
P_gs = 2000 #20000
L_trans = 0.8
L_rec = 0.7
f_dl = 8.5 #GHz
TAR = 749/880
D_gs = 35
e_t = 1
R_up = 1e9 #bits/s
stored_data = 1e12 # bits
t_contact = 12*3600 #hr/day
SNR_req = 10.5 #dB, assuming uncoded at 1e-6 BER


def design_antenna(margin_req):
    possible_P = []
    possible_D = []
    for power in range(1, 100):
        for diameter in np.arange(0.1, 5, 0.01):
            lb = link_budget.LinkBudget(power, P_gs, L_trans, L_rec, f_dl, TAR, diameter, D_gs, e_t, R_up, stored_data, t_contact, SNR_req)
            if lb.margin_up >= margin_req and lb.margin_down >=margin_req:
                possible_P.append(power)
                possible_D.append(diameter)
                #print(lb.margin_up,lb.margin_down, power, diameter)


    D_sc = min(possible_D)
    P_sc = possible_P[possible_D.index(D_sc)]

    return D_sc, P_sc


print(design_antenna(3))