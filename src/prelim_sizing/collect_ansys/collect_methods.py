
SOLAR_IRRADIANCE_1AU = 1361.0           # [W/m2]
STEFAN_BOLTZMANN_CONST = 5.6703e-8      # [W/m2/K4]


class SolarCell:
    def __init__(self, eff, cell_area, av_mass, concentration, op_temp, name="PV Cell"):
        """
        :param eff: pv cell efficiency [-]
        :param cell_area: single pv cell area [m2]
        :param av_mass: single pv cell mass [kg]
        :param concentration: solar irradiance concentration [suns]
        :param op_temp: pv cell operating temperature [K]
        :param name: name of the pv cell
        """
        self.eff = eff
        self.cell_area = cell_area
        self.av_mass = av_mass
        self.concentration = concentration
        self.op_temp = op_temp
        self.name = name

        self.power_dens = self._calc_power_dens()
        self.spec_power = self._calc_spec_power()

    def __str__(self):
        return f"\n{self.name}:\n" \
               f"------------------\n" \
               f"           Efficiency: {self.eff} [-],\n" \
               f"            Cell area: {self.cell_area:.4e} [m2],\n" \
               f"         Average mass: {self.av_mass:.4e} [kg],\n" \
               f"        Concentration: {self.concentration} [suns],\n" \
               f"        Power density: {self.power_dens:.4e} [W/m2],\n" \
               f"       Specific power: {self.spec_power:.4e} [W/kg],\n" \
               f"Operating temperature: {self.op_temp:.4e} [K]."

    def _calc_power_dens(self):
        return SOLAR_IRRADIANCE_1AU * self.concentration * self.eff

    def _calc_spec_power(self):
        return SOLAR_IRRADIANCE_1AU * self.concentration * self.eff * self.cell_area / self.av_mass

    def size(self, power_req):
        area = power_req / self.power_dens
        mass = power_req / self.spec_power
        return area, mass


class Concentrator:
    def __init__(self, surface_density, reflectivity, name="Solar Concentrator"):
        """
        :param surface_density: surface density of the concentrator material [kg/m2]
        :param reflectivity: reflectivity of the concentrator [-]
        :param name: name of the concentrator
        """
        self.surface_density = surface_density
        self.reflectivity = reflectivity
        self.name = name

    def __str__(self):
        return f"\n{self.name}:\n" \
               f"------------------\n" \
               f"Surface density: {self.surface_density:.4e} [kg/m2],\n" \
               f"   Reflectivity: {self.reflectivity} [-]."

    def size(self, power_reflect):
        area = power_reflect / self.reflectivity / SOLAR_IRRADIANCE_1AU
        mass = self.surface_density * area
        return area, mass


class Radiator:
    def __init__(self, emissivity, density, thickness, name="Radiator"):
        """
        :param emissivity: emissivity of the radiator [-]
        :param density: density of the radiator material [kg/m3]
        :param thickness: thickness of the radiator [m]
        :param name: name of the radiator
        """
        self.emissivity = emissivity
        self.density = density
        self.thickness = thickness
        self.name = name

    def __str__(self):
        return f"\n{self.name}:\n" \
               f"------------------\n" \
               f"Emissivity: {self.emissivity} [-],\n" \
               f"   Density: {self.density:.4e} [kg/m3],\n" \
               f" Thickness: {self.thickness:.4e} [m]."

    def size(self, power_abs, op_temp, pv_area):
        emission_area = power_abs / (self.emissivity * STEFAN_BOLTZMANN_CONST * op_temp ** 4)
        if emission_area > pv_area:
            area = emission_area - pv_area
        else:
            area = 0
        mass = area * self.density * self.thickness
        return area, mass


class Collector:
    def __init__(self, pv_cell: SolarCell, concentrator: Concentrator, radiator: Radiator, name="Solar Collector"):
        """
        :param pv_cell:
        :param concentrator:
        :param name:
        """
        self.pv_cell = pv_cell
        self.concentrator = concentrator
        self.radiator = radiator
        self.name = name

    def size(self, power_req, total=False):
        power_reflected = power_req / self.pv_cell.eff
        power_absorbed = power_reflected * (1 - self.pv_cell.eff)

        pv_area, pv_mass = self.pv_cell.size(power_req)

        concentr_area, concentr_mass = 0, 0
        if self.pv_cell.concentration > 1:
            concentr_area, concentr_mass = self.concentrator.size(power_reflected)

        radiator_area, radiator_mass = self.radiator.size(power_absorbed, self.pv_cell.op_temp, pv_area)

        if not total:
            areas = {"PV Cell": pv_area, "Concentrator": concentr_area, "Radiator": radiator_area}
            masses = {"PV Cell": pv_mass, "Concentrator": concentr_mass, "Radiator": radiator_mass}
            return areas, masses
        elif total:
            total_area = max([pv_area, concentr_area])
            total_mass = pv_mass + concentr_mass + radiator_mass
            return total_area, total_mass
