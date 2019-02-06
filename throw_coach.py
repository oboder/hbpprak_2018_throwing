from hbp_nrp_virtual_coach.virtual_coach import VirtualCoach
import std_msgs
import time
import logging
import rospy

from evolution import EvolutionaryAlgo

# disable global logging from the virtual coach
logging.disable(logging.INFO)
logging.getLogger('rospy').propagate = False
logging.getLogger('rosout').propagate = False

brain_template = '''
# -*- coding: utf-8 -*-
"""
Tutorial brain for the throwing experiment
"""

# pragma: no cover
__author__ = 'Jacques Kaiser'

from hbp_nrp_cle.brainsim import simulator as sim
import numpy as np

n_sensors = 3
n_motors = 7

sensors = sim.Population(n_sensors, cellclass=sim.IF_curr_exp())
motors = sim.Population(n_motors, cellclass=sim.IF_curr_exp())
sim.Projection(sensors, motors, sim.AllToAllConnector(),
               sim.StaticSynapse(weight={syn_weight}))

circuit = sensors + motors

'''

curr_cylinder_distance = None


def cylinder_callback(distance):
    global curr_cylinder_distance
    curr_cylinder_distance = distance.data


def subscribe_cylinder_distance():
    rospy.Subscriber('/cylinder_distance', std_msgs.msg.Float32, cylinder_callback)


def test_weights(sim, weights):
    syn_weights = {'syn_weight': weights}
    brain_file = brain_template.format(**syn_weights)
    sim.edit_brain(brain_file)
    sim.start()

    # wait for sim to be finished
    while curr_cylinder_distance is None:
        # print('[{}] still waiting...'.format(curr_sim_time))
        time.sleep(2)

    distance = curr_cylinder_distance

    # reset distance
    global curr_cylinder_distance
    curr_cylinder_distance = None

    # reset sim
    sim.reset('full')
    return distance


def main():
    # logging config
    logging.basicConfig(
        filename='/home/nrpuser/.opt/nrpStorage/template_manipulation_0/evolution_results/evolution.log', filemode='a')
    logger = logging.getLogger('evolution')
    fh = logging.FileHandler('/home/nrpuser/.opt/nrpStorage/template_manipulation_0/evolution_results/evolution.log')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    subscribe_cylinder_distance()

    # log into the virtual coach
    vc = VirtualCoach(environment='local', storage_username='nrpuser', storage_password='password')

    # start simulation
    logger.warning('start expe !!!')
    sim = vc.launch_experiment('template_manipulation_0')

    # create evolution
    num_generations = 5
    population_size = 4
    evol = EvolutionaryAlgo(num_generations, population_size)

    for gen in range(evol.generation_size):
        logger.warning('Generation: {}/{}'.format(gen + 1, num_generations))
        for individual in range(evol.population_size):
            logger.warning('Individual: {}/{}'.format(individual + 1, population_size))

            # get weights
            weights = evol.get_weights(gen, individual)

            # run simulation
            distance = test_weights(sim, weights)

            # save distance
            evol.set_distance(distance, gen, individual)
            logger.warning('Distance: {}'.format(distance))

        # save weights
        filen = evol.save(gen)
        logger.warning('Saved Generation {} to {}'.format(gen, filen))

        # mutate generation
        if gen < evol.generation_size - 1:
            evol.mutate()

    # stop simulation
    sim.stop()

    # print best weights per generation
    for g in evol.generations:
        logger.warning("Elite:")
        logger.warning(g.get_elite(1))


if __name__ == '__main__':
    main()
