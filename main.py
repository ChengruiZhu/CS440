import queue
import utils


def dfs(graph, current_x, current_y, visited):
    visited.append([current_x, current_y])
    if graph[current_x][current_y] == '.':
        return True
    graph[current_x][current_y] = '~'
    children = utils.get_children(graph, current_x, current_y)
    for child in children:
        if child not in visited:
            if dfs(graph, child[0], child[1], visited):
                return True
    return False


def bfs(graph, start_x, start_y):
    q = queue.Queue()
    visited = [[start_x, start_y]]
    q.put([start_x, start_y])
    while q.qsize() > 0:
        [current_x, current_y] = q.get()
        if graph[current_x][current_y] == '.':
            return True
        graph[current_x][current_y] = '~'
        children = utils.get_children(graph, current_x, current_y)
        for child in children:
            if child not in visited:
                visited.append(child)
                q.put(child)


def greedy_bfs(graph, start_x, start_y, end_x, end_y):
    current_x, current_y = start_x, start_y
    children = utils.get_children(graph, current_x, current_y)
    visited = []
    count = 0
    while children:
        count += 1
        if graph[current_x][current_y] == '.':
            return True
        graph[current_x][current_y] = '~'
        min_distance = 2147483647
        for child in children:
            if child not in visited:
                visited.append(child)
                distance_to_end = utils.get_distance(child[0], child[1], end_x, end_y)
                if distance_to_end < min_distance:
                    min_distance = distance_to_end
                    [current_x, current_y] = child
        children = utils.get_children(graph, current_x, current_y)
        if count > 100000:
            return False
    return False


def a_star(graph, start_x, start_y, end_x, end_y):
    current_x, current_y = start_x, start_y
    children = utils.get_children(graph, current_x, current_y)
    visited = []
    count = 0
    while children:
        count += 1
        if graph[current_x][current_y] == '.':
            return True
        graph[current_x][current_y] = '~'
        min_distance = 2147483647
        for child in children:
            if child not in visited:
                visited.append(child)
                f_n = utils.get_distance(child[0], child[1], end_x, end_y) + utils.get_distance(child[0], child[1], start_x, start_y)
                if f_n < min_distance:
                    min_distance = f_n
                    [current_x, current_y] = child
        children = utils.get_children(graph, current_x, current_y)
        if count > 100000:
            return False
    return False


def choose_maze():
    maze_type = input('Please choose a maze:\n'
                        '1. Medium Maze\n'
                        '2. Big Maze\n'
                        '3. Open Maze\n')
    if maze_type == '1':
        maze = utils.setup_maze('mediumMaze.txt')
    elif maze_type == '2':
        maze = utils.setup_maze('bigMaze.txt')
    elif maze_type == '3':
        maze = utils.setup_maze('openMaze.txt')
    else:
        print('Input illegal')
        maze = utils.setup_maze('smallMaze.txt')
    return maze


maze = choose_maze()
[start_x, start_y] = utils.find_start(maze)
[end_x, end_y] = utils.find_end(maze)
visited = []

search_type = input('Please choose a search method:\n'
                    '1. DFS\n'
                    '2. BFS\n'
                    '3. Greedy BFS\n'
                    '4. A*\n')
if search_type == '1':
    print(dfs(maze, start_x, start_y, visited))
elif search_type == '2':
    print(bfs(maze, start_x, start_y))
elif search_type == '3':
    print(greedy_bfs(maze, start_x, start_y, end_x, end_y))
elif search_type == '4':
    print(a_star(maze, start_x, start_y, end_x, end_y))
else:
    print('Input illegal')

maze[start_x][start_y] = 'P'
maze[end_x][end_y] = '.'
for line in maze:
    line = ''.join(line)
    print(line)
