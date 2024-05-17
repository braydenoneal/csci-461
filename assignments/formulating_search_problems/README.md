# Formulating Search Problems

1. Create a Python solution to the Bridge and Torch problem. Your solution should print out the path if one exists, the
   total time taken, and the number of nodes visited. You may use any search technique you wish.
2. Give a complete formulation (state, initial state, actions, etc.) to the following problem. Choose a formulation that
   is precise enough to be implemented.
   
   Problem: You have three jugs, measuring 12 gallons, 8 gallons, and 3 gallons, and a water faucet. You can fill the jugs
   from the faucet, or from one another, or pour their contents on the ground. The goal is to measure out (in a jug)
   exactly one gallon.

## Bridge and Torch Problem

### Output

```text
Total nodes visited: 444

Time  |  Start      |  End
------+-------------+------------
0     |  T A B C D  |           
2     |        C D  |  T A B    
3     |  T A   C D  |      B    
11    |    A        |  T   B C D
13    |  T A B      |        C D
15    |             |  T A B C D

Actions taken: 5

Time  |  Start      |  End
------+-------------+------------
0     |  T A B C D  |           
2     |        C D  |  T A B    
4     |  T   B C D  |    A      
12    |      B      |  T A   C D
13    |  T A B      |        C D
15    |             |  T A B C D

Actions taken: 5
```

### Code

```python
times = [1, 2, 5, 8]
complete_nodes = []
time_goal = 15
nodes_visited = []


class Node:
    def __init__(self, torch: bool, persons: list[bool], time_elapsed: int, parent):
        self.torch = torch
        self.persons = persons
        self.time_elapsed = time_elapsed
        self.parent = parent
        nodes_visited.append(1)

    def get_available_actions(self):
        actions = []
        checked_indices = []

        for index, person in enumerate(self.persons):
            checked_indices.append(index)

            if person == self.torch:
                actions.append([index])

                for second_index, second_person in enumerate(self.persons):
                    if second_index not in checked_indices and second_person == self.torch:
                        actions.append([index, second_index])

        return actions

    def perform_action(self, action):
        self.torch = not self.torch

        for index in action:
            self.persons[index] = not self.persons[index]

        self.time_elapsed += max([times[index] for index in action])

    def is_complete(self):
        return False not in self.persons

    def propagate(self):
        actions = self.get_available_actions()

        for action in actions:
            new_node = Node(self.torch, self.persons.copy(), self.time_elapsed, self)
            new_node.perform_action(action)

            if new_node.is_complete() and new_node.time_elapsed <= time_goal:
                complete_nodes.append(new_node)
            elif not is_repeat(new_node, new_node.parent) and new_node.time_elapsed < time_goal:
                new_node.propagate()


def is_repeat(initial_node: Node, parent: Node) -> bool:
    if parent is None:
        return False

    if initial_node.torch == parent.torch and initial_node.persons == parent.persons:
        return True

    return is_repeat(initial_node, parent.parent)


first_node = Node(False, [False, False, False, False], 0, None)
first_node.propagate()

print(f'Total nodes visited: {len(nodes_visited)}\n')

for complete_node in complete_nodes:
    path = [complete_node]

    while complete_node.parent is not None:
        complete_node = complete_node.parent
        path.insert(0, complete_node)

    print('Time  |  Start      |  End\n'
          '------+-------------+------------')

    for node in path:
        print(
            f'{node.time_elapsed:>4}  |  '
            f'{" " if node.torch else "T"} '
            f'{" " if node.persons[0] else "A"} '
            f'{" " if node.persons[1] else "B"} '
            f'{" " if node.persons[2] else "C"} '
            f'{" " if node.persons[3] else "D"}  |  '
            f'{"T" if node.torch else " "} '
            f'{"A" if node.persons[0] else " "} '
            f'{"B" if node.persons[1] else " "} '
            f'{"C" if node.persons[2] else " "} '
            f'{"D" if node.persons[3] else " "}'
        )

    print(f'\nActions taken: {len(path) - 1}\n')
```

## Three Jugs Problem

```text
Node:
    jug_1 = 0
    jug_2 = 0
    jug_3 = 0
    parent = None

Action:
    jug_index = <0: jug_1 | 1: jug_2 | 2: jug_3>
    action_command = <0: fill from faucet | 1: empty onto ground | 2: fill second jug>
    second_jug_index (optional) = <0: jug_1 | 1: jug_2 | 2: jug_3>
```

### Implementation Output (best 3 solutions)

```text
Total nodes visited: 286

A  | B  | C
---+----+----
0    0    0   
12   0    0   
4    8    0   
12   8    0   
0    8    0   
8    0    0   
5    0    3   
12   0    3   
0    0    3   
0    8    3   
8    0    3   
8    8    3   
12   4    3   
0    4    3   
4    0    3   
4    0    0   
1    0    3

Actions taken: 16

A  | B  | C
---+----+----
0    0    0   
12   0    0   
4    8    0   
4    0    0   
1    0    3

Actions taken: 4

A  | B  | C
---+----+----
0    0    0   
12   0    0   
4    8    0   
1    8    3

Actions taken: 3
```

### Implementation Code

```python
capacities = [12, 8, 3]
complete_nodes = []
capacity_goal = 1
nodes_visited = []


class Node:
    def __init__(self, jugs: list[int], parent, depth):
        self.jugs = jugs
        self.parent = parent
        self.depth = depth

    def get_available_actions(self):
        actions = []
        # [<jug index> <0: fill from faucet | 1: empty onto ground | 2: fill another jug> <jug index>?]

        for index, jug in enumerate(self.jugs):
            if jug < capacities[index]:
                # fill from faucet
                actions.append([index, 0])
            if jug > 0:
                # empty onto ground
                actions.append([index, 1])

                for second_index, second_jug in enumerate(self.jugs):
                    if index != second_index and second_jug < capacities[second_index]:
                        # fill second_jug
                        actions.append([index, 2, second_index])

        return actions


def perform_actions(self, action):
    jug_index = action[0]
    action_command = action[1]

    if action_command == 0:
        self.jugs[jug_index] = capacities[jug_index]
    elif action_command == 1:
        self.jugs[jug_index] = 0
    elif action_command == 2:
        second_jug_index = action[2]
        transfer_amount = min(self.jugs[jug_index], capacities[second_jug_index] - self.jugs[second_jug_index])

        self.jugs[jug_index] -= transfer_amount
        self.jugs[second_jug_index] += transfer_amount


def propagate(self):
    actions = self.get_available_actions()

    for action in actions:
        new_node = Node(self.jugs.copy(), self, self.depth + 1)
        new_node.perform_actions(action)

    if capacity_goal in new_node.jugs:
        complete_nodes.append(new_node)
    elif not is_repeat(new_node):
        nodes_visited.append(self)
        new_node.propagate()


def is_repeat(initial_node: Node) -> bool:
    for visited_node in nodes_visited:
        if initial_node.jugs == visited_node.jugs:
            return True

    return False


first_node = Node([0, 0, 0], None, 0)
first_node.propagate()

print(f'Total nodes visited: {len(nodes_visited)}\n')

complete_nodes = sorted(complete_nodes, key=lambda node: node.depth, reverse=True)

for complete_node in complete_nodes[-3:]:
    path = [complete_node]

    while complete_node.parent is not None:
        complete_node = complete_node.parent
        path.insert(0, complete_node)

    print('A  | B  | C\n'
          '---+----+----')

    for node in path:
        print(f'{node.jugs[0]:<4} {node.jugs[1]:<4} {node.jugs[2]:<4}')

    print(f'\nActions taken: {len(path) - 1}\n')
```
