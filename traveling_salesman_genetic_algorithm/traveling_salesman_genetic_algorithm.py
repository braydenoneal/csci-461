import math
import random

population_size = 128
iterations = 4096

positions = [
    [0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [5, 1], [5, 2], [5, 3], [5, 4],
    [5, 5], [4, 5], [3, 5], [2, 5], [1, 5], [0, 5], [0, 4], [0, 3], [0, 2], [0, 1],
]

positions_size = len(positions)

population = []

for _ in range(population_size):
    order = list(range(positions_size))
    random.shuffle(order)
    population.append(order)


def fitness_of_permutation(permutation):
    total_distance = 0

    for i in range(len(permutation) - 1):
        total_distance += math.dist(positions[permutation[i]], positions[permutation[i + 1]])

    return total_distance


for iteration in range(iterations):
    population = sorted(population, key=lambda x: fitness_of_permutation(x))[:population_size // 2]

    best_distance = round(fitness_of_permutation(population[0]), 1)

    print(f'{best_distance} {iteration} of {iterations}')

    new_children = []

    random.shuffle(population)

    for crossover in range(population_size // 2 - 1):
        parent1 = population[crossover]
        parent2 = population[crossover + 1]

        split_position = positions_size // 2

        child1 = parent1[:split_position]
        indices = []

        for order in parent1[split_position:]:
            indices.append(parent2.index(order))

        for order in sorted(indices):
            child1.append(parent2[order])

        child2 = parent2[:split_position]
        indices = []

        for order in parent2[split_position:]:
            indices.append(parent1.index(order))

        for order in sorted(indices):
            child2.append(parent1[order])

        for permutation in (child1, child2):
            if random.random() < 0.2:
                index1 = random.randint(0, positions_size - 1)
                index2 = random.randint(0, positions_size - 1)

                temp = permutation[index1]
                permutation[index1] = permutation[index2]
                permutation[index2] = temp

        new_children.append(child1)
        new_children.append(child2)

    for child in new_children:
        population.append(child)

population = sorted(population, key=lambda x: fitness_of_permutation(x))[:math.ceil(population_size * 0.5)]
print(population[0])
