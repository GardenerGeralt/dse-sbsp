from src.detailed_design.eps.power_budget import BatteriesBusPower as bt
from src.detailed_design.eps.power_budget import PowerBudget as pb
import src.database.utils as dbu
database = dbu.read()
print(database['power req'])
def sizing_EPS():
    "Sizing of the batteries"
    p_req = pb(p_aocs_ecl=112, p_cdh_ecl=63, p_gnc_ecl=105, p_prop_ecl=35, p_ther_ecl=175, p_struct_ecl=14).calc_eclipse_power_budget()
    battery = bt(p_req=700 , t_eclipse= 0.9558, E_spec=392400, E_dens=4.428e+8,
                 DoD=0.4, bat_eff=0.9, t_mission=25, t_orb=26.93)
    battery_mass = battery.calc_battery_mass()
    battery_volume = battery.calc_battery_volume()
    n_discharges = battery.calc_n_discharges()

    print(f'Battery mass: {battery_mass} [kg]')
    print(f'Battery volume: {battery_volume} [m³]')
    print(f'Number of discharges: {n_discharges} [-]')

sizing_EPS()

