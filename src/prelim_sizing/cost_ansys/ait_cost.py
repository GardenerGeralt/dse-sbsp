import math


class Ait:

    def __init__(self, poi, nsats):
        self.poi = poi
        self.nsats = nsats

    def getcost(self):
        cost = 30805.01*math.log((self.poi+2)*self.nsats)-69164.14
        return cost*1.17273*1000

