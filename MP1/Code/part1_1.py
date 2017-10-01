import queue
import sys

from MP1.Code import utils


def dfs(maze, current, visited):
    global step_dfs, expanded_node_dfs
    visited.append(current)
    if current.value == '.':
        return True
    children = utils.get_children(maze, current)
    for child in children:
        if child not in visited:
            expanded_node_dfs += 1
            if dfs(maze, child, visited):
                child.mark('.')
                step_dfs += 1
                return True
    return False


def bfs(maze, start):
    global step_bfs, expanded_node_bfs
    q = queue.Queue()
    visited = [start]
    parent = {}
    q.put(start)
    while q.qsize() > 0:
        current = q.get()
        if current.value == '.':
            step_bfs = trace(maze, parent, current)
            return True
        children = utils.get_children(maze, current)
        for child in children:
            if child not in visited:
                visited.append(child)
                expanded_node_bfs += 1
                q.put(child)
                parent[child] = current
    return False


def trace(maze, parent, current):
    global step
    curr_parent = parent[current]
    if curr_parent:
        if parent[current].value != 'P':
            parent[current].mark('.')
            step += 1
            trace(maze, parent, parent[current])
    return step


def greedy_bfs(maze, start, end):
    global step_greedy, expanded_node_greedy
    visited = []
    frontier = [start]
    parent = {}
    while frontier:
        current = utils.get_best_score_greedy(frontier, end)
        if current.value == '.':
            step_greedy = trace(maze, parent, current)
            return True
        frontier.remove(current)
        visited.append(current)
        expanded_node_greedy += 1
        for child in utils.get_children(maze, current):
            if (child not in visited) and (child not in frontier):
                frontier.append(child)
                parent[child] = current
    return False


def a_star(maze, start, end):
    global expanded_node_a, step_a
    visited = []
    frontier = [start]
    parent = {}
    g = utils.get_g(maze, start)
    h = {}
    h[start] = utils.get_distance(start, end)
    current_cost_lower = False

    while frontier:
        # find next step where f = (g + h) is the lowest
        current = utils.get_best_score_a_star(frontier, g, h)
        if current.value == '.':
            step_a = trace(maze, parent, current)
            return True
        frontier.remove(current)
        visited.append(current)
        expanded_node_a += 1

        for child in utils.get_children(maze, current):
            if child in visited:
                continue
            child_current_g = g[current] + 1

            if child not in frontier:
                frontier.append(child)
                current_cost_lower = True
            elif child_current_g < g[child]:
                current_cost_lower = True

            if current_cost_lower:
                parent[child] = current
                g[child] = child_current_g
                h[child] = utils.get_distance(child, end)
    return False


def choose_maze():
    maze_type = input('Please choose a maze:\n'
                        '1. Medium Maze\n'
                        '2. Big Maze\n'
                        '3. Open Maze\n')
    if maze_type == '1':
        maze = utils.setup_maze('MP1/Input/mediumMaze.txt')
    elif maze_type == '2':
        maze = utils.setup_maze('MP1/Input/bigMaze.txt')
    elif maze_type == '3':
        maze = utils.setup_maze('MP1/Input/openMaze.txt')
    else:
        print('Input illegal')
        sys.exit()
    return maze


maze = choose_maze()
start = utils.find_start(maze)
end = utils.find_end(maze)
visited = []
step = step_dfs = step_bfs = step_greedy = step_a = 0
expanded_node_dfs = expanded_node_bfs = expanded_node_greedy = expanded_node_a = 0

search_type = input('Please choose a search method:\n'
                    '1. DFS\n'
                    '2. BFS\n'
                    '3. Greedy BFS\n'
                    '4. A*\n')
if search_type == '1':
    print(dfs(maze, start, visited))
    print('Path cost: ', step_dfs + 1)
    print('Expanded node: ', expanded_node_dfs)
elif search_type == '2':
    print(bfs(maze, start))
    print('Path cost: ', step_bfs + 1)
    print('Expanded node: ', expanded_node_bfs)
elif search_type == '3':
    print(greedy_bfs(maze, start, end))
    print('Path cost: ', step_greedy + 1)
    print('Expanded node: ', expanded_node_greedy)
elif search_type == '4':
    print(a_star(maze, start, end))
    print('Path cost: ', step_a + 1)
    print('Expanded node: ', expanded_node_a)
else:
    print('Input illegal')

utils.print_maze(maze)
