import pytest
import numpy as np
import src.prelim_sizing.cost_ansys.cost_pipeline as cstppl


class TestCostPipeline:
    sats = np.arange(1,5000, 10)
    costs = np.array([])
    for sats in range(len(sats)):
        pipeline = cstppl.CostPipeline(100000, sats+1)
        pipeline.populatecost()
        costs = np.append(costs, pipeline.gettotalcost())

    print(min(costs))