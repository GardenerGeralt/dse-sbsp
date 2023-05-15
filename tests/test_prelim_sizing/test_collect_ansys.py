import pytest

from prelim_sizing.collect_ansys.collect_methods import Concentrator
from src.prelim_sizing.collect_ansys import collect_methods as cm


class TestPhotoCell:
    test_pv_cell = cm.SolarCell(0.30, 3.000e-3, 2.000e-3, 1, 393, name="Test PV Cell")
    test_power_req = 1e6
    correct_area = 2449.179525
    correct_mass = 1632.78635

    def test_init(self):
        assert self.test_pv_cell.eff == 0.30
        assert self.test_pv_cell.cell_area == 3.000e-3
        assert self.test_pv_cell.av_mass == 2.000e-3
        assert self.test_pv_cell.concentration == 1
        assert self.test_pv_cell.op_temp == 393
        assert self.test_pv_cell.power_dens == 408.3
        assert self.test_pv_cell.spec_power == 612.45
        assert self.test_pv_cell.name == "Test PV Cell"

    def test_calc_power_dens(self):
        assert self.test_pv_cell._calc_power_dens() == 408.3

    def test_calc_spec_power(self):
        assert self.test_pv_cell._calc_spec_power() == 612.45

    def test_area(self):
        assert (self.test_pv_cell.size(self.test_power_req)[0] - self.correct_area) / self.correct_area < 1e-6

    def test_mass(self):
        assert (self.test_pv_cell.size(self.test_power_req)[1] - self.correct_mass) / self.correct_mass < 1e-6


class TestConcentrator:
    test_concentrator = cm.Concentrator(0.01, 0.90, "Test Concentrator")
    test_power_ref = 1e6
    correct_area = 816.393175
    correct_mass = 8.16393175

    def test_init(self):
        assert self.test_concentrator.surface_density == 0.01
        assert self.test_concentrator.reflectivity == 0.90
        assert self.test_concentrator.name == "Test Concentrator"

    def test_area(self):
        assert (self.test_concentrator.size(self.test_power_ref)[0] - self.correct_area) / self.correct_area < 1e-6

    def test_mass(self):
        assert (self.test_concentrator.size(self.test_power_ref)[1] - self.correct_mass) / self.correct_mass < 1e-6


class TestRadiator:
    test_rad = cm.Radiator(0.90, 1.000e3, 1.000e-3, "Test Radiator")
    pv_temp = 393
    pv_area = 500
    test_power_abs = 1e6
    correct_area = 330.2353178
    correct_mass = 330.2353178

    def test_init(self):
        assert self.test_rad.emissivity == 0.90
        assert self.test_rad.density == 1.000e3
        assert self.test_rad.thickness == 1.000e-3
        assert self.test_rad.name == "Test Radiator"

    def test_area(self):
        assert (self.test_rad.size(self.test_power_abs, self.pv_temp,
                                   self.pv_area)[0] - self.correct_area) / self.correct_area < 1e-6

    def test_mass(self):
        assert (self.test_rad.size(self.test_power_abs, self.pv_temp,
                                   self.pv_area)[1] - self.correct_mass) / self.correct_mass < 1e-6


class TestCollector:
    test_pv_cell = cm.SolarCell(0.30, 3.000e-3, 2.000e-3, 10, 393, name="Test PV Cell")
    test_concentrator = cm.Concentrator(0.01, 0.90, "Test Concentrator")
    test_rad = cm.Radiator(0.90, 1.000e3, 1.000e-3, "Test Radiator")
    test_collector = cm.Collector(test_pv_cell, test_concentrator, test_rad, "Test Collector")
    test_power_req = 1e6
    correct_total_area = 2721.310583
    correct_total_mass = 1862.649307

    def test_init(self):
        assert self.test_collector.pv_cell == self.test_pv_cell
        assert self.test_collector.concentrator == self.test_concentrator
        assert self.test_collector.radiator == self.test_rad
        assert self.test_collector.name == "Test Collector"

    def test_total_area(self):
        assert (self.test_collector.size(self.test_power_req, total=True)[0] -
                self.correct_total_area) / self.correct_total_area < 1e-6

    def test_total_mass(self):
        assert (self.test_collector.size(self.test_power_req, total=True)[1] -
                self.correct_total_mass) / self.correct_total_mass < 1e-6
