import math
import random
import tkinter as tk

window_width = 1000
window_height = 1000

root = tk.Tk()
root.geometry(f'{window_width}x{window_height}')
root.configure(background='#101010')

canvas = tk.Canvas(root, width=window_width, height=window_height, background='#101010',
                   bd=0, highlightthickness=0, relief='ridge')

canvas.pack(expand=True)
root.eval('tk::PlaceWindow . center')

population_iterations = 32
population_size = 128
iterations = 256
mutation_chance = 0.08


def fitness_of_permutation(permutation):
    total_distance = 0

    for i in range(len(permutation) - 1):
        total_distance += math.dist(positions[permutation[i]], positions[permutation[i + 1]])

    return total_distance


positions = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [5, 1], [5, 2], [5, 3], [5, 4],
             [5, 5], [4, 5], [3, 5], [2, 5], [1, 5], [0, 5], [0, 4], [0, 3], [0, 2], [0, 1]]

positions_size = len(positions)

best_genes = []

for population_iteration in range(population_iterations):
    population = []

    for _ in range(population_size):
        order = list(range(positions_size))
        random.shuffle(order)
        population.append(order)

    for iteration in range(iterations):
        population = sorted(population, key=lambda x: fitness_of_permutation(x))[:population_size // 2]

        new_population = []

        random.shuffle(population)

        child_iter = 0

        for crossover in range(population_size // 2):
            parents = (random.choice(population), random.choice(population))

            split_position = random.randint(0, positions_size)

            for parent in (parents, parents[::-1]):
                child = parent[0][:split_position]
                indices = []

                for order in parent[0][split_position:]:
                    indices.append(parent[1].index(order))

                for order in sorted(indices):
                    child.append(parent[1][order])

                if random.random() < mutation_chance:
                    index1 = random.randint(0, positions_size - 1)
                    index2 = random.randint(0, positions_size - 1)

                    temp = child[index1]
                    child[index1] = child[index2]
                    child[index2] = temp

                new_population.append(child)

                for i in range(positions_size - 1):
                    position1 = positions[child[i]]
                    position2 = positions[child[i + 1]]

                    x_mod = child_iter // round(math.sqrt(population_size))
                    y_mod = child_iter % round(math.sqrt(population_size))

                    x1 = position1[0] * 10 + x_mod * 80
                    y1 = position1[1] * 10 + y_mod * 80

                    x2 = position2[0] * 10 + x_mod * 80
                    y2 = position2[1] * 10 + y_mod * 80

                    value = hex(round(64 + 191 * (i / (positions_size - 1))))[2:].rjust(2, '0')
                    canvas.create_line(x1, y1, x2, y2, width=2, fill=f'#{value}{value}{value}')

                child_iter += 1

        population = new_population

        root.update()
        canvas.delete('all')

    population = sorted(population, key=lambda x: fitness_of_permutation(x))

    best_genes.append(population[0])

best_gene = sorted(best_genes, key=lambda x: fitness_of_permutation(x))[0]
