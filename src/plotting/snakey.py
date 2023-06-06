import matplotlib.pyplot as plt
from matplotlib.sankey import Sankey
Sankey(flows=[1, -0.1, -0.40, -0.20, -0.3],
       labels=['', 'second', 'Third', 'Fourth', 'Fifth'],
       orientations=[0, -1, -1, -1, 0]).finish()
plt.title("The default settings produce a diagram like this.")
plt.show()