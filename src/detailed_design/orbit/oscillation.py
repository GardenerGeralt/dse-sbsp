import pandas as pd
import numpy as np
from src.plotting.plots import line_plot
from scipy.signal import butter,filtfilt
from graphs import six_plots, four_plots

def butter_lowpass_filter(data, cutoff, fs, order):
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

# Filter requirements.
T = 5.0         # Sample Period
fs = 30.0       # sample rate, Hz
cutoff = 4      # desired cutoff frequency of the filter, Hz ,      slightly higher than actual 1.2 Hz
nyq = 0.5 * fs  # Nyquist Frequency
order = 2       # sin wave can be approx represented as quadratic
n = int(T * fs) # total number of samples

##################################
# [ElapsedDays, SMA, ECC, INC, RAAN, AOP, TA]

names = ["oscillation"]

for name in names:
    path = r'{}'.format(name + ".csv")
    df = pd.read_csv(path,delim_whitespace=True,header=None)
    DAYS = np.array(df[:][0][1:])
    SMA = np.array(df[:][1][1:])
    ECC = np.array(df[:][2][1:])
    INC = np.array(df[:][3][1:])
    RAAN = np.array(df[:][4][1:])
    AOP = np.array(df[:][5][1:])
    TA = np.array(df[:][6][1:])

    for i in range(len(DAYS)):
        DAYS[i] = float(DAYS[i])
        SMA[i] = float(SMA[i])
        ECC[i] = float(ECC[i])
        INC[i] = float(INC[i])
        RAAN[i] = float(RAAN[i])
        AOP[i] = float(AOP[i])
        TA[i] = float(TA[i])

    SMA_avg = np.average(SMA) * np.ones(shape=np.shape(SMA))
    ECC_avg = np.average(ECC) * np.ones(shape=np.shape(ECC))
    INC_avg = np.average(INC) * np.ones(shape=np.shape(INC))
    AOP_avg = np.average(AOP) * np.ones(shape=np.shape(AOP))
    #SMA_filtered = butter_lowpass_filter(SMA, cutoff, fs, order)

    '''line_plot(x_data=[(DAYS / 365.25), (DAYS / 365.25)], y_data=[SMA, SMA_avg], labels=['Oscillation', 'Average'],
              x_title=r'$\text{{{}}} t\;[years] $'.format('Time (from 01-01-2030) '),
              y_title=r'$\text{{{}}} a\;[km] $'.format('Semi-major axis '))
    line_plot(x_data=[(DAYS / 365.25), (DAYS / 365.25)], y_data=[ECC, ECC_avg], labels=['Oscillation', 'Average'],
              x_title=r'$\text{{{}}} t\;[years] $'.format('Time (from 01-01-2030) '),
              y_title=r'$\text{{{}}} e\;[-] $'.format('Eccentricity '))
    line_plot(x_data=[(DAYS / 365.25), (DAYS / 365.25)], y_data=[INC, INC_avg], labels=['Oscillation', 'Average'],
              x_title=r'$\text{{{}}} t\;[years] $'.format('Time (from 01-01-2030) '),
              y_title=r'$\text{{{}}} i\;[deg] $'.format('Inclination '))
    line_plot(x_data=[(DAYS / 365.25), (DAYS / 365.25)], y_data=[AOP, AOP_avg], labels=['Oscillation', 'Average'],
              x_title=r'$\text{{{}}} t\;[years] $'.format('Time (from 01-01-2030) '),
              y_title=r'$\text{{{}}} \omega\;[deg] $'.format('Argument of periapsis '))'''
    x_data = np.array([DAYS / 365.25, DAYS / 365.25, DAYS / 365.25, DAYS / 365.25])
    y_data = np.array([[SMA, SMA_avg], [ECC, ECC_avg], [INC, INC_avg], [AOP, AOP_avg]])
    x_titles = [r'$\text{{{}}} t\;[years] $'.format('Time (from 01-01-2030) '), r'$\text{{{}}} t\;[years] $'.format('Time (from 01-01-2030) '),r'$\text{{{}}} t\;[years] $'.format('Time (from 01-01-2030) '),r'$\text{{{}}} t\;[years] $'.format('Time (from 01-01-2030) ')]
    y_titles = [r'$\text{{{}}} a\;[km] $'.format('Semi-major axis '), r'$\text{{{}}} e\;[-] $'.format('Eccentricity '), r'$\text{{{}}} i\;[deg] $'.format('Inclination '), r'$\text{{{}}} \omega\;[deg] $'.format('Argument of periapsis ')]
    print(y_data[0][0])
    four_plots(x_data, y_data, x_titles=x_titles, y_titles=y_titles, labels=['Oscillation', 'Oscillation', 'Oscillation', 'Oscillation'])
    x_data_5y = x_data[:, 0:int(365.25)]
    y_data_5y = y_data[:, :, 0:int(365.25)]
    print(x_data_5y)
    four_plots(x_data_5y, y_data_5y, x_titles=x_titles, y_titles=y_titles, labels=['Oscillation', 'Oscillation', 'Oscillation', 'Oscillation'])
    # line_plot(x_data=[(DAYS[0:366] / 365.25), (DAYS[0:366] / 365.25)], y_data=[SMA[0:366], SMA_avg[0:366]], labels=['Oscillation', 'Average'],
    #           x_title=r'$\text{{{}}} t\;[years] $'.format('Time (from 01-01-2030) '),
    #           y_title=r'$\text{{{}}} a\;[km] $'.format('Semi-major axis '))