from src.plotting.plots import line_plot
import numpy as np
from orbit_func import *

INC = np.linspace(39.232,140.768,1000)
ECC = np.sqrt(1 - 5/3*np.cos(deg2rad(INC))**2)

line_plot(x_data=INC, y_data=ECC, labels=['Eccentricity versus inclination'],
          x_title=r'$\text{{{}}} i\;[deg] $'.format('Inclination '),
          y_title=r'$\text{{{}}} e\;[-] $'.format('Eccentricity '))