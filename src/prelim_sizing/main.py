import collect_ansys.collect_methods as cm
import transmit_ansys.transmit_methods as tm
import orbit_ansys.orbit_ansys as oa
import cost_ansys.cost_ansys as ca
import pandas as pd
from math import ceil

EPS2DRY = 2.
DRY2WET = 1.72

COLLECTORS = pd.read_csv("collect_ansys/pv_cells.csv", index_col=0, header=0)
TRANSMITTERS = pd.read_csv("transmit_ansys/transmitters.csv", index_col=0, header=0)
ORBITS = pd.read_csv("orbit_ansys/orbits.csv", index_col=0, header=0)
LAUNCHERS = pd.read_csv("cost_ansys/launchers.csv", index_col=0, header=0)


def create_collector(design):
    name = design[1]["Collector"]
    solar_cell = COLLECTORS.loc[name]
    solar_cell = cm.SolarCell(solar_cell["Efficiency [-]"], solar_cell["Cell area [m2]"],
                              solar_cell["Average cell mass [kg]"], solar_cell["Concentration [suns]"],
                              393, name=name)
    concentrator = cm.Concentrator(0.15, 0.9)
    radiator = cm.Radiator(0.9, 1700, 125e-6)   # carbon composite radiator
    collector = cm.Collector(solar_cell, concentrator, radiator)
    return collector


def create_transmitter(design):
    name = design[1]["Transmitter"]
    transmitter = TRANSMITTERS.loc[name]
    if "Laser" in name:
        transmitter = tm.Laser(transmitter["Frequency [Hz]"], transmitter["TX efficiency [-]"],
                               transmitter["RX efficiency [-]"], transmitter["Min. beam width [m]"],
                               transmitter["M squared [-]"], transmitter["Spec. mass [kg/W]"])
    elif "Microwave" in name:
        transmitter = tm.Microwave(transmitter["Frequency [Hz]"], transmitter["TX efficiency [-]"],
                                   transmitter["RX efficiency [-]"], transmitter["TX gain [dB]"],
                                   transmitter["RX gain [dB]"], transmitter["Spec. mass [kg/W]"])
    else:
        raise ValueError(f"Transmitter type not recognized. Got {name}")
    return transmitter


def create_orbit(design):
    name = design[1]["Orbit"]
    orbit = ORBITS.loc[name]
    orbit = oa.OrbitFromPeri(orbit["Pericenter [m]"], orbit["Eccentricity [-]"],
                             orbit["Inclination [deg]"], name=name)
    return orbit


def create_launcher(design):
    name = design[1]["Launcher"]
    launcher = LAUNCHERS.loc[name]
    launcher = ca.Launcher(launcher["Max payload mass [kg]"], launcher["Cost per launch [M$]"])
    return launcher


def main(designs, power_rx):
    design_df = pd.DataFrame(columns=["Concept name", "Total mass [kg]", "Total cost [M$]"])
    for design in designs.iterrows():
        collector = create_collector(design)
        transmitter = create_transmitter(design)
        orbit = create_orbit(design)
        launcher = create_launcher(design)

        contact_time, contact_altitude = orbit.calc_view()
        power_tx = transmitter.calc_power_tx(power_rx, contact_altitude)
        mass_tx = transmitter.calc_mass_tx(power_tx)
        _, mass_collect = collector.size(power_tx, total=True)
        dry_mass = (mass_tx + mass_collect) * EPS2DRY
        wet_mass = dry_mass * DRY2WET
        cost_total = launcher.cost(wet_mass)
        design_df = pd.concat([design_df, pd.DataFrame({"Concept name": [design[0]],
                                                        "Total mass [kg]": [wet_mass],
                                                        "Total cost [M$]": [cost_total]})], ignore_index=True)
    return design_df


if __name__ == "__main__":
    power_req = 1e6

    concepts = pd.read_csv("concepts.csv", index_col=0, header=0)
    print(main(concepts, power_req))
