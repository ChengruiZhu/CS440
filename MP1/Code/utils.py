class Node(object):
    parent = None

    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def find_parent(self, node):
        self.parent = node

    def mark(self, new_value):
        self.value = new_value


# maze_name is the name of txt file
def setup_maze(maze_name):
    f = open(maze_name, 'r')
    x = y = 0
    maze = []
    for line in f.readlines():
        line = line.rstrip('\n')
        row = []
        y = 0
        for char in line:
            node = Node(x, y, char)
            y += 1
            row.append(node)
        x += 1
        maze.append(row)
    return maze


def find_start(maze):
    for line in maze:
        for char in line:
            if char.value == 'P':
                return char


def find_end(maze):
    for line in maze:
        for char in line:
            if char.value == '.':
                return char


def get_distance(current, goal):
    return abs(goal.x - current.x) + abs(goal.y - current.y)


def get_children(maze, node):
    children = []
    maze_length = len(maze[0])
    maze_width = len(maze)
    if (node.x + 1) < maze_width:
        if maze[node.x + 1][node.y].value != '%' and maze[node.x + 1][node.y].value != 'P':
            children.append(maze[node.x + 1][node.y])
    if (node.y + 1) < maze_length:
        if maze[node.x][node.y + 1].value != '%' and maze[node.x][node.y + 1].value != 'P':
            children.append(maze[node.x][node.y + 1])
    if node.x > 0:
        if maze[node.x - 1][node.y].value != '%' and maze[node.x - 1][node.y].value != 'P':
            children.append(maze[node.x - 1][node.y])
    if node.y > 0:
        if maze[node.x][node.y - 1].value != '%' and maze[node.x][node.y - 1].value != 'P':
            children.append(maze[node.x][node.y - 1])
    return children


def get_best_score_a_star(nodes, g, h):
    res = None
    min_distance = 2147483647

    for node in nodes:
        if (g[node] + h[node]) < min_distance:
            min_distance = g[node] + h[node]
            res = node
    return res


def get_best_score_greedy(nodes, end):
    res = None
    min_distance = 2147483647
    for node in nodes:
        distance_to_end = get_distance(node, end)
        if distance_to_end < min_distance:
            min_distance = distance_to_end
            res = node
    return res


def get_g(maze, start):
    g = {}
    for line in maze:
        for char in line:
            g[char] = get_distance(char, start)
    return g


def print_maze(maze):
    res = []
    for line in maze:
        row = []
        for char in line:
            row.append(char.value)
        res.append(row)
        print(''.join(row))
