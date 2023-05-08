

class Material:
    def __init__(self, density):
        self.density = density


class StructuralMaterial(Material):
    def __init__(self, density, elastic_mod, tens_strength, lin_therm_exp_coef):
        super().__init__(density)
        self.elastic_mod = elastic_mod
        self.tens_strength = tens_strength
        self.lin_therm_exp_coef = lin_therm_exp_coef


class Propellant(Material):
    def __init__(self, density, spec_impulse):
        super().__init__(density)
        self.spec_impulse = spec_impulse
