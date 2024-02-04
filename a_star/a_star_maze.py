from __future__ import annotations
import math
import random
from dataclasses import dataclass

from graphics import *

window_width = 1000
window_height = 1000

window = GraphWin('A*', window_width, window_height)
window.setBackground(color_rgb(16, 16, 16))

window_scaling = 110
window_padding = 64

lines = {}
end_nodes = []


@dataclass
class Node:
    position: tuple[float, float]
    adjacent_node_indices: list[int]


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


def draw_node(node: Node, color=color_rgb(255, 128, 128), size=5):
    p = Circle(point_at_node_position(node.position), size)
    p.setFill(color)
    p.setOutline(color)
    p.draw(window)
    return p


@dataclass
class Path:
    node: Node
    cost: float
    distance_to_end_node: float
    parent: Path or None


def sort_paths(paths: list[Path]) -> list[Path]:
    return sorted(paths, key=lambda x: x.cost + x.distance_to_end_node)


while True:
    window.autoflush = False

    for line in lines:
        lines[line].undraw()
        del line

    for node in end_nodes:
        node.undraw()
        del node

    window.autoflush = True

    nodes = []

    size = 64
    density = 0.36
    scale = 0.125

    for y in range(size):
        for x in range(size):
            adjacent_node_indices = []

            if x - 1 >= 0 and random.random() < density:
                adjacent_node_indices.append(y * size + x - 1)

            if x + 1 < size and random.random() < density:
                adjacent_node_indices.append(y * size + x + 1)

            if y - 1 >= 0 and random.random() < density:
                adjacent_node_indices.append((y - 1) * size + x)

            if y + 1 < size and random.random() < density:
                adjacent_node_indices.append((y + 1) * size + x)

            nodes.append(Node((x * scale, y * scale), adjacent_node_indices))

    for node_index, node in enumerate(nodes):
        for adjacent_node_index in node.adjacent_node_indices:
            nodes[adjacent_node_index].adjacent_node_indices.append(node_index)

    lines.clear()

    window.autoflush = False

    for node in nodes:
        adjacent_nodes = [nodes[adjacent_node_index] for adjacent_node_index in node.adjacent_node_indices]

        for adjacent_node in adjacent_nodes:
            draw_line(node, adjacent_node)

    window.autoflush = True

    maxi = size * size - 1
    start_index = random.randint(0, maxi)
    end_index = (start_index + random.randint(maxi // 2 - round(maxi * 0.25), maxi // 2 + round(maxi * 0.25))) % maxi
    start_node = nodes[start_index]
    end_node = nodes[end_index]

    end_nodes.append(draw_node(start_node))
    end_nodes.append(draw_node(end_node))

    queue = [Path(start_node, 0, math.dist(start_node.position, end_node.position), None)]

    complete = []

    current_path = queue[-1]

    while current_path.node is not end_node:
        queue.pop(0)
        complete.append(current_path.node)

        adjacent_nodes = [nodes[adjacent_node_index] for adjacent_node_index in current_path.node.adjacent_node_indices]

        for adjacent_node in adjacent_nodes:
            cost = math.dist(current_path.node.position, adjacent_node.position) + current_path.cost
            # distance_to_end_node = (abs(adjacent_node.position[0] - end_node.position[0]) +
            #                         abs(adjacent_node.position[1] - end_node.position[1]))
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
                draw_line(current_path.node, adjacent_node, color_rgb(192, 96, 96), 4)
                queue.append(Path(adjacent_node, cost, distance_to_end_node, current_path))

        queue = sort_paths(queue)

        if not queue:
            current_path.parent = None
            break

        best_path = queue[0]

        # time.sleep(0.01)
        draw_line(best_path.parent.node, best_path.node, color_rgb(128, 64, 64), 3)

        current_path = queue[0]

    complete_path = []

    while current_path.parent is not None:
        complete_path.insert(0, current_path)
        current_path = current_path.parent

    for path in complete_path:
        draw_line(path.parent.node, path.node, color_rgb(255, 96, 96), 5)

    # window.getMouse()
