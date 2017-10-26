import time
import sys
from random import shuffle
from MP2.code import utils


def dumb(graph, sources):
    global num_assignment
    if utils.assignment_complete(graph, sources):
        utils.print_graph(graph)
        return True
    for line in graph:
        for node in line:
            num_assignment += 1
            if node.value == '_':
                shuffle(colors)
                for color in colors:
                    node.value = color
                    result = dumb(graph, sources)
                    if result:
                        return result
                    node.mark('_')
    return False


def smart(graph, sources):
    global num_assignment
    if utils.assignment_complete(graph, sources):
        utils.print_graph(graph)
        print(num_assignment)
        return True
    node = utils.select_node(graph)
    num_assignment += 1
    for color in utils.select_color(graph, colors, node):
        node.mark(color)
        if utils.current_assignment_valid(graph, sources, node):
            result = smart(graph, sources)
            if result:
                return result
        node.mark('_')
    return False


def choose_input():
    input_type = input('Please choose a graph:\n'
                        '1. 7*7\n'
                        '2. 8*8\n'
                        '3. 9*9\n'
                        '4. 10*10 (1)\n'
                        '5. 10*10 (2)\n'
                        '6. 12*12\n'
                        '7. 12*14\n'
                        '8. 14*14\n'
                       )
    if input_type == '1':
        graph = utils.setup_graph('../../MP2/inputs/input77.txt')
    elif input_type == '2':
        graph = utils.setup_graph('../../MP2/inputs/input88.txt')
    elif input_type == '3':
        graph = utils.setup_graph('../../MP2/inputs/input991.txt')
    elif input_type == '4':
        graph = utils.setup_graph('../../MP2/inputs/input10101.txt')
    elif input_type == '5':
        graph = utils.setup_graph('../../MP2/inputs/input10102.txt')
    elif input_type == '6':
        graph = utils.setup_graph('../../MP2/inputs/input1212.txt')
    elif input_type == '7':
        graph = utils.setup_graph('../../MP2/inputs/input1214.txt')
    elif input_type == '8':
        graph = utils.setup_graph('../../MP2/inputs/input1414.txt')
    else:
        print('Input illegal')
        sys.exit()
    return graph


graph = choose_input()
sources = utils.find_sources(graph)
colors = utils.find_colors(graph)
num_assignment = 0

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
