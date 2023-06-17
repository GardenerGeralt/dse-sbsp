import pandas as pd
import numpy as np
from src.plotting.plots import line_plot

names = ["Eclipse"]
months = {"Jan": 0, "Feb": 31, "Mar": 59.25,
          "Apr": 90.25, "May": 120.25, "Jun": 151.25,
          "Jul": 181.25, "Aug": 212.25, "Sep": 243.25,
          "Oct": 273.25, "Nov": 304.25, "Dec": 334.25}
types = {"Penumbra": 0.5, "Umbra": 1}

for name in names:
    path = r'{}'.format(name)
    df = pd.read_csv(path,delim_whitespace=True,header=None)
    START = np.array(df[:][1:])[:,:4]
    STOP = np.array(df[:][1:])[:,4:8]
    START_times = []
    STOP_times = []
    FACTORS = []
    ECLIPSE_times = []
    DELTA_times = []

    for i in range(len(START)):
        start_i = START[i][3].split(":")
        START_times.append((((float(START[i][2]) * 365.25 + float(months[START[i][1]]) + float(
            START[i][0])) * 24 + float(start_i[0])) * 60 + float(start_i[1])) * 60 + float(start_i[2]))

        stop_i = STOP[i][3].split(":")
        STOP_times.append((((float(STOP[i][2]) * 365.25 + float(months[STOP[i][1]]) + float(
            STOP[i][0])) * 24 + float(stop_i[0])) * 60 + float(stop_i[1])) * 60 + float(stop_i[2]))

        type_i = np.array(df[:][1:])[i, 10]
        factor_i = float(types[type_i])
        FACTORS.append(factor_i)
        ECLIPSE_times.append(factor_i*float(np.array(df[:][1:])[i, 8]))

    counter = 0
    del_i = []
    for i in range(len(START)-1):
        if counter == 0:
            if (START_times[i + 1] - STOP_times[i]) < 86400:
                ECLIPSE_times[i] = ECLIPSE_times[i] + FACTORS[i]*(START_times[i + 1] - STOP_times[i]) + ECLIPSE_times[i+1]
                STOP_times[i] = STOP_times[i+1]
                counter = counter + 1
                del_i.append(i+1)
        else:
            if (START_times[i + 1] - STOP_times[i]) < 86400:
                ECLIPSE_times[i-counter] = ECLIPSE_times[i-counter] + FACTORS[i]*(START_times[i + 1] - STOP_times[i]) + ECLIPSE_times[i+1]
                STOP_times[i-counter] = STOP_times[i+1]
                counter = counter + 1
                del_i.append(i + 1)
            else:
                counter = 0

    for i in sorted(del_i, reverse=True):
        del START_times[i], STOP_times[i], ECLIPSE_times[i]

    for i in range(len(START_times) - 1):
        DELTA_times.append(START_times[i + 1] - STOP_times[i])

    print("Max eclipse time: "+str(round(max(ECLIPSE_times)/3600,2))+" [hrs]")
    print("Min time between eclipses: " + str(round(min(DELTA_times)/86400,2)) + " [days]")
    print("Lunar eclipse transmission factor: "+str(round((max(ECLIPSE_times) + min(DELTA_times)) / min(DELTA_times),4)) + " [-]")

