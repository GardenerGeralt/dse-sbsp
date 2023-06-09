from orbitfull import Orbit, OrbitPlot
from orbit_params import orbpar



if __name__ == "__main__":
    #orb = Orbit(*orbpar)
    orbplot = OrbitPlot(orbpar)
    #orbplot.plot_angle()
    orbplot.plot_all()

    #orbplot.vary_sc()
    #orbplot.add_slider()
    #orbplot.animate_plot()
    #print(len(orbplot.fig.data))
    orbplot.show()