import numpy as np

MISSION_DURATION = 25  # [yrs]


class ChemicalPropulsion:
    def __init__(self, dv_insertion, dv_st_keeping, dv_eol):
        """
        :param dv_insertion: Delta V required for orbit insertion [m/s]
        :param dv_st_keeping: Delta V required for station keeping [m/s/yrs]
        :param dv_eol: Delta V required for end of life manoeuvres [m/s/year]
        """

        self.dv_insertion = dv_insertion
        self.dv_st_keeping = dv_st_keeping
        self.dv_eol = dv_eol

    def calc_delta_V(self):
        return sum([self.dv_insertion, self.dv_st_keeping * MISSION_DURATION, self.dv_eol])
