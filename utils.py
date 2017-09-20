# maze_name is the name of txt file
def setup_maze(maze_name):
    f = open(maze_name, 'r')
    maze = [list(line.rstrip('\n')) for line in f.readlines()]
    return maze


def find_start(maze):
    x = -1
    for line in maze:
        x += 1
        y = -1
        for char in line:
            y += 1
            if char == 'P':
                return x, y


def find_end(maze):
    x = -1
    for line in maze:
        x += 1
        y = -1
        for char in line:
            y += 1
            if char == '.':
                return [x, y]


def get_distance(current_x, current_y, end_x, end_y):
    return abs(end_x - current_x) + abs(end_y - current_y)


def get_children(graph, x, y):
    children = []
    graph_length = len(graph[0])
    graph_width = len(graph)
    if (x + 1) < graph_width:
        if graph[x + 1][y] != '%':
            children.append([x + 1, y])
    if (y + 1) < graph_length:
        if graph[x][y + 1] != '%':
            children.append([x, y + 1])
    if x > 0:
        if graph[x - 1][y] != '%':
            children.append([x - 1, y])
    if y > 0:
        if graph[x][y - 1] != '%':
            children.append([x, y - 1])

    return children
