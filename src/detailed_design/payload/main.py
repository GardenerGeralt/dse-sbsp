import transmit_methods as tm
# from transmit_methods import deg
# from src.plotting import plots as plt
import numpy as np
# from src.prelim_design.orbit import


def main():
    return None


if __name__ == "__main__":
    freq = 3e8/(976e-9)
    # L = np.arange(10000,100000)
    laser = tm.Laser(freq, 0.43, 1e-6, 5.4e-3, 1.2, 1e3)
    print(laser)
    print(laser.calc_beam_width(18e6))
    # laser = tm.Laser(3e8 / 976e-9, 0.43, 0.33, 200e-6, 2, 1e3)
    # laser.beam_div_angle = 0.0065*np.pi/180
    # print(laser.calc_beam_width(17000))
    # .line_plot(L, laser.flux)
    # array = tm.LaserArray(177, 0.06)
    # print(array.circ_array())
    # print(array.square_array(0.1))
    # array.gaussian_field()
    # array.plot_flat_array(array.circ_array())
    # print(array.module_beam_width)
    # print(array.calc_total_beam_diameter())

    # print(array)
    # print(array.calc_size_rx(816e3, 1.8e-6, 0.4e-6))
    # print(array.calc_pointing_accuracy(18e6, 100, 0.4e-6))
    # print(array.calc_n_modules(1e6, 0.99, 0.99, 0.74, 0.33))
    # array.plot_3d_array(array.circ_array())
    # print('Time'+r'$t\;[hours]$')

