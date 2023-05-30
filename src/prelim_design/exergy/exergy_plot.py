import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

from main import exergy_calc
from tests.test_prelim_sizing.test_cost_pipeline import TestCostPipeline as tcstppl

Ex_total, En_year = exergy_calc(tcstppl.M, tcstppl.n_id)

res = 10
x = np.arange(0, 25, 1/res)
Ex = np.repeat(Ex_total, len(x))

En = x*En_year * (1-0.003)**x
Ens = x * En_year

def f(x):
    return x*En_year*(1-0.003)**x - Ex_total
z = fsolve(f, [7])
print('the root is', z[0])


plt.clf()
plt.title('Energy balance of system')
plt.xlabel('Energy invested/geerated [MJ]')
plt.ylabel('Years of operation [years]')
plt.plot(x, Ex, color='black', label='Energy Input into system')
plt.plot(x, En, color='green', label='energy generation by system')
plt.plot(z, Ex[0], 'o', color='red')
plt.legend()
plt.show()
