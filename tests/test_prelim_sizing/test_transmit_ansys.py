import pytest
from src.prelim_sizing.transmit_ansys import transmit_methods as tm


class TestGeneral:
    def test_db2lin(self):
        ...

    def test_calc_wavelength(self):
        ...

    def test_circ_area(self):
        ...


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

