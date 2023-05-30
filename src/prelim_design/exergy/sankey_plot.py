import matplotlib.pyplot as plt
from matplotlib.sankey import Sankey

Sankey(flows=[1, -0.0917, -0.1788, -0.0064, -0.68, -0.04312],
labels=['P_in', 'EM-DC', 'DC-EM',
        'DC-DC', 'Solar-DC', 'P_a'],
orientations=[0, -1, -1, -1, -1, 0]).finish()
plt.title("Energy conversion breakdown")
plt.show()