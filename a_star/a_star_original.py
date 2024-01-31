import math

from graphics import *

window = GraphWin("A*", 720, 640)

points = [
    [1, 358, 170], [2, 0, 43], [3, 115, 42], [4, 268, 1], [5, 460, 0], [6, 604, 2], [7, 270, 44], [8, 460, 51],
    [9, 269, 172], [10, 404, 175], [11, 462, 174], [12, 600, 125], [13, 124, 327], [14, 248, 327], [15, 401, 328],
    [16, 455, 327], [17, 604, 334], [18, 254, 434], [19, 402, 437], [20, 457, 434], [21, 606, 445],
]

connections = [
    [1, 9], [1, 10], [2, 3], [3, 4], [3, 7], [3, 13], [4, 5], [4, 7], [5, 6], [5, 8], [6, 12], [7, 8], [7, 9], [8, 11],
    [9, 14], [10, 11], [10, 15], [11, 12], [11, 16], [11, 17], [12, 17], [13, 14], [14, 15], [14, 18], [15, 16],
    [15, 19], [16, 17], [16, 20], [17, 21], [18, 19], [19, 20], [20, 21],
]

circles = []
lines = []
lengths = []

for point in points:
    point[1] += 64
    point[2] += 64

for connection in connections:
    point_1 = points[connection[0] - 1][1:]
    point_2 = points[connection[1] - 1][1:]

    line = Line(Point(*point_1), Point(*point_2))
    line.setWidth(2)
    line.draw(window)

    lines.append(line)

    dx = point_2[0] - point_1[0]
    dy = point_2[1] - point_1[1]

    distance = math.sqrt(dx ** 2 + dy ** 2)

    lengths.append(distance)

    center = [point_1[0] + dx / 2, point_1[1] + dy / 2]

lengths = [length / 71 for length in lengths]

for point in points:
    circle = Circle(Point(point[1], point[2]), 16)
    circle.setFill(color_rgb(255, 255, 255))
    circle.setWidth(2)
    circle.draw(window)

    circles.append(circle)

    text = Text(Point(point[1], point[2]), point[0])
    text.draw(window)


def distance_of(point_1, point_2):
    return math.sqrt((point_2[0] - point_1[0]) ** 2 + (point_2[1] - point_1[1]) ** 2)


point = points[0]

goal_point = points[1]
line_colors = [False for line in lines]

wait_time_seconds = 0.25

window.getMouse()

total_distance = 0

while point != goal_point:
    costs = []

    for connection_index, connection in enumerate(connections):
        if connection[0] == point[0] or connection[1] == point[0]:
            if not line_colors[connection_index]:
                lines[connection_index].setFill('green')
                time.sleep(wait_time_seconds)
                lines[connection_index].setFill('black')
                distance = lengths[connection_index]
                other_point = connection[0] if connection[1] == point[0] else connection[1]
                h = distance_of(points[other_point - 1][1:], goal_point[1:])
                costs.append([distance + h + total_distance, other_point - 1, connection_index, distance])

    minimum = costs[0][0]
    min_index = costs[0][1]
    min_connection = costs[0][2]
    min_distance = costs[0][3]

    for cost in costs:
        if cost[0] < minimum:
            minimum = cost[0]
            min_index = cost[1]
            min_connection = cost[2]
            min_distance = cost[3]

    total_distance += min_distance
    time.sleep(wait_time_seconds)
    line_colors[min_connection] = True
    lines[min_connection].setFill('red')

    point = points[min_index]

window.getMouse()
window.close()

print(total_distance)
