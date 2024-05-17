from __future__ import annotations
import math
import random
from dataclasses import dataclass
import torch
import numpy as np

from graphics import *

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

iterations = 64

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
        current_node: Node = path.parent.node
        current_position = path.parent.node.position
        next_position = path.node.position
        input_nodes.append(InputNode(current_position, end_node.position, path.parent.node.adjacent_bools))

        output_float = float(current_node.adjacent_node_indices.index(nodes.index(path.node)))

        # output_float = 0.0
        #
        # if next_position[0] > current_position[0]:
        #     output_float = 1.0
        # if next_position[1] < current_position[1]:
        #     output_float = 2.0
        # if next_position[1] > current_position[1]:
        #     output_float = 3.0

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
    output_data.append([output_node.direction])

print(input_data)
print(output_data)

input_data = torch.FloatTensor(np.array(input_data).astype(float))
output_data = torch.FloatTensor(np.array(output_data).astype(float))

# input_data.sub_(input_data.mean(0))
# input_data.div_(input_data.std(0))
#
# output_data.sub_(output_data.mean(0))
# output_data.div_(output_data.std(0))

# print(input_data.shape)
# print(output_data.shape)


class Model(torch.nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.layer1 = torch.nn.Linear(8, 6)
        self.layer2 = torch.nn.Linear(6, 1)

    def forward(self, values):
        values = self.layer1(values)
        values = torch.relu(values)
        return self.layer2(values)


model = Model()
# print(model)

# Create momentum weights
z_parameters = []
for param in model.parameters():
    z_parameters.append(param.data.clone())
for param in z_parameters:
    param.zero_()

criterion = torch.nn.MSELoss()

num_examples = len(input_data)
batch_size = 16
learning_rate = 0.0001
momentum = 0.899
epochs = 1000

# train the model
for epoch in range(epochs):
    random_indices = torch.randperm(input_data.size(0))

    x_feature_batches = torch.split(input_data[random_indices], batch_size)
    y_feature_batches = torch.split(output_data[random_indices], batch_size)

    current_total_loss = 0

    for x_features_batch, y_features_batch in zip(x_feature_batches, y_feature_batches):
        loss = criterion(model.forward(x_features_batch), y_features_batch)

        current_total_loss += loss.item()

        model.zero_grad()
        loss.backward()

        # Adjust the weights with momentum
        for i, (z_param, param) in enumerate(zip(z_parameters, model.parameters())):
            z_parameters[i] = momentum * z_param + param.grad.data
            param.data.sub_(z_parameters[i] * learning_rate)

    print_str = f'epoch: {epoch + 1}, loss: {current_total_loss * batch_size / input_data.size(0):11.8f}'

    # print(print_str)

print('total number of examples:', num_examples, end='; ')
print('batch size:', batch_size)
print('learning rate:', learning_rate)
print('momentum:', momentum)

# Compute 1-SSE/SST which is the proportion of the variance in the data
# explained by the regression hyperplane.
SS_E = 0.0
SS_T = 0.0
mean = output_data.mean()
# mean = 0

for xs, ys in zip(input_data, output_data):
    SS_E = SS_E + (ys - model(xs)) ** 2
    SS_T = SS_T + (ys - mean) ** 2

print(f'1-SSE/SST = {1.0 - (SS_E / SS_T).item():1.4f}')

# Test the model

print(model(torch.FloatTensor([
    0.0,
    0.0,
    10.0,
    10.0,
    0.0,
    0.0,
    1.0,
    0.0,
])))

# Run the model

window_width = 1000
window_height = 1000

window = GraphWin('Neural A*', window_width, window_height)
window.setBackground(color_rgb(16, 16, 16))

window_scaling = 110
window_padding = 64

lines = {}
end_nodes = []


@dataclass
class Node:
    position: tuple[float, float]
    adjacent_node_indices: list[int]
    adjacent_bools: list[bool]


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

    current_node = start_node

    visited = []

    while current_node is not end_node:
        visited.append(current_node)
        previous_node = current_node
        # queue.pop(0)
        # complete.append(current_path.node)

        adjacent_nodes = [nodes[adjacent_node_index] for adjacent_node_index in current_node.adjacent_node_indices]

        adjacent_index = min(3, math.floor(model(torch.FloatTensor([
            start_node.position[0],
            start_node.position[1],
            end_node.position[0],
            end_node.position[1],
            float(current_node.adjacent_bools[0]),
            float(current_node.adjacent_bools[1]),
            float(current_node.adjacent_bools[2]),
            float(current_node.adjacent_bools[3]),
        ]))))

        print(adjacent_index)

        if not adjacent_nodes:
            break

        current_node = adjacent_nodes[0]

        if len(adjacent_nodes) > adjacent_index:
            current_node = adjacent_nodes[adjacent_index]

        if current_node in visited:
            for adjacent_node in adjacent_nodes:
                if adjacent_node not in visited:
                    current_node = adjacent_node

        if current_node in visited:
            print('break')
            break

        # node_choices = [adjacent_nodes[0], adjacent_nodes[0], adjacent_nodes[0], adjacent_nodes[0]]
        #
        # for adjacent_node in adjacent_nodes:
        #     if adjacent_node.position[0] < current_node.position[0]:
        #         node_choices[0] = adjacent_node
        #     elif adjacent_node.position[0] > current_node.position[0]:
        #         node_choices[1] = adjacent_node
        #     elif adjacent_node.position[1] < current_node.position[1]:
        #         node_choices[2] = adjacent_node
        #     elif adjacent_node.position[1] > current_node.position[1]:
        #         node_choices[3] = adjacent_node
        #
        # current_node = node_choices[adjacent_index]

        # for adjacent_node in adjacent_nodes:
        #     cost = math.dist(current_path.node.position, adjacent_node.position) + current_path.cost
        #     distance_to_end_node = math.dist(adjacent_node.position, end_node.position)
        #
        #     add = True
        #
        #     if adjacent_node in complete:
        #         add = False
        #
        #     for path in queue:
        #         if path.node is adjacent_node:
        #             if cost >= path.cost:
        #                 add = False
        #             else:
        #                 queue.remove(path)
        #
        #     if add:
        #         draw_line(current_path.node, adjacent_node, color_rgb(192, 96, 96), 4)
        #         queue.append(Path(adjacent_node, cost, distance_to_end_node, current_path))
        #
        # queue = sort_paths(queue)
        #
        # if not queue:
        #     current_path.parent = None
        #     break
        #
        # best_path = queue[0]

        # time.sleep(0.01)
        draw_line(previous_node, current_node, color_rgb(128, 64, 64), 3)

        # current_path = queue[0]

    # complete_path = []
    #
    # while current_path.parent is not None:
    #     complete_path.insert(0, current_path)
    #     current_path = current_path.parent
    #
    # for path in complete_path:
    #     draw_line(path.parent.node, path.node, color_rgb(255, 96, 96), 5)

    window.getMouse()
