import math

class Launcher:

    def __init__(self, price, mass):
        self.price = price
        self.mass = mass

    def getcost(self, mass):
        launches = math.ceil(mass/self.mass)
        cost = launches * self.price

        return cost