from src.prelim_design.eps.power_budget import Batteries as bt
import src.prelim_sizing.collect_ansys.collect_methods as cm

"""Solar Panel characteristics"""
PV_OP_TEMP = 393.
sample_pv_cell = cm.SolarCell(0.201, 3.018e-3, 1.780e-3, 8.5, PV_OP_TEMP, name="AZUR QJ 4G32C C8.5")
solar_sail = cm.Concentrator(0.01, 0.9)
fresnel_lens = cm.Concentrator(0.15, 0.9)    # 1080 kg/m3 silicone density * 140 microns thick
radiator = cm.Radiator(0.9, 1700, 125e-6)   # carbon composite radiator
collect = cm.Collector(sample_pv_cell, fresnel_lens, radiator)
power_required_no_bat = 2e6  # (placeholder)

def panel_no_bat_sizing():
    """Sizing of panels when no batteries are used"""
    area_no_bat = collect.size(power_required_no_bat, total=True)[0]
    mass_no_bat = collect.size(power_required_no_bat, total=True)[1]
    return area_no_bat, mass_no_bat

def panel_battery_sizing():
    """With using a battery, this includes batteries and solar panels"""
    battery = bt(p_req=power_required_no_bat , T_orb=3600*8.7, t_contact=3600*6, t_eclipse_contact=600, E_spec=392400, E_dens=4.428e+8, DoD=0.4, bat_eff=0.9)
    #stored_energy = battery.calc_stored_energy()
    power_required_bat = battery.calc_required_coll_power()
    mass_of_bat = battery.calc_battery_mass()
    volume_of_bat = battery.calc_battery_volume()
    area_with_bat = collect.size(power_required_bat, total= True)[0]
    mass_with_bat = collect.size(power_required_bat, total= True)[1]
    #total_mass_bat_pan = mass_with_bat + mass_of_bat

    return power_required_bat, mass_of_bat, volume_of_bat, mass_with_bat, area_with_bat

def bat_tradeoff():
    "Only solar panels"
    area_no_bat = panel_no_bat_sizing()[0]
    mass_no_bat = panel_no_bat_sizing()[1]

    "With bats"
    power_required_bat = panel_battery_sizing()[0]
    mass_of_bat = panel_battery_sizing()[1]
    volume_of_bat = panel_battery_sizing()[2]
    mass_with_bat = panel_battery_sizing()[3]
    area_with_bat = panel_battery_sizing()[4]

    print('---Only Solar Panels---')
    print(f'Required power generation without batteries: {power_required_no_bat} [W]')
    print(f'Solar panel area without batteries: {area_no_bat} [m²]')
    print(f'Solar panel mass without batteries: {mass_no_bat} [kg]\n')
    print('---Solar Panels & Batteries---')
    print(f'Required power generation with batteries: {power_required_bat} [W]')
    print(f'Solar panel area with using batteries: {area_with_bat} [m²]')
    print(f'Solar panel mass with using batteries: {mass_with_bat} [kg]')
    print(f'Battery mass: {mass_of_bat} [kg]')
    print(f'Battery volume: {volume_of_bat} [m³]')
    print(f'Total mass: {mass_with_bat + mass_of_bat}')

    print(f'\nChange in Solar panel mass: {(mass_with_bat-mass_no_bat)/mass_no_bat*100} [%]')
    print(f'Change in total mass: {(mass_with_bat + mass_of_bat- mass_no_bat)/mass_no_bat*100} [%]')

def sizing_EPS():
    "Actual sizing of the solar panels and batteries"
    panel_area, panel_mass = collect.size(power_required_no_bat, total=True)

    battery = bt(p_req=power_required_no_bat , T_orb=3600*8.7, t_contact=3600*6, t_eclipse_contact=600, E_spec=392400, E_dens=4.428e+8, DoD=0.4, bat_eff=0.9)
    battery_mass = battery.calc_battery_mass()
    battery_volume = battery.calc_battery_volume()

    tot_mass = battery_mass + panel_mass

    print(f'Solar panel mass: {panel_mass} [kg]')
    print(f'Solar panel area: {panel_area} [m²]\n')
    print(f'Battery mass: {battery_mass} [kg]')
    print(f'Battery volume: {battery_volume} [m³]\n')
    print(f'Total mass: {tot_mass} [kg]')
#bat_tradeoff()
sizing_EPS()

