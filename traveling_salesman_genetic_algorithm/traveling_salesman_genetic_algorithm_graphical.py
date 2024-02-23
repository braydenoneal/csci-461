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
population_size = 1000
iterations = 4096
mutation_chance = 0.08


def fitness_of_permutation(permutation):
    total_distance = 0

    for i in range(len(permutation)):
        total_distance += math.dist(positions[permutation[i]], positions[permutation[(i + 1) % len(permutation)]])

    return total_distance


positions = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [5, 1], [5, 2], [5, 3], [5, 4],
             [5, 5], [4, 5], [3, 5], [2, 5], [1, 5], [0, 5], [0, 4], [0, 3], [0, 2], [0, 1]]

positions_size = len(positions)

best_genes = []

text = tk.Label(root, text='')
text.place(x=16, y=16)

for population_iteration in range(population_iterations):
    population = []

    for _ in range(population_size):
        order = list(range(positions_size))
        random.shuffle(order)
        population.append(order)

    for iteration in range(iterations):
        if fitness_of_permutation(population[0]) > 20:
            new_population = []

            random.shuffle(population)

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

                    for gene in range(positions_size):
                        if random.random() < mutation_chance * (gene + 1):
                            index1 = random.randint(0, positions_size - 1)
                            index2 = random.randint(0, positions_size - 1)

                            temp = child[index1]
                            child[index1] = child[index2]
                            child[index2] = temp
                        else:
                            break

                    new_population.append(child)

            display_size = 1

            for order in range(display_size):
                for i in range(positions_size):
                    position1 = positions[population[order][i]]
                    position2 = positions[population[order][(i + 1) % positions_size]]

                    x_mod = order // round(math.sqrt(display_size))
                    y_mod = order % round(math.sqrt(display_size))

                    x1 = position1[0] * 10 + x_mod * 80 + 64
                    y1 = position1[1] * 10 + y_mod * 80 + 64

                    x2 = position2[0] * 10 + x_mod * 80 + 64
                    y2 = position2[1] * 10 + y_mod * 80 + 64

                    value = hex(round(64 + 191 * (i / (positions_size - 1))))[2:].rjust(2, '0')
                    canvas.create_line(x1, y1, x2, y2, width=2, fill=f'#{value}{value}{value}')

            population = sorted(new_population, key=lambda x: fitness_of_permutation(x))[:population_size // 2]

            text.config(text=f'Best Distance: {str(round(fitness_of_permutation(population[0]), 2))}')

            root.update()
            canvas.delete('all')

    population = sorted(population, key=lambda x: fitness_of_permutation(x))

    best_genes.append(population[0])

best_gene = sorted(best_genes, key=lambda x: fitness_of_permutation(x))[0]
