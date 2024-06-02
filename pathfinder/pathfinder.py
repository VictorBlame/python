import sys

from variables import RED, GREEN, END, LOG


def result_saver(file_name, minimum_node):
    try:
        result_reader = open(file_name, 'r')
        file_lines = result_reader.readlines()
        file_lines[minimum_node] = file_lines[minimum_node].replace('e', 'ne')
        result_writer = open(file_name, 'w')
        result_writer.writelines(file_lines)
        LOG.info('Map actualizing SUCCESSFUL')
    except Exception as ex:
        LOG.error('Something went wrong!\n' + str(ex))
    finally:
        result_reader.close()
        result_writer.close()


def map_builder(map_file):
    graph = []
    try:
        map = open(map_file, 'r')
        for line in map:
            graph.append(line.split("\t"))
        for row in graph:
            row[-1] = row[-1].rstrip("\n")
        LOG.info('Map building SUCCESSFUL from ' + map_file)
    except Exception as ex:
        LOG.error('Something went wrong with reading ' + map_file + ' map file!\n' + str(ex))
    finally:
        map.close()
    return graph


def minimum_distance(distance, visited_node, number_of_nodes):
    min = sys.maxsize
    minimum_index = 0
    for check in range(number_of_nodes):
        if distance[check] < min and not visited_node[check]:
            min = distance[check]
            minimum_index = check
    return minimum_index


def path_builder(parent, minimum_node, path):
    if parent[minimum_node] == -1:
        path.append(minimum_node)
        return
    path_builder(parent, parent[minimum_node], path)
    path.append(minimum_node)
    LOG.info('Path built successfully!')
    return path


def print_solution(distance, node_number, graph, start, file_name, parent):
    minimum_path, minimum_node = sys.maxsize, sys.maxsize
    occupied_counter, total_counter = 0, 0
    optimal_path = []
    print("Starting node:", start)
    print("Parking nodes: ")
    for node in range(node_number):
        rows_of_graph = graph[node]
        if distance[node] < minimum_path and distance[node] is not 0 and rows_of_graph[-2] == 'p' and rows_of_graph[
            -1] == 'e':
            minimum_path = distance[node]
            minimum_node = node
        if rows_of_graph[-2] == 'p':
            total_counter += 1
            if rows_of_graph[-1] == 'e':
                print("Node", node, "is a parking node, status: " + GREEN + "EMPTY" + END)
                LOG.debug('Empty node: ' + str(node))
            if rows_of_graph[-1] == 'ne':
                print("Node", node, "is a parking node, status: " + RED + "NOT EMPTY" + END)
                occupied_counter += 1
                LOG.debug('Not empty node: ' + str(node))
    if minimum_node > node_number:
        print('========================================')
        print('Occupied slots: ' + RED + str(occupied_counter) + '/' + str(total_counter) + END)
        print(RED + 'THERE IS NO EMPTY PARKING NODE RIGHT NOW' + END)
        LOG.info('Optimal path: NO EMPTY SLOT')
        print('========================================')
    else:
        print('========================================')
        print("Shortest path from starting node is: ", minimum_path, " and the target node to park is: ", minimum_node)
        optimal_path = path_builder(parent, minimum_node, optimal_path)
        print(GREEN + "Optimal path is: " + str(optimal_path) + END)
        print('Occupied slots: ' + GREEN + str(occupied_counter) + '/' + str(total_counter) + END)
        LOG.info('Optimal path: ' + str(optimal_path))
        print('========================================')
        result_saver(file_name, minimum_node)


def pathfinder(starting_node, file_name):
    LOG.info('Pathfinding started')
    graph = map_builder(file_name)
    node_number = len(graph)
    distance = [sys.maxsize] * node_number
    distance[starting_node] = 0
    visited = [False] * node_number
    parent = [-1] * len(graph[0])
    for _ in range(node_number):
        row = minimum_distance(distance, visited, node_number)
        visited[row] = True
        for col in range(node_number):
            if int(graph[row][col]) > 0 and not visited[col] and distance[col] > distance[row] + int(
                    graph[row][col]):
                distance[col] = distance[row] + int(graph[row][col])
                parent[col] = row
    LOG.info('Pathfinding finished')
    print_solution(distance, node_number, graph, starting_node, file_name, parent)


# pathfinder(0 , 'map_state_ip.txt')
pathfinder(52, 'map_state_ai.txt')
