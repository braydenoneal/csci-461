from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Node:
    label: str
    value: float
    code: str
    left_child: Node or None
    right_child: Node or None


queue: list[Node] = [Node(parameters[0], parameters[1], '', None, None) for parameters in [
    ('A', 8.20), ('B', 1.50), ('C', 2.80), ('D', 4.30), ('E', 12.7), ('F', 2.20), ('G', 2.00), ('H', 6.10), ('I', 7.00),
    ('J', 0.15), ('K', 0.77), ('L', 4.00), ('M', 2.40), ('N', 6.70), ('O', 7.50), ('P', 1.90), ('Q', .095), ('R', 6.00),
    ('S', 6.30), ('T', 9.10), ('U', 2.80), ('V', 0.98), ('W', 2.40), ('X', 0.15), ('Y', 2.00), ('Z', .074)
]]

while len(queue) > 1:
    queue = sorted(queue, key=lambda x: x.value, reverse=True)

    right = queue.pop()
    left = queue.pop()

    queue.append(Node('', round(left.value + right.value, 3), '', left, right))

tree_string = ''
code_string = ''

while len(queue):
    next_queue = []

    for node in queue:
        left = node.left_child
        right = node.right_child

        output_string = ''

        if left:
            left.code = node.code + '0'

            if left.label:
                output_string += f'({left.label}) '
                code_string += f'{left.label}: {left.code}\n'

            output_string += f'{left.value}, '
            next_queue.append(left)

        if right:
            right.code = node.code + '1'

            if right.label:
                output_string += f'({right.label}) '
                code_string += f'{right.label}: {right.code}\n'

            output_string += f'{right.value}'
            next_queue.append(right)

        if left and right:
            tree_string += f'{node.value:<7} [ {output_string} ]\n'

    queue = next_queue

print(tree_string)
print(code_string)
