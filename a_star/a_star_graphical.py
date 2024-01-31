import math
from dataclasses import dataclass

from graphics import *


@dataclass
class Node:
    position: tuple[float, float]
    adjacent_node_indices: list[int]


nodes = [Node(*node) for node in [
    ((5.04, 2.39), [8, 9]),
    ((0.00, 0.61), [2]),
    ((1.62, 0.59), [1, 3, 6, 12]),
    ((3.77, 0.01), [2, 4, 6]),
    ((6.48, 0.00), [3, 5, 7]),
    ((8.51, 0.03), [4, 11]),
    ((3.80, 0.62), [2, 3, 7, 8]),
    ((6.48, 0.72), [4, 6, 10]),
    ((3.79, 2.42), [0, 6, 13]),
    ((5.69, 2.46), [0, 10, 14]),
    ((6.51, 2.45), [7, 9, 11, 15, 16]),
    ((8.45, 1.76), [5, 10, 16]),
    ((1.75, 4.61), [2, 13]),
    ((3.49, 4.61), [8, 12, 14, 17]),
    ((5.65, 4.62), [9, 13, 15, 18]),
    ((6.41, 4.61), [10, 14, 16, 19]),
    ((8.51, 4.70), [10, 11, 15, 20]),
    ((3.58, 6.11), [13, 18]),
    ((5.66, 6.15), [14, 17, 19]),
    ((6.44, 6.11), [15, 18, 20]),
    ((8.54, 6.27), [16, 19]),
]]

window_width = 720
window_height = 640

window = GraphWin('A*', window_width, window_height)

window_scaling = 71
window_padding = 64

lines = {}


def point_at_node_position(position: tuple[float, float]) -> Point:
    x_position = position[0] * window_scaling + window_padding
    y_position = position[1] * window_scaling + window_padding

    return Point(x_position, y_position)


def draw_circle(node: Node):
    center_point = point_at_node_position(node.position)

    circle = Circle(center_point, 16)
    circle.setFill('white')
    circle.setWidth(2)
    circle.draw(window)

    text = Text(center_point, nodes.index(node) + 1)
    text.draw(window)


def draw_line(node: Node, adjacent_node: Node, color='black'):
    if f'{(node, adjacent_node)}' in lines:
        lines[f'{(node, adjacent_node)}'].setFill(color)
    elif f'{(adjacent_node, node)}' in lines:
        lines[f'{(adjacent_node, node)}'].setFill(color)
    else:
        line = Line(point_at_node_position(node.position), point_at_node_position(adjacent_node.position))
        line.setWidth(2)
        line.setFill(color)
        line.draw(window)

        lines[f'{(node, adjacent_node)}'] = line

        draw_circle(node)
        draw_circle(adjacent_node)


for node in nodes:
    adjacent_nodes = [nodes[adjacent_node_index] for adjacent_node_index in node.adjacent_node_indices]

    for adjacent_node in adjacent_nodes:
        draw_line(node, adjacent_node)


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

window.getMouse()

while current_node is not end_node:
    path.append(current_node)

    adjacent_nodes = [nodes[adjacent_node_index] for adjacent_node_index in current_node.adjacent_node_indices]
    paths = []

    for adjacent_node in adjacent_nodes:
        if adjacent_node not in path:
            draw_line(current_node, adjacent_node, 'green')
            time.sleep(0.25)
            draw_line(current_node, adjacent_node)

            distance_to_adjacent_node = math.dist(current_node.position, adjacent_node.position)
            distance_to_end_node = math.dist(adjacent_node.position, end_node.position)

            paths.append(Path(adjacent_node, distance_to_adjacent_node, distance_to_end_node))

    best_path = get_best_path(paths, current_total_cost)
    current_total_cost += best_path.distance_to_adjacent_node

    draw_line(current_node, best_path.node, 'red')

    current_node = best_path.node

window.getMouse()
window.close()

print(current_total_cost)
