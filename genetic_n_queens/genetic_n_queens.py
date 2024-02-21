"""
Genetic algorithm for n queens
For A.I. class
Dr. Browning,
March 3, 2020
"""

import random

# Identify constants.
# Can get excellent results using the constants 8, 50, 100, 70.
# How can we make better choice so we can minimize population size
# and number of generations and still get excellent results?
BOARD_SIZE = 8  # Use 8x8 boards
POPULATION_SIZE = 50  # How many boards are in the population?
GENERATIONS = 200  # Times we will cull, make children,and mutate
MUTATION_FREQUENCY = 20  # Percentage of the time to mutate


# The model of a game board is a list of numbers 1-8.  The first number
# indicates the row of the queen in column 1, second for column 2, etc.
# A random starting configuration is provided.
class Board:
    # A board consists of a list of row numbers for the queens and maintains
    # the value of the heuristic function.
    def __init__(self):  # Create a new game board
        self.list = [random.randint(1, BOARD_SIZE) for i in range(BOARD_SIZE)]
        self.value = 0
        self.set_value()

    # Each board has a makeChild method that takes a second existing board.
    # It generates a split point and then creates a new board that consists of
    # the first part of the current board, up to and including the split point,
    # and the second part of the second board, from the split point on.
    def make_child(self, board2):
        # Change the split point range for different results.
        split_point = random.randint(1, BOARD_SIZE - 1)
        board = Board()
        board.list = self.list[:split_point] + board2.list[split_point:]
        board.set_value()
        return board

    # Determine if this board should mutate. If so, change a random column
    # to a random new value.
    # Change the mutation frequency for different results.
    def mutate(self):
        if random.randint(1, 100) < MUTATION_FREQUENCY:
            column = random.randint(1, BOARD_SIZE)
            new_value = random.randint(1, BOARD_SIZE)
            self.list[column - 1] = new_value
            self.set_value()

    # The setValue method computes the heuristic = the number of pairs
    # of queens that can"t capture each other on this board.
    # TODO: Is this code correct?
    def set_value(self):
        n = BOARD_SIZE
        # Best possible value for 8 queens board is 28. Why?
        self.value = n * (n - 1) // 2
        # Check each possible pair of queens.
        for i in range(n):
            for j in range(i + 1, n):
                difference = self.list[i] - self.list[j]
                if difference == 0:
                    # These two queens are on the same row.
                    self.value = self.value - 1
                elif abs(difference) == j - i:
                    # These two queens are on the same diagonal.
                    self.value = self.value - 1

                # The population consists of a number of boards, sorted in decreasing order


# of heuristic value.
class Population:
    # Create a random population.
    def __init__(self):
        self.boards = [Board() for i in range(POPULATION_SIZE)]
        self.sort_boards()

    # Sort the population in decreasing order by value of the heuristic
    # function.
    def sort_boards(self):
        self.boards.sort(reverse=True, key=lambda x: x.value)

    # If you have a large population, use boards[:5] to see the top 5.
    def print_best_boards(self):
        for board in self.boards[:5]:
            print(board.list, board.value)

    # TODO: Change this to a smarter culling procedure.
    # Reduce the population size before adding in a new generation of
    # children boards.  This method removes the lower scoring half of
    # the population.
    def cull(self):
        self.boards = self.boards[:POPULATION_SIZE // 2]

    # When we add a collection of children to the population, we then need
    # to resort the boards. Here children is a list of children.
    def add(self, children):
        self.boards = self.boards + children
        self.sort_boards()


# Here is the main program.  Create a population.  For several generations,
# cull, generate children, and consider mutations.  Print the initial
# population best boards and the final population best boards.
def find_good_board():
    pop = Population()
    pop.print_best_boards()

    for gens in range(GENERATIONS):
        pop.cull()
        children = []

        for kids in range(POPULATION_SIZE // 2):
            # TODO: Change the choice of parents to a smarter approach.
            board1 = random.choice(pop.boards)
            board2 = random.choice(pop.boards)
            new_child = board1.make_child(board2)
            new_child.mutate()
            children.append(new_child)

        pop.add(children)

    print("Generation:", gens)
    pop.print_best_boards()


find_good_board()
