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


def setup_graph(input_name):
    f = open(input_name, 'r')
    f = f.readlines()
    graph = []
    x = 0
    for line in f:
        line = line.rstrip('\n')
        row = []
        y = 0
        for char in line:
            node = Node(x, y, char)
            y += 1
            row.append(node)
        x += 1
        graph.append(row)
    return graph


# return source nodes
def find_sources(graph):
    result = []
    for line in graph:
        for node in line:
            if node.value != '_':
                result.append(node)
    return result


# return ['O', 'B', 'Y', ...]
def find_colors(graph):
    sources = find_sources(graph)
    colors = []
    while sources:
        tmp = sources[0]
        sources = sources[1:]
        for node in sources:
            if tmp.value == node.value:
                colors.append(tmp.value)
                sources.remove(node)
    return colors


def node_is_source(node, sources):
    for source in sources:
        if source.x == node.x and source.y == node.y:
            return True
    return False


def assignment_complete(graph, sources):
    for line in graph:
        for node in line:
            if node.value == '_':
                return False
            neighbors = get_assigned_neighbors(graph, node)
            if node_is_source(node, sources):
                count = 0
                for neighbor in neighbors:
                    if neighbor.value == node.value:
                        count += 1
                if count != 1:
                    return False
            else:
                count = 0
                for neighbor in neighbors:
                    if neighbor.value == node.value:
                        count += 1
                if count != 2:
                    return False
    return True


# select the most constrained variable
def select_node(graph):
    result = None
    num = 100
    for line in graph:
        for node in line:
            if node.value == '_':
                num_of_u_neighbors = len(get_unassigned_neighbors(graph, node))
                if num_of_u_neighbors < num:
                    num = num_of_u_neighbors
                    result = node
    return result


# select the least constraining value
def select_color(graph, colors, node):
    res = []
    assigned_neighbors = get_assigned_neighbors(graph, node)
    num_neighbors = len(assigned_neighbors)
    if assigned_neighbors:
        res.append(assigned_neighbors[0].value)
    if num_neighbors > 1 and assigned_neighbors[1].value not in res:
        res.append(assigned_neighbors[1].value)
    if num_neighbors > 2 and assigned_neighbors[2].value not in res:
        res.append(assigned_neighbors[2].value)
    for color in colors:
        if color not in res:
            res.append(color)
    return res


def current_assignment_valid(graph, sources, current_node):
    nodes = [current_node]
    neighbors = get_assigned_neighbors(graph, current_node)
    u_neighbors = get_unassigned_neighbors(graph, current_node)

    for neighbor in neighbors:
        nodes.append(neighbor)
    for node in nodes:
        a_neighbors = get_assigned_neighbors(graph, node)
        num_of_unassigned_neighbors = len(get_unassigned_neighbors(graph, node))
        if node_is_source(node, sources):
            count = 0
            for neighbor in a_neighbors:
                if neighbor.value == node.value:
                    count += 1
            if count > 1 or (count == 0 and num_of_unassigned_neighbors == 0):
                return False
        else:
            count = 0
            for neighbor in a_neighbors:
                if neighbor.value == node.value:
                    count += 1
            if count > 2 or (count == 0 and num_of_unassigned_neighbors < 2) or \
                    (count == 1 and num_of_unassigned_neighbors == 0):
                return False
    if u_neighbors:
        for u_neighbor in u_neighbors:
            # assigned neighbors of the unassigned neighbor
            au_neighbors = get_assigned_neighbors(graph, u_neighbor)
            # unassigned neighbors of the unassigned neighbor
            uu_neighbors = get_unassigned_neighbors(graph, u_neighbor)
            a_num = len(au_neighbors)
            u_num = len(uu_neighbors)
            a_value = []
            if au_neighbors:
                for neighbor in au_neighbors:
                    a_value.append(neighbor.value)
                a_value = list(set(a_value))

                if a_num == 4 and len(a_value) != 3:
                    return False
                if a_num == 3 and len(a_value) == 1:
                    return False
                if a_num == 3 and u_num == 0 and len(a_value) == 3:
                    return False
                if a_num == 2 and u_num == 0 and len(a_value) == 2:
                    return False
    return True


def print_graph(graph):
    res = []
    for line in graph:
        row = []
        for char in line:
            row.append(char.value)
        res.append(row)
        print(''.join(row))


def get_assigned_neighbors(graph, node):
    children = []
    graph_length = len(graph[0])
    graph_width = len(graph)
    if (node.x + 1) < graph_width:
        if graph[node.x + 1][node.y].value != '_':
            children.append(graph[node.x + 1][node.y])
    if (node.y + 1) < graph_length:
        if graph[node.x][node.y + 1].value != '_':
            children.append(graph[node.x][node.y + 1])
    if node.x > 0:
        if graph[node.x - 1][node.y].value != '_':
            children.append(graph[node.x - 1][node.y])
    if node.y > 0:
        if graph[node.x][node.y - 1].value != '_':
            children.append(graph[node.x][node.y - 1])
    return children


def get_unassigned_neighbors(graph, node):
    children = []
    graph_length = len(graph[0])
    graph_width = len(graph)
    if (node.x + 1) < graph_width:
        if graph[node.x + 1][node.y].value == '_':
            children.append(graph[node.x + 1][node.y])
    if (node.y + 1) < graph_length:
        if graph[node.x][node.y + 1].value == '_':
            children.append(graph[node.x][node.y + 1])
    if node.x > 0:
        if graph[node.x - 1][node.y].value == '_':
            children.append(graph[node.x - 1][node.y])
    if node.y > 0:
        if graph[node.x][node.y - 1].value == '_':
            children.append(graph[node.x][node.y - 1])
    return children
