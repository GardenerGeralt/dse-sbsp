import math


class Ait:

    def __init__(self, poi, nsats, M):
        self.poi = poi
        self.nsats = nsats
        self.M = M

    def getcost(self):

        cost = 30805.01*math.log((self.poi+2)*self.nsats)-69164.14
        inflation = 1.17273*1000
        weight = 0.01017*(self.M / 1000) + 0.23218

        return cost*inflation*(weight)

