

class Laser:
    def __init__(self, dtr_eff, wavelength, av_mass):
        """
        :param dtr_eff: DC to RF efficiency [-]
        """
        self.dtr_eff = dtr_eff
        self.wavelength = wavelength
        self.av_mass = av_mass
        # self.
        ...

    def __str__(self, ):
        return f"\nLaser:\n" \
                 f"------------------\n" \
               f"    DC-to-RF efficiency: {self.dtr_eff} [-],\n" \
               f"     Cell area: {self.cell_area} [m2],\n" \
               f"  Average mass: {self.av_mass} [kg],\n" \
               # f" Power density: {self.power_dens} [W/m2],\n" \
               # f"Specific power: {self.spec_power} [W/kg]."

    def calc_power_dens(self, ):

        pass

class Microwave:
    def __init__(self):
        ...
