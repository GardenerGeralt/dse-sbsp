from numpy import pi, sqrt, tan, exp


class Laser:
    def __init__(self, dcrf_eff=0.33, wavelength=800e-9, w0=0.1, m2=3, P_0=500, z=100000):
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
        self.flux_0 = self.P_0/(self.w0**2*pi)
        self.flux_z = self.calc_flux_dens_z()

    def __str__(self, ):
        return f"\nLaser:\n" \
               f"------------------\n" \
               f"    Laser wavelength : {self.wavelength * 10 ** 9} [nm],\n" \
               f"    Beam quality factor M**2 : {self.m2} [-],\n" \
               f"    Distance to receiver : {self.z} [m],\n" \
               f"    Minimum beam width (close to transmitter) : {self.w0} [m],\n" \
               f"    Minimum beam area (close to transmitter) : {self.w0**2*pi} [m^2],\n" \
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
        return 2 * self.m2 * self.wavelength / (pi * self.w0)

    def calc_beam_width(self):
        """
        Returns:
            w(z): width of beam at certain z [m]
        """
        # according to https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7885601:
        return self.w0 * sqrt(1 + (self.wavelength * self.z / (pi * self.w0 ** 2)) ** 2)

    def calc_area_z(self):
        """
        Returns:
            A(z): beam area at certain z [m^2]
        """
        return pi * self.calc_beam_width() ** 2

    def calc_flux_dens_z(self):
        """
        Returns:
            F(z): flux density at certain z [W/m^2]
        """
        return self.P_0 / self.calc_area_z()


class Microwave:
    def __init__(self):
        ...
