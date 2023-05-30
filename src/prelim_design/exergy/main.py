import numpy as np
from tests.test_prelim_sizing.test_cost_pipeline import TestCostPipeline as tcstppl
from material_exergy import MatEE
from subsys_weights import subsys_weights
from launch_exergy import S_Ex, S_cap

def exergy_calc(M, n):
    m = M/n

    M_sys_col = (1517.37+3644.61)
    M_sys_rad = (3193.84)
    M_sys_trans = (3600)

    delta_V = 1200
    M_prop = m * (1 - 1/( np.exp( delta_V/(250*9.81) ) ) )

    M_payload = (M_sys_col/n) + (M_sys_rad/n) + (M_sys_trans/n)

    M_bus = m - M_payload - M_prop

    m_subsys = []

    for i in subsys_weights:
        x = np.round(float(M_bus)*float(subsys_weights[i]), 2)
        m_subsys.append(float(x))

    subsys_materials = ["aluminium", "graphite", "electronics", "electronics",
                        "electronics", "chromium", "aluminium"]
    ex_subsys = []
    for i in range(len(subsys_materials)):
        ex_subsys.append(m_subsys[i]*float(MatEE[subsys_materials[i]]))
    #print(ex_subsys)

    Ex_prop = (M_prop)*(1/7)*float(MatEE["hydrogen"])+(M_prop)*(6/7)*float(MatEE["oxygen"])
    Ex_payload = (M_sys_col/n)*float(MatEE["silicon"]) + (M_sys_rad/n)*float(MatEE["graphite"]) \
                 + (M_sys_trans/n)*float(MatEE["electronics"])


    Ex_sc_sys = (Ex_payload + Ex_prop + np.sum(ex_subsys))*n  # in MJ

    Ex_launch = S_Ex * int(np.ceil(tcstppl.M/S_cap))

    Ex_total = Ex_sc_sys + Ex_launch
    #print(Ex_total, 'MJ')


    ##############################
    # Production

    Power_gen = 1  # MW
    s_year = 365.25*24*60*60  # [s]

    En_year = Power_gen*s_year
    #print(En_year, "MJ generated")

    Ex_BEP = Ex_total/En_year
    #print(Ex_BEP, 'years')

    return Ex_total, En_year


exergy_calc(tcstppl.M, tcstppl.n_id)


