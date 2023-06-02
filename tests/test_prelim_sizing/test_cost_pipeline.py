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
    pipeline = cstppl.CostPipeline(M)
    for n in range(1, 201, 1):
        costs = np.append(costs, [pipeline.gettotalcost()])
        launch = np.append(launch, pipeline.launchcost)
        prod = np.append(prod, pipeline.prodcost)
        ait = np.append(ait, pipeline.aitcost)
        dev = np.append(dev, pipeline.devcost)

    n_id = np.argmin(costs)
    cost_id = np.min(costs)


    # plt.clf()
    # x = np.arange(1,201, 1)
    # plt.title(F"System mass {M} kg and optimal n {np.argmin(costs)}")
    # plt.plot(n_id,cost_id, marker='o', markersize=5, color="red")
    #plt.xlabel("Number of Spacecraft [n]")
    #plt.ylabel("Total Mission costs [EUR (2023)]")
    # plt.plot(x, costs, color='black')
    #plt.plot(x, launch, color='green')
    #plt.plot(x, prod, color='blue')
    #plt.plot(x, ait, color='red')
    #plt.plot(x, dev, color='pink')
    # plt.show()
    #plt.savefig()

    # print(np.argmin(costs))
    # print(np.min(costs))
    # print(launch[n_id])
    # print(prod[n_id])
    # print(ait[n_id])
    # print(dev[n_id])






