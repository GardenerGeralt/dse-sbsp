

class Launcher:

    def __init__(self, price, mass):
        self.price = price
        self.mass = mass

    def getcost(self, mass):
        launches = mass/self.mass
        cost = launches * self.price

        return cost