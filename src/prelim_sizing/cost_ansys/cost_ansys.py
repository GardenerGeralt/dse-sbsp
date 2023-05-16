import numpy as np


class Launcher:
    def __init__(self, max_launch_mass, launch_cost):
        """
        :param max_launch_mass:
        :param launch_cost:
        """
        self.max_launch_mass = max_launch_mass
        self.launch_cost = launch_cost

    def n_launches(self, payload_mass):
        """
        :param payload_mass:
        :return:
        """
        return np.ceil(payload_mass / self.max_launch_mass)

    def cost(self, payload_mass):
        """
        :param payload_mass:
        :return:
        """
        return self.launch_cost * self.n_launches(payload_mass)
