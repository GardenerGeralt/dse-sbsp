import numpy as np
class LinkBudget:
    def __init__(self, P_trans_sc, P_trans_gs, L_trans, L_rec, f_dl, TAR, D_sc, D_gs, alt, e_t, R_up, R_down, SNR_req):
        """
        :param P_trans_sc: Spacecraft communication subsystem power [W]
        :param P_trans_gs: Groundstation communication power [W]
        :param L_trans: Transmitter losses [-]
        :param L_rec: Receiver losses [-]
        :param f_dl: Downlink frequency [GHz]
        :param TAR: Turn-Around-Ratio (uplink/downlink) [-]
        :param D_sc: Spacecraft dish diameter [m]
        :param D_gs: Ground station dish diameter [m]
        :param alt: Orbital altitude [km]
        :param e_t: Pointing offset angle [deg]
        :param R_up: Uplink data rate [bit/s]
        :param R_down: Downlink data rate [bit/s]
        :param SNR_req: Required Signal-to-Noise Ratio (based on coding and BER) [dB]
        """

