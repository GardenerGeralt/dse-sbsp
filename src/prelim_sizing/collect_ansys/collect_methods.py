
SOLAR_IRRADIANCE_1AU = 1361.0   # [W/m2]


class PhotoCell:
    def __init__(self, eff, cell_area, av_mass, concentration):
        """
        :param eff: pv cell efficiency [-]
        :param cell_area: single pv cell area [m2]
        :param av_mass: single pv cell mass [kg]
        :param concentration: solar irradiance concentration [suns]
        """
        self.eff = eff
        self.cell_area = cell_area
        self.av_mass = av_mass
        self.concentration = concentration

        self.power_dens = self.calc_power_dens()
        self.spec_power = self.calc_spec_power()

    def __str__(self):
        return f"\nPhotovoltaic Cell:\n" \
                 f"------------------\n" \
               f"    Efficiency: {self.eff} [-],\n" \
               f"     Cell area: {self.cell_area} [m2],\n" \
               f"  Average mass: {self.av_mass} [kg],\n" \
               f" Concentration: {self.concentration} [suns],\n" \
               f" Power density: {self.power_dens} [W/m2],\n" \
               f"Specific power: {self.spec_power} [W/kg]."

    def calc_power_dens(self):
        return SOLAR_IRRADIANCE_1AU * self.concentration * self.eff

    def calc_spec_power(self):
        return SOLAR_IRRADIANCE_1AU * self.concentration * self.eff * self.cell_area / self.av_mass


class Concentrator:
    def __init__(self):
        ...
