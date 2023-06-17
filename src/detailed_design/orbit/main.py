from orbitfull import Orbit, OrbitPlot
from orbit_params import *
from operator import itemgetter
import pickle

if __name__ == "__main__":
    #orb = Orbit(*orbpar)
    orbplot = OrbitPlot(orbpar)
    #orbplot.plot_angle()
    # orbplot.plot_eta_d()
    # orbplot.plot_d_rec()
    orbplot.plot_all()

    # orbplot.vary_sc()
    # orbplot.add_slider()
    # orbplot.animate_plot()
    # #print(len(orbplot.fig.data))
    #orbplot.show()

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
    #         if (orbplot.eff > 0) and (orbplot.alt_max < 14150):
    #             data.append([orbplot.eff, orbplot.trans_frac, orbplot.cos_transmit, orbplot.alt_max, SMA_range[i] ,ECC_range[j] ,INC_range[j]])
    # data_sorted = sorted(data, key=itemgetter(0), reverse=True)

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

    # #GMAT min-max
    # length = len(SMA_range)
    # data = []
    # for i in range(length):
    #     print(str(round(100*(i/length),3))+"%")
    #
    #     orbpar = [SMA_range[i], ECC_range[i], INC_range[i], 0, AOP_range[i]]
    #     orbplot = OrbitPlot(orbpar)
    #     data.append([[SMA_range[i], ECC_range[i], INC_range[i], AOP_range[i]],
    #                 [orbplot.eff, orbplot.peri, orbplot.apo, orbplot.spacing, orbplot.T, orbplot.t_transmit, orbplot.trans_perc, orbplot.sat_in_view, orbplot.theta_inc, orbplot.cos_transmit, orbplot.alt_min, orbplot.alt_max, orbplot.alt_transmit],
    #                 [orbplot.z_min, orbplot.z_max, orbplot.vel_z, orbplot.acc_z, orbplot.x_min, orbplot.x_max, orbplot.vel_x, orbplot.acc_x],
    #                 [orbplot.f_bd, orbplot.D_rec, orbplot.max_eclipse_time, orbplot.max_eclipse_velocity]])
    #
    # pickle.dump(data,open("orbit_data_2.p", 'wb'))