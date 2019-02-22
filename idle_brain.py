# -*- coding: utf-8 -*-
"""
Tutorial brain for the baseball experiment
"""

# pragma: no cover
__author__ = 'Jacques Kaiser'

from hbp_nrp_cle.brainsim import simulator as sim
import numpy as np

n_sensors = 3
n_motors = 7
np.random.seed(42)
weights = np.random.rand(3,7) * 5

sensors = sim.Population(n_sensors, cellclass=sim.IF_curr_exp())
motors = sim.Population(n_motors, cellclass=sim.IF_curr_exp())
sim.Projection(sensors, motors, sim.AllToAllConnector(),
               sim.StaticSynapse(weight=weights))

circuit = sensors + motors
