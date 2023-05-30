import numpy as np
import multiprocessing as mp
from src.gen_eng.materials import StructuralMaterial
from src.plotting import plots as plt

G_ACCELERATION = 9.80665


class SafetyFactors:
    def __init__(self, k_qualif, k_project, k_model, k_local, fos_yield, fos_ultimate):
        self._k_qualif = k_qualif
        self._k_project = k_project
        self._k_model = k_model
        self._k_local = k_local
        self._fos_yield = fos_yield
        self._fos_ultimate = fos_ultimate

        self.coef_a = self._calc_coef_a()
        self.coef_b = self._calc_coef_b()
        self.coef_c = self._calc_coef_c()

        self.fos_dyl = self.coef_a * self.coef_b
        self.fos_dul = self.coef_a * self.coef_c

    def _calc_coef_a(self):
        return self._k_qualif * self._k_project * self._k_model

    def _calc_coef_b(self):
        return self._k_local * self._fos_yield

    def _calc_coef_c(self):
        return self._k_local * self._fos_ultimate


class Loading:
    def __init__(self, qs_axial, qs_lateral):
        """
            Set the launch loads on the structure.
            Args:
                qs_axial: [min, max] Quasi-static axial load
                qs_lateral: [min, max] Quasi-static lateral load
            Returns:

        """
        self.qs_axial = qs_axial
        self.qs_lateral = qs_lateral

    def _normal_force(self, z, thickness, structure, safety_factor):
        return safety_factor * self.qs_axial * G_ACCELERATION * \
            (structure.structure_mass(thickness) * (1 - z / structure.height) +
             structure.load_mass * np.heaviside(structure.height / 2 - z, 1))

    def _shear_force(self, z, thickness, structure, safety_factor):
        return safety_factor * self.qs_lateral * G_ACCELERATION * \
            (structure.structure_mass(thickness) * (1 - z / structure.height) +
             structure.load_mass * np.heaviside(structure.height / 2 - z, 1))

    def _bending_moment(self, z, thickness, structure, safety_factor):
        return safety_factor * self.qs_lateral * G_ACCELERATION * \
            (structure.structure_mass(thickness) * (structure.height / 2 - z + (z ** 2) / (2 * structure.height)) +
             structure.load_mass * np.heaviside(structure.height / 2 - z, 1) * (structure.height / 2 - z))

    def normal_stress(self, z, thickness, structure, safety_factor):
        return - self._normal_force(z, thickness, structure, safety_factor) / structure.cs_area(thickness)

    def shear_stress(self, z, thickness, structure, safety_factor):
        return self._shear_force(z, thickness, structure, safety_factor) / structure.cs_area(thickness)

    def bending_stress(self, z, y_mesh, thickness, structure, safety_factor):
        a = self._bending_moment(z, thickness, structure, safety_factor)
        b = y_mesh
        c = structure.i_xx(thickness)
        return self._bending_moment(z, thickness, structure, safety_factor) * y_mesh / structure.i_xx(thickness)

    def _combined_stress(self, z, y_mesh, thickness, structure, safety_factor):
        comb_strss = self.normal_stress(z, thickness, structure, safety_factor) + \
                     self.bending_stress(z, y_mesh, thickness, structure, safety_factor)
        comb_strss[:, 1:-1, 1:-1] = 0
        return comb_strss

    def volume_stress(self, thickness, structure, safety_factor, mesh_size, return_mesh=False):
        mesh = np.meshgrid(np.linspace(0, structure.height, mesh_size[2]),
                           np.linspace(-structure.width / 2, structure.width / 2, mesh_size[0]),
                           np.linspace(-structure.width / 2, structure.width / 2, mesh_size[1]), indexing='ij')
        z_mesh, x_mesh, y_mesh = mesh
        comb_strss = self._combined_stress(z_mesh, y_mesh, thickness, structure, safety_factor)
        if return_mesh:
            return comb_strss, mesh
        else:
            return comb_strss


class Structure:
    """
    A class for sizing the spacecraft structure,
    under the assumption that the structure is a thin-walled square prism.
    """

    def __init__(self, load_mass, material: StructuralMaterial, name="Structure"):
        # Load mass
        self.load_mass = load_mass
        # Material
        self.material = material
        # Dimensions
        self.width = None
        self.height = None
        self.thickness = None
        # Name
        self.name = name

    def cs_area(self, thickness):
        return 4 * self.width * thickness

    def i_xx(self, thickness):
        def _i_xx_rect(width, height):
            return width * height ** 3 / 12

        def _par_ax(area, dist):
            return area * dist ** 2

        return 2 * _i_xx_rect(thickness, self.width) + 2 * _i_xx_rect(self.width, thickness) + \
            2 * _par_ax(self.width * thickness, self.width / 2)

    def buckling_load(self, thickness):
        def _crit_buckling():
            buckling_coef = 4.00    # SSSS
            return buckling_coef * np.pi ** 2 * self.material.elastic_mod / \
                (12 * (1 - self.material.poisson_ratio ** 2)) * (thickness / self.width) ** 2

        def _crippling():   # TODO: replace magic numbers with variables
            return self.material.yield_strength * 0.8 * (_crit_buckling() / self.material.yield_strength) ** (1 - 0.6)

        buckling_loads = [_crit_buckling(), _crippling(), self.material.yield_strength]
        return np.min(buckling_loads)

    def structure_mass(self, thickness):
        return self.material.density * self.cs_area(thickness) * self.height

    def total_mass(self, thickness):
        return self.load_mass + self.structure_mass(thickness)

    def set_dimensions(self, width, height):
        self.width = width
        self.height = height

    def plot_loads(self, loading):
        """
        Plot the loads on the structure.
        Args:
            loading: Loading on the structure
        Returns:

        """
        strss, mesh = loading.volume_stress(self.thickness, self, 1, [10, 10, 10])
        plt.volume_slice(strss, mesh)

    def size_structure(self, loading, safety_factors, mesh_size=(100, 100, 100), thickness_range=(0, 0.005, 100)):
        """
        Size the structure.
        Args:
            loading: Loading on the structure
            safety_factors: Safety factors for the structure
            mesh_size: Number of points in the x and y directions to use for the mesh
            thickness_range: Range of thicknesses to check
        Returns:
        """
        def _is_safe(thickness):
            yield_safe = np.all(np.abs(loading.volume_stress(thickness, self, safety_factors.fos_dyl, mesh_size))
                                < self.material.yield_strength)
            ult_safe = np.all(np.abs(loading.volume_stress(thickness, self, safety_factors.fos_dul, mesh_size))
                              < self.material.ultimate_strength)
            buckl_safe = np.all(np.abs(loading.normal_stress(self.height/2, thickness, self, safety_factors.fos_dyl))
                                < self.buckling_load(thickness))  # TODO: check buckling load at all heights
            return yield_safe and ult_safe and buckl_safe

        def _find_thickness():
            thick_arr = np.linspace(*thickness_range)[1:]
            return np.min(thick_arr[[_is_safe(t) for t in thick_arr]])

        self.thickness = _find_thickness()

        return {"Minimum thickness [m]": self.thickness, "Minimum mass [kg]": self.total_mass(self.thickness)}
