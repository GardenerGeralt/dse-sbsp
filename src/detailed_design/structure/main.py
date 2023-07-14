import numpy as np
import utils as ut
import src.plotting.plots as plt
import src.gen_eng.materials as gem
import src.database.utils as dbu


def main(structure, loading):
    print(sat.thickness)
    print(sat.total_mass(sat.thickness))
    print(f"{loading.normal_stress(0.05, 0.001, sat, 1):.3e}, "
          f"{loading.bending_stress(0.05, 0.05, 0.001, sat, 1) :.3e}, "
          f"{loading.shear_stress(0.05, 0.001, sat, 1) :.3e}")
    print(f"{loading.normal_stress(0.7, 0.001, sat, 1):.3e}, "
          f"{loading.bending_stress(0.7, 0.05, 0.001, sat, 1) :.3e}, "
          f"{loading.shear_stress(0.7, 0.001, sat, 1, ) :.3e}")
    print(f"{loading.normal_stress(1.4, 0.001, sat, 1):.3e}, "
          f"{loading.bending_stress(1.4, 0.05, 0.001, sat, 1) :.3e}, "
          f"{loading.shear_stress(1.4, 0.001, sat, 1) :.3e}")
    print(sat.ax_natural_freq(sat.thickness, loading))
    print("Euler-Bernoulli freq", sat.lat_natural_freq(sat.thickness, loading))
    print(sat.buckling_load(sat.thickness))
    print(sat.i_xx(sat.thickness))
    return loading, sat


if __name__ == "__main__":
    fos = ut.SafetyFactors(1.25, 1.00, 1.00, 1.00, 1.25, 1.25)
    loads = ut.Loading(6, 2, 15, 8)
    aluminum = gem.StructuralMaterial(2700, 69e9, 26e9, 255e6, 290e6, 0.33, 1, 0.8, 0.6)
    sat = ut.Structure(608, aluminum, name="Test")
    sat.set_dimensions(0.5, 1.5)
    sat.size_structure(loads, fos, thickness_range=(0.00, 0.005, 100))

    ld, sc = main(sat, loads)
    abaqus_result = np.genfromtxt(r"abaqus_results\vonMises_Vertical_pxpy.csv", delimiter=",", skip_header=1).T
    x_values = [abaqus_result[0], np.linspace(0, 1.5, 32)]
    y_values = [abaqus_result[1] / 1e6, ld.combined_stress(np.linspace(0, 1.5, 32), -0.25, sc.thickness, sc, 1)[::-1] / 1e6]
    # plt.line_plot(x_values, y_values,
    #               ["Abaqus von Mises Stress", "Calculated Stress"], "Position from top [m]", "Stress [MPa]")
    print(sc.lat_natural_freq_tbt(sc.thickness, ld))
    b = np.linspace(0, 100, 1000)
    values = np.array([sc.implicit_eq(bi, sc.thickness) for bi in b])
    plt.line_plot(b, values, "TBT nat. freq.", "freq", "value")
