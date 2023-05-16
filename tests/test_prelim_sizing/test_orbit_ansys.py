import pytest
from src.prelim_sizing.orbit_ansys import orbit_ansys as oa
from numpy import abs


class TestGeneral:
    def test_sec2hrs(self):
        assert oa.sec2hrs(3600) == 1
        assert oa.sec2hrs(0) == 0

    def test_percentage(self):
        assert oa.percentage(5, 20) == 25
        with pytest.raises(ZeroDivisionError):
            oa.percentage(100, 0)

    def test_m2km(self):
        assert oa.m2km(0) == 0
        assert oa.m2km(1) == 0.001


class TestOrbit:
    test_semi_maj_ax = 1500e3  # [m]
    test_pericenter = 750e3  # [m]
    test_eccentricity = 0.5
    test_apocenter = test_pericenter*(1+test_eccentricity)/(1-test_eccentricity)  # [m]
    test_inclination = 48.46  # [deg]
    test_orbit = oa.Orbit(test_semi_maj_ax, test_pericenter, test_apocenter, test_eccentricity, test_inclination,
                          name="Test Orbit")

    #  Manually calculated values
    test_period = 5211.983408  # [s]
    test_h_peri = test_pericenter - 1737.4e3  # [m], second val is mean volumetric Moon radius
    test_h_apo = test_apocenter - 1737.4e3  # [m], second val is mean volumetric Moon radius

    def test_init(self):
        assert self.test_orbit.semi_maj_ax == self.test_semi_maj_ax
        assert self.test_orbit.h_peri == self.test_pericenter
        assert self.test_orbit.h_apo == self.test_apocenter
        assert self.test_orbit.eccentricity == self.test_eccentricity
        assert self.test_orbit.inclination == self.test_inclination

    def test_calc_period(self):
        assert abs(self.test_orbit.calc_period() - self.test_period)/self.test_orbit.calc_period() < 1e-6

    def test_calc_altitude(self):
        h_peri, h_apo = self.test_orbit.calc_altitude()
        print(h_peri)
        assert abs(h_peri - self.test_h_peri) / h_peri < 1e-6
        assert abs(h_apo - self.test_h_apo) / h_apo < 1e-6

    def test_calc_view(self):
        ...

    def test_calc_eclipse(self):
        ...


class TestOrbitFromPeri:
    def test_init(self):
        ...

    def test_calc_distance(self):
        ...


class TestOrbitFromApo:
    def test_init(self):
        ...

    def test_calc_distance(self):
        ...
