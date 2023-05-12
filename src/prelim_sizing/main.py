import collect_ansys.collect_methods as cm
import pandas as pd
from math import ceil


DRY2WET = 1.72
LASER_SPEC_MASS = 7e-3  # kg/W
MAX_LAUNCH_MASS = 8e3  # kg
LAUNCH_COST = 115e6  # USD (Ariane 6)
PERCENT_IN_VIEW = 0.7


def main(collector_obj, power, eff_trans):
    power_out_pv = power / eff_trans
    mass_laser = power_out_pv * LASER_SPEC_MASS

    _, mass_collect = collector_obj.size(power_out_pv, total=True)

    dry_mass = (mass_laser + mass_collect) * 2 / PERCENT_IN_VIEW
    wet_mass = dry_mass * DRY2WET

    num_of_sc = ceil(wet_mass / MAX_LAUNCH_MASS)
    launch_cost = num_of_sc * LAUNCH_COST

    return {"dry_mass": dry_mass,
            "wet_mass": wet_mass,
            "num_of_sc": num_of_sc,
            "launch_cost": launch_cost}


if __name__ == "__main__":
    power_req = 1e6
    eff_rf2dc = 0.30
    eff_dc2rf = 0.40
    eff_microwave = 0.5
    name_pv, eff_pv, area_pv, mass_pv, suns = pd.read_csv("collect_ansys/pv_cells.csv").values[5]

    pv_cell = cm.SolarCell(eff_pv, area_pv, mass_pv, suns, 393, name=name_pv)
    fresnel_lens = cm.Concentrator(0.15, 0.9)   # 1080 kg/m3 silicone density * 140 microns thick
    radiator = cm.Radiator(0.9, 1700, 125e-6)  # carbon composite radiator
    collector = cm.Collector(pv_cell, fresnel_lens, radiator)

    print(main(collector, power_req, eff_dc2rf*eff_rf2dc))
