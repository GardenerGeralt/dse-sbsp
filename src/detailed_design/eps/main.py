from src.detailed_design.eps.power_budget import BatteriesBusPower as bt
from src.detailed_design.eps.power_budget import PowerBudget as pb
from src.detailed_design.eps.power_budget import PowerMass as pm
import numpy as np
import src.database.utils as dbu

def sizing_EPS():
    """Sizing of the batteries"""
    bus_power = pb(p_aocs_ecl=112, p_cdh_ecl=63, p_gnc_ecl=105, p_prop_ecl=35, p_ther_ecl=175, p_struct_ecl=14,
                   p_pow_ecl=196, p_aocs_peak= 1, p_cdh_peak= 1, p_gnc_peak= 1, p_prop_peak=1, p_ther_peak=1,
                   p_struct_peak=1, p_pow_peak=1).calc_eclipse_power_budget()
    # battery = bt(p_req=bus_power , t_eclipse= 0.9558, E_spec=392400, E_dens=4.428e+8,
    #              DoD=0.4, bat_eff=0.9, t_mission=25, t_orb=26.93, m_battery=18, exergy=65)
    battery = bt(p_req=bus_power , t_eclipse= 0.9558, E_spec= 141, E_dens=335,
                 DoD=0.4, bat_eff=0.9, t_mission=25, t_orb=26.93, m_battery=0.950, exergy=65)
    battery_energy = battery.calc_battery_energy()
    battery_mass = battery.calc_battery_mass()
    battery_volume = battery.calc_battery_volume()
    n_discharges = battery.calc_n_discharges()
    n_batteries = int(np.ceil(battery.calc_n_batteries()))
    production_energy = battery.calc_battery_exergy()
    total_battery_mass = n_batteries * battery.m_battery

    "Mass of the total EPS system"
    masses = pm(2.4, 4.4, 20, total_battery_mass, 16)
    total_EPS_mass = masses.calc_EPS_mass()

    return bus_power, battery_energy, battery_mass, battery_volume, n_discharges, n_batteries, n_batteries, \
        production_energy, total_battery_mass, total_EPS_mass

def printing():
    bus_power, battery_energy, battery_mass, battery_volume, n_discharges, n_batteries, n_batteries, \
        production_energy, total_battery_mass, total_EPS_mass = sizing_EPS()
    print(f'Bus power required: {bus_power} [W]')
    print(f'Required Energy storage {battery_energy} [Wh]')
    print(f'Battery mass based on specific mass: {battery_mass} [kg]')
    print(f'Battery volume based on density: {battery_volume} [L]')
    print(f'Number of batteries: {n_batteries}')
    print(f'Total battery mass based on number of batteries: {round(total_battery_mass, 2)} [kg]')
    print(f'Number of discharges: {n_discharges} [-]')
    print(f'Energy required to produce batteries: {production_energy} [Wh]')
    print(f'Total mass of the EPS system {round(total_EPS_mass,2)} [kg]')
printing()


