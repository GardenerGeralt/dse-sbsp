import math
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np


class Field:

    def __init__(self, devboundary, cilowbound, cihighbound, modelstrength):

        """
        Args:
            devboundary: deviation range for power and mass (amount of sigma's or float)
            cilowbound: minimum complexity value (negative for a simplified system)
            cihighbound: maximum complexity value to calculate (to prevent infinities)
            modelstrength: how quickly does complexity change with deviations from 'normal' situation
        """

        self.devboundary = devboundary
        self.cilowbound = cilowbound
        self.cihighbound = cihighbound
        self.strength = modelstrength
        self.precision = 0.005

    def miniaturise(self, pdev, mdev):
        ci = self.strength*math.exp(-0.4*(pdev*mdev)**3)*(pdev**2+mdev**2)
        if ci >= self.cihighbound*2:
            ci = self.cihighbound*2
        return ci

    def simplify(self, pdev, mdev):
        ci = ((2*self.strength*(pdev+mdev)**2+1)*math.exp(0.1*(pdev*mdev)**3)-1)/(math.exp(0.1*(pdev*mdev)**3)+1)

        return ci

    def scale(self, pdev, mdev):
        ci = self.strength*(pdev+mdev)**2

        return ci

    def getci(self, pdev, mdev):
            if abs(pdev)+abs(mdev) == abs(pdev+mdev):
                return self.scale(pdev,mdev)
            if pdev >= 0 > mdev:
                return self.miniaturise(pdev,mdev)
            if pdev <= 0 < mdev:
                return self.simplify(pdev,mdev)

    @np.vectorize
    def plotfieldsegmented(self):
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

        miniP = np.arange(0, self.devboundary, self.devboundary*self.precision)
        miniM = np.arange(-self.devboundary, 0, self.devboundary*self.precision)
        miniP, miniM = np.meshgrid(miniP, miniM)

        simplifyP = np.arange(-self.devboundary, 0, self.devboundary*self.precision)
        simplifyM = np.arange(0, self.devboundary, self.devboundary*self.precision)
        simplifyP, simplifyM = np.meshgrid(simplifyP, simplifyM)

        scaleP = np.arange(-self.devboundary, self.devboundary, self.devboundary*self.precision)
        scaleM = np.arange(-self.devboundary, self.devboundary, self.devboundary*self.precision)
        scaleP, scaleM = np.meshgrid(scaleP, scaleM)

        miniz = np.array([[0.0 for x in range(miniP.shape[0])] for y in range(miniP.shape[1])])
        simpz = np.array([[0.0 for x in range(simplifyP.shape[0])] for y in range(simplifyP.shape[1])])
        scalez = np.array([[0.0 for x in range(scaleP.shape[0])] for y in range(scaleP.shape[1])])

        for i in range(simplifyP.shape[0]):
            for j in range(simplifyP.shape[1]):
                simpz[i][j] = self.getci(simplifyP[i][j], simplifyM[i][j])
        for i in range(scaleP.shape[0]):
            for j in range(scaleP.shape[1]):
                scalez[i][j] = self.getci(scaleP[i][j], scaleM[i][j])

        for i in range(miniP.shape[0]):
            for j in range(miniP.shape[1]):
                miniz[i][j] = self.getci(miniP[i][j], miniM[i][j])

        surf1 = ax.plot_surface(miniP, miniM, miniz, cmap=cm.coolwarm,
                                linewidth=0, antialiased=True)
        surf2 = ax.plot_surface(simplifyP, simplifyM, simpz, cmap=cm.coolwarm,
                                linewidth=0, antialiased=True)
        surf3 = ax.plot_surface(scaleP, scaleM, scalez, cmap=cm.coolwarm,
                                linewidth=0, antialiased=True)

        ax.set_zlim(self.cilowbound, self.cihighbound)
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter('{x:.02f}')

        plt.show()

