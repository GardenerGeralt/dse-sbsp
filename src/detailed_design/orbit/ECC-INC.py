from src.plotting.plots import line_plot
import numpy as np



line_plot(x_data=DAYS / 365.25, y_data=RATE, labels=['Nodal precession rate'],
          x_title=r'$\text{{{}}} t\;[years] $'.format('Time from 01-01-2030 '),
          y_title=r'$\text{{{}}} \omega_p\;[deg/day] $'.format('Nodal precession rate '))