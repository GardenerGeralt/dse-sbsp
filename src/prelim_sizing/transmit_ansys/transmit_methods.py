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


def calc_circ_area(diameter):
    """
    Args:
        diameter: diameter of circle [m]
    Returns:
        area: area of circle [m2]
    """
    return np.pi * (diameter / 2) ** 2


class Laser:
    def __init__(self, freq, eff_tx, eff_rx, min_beam_width, m_squared, spec_mass):
        """
        :param freq: frequency of laser [Hz]
        :param eff_tx: transmitter (DC to RF) efficiency [-]
        :param eff_rx: receiver (RF to DC) efficiency [-]
        :param min_beam_width: minimum beam width, very close to transmitter [m]
        :param m_squared: M squared, the beam quality factor (deg of var from gaussian beam, lower is better)
        :param spec_mass: specific mass of laser [kg/W]
        """
        #  Frequency and wavelength
        self.freq = freq
        self.wavelength = calc_wavelength(freq)
        #  Efficiencies
        self.eff_tx = eff_tx
        self.eff_rx = eff_rx
        # Beam parameters
        self.min_beam_width = min_beam_width
        self.min_beam_area = calc_circ_area(min_beam_width)
        self.m_squared = m_squared
        #  Mass
        self.spec_mass = spec_mass
        #  Calculated parameters
        self.beam_div_angle = self.calc_beam_div_angle()

    def __str__(self, ):
        return f"\nLaser:\n" \
               f"------------------\n" \
               f"       Laser frequency : {self.freq:.4e} [Hz],\n" \
               f"      Laser wavelength : {self.wavelength:.4e} [m],\n" \
               f"Transmitter efficiency : {self.eff_tx} [-],\n" \
               f"   Receiver efficiency : {self.eff_rx} [-],\n" \
               f"    Minimum beam width : {self.min_beam_width:.4e} [m],\n" \
               f"     Minimum beam area : {self.min_beam_area:.4e} [m2],\n" \
               f"             M squared : {self.m_squared} [-],\n" \
               f" Beam divergence angle : {self.beam_div_angle:.4e} [rad]."

    def calc_beam_div_angle(self):
        """
        Returns: full divergence angle theta (NOT HALF)
        """
        return 2 * self.m_squared * self.wavelength / (np.pi * self.min_beam_width)

    def calc_beam_width(self, distance):
        """
        Args:
            distance: distance from transmitter [m]
        Returns:
            w(distance): beam width at certain distance [m]
        """
        # according to https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7885601:
        return self.min_beam_width * np.sqrt(1 + (self.wavelength * distance / (np.pi * self.min_beam_width ** 2)) ** 2)

    def flux_density(self, power_tx, distance):
        """
        Args:
            power_tx: power at transmitter [W]
            distance: distance from transmitter [m]
        Returns:
            S(distance): flux density at certain distance [W/m2]
        """
        return power_tx / calc_circ_area(self.calc_beam_width(distance))

    def calc_power_tx(self, power_rx, distance):
        """
        Args:
            power_rx: power at receiver [W]
            distance: distance from transmitter [m]
        Returns:
            power_tx: power at transmitter [W]
        """
        return power_rx / (self.eff_rx * self.eff_tx)

    def calc_mass_tx(self, power_tx):
        """
        Args:
            power_tx: power at transmitter [W]
        Returns:
            mass_tx: mass of transmitter [kg]
        """
        return power_tx * self.spec_mass


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
        return (self.wavelength / (4 * np.pi * distance)) ** 2

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
