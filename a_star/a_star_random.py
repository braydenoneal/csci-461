import math
import random
from dataclasses import dataclass

from graphics import *


@dataclass
class Node:
    position: tuple[float, float]
    adjacent_node_indices: list[int]


nodes = []

size = 40
density = 40
scale = 0.2

for y in range(size):
    for x in range(size):
        adjacent_node_indices = []

        if x - 1 >= 0 and random.randint(0, 100) < density:
            adjacent_node_indices.append(y * size + x - 1)

        if x + 1 < size and random.randint(0, 100) < density:
            adjacent_node_indices.append(y * size + x + 1)

        if y - 1 >= 0 and random.randint(0, 100) < density:
            adjacent_node_indices.append((y - 1) * size + x)

        if y + 1 < size and random.randint(0, 100) < density:
            adjacent_node_indices.append((y + 1) * size + x)

        nodes.append(Node((x * scale, y * scale), adjacent_node_indices))

for node_index, node in enumerate(nodes):
    for adjacent_node_index in node.adjacent_node_indices:
        nodes[adjacent_node_index].adjacent_node_indices.append(node_index)

window_width = 1000
window_height = 1000

window = GraphWin('A*', window_width, window_height)
window.setBackground(color_rgb(16, 16, 16))

window_scaling = 110
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


def draw_line(node: Node, adjacent_node: Node, color=color_rgb(64, 64, 64), width=2):
    if f'{(node, adjacent_node)}' in lines:
        lines[f'{(node, adjacent_node)}'].setWidth(width)
        lines[f'{(node, adjacent_node)}'].setFill(color)
    elif f'{(adjacent_node, node)}' in lines:
        lines[f'{(adjacent_node, node)}'].setWidth(width)
        lines[f'{(adjacent_node, node)}'].setFill(color)
    else:
        line = Line(point_at_node_position(node.position), point_at_node_position(adjacent_node.position))
        line.setWidth(width)
        line.setFill(color)
        line.draw(window)

        lines[f'{(node, adjacent_node)}'] = line


window.autoflush = False

for node in nodes:
    adjacent_nodes = [nodes[adjacent_node_index] for adjacent_node_index in node.adjacent_node_indices]

    for adjacent_node in adjacent_nodes:
        draw_line(node, adjacent_node)

window.autoflush = True


@dataclass
class Path:
    node: Node
    distance_to_adjacent_node: float
    distance_to_end_node: float


def get_best_path(paths, current_total_cost) -> Path:
    return sorted(paths, key=lambda x: x.distance_to_adjacent_node + x.distance_to_end_node + current_total_cost)[0]


start_node = nodes[0]
end_node = nodes[-1]

path: list[Node] = []
visited = []

current_node = start_node
current_total_cost = 0

speed = 0.0005

while current_node is not end_node:
    if current_node not in path:
        path.append(current_node)

    adjacent_nodes = [nodes[adjacent_node_index] for adjacent_node_index in current_node.adjacent_node_indices]
    paths = []

    for adjacent_node in adjacent_nodes:
        if adjacent_node not in path and adjacent_node not in visited:
            draw_line(current_node, adjacent_node, color_rgb(128, 64, 64), 3)
            time.sleep(speed)
            draw_line(current_node, adjacent_node)

            distance_to_adjacent_node = math.dist(current_node.position, adjacent_node.position)
            distance_to_end_node = math.dist(adjacent_node.position, end_node.position)

            paths.append(Path(adjacent_node, distance_to_adjacent_node, distance_to_end_node))

    if paths:
        best_path = get_best_path(paths, current_total_cost)
        current_total_cost += best_path.distance_to_adjacent_node

        draw_line(current_node, best_path.node, color_rgb(255, 64, 64), 5)

        current_node = best_path.node
    else:
        last_node = path[-1]
        current_node = path[-2]
        visited.append(last_node)
        path.pop()
        time.sleep(speed)
        draw_line(current_node, last_node, color_rgb(96, 64, 64))

window.getMouse()
window.close()
