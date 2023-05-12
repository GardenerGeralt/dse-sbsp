import numpy as np

LIGHT_SPEED = 3e8   # [m/s]


def db2lin(db):
    """
    Args:
        db: value in dB
    Returns:
        lin: value in linear
    """
    return 10 ** (db / 10)


def calc_wavelength(freq):
    """
    Returns:
        wavelength: wavelength of microwave [m]
    """
    return LIGHT_SPEED / freq


class Laser:
    def __init__(self, dcrf_eff=0.3, wavelength=800e-9, w0=0.1, m2=3, P_0=500, z=100000):
        """
        :param dcrf_eff: DC to RF efficiency [-]
        :param wavelength: wavelength of laser [m]
        :param w0: minimum beam width, very close to transmitter [m]
        :param m2: M squared, the beam quality factor (deg of var from gaussian beam, lower is better)
        :param P_0: beam power just outside transmitter [W]
        :param z: distance from emitter to receiver [m]
        """
        #  Efficiencies
        self.dcrf_eff = dcrf_eff
        #  Input parameters
        self.wavelength = wavelength
        self.w0 = w0
        self.m2 = m2
        self.P_0 = P_0
        self.z = z
        # Calculated parameters
        self.calc_beam_div_angle()
        self.flux_0 = self.P_0/(self.w0**2*np.pi)
        self.flux_z = self.calc_flux_dens_z()

    def __str__(self, ):
        return f"\nLaser:\n" \
               f"------------------\n" \
               f"    Laser wavelength : {self.wavelength * 10 ** 9} [nm],\n" \
               f"    Beam quality factor M**2 : {self.m2} [-],\n" \
               f"    Distance to receiver : {self.z} [m],\n" \
               f"    Minimum beam width (close to transmitter) : {self.w0} [m],\n" \
               f"    Minimum beam area (close to transmitter) : {self.w0**2*np.pi} [m^2],\n" \
               f"    Beam divergence angle (full) : {self.calc_beam_div_angle()} [rad],\n" \
               f"    Beam width at receiver: {self.calc_beam_width()} [m],\n" \
               f"    Beam area at receiver: {self.calc_area_z()} [m^2],\n" \
               f"    Power at transmitter : {self.P_0} [W],\n" \
               f"    Flux density at transmitter : {self.flux_0} [W/m^2],\n" \
               f"    Flux density at receiver : {self.flux_z} [W/m^2],\n"

    def set_z(self, z):
        """
        Args:
            z: Distance to receiver [m]
        Returns:
            nada
        """
        self.z = z

    def calc_beam_div_angle(self):
        """
        Returns: full divergence angle theta (NOT HALF)
        """
        return 2 * self.m2 * self.wavelength / (np.pi * self.w0)

    def calc_beam_width(self):
        """
        Returns:
            w(z): width of beam at certain z [m]
        """
        # according to https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7885601:
        return self.w0 * np.sqrt(1 + (self.wavelength * self.z / (np.pi * self.w0 ** 2)) ** 2)

    def calc_area_z(self):
        """
        Returns:
            A(z): beam area at certain z [m^2]
        """
        return np.pi * self.calc_beam_width() ** 2

    def calc_flux_dens_z(self):
        """
        Returns:
            F(z): flux density at certain z [W/m^2]
        """
        return self.P_0 / self.calc_area_z()


class Microwave:
    def __init__(self, freq, eff_tx, eff_rx, db_gain_tx, db_gain_rx, spec_mass):
        """
        :param freq: frequency of microwave [Hz]
        :param eff_tx: transmitter efficiency [-]
        :param eff_rx: receiver efficiency [-]
        :param db_gain_tx: transmitter gain [dB]
        :param db_gain_rx: receiver gain [dB]
        :param spec_mass: specific mass of transmitter [kg/W]
        """
        #  Frequency and wavelength
        self.freq = freq
        self.wavelength = calc_wavelength(freq)
        #  Efficiencies
        self.eff_tx = eff_tx
        self.eff_rx = eff_rx
        #  Gains
        self.db_gain_tx = db_gain_tx
        self.db_gain_rx = db_gain_rx
        self.gain_tx = db2lin(db_gain_tx)
        self.gain_rx = db2lin(db_gain_rx)
        #  Specific mass
        self.spec_mass = spec_mass

    def __str__(self):
        return f"\nMicrowave:\n" \
               f"------------------\n" \
               f"   Microwave frequency : {self.freq:.4e} [Hz],\n" \
               f"  Microwave wavelength : {self.wavelength:.4e} [m],\n" \
               f"Transmitter efficiency : {self.eff_tx} [-],\n" \
               f"   Receiver efficiency : {self.eff_rx} [-],\n" \
               f"      Transmitter gain : {self.db_gain_tx} [dB],\n" \
               f"         Receiver gain : {self.db_gain_rx} [dB]."

    def free_space_loss(self, distance):
        """
        Args:
            distance: distance between transmitter and receiver [m]
        Returns:
            free space loss: [dB]
        """
        return (4 * np.pi * distance / self.wavelength) ** 2

    def calc_power_tx(self, power_rx, distance):
        """
        Args:
            power_rx: power at receiver [W]
            distance: distance between transmitter and receiver [m]
        Returns:
            power_tx: power at transmitter [W]
        """
        return power_rx / (self.eff_rx * self.gain_rx * self.free_space_loss(distance) * self.gain_tx * self.eff_tx)

    def calc_mass_tx(self, power_tx):
        """
        Args:
            power_tx: power at transmitter [W]
        Returns:
            mass_tx: mass of transmitter [kg]
        """
        return power_tx * self.spec_mass
