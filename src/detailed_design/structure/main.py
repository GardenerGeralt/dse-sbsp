import utils as ut
import src.gen_eng.materials as gem
import src.database.utils as dbu


def main():
    ...


if __name__ == "__main__":
    print(dbu.read())
    fos = ut.SafetyFactors(1.25, 1.00, 1.00, 1.00, 1.25, 1.25)
    loading = ut.Loading(6, 2, 15, 8)
    aluminum = gem.StructuralMaterial(2700, 69e9, 255e6, 290e6, 0.33, 1)
    sat = ut.Structure(608, aluminum, name="Test")
    sat.set_dimensions(0.5, 1.5)
    sat.size_structure(loading, fos, thickness_range=(0.00, 0.005, 100))
    print(sat.thickness)
    print(sat.total_mass(sat.thickness))
    print(f"{loading.normal_stress(0, 0.001, sat, 1):.3e}, "
          f"{loading.bending_stress(0, 0.05, 0.001, sat, 1) :.3e}, "
          f"{loading.shear_stress(0, 0.001, sat, 1) :.3e}")
    print(f"{loading.normal_stress(0.2, 0.001, sat, 1):.3e}, "
          f"{loading.bending_stress(0.2, 0.05, 0.001, sat, 1) :.3e}, "
          f"{loading.shear_stress(0.2, 0.001, sat, 1, ) :.3e}")
    print(f"{loading.normal_stress(0.4, 0.001, sat, 1):.3e}, "
          f"{loading.bending_stress(0.4, 0.05, 0.001, sat, 1) :.3e}, "
          f"{loading.shear_stress(0.4, 0.001, sat, 1) :.3e}")
    print(sat.ax_natural_freq(sat.thickness, loading))
    print(sat.lat_natural_freq(sat.thickness, loading))
    print(sat.buckling_load(sat.thickness))
    # sat.plot_loads()
