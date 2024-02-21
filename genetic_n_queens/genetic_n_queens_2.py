import random

BOARD_SIZE = 8  # Use 8x8 boards
POPULATION_SIZE = 50  # How many boards are in the population?
GENERATIONS = 200  # Times we will cull, make children,and mutate
MUTATION_FREQUENCY = 20  # Percentage of the time to mutate


class Board:
    def __init__(self):  # Create a new game board
        self.list = [random.randint(1, BOARD_SIZE) for i in range(BOARD_SIZE)]
        self.value = 0
        self.set_value()

    def make_child(self, board2):
        split_point = random.randint(1, BOARD_SIZE - 1)
        board = Board()
        board.list = self.list[:split_point] + board2.list[split_point:]
        board.set_value()

        return board

    def mutate(self):
        if random.randint(1, 100) < MUTATION_FREQUENCY:
            column = random.randint(1, BOARD_SIZE)
            new_value = random.randint(1, BOARD_SIZE)
            self.list[column - 1] = new_value
            self.set_value()

    def set_value(self):
        n = BOARD_SIZE
        self.value = n * (n - 1) // 2

        for i in range(n):
            for j in range(i + 1, n):
                difference = self.list[i] - self.list[j]
                if difference == 0:
                    self.value = self.value - 1
                elif abs(difference) == j - i:
                    self.value = self.value - 1


class Population:
    def __init__(self):
        self.boards = [Board() for i in range(POPULATION_SIZE)]
        self.sort_boards()

    def sort_boards(self):
        self.boards.sort(reverse=True, key=lambda x: x.value)

    def print_best_boards(self):
        for board in self.boards[:5]:
            print(board.list, board.value)

    def cull(self):
        self.boards = self.boards[:POPULATION_SIZE // 2]

    def add(self, children):
        self.boards = self.boards + children
        self.sort_boards()


def find_good_board():
    pop = Population()
    pop.print_best_boards()

    for gens in range(GENERATIONS):
        pop.cull()
        children = []

        for kids in range(POPULATION_SIZE // 2):
            board1 = random.choice(pop.boards)
            board2 = random.choice(pop.boards)
            new_child = board1.make_child(board2)
            new_child.mutate()
            children.append(new_child)

        pop.add(children)

    print("Generation:", gens)
    pop.print_best_boards()


find_good_board()
