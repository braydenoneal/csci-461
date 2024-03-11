from __future__ import annotations
import math
import random
from dataclasses import dataclass
from PIL import Image
import numpy as np

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
class StorageNode:
    start: bool
    end: bool
    explored: bool
    open: bool
    adjacent_bools: list[bool]


def sort_paths(paths: list[Path]) -> list[Path]:
    return sorted(paths, key=lambda x: x.cost + x.distance_to_end_node)


iterations = 1

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

        for adjacent_node in adjacent_nodes:
            # make connections
            # draw_line(node, adjacent_node)
            pass

    maxi = size * size - 1
    start_index = random.randint(0, maxi)
    end_index = (start_index + random.randint(maxi // 2 - round(maxi * 0.25), maxi // 2 + round(maxi * 0.25))) % maxi
    start_node = nodes[start_index]
    end_node = nodes[end_index]

    current_graph: list[StorageNode] = []

    for node in nodes:
        current_graph.append(StorageNode(False, False, False, False, node.adjacent_bools))

    current_graph[start_index].start = True
    current_graph[end_index].end = True

    queue = [Path(start_node, 0, math.dist(start_node.position, end_node.position), None)]

    complete = []

    current_path = queue[-1]

    graphs: list[list[StorageNode]] = []

    while current_path.node is not end_node:
        queue.pop(0)
        current_graph[nodes.index(current_path.node)].explored = True
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
                current_graph[nodes.index(adjacent_node)].open = True
                queue.append(Path(adjacent_node, cost, distance_to_end_node, current_path))

        queue = sort_paths(queue)

        if not queue:
            current_path.parent = None
            break

        best_path = queue[0]

        current_path = queue[0]

        graphs.append(current_graph)

    complete_path = []

    while current_path.parent is not None:
        complete_path.insert(0, current_path)
        current_path = current_path.parent

    for path in complete_path:
        # draw the best path
        # draw_line(path.parent.node, path.node, color_rgb(255, 96, 96), 5)
        pass

    datas = []

    for graph in graphs:
        ints = []

        for node in graph:
            order = ['1', '0']
            binary = '0b'
            binary += order[node.start]
            binary += order[node.end]
            binary += order[node.explored]
            binary += order[node.open]

            for direction in node.adjacent_bools:
                binary += order[direction]

            ints.append(int(binary, 2))

        for remainder in range(len(ints) % 4):
            ints.append(0)

        pixels_quantity = len(ints) // 4

        pixels = []

        for i in range(pixels_quantity):
            pixels.append(tuple(ints[i * 4:(i + 1) * 4]))

        size = math.ceil(math.sqrt(len(pixels)))

        for remainder in range(size ** 2 - len(pixels)):
            pixels.append((0, 0, 0, 0))

        data = np.array([pixels]).astype(np.uint8)
        data = data.reshape((size, size, 4))

        datas.append(data)

        # export_image = Image.fromarray(data)

#         export_image.save('export1.png')

    datas_size = math.ceil(math.sqrt(len(datas)))

    image_data = np.zeros((datas_size * size, datas_size * size, 4)).astype(np.uint8)

    # for remainder in range(datas_size ** 2 - len(datas)):
    #     datas.append(np.zeros((size, size, 4)))

    for x in range(datas_size):
        for y in range(datas_size):
            image_data[x * size:(x + 1) * size, y * size:(y + 1) * size] = datas[x * size + y]

    export_image = Image.fromarray(image_data)

    export_image.save('export3.png')
