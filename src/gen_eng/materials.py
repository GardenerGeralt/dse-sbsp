

class Material:
    def __init__(self, density):
        self.density = density


class StructuralMaterial(Material):
    def __init__(self, density, elastic_mod, shear_mod, yield_strength, ultimate_strength, poisson_ratio, lin_therm_exp_coef,
                 alpha_crippling_correction=None, n_buckling_correction=None):
        super().__init__(density)
        self.elastic_mod = elastic_mod
        self.shear_mod = shear_mod
        self.yield_strength = yield_strength
        self.ultimate_strength = ultimate_strength
        self.poisson_ratio = poisson_ratio
        self.lin_therm_exp_coef = lin_therm_exp_coef

        self.alpha_crippling_correction = alpha_crippling_correction
        self.n_buckling_correction = n_buckling_correction


class Propellant(Material):
    def __init__(self, density, spec_impulse):
        super().__init__(density)
        self.spec_impulse = spec_impulse
