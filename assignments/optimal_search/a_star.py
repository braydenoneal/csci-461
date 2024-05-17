import math
from dataclasses import dataclass


@dataclass
class Node:
    index: int
    position: tuple[float, float]
    adjacent_node_indices: list[int]


nodes = [Node(*node) for node in [
    [0, [5.04, 2.39], [8, 9]],
    [1, [0.00, 0.61], [2]],
    [2, [1.62, 0.59], [1, 3, 6, 12]],
    [3, [3.77, 0.01], [2, 4, 6]],
    [4, [6.48, 0.00], [3, 5, 7]],
    [5, [8.51, 0.03], [4, 11]],
    [6, [3.80, 0.62], [2, 3, 7, 8]],
    [7, [6.48, 0.72], [4, 6, 10]],
    [8, [3.79, 2.42], [0, 6, 13]],
    [9, [5.69, 2.46], [0, 10, 14]],
    [10, [6.51, 2.45], [7, 9, 11, 15, 16]],
    [11, [8.45, 1.76], [5, 10, 16]],
    [12, [1.75, 4.61], [2, 13]],
    [13, [3.49, 4.61], [8, 12, 14, 17]],
    [14, [5.65, 4.62], [9, 13, 15, 18]],
    [15, [6.41, 4.61], [10, 14, 16, 19]],
    [16, [8.51, 4.70], [10, 11, 15, 20]],
    [17, [3.58, 6.11], [13, 18]],
    [18, [5.66, 6.15], [14, 17, 19]],
    [19, [6.44, 6.11], [15, 18, 20]],
    [20, [8.54, 6.27], [16, 19]],
]]


@dataclass
class Path:
    node: Node
    distance_to_adjacent_node: float
    distance_to_end_node: float


def get_best_path(paths, current_total_cost) -> Path:
    return sorted(paths, key=lambda x: x.distance_to_adjacent_node + x.distance_to_end_node + current_total_cost)[0]


start_node = nodes[0]
end_node = nodes[1]

path: list[Node] = []

current_node = start_node
current_total_cost = 0

while current_node is not end_node:
    path.append(current_node)

    adjacent_nodes = [nodes[adjacent_node_index] for adjacent_node_index in current_node.adjacent_node_indices]
    paths = []

    for adjacent_node in adjacent_nodes:
        distance_to_adjacent_node = math.dist(current_node.position, adjacent_node.position)
        distance_to_end_node = math.dist(adjacent_node.position, end_node.position)

        paths.append(Path(adjacent_node, distance_to_adjacent_node, distance_to_end_node))

    best_path = get_best_path(paths, current_total_cost)
    current_total_cost += best_path.distance_to_adjacent_node
    current_node = best_path.node

    print(current_node.index)

print(current_total_cost)
