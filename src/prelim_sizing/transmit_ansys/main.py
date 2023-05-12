import transmit_methods as tm
from src.plotting import plots as plt
import numpy as np

def main():
    return None


if __name__ == "__main__":
    trumpf8002laser = tm.Laser(wavelength=1030e-9, m2=2.5, w0=0.05, P_0=8000, z=100000)
    print(trumpf8002laser.__str__())

    # L = np.arange(10000,100000)
    # laser = tm.Laser(2.4e15, 0.25, 1, L)
    # .line_plot(L, laser.flux)

