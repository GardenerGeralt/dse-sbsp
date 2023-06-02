import math


class Ait:

    def __init__(self, poi, M):
        self.poi = poi
        self.M = M

    def getcost(self, nsats):

        cost = 30805.01*math.log((self.poi+2)*nsats)-69164.14
        inflation = 1.17273*1000
        weight = 0.01017*(self.M / 1000) + 0.23218

        return cost*inflation*(weight)

