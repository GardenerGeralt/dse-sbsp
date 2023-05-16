import pytest
from numpy import pi, abs
from src.prelim_sizing.transmit_ansys import transmit_methods as tm


class TestGeneral:
    def test_db2lin(self):
        assert tm.db2lin(0) == 1
        assert tm.db2lin(60) == 1e6

    def test_calc_wavelength(self):
        assert tm.calc_wavelength(1) == tm.LIGHT_SPEED
        assert tm.calc_wavelength(3e9) == 0.1
        assert tm.calc_wavelength(1e4) == 30000

    def test_circ_area(self):
        assert tm.calc_circ_area(0) == 0
        assert tm.calc_circ_area(10) == pi * 5 ** 2


class TestLaser:
    test_laser = tm.Laser(3*10**14, 0.6, 0.4, 0.5, 2, 10)
    test_power_req = 1e6

    def test_init(self):
        assert self.test_laser.freq == 3*10**14
        assert self.test_laser.wavelength == 1000e-9
        assert self.test_laser.eff_tx == 0.6
        assert self.test_laser.eff_rx == 0.4
        assert self.test_laser.min_beam_width == 0.5
        assert self.test_laser.min_beam_area == pi*(0.5/2)**2
        assert self.test_laser.m_squared == 2
        assert self.test_laser.spec_mass == 10

    def test_calc_beam_div_angle(self):
        assert abs(self.test_laser.calc_beam_div_angle() - 2.54647909e-6) < 1e-6

    def test_calc_beam_width(self):
        assert self.test_laser.calc_beam_width(0) == self.test_laser.min_beam_width
        assert abs(self.test_laser.calc_beam_width(1e6) - 0.8094965933) < 1e-6

    def test_flux_density(self):
        assert self.test_laser.flux_density(0, 0) == 0
        assert abs(self.test_laser.flux_density(1e6, 1e6) - 1943032.513) < 1e-3

    def test_calc_power_tx(self):
        assert self.test_laser.calc_power_tx(0, 0) == 0
        assert abs(self.test_laser.calc_power_tx(1e6, 0) - 1e6/0.6/0.4) < 1e-6

    def test_calc_mass_tx(self):
        assert self.test_laser.calc_mass_tx(0) == 0
        assert self.test_laser.calc_mass_tx(1e6) == 1e6*10


class TestMicrowave:
    def test_init(self):
        ...

    def test_free_space_loss(self):
        ...

    def test_calc_power_tx(self):
        ...

    def test_calc_mass_tx(self):
        ...

