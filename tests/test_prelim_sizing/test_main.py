import pytest
import numpy as np
import pandas as pd
from src.prelim_sizing import main as pm
from src.prelim_sizing.collect_ansys import collect_methods as cm


COLLECTORS = pd.DataFrame({'Efficiency [-]': [0.30],
                           'Cell area [m2]': [3e-3],
                           'Average cell mass [kg]': [2e-3],
                           'Concentration [suns]': [10]},
                          index=['Test collector'])
TRANSMITTERS = pd.DataFrame({'Frequency [Hz]': [2e14, 5e9],
                             'TX efficiency [-]': [0.4, 0.9],
                             'RX efficiency [-]': [0.3, 0.8],
                             'TX gain [dB]': [np.nan, 60],
                             'RX gain [dB]': [np.nan, 60],
                             'Min. beam width [m]': [0.1, np.nan],
                             'M squared [-]': [3, np.nan],
                             'Spec. mass [kg/W]': [20e-3, 1e-3]},
                            index=['Test laser', 'Test microwave'])
ORBITS = pd.DataFrame({'Pericenter [m]': [750e3],
                       'Eccentricity [-]': [0.5],
                       'Inclination [deg]': [47.87]},
                      index=['Test orbit'])
LAUNCHERS = pd.DataFrame({'Max payload mass [kg]': [10000],
                          'Cost per launch [M$]': [100]},
                         index=['Test launcher'])


class TestCreate:
    test_laser_design = ('Test laser concept',
                         pd.Series(['Test collector', 'Test laser', 'Test orbit',
                                    'Test single sc mass', 'Test launcher'],
                                   index=['Collector', 'Transmitter', 'Orbit',
                                          'Single sc mass', 'Launcher']))
    test_micro_design = ('Test microwave concept',
                         pd.Series(['Test collector', 'Test microwave', 'Test orbit',
                                    'Test single sc mass', 'Test launcher'],
                                   index=['Collector', 'Transmitter', 'Orbit',
                                          'Single sc mass', 'Launcher']))

    def test_create_collector(self):
        corr_solar_cell = cm.SolarCell(0.30, 3e-3, 2e-3, 10, 393, 'Test collector')
        corr_concentrator = cm.Concentrator(0.15, 0.9)
        corr_radiator = cm.Radiator(0.9, 1700, 125e-6)
        correct_collector = cm.Collector(corr_solar_cell, corr_concentrator, corr_radiator)

        assert pm.create_collector(self.test_laser_design) == correct_collector

    def test_create_transmitter(self):
        ...

    def test_create_orbit(self):
        ...

    def test_create_launcher(self):
        ...


class TestMain:
    ...