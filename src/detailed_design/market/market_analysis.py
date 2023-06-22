import numpy as np

class OperationalCosts:
    def __init__(self, FTE_tech, FTE_eng, N_engineers, N_technicians, SLOC_fsw, SLOC_gsw):
        """

        Args:
            FTE_tech: yearly FTE of technician (Full Time Equivalent) [2018 USD]
            FTE_eng: yearly FTE of engineers (FTE)
            SLOC_fsw: Software Lines Of Code for space
            SLOC_gsw: Software Lines Of Code for ground station
            N_engineers: number of engineers
            N_technicians: number technicians
        """

        self.FTE_tech = FTE_tech
        self.FTE_eng = FTE_eng
        self.N_engineers = N_engineers
        self.N_technicians = N_technicians
        self.SLOC_fsw = SLOC_fsw
        self.SLOC_gsw = SLOC_gsw

        self.mission_operations_cost = self.calc_mission_operations_cost()
        self.ground_software_cost = self.calc_ground_software_cost()
        self.space_software_cost = self.calc_space_software_cost()
        self.total_operational_cost = self.calc_total_operational_cost()

    def calc_mission_operations_cost(self):
        return self.FTE_eng * self.N_engineers + self.FTE_tech * self.N_technicians

    def calc_space_software_cost(self):
        return self.SLOC_fsw / 16000 * self.FTE_eng

    def calc_ground_software_cost(self):
        return self.SLOC_gsw / 28200 * self.FTE_eng

    def calc_total_operational_cost(self):
        return self.mission_operations_cost + self.ground_software_cost + self.space_software_cost


class LCOE:
    def __init__(self, investment_cost, maintenance_cost, energy_prod, r, t):
        """
        Args:
            investment_cost: yearly investment cost as list/array [€]
            maintenance_cost: yearly maintenance & operations cost as list/array [€]
            energy_prod: yearly energy production as list/array [MWh]
            r: discount rate as single number [-]
            t: life time [years]
        """

        self.investment_cost = np.array(investment_cost)
        self.maintenance_cost = np.array(maintenance_cost)
        self.energy_prod = np.array(energy_prod)
        self.r = r  # * np.ones((1,25))
        self.t = np.arange(0, t)
        self.lcoe = self.calc_lcoe()

    def calc_lcoe(self):
        total_cost = self.investment_cost + self.maintenance_cost
        num = np.sum([total_cost[t]/(1+self.r)**t for t in self.t])
        denum = np.sum(self.energy_prod[t]/(1+self.r)**t for t in self.t)
        return num/denum

