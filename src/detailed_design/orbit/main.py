from orbitfull import Orbit, OrbitPlot
from orbit_params import *
from orbit_func import *
import pickle
from src.plotting.plots import line_plot
from graphs import six_plots
import numpy as np
from scipy.interpolate import CubicSpline

if __name__ == "__main__":
    #orb = Orbit(*orbpar)
    orbplot = OrbitPlot(orbpar)
    # orbplot.plot_angle()
    # orbplot.plot_eta_d()
    # orbplot.plot_d_rec()
    orbplot.plot_all()

    orbplot.vary_sc()
    # orbplot.add_slider()
    orbplot.animate_plot()
    orbplot.fig.data = orbplot.fig.data[::-1]
    orbplot.fig.update(layout_coloraxis_showscale=False)

    orbplot.show()

    #Orbit optimisation
    # RAAN = 0
    # AOP = deg2rad(90)
    #
    # data = []
    # for i in range(len(SMA_range)):
    #     for j in range(len(ECC_range)):
    #         print(str(round(100*(i/len(SMA_range) + j/len(ECC_range)/100),2))+"%")
    #
    #         if ((SMA_range[i] * (1 - ECC_range[j]) - R_M) < lim_down) or ((SMA_range[i] * (1 + ECC_range[j]) - R_M) > lim_up):
    #             continue
    #
    #         orbpar = [SMA_range[i], ECC_range[j], INC_range[j], RAAN, AOP]
    #         orbplot = OrbitPlot(orbpar)
    #
    #         if (orbplot.eff > 0) and (orbplot.alt_max < lim_trans):
    #             data.append([orbplot.eff, orbplot.trans_frac, orbplot.inc_eff, orbplot.alt_max, orbplot.D_rec, orbplot.max_eclipse_time, SMA_range[i] ,ECC_range[j] ,INC_range[j]])
    # data_sorted = sorted(data, key=lambda x : x[0],reverse=False)
    # pickle.dump(data_sorted, open("optimisation.p", 'wb'))

    # #GMAT min-max
    # data = []
    # for i in range(len(SMA_range)):
    #     print(str(round(100*(i/len(SMA_range))))+"%")
    #
    #     orbpar = [SMA_range[i], ECC_range[i], INC_range[i], 0, AOP_range[i]]
    #     orbplot = OrbitPlot(orbpar)
    #     data.append([orbplot.alt_max, orbplot.eff, orbplot.trans_frac, orbplot.cos_transmit, SMA_range[i] ,ECC_range[i] ,INC_range[i]])
    #
    # data_sorted = sorted(data, key=itemgetter(1), reverse=False)
    # print(data_sorted)

    # # #GMAT min-max
    # length = len(SMA_range)
    # data = []
    # for i in range(length):
    #     print(str(round(100*(i/length),2))+"%")
    #
    #     orbpar = [SMA_range[i], ECC_range[i], INC_range[i], 0, AOP_range[i]]
    #     orbplot = OrbitPlot(orbpar)
    #     data.append([[SMA_range[i], ECC_range[i], INC_range[i], AOP_range[i]],
    #                 [orbplot.eff, orbplot.peri, orbplot.apo, orbplot.spacing, orbplot.T, orbplot.t_transmit, orbplot.trans_perc, orbplot.sat_in_view, orbplot.theta_inc, orbplot.cos_transmit, orbplot.inc_eff, orbplot.alt_min, orbplot.alt_max, orbplot.alt_transmit, orbplot.alt_avg],
    #                 [orbplot.z_min, orbplot.z_max, orbplot.vel_z, orbplot.acc_z, orbplot.x_min, orbplot.x_max, orbplot.vel_x, orbplot.acc_x],
    #                 [orbplot.f_bd, orbplot.D_rec, orbplot.max_eclipse_time, orbplot.max_eclipse_velocity]])
    # #data = sorted(data, key=lambda x : x[0][0],reverse=True)[0]
    # pickle.dump(data,open("orbit_data_7.p", 'wb'))

    # print("Minimum spacing: "+str(sorted(data, key=lambda x : x[1][3],reverse=False)[0][1][3]))
    # print("Minimum number of S/C in view: "+str(sorted(data, key=lambda x : x[1][7],reverse=False)[0][1][7]))

    # Optimisation Monte Carlo
    # SD = 0.1
    # res = 20
    # # lim_up = np.random.normal(lim_up, SD*lim_up, res)
    # # lim_down = np.random.normal(lim_down, SD*lim_down, res)
    # lim_trans = np.linspace(500, 20000, res)
    # INC_range = deg2rad(np.linspace(110, 140.75, 50))
    # ECC_range = np.sqrt(1 - 5 / 3 * np.cos(INC_range) ** 2)
    # SMA_range = np.linspace(R_M + lim_down, R_M + lim_up, 50)
    #
    # data = []
    #
    # for i in range(res):
    #     score = 0
    #     params = []
    #
    #     for j in range(len(SMA_range)):
    #         for k in range(len(ECC_range)):
    #             print(str(round(100*(j/len(SMA_range) + k/len(ECC_range)/100),2))+"%")
    #             # print(SMA_range[j],ECC_range[k])
    #
    #             if ((SMA_range[j] * (1 - ECC_range[k]) - R_M) < lim_down) or ((SMA_range[j] * (1 + ECC_range[k]) - R_M) > lim_up):
    #                 continue
    #
    #             orbpar = [SMA_range[j], ECC_range[k], INC_range[k], 0, np.pi/2]
    #             orbplot = OrbitPlot(orbpar)
    #
    #             if (orbplot.eff > 0) and (orbplot.alt_max < lim_trans[i]):
    #                 if orbplot.eff >= score:
    #                     score = orbplot.eff
    #                     params = [SMA_range[j], ECC_range[k], INC_range[k]]
    #     params.insert(0, score)
    #     data.append(params)

    # #Laser pickle
    # # z:      1379 - avg - 1831
    # # z_d:    1611 - avg - 3717
    # # z_dd:   1843 - avg - 2922
    # #
    # # x:      3470 - avg - 1845
    # # x_d:    2508 - avg - 1286
    # # x_dd:   2508 - avg - 1285
    #
    # indices = [1379, 1831, 1611, 3717, 1843, 2922, 3470, 1845, 2508, 1286, 2508, 1285]
    # data = []
    #
    # orbpar = [8930.433254724203, 0.7084911987073012, 0.9903587297841806, 0, 1.5710584962224825]
    # orbplot = OrbitPlot(orbpar)
    # laserdata = [np.flip(orbplot.angles_z), np.flip(orbplot.angles_x),
    #              np.flip(orbplot.d_angles_z), np.flip(orbplot.d_angles_x),
    #              np.flip(orbplot.dd_angles_z), np.flip(orbplot.dd_angles_x)]
    # data.append(laserdata)
    #
    # for i in range(len(indices)):
    #     orbpar = SMA_range[indices[i]], ECC_range[indices[i]], INC_range[indices[i]], RAAN, AOP_range[indices[i]]
    #     orbplot = OrbitPlot(orbpar)
    #     laserdata = [np.flip(orbplot.angles_z), np.flip(orbplot.angles_x),
    #                  np.flip(orbplot.d_angles_z), np.flip(orbplot.d_angles_x),
    #                  np.flip(orbplot.dd_angles_z), np.flip(orbplot.dd_angles_x)]
    #     data.append(laserdata)
    #
    # x_data = sec2hrs(orbplot.t_array) * np.ones(shape=(6,1))
    #
    # y_data = np.array([[data[0][0],data[1][0],data[2][0]], [data[0][1],data[3][1],data[4][1]],
    #                   [data[0][2],data[5][2],data[6][2]], [data[0][3],data[7][3],data[8][3]],
    #                   [data[0][4],data[9][4],data[10][4]], [data[0][5],data[11][5],data[12][5]]])
    #
    # x_titles = [r'$\text{{{}}} t\;[hrs] $'.format('Time from periapsis '),
    #             r'$\text{{{}}} t\;[hrs] $'.format('Time from periapsis '),
    #             r'$\text{{{}}} t\;[hrs] $'.format('Time from periapsis '),
    #             r'$\text{{{}}} t\;[hrs] $'.format('Time from periapsis '),
    #             r'$\text{{{}}} t\;[hrs] $'.format('Time from periapsis '),
    #             r'$\text{{{}}} t\;[hrs] $'.format('Time from periapsis ')]
    # y_titles = [r'$\text{{{}}} \theta_z\;[deg] $'.format('Pointing angle '),
    #             r'$\text{{{}}} \theta_x\;[deg] $'.format('Pointing angle '),
    #             r'$\text{{{}}} \omega_z\;[deg/s] $'.format('Angular velocity '),
    #             r'$\text{{{}}} \omega_x\;[deg/s] $'.format('Angular velocity '),
    #             r'$\text{{{}}} \alpha_z\;[deg/s^2] $'.format('Angular acceleration '),
    #             r'$\text{{{}}} \alpha_x\;[deg/s^2] $'.format('Angular acceleration ')]
    #
    # six_plots(x_data=x_data,
    #           y_data=y_data,
    #           x_titles=x_titles,
    #           y_titles=y_titles)

    # # Altitude BC plot
    # lim_trans = np.linspace(500, 20000, 20)
    # orb_score = np.array([0, 0, 0, 0, 0.2481, 0.3547, 0.4656, 0.5251, 0.5623, 0.6223, 0.641, 0.6711, 0.7014, 0.7129, 0.728, 0.7509, 0.7624, 0.7739, 0.7854, 0.7932])
    # # orb_score_spline = CubicSpline(lim_trans, orb_score)
    # a = np.polyfit(lim_trans[3:], orb_score[3:], deg=5)
    # b = np.poly1d(a)
    # orb_score = np.concatenate((orb_score[:3],b(lim_trans[3:])))
    #
    # line_plot(
    #     x_data=lim_trans,
    #     y_data=orb_score*100,
    #     x_title=r'$\text{{{}}} h_t\;[km] $'.format('Max. transmission altitude BC '),
    #     y_title=r'$\text{{{}}} \;[-] $'.format('Orbit efficiency score '))


