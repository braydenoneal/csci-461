import math
import random
from dataclasses import dataclass

from graphics import *


@dataclass
class Node:
    position: tuple[float, float]
    adjacent_node_indices: list[int]


nodes = []

size = 20
density = 50
scale = 0.4

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

window = GraphWin('A*', window_width, window_height, autoflush=True)
window.setBackground(color_rgb(16, 16, 16))

window_scaling = 110
window_padding = 64

lines = {}


def point_at_node_position(position: tuple[float, float]) -> Point:
    x_position = position[0] * window_scaling + window_padding
    y_position = position[1] * window_scaling + window_padding

    return Point(x_position, y_position)


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


for node in nodes:
    adjacent_nodes = [nodes[adjacent_node_index] for adjacent_node_index in node.adjacent_node_indices]

    for adjacent_node in adjacent_nodes:
        draw_line(node, adjacent_node)


@dataclass
class Path:
    node: Node
    cost: float
    distance_to_end_node: float
    parent: object


def sort_paths(paths: list[Path]) -> list[Path]:
    return sorted(paths, key=lambda x: x.cost + x.distance_to_end_node)


start_node = nodes[0]
end_node = nodes[-1]

start_path = Path(start_node, 0, math.dist(start_node.position, end_node.position), None)

queue = [start_path]

speed = 0.005

current_path = queue[-1]

while current_path.node is not end_node:
    queue.pop(0)

    adjacent_nodes = [nodes[adjacent_node_index] for adjacent_node_index in current_path.node.adjacent_node_indices]

    for adjacent_node in adjacent_nodes:
        # time.sleep(speed)

        cost = math.dist(current_path.node.position, adjacent_node.position) + current_path.cost
        distance_to_end_node = math.dist(adjacent_node.position, end_node.position)

        add = True

        for path in queue:
            if path.node is adjacent_node:
                if cost >= path.cost:
                    add = False
                else:
                    queue.remove(path)

        if add:
            queue.append(Path(adjacent_node, cost, distance_to_end_node, current_path))

    queue = sort_paths(queue)

    best_path = queue[0]

    draw_line(best_path.parent.node, best_path.node, color_rgb(128, 64, 64), 3)

    current_path = queue[0]

while current_path.parent is not None:
    draw_line(current_path.parent.node, current_path.node, color_rgb(255, 64, 64), 5)
    current_path = current_path.parent

window.getMouse()
window.close()
