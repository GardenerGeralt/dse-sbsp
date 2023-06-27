import pandas as pd
import numpy as np
from src.plotting.plots import line_plot

names = ["RAAN"]

for name in names:
    path = r'{}'.format(name + ".csv")
    df = pd.read_csv(path,delim_whitespace=True,header=None)
    DAYS = np.array(df[:][0][1:])
    RAAN = np.array(df[:][1][1:])

    for i in range(len(DAYS)):
        DAYS[i] = float(DAYS[i])
        RAAN[i] = float(RAAN[i])

    RATE = RAAN + 0
    for i in range(len(DAYS)-1):
        diff = abs(RATE[i+1] - RATE[i])
        if diff > 300:
            RATE[i+1:] = RATE[i+1:] + 360
    RATE = np.gradient(RATE)
    print("Average nodal precession = "+str(round(np.average(RATE),4))+" [deg/day]")

    line_plot(x_data=DAYS/365.25, y_data=RAAN,
              x_title=r'$\text{{{}}} t\;[years] $'.format('Time from 01-01-2030 '),
              # y_title=r'$\text{{{}}} \omega_p\;[deg/day] $'.format('Nodal precession rate '))
              y_title = r'$\text{{{}}} \Omega\;[deg] $'.format('Right ascension of the ascending node '))



