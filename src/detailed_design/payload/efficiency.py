import numpy as np
import matplotlib.pyplot as plt

from matplotlib.sankey import Sankey

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, xticks=[], yticks=[],
                     title="EoL Exergy of the LUMEN system")
sankey = Sankey(ax=ax, scale=0.011, offset=0.2, head_angle=90,
                format='%.1f', unit='%', tolerance=1e-02)

flows_eol = [1,
-0.08,
-0.0092,
-0.638744286,
-0.008161671,
-0.171737776,
-0.001829348,
-0.015807211,
-0.000745197,
-0.046331632,
-0.027442879
]

flows = [1,
-0.08,
-0.0092,
-0.6175224,
-0.008798328,
-0.142239636,
-0.002823528,
-0.024397819,
-0.001150183,
-0.068206996,
-0.045661111
         ]
flows = [1,
-0.08,
-0.0092,
-0.6175224,
-0.008798328,
-0.002221885,
-0.141128694,
-0.002801475,
-0.001383272,
-0.052175644,
-0.050776213,
-0.033992089
         ]
flows = [1,
         -0.08,
         -0.0092,
         -0.638744286,
         -0.008161671,
         -0.002061107,
         -0.170396443,
         -0.00181506,
         -0.000896214,
         -0.033804308
         -0.034491254,
-0.020429656
         ]


a = []
a.append(flows[0])
a.extend(reversed(flows[1:-1]))
print(a)
print(flows)
a.append(flows[-1])
print(a)
flows = np.array(a)
print(sum(flows))

sankey.add(flows=100*flows,
       # labels=['Insolation', '', '', 'First', 'Second', 'Third', 'Fourth', 'Fifth'],
       orientations=[0, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0],
           pathlengths=[0.05, 0.07, 0.2, 0.35, 0.55, 0.45, 0.15, 0.3, 0.35, 0.1, 0.3],)
           #patchlabel="Widget\nA")  # Arguments to matplotlib.patches.PathPatch

diagrams = sankey.finish()
diagrams[0].texts[-1].set_color('r')
diagrams[0].text.set_fontweight('bold')

diagrams[0].texts[0].set_horizontalalignment('right')

plt.show()