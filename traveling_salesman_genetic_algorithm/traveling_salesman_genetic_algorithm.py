import math
import random
import time

import numpy as np

initial_population_size = 64
iterations = 20_000

positions = np.array([
    [0, 0], [1, 0], [2, 0], [3, 0], [4, 0],
    [5, 0], [5, 1], [5, 2], [5, 3], [5, 4],
    [5, 5], [4, 5], [3, 5], [2, 5], [1, 5],
    [0, 5], [0, 4], [0, 3], [0, 2], [0, 1],
])

population = []

for _ in range(initial_population_size):
    population.append(np.random.permutation(np.arange(len(positions))))


def fitness_of_permutation(permutation):
    total_distance = 0

    for i in range(len(permutation) - 1):
        total_distance += math.dist(positions[permutation[i]], positions[permutation[i + 1]])

    return total_distance


step = 0

for iteration in range(iterations):
    population = sorted(population, key=lambda x: fitness_of_permutation(x))

    best_distance = fitness_of_permutation(population[0])

    step %= 4

    loading_chars = ["-", "\\", "|", "/"]

    print(f'{best_distance} {loading_chars[step]}', end='')
    time.sleep(0.2)
    print('\b' * (len(str(best_distance)) + 2), end='')

    step += 1

    parent1 = population[0]
    parent2 = population[1]

    split_position = len(positions) // 2

    child1 = np.concatenate((parent1[:split_position], parent2[split_position:]))
    child2 = np.concatenate((parent2[:split_position], parent1[split_position:]))

    for permutation in population:
        if random.random() < 0.05:
            index1 = random.randint(0, len(positions) - 1)
            index2 = random.randint(0, len(positions) - 1)

            temp = permutation[index1]
            permutation[index1] = permutation[index2]
            permutation[index2] = temp

    population.append(child1)
    population.append(child2)

print(population[0])
