import sys
import logging

GREEN = '\x1b[1;32;40m'
RED = '\x1b[1;31;40m'
END = '\x1b[0m'
logging.basicConfig(
    filename='runLog.log',
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
log = logging.getLogger(__name__)

def resultSaver(fileName, minimumNode):
    try:
        resultReader = open(fileName, 'r')
        fileLines = resultReader.readlines()
        fileLines[minimumNode] = fileLines[minimumNode].replace('e', 'ne')
        resultWriter = open(fileName, 'w')
        resultWriter.writelines(fileLines)
        log.info('Map actualizing SUCCESSFUL')
    except Exception as ex:
        log.error('Something went wrong!\n' + str(ex))
    finally:
        resultReader.close()
        resultWriter.close()

def mapBuilder(mapFile):
    graph = []
    try:
        map = open(mapFile, 'r')
        for line in map:
            graph.append(line.split("\t"))
        for row in graph:
            row[-1] = row[-1].rstrip("\n")
        log.info('Map building SUCCESSFUL from ' + mapFile)   
    except Exception as ex:
        log.error('Something went wrong with reading ' + mapFile + ' map file!\n' + str(ex))
    finally:
        map.close()
    return graph   

def minimumDistance(distance, visitedNode, numberOfNodes):
    min = sys.maxsize
    minimumIndex = 0
    for check in range(numberOfNodes):
        if distance[check] < min and visitedNode[check] == False:
            min = distance[check]
            minimumIndex = check
    return minimumIndex

def pathBuilder(parent, minimumNode, path):
    if parent[minimumNode] == -1 :
        path.append(minimumNode)
        return
    pathBuilder(parent , parent[minimumNode], path)
    path.append(minimumNode)
    log.info('Path built successfully!')
    return path

def printSolution(distance, nodeNumber, graph, start, fileName, parent):
    minimumPath = sys.maxsize
    minimumNode = sys.maxsize
    occupiedCounter = 0
    totalCounter = 0
    optimalPath = []
    print ("Starting node:", start)
    print ("Parking nodes: ")
    for node in range(nodeNumber):
        rowsOfGraph = graph[node]
        if distance[node] < minimumPath and distance[node] != 0 and rowsOfGraph[-2] == 'p' and rowsOfGraph[-1] == 'e':
            minimumPath = distance[node]
            minimumNode = node
        if rowsOfGraph[-2] == 'p':
            totalCounter += 1
            if rowsOfGraph[-1] == 'e':
                print ("Node", node, "is a parking node, status: " + GREEN + "EMPTY" + END) 
                log.debug('Empty node: ' + str(node)) 
            if rowsOfGraph[-1] == 'ne':
                print ("Node", node, "is a parking node, status: " + RED + "NOT EMPTY" + END)
                occupiedCounter += 1
                log.debug('Not empty node: ' + str(node))
    if minimumNode > nodeNumber:
        minimumNode = 'NO EMPTY SLOT'
        minimumPath = 'NO EMPTY SLOT'
        print ('========================================')
        print ('Occupied slots: ' + RED + str(occupiedCounter) + '/' + str(totalCounter) + END)
        print (RED + 'THERE IS NO EMPTY PARKING NODE RIGHT NOW' + END)
        log.info('Optimal path: NO EMPTY SLOT')
        print ('========================================')  
    else:
        print ('========================================')
        print ("Shortest path from starting node is: ", minimumPath, " and the target node to park is: ", minimumNode)
        optimalPath = pathBuilder(parent, minimumNode, optimalPath)
        print (GREEN + "Optimal path is: " + str(optimalPath) + END)
        print ('Occupied slots: ' + GREEN + str(occupiedCounter) + '/' + str(totalCounter) + END)
        log.info('Optimal path: ' + str(optimalPath))
        print ('========================================')
        resultSaver(fileName, minimumNode)  

def pathfinder(startingNode, fileName):
    log.info('Pathfinding started')
    graph = mapBuilder(fileName)
    nodeNumber = len(graph)
    distance = [sys.maxsize] * nodeNumber
    distance[startingNode] = 0
    visited = [False] * nodeNumber
    parent = [-1] * len(graph[0])
    for cout in range(nodeNumber):
        row = minimumDistance(distance, visited, nodeNumber)
        visited[row] = True
        for col in range(nodeNumber):
            if int(graph[row][col]) > 0 and visited[col] == False and distance[col] > distance[row] + int(graph[row][col]):
                distance[col] = distance[row] + int(graph[row][col])
                parent[col] = row
    log.info('Pathfinding finished')   
    printSolution(distance, nodeNumber, graph, startingNode, fileName, parent)

#pathfinder(0 , 'map_state_ip.txt')
pathfinder(52 , 'map_state_ai.txt')