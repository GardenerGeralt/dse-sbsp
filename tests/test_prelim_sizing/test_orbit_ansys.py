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
    r_Moon = 1737.4e3  # [m]
    test_h_peri = 750e3  # [m]
    test_h_apo = 5724.8e3  # [m]
    test_eccentricity = 0.5
    test_inclination = 48.46  # [deg]
    #test_semi_maj_ax = 0.5*(test_h_peri+test_h_apo+2*r_Moon)  # [m]
    test_semi_maj_ax = 4974.8e3  # [m]
    test_orbit = oa.Orbit(test_semi_maj_ax, test_h_peri, test_h_apo, test_eccentricity, test_inclination,
                          name="Test Orbit")

    #  Manually calculated values
    test_period = 31479.62675  # [s]

    def test_init(self):
        assert self.test_orbit.semi_maj_ax == self.test_semi_maj_ax
        assert self.test_orbit.h_peri == self.test_h_peri
        assert self.test_orbit.h_apo == self.test_h_apo
        assert self.test_orbit.eccentricity == self.test_eccentricity
        assert self.test_orbit.inclination == self.test_inclination

    def test_calc_period(self):
        assert abs(self.test_orbit.calc_period() - self.test_period)/self.test_orbit.calc_period() < 1e-6

    def test_calc_altitude(self):
        h_peri, h_apo = self.test_orbit.calc_altitude()
        assert abs(h_peri - self.test_h_peri) / h_peri < 1e-6
        assert abs(h_apo - self.test_h_apo) / h_apo < 1e-6

    def test_calc_view_angle(self):
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
