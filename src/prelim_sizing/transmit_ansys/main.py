import transmit_methods as tm
from src.plotting import plots as plt
import numpy as np

def main():
    return None

if __name__ = "__main__":


    L = np.arange(10000,100000)
    laser = tm.Laser(2.4e15, 0.25, 1, L)
    plt.line_plot(L, laser.flux)

