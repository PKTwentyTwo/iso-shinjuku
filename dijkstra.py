#An implementation of Djikstra's algorithm.
#See https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm for more info.
#It can find the shortest path between two points on a network with n nodes in O(n^2) time.
#In this project (as well as the original Shinjuku), it is used to compile optimal syntheses from avaliable components.


#My testing variables are below. Note that they are not accurate to real data.
##nodes = ['xs0_0', 'xs4_33', 'xs5_253', 'xs7_25ac']
##distances = {'xs4_33':{'xs5_253':1, 'xs0_0':1, 'xs7_25ac':2}, 'xs5_253':{'xs4_33':1, 'xs0_0':2}, 'xs7_25ac':{'xs4_33':3,'xs0_0':5,'xs5_253':2}, 'xs0_0':{'xs4_33':1, 'xs5_253':1,'xs7_25ac':1}}
##target = 'xs0_0'
##startpoint = 'xs7_25ac'
import copy, random
values = {}
visited = []
def applydistances(node, distances, paths):
    global values, visited
    
    for x in distances[node]:
        distance = values[node] + distances[node][x]
        if distance < values[x]:
            values[x] = distance
            paths[x] = copy.deepcopy(paths[node])
            paths[x] += [x]
    visited.append(node)
    return paths
def getclosestunvisited(nodes, visited):
    mindistance = 999999
    minnode = None
    for x in nodes:
        if values[x] < mindistance and x not in visited:
            minnode = x
            mindistance = values[x]
    return minnode
def Dijkstra(nodes, distances, startpoint, target='xs0_0'):
    '''Finds the optimal order to apply components to synthesise a target apgcode
in as few gliders as possible.'''
    global values, visited
    values = {x:999999 for x in nodes}
    values[startpoint] = 0
    visited = []
    paths = {x:[] for x in nodes}
    paths[startpoint] = []


    while len(visited) < len(nodes):
        selectednode = getclosestunvisited(nodes, visited)
        paths = applydistances(selectednode, distances, paths)
    if target not in values:
        if len(nodes) > 1:
            giventargets = []
            nodes2 = copy.deepcopy(nodes)
            nodes2.remove(startpoint)
            for x in range(min(20, len(nodes2))):
                node = random.choice(nodes2)
                nodes2.remove(node)
                giventargets.append(node)
            return ['Error', giventargets]
        else:
            return ['Error']
    if values[target] < 999999:
        path = paths[target][::-1] + [startpoint]

    return path
        
