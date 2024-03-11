from __future__ import annotations
import math
import random
from dataclasses import dataclass

lines = {}
end_nodes = []


@dataclass
class Node:
    position: tuple[float, float]
    adjacent_node_indices: list[int]
    adjacent_bools: list[bool]


@dataclass
class Path:
    node: Node
    cost: float
    distance_to_end_node: float
    parent: Path or None


@dataclass
class InputNode:
    current_node_position: tuple[float, float]
    end_node_position: tuple[float, float]
    directions: list[bool]


@dataclass
class OutputNode:
    direction: float


def sort_paths(paths: list[Path]) -> list[Path]:
    return sorted(paths, key=lambda x: x.cost + x.distance_to_end_node)


input_nodes: list[InputNode] = []
output_nodes: list[OutputNode] = []

iterations = 10

for iteration in range(iterations):
    iterations += 1
    nodes = []

    size = 64
    density = 0.36
    scale = 0.125

    for y in range(size):
        for x in range(size):
            adjacent_node_indices = []
            adjacent_bools = [False, False, False, False]

            if x - 1 >= 0 and random.random() < density:
                adjacent_node_indices.append(y * size + x - 1)
                adjacent_bools[0] = True

            if x + 1 < size and random.random() < density:
                adjacent_node_indices.append(y * size + x + 1)
                adjacent_bools[1] = True

            if y - 1 >= 0 and random.random() < density:
                adjacent_node_indices.append((y - 1) * size + x)
                adjacent_bools[2] = True

            if y + 1 < size and random.random() < density:
                adjacent_node_indices.append((y + 1) * size + x)
                adjacent_bools[3] = True

            nodes.append(Node((x * scale, y * scale), adjacent_node_indices, adjacent_bools))

    for node_index, node in enumerate(nodes):
        for adjacent_node_index in node.adjacent_node_indices:
            nodes[adjacent_node_index].adjacent_node_indices.append(node_index)

    for node in nodes:
        adjacent_nodes = [nodes[adjacent_node_index] for adjacent_node_index in node.adjacent_node_indices]

    maxi = size * size - 1
    start_index = random.randint(0, maxi)
    end_index = (start_index + random.randint(maxi // 2 - round(maxi * 0.25), maxi // 2 + round(maxi * 0.25))) % maxi
    start_node = nodes[start_index]
    end_node = nodes[end_index]

    queue = [Path(start_node, 0, math.dist(start_node.position, end_node.position), None)]

    complete = []

    current_path = queue[-1]

    while current_path.node is not end_node:
        queue.pop(0)
        complete.append(current_path.node)

        adjacent_nodes = [nodes[adjacent_node_index] for adjacent_node_index in current_path.node.adjacent_node_indices]

        for adjacent_node in adjacent_nodes:
            cost = math.dist(current_path.node.position, adjacent_node.position) + current_path.cost
            distance_to_end_node = math.dist(adjacent_node.position, end_node.position)

            add = True

            if adjacent_node in complete:
                add = False

            for path in queue:
                if path.node is adjacent_node:
                    if cost >= path.cost:
                        add = False
                    else:
                        queue.remove(path)

            if add:
                queue.append(Path(adjacent_node, cost, distance_to_end_node, current_path))

        queue = sort_paths(queue)

        if not queue:
            current_path.parent = None
            break

        best_path = queue[0]

        current_path = queue[0]

    complete_path = []

    while current_path.parent is not None:
        complete_path.insert(0, current_path)
        current_path = current_path.parent

    for path in complete_path:
        current_position = path.parent.node.position
        next_position = path.node.position
        input_nodes.append(InputNode(current_position, end_node.position, path.parent.node.adjacent_bools))

        output_float = 0.0

        if next_position[0] > current_position[0]:
            output_float = 1.0
        if next_position[1] < current_position[1]:
            output_float = 2.0
        if next_position[1] > current_position[1]:
            output_float = 3.0

        output_nodes.append(OutputNode(output_float))

input_data = []

for input_node in input_nodes:
    input_data.append([
        input_node.current_node_position[0],
        input_node.current_node_position[1],
        input_node.end_node_position[0],
        input_node.end_node_position[1],
        float(input_node.directions[0]),
        float(input_node.directions[1]),
        float(input_node.directions[2]),
        float(input_node.directions[3]),
    ])

output_data = []

for output_node in output_nodes:
    output_data.append(output_node.direction)

print(input_data)
print(output_data)
