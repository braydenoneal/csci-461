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
        # [<jug index> <0: fill | 1: empty onto ground | 2: fill another jug> <jug index>]

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
            jug_amount = self.jugs[jug_index]
            second_jug_index = action[2]
            second_jug_amount = self.jugs[second_jug_index]
            second_jug_capacity = capacities[second_jug_index]

            amount_until_second_jug_full = second_jug_capacity - second_jug_amount

            transfer_amount = min(jug_amount, amount_until_second_jug_full)

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

for complete_node in complete_nodes:
    path = [complete_node]

    while complete_node.parent is not None:
        complete_node = complete_node.parent
        path.insert(0, complete_node)

    print('A  | B  | C\n'
          '---+----+----')

    for node in path:
        print(f'{node.jugs[0]:<4} {node.jugs[1]:<4} {node.jugs[2]:<4}')

    print(f'\nActions taken: {len(path) - 1}\n')
