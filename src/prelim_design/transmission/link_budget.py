import numpy as np

def convert_dB(x):
    return 10 * np.log10(x)
def calc_wavelength(f):
    c = 3e8
    return c / f
def calc_a(R,h):
    return R + h
def calc_G_trans(D_transmitter, f):
    return 20 * np.log10(D_transmitter) + 20 * np.log10(f/1e9) + 17.8
def calc_G_rec(eta_trans, D_receiver, wavelength):
    return 10 * np.log10(eta_trans * (np.pi * D_receiver) ** 2 / wavelength ** 2)
def calc_alpha_12(f, D):
    return 21 / (f * D)
def calc_L_atm(f):
    f = f / (1e9)
    return -(6E-8 * f ** 6 - 3E-6 * f ** 5 + 4E-5 * f ** 4 - 0.0002 * f ** 3 - 0.0003 * f ** 2 + 0.0065 * f + 0.0233)
def calc_L_pr(alpha_transmitter, e_t):
    return -12 * (e_t / alpha_transmitter) ** 2 - 12 * (0.1) ** 2
def calc_L_s(wavelength, S):
    return (wavelength / (4 * np.pi * S)) ** 2
def calc_EB_over_N0(P_trans, L_trans, L_atm, G_receiver, G_transmitter, L_s, L_pr, L_rec, k_b, T_sys, R_req):
    return P_trans + L_trans + L_atm + G_transmitter + G_receiver+ L_s + L_pr + L_rec - k_b - T_sys - R_req
def calc_margin(EB_over_N0, E_over_B_req):
    return EB_over_N0 - E_over_B_req

class LinkBudget:
    def __init__(self, P_trans_sc, P_trans_gs, L_trans, L_rec, f_dl, TAR, D_sc, D_gs, e_t,
                 R_up, stored_data, t_contact, SNR_req):
        """
        :param P_trans_sc: Spacecraft communication subsystem power [W]
        :param P_trans_gs: Groundstation communication power [W]
        :param L_trans: Transmitter losses [-]
        :param L_rec: Receiver losses [-]
        :param f_dl: Downlink frequency [GHz]
        :param TAR: Turn-Around-Ratio (uplink/downlink) [-]
        :param D_sc: Spacecraft dish diameter [m]
        :param D_gs: Ground station dish diameter [m]
        :param e_t: Pointing offset angle [deg]
        :param R_up: Uplink data rate [bit/s]
        :param stored_data: data stored over one orbit [bits]
        :param t_contact: contact time with Earth [s]
        :param SNR_req: Required Signal-to-Noise Ratio (based on coding and BER) [dB]
        """
        #Note to self: we use X-band (8.5GHz) and a 35m diameter gs antenna at 20kW (or 2000 like the adsee assignments
        #,just use TAR = 749/880
        #Asssume each storage element = 8 bytes ->

        """Inputs"""
        self.P_trans_sc = P_trans_sc
        self.P_trans_gs = P_trans_gs
        self.L_trans = L_trans
        self.L_rec = L_rec
        self.f_dl = f_dl * 1e9 #converting to Hz
        self.TAR = TAR
        self.D_sc = D_sc
        self.D_gs = D_gs
        #self.alt = alt
        self.e_t = e_t
        self.R_up = R_up
        self.stored_data = stored_data
        self.t_contact = t_contact
        self.SNR_req = SNR_req

        "Constants"
        self.g = 9.81 #m/s^2
        self.G = 6.67430e-11 # m^3/kgs^2
        self.T_0 = 290  # K
        self.c = 3e8  # m/s
        self.k_b = 1.38064852e-23  # m^2*kg/s^2*K
        self.E_over_B_req = 10.5  # dB
        self.AU = 1.495978707e11  # m
        self.T_sys_up = 614  # K
        self.T_sys_down = 135  # K
        self.eta_trans = 0.55
        self.R_moon = 1738000  # m
        self.mu_moon = 4.9048695e12  # m^3/s^2
        self.distance_moon = 384403000  # m

        """General"""
        self.L_trans_dB = convert_dB(self.L_trans)
        self.L_rec_dB = convert_dB(self.L_rec)
        self.k_b_dB = convert_dB(self.k_b)
        self.distance = self.calculate_distance()

        """Uplink"""
        self.f_ul = self.calc_f_ul()
        self.wavelength_up = calc_wavelength(self.f_ul)
        self.T_sys_up_dB = convert_dB(self.T_sys_up)
        self.G_receiver_up = calc_G_rec(self.eta_trans, self.D_sc, self.wavelength_up)
        self.G_transmitter_up = calc_G_trans(self.D_gs, self.f_ul)
        self.L_atm_up = calc_L_atm(self.f_ul)
        self.L_space_up = convert_dB(calc_L_s(self.wavelength_up, self.distance))
        self.P_up = convert_dB(self.P_trans_gs)
        self.alpha_up_gs = calc_alpha_12(self.f_ul/1e9, self.D_gs)
        self.alpha_up_sc = calc_alpha_12(self.f_ul/1e9, self.D_sc)
        self.L_pr_up = calc_L_pr(self.alpha_up_sc, self.e_t)
        self.R_up_dB = convert_dB(self.R_up)
        self.Eb_over_N0_up = calc_EB_over_N0(self.P_up, self.L_trans_dB, self.L_atm_up, self.G_receiver_up,
                                             self.G_transmitter_up,self.L_space_up, self.L_pr_up, self.L_rec_dB,
                                             self.k_b_dB, self.T_sys_up_dB, self.R_up_dB)
        self.margin_up = calc_margin(self.Eb_over_N0_up, self.SNR_req)

        """Downlink"""
        self.R_down = self.calculate_R_down()
        self.wavelength_dl = calc_wavelength(self.f_dl)
        self.T_sys_down_dB = convert_dB(self.T_sys_down)
        self.G_receiver_down = calc_G_rec(self.eta_trans, self.D_gs, self.wavelength_dl)
        self.G_transmitter_down = calc_G_trans(self.D_sc, self.f_dl)
        self.L_atm_down = calc_L_atm(self.f_dl)
        self.L_space_down = convert_dB(calc_L_s(self.wavelength_dl, self.distance))
        self.P_down = convert_dB(self.P_trans_sc)
        self.alpha_down_gs = calc_alpha_12(self.f_dl/1e9, self.D_gs)
        self.alpha_down_sc = calc_alpha_12(self.f_dl/1e9, self.D_sc)
        self.L_pr_down = calc_L_pr(self.alpha_down_sc, self.e_t)
        self.R_down_dB = convert_dB(self.R_down)
        self.Eb_over_N0_down = calc_EB_over_N0(self.P_down, self.L_trans_dB, self.L_atm_down, self.G_receiver_down,
                                             self.G_transmitter_down, self.L_space_down, self.L_pr_down, self.L_rec_dB,
                                             self.k_b_dB, self.T_sys_down_dB, self.R_down_dB)
        self.margin_down = calc_margin(self.Eb_over_N0_down, self.SNR_req)


    def calculate_distance(self):
        return np.sqrt((self.R_moon + self.distance_moon) ** 2 - self.R_moon ** 2)

    """Calculations specific for uplink"""
    def calc_f_ul(self):
        return self.TAR * self.f_dl

    """Calculations specific for downlink"""
    def calculate_R_down(self):
        #return self.stored_data / self.t_contact
        return 8e6