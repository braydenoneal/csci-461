from __future__ import annotations
import math


class Adjacent:
    def __init__(self, adjacent_index, cost):
        self.adjacent_index = adjacent_index
        self.cost = cost


class Node:
    def __init__(self, name: str, adjacent: list[Adjacent], cost: float = math.inf, closed: bool = False,
                 parent: Node or None = None):
        self.name = name
        self.adjacent = adjacent
        self.cost = cost
        self.closed = closed
        self.parent = parent

    def __str__(self):
        return (
            f'{self.name} {"I" if self.cost is math.inf else self.cost} {"C" if self.closed else "O"} '
            f'{self.parent.name if self.parent else "X"}'
        )


nodes = [Node(node[0], [Adjacent(*adjacent) for adjacent in node[1]]) for node in [
    ('a', [(1, 6), (3, 2)]),
    ('b', [(0, 6), (3, 3), (2, 1)]),
    ('c', [(1, 1), (3, 2), (4, 2)]),
    ('d', [(0, 2), (1, 3), (2, 2), (4, 6)]),
    ('e', [(2, 2), (4, 6)]),
]]

current_node = nodes[0]
end_node = nodes[-1]

current_node.cost = 0

print('   '.join(str(node) for node in nodes))

while current_node is not end_node:
    for adjacent in current_node.adjacent:
        adjacent_node = nodes[adjacent.adjacent_index]

        cost = current_node.cost + adjacent.cost

        if cost < adjacent_node.cost:
            adjacent_node.cost = cost
            adjacent_node.parent = current_node
            adjacent_node.closed = False

    current_node.closed = True

    current_node = sorted([x for x in nodes if not x.closed], key=lambda x: x.cost)[0]
    print('   '.join(str(node) for node in nodes))

print(f'\nCost: {current_node.cost}')
print(current_node.name, end='')

while current_node.parent is not None:
    current_node = current_node.parent
    print(' <- ', end='')
    print(current_node.name, end='')

print()
