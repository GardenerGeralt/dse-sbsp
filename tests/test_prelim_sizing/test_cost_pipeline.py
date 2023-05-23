import pytest
import numpy as np
import src.prelim_sizing.cost_ansys.cost_pipeline as cstppl
import src.prelim_sizing.complexity.field as fld

class TestCostPipeline:
    costs = np.array([])
    for i in range(1, 5000):
        pipeline = cstppl.CostPipeline(63550, i)
        pipeline.populatecost()
        costs = np.append(costs, [pipeline.gettotalcost()])
    print(np.argmin(costs))
    print('tot', costs[np.argmin(costs)]*1e-9)
