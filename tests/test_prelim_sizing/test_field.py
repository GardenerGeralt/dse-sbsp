import pytest
import numpy as np
from src.prelim_sizing.complexity import field as fld

class TestField:

    complexityfield = fld.Field(3,-1,8,0.3)

    fld.Field.plotfieldsegmented(complexityfield)
