import numpy as np
import matplotlib.pyplot as plt
from src.detailed_design.market.market_analysis import LCOE

investment = 1.7e9 #Euro
eur_to_usd_2018 = 1.17
eur_2023_to_eur_2018 = 1.7e9/1420000000

I_0 = investment * eur_2023_to_eur_2018 *eur_to_usd_2018

I = np.concatenate((np.array([I_0]), np.zeros(24)))



