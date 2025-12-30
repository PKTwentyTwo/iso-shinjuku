'''This module contains functions for pattern separation.'''
def getdistance(comp1, comp2):
    '''Calculates the distance between two components.'''
    bbox_1 = comp1.bounding_box
    bbox_2 = comp2.bounding_box
    dx = min(abs(bbox_1[0] - bbox_2[0]), abs(bbox_1[0] + bbox_1[2] - bbox_2[0]), abs(bbox_1[0] - bbox_2[0] - bbox_2[2]), abs(bbox_1[0] + bbox_1[2] - bbox_2[0] - bbox_2[2]))
    dy = min(abs(bbox_1[1] - bbox_2[1]), abs(bbox_1[1] + bbox_1[3] - bbox_2[1]), abs(bbox_1[1] - bbox_2[1] - bbox_2[3]), abs(bbox_1[1] + bbox_1[3] - bbox_2[1] - bbox_2[3]))
    distance = max(dx, dy) #Take the max of the horizontal and vertical difference.
    return distance
def groupsep(pt):
    '''Separates a pattern into groups where each group has patterns no more than 30 cells apart.'''
    #Time complexity is O(n^2), but that's the same as Dijkstra, so it's fine.
    components = pt.components()
    groups = {}
    idlist = []
    compid = -1
    for x in components:
        compid += 1
        idlist.append(compid)
        groups[compid] = [compid]
        for y in components:
            if x.bounding_box != y.bounding_box:
                dist = getdistance(x, y)
                if dist <= 30:
                    groups[compid].append(components.index(y))
    print(groups)
    #Merge the lists of close patterns into groups:
    for x in groups:
        grouplist = groups[x]
        for y in grouplist:
            for z in groups[y]:
                if z not in grouplist:
                    grouplist.append(z)
    ptgroups = []
    while len(idlist) > 0:
        #Partition the pattern into groups based on the dictionary:
        chosenid = idlist[0]
        ids = groups[chosenid]
        pt = components[0] - components[0]
        for x in ids:
            pt = pt + components[x]
            idlist.remove(x)
        ptgroups.append(pt)
    return ptgroups
