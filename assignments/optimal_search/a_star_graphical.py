from __future__ import annotations
import math
from dataclasses import dataclass

from graphics import *


@dataclass
class Node:
    position: tuple[float, float]
    adjacent_node_indices: list[int]
    opened: bool
    cost: float
    heuristic: float
    parent: Node or None


nodes = [Node(node[0], node[1], True, math.inf, 0, None) for node in [
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
    return Point(position[0] * window_scaling + window_padding, position[1] * window_scaling + window_padding)


def draw_circle(node: Node):
    center_point = point_at_node_position(node.position)

    circle = Circle(center_point, 16)
    circle.setFill('white')
    circle.setWidth(3)
    circle.draw(window)

    text = Text(center_point, nodes.index(node) + 1)
    text.draw(window)


def draw_line(node: Node, adjacent_node: Node, color='black', width=2):
    first_str = f'{nodes.index(node)} {nodes.index(adjacent_node)}'
    second_str = f'{nodes.index(adjacent_node)} {nodes.index(node)}'

    if first_str in lines:
        lines[first_str].setWidth(width)
        lines[first_str].setFill(color)
    elif second_str in lines:
        lines[second_str].setWidth(width)
        lines[second_str].setFill(color)
    else:
        line = Line(point_at_node_position(node.position), point_at_node_position(adjacent_node.position))
        line.setWidth(width)
        line.setFill(color)
        line.draw(window)

        lines[first_str] = line

        draw_circle(node)
        draw_circle(adjacent_node)


for node in nodes:
    adjacent_nodes = [nodes[adjacent_node_index] for adjacent_node_index in node.adjacent_node_indices]

    for adjacent_node in adjacent_nodes:
        draw_line(node, adjacent_node)

current_node = nodes[0]
end_node = nodes[1]

current_node.cost = 0

for node in nodes:
    node.heuristic = math.dist(node.position, end_node.position)


while current_node is not end_node:
    adjacent_nodes = [nodes[adjacent_node_index] for adjacent_node_index in current_node.adjacent_node_indices]

    for adjacent_node in adjacent_nodes:
        time.sleep(0.25)

        cost = current_node.cost + math.dist(current_node.position, adjacent_node.position)

        if cost < adjacent_node.cost:
            draw_line(current_node, adjacent_node, 'green', 3)
            adjacent_node.cost = cost
            adjacent_node.parent = current_node
            adjacent_node.opened = True

    current_node.opened = False

    current_node = sorted([x for x in nodes if x.opened], key=lambda x: x.cost + x.heuristic)[0]

    if current_node.parent is not None:
        draw_line(current_node.parent, current_node, 'blue', 4)

print(round(current_node.cost, 2))

while current_node.parent is not None:
    time.sleep(0.25)
    draw_line(current_node.parent, current_node, 'red', 5)
    current_node = current_node.parent

window.getMouse()
window.close()
