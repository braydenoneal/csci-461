import math
import random
import tkinter as tk

window_width = 640
window_height = 640
window_padding = 96
tile_margin = 32

root = tk.Tk()
root.geometry(f'{window_width}x{window_height}')
root.configure(background='#101010')

canvas = tk.Canvas(root, width=window_width, height=window_height, background='#181818',
                   bd=0, highlightthickness=0, relief='ridge')

canvas.pack(expand=True)
root.eval('tk::PlaceWindow . center')

run = True
population_size = 1000
mutation_chance = 0.08
display_size = 5


def fitness_of_permutation(permutation):
    total_distance = 0

    for i in range(len(permutation)):
        total_distance += math.dist(positions[permutation[i]], positions[permutation[(i + 1) % len(permutation)]])

    return total_distance


positions = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [5, 1], [5, 2], [5, 3], [5, 4],
             [5, 5], [4, 5], [3, 5], [2, 5], [1, 5], [0, 5], [0, 4], [0, 3], [0, 2], [0, 1]]

positions_size = len(positions)

tile_width = (window_width - 2 * window_padding - tile_margin * (display_size - 1)) // display_size
tile_height = (window_height - 2 * window_padding - tile_margin * (display_size - 1)) // display_size

best_genes = []

text = tk.Label(root, text='')
text.place(x=16, y=16)

while run:
    population = []

    for _ in range(population_size):
        order = list(range(positions_size))
        random.shuffle(order)
        population.append(order)

    fitness_counter = 0

    while fitness_counter < 16:
        population = sorted(population, key=lambda x: fitness_of_permutation(x))[:population_size // 2]

        text.config(text=f'Population Size: {population_size}\n'
                         f'Mutation Rate: {mutation_chance * 100}%\n'
                         f'Best Distance: {str(round(100 * fitness_of_permutation(population[0])))}')

        root.update()
        canvas.delete('all')

        if fitness_of_permutation(population[0]) <= 20:
            fitness_counter += 1

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

        for order in range(display_size ** 2):
            for i in range(positions_size):
                position1 = positions[population[order][i]]
                position2 = positions[population[order][(i + 1) % positions_size]]

                x_mod = order // round(display_size)
                y_mod = order % round(display_size)

                x1 = position1[0] * (tile_width // 5) + x_mod * (tile_margin + tile_width) + window_padding
                y1 = position1[1] * (tile_height // 5) + y_mod * (tile_margin + tile_height) + window_padding

                x2 = position2[0] * (tile_width // 5) + x_mod * (tile_margin + tile_width) + window_padding
                y2 = position2[1] * (tile_height // 5) + y_mod * (tile_margin + tile_height) + window_padding

                value = hex(round(64 + 191 * (i / (positions_size - 1))))[2:].rjust(2, '0')
                canvas.create_line(x1, y1, x2, y2, width=2, fill=f'#{value}{value}{value}')

        population = new_population

    population = sorted(population, key=lambda x: fitness_of_permutation(x))

    best_genes.append(population[0])

best_gene = sorted(best_genes, key=lambda x: fitness_of_permutation(x))[0]
