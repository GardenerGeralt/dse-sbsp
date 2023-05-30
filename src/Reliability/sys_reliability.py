import math
import sys
import matplotlib.pyplot as plt
import numpy as np


class SystemReliability:

    def __init__(self, req_sats, sys_reliability, sat_reliability):
        if sys_reliability >= sat_reliability:
            print('Incompatible Configuration...')
            sys.exit()
        self.sats = req_sats
        self.reliability = sys_reliability
        self.sat_reliability = sat_reliability
        self.sat_yr_reliability = None
        self.mission_duration = 25

    def getBuffer(self):
        i=0
        rate = 0
        while rate <= self.reliability:
            j=i
            rate = 0
            while j >= 0:
                rate = rate + math.comb(self.sats+i,j) * self.sat_reliability**(self.sats+i)*(1-self.sat_reliability)**j
                j-=1
            i += 1
        self.sat_yr_reliability = rate**(1/self.mission_duration)
        return i-1

    def getReqSatRel(self):
        if self.sat_yr_reliability == None:
            self.getBuffer()
        else:
            pass

        return self.sat_yr_reliability

    def costinfo(self, budget, sat_cost):
        fail_price = np.array([])
        sat_price = np.array([])
        i = 0
        rate = 0
        while rate <= self.reliability:
            j = i
            rate = 0
            while j >= 0:
                rate = rate + math.comb(self.sats + i, j) * self.sat_reliability ** (self.sats + i) * (
                            1 - self.sat_reliability) ** j
                j -= 1
            fail_price = np.append(fail_price, (1-rate) * budget)
            sat_price = np.append(sat_price, i * sat_cost)
            i += 1
        x = np.arange(0,len(fail_price))
        plt.plot(x, fail_price)
        plt.plot(x, sat_price)
        plt.show()
        return