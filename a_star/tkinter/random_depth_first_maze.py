import time
import tkinter as tk
import random
import numpy as np
import ctypes as ct


window_width = 1000
window_height = 1000
window_padding = 64

maze_columns = 63
maze_rows = 63

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

canvas = tk.Canvas(root, width=window_width, height=window_height, background='#111',
                   bd=0, highlightthickness=0, relief='ridge')

for maze_row in range(maze_rows):
    for maze_column in range(maze_columns):
        x = maze_column * tile_width + window_padding
        y = maze_row * tile_height + window_padding

        tile = canvas.create_rectangle(x, y, x + tile_width, y + tile_height, fill='#222', outline='')

canvas.pack()
root.eval('tk::PlaceWindow . center')

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

    canvas.create_rectangle(x, y, x + tile_width, y + tile_height, fill='#666', outline='')

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

        canvas.create_rectangle(x, y, x + tile_width, y + tile_height, fill='#666', outline='')

        time.sleep(0.0125)
        root.update()

root.mainloop()
