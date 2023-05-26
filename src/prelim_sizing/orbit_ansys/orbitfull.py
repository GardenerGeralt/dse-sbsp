# -*- coding: utf-8 -*-
"""
Created on Wed May 17 12:18:52 2023

@author: daans
"""

# Add transmit angle in plot - done?
# Add position of receiver

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
        self.index = np.where(np.array(angles) <= trans_angle)[0]

        # Transmission time
        if self.index.size > 0:
            t_transmit = self.t_array[self.index][-1] - self.t_array[self.index][0]
        else:
            t_transmit = 0

        # Transmission altitude
        if self.index.size > 0:
            alts = []
            for i in range(len(self.index)):
                alt = np.sqrt(
                    self.orbit[0][self.index[i]] ** 2
                    + self.orbit[1][self.index[i]] ** 2
                    + (self.orbit[2][self.index[i]] + R_M) ** 2
                )
                alts.append(alt)
            alt_transmit = np.sum(alts) / len(self.index)
            alt_min = np.min(alts)
            alt_max = np.max(alts)
        if self.index.size == 0:
            alt_transmit = float("NaN")

        # Time-averaged angle of incidence
        theta_transmit = np.average(np.array(angles)[self.index])

        self.ecl = np.where(
            (self.orbit[0] > 0) & (np.sqrt(self.orbit[1] ** 2 + self.orbit[2] ** 2) < R_M)
        )[0]
        max_eclipse = 0

        # --===== Number of spacecraft in view =====--
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
                        self.orbit[0][self.index[i]],
                        self.orbit[1][self.index[i]],
                        self.orbit[2][self.index[i]],
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
        if self.index.size == 0:
            arclength = float("NaN")
            spacing = float("NaN")

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
            + str(round(arclength / spacing, 2))
            + " satellites can transmit at the same time."
        )


class OrbitPlot(Orbit):
    def __init__(self, orbparams):
        super().__init__(*orbparams)
        self.fig = go.Figure()
        self.fig.update_layout(
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
            width=1200,
            margin=dict(r=20, l=10, b=10, t=10),
        )
        self.fig.update_layout(scene_aspectmode="cube")

    def plot_moon(self):
        u_m, v_m = np.mgrid[0 : 2 * pi : 200j, 0:pi:20j]
        x_m = R_M * cos(u_m) * sin(v_m)
        y_m = R_M * sin(u_m) * sin(v_m)
        z_m = R_M * cos(v_m)
        self.fig.add_trace(
            go.Surface(x=x_m, y=y_m, z=z_m, colorscale=[[0, "white"], [1, "white"]], opacity=1)
        )
        return x_m, y_m, z_m

    def plot_cone(self):
        """u_c, v_c = np.mgrid[0 : 2 * pi : 200j, 0:pi:200j]
        x_c = SMA * cos(u_c) * sin(v_c)
        y_c = SMA * sin(u_c) * sin(v_c)
        z_c = -1 * np.sqrt((x_c**2 + y_c**2) / tan(trans_angle)) - R_M"""

        phi = deg2rad(70)
        h = np.linspace(0, 20000, 100)
        th = np.linspace(0, 2 * pi, 100)
        H, TH = np.meshgrid(h, th)
        x_c = H * np.arctan(phi) * sin(TH)
        y_c = H * np.arctan(phi) * cos(TH)
        z_c = -H - R_M

        self.fig.add_trace(
            go.Surface(x=x_c, y=y_c, z=z_c, colorscale=[[0, "blue"], [1, "blue"]], opacity=0.1)
        )

    def plot_umbra(self):
        z_s, y_s, x_s = cylinder(R_M, SMA)
        self.fig.add_trace(
            go.Surface(x=x_s, y=y_s, z=z_s, colorscale=[[0, "grey"], [1, "grey"]], opacity=0.5)
        )

    def plot_sc(self, n=80):
        SC_80 = self.orbit[:, np.round(np.linspace(0, len(self.orbit[0]) - 1, n)).astype(int)]
        self.fig.add_trace(
            go.Scatter3d(
                x=SC_80[0],
                y=SC_80[1],
                z=SC_80[2],
                connectgaps=False,
                mode="markers",
                marker=dict(
                    size=3,
                    color="white",
                ),
            )
        )

    def plot_orbit(self):
        if self.index[0] < self.ecl[0]:
            orb_x1 = self.orbit[0][: self.index[0]]
            orb_x2 = self.orbit[0][self.index[-1] : self.ecl[0]]
            orb_x3 = self.orbit[0][self.ecl[-1] :]

            orb_y1 = self.orbit[1][: self.index[0]]
            orb_y2 = self.orbit[1][self.index[-1] : self.ecl[0]]
            orb_y3 = self.orbit[1][self.ecl[-1] :]

            orb_z1 = self.orbit[2][: self.index[0]]
            orb_z2 = self.orbit[2][self.index[-1] : self.ecl[0]]
            orb_z3 = self.orbit[2][self.ecl[-1] :]
        else:
            orb_x1 = self.orbit[0][: self.ecl[0]]
            orb_x2 = self.orbit[0][self.ecl[-1] : self.index[0]]
            orb_x3 = self.orbit[0][self.index[-1] :]

            orb_y1 = self.orbit[1][: self.ecl[0]]
            orb_y2 = self.orbit[1][self.ecl[-1] : self.index[0]]
            orb_y3 = self.orbit[1][self.index[-1] :]

            orb_z1 = self.orbit[2][: self.ecl[0]]
            orb_z2 = self.orbit[2][self.ecl[-1] : self.index[0]]
            orb_z3 = self.orbit[2][self.index[-1] :]

        self.fig.add_trace(
            go.Scatter3d(
                x=orb_x1,
                y=orb_y1,
                z=orb_z1,  # Plot Orbit part 1
                connectgaps=True,
                line=dict(color="red", width=1),
                marker=dict(
                    size=1,
                    color="red",
                ),
            ),
        )
        self.fig.add_trace(
            go.Scatter3d(
                x=orb_x2,
                y=orb_y2,
                z=orb_z2,  # Plot Orbit part 2
                connectgaps=True,
                line=dict(color="red", width=1),
                marker=dict(
                    size=1,
                    color="red",
                ),
            ),
        )
        self.fig.add_trace(
            go.Scatter3d(
                x=orb_x3,
                y=orb_y3,
                z=orb_z3,  # Plot Orbit part 3
                connectgaps=True,
                line=dict(color="red", width=1),
                marker=dict(
                    size=1,
                    color="red",
                ),
            ),
        )
        self.fig.add_trace(
            go.Scatter3d(
                x=self.orbit[0][self.index],
                y=self.orbit[1][self.index],
                z=self.orbit[2][self.index],  # Plot transmission orbit
                marker=dict(
                    size=1,
                    color="blue",
                ),
            ),
        )
        self.fig.add_trace(
            go.Scatter3d(
                x=self.orbit[0][self.ecl],
                y=self.orbit[1][self.ecl],
                z=self.orbit[2][self.ecl],  # Plot eclipse orbit
                marker=dict(
                    size=1,
                    color="black",
                ),
            ),
        )

    def plot_rec(self):
        ...

    def plot_all(self):
        self.plot_moon()
        self.plot_cone()
        self.plot_umbra()
        self.plot_orbit()
        self.plot_sc()
        self.plot_rec()

    def show(self):
        self.fig.show()
