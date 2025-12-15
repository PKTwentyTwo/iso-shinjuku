#This is the SYNTHesis DATA MANager, which handles interactions with the database.
#It contains functions to assemble syntheses using Dijkstra's algorithm, as well as add components to the database.

import os, lifelib, sys, csv, math, re
import dijkstra

tabulations = {}
rule = 'b3s23' #Use standard Life as the default rule.
def makedirstructure(rule, tabulation=None):
    #Creates a new directory/file when necessary.
    #The structure of the database is <root>/rules/<rule>/<tabulation>.csv.
    root = os.getcwd()
    if not os.path.exists(root + '/rules'):
        os.mkdir(root + '/rules')
    if not os.path.exists(root + '/rules/' + rule):
        os.mkdir(root + '/rules/' + rule)
    if tabulation is not None:
        if not os.path.exists(root + '/rules/' + rule + '/' + tabulation + '.csv'):
            f = open(root + '/rules/' + rule + '/' + tabulation + '.csv', 'w')
            f.write('input,rle,cost,output\n')
            f.close()

def wipetabulations():
    #Wipes the copied tabulations.
    #Used when loading a new rule.
    global tabulations
    tabulations = {}
def loadtabulation(tabulation):
    #Loads a tabulation into a dictionary from the corresponding csv file.
    global tabulations
    makedirstructure(rule, tabulation)
    filename = os.getcwd() + '/rules/' + rule + '/' + tabulation + '.csv' 
    rows = []    
    #Use a csv reader to get the data from the file.
    #(pandas might be better, but ideally lifelib should be the only non standard-library module).
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:     
            rows.append(row)
    rows.pop(0)
    for x in rows:
        if '' in x:
            x.remove('')
    tabulations[tabulation] = rows
def getapgcode(pt):
    #Gets the apgcode of a pattern which might not be periodic.
    #Returns 'aperiodic' if the pattern is not determined to be periodic.
    period = pt.pdetect_or_advance()
    if type(period) == type({}):
        return pt.apgcode
    else:
        return 'aperiodic'

def makequery(fields, tabulation, conditions = []):
    #SQL-like query system for searching through the csv files.
    #The function puts spaghetti to shame; cleanup will be necessary.
    #Later, I should write a parser so that we can run actual SQL statements.
    listedfields = ['input', 'rle', 'cost', 'output']
    fielddict = {'input':0,'rle':1,'cost':2,'output':3}
    toreturn = []
    if tabulation not in tabulations:
        loadtabulation(tabulation)
    tabulationdata = tabulations[tabulation]

    if fields == '*':
        fields = listedfields.copy()
    if fields in listedfields:
        fields = [fields]
    conditions = ['OR'] + conditions
    for x in tabulationdata:
        satisfied = len(conditions) == 1
        for n in range((len(conditions))//4):
            boolean = conditions[4*n]
            field = conditions[4*n+1]
            comparison = conditions[4*n+2]
            value = conditions[4*n+3]
            
            conditionsatisfied = False
            if field in listedfields:
                intfield = fielddict[field]
            else:
                continue

            #The logic which runs comparisons.
            #It supports numerical comparisons, equal and not equal, and regular expressions.
            #(I don't know much about them yet, but I bet they will come in handy.)
            if comparison == '=' or comparison == '==':
                conditionsatisfied = (x[intfield] == value)
            elif comparison == '>':
                conditionsatisfied = (x[intfield] > value)
            elif comparison == '<':
                conditionsatisfied = (x[intfield] < value)
            elif comparison == '!=':
                conditionsatisfied = (x[intfield] != value)
            elif comparison == 'MATCH':
                conditionsatisfied = True and (re.match(value, x[intfield]))
            if boolean == 'OR':
                satisfied = satisfied or conditionsatisfied
            else:
                satisfied = satisfied and conditionsatisfied
        if satisfied:
            recordtoreturn = []
            for f in fields:
                if f in fielddict:
                    recordtoreturn.append(x[fielddict[f]])
            toreturn.append(recordtoreturn)
    return toreturn



def striprle(rle):
    #Strips an RLE from a lifelib pattern down to its bare minimum.
    for n in range(2):
        rle = rle[rle.find('\n') + 1:]
    rle = rle.replace('\n', '')
    return rle
def getgcount(pt):
    #Gets the number of gliders in a pattern.
    gliders = 0
    components = pt.components()
    for x in components:
        if x.wechsler in ['153', '163']:
            gliders = gliders + 1
    return gliders
def getgliderset(pt):
    #Gets just the gliders of a pattern.
    #Useful for determining validity, as well as rewinding.

    gliders = lt.pattern('b!')
    components = pt.components()
    for x in components:
        if x.wechsler in ['153', '163']:
            gliders = gliders + x
    return gliders
def grewind(pt, amount):
    #Rewinds gliders in a pattern by a given number of generations.
    components = pt.components()
    shift = math.ceil(amount/4)
    for x in components:
        if x.wechsler in ['153', '163']:
            pt = pt - x
            displacement = x.displacement
            x = x(displacement[0] * -1 * shift, displacement[1] * -1 * shift)
            if amount%4 != 0:
                x = x[4-(amount%4)]
            pt = pt + x
    return pt
def rewind(pt, amount):
    #Rewinds a pattern by a given number of generations.
    #It differs to grewind in that it rewinds oscillators as well as still lifes.
    #No support for spaceships yet. :(
    gliders = getgliderset(pt)
    rewound = grewind(gliders, amount)
    pt2 = pt - gliders
    apgcode = getapgcode(pt2)
    if apgcode == 'aperiodic' or apgcode[0:1] == 'xq':
        return None
    shift = (-amount)%pt2.period
    pt3 = pt2[shift]
    return pt3 + rewound
def isvalid(pt):
    #Determines if a synthesis is valid or not.
    gliders = getgliderset(pt)
    return rewind(gliders, 500)[500].digest() == gliders.digest()
def advance(pt):
    #Advances a synthesis until 3 generations before the number of gliders decreases.
    #A basic binary search is employed to do this.
    pt = rewind(pt, 4) #Rewind the pattern to ensure we can advance it.
    glidercount = getgcount(pt)
    if glidercount == 0:
        return pt
    gens = 1
    while getgcount(pt[gens]) == glidercount:
        gens = gens * 2
    gap = gens//4
    gens = gens - gap
    while gap > 1:
        evpt = pt[gens]
        gap = gap//2
        if getgcount(evpt) == glidercount:
            gens = gens + gap
        else:
            gens = gens - gap
    return pt[gens - 3]
def naivecheck(pt):
    #To save time when checking periodicity, check if gliders are present.
    comp = pt.components()
    wechslers = [x.wechsler for x in comp]
    if '153' in wechslers or '163' in wechslers:
        return False
    else:
        return True        
def addsynth(pt):
    #Adds a synthesis to the corresponding csv file.
    if not isvalid(pt):
        print(pt.rle_string())
        print('Synthesis is not valid.')
        return None
    starting_constellation = pt
    components = pt.components()
    for x in components:
        if x.wechsler in ['153', '163']:
            starting_constellation = starting_constellation - x
    glidercost = (pt.population - starting_constellation.population)//5
    
    starting_apgcode = getapgcode(starting_constellation)
    if starting_apgcode == 'aperiodic':
        print('Initial pattern is aperiodic.')
        return None
    final_constellation = pt[4000]
    if not naivecheck(final_constellation):
        print('Final pattern is aperiodic.')
        return None
    final_apgcode = getapgcode(final_constellation)
    if getapgcode(final_constellation) == 'aperiodic':
        print('Final pattern is aperiodic.')
        return None
    proper_format_pt = advance(pt)
    rle = striprle(proper_format_pt.rle_string())
    record = [starting_apgcode, rle, str(glidercost), final_apgcode]
    tabulation = final_apgcode[0:final_apgcode.find('_')]
    makedirstructure(rule, tabulation)
    oldsynth = makequery('*', tabulation, ['input', '=', starting_apgcode, 'AND', 'output', '=', final_apgcode])
    if oldsynth == []:
        #print('New synthesis added!')
        tabulations[tabulation].append(record)
        #pushsynths(tabulation)
    else:
        oldsynth = oldsynth[0]
        oldcost = int(oldsynth[2])
        newcost = int(record[2])
        if newcost < oldcost:
            #print('New synthesis is cheaper than current synthesis.')
            tabulations[tabulation].remove(oldsynth)
            tabulations[tabulation].append(record)
            #pushsynths(tabulation)
        else:
            #print('New synthesis is no cheaper than current synthesis.')
            pass
def pushsynths(tabulation):
    #Uploads the fresh data to a csv file.
    print('Uploading syntheses for '+tabulation+'...')
    text = 'input,rle,cost,output\n'
    tabdata = tabulations[tabulation]
    tabdata.sort()
    tablist = []
    for x in tabdata:
        for y in x:
            text = text + y + ','
        text = text + '\n'
    f = open(os.getcwd() + '/rules/' + rule + '/' + tabulation + '.csv', 'w')
    f.write(text)
    f.close()
def compilesynth(steps):
    #Puts together a synthesis based on RLEs representing each step.
    synth = lt.pattern('b!')
    count = -1
    for x in steps:
        count = count + 1
        pt = lt.pattern(x)
        #Make sure that the synthesis has the same orientation as the previous step's output:
        if count != 0:
            prevstep = lt.pattern(steps[count-1])
            prevstep = prevstep[4000]
            
            cstep = pt - getgliderset(pt)

            gens = 0

            while cstep[gens].octodigest() != prevstep.octodigest():

                gens = gens + 1
                if gens > 9999:
                    print('Exceeded limit of 9999 generations!') #I had to modify this print statement so it wouldn't be interpreted as a factorial.
                    break
            orientations = ['identity', 'rot270', 'rot180', 'rot90', 'flip_x', 'flip_y', 'swap_xy', 'swap_xy_flip']
            count2 = 0
            while cstep(orientations[count2]).digest() != prevstep.digest():
                count2 = count2 + 1
                if count >= 8:
                    break
            period = cstep.period
            shift = (period-gens)%period
            if shift != 0:
                pt = rewind(pt, shift)
            pt = pt(orientations[count2])
        
        if synth.population > 0:
            bbox = synth.bounding_box
        else:
            bbox = [0,0,0,0]
        synth = synth + pt(bbox[2]+bbox[0]+21, 0)
    return synth
def striptab(apgcode):
    #Gets the tabulation from an apgcode.
    return apgcode[0:apgcode.find('_')]
def assemblesynth(apgcode):
    #Uses Dijkstra's algorithm to assemble a synthesis based on components.
    tabulations = {}
    apgcodes = [apgcode]
    paths = {}
    for x in apgcodes:
        if x not in apgcodes:
            apgcodes.append(x)
        if True:
            tab = striptab(x)
            paths[x] = {}
            if tab not in tabulations:
                loadtabulation(tab)
            syntheses = makequery('*', tab, ['output', '=', x])
            for s in syntheses:
                inputcode = s[0]
                if inputcode not in apgcodes:
                    apgcodes.append(inputcode)
                
                    
                paths[x][inputcode] = int(s[2])
    
    result = dijkstra.Dijkstra(apgcodes, paths, apgcode)
    if result[0] == 'Error':
        print('Error: Unable to assemble synthesis for '+apgcode)
        if len(result) == 2:
            toprint = 'Try and manually find a synthesis for one of the following:\n'
            for n in result[1]:
                toprint = toprint + n + '\n'
            print(toprint)
        return 'Error!'
    stages = []
    for x in range(len(result) - 1):
        startcode = result[x]
        endcode = result[x+1]
        synthesis = makequery(['rle'], striptab(endcode), ['input', '=', startcode, 'AND', 'output', '=', endcode])
        stages.append(synthesis[0][0])
    synth = compilesynth(stages)
    print(synth.rle_string())
        
def processfile(file):
    f = open(file, 'r')
    rles = f.read().split('\n')
    f.close()
    line = 0
    lines = len(rles)
    for rle in rles:
        try:
            line = line + 1
            if line%100 == 0:
                print(str(line)+'/'+str(lines)+' syntheses processed.')
            if len(rle) == 0:
                continue
            if rle[-1] != '!':
                continue
            if rle[0] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'o', 'b', '$', '!']:
                continue
        except KeyboardInterrupt:
            print('Received KeyboardInterrupt, terminating...')
            break
        addsynth(lt.pattern(rle))
    for tabulation in tabulations:
        pushsynths(tabulation)

