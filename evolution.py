import numpy as np
import pickle

mask = np.array([[0., -1., 1., 0., 1., 0., 1.]] * 3)  # no horizontal rotation
mask2 = np.array([[0., 0., 0., 0., 0., 1.5, 0.]] * 3)  # horizontal hand


class Population():

    def __init__(self, size, elite=None, mutation=None):
        if elite is None:
            self.individuals = [self._create_individual() for _ in range(size)]
        else:
            elite = [self._create_individual(e['weights'], e['id']) for e in elite]

            self.individuals = elite + self._mutate(elite, mutation)
            while len(self.individuals) < size:
                self.individuals += [self._create_individual()]

    def _mutate(self, elite, mutation):
        if mutation == 'crossover':
            if len(elite) % 2 == 1:
                elite = elite[:-1]
            children = [self._mutate_cross_over(elite[i], elite[i + 1]) for i in range(0, len(elite), 2)]
            return list(sum(children, ()))
        elif mutation == 'single_crossover':
            if len(elite) % 2 == 1:
                elite = elite[:-1]
            children = [self._mutate_single_cross_over(elite[i], elite[i + 1]) for i in range(0, len(elite), 2)]
            return list(sum(children, ()))
        elif mutation == 'random':
            return [self._mutate_individual(e) for e in elite]
        else:
            raise ValueError('unknown mutation: {}'.format(mutation))

    def _create_individual(self, weights=None, id=None):
        if weights is None:
            return {'weights': self._get_syn_weights(), 'distance': -1., 'id': id}
        else:
            return {'weights': weights, 'distance': -1., 'id': id}

    def _get_syn_weights(self):
        weights = (np.random.rand(3, 7) * 5)
        return (weights * mask + mask2).tolist()

    def _mutate_individual(self, individual):
        weights = individual['weights']
        weights += np.random.rand(3, 7) - .5
        weights *= mask
        weights += mask2
        return self._create_individual(weights.tolist())

    def _mutate_cross_over(self, individual1, individual2):
        weights1 = individual1['weights']
        weights2 = individual2['weights']

        mask1 = np.randon.randint(2, size=len(weights1))
        mask2 = np.ones(len(weights2)) - mask1

        new1 = self._create_individual((weights1 * mask1 + weights2 * mask2).tolist())
        new2 = self._create_individual((weights1 * mask2 + weights2 * mask1).tolist())
        return new1, new2

    def _mutate_single_cross_over(self, individual1, individual2):
        weights1 = individual1['weights']
        weights2 = individual2['weights']

        random = np.random.randint(len(weights1))

        mask1 = np.concatenate((np.ones(random), np.zeros(len(weights1) - random)))

        mask2 = np.ones(len(weights2)) - mask1

        new1 = self._create_individual((weights1 * mask1 + weights2 * mask2).tolist())
        new2 = self._create_individual((weights1 * mask2 + weights2 * mask1).tolist())
        return new1, new2

    def get_elite(self, size):
        size = min(size, len(self.individuals))
        return sorted(self.individuals, key=lambda i: i['distance'], reverse=True)[:size]

    def get_population_size(self):
        return len(self.individuals)

    def load(self, filename):
        with open(filename, 'r') as f:
            individuals = pickle.load(f)
        self.individuals = individuals


class EvolutionaryAlgo():

    def __init__(self, generation_size, population_size, seed=None, mutation='random'):
        self.seed = seed
        self.population_size = population_size
        self.generation_size = generation_size
        self.generations = [Population(population_size)]
        self.mutation = mutation

    def set_distance(self, distance, generation, individual):
        self.generations[generation].individuals[individual]['distance'] = distance

    def set_id(self, generation, individual):
        if self.get_id(generation, individual) is None:
            id = (generation, individual)
            self.generations[generation].individuals[individual]['id'] = id

    def get_id(self, generation, individual):
        return self.generations[generation].individuals[individual]['id']

    def get_weights(self, generation, individual):
        return self.generations[generation].individuals[individual]['weights']

    def mutate(self):
        elite = self.generations[-1].get_elite(self.population_size / 2)
        self.generations += [Population(self.population_size, elite=elite, mutation=self.mutation)]

    def _get_filename(self, generation):
        return 'evolution_results/generation_{}.pickle'.format(generation)

    def save(self, generation):
        filename = self._get_filename(generation)
        with open(filename, 'w') as f:
            pickle.dump(self.generations[generation].individuals, f)
        return filename

    def load(self, generation):
        filename = self._get_filename(generation)
        pop = Population(self.population_size)
        pop.load(filename)
        self.population_size = pop.get_population_size()
        self.generations = [pop]

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
