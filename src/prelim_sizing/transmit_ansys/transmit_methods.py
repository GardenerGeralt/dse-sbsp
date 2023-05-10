

class Laser:
    def __init__(self, R_source, trans_eff, A_source, L):
        """
        :param dtr_eff: DC to RF efficiency [-]
        """
        self.R_source = R_source
        self.trans_eff = trans_eff
        self.A_source = A_source
        self.L = L
        self.flux = self.calcflux()
        ...

    def __str__(self, ):
        return f"\nLaser:\n" \
                 f"------------------\n" \
               f"    Flux at receiver : {self.flux} [W/m2],\n" \

               #f"    Cell area: {self.cell_area} [m2],\n" \
               #f"  Average mass: {self.av_mass} [kg],\n" \
               # f" Power density: {self.power_dens} [W/m2],\n" \
               # f"Specific power: {self.spec_power} [W/kg]."

    def calcflux(self):
        phi = self.R_source * self.A_source * self.trans_eff / self.L**2
        return phi

class Microwave:
    def __init__(self):
        ...
