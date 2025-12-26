#This is a program to generate data for synthesising constellations.
#It saves the results in csv format, as apgcode,octodigest,rle.
#It only saves period 1 and 2 constellations.

import lifelib, hashlib, random, math, time, os, sys
def load(rule):
    global gliders2
    sess = lifelib.load_rules(rule)
    lt = sess.lifetree(n_layers = 1, memory = 1000)
    gliders = [lt.pattern('bob$bbo$ooo!'), lt.pattern('bob$obb$ooo!'), lt.pattern('ooo$bbo$bob!'), lt.pattern('ooo$obb$bob!')]
    gliders2 = []
    for x in gliders:
        for y in range(4):
            gliders2.append(x[y])

#Generate a seed based on the current time:
seed = hashlib.sha1(str(time.time()).encode('utf-8')).hexdigest()

#This is the dictionary that stores the data to save.
#It maps an apgcode to a list of tuples in the form (octodigest, rle).\
datadict = {}
#The below set stores octodigests, so the same synthesis is not saved multiple times.
#This reduces file size and processing time in both the training and testing phases.
octodigests = set()

#List of gliders, which is filled when the lifetree is loaded:
gliders2 = []
#Function to create a synthesis:
def makesynth(instring, gliders):
    hashed = hashlib.sha1(instring.encode('utf-8')).digest()
    hashvals = [hashed[x] for x in range(20)]
    pt = lt.pattern('b!')
    for x in range(gliders):
        position = (hashed[(2*x)]//16, hashed[2*x]%16)
        quadrant = (hashed[2*x+1]//16)%4
        phase = (hashed[2*x+1])%4
        glider = gliders2[4*quadrant + phase]
        glider = glider(8-position[0], 8-position[1])
        match quadrant:
            case 0:
                glider = glider(-16, -16)
            case 1:
                glider = glider(16, -16)
            case 2:
                glider = glider(-16, 16)
            case 3:
                glider = glider(16, 16)
        pt += glider
    return pt
def rewind4(synth):
    components = synth.components()
    for x in components:
        if x.wechsler in ['153', '163']:
            displacement = x.displacement
            synth = synth - x
            x2 = x(-displacement[0], -displacement[1])
            synth = synth + x2
    return synth
def isvalid(synth):
    return rewind4(synth)[4] == synth
def striprle(rle):
    for n in range(2):
        rle = rle[rle.find('\n')+1:]
    rle = rle.replace('\n', '')
    return rle
def advance(pt):
    #Advances a synthesis until 3 generations before the number of gliders decreases.
    #A basic binary search is employed to do this.
    pt = rewind4(pt) #Rewind the pattern to ensure we can advance it.
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
def getgcount(pt):
    #Gets the number of gliders in a pattern.
    gliders = 0
    components = pt.components()
    for x in components:
        if x.wechsler in ['153', '163']:
            gliders = gliders + 1
    return gliders
def search(seed, gliders, collisions):
    for c in range(collisions):
        try:
            if (c+1)%1000 == 0:
                print(str(c+1)+'/'+str(collisions)+' collisions searched.')
            pt = makesynth(seed+str(c), gliders)
            if not isvalid(pt):
                continue
            evpt = pt[300]
            if evpt[2] == evpt and evpt.nonempty():
                advpt = advance(pt)
                octodigest = advpt.octodigest()
                if octodigest not in octodigests:
                    octodigests.add(octodigest)
                    apgcode = evpt.apgcode
                    rle = striprle(pt.rle_string())
                    if apgcode not in datadict:
                        datadict[apgcode] = []
                    datadict[apgcode].append([octodigest, rle])
        except KeyboardInterrupt:
            print('Terminating...')
            break
    saveresults('const.csv')
def saveresults(file):
    #Saves the results of a search to a csv file.
    data = ''
    for x in datadict:
        for y in datadict[x]:
            data = data + x + ',' + str(y[0]) + ',' + y[1] + '\n'
    f = open(file, 'w')
    f.write(data)
    f.close()
