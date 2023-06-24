import pickle
import numpy as np
import pandas as pd
from src.plotting.plots import line_plot


def Extract(lst,idx1,idx2):
    return [item[idx1][idx2] for item in lst]

path = r'{}'.format("oscillation.csv")
df = pd.read_csv(path,delim_whitespace=True,header=None)
DAYS = np.array(df[:][0][1:])

# [SMA_range[i], ECC_range[i], INC_range[i], AOP_range[i]
# [orbplot.eff, orbplot.peri, orbplot.apo, orbplot.spacing, orbplot.T, orbplot.t_transmit, orbplot.trans_perc, orbplot.sat_in_view, orbplot.theta_inc, orbplot.cos_transmit, orbplot.inc_eff, orbplot.alt_min, orbplot.alt_max, orbplot.alt_transmit, orbplot.alt_avg]
# [orbplot.z_min, orbplot.z_max, orbplot.vel_z, orbplot.acc_z, orbplot.x_min, orbplot.x_max, orbplot.vel_x, orbplot.acc_x]
# [orbplot.f_bd, orbplot.D_rec, orbplot.max_eclipse_time, orbplot.max_eclipse_velocity]

# Load data
data = pickle.load(open('orbit_data_6.p', 'rb'))
PARAM1 = np.array(Extract(data,1,6))
PARAM2 = np.array(Extract(data,1,10))
PARAM3 = 100*np.array(Extract(data,1,0))
#print(np.average(PARAM))



# line_plot(x_data=[(DAYS[:]/365.25), (DAYS[:]/365.25), (DAYS[:]/365.25)], y_data=[PARAM1[:], PARAM2[:], PARAM3[:]],
#           labels=['Transmission efficiency', 'Incidence efficiency', 'Total efficiency'],
#           x_title=r'$\text{{{}}} t\;[years] $'.format('Time (from 01-01-2030) '),
#           y_title=r'$\text{{{}}} \eta\;[\%] $'.format('Efficiency '))