import pytest
import numpy as np
from src.prelim_design.structure import utils as ut
import src.gen_eng.materials as gem


class TestSafetyFactors:
    test_safety_factors = ut.SafetyFactors(1.00, 1.25, 1.50, 1.75, 2.00, 2.25)

    def test_init(self):
        assert self.test_safety_factors._k_qualif == 1.00
        assert self.test_safety_factors._k_project == 1.25
        assert self.test_safety_factors._k_model == 1.50
        assert self.test_safety_factors._k_local == 1.75
        assert self.test_safety_factors._fos_yield == 2.00
        assert self.test_safety_factors._fos_ultimate == 2.25

    def test_calc_coef_a(self):
        assert self.test_safety_factors.coef_a == 1.875

    def test_calc_coef_b(self):
        assert self.test_safety_factors.coef_b == 3.5

    def test_calc_coef_c(self):
        assert self.test_safety_factors.coef_c == 3.9375

    def test_fos_dyl(self):
        assert self.test_safety_factors.fos_dyl == 6.5625

    def test_fos_dul(self):
        assert self.test_safety_factors.fos_dul == 7.3828125


class TestLoading:
    test_safety_factors = ut.SafetyFactors(1.00, 1.25, 1.50, 1.75, 2.00, 2.25)
    test_loading = ut.Loading(5, -2)
    test_material = gem.StructuralMaterial(2000, 50e9, 100e6, 150e6, 0.30, 1)
    test_structure = ut.Structure(50, test_material, name="test_structure")
    test_structure.set_dimensions(0.1, 1)

    def test_init(self):
        assert self.test_loading.qs_axial == 5
        assert self.test_loading.qs_lateral == -2

    def test_normal_force(self):    # mass = 0.8kg, at thickness = 0.001m
        assert np.isclose(self.test_loading._normal_force(0.2, 0.001, self.test_structure, 1.2),
                          2979.652536, rtol=1e-6)
        assert np.isclose(self.test_loading._normal_force(0.8, 0.001, self.test_structure, 1.2),
                          9.414384, rtol=1e-6)

    def test_shear_force(self):
        assert np.isclose(self.test_loading._shear_force(0.2, 0.001, self.test_structure, 1.2),
                          -1191.861014, rtol=1e-6)
        assert np.isclose(self.test_loading._shear_force(0.8, 0.001, self.test_structure, 1.2),
                          -3.7657536, rtol=1e-6)

    def test_bending_moment(self):
        assert np.isclose(self.test_loading._bending_moment(0.2, 0.001, self.test_structure, 1.2),
                          -359.0646058, rtol=1e-6)
        assert np.isclose(self.test_loading._bending_moment(0.8, 0.001, self.test_structure, 1.2),
                          -0.37657536, rtol=1e-6)

    def test_normal_stress(self):
        assert np.isclose(self.test_loading.normal_stress(0.2, 0.001, self.test_structure, 1.2),
                          -7449131.34, rtol=1e-6)
        assert np.isclose(self.test_loading.normal_stress(0.8, 0.001, self.test_structure, 1.2),
                          -23535.96, rtol=1e-6)

    def test_shear_stress(self):
        assert np.isclose(self.test_loading.shear_stress(0.2, 0.001, self.test_structure, 1.2),
                          -2979652.535, rtol=1e-6)
        assert np.isclose(self.test_loading.shear_stress(0.8, 0.001, self.test_structure, 1.2),
                          -9414.384, rtol=1e-6)

    def test_bending_stress(self):  # i_xx = 6.6668333333e-7, at thickness = 0.001m
        test_y_mesh = np.array([-0.05, 0, 0.05])
        assert np.all(np.isclose(self.test_loading.bending_stress(0.2, test_y_mesh, 0.001, self.test_structure, 1.2),
                                 np.array([26929172.21, 0, -26929172.21]), rtol=1e-6))
        assert np.all(np.isclose(self.test_loading.bending_stress(0.8, test_y_mesh, 0.001, self.test_structure, 1.2),
                                 np.array([28242.44594, 0, -28242.44594]), rtol=1e-6))

    def test_combined_stress(self):
        test_y_mesh = np.meshgrid(np.linspace(0, self.test_structure.height, 3),
                                  np.linspace(-self.test_structure.width / 2, self.test_structure.width / 2, 3),
                                  np.linspace(-self.test_structure.width / 2, self.test_structure.width / 2, 3),
                                  indexing='ij')[2]
        ref_sol_1 = np.meshgrid([0, 0, 0], [0, 0, 0], [19480040.87, -7449131.34, -34378303.55], indexing='ij')[2]
        ref_sol_1[1:-1, 1:-1, :] = 0
        ref_sol_2 = np.meshgrid([0, 0, 0], [0, 0, 0], [4706.48594, -23535.96, -51778.40594], indexing='ij')[2]
        ref_sol_2[1:-1, 1:-1, :] = 0
        assert np.all(np.isclose(self.test_loading._combined_stress(0.2, test_y_mesh, 0.001, self.test_structure, 1.2),
                                 ref_sol_1, rtol=1e-6))
        assert np.all(np.isclose(self.test_loading._combined_stress(0.8, test_y_mesh, 0.001, self.test_structure, 1.2),
                                 ref_sol_2, rtol=1e-6))

    def test_volume_stress(self):
        test_y_mesh = np.meshgrid(np.linspace(0, self.test_structure.height, 3),
                                  np.linspace(-self.test_structure.width / 2, self.test_structure.width / 2, 3),
                                  np.linspace(-self.test_structure.width / 2, self.test_structure.width / 2, 3),
                                  indexing='ij')[2]
        ref_sol = np.array([[[37362215.63, -7472667.3, -52307550.23],
                             [37362215.63,          0, -52307550.23],
                             [37362215.63, -7472667.3, -52307550.23]],
                            [[-7237312.113, -7413827.4, -7590342.687],
                             [-7237312.113,          0, -7590342.687],
                             [-7237312.113, -7413827.4, -7590342.687]],
                            [[0, 0, 0],
                             [0, 0, 0],
                             [0, 0, 0]]])
        sol = self.test_loading.volume_stress(0.001, self.test_structure, 1.2, [3, 3, 3])
        assert np.all(np.isclose(self.test_loading.volume_stress(0.001, self.test_structure, 1.2, [3, 3, 3]),
                                 ref_sol, rtol=1e-6))


class TestStructure:
    test_material = gem.StructuralMaterial(2000, 50e9, 100e6, 150e6, 0.30, 1)
    test_structure = ut.Structure(50, test_material, name="test_structure")
    test_structure.set_dimensions(0.1, 1)

    def test_init(self):
        assert self.test_structure.load_mass == 50
        assert self.test_structure.material == self.test_material
        assert self.test_structure.name == "test_structure"

    def test_cs_area(self):
        assert np.isclose(self.test_structure.cs_area(0.001), 0.0004, rtol=1e-6)

    def test_i_xx(self):
        assert np.isclose(self.test_structure.i_xx(0.001), 6.6668e-7, rtol=1e-6)

    def test_buckling_load(self):
        # crit_buckling = 18076198.54 <-
        # crippling = 40358296.63
        assert np.isclose(self.test_structure.buckling_load(0.001), 18076198.54, rtol=1e-6)

    def test_structure_mass(self):
        assert np.isclose(self.test_structure.structure_mass(0.001), 0.8, rtol=1e-6)

    def test_total_mass(self):
        assert np.isclose(self.test_structure.total_mass(0.001), 50.8, rtol=1e-6)

    def test_set_dimensions(self):
        assert self.test_structure.width == 0.1
        assert self.test_structure.height == 1

    def test_plot_loads(self):
        pass

    def test_size_structure(self):
        test_safety_factors = ut.SafetyFactors(1.00, 1.25, 1.50, 1.75, 2.00, 2.25)
        test_loading = ut.Loading(5, -2)
        assert np.all(np.isclose(
            sorted(self.test_structure.size_structure(test_loading, test_safety_factors).values()),
            [0.00297979797979798, 52.38383838383838], rtol=1e-6
        ))
