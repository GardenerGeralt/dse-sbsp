import numpy as np
from scipy.optimize import fsolve

MOON_RADIUS = 1737.4e3              # [m]
MOON_GRAV_PARAM = 4.90486959e12     # [m^3/s^2]


def sec2hrs(value):
    return value / 3600


def percentage(part, total):
    return part / total * 100


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
        self.view_time = self.calc_view_time()
        self.view_altitude = self.calc_view_altitude()
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

    def _calc_view_angle(self):
        semi_latus_rectum = self.semi_maj_ax * (1 - self.eccentricity ** 2)
        semi_minor_axis = np.sqrt(self.semi_maj_ax * semi_latus_rectum)
        orb_center_distance = self.semi_maj_ax * self.eccentricity - MOON_RADIUS
        horizon_distance = semi_minor_axis * np.sqrt(1 - (orb_center_distance / self.semi_maj_ax) ** 2)
        return np.pi - np.arctan2(horizon_distance, MOON_RADIUS)

    def _calc_half_eclipse_time(self):
        view_angle = self._calc_view_angle()
        eccentric_anomaly = 2 * np.arctan2(np.sqrt((1 - self.eccentricity)) * np.tan(view_angle / 2),
                                           np.sqrt(1 + self.eccentricity))
        if eccentric_anomaly < 0:
            E0 = 2 * np.arctan2(np.sqrt((1 - self.eccentricity)) * np.tan(np.pi / 2), np.sqrt(1 + self.eccentricity))
            eccentric_anomaly = 2 * E0 + eccentric_anomaly
        mean_anomaly = eccentric_anomaly - self.eccentricity * np.sin(eccentric_anomaly)
        return mean_anomaly / (2 * np.pi) * self.period

    def calc_view_time(self):
        half_eclipse_time = self._calc_half_eclipse_time()
        return self.period - 2 * half_eclipse_time

    def calc_view_altitude(self, resolution=100):
        half_eclipse_time = self._calc_half_eclipse_time()
        times_in_view = np.arange(half_eclipse_time, (self.period - half_eclipse_time) + resolution, resolution)
        alts_in_view = np.zeros(np.shape(times_in_view))
        for i in range(len(times_in_view)):
            time_point = times_in_view[i]
            mean_anomaly = time_point / self.period * 2 * np.pi
            eccentric_anomaly = fsolve(lambda E: E - self.eccentricity * np.sin(E) - mean_anomaly, mean_anomaly)[0]
            theta = 2 * np.arctan2(np.tan(eccentric_anomaly / 2),
                                   np.sqrt((1 - self.eccentricity) / (1 + self.eccentricity)))
            alts_in_view[i] = self.semi_maj_ax * (1 - self.eccentricity ** 2) / (1 + self.eccentricity * np.cos(theta)) - MOON_RADIUS
        return np.average(alts_in_view)

    def calc_eclipse(self):
        phi = np.arcsin(MOON_RADIUS / self.semi_maj_ax)
        return phi / np.pi * self.period


class OrbitFromPeri(Orbit):
    def __init__(self, pericenter, eccentricity, inclination, name="Orbit"):
        self.pericenter = pericenter
        self.eccentricity = eccentricity
        self.semi_maj_ax = self._calc_semi_maj_ax()
        self.apocenter = self._calc_apocenter()

        super().__init__(self.semi_maj_ax, self.pericenter, self.apocenter, self.eccentricity, inclination, name)

    def _calc_semi_maj_ax(self):
        return (MOON_RADIUS + self.pericenter) / (1 - self.eccentricity)

    def _calc_apocenter(self):
        return self.semi_maj_ax * (1 + self.eccentricity) - MOON_RADIUS


class OrbitFromApo(Orbit):
    def __init__(self, apocenter, eccentricity, inclination, name="Orbit"):
        self.apocenter = apocenter
        self.eccentricity = eccentricity
        self.semi_maj_ax = self._calc_semi_maj_ax()
        self.pericenter = self._calc_pericenter()

        super().__init__(self.semi_maj_ax, self.pericenter, self.apocenter, self.eccentricity, inclination, name)

    def _calc_semi_maj_ax(self):
        return (MOON_RADIUS + self.apocenter) / (1 + self.eccentricity)

    def _calc_pericenter(self):
        return self.semi_maj_ax * (1 - self.eccentricity) - MOON_RADIUS
