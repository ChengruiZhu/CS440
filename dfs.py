# maze_name is the name of txt file
def setup_maze(maze_name):
    f = open(maze_name, 'r')
    maze = [list(line.rstrip('\n')) for line in f.readlines()]

    start_x = find_start(maze)[0]
    start_y = find_start(maze)[1]
    end_x = find_end(maze)[0]
    end_y = find_end(maze)[1]
    print('start: ', start_x, start_y, 'end: ', end_x, end_y)
    print(maze)
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


setup_maze('mediumMaze.txt')

