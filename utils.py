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


def get_distance(current_x, current_y, goal_x, goal_y):
    return abs(goal_x - current_x) + abs(goal_y - current_y)


def get_children(graph, x, y):
    children = []
    graph_length = len(graph[0])
    graph_width = len(graph)
    if (x + 1) < graph_width:
        if graph[x + 1][y] != '%' and graph[x + 1][y] != 'P':
            children.append([x + 1, y])
    if (y + 1) < graph_length:
        if graph[x][y + 1] != '%' and graph[x][y + 1] != 'P':
            children.append([x, y + 1])
    if x > 0:
        if graph[x - 1][y] != '%' and graph[x - 1][y] != 'P':
            children.append([x - 1, y])
    if y > 0:
        if graph[x][y - 1] != '%' and graph[x][y - 1] != 'P':
            children.append([x, y - 1])
    return children


def get_best_score_a_star(nodes, start_x, start_y, end_x, end_y):
    min_distance = 2147483647
    for node in nodes:
        f_n = (get_distance(node[0], node[1], start_x, start_y) +
               get_distance(node[0], node[1], end_x, end_y))
        if f_n < min_distance:
            min_distance = f_n
            res_x, res_y = node
    return [res_x, res_y]


def get_best_score_greedy(nodes, end_x, end_y):
    min_distance = 2147483647
    for node in nodes:
        distance_to_end = get_distance(node[0], node[1], end_x, end_y)
        if distance_to_end < min_distance:
            min_distance = distance_to_end
            [res_x, res_y] = node
    return [res_x, res_y]


def get_g(graph, start_x, start_y):
    g = [[0 for i in range(len(graph[0]))] for j in range(len(graph))]
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            g[i][j] = get_distance(i, j, start_x, start_y)
    return g
