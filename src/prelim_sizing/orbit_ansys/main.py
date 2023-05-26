from orbitfull import Orbit, OrbitPlot
from orbit_params import orbpar



if __name__ == "__main__":
    # orb = Orbit(*orbpar)
    orbplot = OrbitPlot(orbpar)
    orbplot.plot_all()
    orbplot.add_slider()
    orbplot.show()
