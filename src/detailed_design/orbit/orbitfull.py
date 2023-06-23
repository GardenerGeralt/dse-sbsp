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
from src.plotting.plots import line_plot

#import plotly.io as io

#io.renderers.default = 'browser'


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
            theta = 2 * np.arctan2(tan(eccentric_anomaly / 2), np.sqrt((1 - ECC) / (1 + ECC)))
            if theta < 0:
                theta = 2 * np.pi + theta
            self.theta_array[i] = theta
        self.orbit = position3D(SMA, ECC, INC, RAAN, AOP, TA=self.theta_array)
        for i in range(3):
            self.orbit[i][np.where(np.abs(self.orbit[i]) < 0.0001)[0]] = 0

        # Find the self.angles between all orbital points and the lunar South Pole
        norm = np.array([0, 0, -1])
        self.angles = []
        for i in range(len(self.orbit[0])):
            vec = np.array([self.orbit[0][i], self.orbit[1][i], self.orbit[2][i] + R_M])
            vec = vec / np.sqrt(vec.dot(vec))
            angle = np.arccos(np.dot(vec, norm))
            self.angles.append(angle)
        self.angles = np.array(self.angles)
        self.trans_idx = np.where(np.array(self.angles) <= trans_angle)[0]

        # --===== Transmission time  =====--
        if self.trans_idx.size > 0:
            self.t_transmit = self.t_array[self.trans_idx][-1] - self.t_array[self.trans_idx][0]
        else:
            self.t_transmit = 0

        # --===== Average altitude =====--
        self.altitudes = []
        for i in range(len(self.t_array)):
            altitude = np.sqrt(self.orbit[0] ** 2 + self.orbit[1] ** 2 + self.orbit[2] ** 2) - R_M
            self.altitudes.append(altitude)
        self.alt_avg = np.average(self.altitudes)

        # --===== Transmission altitude  =====--
        if self.trans_idx.size > 0:
            self.alts = []
            for i in range(len(self.trans_idx)):
                alt = np.sqrt(
                    self.orbit[0][self.trans_idx[i]] ** 2
                    + self.orbit[1][self.trans_idx[i]] ** 2
                    + (self.orbit[2][self.trans_idx[i]] + R_M) ** 2
                )
                self.alts.append(alt)
            self.alts = np.array(self.alts)
            self.alt_transmit = np.sum(self.alts) / len(self.trans_idx)
            self.alt_min = np.min(self.alts)
            self.alt_max = np.max(self.alts)
        if self.trans_idx.size == 0:
            self.alt_transmit = float("NaN")
            self.alt_min = float("NaN")
            self.alt_max = float("NaN")
            self.alts = np.array([])

        # --===== Time-averaged angle of incidence  =====--
        theta_transmit = np.average(np.array(self.angles)[self.trans_idx])
        self.cos_transmit = np.average(cos(np.array(self.angles)[self.trans_idx]))

        # --===== Eclipse =====--
        self.max_eclipse_time = 0
        self.max_eclipse_velocity = 0

        # d = []
        # phi = []
        # for theta_s in range(0, 360 + res_e, res_e):
        #     theta_s = deg2rad(theta_s)
        #     print(str(round(theta_s / (2 * np.pi) * 100, 1)) + " %")
        #     for theta_i in np.linspace(-declination,declination,5):
        #         for i in range(len(self.orbit[0])):
        #             x_sat, y_sat, z_sat = self.orbit[0][i], self.orbit[1][i], self.orbit[2][i]
        #             x_i = (x_sat + tan(theta_s) * y_sat) / (1 + (tan(theta_s)) ** 2)
        #             y_i = tan(theta_s) * x_i
        #
        #             d_i = np.sqrt((x_sat - x_i) ** 2 + (y_sat - y_i) ** 2 + (z_sat - np.sqrt(x_sat**2 + y_sat**2)*sin(theta_i)) ** 2)
        #             d.append(d_i)
        #
        #             phi_i = np.arctan2(y_sat, x_sat)
        #             if phi_i < 0:
        #                 phi_i = 2 * np.pi + phi_i
        #             phi.append(phi_i)
        #
        #         ecl = np.where((d < np.ones(np.shape(d)) * R_M) & (phi > np.ones(np.shape(phi)) * (theta_s + np.pi / 2)) & (
        #               phi < np.ones(np.shape(phi)) * (theta_s + 3 * np.pi / 2)))
        #         if ecl[0].size > 0:
        #             # Max eclipse time
        #             eclipse_time = self.t_array[ecl][-1] - self.t_array[ecl][0]
        #             if eclipse_time > self.max_eclipse_time:
        #                 self.max_eclipse_time = eclipse_time
        #
        #             # Max eclipse velocity
        #             for j in range(0, -2, -1):
        #                 r_j = np.sqrt(self.orbit[0][ecl[0][j]] ** 2 + self.orbit[1][ecl[0][j]] ** 2 + self.orbit[2][ecl[0][j]] ** 2)
        #                 v_j = np.sqrt(mu_M * (2 / r_j - 1 / SMA))
        #                 if v_j > self.max_eclipse_velocity:
        #                     self.max_eclipse_velocity = v_j
        #
        #         d = []
        #         phi = []

        self.ecl_idx = np.where(
            (self.orbit[0] > 0) & (np.sqrt(self.orbit[1] ** 2 + self.orbit[2] ** 2) < R_M)
        )[0]

        # --===== Number of spacecraft in view =====--
        if self.trans_idx.size > 0:
            t_spacing = self.T / n_sat
            self.sat_in_view = round(np.round((self.t_transmit / t_spacing),0) - 1)
        else:
            self.sat_in_view = float("NaN")
            self.trans_idx = [0]

        # --===== Minimum spacecraft spacing =====--
        self.sats = self.orbit[:, np.round(np.linspace(0, len(self.orbit[0])-1, n_sat+1)).astype(int) % len(self.orbit[0])]
        self.sats = self.sats[:,:-1]

        if n_sat % 2 == 0:
            idx = int(n_sat/2)
        else:
            idx = int(n_sat/2 - 1)
        d_min = np.sqrt(
            (self.sats[0][idx] - self.sats[0][idx + 1]) ** 2 + (self.sats[1][idx] - self.sats[1][idx + 1]) ** 2 + (
                    self.sats[2][idx] - self.sats[2][idx + 1]) ** 2)

        # --===== Laser pointing =====--
        norm_y = np.array([0, 1, 0])
        dt = self.T / res_t

        z_angles = []
        x_angles = []

        if len(self.trans_idx) > 1:
            for i in range(len(self.t_array))[self.trans_idx[0]-1:self.trans_idx[-1]+2]:
                # Z angle
                vec_xy = -np.array([self.orbit[0][i], self.orbit[1][i], 0])
                vec_xy = vec_xy / np.sqrt(vec_xy.dot(vec_xy))
                z_angle = np.arctan2((vec_xy[1]*norm_y[0]-vec_xy[0]*norm_y[1]),(vec_xy[0]*norm_y[0]+vec_xy[1]*norm_y[1]))
                z_angles.append(z_angle)

                # X angle
                vec_yz = -np.array([0, self.orbit[1][i], self.orbit[2][i] + R_M])
                vec_yz = vec_yz / np.sqrt(vec_yz.dot(vec_yz))
                x_angle = np.arccos(np.dot(vec_yz, norm_y))
                if self.orbit[2][i] <= 0:
                    x_angles.append(x_angle)
                else:
                    x_angles.append(-x_angle)

            # Pointing about Z axis
            point = (z_angles[-1] - z_angles[0]) * (len(self.t_array) - (self.trans_idx[-1] + 1)) / (
                        len(self.t_array) - len(self.trans_idx))

            angles_z2 = z_angles[1:-1]
            d_angles_z2 = np.gradient(angles_z2,dt)
            dd_angles_z2 = np.gradient(d_angles_z2,dt)
            angles_z1 = np.linspace(z_angles[-1] - point, z_angles[0], self.trans_idx[0])
            d_angles_z1 = np.gradient(angles_z1,dt)
            dd_angles_z1 = np.gradient(d_angles_z1,dt)
            angles_z3 = np.linspace(z_angles[-1], z_angles[-1] - point, len(self.t_array) - (self.trans_idx[-1] + 1))
            d_angles_z3 = np.gradient(angles_z3,dt)
            dd_angles_z3 = np.gradient(d_angles_z3,dt)

            self.angles_z = rad2deg(np.concatenate((angles_z1,angles_z2,angles_z3)))
            self.d_angles_z = rad2deg(np.concatenate((d_angles_z1,d_angles_z2,d_angles_z3)))
            self.dd_angles_z = rad2deg(np.concatenate((dd_angles_z1, dd_angles_z2, dd_angles_z3)))

            # Pointing about X axis
            point = (x_angles[-1] - x_angles[0]) * (len(self.t_array) - (self.trans_idx[-1] + 1)) / (
                        len(self.t_array) - len(self.trans_idx))

            angles_x2 = x_angles[1:-1]
            d_angles_x2 = np.gradient(angles_x2,dt)
            dd_angles_x2 = np.gradient(d_angles_x2,dt)
            angles_x1 = np.linspace(x_angles[-1] - point, x_angles[0], self.trans_idx[0])
            d_angles_x1 = np.gradient(angles_x1,dt)
            dd_angles_x1 = np.gradient(d_angles_x1,dt)
            angles_x3 = np.linspace(x_angles[-1], x_angles[-1] - point, len(self.t_array) - (self.trans_idx[-1] + 1))
            d_angles_x3 = np.gradient(angles_x3,dt)
            dd_angles_x3 = np.gradient(d_angles_x3,dt)

            self.angles_x = rad2deg(np.concatenate((angles_x1,angles_x2,angles_x3)))
            self.d_angles_x = rad2deg(np.concatenate((d_angles_x1,d_angles_x2,d_angles_x3)))
            self.dd_angles_x = rad2deg(np.concatenate((dd_angles_x1, dd_angles_x2, dd_angles_x3)))
        else:
            self.angles_z, self.d_angles_z, self.dd_angles_z = 0, 0, 0
            self.angles_x, self.d_angles_x, self.dd_angles_x = 0, 0, 0

        self.z_min = np.min(self.angles_z)
        self.z_max = np.max(self.angles_z)
        self.vel_z = np.max(np.abs(self.d_angles_z))
        self.acc_z = np.max(np.abs(self.dd_angles_z))
        self.x_min = np.min(self.angles_x)
        self.x_max = np.max(self.angles_x)
        self.vel_x = np.max(np.abs(self.d_angles_x))
        self.acc_x = np.max(np.abs(self.dd_angles_x))

        # --===== Required yaw rate =====--
        self.precession_rate = -(3/2) * (R_M/(self.SMA*(1-self.ECC**2)))**2 * J2_M * (2*pi/self.T) * cos(self.INC)
        self.yaw_rate = pi/yrs2sec(0.5) + self.precession_rate

        # --===== Receiver incidence diameter ratio =====--
        if len(self.trans_idx) > 1:
            self.eta_d = (self.alts / self.alt_max) / sin(pi/2 - self.angles[self.trans_idx])
            self.ratio = np.average(self.eta_d)
            self.f_bd = round(np.max(self.eta_d), 3)
        else:
            self.eta_d = 1
            self.ratio = 1
            self.f_bd = 1

        # --===== Receiver diameter =====--
        Ms = 1.44
        lam = 976*10**-9
        D_exp = 2
        theta_p = 1.26*10**-6
        theta_pk = 0.65*10**-6

        if len(self.trans_idx) > 1:
            self.D_rec_range = 2*self.alts*1000*(1.52*(2*Ms*lam)/(np.pi*D_exp)*self.eta_d + theta_p + theta_pk) + D_exp
            self.D_rec = round(np.max(self.D_rec_range), 2)
        else:
            self.D_rec = 0

        # --===== System efficiency =====--
        if len(self.trans_idx) > 1:
            self.trans_frac = self.t_transmit/self.T
            self.inc_eff = 100*(1 - np.average(5.6*10**-4 * rad2deg(np.array(self.angles)[self.trans_idx]) + 0.052*np.ones(shape=np.shape(self.trans_idx))))
            self.eff = round(self.t_transmit/self.T * self.inc_eff/100, 4)

        else:
            self.trans_frac = 0
            self.inc_eff = 0
            self.eff = 0

        # Random calcs
        self.peri = round(SMA * (1 - ECC) - R_M, 2)
        self.apo = round(SMA * (1 + ECC) - R_M, 2)
        self.spacing = round(d_min,2)
        self.trans_perc = round(percentage(self.t_transmit, self.T), 2)
        self.theta_inc = round(rad2deg(theta_transmit), 2)

        # --===== Report data =====--
        # print("")
        # print("--===== Orbit datasheet =====--")
        # print("-Periapsis altitude = " + str(self.peri))
        # print("-Apoapsis altitude = " + str(self.apo))
        # print("-Orbital period = " + str(round(sec2hrs(self.T),2)) + " hrs")
        # print("-Transmission time = " + str(round(sec2hrs(self.t_transmit), 2)) + " hrs")
        # print("-Transmission percentage = " + str(self.trans_perc) + " %")
        # print(
        #     "-Minimum transmission altitude (from South Pole) = " + str(round(self.alt_min, 2)) + " km"
        # )
        # print(
        #     "-Maximum transmission altitude (from South Pole) = " + str(round(self.alt_max, 2)) + " km"
        # )
        # print(
        #     "-Time-averaged transmission altitude (from South Pole) = "
        #     + str(round(self.alt_transmit, 2))
        #     + " km"
        # )
        # print(
        #     "-Time-averaged angle of incidence = " + str(self.theta_inc) + " deg"
        # )
        # print(
        #     "-Time-averaged cosine of angle of incidence = " + str(round(self.cos_transmit, 4))
        # )
        # print(
        #     "-Time-averaged incidence efficiency = " + str(round(self.inc_eff, 2)) + " %"
        # )
        # print(
        #     "-Maximum eclipse time = " + str(round(sec2hrs(self.max_eclipse_time), 3)) + " hrs"
        # )
        # print(
        #     "-Maximum eclipse velocity = " + str(round(self.max_eclipse_velocity, 3)) + " km/s"
        # )
        # print(
        #     "-Nodal precession over mission lifetime = " + str(round(rad2deg(25*yrs2sec(self.precession_rate)),2)) + " deg"
        # )
        # print(
        #     f"-Yaw rate to always face the Sun = {rad2deg(self.yaw_rate):.3e} deg/s"
        # )
        # print(
        #     "-For "
        #     + str(n_sat)
        #     + " equally spaced satellites in orbit, at least "
        #     + str(self.sat_in_view)
        #     + " satellites can transmit at the same time."
        # )
        # print("-Minimum spacecraft spacing = " + str(self.spacing) + " km"
        #       )
        # print(
        #     "-Laser pointing z-angle range = " + str(round(rad2deg(np.max(self.angles_z)-np.min(self.angles_z)),2)) + " deg"
        # )
        # print(
        #     "-Laser pointing x-angle range = " + str(round(rad2deg(np.max(self.angles_x) - np.min(self.angles_x)), 2)) + " deg"
        # )
        # print(
        #     "-Receiver incidence diameter factor = " + str(round(self.ratio,3))
        # )
        # print("-Maximum beam dilution factor = " + str(self.f_bd))
        # print("-Maximum required receiver diameter = " + str(self.D_rec) + " m")
        # print("-Efficiency = "+ str(self.eff))

        # print("SMA: " + str(self.SMA) + " km")
        # print("ECC: " + str(self.ECC))
        # print("INC: " + str(rad2deg(self.INC)) + " deg")
        # print("EFF: " + str(self.eff))

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
        self.fig.update_layout(transition={'duration': 0.2})

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
        # print(len(self.fig.data))
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

    def vary_sc(self, n_sc=n_sat, n_pos=1000):
        SC_varied = np.array([[],[],[]])
        '''for i in np.linspace(0, len(self.orbit[0])-1, n_pos):
            print(i)
            np.dstack((SC_varied, self.orbit[:, np.round(np.linspace(1000, 1000+len(self.orbit[0]) - 1, n_sc)).astype(int) % len(self.orbit[0])]))'''
        #SC_varied = np.array([self.orbit[:, np.round(np.linspace(i, i+len(self.orbit[0]) - 1, n_sc + 1)).astype(int) % len(self.orbit[0])] for i in np.linspace(0, len(self.orbit[0])-1, n_pos)])

        SC_varied = np.array([self.orbit[:,
                              np.round(np.linspace(i, i + len(self.orbit[0]) - 1, n_sat + 1)).astype(int) % len(
                                  self.orbit[0])] for i in np.linspace(0, len(self.orbit[0]) - 1, n_pos)])[:, :, :-1]

        '''for i in SC_varied:
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
        '''
        return SC_varied

    def animate_plot(self):
        SC_varied = self.vary_sc()
        frames = [go.Frame(data=[go.Scatter3d(x=i[0],y = i[1],z = i[2],visible = True,connectgaps=False,mode="markers",marker=dict(size=3, color="black",))]) for i in SC_varied]
        print(frames)
        self.plot_moon()
        self.fig.frames = frames

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

    def plot_angle(self):
        # Z plot
        line_plot(x_data=sec2hrs(self.t_array), y_data=self.angles_z,labels=['Pointing angle vs time'],
                  x_title=r'$\text{{{}}} t\;[hrs] $'.format('Time from periapsis '),
                  y_title=r'$\text{{{}}} \theta_z\;[deg] $'.format('Pointing angle '))
        line_plot(x_data=sec2hrs(self.t_array), y_data=self.d_angles_z,labels=['Pointing angular velocity vs time'],
                  x_title=r'$\text{{{}}} t\;[hrs] $'.format('Time from periapsis '),
                  y_title=r'$\text{{{}}} \omega_z\;[deg/s] $'.format('Pointing angular velocity '))
        line_plot(x_data=sec2hrs(self.t_array), y_data=self.dd_angles_z, labels=['Pointing angular acceleration vs time'],
                  x_title=r'$\text{{{}}} t\;[hrs] $'.format('Time from periapsis '),
                  y_title=r'$\text{{{}}} \alpha_z\;[deg/s^2] $'.format('Pointing angular acceleration '))
        
        # X plot
        line_plot(x_data=sec2hrs(self.t_array), y_data=self.angles_x, labels=['Pointing angle vs time'],
                  x_title=r'$\text{{{}}} t\;[hrs] $'.format('Time from periapsis '),
                  y_title=r'$\text{{{}}} \theta_x\;[deg] $'.format('Pointing angle '))
        line_plot(x_data=sec2hrs(self.t_array), y_data=self.d_angles_x, labels=['Pointing angular velocity vs time'],
                  x_title=r'$\text{{{}}} t\;[hrs] $'.format('Time from periapsis '),
                  y_title=r'$\text{{{}}} \omega_x\;[deg/s] $'.format('Pointing angular velocity '))
        line_plot(x_data=sec2hrs(self.t_array), y_data=self.dd_angles_x, labels=['Pointing angular acceleration vs time'],
                  x_title=r'$\text{{{}}} t\;[hrs] $'.format('Time from periapsis '),
                  y_title=r'$\text{{{}}} \alpha_x\;[deg/s^2] $'.format('Pointing angular acceleration '))

    def plot_eta_d(self):
        line_plot(x_data=sec2hrs(self.t_array[self.trans_idx]), y_data=self.eta_d, labels=['Beam dilution factor vs transmission time'],
                  x_title=r'$\text{{{}}} t\;[hrs] $'.format('Time from periapsis '),
                  y_title=r'$\text{{{}}} f_bd\;[-] $'.format('Beam dilution factor '))

    def plot_d_rec(self):
        line_plot(x_data=sec2hrs(self.t_array[self.trans_idx]), y_data=self.D_rec_range, labels=['Required receiver diameter vs transmission time'],
                  x_title=r'$\text{{{}}} t\;[hrs] $'.format('Time from periapsis '),
                  y_title=r'$\text{{{}}} D_rec\;[m] $'.format('Required receiver diameter '))

    def plot_all(self):
        self.plot_moon()
        self.plot_cone()
        self.plot_umbra()
        self.plot_orbit()
        # self.plot_sc()
        # self.plot_rec()

    def show(self):
        self.fig.show()
