from __future__ import annotations
import math
import time
import tkinter as tk
import random
import numpy as np
import ctypes as ct
from dataclasses import dataclass

window_width = 1000
window_height = 1000
window_padding = 64

maze_columns = 65
maze_rows = 65

tile_width = (window_width - window_padding * 2) / maze_columns
tile_height = (window_height - window_padding * 2) / maze_rows


def dark_title_bar(window):
    window.update()
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = 20
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))


root = tk.Tk()
root.geometry(f'{window_width}x{window_height}')
dark_title_bar(root)
root.configure(background='#101010')

canvas = tk.Canvas(root, width=window_width, height=window_height, background='#101010',
                   bd=0, highlightthickness=0, relief='ridge')

canvas.pack(expand=True)
root.eval('tk::PlaceWindow . center')

time_step = 0.0005


def draw_to_parent(current_node, color):
    x = current_node.parent.position[0] * tile_width + window_padding
    y = current_node.parent.position[1] * tile_height + window_padding

    canvas.create_rectangle(x, y, x + tile_width, y + tile_height, fill=color, outline='')

    x = (current_node.position[0] + (current_node.parent.position[0] -
                                     current_node.position[0]) // 2) * tile_width + window_padding
    y = (current_node.position[1] + (current_node.parent.position[1] -
                                     current_node.position[1]) // 2) * tile_height + window_padding

    canvas.create_rectangle(x, y, x + tile_width, y + tile_height, fill=color, outline='')

    x = current_node.position[0] * tile_width + window_padding
    y = current_node.position[1] * tile_height + window_padding

    canvas.create_rectangle(x, y, x + tile_width, y + tile_height, fill=color, outline='')


while True:
    for maze_row in range(maze_rows):
        for maze_column in range(maze_columns):
            x = maze_column * tile_width + window_padding
            y = maze_row * tile_height + window_padding

            tile = canvas.create_rectangle(x, y, x + tile_width, y + tile_height, fill='#181818', outline='')

    tiles = np.zeros((maze_columns, maze_rows), dtype=np.bool_)

    start_tile = (1, 1)

    stack = [start_tile]

    visited = []

    while len(stack):
        current_tile = stack[-1]
        visited.append(current_tile)
        tiles[current_tile[0]][current_tile[1]] = True
        stack.pop()

        x = current_tile[0] * tile_width + window_padding
        y = current_tile[1] * tile_height + window_padding

        canvas.create_rectangle(x, y, x + tile_width, y + tile_height, fill='#404040', outline='')

        options = []

        if current_tile[0] > 1 and (current_tile[0] - 2, current_tile[1]) not in visited:
            options.append((-1, 0))
        if current_tile[1] > 1 and (current_tile[0], current_tile[1] - 2) not in visited:
            options.append((0, -1))
        if current_tile[0] < maze_columns - 2 and (current_tile[0] + 2, current_tile[1]) not in visited:
            options.append((1, 0))
        if current_tile[1] < maze_rows - 2 and (current_tile[0], current_tile[1] + 2) not in visited:
            options.append((0, 1))

        if options:
            stack.append(current_tile)
            option = random.choice(options)

            tiles[current_tile[0] + option[0]][current_tile[1] + option[1]] = True
            stack.append((current_tile[0] + 2 * option[0], current_tile[1] + 2 * option[1]))

            x = (current_tile[0] + option[0]) * tile_width + window_padding
            y = (current_tile[1] + option[1]) * tile_height + window_padding

            canvas.create_rectangle(x, y, x + tile_width, y + tile_height, fill='#404040', outline='')

            time.sleep(time_step)
            root.update()

    root.update()


    @dataclass
    class Node:
        position: tuple[int, int]
        cost: float
        heuristic: float
        opened: bool
        parent: Node or None


    current_node = Node((1, 1), 0, math.dist((1, 1), (maze_columns - 2, maze_rows - 2)), True, None)
    end_node = Node((maze_columns - 2, maze_rows - 2), math.inf, 0, True, None)

    nodes: list[Node] = [current_node]

    while current_node.position != end_node.position:
        for direction in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            relative_x = current_node.position[0] + 2 * direction[0]
            relative_y = current_node.position[1] + 2 * direction[1]

            intermediate_x = current_node.position[0] + direction[0]
            intermediate_y = current_node.position[1] + direction[1]

            if (((direction == (-1, 0) and current_node.position[0] > 1) or
                    (direction == (0, -1) and current_node.position[1] > 1) or
                    (direction == (1, 0) and current_node.position[0] < maze_columns - 2) or
                    (direction == (0, 1) and current_node.position[1] < maze_rows - 2))
                    and tiles[intermediate_x][intermediate_y]):
                adjacent_position = (relative_x, relative_y)

                cost = current_node.cost + 2

                # heuristic = abs(maze_columns - 1 - adjacent_position[0]) + abs(maze_rows - 1 - adjacent_position[1])
                heuristic = math.dist(adjacent_position, (maze_columns - 1, maze_rows - 1))

                duplicates = [x for x in nodes if x.position == adjacent_position]

                if duplicates:
                    if cost < duplicates[0].cost:
                        duplicates[0].cost = cost
                        duplicates[0].parent = current_node
                        duplicates[0].opened = True
                else:
                    nodes.append(Node(adjacent_position, cost, heuristic, True, current_node))

                    color = '#c06060'

                    x = relative_x * tile_width + window_padding
                    y = relative_y * tile_height + window_padding

                    canvas.create_rectangle(x, y, x + tile_width, y + tile_height, fill=color, outline='')

                    x = intermediate_x * tile_width + window_padding
                    y = intermediate_y * tile_height + window_padding

                    canvas.create_rectangle(x, y, x + tile_width, y + tile_height, fill=color, outline='')

                    time.sleep(time_step)
                    root.update()

        current_node.opened = False

        sorted_nodes = sorted([x for x in nodes if x.opened], key=lambda x: x.cost + x.heuristic)

        if sorted_nodes:
            current_node = sorted_nodes[0]

        if current_node.parent is not None:
            draw_to_parent(current_node, '#804040')

            time.sleep(time_step)
            root.update()

    while current_node.parent is not None:
        time.sleep(time_step)

        draw_to_parent(current_node, '#ff6060')

        time.sleep(time_step)
        root.update()

        current_node = current_node.parent

    time.sleep(0.25)
    canvas.delete('all')
