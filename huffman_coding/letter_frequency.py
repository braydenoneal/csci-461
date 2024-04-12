from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Node:
    label: str
    value: float
    left_child: Node or None
    right_child: Node or None


queue: list[Node] = [
    Node('A', 8.20, None, None),
    Node('B', 1.50, None, None),
    Node('C', 2.80, None, None),
    Node('D', 4.30, None, None),
    Node('E', 12.7, None, None),
    Node('F', 2.20, None, None),
    Node('G', 2.00, None, None),
    Node('H', 6.10, None, None),
    Node('I', 7.00, None, None),
    Node('J', 0.15, None, None),
    Node('K', 0.77, None, None),
    Node('L', 4.00, None, None),
    Node('M', 2.40, None, None),
    Node('N', 6.70, None, None),
    Node('O', 7.50, None, None),
    Node('P', 1.90, None, None),
    Node('Q', 0.10, None, None),
    Node('R', 6.00, None, None),
    Node('S', 6.30, None, None),
    Node('T', 9.10, None, None),
    Node('U', 2.80, None, None),
    Node('V', 0.98, None, None),
    Node('W', 2.40, None, None),
    Node('X', 0.15, None, None),
    Node('Y', 2.00, None, None),
    Node('Z', 0.07, None, None),
]

while len(queue) > 1:
    queue = sorted(queue, key=lambda x: x.value)

    right = queue.pop()
    left = queue.pop()

    queue.append(Node('', left.value + right.value, left, right))


def print_children(node: Node):
    print(node)

    left = node.left_child
    right = node.right_child

    if left:
        print_children(left)

    if right:
        print_children(right)


print_children(queue[0])
