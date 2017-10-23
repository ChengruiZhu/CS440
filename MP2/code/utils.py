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
    # colors = []
    # for line in f:
    #     line = line.rstrip('\n')
    #     for char in line:
    #         if char != '_':
    #             colors.append(char)
    # colors = list(set(colors))
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
# def select_node(graph):
#     result = None
#     maxnum_of_neighbors = 0
#     for line in graph:
#         for node in line:
#             if node.value == '_':
#                 num_of_neighbors = len(get_assigned_neighbors(graph, node))
#                 if num_of_neighbors >= maxnum_of_neighbors:
#                     maxnum_of_neighbors = num_of_neighbors
#                     result = node
#     return result


def select_node(graph):
    for line in graph:
        for node in line:
            if node.value == '_':
                return node


# select the least constraining value
# def select_color(graph, node):
#     colors = node.colors
#     assigned_neighbors = get_assigned_neighbors(graph, node)
#     num_neighbors = len(assigned_neighbors)
#     for neighbor in assigned_neighbors:


# def current_assignment_valid(graph, sources):
#     for line in graph:
#         for node in line:
#             if node.value != '_':
#                 a_neighbors = get_assigned_neighbors(graph, node)
#                 num_of_unassigned_neighbors = len(get_unassigned_neighbors(graph, node))
#                 if node_is_source(node, sources):
#                     count = 0
#                     for neighbor in a_neighbors:
#                         if neighbor.value == node.value:
#                             count += 1
#                     if count > 1 or (count != 1 and num_of_unassigned_neighbors == 0):
#                         return False
#                 else:
#                     count = 0
#                     for neighbor in a_neighbors:
#                         if neighbor.value == node.value:
#                             count += 1
#                     if count > 2 or (count != 2 and num_of_unassigned_neighbors < 2):
#                         return False
#     return True


def current_assignment_valid(graph, sources, current_node):
    nodes = [current_node]
    neighbors = get_assigned_neighbors(graph, current_node)
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
            if count > 1 or (count != 1 and num_of_unassigned_neighbors == 0):
                return False
        else:
            count = 0
            for neighbor in a_neighbors:
                if neighbor.value == node.value:
                    count += 1
            if count > 2 or (count != 2 and num_of_unassigned_neighbors < 2):
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


graph = setup_graph('../../MP2/inputs/input77.txt')
sources = find_sources(graph)
print(current_assignment_valid(graph, sources, graph[0][0]))
