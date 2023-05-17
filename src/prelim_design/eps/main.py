from src.prelim_design.eps.power_budget import Batteries as bt
import src.prelim_sizing.collect_ansys.collect_methods as cm

"""Placeholder for now, since once we have orbit stuff I guess we can import from there"""
"""orbit = [p_req, T_orb, contact_frac, collect_frac]"""


"""Solar Panel characteristics"""
PV_OP_TEMP = 393.
sample_pv_cell = cm.SolarCell(0.32, 3.018e-3, 1.780e-3, 8.5, PV_OP_TEMP, name="AZUR QJ 4G32C C8.5")
solar_sail = cm.Concentrator(0.01, 0.9)
fresnel_lens = cm.Concentrator(0.15, 0.9)    # 1080 kg/m3 silicone density * 140 microns thick
radiator = cm.Radiator(0.9, 1700, 125e-6)   # carbon composite radiator
collect = cm.Collector(sample_pv_cell, fresnel_lens, radiator)

def battery_panels_tradeoff():
    #First without batteries:
    power_required_no_bat = 2e6 #(placeholder)
    area_no_bat = collect.size(power_required_no_bat, total= True)[0]
    mass_no_bat = collect.size(power_required_no_bat, total= True)[1]

    #With using a battery:
    battery = bt(p_req=2e6, T_orb=3600, contact_frac=0.25, collect_frac=0.9, E_spec=392400)
    stored_energy = battery.calc_stored_energy()
    power_required_bat = battery.calc_required_coll_power()
    mass_of_bat = battery.calc_battery_mass()
    area_with_bat = collect.size(power_required_bat, total= True)[0]
    mass_with_bat = collect.size(power_required_bat, total= True)[1]

    return

print(battery_panels_tradeoff())