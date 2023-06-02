import math


class Production:

    def __init__(self, mass):
        self.mass = mass
        self.learning = 0.8

    def t1cost(self, mass, n):
        satmass = mass / n
        # print(satmass)
        t1cost = 283.5 * satmass ** 0.716
        # t1cost = 90 * satmass
        # print(t1cost)
        return t1cost * 1000 * 1.27131

    def getcost(self, mass, n):
        cost = self.t1cost(mass, n) * n ** (1 + math.log(self.learning) / math.log(2))
        euros = cost

        return euros
