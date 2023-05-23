import pandas as pd
import numpy as np
import scipy as sp
import os
import sys
import matplotlib.pyplot as plt


class CiDatabase:

    def __init__(self, field):
        self.database = np.array([])
        self.distributions = np.array([])
        self.cis = np.array([0,0,0])
        self.getmissiondata()
        self.getdistributions()
        self.populatedb(field)

    def getmissiondata(self):
        df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'missions.csv'))
        self.database = df.to_numpy()

    def getdistributions(self):
        df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'subsys_distribution.csv'))
        self.distributions = df.to_numpy()

    def populatedb(self, instance):
        for i in range(self.database.shape[0]):
            ci = 0
            for j in range(self.distributions.shape[0]):
                # print(self.database[i][j+2], self.distributions[j][4])
                devP = (self.database[i][j+2]-self.distributions[j][4])/self.distributions[j][5]
                devM = (self.database[i][j+self.distributions.shape[0]+2]-self.distributions[j][1])/self.distributions[j][2]
                ci = ci + instance.getci(devP, devM)*self.distributions[j][3]

            data = [self.database[i][0], self.database[i][1], ci]
            # print("data")
            # print(data)
            # print("cis")
            # print(self.cis)
            self.cis = np.vstack((self.cis, data))

        df = pd.DataFrame(self.cis)
        df = df.drop(index=0)
        path = os.path.join(os.path.dirname(__file__))
        df.to_csv(path+'/cis.csv', header=False, index=False)

    def getlinearregressor(self):
        df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'cis.csv'))
        cilist = df.to_numpy()
        costvals = np.array([])
        civals = np.array([])
        for i in range(cilist.shape[0]):
            costvals = np.append(costvals, cilist[i][1])
            civals = np.append(civals, cilist[i][2])
        # print(cilist)
        regressor = sp.stats.linregress(civals, costvals)
        slope = regressor.slope
        intercept = regressor.intercept
        rvalue = regressor.rvalue
        plt.scatter(civals, costvals)
        cicustom = np.arange(0.0, 6.5, 0.5)
        costcustom = cicustom*slope+intercept
        plt.plot(cicustom, costcustom)
        # plt.show()
        return slope, intercept, rvalue
