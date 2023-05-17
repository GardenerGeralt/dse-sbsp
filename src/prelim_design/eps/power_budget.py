import numpy as np


class PowerBudget:
    def __init__(self, p_trans, p_aocs, p_cdh, p_gnc, p_prop, p_struct, p_ther):
        """
        :param p_trans: Power needed for transmission [W] (accounting for transmission losses)
        :param p_aocs: AOCS Power requirement [W]
        :param p_cdh: Command & Data Handeling power requirement [W]
        :param p_gnc: Guidance, navigation & control power requirement [W]
        :param p_prop: Propulsion power requirement [W]
        :param p_struct: Structures power requirement [W]
        :param p_ther: Thermal subsystem power requirement [W]
        """
        self.p_trans = p_trans
        self.p_aocs = p_aocs
        self.p_cdh = p_cdh
        self.p_gnc = p_gnc
        self.p_prop = p_prop
        self.p_struct = p_struct
        self.p_ther = p_ther
        self.power_budget = self.calc_power_budget()

    # def __str__(self, ):
    #     return

    def calc_power_budget(self):
        """Sum all subsystem power requirements to find power that must be generated by collection system"""
        return sum([self.p_trans, self.p_aocs, self.p_cdh, self.p_gnc, self.p_prop, self.p_struct, self.p_ther])


class Batteries:
    def __init__(self, p_req, T_orb, contact_frac, collect_frac, E_spec, E_dens):
        """
        :param p_req: Power needed for transmission [W] (accounts for losses)
        :param T_orb: Total orbital period (s)
        :param contact_frac: fraction of the orbit that allows for power transmission [-]
        :param collect_frac: fraction of the orbit that allows for power collection [-]
        :param E_spec: Specific battery energy [J/kg]
        :param E_dens: Energy volume density [J/L]
        """

        self.p_req = p_req
        self.T_orb = T_orb
        self.contact_frac = contact_frac
        self.collect_frac = collect_frac
        self.E_spec = E_spec
        self.E_dens = E_dens

        self.stored_energy = self.calc_stored_energy()
        self.battery_mass = self.calc_battery_mass()

    def calc_stored_energy(self):
        return self.p_req * self.T_orb * self.contact_frac
        #return self.p_req * (self.T_orb*self.contact_frac -  eclipse_w_tx_frac * t_eclipse)
        # return p_req * (t_tx -eclipse_w_tx_frac * t_eclipse)

    def calc_battery_mass(self):
        return self.stored_energy / self.E_spec

    def calc_battery_volume(self):
        return self.stored_energy / self.E_dens

    def calc_required_coll_power(self):
        return self.stored_energy / (self.T_orb * self.collect_frac)
