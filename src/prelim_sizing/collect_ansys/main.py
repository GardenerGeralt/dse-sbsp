import collect_methods as cm
import pandas as pd
import numpy as np
import plotly.express as px

# Assumptions:
# the AZUR TJ 3C44 C250 solar cell has the same density as the AZUR TJ 3G30C solar cell


PV_OP_TEMP = 393.   # [K] solar cell maximum operating temperature (120 C)


def convert_to_object(row):
    return cm.SolarCell(row["Efficiency [-]"], row["Cell area [m2]"], row["Average cell mass [kg]"],
                        row["Concentration [suns]"], PV_OP_TEMP, name=row["PV cell name"])


def main(pv_cell_df: pd.DataFrame, concentrator_obj: cm.Concentrator, radiator_obj: cm.Radiator,
         power_req: float, plot: bool = False):
    pv_cell_objs = [convert_to_object(r) for _, r in pv_cell_df.iterrows()]

    pv_cell_df2 = pd.DataFrame(columns=["PV cell name", "Power density [W/m_squared]", "Specific power [W/kg]"])
    collectors_df = pd.DataFrame(columns=["PV cell name", "Total area [m_squared]", "Total mass [kg]"])
    for pv_cell in pv_cell_objs:
        collector = cm.Collector(pv_cell, concentrator_obj, radiator_obj)
        pv_cell_df2.loc[pv_cell.name, "PV cell name"] = pv_cell.name
        collectors_df.loc[pv_cell.name, "PV cell name"] = pv_cell.name
        total_area, total_mass = collector.size(power_req, total=True)
        pv_cell_df2.loc[pv_cell.name, "Power density [W/m_squared]"] = power_req / total_area
        pv_cell_df2.loc[pv_cell.name, "Specific power [W/kg]"] = power_req / total_mass
        collectors_df.loc[pv_cell.name, "Total area [m_squared]"] = total_area
        collectors_df.loc[pv_cell.name, "Total mass [kg]"] = total_mass

    # pv_cell_df["Power density [W/m_squared]"] = pv_cell_df.apply(lambda r: convert_to_object(r).power_dens, axis=1)
    # pv_cell_df["Specific power [W/kg]"] = pv_cell_df.apply(lambda r: convert_to_object(r).spec_power, axis=1)

    # pv_cell_df.apply(lambda r: print(convert_to_object(r)), axis=1)

    if plot:
        fig1 = px.scatter(pv_cell_df2, x="Power density [W/m_squared]", y="Specific power [W/kg]", hover_name="PV cell name")
        fig1.show()

        fig2 = px.scatter(collectors_df, x="Total area [m_squared]", y="Total mass [kg]", hover_name="PV cell name")
        fig2.show()

    return collectors_df


if __name__ == "__main__":
    pv_cells = pd.read_csv("pv_cells.csv")
    sample_pv_cell = cm.SolarCell(0.421, 0.100e-3, 0.089e-3, 250, PV_OP_TEMP, name="AZUR TJ 3C44 C250")
    solar_sail = cm.Concentrator(0.01, 0.9)
    fresnel_lens = cm.Concentrator(0.15, 0.9)    # 1080 kg/m3 silicone density * 140 microns thick
    radiator = cm.Radiator(0.9, 1700, 125e-6)   # carbon composite radiator
    # radiator = cm.Radiator(0.9, 2700, 125e-6)  # aluminium radiator
    power_required = 1e6
    collect = cm.Collector(sample_pv_cell, fresnel_lens, radiator)
    # print(collect.size(power_required))

    main(pv_cells, solar_sail, radiator, power_required, plot=True)

