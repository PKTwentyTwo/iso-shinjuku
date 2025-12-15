#This stores the functions used by other utility software to automatically find destructions.
#cleanup() destroys a pattern with slow gliders (as far as it can), then returns a list of the stages.
import lifelib, sys, random
#sess = lifelib.load_rules(rule)
#lt = sess.lifetree(n_layers = 1, memory = 1000)
#glider = lt.pattern('bob$bbo$ooo!')
def getcanon(pattern):
    #Returns all unique orientations of a pattern.
    digests = []
    orientations = []
    period = pattern.period
    for x in range(period):
        for y in range(2):
            for z in range(4):
                pattern = pattern('rccw')
                if pattern.digest() not in digests:
                    digests.append(pattern.digest())
                    orientations.append(lt.pattern(pattern.rle_string()))
            pattern = pattern('flip_x')
        pattern = pattern[1]
    return orientations
def getpreserve(pattern, apgcode):
    #Given some ash, isolate the pattern we must protect.
    apg = lt.pattern(apgcode)
    orientations = getcanon(apg)#
    pt2 = pattern
    
    for x in orientations:
        pt2 = pt2.replace(x.rle_string(), 'b!')
    topreserve = pattern - pt2
    return topreserve
def clean1G(pattern, apgcode):
    glider = lt.pattern('bob$bbo$ooo!')
    #Collide a single glider with a pattern, and find the lowest population ash that still contains the target still life.
    minpop = pattern.population
    mincol = None
    orientations = getcanon(pattern)
    topreserve = getpreserve(pattern, apgcode).rle_string()
    period = pattern.period
    for pt in orientations:
        if pt.nonempty():
            bbox = pt.bounding_box
        else:
            break
        x = bbox[0]
        y = bbox[1]
        dx = bbox[2]
        dy = bbox[3]
        for a in range(8 + dx + dy):
            collision = pt
            collision = collision + glider(x - 13 - dy + a, y - 10)
            evcol = collision[300]
            
            if evcol.replace(topreserve, 'b!') != evcol:
                if getapgcode(evcol) != 'aperiodic':
                    if evcol.population < minpop:
                        minpop = evcol.population
                        mincol = collision
    return mincol
def getapgcode(pt):
    #Gets the apgcode of a pattern which might not be periodic.
    #Returns 'aperiodic' if the pattern is not determined to be periodic.
    period = pt.pdetect_or_advance()
    if type(period) == type({}):
        return pt.apgcode
    else:
        return 'aperiodic'
def cleanup(pt, apgcode):
    #Iterate the slow-glider destruction algorithm until it stops leading to reductions in population.
    #Then, return a list of each intermediate pattern so they can be committed to the database.
    stages = []
    pt2 = pt
    if getapgcode(pt2[300]) == 'aperiodic':
        return []
    print(type(None))
    while type(pt2) != type(None):
        evpt = pt2[300]
        print('Best minpop: '+str(evpt.population))
        pt2 = clean1G(evpt, apgcode)
        stages.append(pt2)
    stages.pop(-1)
    return stages
