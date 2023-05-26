import pytest
import numpy as np
import src.prelim_sizing.cost_ansys.cost_pipeline as cstppl
import src.prelim_sizing.complexity.field as fld
import matplotlib.pyplot as plt

class TestCostPipeline:

    M = 48620
    costs = np.array([])
    launch = np.array([])
    prod = np.array([])
    ait = np.array([])
    dev = np.array([])
    for n in range(1, 501, 1):
        pipeline = cstppl.CostPipeline(M, n)
        pipeline.populatecost()
        costs = np.append(costs, [pipeline.gettotalcost()])
        launch = np.append(launch, pipeline.launchcost)
        prod = np.append(prod, pipeline.prodcost)
        ait = np.append(ait, pipeline.aitcost)
        dev = np.append(dev, pipeline.devcost)

    plt.clf()
    x = np.arange(1,501, 1)
    plt.title(F"System mass {M} kg and n {np.argmin(costs)}")
    #plt.plot(x, costs, color='black')
    #plt.plot(x, launch, color='green')
    plt.plot(x, prod, color='blue')
    plt.plot(x, ait, color='red')
    #plt.plot(x, dev, color='pink')
    plt.show()
    n_id = np.argmin(costs)
    print(np.argmin(costs))
    print(np.min(costs))
    print(launch[n_id])
    print(prod[n_id])
    print(ait[n_id])
    print(dev[n_id])





