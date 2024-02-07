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
        options.append('left')
    if current_tile[1] > 1 and (current_tile[0], current_tile[1] - 2) not in visited:
        options.append('up')
    if current_tile[0] < maze_columns - 2 and (current_tile[0] + 2, current_tile[1]) not in visited:
        options.append('right')
    if current_tile[1] < maze_rows - 2 and (current_tile[0], current_tile[1] + 2) not in visited:
        options.append('down')

    option = ''

    if options:
        stack.append(current_tile)
        option = random.choice(options)

    intermediate_tile = (0, 0)

    if option == 'left':
        tiles[current_tile[0] - 1][current_tile[1]] = True
        intermediate_tile = (current_tile[0] - 1, current_tile[1])
        stack.append((current_tile[0] - 2, current_tile[1]))
    if option == 'up':
        tiles[current_tile[0]][current_tile[1] - 1] = True
        intermediate_tile = (current_tile[0], current_tile[1] - 1)
        stack.append((current_tile[0], current_tile[1] - 2))
    if option == 'right':
        tiles[current_tile[0] + 1][current_tile[1]] = True
        intermediate_tile = (current_tile[0] + 1, current_tile[1])
        stack.append((current_tile[0] + 2, current_tile[1]))
    if option == 'down':
        tiles[current_tile[0]][current_tile[1] + 1] = True
        intermediate_tile = (current_tile[0], current_tile[1] + 1)
        stack.append((current_tile[0], current_tile[1] + 2))

    if option:
        x = intermediate_tile[0] * tile_width + window_padding
        y = intermediate_tile[1] * tile_height + window_padding

        canvas.create_rectangle(x, y, x + tile_width, y + tile_height, fill='#666', outline='')

        time.sleep(0.0125)
        root.update()

root.mainloop()
