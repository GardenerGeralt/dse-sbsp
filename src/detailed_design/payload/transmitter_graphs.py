import numpy as np
from src.plotting.plots import line_plot
import plotly.graph_objects as go
def pointing_accuracy(theta_rms):
    d = np.linspace(1e6, 20e6, 200)
    return d/1000, np.arctan(theta_rms/d)


line_plot(*pointing_accuracy(20), y_title="Pointing accuracy to achieve +-20 m (RMS) [rad]", x_title="Distance [km]")
# fig.update_layout(showlegend=False)
def spot_size(M2=1.44, wavelength=976e-9, z=14522.70e3):
    w0 = np.linspace(0.1, 5, 200)
    theta = M2*wavelength/(np.pi*w0)
    wz = w0+z*theta*1.52
    fig1 = go.Figure(data=go.Scatter(x=w0, y=wz, mode="lines+markers"))
    fig1.update_layout(showlegend=False)
    fig1.update_layout(
        # title="Plot Title",
        xaxis_title="Beam waist radius [m]",
        yaxis_title="Beam radius at 14522.70 km [m]",
        # xaxis=dict(
        #     tickmode='linear',
        #     tick0=0.1,
        #     dtick=1
        # ),
        #legend_title="Legend Title",
        #font=dict(
        #    family="Courier New, monospace",
        #    size=18,
        #    color="RebeccaPurple"
        #)
    )

    fig1.show()

'''def spot_size(M2=2,):
    d = np.linspace()'''

spot_size()
# line_plot(*spot_size())
