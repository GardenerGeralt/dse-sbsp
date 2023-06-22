from src.detailed_design.eps.power_budget import BatteriesBusPower as bt
from src.detailed_design.eps.power_budget import PowerBudget as pb
from src.detailed_design.eps.power_budget import PowerMass as pm
import numpy as np
import src.database.utils as dbu

def sizing_EPS():
    """Sizing of the batteries"""
    bus_power = pb(p_aocs_ecl=62+18.4+2, p_cdh_ecl=0, p_gnc_ecl=0, p_prop_ecl=0, p_ther_ecl=0, p_struct_ecl=0,
                   p_pow_ecl=0, p_aocs_peak= 650, p_cdh_peak= 0, p_gnc_peak= 0, p_prop_peak=0, p_ther_peak=0,
                   p_struct_peak=0, p_pow_peak=0).calc_eclipse_power_budget()
    # battery = bt(p_req=bus_power , t_eclipse= 0.9558, E_spec=392400, E_dens=4.428e+8,
    #              DoD=0.4, bat_eff=0.9, t_mission=25, t_orb=26.93, m_battery=18, exergy=65)
    #bus_power = 351.2 #4.94
    battery = bt(p_req=bus_power , t_eclipse= 4.94, E_spec= 141, E_dens=335,
                 DoD=0.4, bat_eff=0.9, t_mission=25, t_orb=21.05, m_battery=0.950, exergy=65)
    # battery = bt(p_req=1e6, t_eclipse=4.94, E_spec=141, E_dens=335,
    #              DoD=0.4, bat_eff=0.9, t_mission=25, t_orb=26.93, m_battery=0.950, exergy=65)
    battery_energy = battery.calc_battery_energy()
    battery_mass = battery.calc_battery_mass()
    battery_volume = battery.calc_battery_volume()
    n_discharges = battery.calc_n_discharges()
    n_batteries = int(np.ceil(battery.calc_n_batteries()))
    production_energy = battery.calc_battery_exergy()
    total_battery_mass = n_batteries * battery.m_battery

    "Mass of the total EPS system"
    masses = pm(shunt_mass=2.4, cable_sp_mass=4.4, L_cables=20, batteries_mass=total_battery_mass, PMAD_mass=27,
                dry_mass=669.31, harness_frac=0.03, n_conv=235, m_conv=0.215)
    V_conv = masses.n_conv * 47.33e-6*1000
    total_EPS_mass = masses.calc_EPS_mass()
    harness_mass = masses.harness_mass_v2

    return bus_power, battery_energy, battery_mass, battery_volume, n_discharges, n_batteries, n_batteries, \
        production_energy, total_battery_mass, total_EPS_mass, harness_mass, V_conv


#print(130+24.5+70+9+131.5+35+58.07+27.7+75+77)
def printing():
    bus_power, battery_energy, battery_mass, battery_volume, n_discharges, n_batteries, n_batteries, \
        production_energy, total_battery_mass, total_EPS_mass, harness_mass, V_conv = sizing_EPS()
    print(f'Bus power required: {bus_power} [W]')
    print(f'Required Energy storage {battery_energy} [Wh]')
    print(f'Battery mass based on specific mass: {battery_mass} [kg]')
    print(f'Battery volume based on density: {battery_volume} [L]')
    print(f'Number of batteries (2 added for redundancy): {n_batteries}')
    print(f'Total battery mass based on number of batteries: {round(total_battery_mass, 2)} [kg]')
    print(f'Number of discharges: {n_discharges} [-]')
    print(f'Energy required to produce batteries: {production_energy} [Wh]')
    print(f'Total mass of the EPS system {round(total_EPS_mass,2)} [kg]')
    print(f'Harness mass: {harness_mass} [kg]')
    print(f'Converter volume {V_conv} [L]')

printing()

def sensitivity_analysis():
    bus_power = 1
