import queue
import utils


def dfs(graph, current_x, current_y, visited):
    visited.append([current_x, current_y])
    if graph[current_x][current_y] == '.':
        return True
    graph[current_x][current_y] = '.'
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
        graph[current_x][current_y] = '.'
        children = utils.get_children(graph, current_x, current_y)
        for child in children:
            if child not in visited:
                visited.append(child)
                q.put(child)


def greedy_bfs(graph, start_x, start_y, end_x, end_y):
    visited = []
    frontier = [[start_x, start_y]]
    while frontier:
        [current_x, current_y] = utils.get_best_score_greedy(frontier, end_x, end_y)
        if graph[current_x][current_y] == '.':
            return True
        frontier.remove([current_x, current_y])
        visited.append([current_x, current_y])
        graph[current_x][current_y] = '.'
        for child in utils.get_children(graph, current_x, current_y):
            if (child not in visited) and (child not in frontier):
                frontier.append(child)
    return False


def a_star(graph, start_x, start_y, end_x, end_y):
    visited = []
    frontier = [[start_x, start_y]]
    g = utils.get_g(graph, start_x, start_y)
    h = [[0 for i in range(len(graph[0]))] for j in range(len(graph))]
    h[start_x][start_y] = utils.get_distance(start_x, start_y, end_x, end_y)
    while frontier:
        [current_x, current_y] = utils.get_best_score_a_star(frontier, g, h)
        if graph[current_x][current_y] == '.':
            return True
        frontier.remove([current_x, current_y])
        visited.append([current_x, current_y])
        graph[current_x][current_y] = '.'
        for child in utils.get_children(graph, current_x, current_y):
            child_current_cost = g[current_x][current_y] + 1
            if child in frontier:
                if g[child[0]][child[1]] <= child_current_cost:
                    continue
            elif child in visited:
                if g[child[0]][child[1]] <= child_current_cost:
                    continue
                visited.remove(child)
                frontier.append(child)
            else:
                frontier.append(child)
                h[child[0]][child[1]] = utils.get_distance(child[0], child[1], end_x, end_y)
            g[child[0]][child[1]] = child_current_cost
        visited.append([current_x, current_y])
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
