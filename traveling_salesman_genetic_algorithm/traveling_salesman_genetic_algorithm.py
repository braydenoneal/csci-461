import math
import random

population_iterations = 16
population_size = 128
iterations = 1024
print_iterations = False


def fitness_of_permutation(permutation):
    total_distance = 0

    for i in range(len(permutation) - 1):
        total_distance += math.dist(positions[permutation[i]], positions[permutation[i + 1]])

    return total_distance


positions = [
    [0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [5, 1], [5, 2], [5, 3], [5, 4],
    [5, 5], [4, 5], [3, 5], [2, 5], [1, 5], [0, 5], [0, 4], [0, 3], [0, 2], [0, 1],
]

positions_size = len(positions)

best_genes = []

for _ in range(population_iterations):
    population = []

    for _ in range(population_size):
        order = list(range(positions_size))
        random.shuffle(order)
        population.append(order)

    for iteration in range(iterations):
        population = sorted(population, key=lambda x: fitness_of_permutation(x))[:population_size // 2]

        if print_iterations:
            print(f'{round(fitness_of_permutation(population[0]), 1)} {iteration + 1} of {iterations}')

        new_population = []

        random.shuffle(population)

        for crossover in range(population_size // 2):
            parent1 = random.choice(population)
            parent2 = random.choice(population)

            split_position = positions_size // 2

            for parents in ((parent1, parent2), (parent2, parent1)):
                child = parents[0][:split_position]
                indices = []

                for order in parents[0][split_position:]:
                    indices.append(parents[1].index(order))

                for order in sorted(indices):
                    child.append(parents[1][order])

                if random.random() < 0.2:
                    index1 = random.randint(0, positions_size - 1)
                    index2 = random.randint(0, positions_size - 1)

                    temp = child[index1]
                    child[index1] = child[index2]
                    child[index2] = temp

                new_population.append(child)

        population = new_population

    best_genes.append(sorted(population, key=lambda x: fitness_of_permutation(x))[0])

best_gene = sorted(best_genes, key=lambda x: fitness_of_permutation(x))[0]

print(f'Number of Population Iterations: {population_iterations}\n'
      f'Population Size: {population_size}\n'
      f'Number of Generations: {iterations}\n'
      f'Best Gene: {best_gene}\n'
      f'Best Gene Distance: {round(fitness_of_permutation(best_gene), 1)}')
