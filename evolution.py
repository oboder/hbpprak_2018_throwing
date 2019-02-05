import numpy as np
import pickle


class Population():

    def __init__(self, size, elite=None):
        if elite is None:
            self.individuals = [self._create_individual() for _ in range(size)]
        else:
            elite = [self._create_individual(e['weights']) for e in elite]
            self.individuals = elite + [self._mutate_individual(e) for e in elite]
            if len(self.individuals) < size:
                self.individuals += [self._create_individual()]

    def _create_individual(self, weights=None):
        if weights is None:
            return {'weights': self._get_syn_weights(), 'distance': -1.}
        else:
            return {'weights': weights, 'distance': -1.}

    def _get_syn_weights(self):
        return (np.random.rand(3, 7) * 5).tolist()

    def _mutate_individual(self, individual):
        weights = individual['weights']
        weights += np.random.rand(3, 7) -.5
        return self._create_individual(weights.tolist())

    def get_elite(self, size):
        size = min(size, len(self.individuals))
        return sorted(self.individuals, key=lambda i: i['distance'], reverse=True)[:size]


class EvolutionaryAlgo():

    def __init__(self, generation_size, population_size, seed=None):
        self.seed = seed
        self.population_size = population_size
        self.generation_size = generation_size
        self.generations = [Population(population_size)]

    def set_distance(self, distance, generation, individual):
        self.generations[generation].individuals[individual]['distance'] = distance

    def get_weights(self, generation, individual):
        return self.generations[generation].individuals[individual]['weights']

    def mutate(self):
        elite = self.generations[-1].get_elite(self.population_size/2)
        self.generations += [Population(self.population_size, elite=elite)]

    def save(self, generation):
        filename = 'evolution_results/generation_{}.pickle'.format(generation)
        with open(filename, 'w') as f:
            pickle.dump(self.generations[generation].individuals, f)
            print('Saved Generation {} to {}'.format(generation, filename))


# evol = EvolutionaryAlgo(3,2)
#
# population = evol.generations[0]
#
# for ind in range(len(population.individuals)):
#     evol.set_distance(1000.-ind, 0, ind)
#
# print(evol.generations[0].individuals)
# population = evol.generations[0]
#
# print(sorted(population.individuals, key=lambda i: i['distance'], reverse=True))
#
# evol.mutate()
# print(evol.generations[1].individuals)
