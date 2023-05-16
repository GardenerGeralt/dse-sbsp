import pytest
from numpy import pi
from src.prelim_sizing.transmit_ansys import transmit_methods as tm


class TestGeneral:
    def test_db2lin(self):
        assert tm.db2lin(0) == 1
        assert tm.db2lin(60) == 1e6

    def test_calc_wavelength(self):
        assert tm.calc_wavelength(1) == tm.LIGHT_SPEED
        assert tm.calc_wavelength(3e9) == 0.1
        assert tm.calc_wavelength(10e4) == 30000

    def test_circ_area(self):
        assert tm.calc_circ_area(0) == 0
        assert tm.calc_circ_area(10) == pi * 5 ** 2


class TestLaser:
    def test_init(self):
        ...

    def test_calc_beam_div_angle(self):
        ...

    def test_calc_beam_width(self):
        ...

    def test_flux_density(self):
        ...

    def test_calc_power_tx(self):
        ...

    def test_calc_mass_tx(self):
        ...


class TestMicrowave:
    def test_init(self):
        ...

    def test_free_space_loss(self):
        ...

    def test_calc_power_tx(self):
        ...

    def test_calc_mass_tx(self):
        ...

