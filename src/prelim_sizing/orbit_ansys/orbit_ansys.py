import numpy as np

MOON_RADIUS = 1737.4e3              # [m]
MOON_GRAV_PARAM = 4.90486959e12     # [m^3/s^2]


def sec2hrs(value):
    return value / 3600

def percentage(value1, value2):
    return value1 / value2 * 100

def m2km(value):
    return value/1000


class Orbit:
    def __init__(self, semi_maj_ax, pericenter, apocenter, eccentricity, inclination, name="Orbit"):
        """
        :param semi_maj_ax: orbit semi-major axis [m]
        :param eccentricity: orbit eccentricity [-]
        :param inclination: orbit inclination [deg]
        :param name: name of the orbit
        """
        self.semi_maj_ax = semi_maj_ax
        self.pericenter = pericenter
        self.apocenter = apocenter
        self.eccentricity = eccentricity
        self.inclination = inclination
        self.name = name

        self.period = self.calc_period()
        self.view_time, self.view_altitude = self.calc_view()
        self.eclipse_time = self.calc_eclipse()

    def __str__(self):
        return f"\n{self.name}:\n" \
               f"------------------\n" \
               f"           Semi-major axis: {m2km(self.semi_maj_ax):.2f} [km],\n" \
               f"           Eccentricity: {self.eccentricity} [-],\n" \
               f"           Inclination: {self.inclination} [deg],\n" \
               f"           Pericenter altitude: {m2km(self.pericenter):.2f} [km],\n" \
               f"           Apocenter altitude: {m2km(self.apocenter):.2f} [km],\n" \
               f"           Orbital period: {sec2hrs(self.period):.3f} [hrs],\n" \
               f"           Time in view: {sec2hrs(self.view_time):.3f} [hrs],\n" \
               f"           Percentage in view: {percentage(self.view_time, self.period):.2f} [%],\n" \
               f"           Average altitude while in view: {m2km(self.view_altitude):.2f} [km].\n" \
               f"           Time without eclipse: {sec2hrs(self.eclipse_time):.3f} [hrs],\n" \
               f"           Percentage without eclipse: {percentage(self.eclipse_time, self.period):.2f} [%]."

    def calc_period(self):
        return 2 * np.pi * np.sqrt(self.semi_maj_ax ** 3 / MOON_GRAV_PARAM)

    def calc_altitude(self):
        h_peri = self.semi_maj_ax * (1 - self.eccentricity) - MOON_RADIUS  # [m]
        h_apo = self.semi_maj_ax * (1 + self.eccentricity) - MOON_RADIUS  # [m]
        return h_peri, h_apo

    def calc_view(self):
        # View angle
        l = self.semi_maj_ax * (1 - self.eccentricity ** 2)
        b = np.sqrt(self.semi_maj_ax * l)
        x = self.semi_maj_ax * self.eccentricity - MOON_RADIUS
        y = b * np.sqrt(1 - (x / self.semi_maj_ax) ** 2)
        theta_v = np.pi - np.arctan2(y, MOON_RADIUS)

        # View time
        E = 2 * np.arctan2(np.sqrt((1 - self.eccentricity)) * np.tan(theta_v / 2), np.sqrt(1 + self.eccentricity))
        if E < 0:
            E0 = 2 * np.arctan2(np.sqrt((1 - self.eccentricity)) * np.tan(np.pi / 2), np.sqrt(1 + self.eccentricity))
            E = 2 * E0 + E
        M = E - self.eccentricity * np.sin(E)
        t = M / (2 * np.pi) * self.period
        view_time = self.period - 2 * t

        # View altitude
        resolution = 100
        t_array = np.arange(round(t), (round(self.period - t) + resolution), resolution)
        h_array = []
        for i in t_array:
            # print(i / T)
            M = i / self.period * 2 * np.pi
            E = 0
            E_new = 0.1
            counter = 0
            while abs(E_new - E) > 0.001:
                E = E_new
                E_new = E - (E - self.eccentricity * np.sin(E) - M) / (1 - self.eccentricity * np.cos(E))
                counter = counter + 1
                if counter > 1000:
                    break
            theta = 2 * np.arctan2(np.tan(E_new / 2), np.sqrt((1 - self.eccentricity) / (1 + self.eccentricity)))
            h_array.append(self.semi_maj_ax * (1 - self.eccentricity ** 2) / (1 + self.eccentricity * np.cos(theta)) - MOON_RADIUS)
        view_altitude = np.average(h_array)
        return view_time, view_altitude

    def calc_eclipse(self):
        phi = np.arcsin(MOON_RADIUS / self.semi_maj_ax)
        return phi / np.pi * self.period


class OrbitFromPeri(Orbit):
    def __init__(self, pericenter, eccentricity, inclination, name="Orbit"):
        self.pericenter = pericenter
        self.eccentricity = eccentricity
        self.semi_maj_ax, self.apocenter = self.calc_distance()

        super().__init__(self.semi_maj_ax, self.pericenter, self.apocenter, self.eccentricity, inclination, name)

    def calc_distance(self):
        semi_maj_ax = (MOON_RADIUS + self.pericenter) / (1 - self.eccentricity)
        apocenter = semi_maj_ax * (1 + self.eccentricity) - MOON_RADIUS
        return semi_maj_ax, apocenter


class OrbitFromApo(Orbit):
    def __init__(self, apocenter, eccentricity, inclination, name="Orbit"):
        self.apocenter = apocenter
        self.eccentricity = eccentricity
        self.semi_maj_ax, self.pericenter = self.calc_distance()

        super().__init__(self.semi_maj_ax, self.pericenter, self.apocenter, self.eccentricity, inclination, name)

    def calc_distance(self):
        semi_maj_ax = (MOON_RADIUS + self.apocenter) / (1 + self.eccentricity)
        pericenter = semi_maj_ax * (1 - self.eccentricity) - MOON_RADIUS
        return semi_maj_ax, pericenter
