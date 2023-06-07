import transmit_methods as tm
# from transmit_methods import deg
# from src.plotting import plots as plt
import numpy as np
# from src.prelim_design.orbit import


def main():
    return None


if __name__ == "__main__":
    main()
    NA = 0.22
    div = np.arcsin(0.22)
    print(div*180/np.pi)

    # L = np.arange(10000,100000)
    laser = tm.Laser(3e8/976e-9, 0.43, 0.33, 5.4e-3, 4, 1e3)
    print(laser)
    # laser = tm.Laser(3e8 / 976e-9, 0.43, 0.33, 200e-6, 2, 1e3)
    laser.beam_div_angle = 0.0065*np.pi/180
    print(laser.calc_beam_width(17000))
    # .line_plot(L, laser.flux)
    array = tm.LaserArray(177, 0.055)
    print(array.circ_array())
    # print(array.square_array(0.1))
    array.plot_flat_array(array.circ_array())
    # array.plot_3d_array(array.circ_array())
    # print('Time'+r'$t\;[hours]$')

