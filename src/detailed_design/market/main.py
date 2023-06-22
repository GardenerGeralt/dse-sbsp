import numpy as np
import matplotlib.pyplot as plt
from src.detailed_design.market.market_analysis import LCOE
from src.detailed_design.market.market_analysis import OperationalCosts

#Original investment in Euro
investment = 3.051e9  # Euro
eur_to_usd_2018 = 1.17
eur_2023_to_eur_2018 = 1.7e9/1420000000
lifetime = 25

#Original investment in 2018 USD
I_0 = investment * eur_2023_to_eur_2018 * eur_to_usd_2018

#List of Investment per year
I_t = np.concatenate((np.array([I_0]), np.zeros(lifetime-1)))

OC = OperationalCosts(150000, 200000, 26, 8, 16000, 28200+30700)
operations_list = OC.total_operational_cost * np.ones(25)
print(operations_list)
maintenance_list = 16500 * np.ones(lifetime)
M_t = operations_list + maintenance_list

P_0 = 1.6638  # MW
t = np.arange(0, lifetime)
P_t = P_0 * (1-0.003)**t*(1-0.003)**t
hours_per_year = 365*24

E_t = P_t * hours_per_year

LCOE = LCOE(I_t, M_t, E_t, 0.07, lifetime).lcoe
print(LCOE)
