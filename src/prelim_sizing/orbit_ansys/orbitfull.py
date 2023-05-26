# -*- coding: utf-8 -*-
"""
Created on Wed May 17 12:18:52 2023

@author: daans
"""

# Add transmit angle in plot - done?
# Add position of receiver
# Solve orbit plotting bug when changing orbital elements

import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, tan, pi
from scipy.optimize import fsolve
from scipy.special import ellipe, ellipeinc
import plotly.graph_objects as go
from orbit_params import *
from orbit_func import *

# import plotly.io as io

# io.renderers.default = 'browser'


class Orbit:
    def __init__(self, SMA, ECC, INC, RAAN, AOP):
        self.SMA = SMA
        self.ECC = ECC
        self.INC = INC
        self.RAAN = RAAN
        self.AOP = AOP
        self.T = 2 * np.pi * np.sqrt(self.SMA**3 / mu_M)
        self.t_array = np.arange(
            0, self.T * (1 + 1 / res_t), self.T / res_t
        )  # what is the 1/res_t for?
        self.theta_array = np.zeros(np.shape(self.t_array))
        for i in range(len(self.t_array)):
            time_point = self.t_array[i]
            mean_anomaly = time_point / self.T * 2 * np.pi
            eccentric_anomaly = fsolve(lambda E: E - ECC * sin(E) - mean_anomaly, mean_anomaly)[0]
            self.theta_array[i] = 2 * np.arctan2(
                tan(eccentric_anomaly / 2), np.sqrt((1 - ECC) / (1 + ECC))
            )
        self.orbit = position3D(SMA, ECC, INC, RAAN, AOP, TA=self.theta_array)
        for i in range(3):
            self.orbit[i][np.where(np.abs(self.orbit[i]) < 0.0001)[0]] = 0

        # Find the angles between all orbital points and the lunar South Pole
        norm = np.array([0, 0, -1])
        angles = []
        for i in range(len(self.orbit[0])):
            vec = np.array([self.orbit[0][i], self.orbit[1][i], self.orbit[2][i] + R_M])
            vec = vec / np.sqrt(vec.dot(vec))
            angle = np.arccos(np.dot(vec, norm))
            angles.append(angle)
        self.trans_idx = np.where(np.array(angles) <= trans_angle)[0]

        # Transmission time
        if self.trans_idx.size > 0:
            t_transmit = self.t_array[self.trans_idx][-1] - self.t_array[self.trans_idx][0]
        else:
            t_transmit = 0

        # Transmission altitude
        if self.trans_idx.size > 0:
            alts = []
            for i in range(len(self.trans_idx)):
                alt = np.sqrt(
                    self.orbit[0][self.trans_idx[i]] ** 2
                    + self.orbit[1][self.trans_idx[i]] ** 2
                    + (self.orbit[2][self.trans_idx[i]] + R_M) ** 2
                )
                alts.append(alt)
            alt_transmit = np.sum(alts) / len(self.trans_idx)
            alt_min = np.min(alts)
            alt_max = np.max(alts)
        if self.trans_idx.size == 0:
            alt_transmit = float("NaN")

        # Time-averaged angle of incidence
        theta_transmit = np.average(np.array(angles)[self.trans_idx])

        # # Eclipse time
        # eclipse_times = []
        # for theta_s in range(0, 360 + res_e, res_e):
        #     theta_s = deg2rad(theta_s)
        #     d = []
        #     phi = []
        #     print(str(round(theta_s / (2 * np.pi) * 100, 1)) + " %")
        #     for i in range(len(orbit[0])):
        #         x_sat, y_sat, z_sat = orbit[0][i], orbit[1][i], orbit[2][i]
        #         x_i = (x_sat + tan(theta_s) * y_sat) / (1 + (tan(theta_s)) ** 2)
        #         y_i = tan(theta_s) * x_i
        #         d_i = np.sqrt((x_sat - x_i) ** 2 + (y_sat - y_i) ** 2 + z_sat ** 2)
        #         d.append(d_i)
        #         phi_i = np.arctan2(y_sat, x_sat)
        #         if phi_i < 0:
        #             phi_i = 2 * np.pi + phi_i
        #         phi.append(phi_i)
        #     ecl = np.where((d < np.ones(np.shape(d)) * R_M) & (phi > np.ones(np.shape(phi)) * (theta_s + np.pi / 2)) & (
        #                 phi < np.ones(np.shape(phi)) * (theta_s + 3 * np.pi / 2)))
        #     if ecl[0].size > 0:
        #         eclipse_time = t_array[ecl][-1] - t_array[ecl][0]
        #     else:
        #         eclipse_time = 0
        #     eclipse_times.append(eclipse_time)
        # max_eclipse = np.max(eclipse_times)

        max_eclipse = 0
        self.ecl_idx = np.where(
            (self.orbit[0] > 0) & (np.sqrt(self.orbit[1] ** 2 + self.orbit[2] ** 2) < R_M)
        )[0]


        # --===== Number of spacecraft in view =====--
        if self.trans_idx.size > 0:
            t_spacing = self.T / n_sat
            sat_in_view = t_transmit / t_spacing
        '''
        if self.index.size > 0:
            l1 = cos(RAAN) * cos(AOP) - sin(RAAN) * sin(AOP) * cos(INC)
            l2 = -cos(RAAN) * sin(AOP) - sin(RAAN) * cos(AOP) * cos(INC)
            m1 = sin(RAAN) * cos(AOP) + cos(RAAN) * sin(AOP) * cos(INC)
            m2 = -sin(RAAN) * sin(AOP) + cos(RAAN) * cos(AOP) * cos(INC)
            n1 = sin(AOP) * sin(INC)
            n2 = cos(AOP) * sin(INC)

            # Find normal vector
            plane_2D = [[0, 1], [1, 0]]
            plane_3D = []
            transform = np.array([[l1, l2], [m1, m2], [n1, n2]])
            for i in range(2):
                plane_3D.append(np.matmul(transform, plane_2D[i]))
            normal_vec = np.cross(plane_3D[0], plane_3D[1])

            ref = position3D(SMA, ECC, INC, RAAN, AOP, TA=deg2rad(0))
            angles = []
            for i in range(0, -2, -1):
                point = np.array(
                    [
                        self.orbit[0][self.trans_idx[i]],
                        self.orbit[1][self.trans_idx[i]],
                        self.orbit[2][self.trans_idx[i]],
                    ]
                )

                # Find angle
                dot = np.dot(ref, point)
                det = (
                    ref[0] * point[1] * normal_vec[2]
                    + point[0] * normal_vec[1] * ref[2]
                    + normal_vec[0] * ref[1] * point[2]
                    - ref[2] * point[1] * normal_vec[0]
                    - point[2] * normal_vec[1] * ref[0]
                    - normal_vec[2] * ref[1] * point[0]
                )
                TA_point = -1 * np.arctan2(det, dot)
                if TA_point < 0:
                    TA_point = 2 * np.pi + TA_point
                angles.append(TA_point)

            # Integrate ellipse equation
            b = np.sqrt(SMA**2 * (1 - ECC**2))
            m = ECC**2
            perim = 4 * SMA * ellipe(m)
            spacing = perim / n_sat

            T0, T1 = angles[0], angles[1]
            t0 = ellipeinc(T0 - 0.5 * np.pi, m)
            t1 = ellipeinc(T1 - 0.5 * np.pi, m)
            arclength = SMA * (t1 - t0)
        if self.trans_idx.size == 0:
            arclength = float("NaN")
            spacing = float("NaN")
        sat_in_view = arclength / spacing
        '''
        # --===== Report data =====--
        print("-Pericenter altitude = " + str(round(SMA * (1 - ECC) - R_M, 2)))
        print("-Apocenter altitude = " + str(round(SMA * (1 + ECC) - R_M, 2)))
        print("-Transmission time = " + str(round(sec2hrs(t_transmit), 2)) + " hrs")
        print("-Transmission percentage = " + str(round(percentage(t_transmit, self.T), 2)) + " %")
        print(
            "-Minimum transmission altitude (from South Pole) = " + str(round(alt_min, 2)) + " km"
        )
        print(
            "-Maximum transmission altitude (from South Pole) = " + str(round(alt_max, 2)) + " km"
        )
        print(
            "-Time-averaged transmission altitude (from South Pole) = "
            + str(round(alt_transmit, 2))
            + " km"
        )
        print(
            "-Time-averaged angle of incidence = " + str(round(rad2deg(theta_transmit), 2)) + " deg"
        )
        print("-Maximum eclipse time = " + str(round(sec2hrs(max_eclipse), 2)) + " hrs")
        print(
            "-For "
            + str(n_sat)
            + " equally spaced satellites in orbit, at any given instant "
            + str(round(sat_in_view, 2))
            + " satellites can transmit at the same time."
        )


class OrbitPlot(Orbit):
    def __init__(self, orbparams):
        super().__init__(*orbparams)
        self.fig = go.Figure()
        self.fig.update_layout(
            template="ggplot2",
            scene=dict(
                xaxis=dict(
                    nticks=4,
                    range=[-20000, 20000],
                ),
                yaxis=dict(
                    nticks=4,
                    range=[-20000, 20000],
                ),
                zaxis=dict(
                    nticks=4,
                    range=[-25000, 15000],
                ),
            ),
            width=1500,
            margin=dict(r=10, l=10, b=10, t=10),
            scene_aspectmode="cube",
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play",
                              method="animate",
                              args=[None])])],
        )


    def plot_moon(self):
        u_m, v_m = np.mgrid[0 : 2 * pi : 200j, 0:pi:200j]
        x_m = R_M * cos(u_m) * sin(v_m)
        y_m = R_M * sin(u_m) * sin(v_m)
        z_m = R_M * cos(v_m)
        self.fig.add_trace(
            go.Surface(x=x_m, y=y_m, z=z_m, colorscale=[[0, "white"], [1, "white"]], opacity=1)
        )
        return x_m, y_m, z_m

    def plot_cone(self, half_angle=70):
        h = np.linspace(0, 20000, 100)
        th = np.linspace(0, 2 * pi, 100)
        H, TH = np.meshgrid(h, th)
        x_c = H * tan(deg2rad(half_angle)) * sin(TH)
        y_c = H * tan(deg2rad(half_angle)) * cos(TH)
        z_c = -H - R_M

        self.fig.add_trace(
            go.Surface(x=x_c, y=y_c, z=z_c, colorscale=[[0, "blue"], [1, "blue"]], opacity=0.1)
        )

    def plot_umbra(self):
        z_s, y_s, x_s = cylinder(R_M, 20000)
        self.fig.add_trace(
            go.Surface(x=x_s, y=y_s, z=z_s, colorscale=[[0, "grey"], [1, "grey"]], opacity=0.5)
        )

    def plot_sc(self, n=80):
        self.SC = self.orbit[:, np.round(np.linspace(0, len(self.orbit[0]) - 1, n)).astype(int)]
        self.fig.add_trace(
            go.Scatter3d(
                x=self.SC[0],
                y=self.SC[1],
                z=self.SC[2],
                connectgaps=False,
                mode="markers",
                marker=dict(
                    size=3,
                    color="black",
                ),
            )
        )

    def plot_orbit(self):

        trans_orbit = self.orbit[:, self.trans_idx]
        ecl_orbit = self.orbit[:, self.ecl_idx]
        rest_orbit = np.hstack((self.orbit[:, self.trans_idx[0]:], self.orbit[:, :self.trans_idx[0]]))
        rest_orbit = np.delete(self.orbit, np.append(self.trans_idx, self.ecl_idx), axis=1)

        # rest_orbit1 = self.orbit[:, self.trans_idx[-1]: self.ecl_idx[0]-100]
        # rest_orbit2 = self.orbit[:, self.ecl_idx[-1]: self.trans_idx[0]]
        #rest_orbit2 = rest_orbit1[:self.ecl_idx[0]]

        '''if self.trans_idx[0] < self.ecl_idx[0]:
            orb_x1 = self.orbit[0][: self.trans_idx[0]]
            orb_x2 = self.orbit[0][self.trans_idx[-1]: self.ecl_idx[0]]
            orb_x3 = self.orbit[0][self.ecl_idx[-1]:]

            orb_y1 = self.orbit[1][: self.trans_idx[0]]
            orb_y2 = self.orbit[1][self.trans_idx[-1]: self.ecl_idx[0]]
            orb_y3 = self.orbit[1][self.ecl_idx[-1]:]

            orb_z1 = self.orbit[2][: self.trans_idx[0]]
            orb_z2 = self.orbit[2][self.trans_idx[-1]: self.ecl_idx[0]]
            orb_z3 = self.orbit[2][self.ecl_idx[-1]:]
        else:
            orb_x1 = self.orbit[0][: self.ecl_idx[0]]
            orb_x2 = self.orbit[0][self.ecl_idx[-1]: self.trans_idx[0]]
            orb_x3 = self.orbit[0][self.trans_idx[-1]:]

            orb_y1 = self.orbit[1][: self.ecl_idx[0]]
            orb_y2 = self.orbit[1][self.ecl_idx[-1]: self.trans_idx[0]]
            orb_y3 = self.orbit[1][self.trans_idx[-1]:]

            orb_z1 = self.orbit[2][: self.ecl_idx[0]]
            orb_z2 = self.orbit[2][self.ecl_idx[-1]: self.trans_idx[0]]
            orb_z3 = self.orbit[2][self.trans_idx[-1]:]'''

        self.fig.add_trace(
            go.Scatter3d(
                x=trans_orbit[0],
                y=trans_orbit[1],
                z=trans_orbit[2],  # Plot transmission part of orbit
                connectgaps=True,
                line=dict(color="green", width=1),
                marker=dict(
                    size=1,
                    color="green",
                ),
            ),
        )
        self.fig.add_trace(
            go.Scatter3d(
                x=ecl_orbit[0],
                y=ecl_orbit[1],
                z=ecl_orbit[2],  # Plot eclipse orbit
                connectgaps=True,
                line=dict(color="black", width=1),
                marker=dict(
                    size=1,
                    color="black",
                ),
            ),
        )
        self.fig.add_trace(
            go.Scatter3d(
                x=rest_orbit[0],
                y=rest_orbit[1],
                z=rest_orbit[2],  # Plot "normal" orbit
                connectgaps=True,
                line=dict(color="red", width=1),
                marker=dict(
                    size=1,
                    color="red",
                ),
            ),
        )
        print(len(self.fig.data))
        # self.fig.add_trace(
        #     go.Scatter3d(
        #         x=rest_orbit2[0],
        #         y=rest_orbit2[1],
        #         z=rest_orbit2[2],  # Plot transmission orbit
        #         connectgaps=True,
        #         marker=dict(
        #             size=1,
        #             color="blue",
        #         ),
        #     ),
        # )
        # self.fig.add_trace(
        #     go.Scatter3d(
        #         x=self.orbit[0][self.ecl_idx],
        #         y=self.orbit[1][self.ecl_idx],
        #         z=self.orbit[2][self.ecl_idx],  # Plot eclipse orbit
        #         marker=dict(
        #             size=1,
        #             color="black",
        #         ),
        #     ),
        # )

    def plot_rec(self):
        ...

    def vary_sc(self, n_sc=80, n_pos=500):
        SC_varied = np.array([[],[],[]])
        '''for i in np.linspace(0, len(self.orbit[0])-1, n_pos):
            print(i)
            np.dstack((SC_varied, self.orbit[:, np.round(np.linspace(1000, 1000+len(self.orbit[0]) - 1, n_sc)).astype(int) % len(self.orbit[0])]))'''
        SC_varied = np.array([self.orbit[:, np.round(np.linspace(i, i+len(self.orbit[0]) - 1, n_sc)).astype(int) % len(self.orbit[0])] for i in np.linspace(0, len(self.orbit[0])-1, n_pos)])
        for i in SC_varied:
            self.fig.add_trace(go.Scatter3d(
                x = i[0],
                y = i[1],
                z = i[2],
                visible = False,
                connectgaps=False,
                mode="markers",
                marker=dict(
                    size=3,
                    color="black",
                ),
            ))

        print(len(self.fig.data))
        return SC_varied

    def add_slider(self):
        # Create and add slider
        steps = []
        SC_varied = self.vary_sc()
        for i in range(len(SC_varied[:, 0, 0])):
            step = dict(
                method="update",
                args=[{"visible": [True]*6 + [False] * len(SC_varied[:, 0, 0])},
                      {"title": "Slider switched to step: " + str(i)}],  # layout attribute
            )
            step["args"][0]["visible"][i+5] = True  # Toggle i'th trace to "visible"
            steps.append(step)

        sliders = [dict(
            active=0,
            currentvalue={"prefix": "Frequency: "},
            pad={"t": 50},
            steps=steps
        )]

        self.fig.update_layout(
            sliders=sliders
        )

    def plot_all(self):
        self.plot_moon()
        self.plot_cone()
        self.plot_umbra()
        self.plot_orbit()
        print(len(self.fig.data))
        # self.plot_sc()
        # self.plot_rec()

    def show(self):
        self.fig.show()
