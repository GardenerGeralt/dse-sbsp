from orbitfull import Orbit, OrbitPlot
from orbit_params import *
import pickle
import numpy as np

if __name__ == "__main__":
    #orb = Orbit(*orbpar)
    orbplot = OrbitPlot(orbpar)
    # orbplot.plot_angle()
    # orbplot.plot_eta_d()
    # orbplot.plot_d_rec()
    orbplot.plot_all()

    # orbplot.vary_sc()
    # # orbplot.add_slider()
    # orbplot.animate_plot()
    # orbplot.fig.data = orbplot.fig.data[::-1]
    # orbplot.fig.update(layout_coloraxis_showscale=False)

    orbplot.show()

    #Orbit optimisation
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
    #             data.append([orbplot.eff, orbplot.trans_frac, orbplot.inc_eff, orbplot.alt_max, SMA_range[i] ,ECC_range[j] ,INC_range[j]])
    # data_sorted = sorted(data, key=lambda x : x[0],reverse=True)[0]

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

    #Optimisation Monte Carlo
    # SD = 0.1
    # res = 2
    # # lim_up = np.random.normal(lim_up, SD*lim_up, res)
    # # lim_down = np.random.normal(lim_down, SD*lim_down, res)
    # INC_range = deg2rad(np.linspace(110, 140.75, 100))
    # ECC_range = np.sqrt(1 - 5 / 3 * np.cos(INC_range) ** 2)
    #
    # data = []
    # for i in range(res):
    #     SMA_range = np.linspace(R_M + lim_down, R_M + lim_up, 100)
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
    #             if (orbplot.eff > 0) and (orbplot.alt_max < lim_trans):
    #                 if orbplot.eff >= score:
    #                     score = orbplot.eff
    #                     params = [SMA_range[j], ECC_range[k]]
    #     params.insert(0, score)
    #     data.append(params)



