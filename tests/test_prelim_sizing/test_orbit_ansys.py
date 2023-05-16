import pytest
import numpy as np
from src.prelim_sizing.orbit_ansys import orbit_ansys as oa


class TestGeneral:
    def test_sec2hrs(self):
        assert oa.sec2hrs(3600) == 1
        assert oa.sec2hrs(7200) == 2
        assert oa.sec2hrs(0) == 0
        assert oa.sec2hrs(-3600 * 24) == -24

    def test_percentage(self):
        assert oa.percentage(0.5, 100) == 50
        assert oa.percentage(0.5, 50) == 25
        assert oa.percentage(0.5, 0) == 0
        assert oa.percentage(0.5, -100) == -50


class TestOrbit:
    test_orbit = oa.Orbit(..., 750000, ..., 0.5, 47.87, name="Test Orbit")

    def test_init(self):
        assert self.test_orbit.semi_maj_ax == ...
        assert self.test_orbit.pericenter == 750000
        assert self.test_orbit.apocenter == ...
        assert self.test_orbit.eccentricity == 0.5
        assert self.test_orbit.inclination == 47.87
        assert self.test_orbit.name == "Test Orbit"

    def test_calc_period(self):
        assert np.isclose(self.test_orbit.calc_period(), ...)

    def test_calc_altitude(self):
        assert np.isclose(self.test_orbit.calc_altitude(), ...)

    def test_calc_view_angle(self):
        assert np.isclose(self.test_orbit._calc_view_angle(), ...)

    def test_calc_half_eclipse_time(self):
        assert np.isclose(self.test_orbit._calc_half_eclipse_time(), ...)

    def test_calc_view_time(self):
        assert np.isclose(self.test_orbit.calc_view_time(), ...)

    def test_calc_view_altitude(self):
        assert np.isclose(self.test_orbit.calc_view_altitude(), ...)

    def test_calc_eclipse(self):
        assert np.isclose(self.test_orbit.calc_eclipse(), ...)


class TestOrbitFromPeri:
    test_orbit = oa.OrbitFromPeri(750000, 0.5, 47.87, name="Test Orbit")

    def test_init(self):
        assert self.test_orbit.pericenter == 750000
        assert self.test_orbit.eccentricity == 0.5
        assert self.test_orbit.inclination == 47.87
        assert self.test_orbit.name == "Test Orbit"

    def test_calc_semi_maj_ax(self):
        assert np.isclose(self.test_orbit._calc_semi_maj_ax(), ...)

    def test_calc_apocenter(self):
        assert np.isclose(self.test_orbit._calc_apocenter(), ...)


class TestOrbitFromApo:
    test_orbit = oa.OrbitFromApo(..., 0.5, 47.87, name="Test Orbit")

    def test_init(self):
        assert self.test_orbit.apocenter == ...
        assert self.test_orbit.eccentricity == 0.5
        assert self.test_orbit.inclination == 47.87
        assert self.test_orbit.name == "Test Orbit"

    def test_calc_semi_maj_ax(self):
        assert np.isclose(self.test_orbit._calc_semi_maj_ax(), ...)

    def test_calc_pericenter(self):
        assert np.isclose(self.test_orbit._calc_pericenter(), ...)
