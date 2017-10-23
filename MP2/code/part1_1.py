import time
import sys
from random import shuffle
from MP2.code import utils


def dumb(graph, sources):
    utils.print_graph(graph)
    print('\n')
    if utils.assignment_complete(graph, sources):
        utils.print_graph(graph)
        return True
    for line in graph:
        for node in line:
            if node.value == '_':
                colors = utils.find_colors(graph)
                shuffle(colors)
                for color in colors:
                    node.value = color
                    result = dumb(graph, sources)
                    if result:
                        return result
                    node.value = '_'
    return False


def smart(graph, sources):
    utils.print_graph(graph)
    print('\n')
    if utils.assignment_complete(graph, sources):
        utils.print_graph(graph)
        return True
    node = utils.select_node(graph)
    for color in colors:
        node.value = color
        if utils.current_assignment_valid(graph, sources, node):
            smart(graph, sources)
        node.value = '_'
    return False


def choose_input():
    input_type = input('Please choose a graph:\n'
                        '1. 7*7\n'
                        '2. 8*8\n'
                        '3. 9*9\n')
    if input_type == '1':
        graph = utils.setup_graph('../../MP2/inputs/input77.txt')
    elif input_type == '2':
        graph = utils.setup_graph('../../MP2/inputs/input88.txt')
    elif input_type == '3':
        graph = utils.setup_graph('../../MP2/inputs/input991.txt')
    else:
        print('Input illegal')
        graph = utils.setup_graph('../../MP2/inputs/input44.txt')
        # sys.exit()
    return graph


graph = choose_input()
sources = utils.find_sources(graph)
colors = utils.find_colors(graph)

input_type = input('Please choose a method:\n'
                       '1. dumb\n'
                       '2. smart\n')
if input_type == '1':
    start = time.time()
    print(dumb(graph, sources))
    print(time.time() - start)
elif input_type == '2':
    start = time.time()
    print(smart(graph, sources))
    print(time.time() - start)
else:
    print('Input illegal')
    sys.exit()











































