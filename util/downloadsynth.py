#This is a script to find syntheses based on Catagolue glider stdin symmetries.
#The first such stdin was b3s23/5Glider_stdin, and there have been many others.
import lifelib, sys, os, re, sys, urllib.request, math
import cleanup
if len(sys.argv) > 1:
    rule = sys.argv[1]
else:
    rule = input('Please enter a rule.\n>')
if len(sys.argv) > 2:
    symmetry = sys.argv[2]
else:
    symmetry = input('Please enter a symmetry to take syntheses from.\n>')
sess = lifelib.load_rules(rule)
lt = sess.lifetree(n_layers = 1, memory = 1000)
cleanup.lt = lt
#Download the textcensus from Catagolue, so we know which objects we need:

objects = urllib.request.urlopen('https://catagolue.hatsya.com/textcensus/'+rule+'/'+symmetry).read().decode('utf-8')
objects = objects.split('\n')
apgcodes = []
for x in objects:
    if x.count(',') > 0 and x != 'apgcode,occurences':
        apgcodes.append(x[0:x.find(',')].replace('\"', ''))

#Create a dictionary to store apgcodes and their 'soups'.
soupdict = {}
#I prefer to download all of the soups at the start, rather than when they are needed.
for x in apgcodes:
    try:
        print('Downloading soups for '+x+'...')
        soups = lt.download_samples(x, rule)[symmetry]
    except KeyError:
        continue
    if len(soups) > 0:
        soupdict[x] = soups
#I've borrowed the functions from synthdataman.py for this:
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
def getapgcode(pt):
    #Gets the apgcode of a pattern which might not be periodic.
    #Returns 'aperiodic' if the pattern is not determined to be periodic.
    period = pt.pdetect_or_advance()
    if type(period) == type({}):
        return pt.apgcode
    else:
        return 'aperiodic'
def isvalid(pt):
    #Determines if a synthesis is valid or not.
    gliders = getgliderset(pt)
    return rewind(gliders, 4)[4].digest() == gliders.digest()
def striprle(rle):
    #Strips an RLE from a lifelib pattern down to its bare minimum.
    for n in range(2):
        rle = rle[rle.find('\n') + 1:]
    rle = rle.replace('\n', '')
    return rle
def process(apgcode):
    #Go through the soups and make syntheses for the apgcode.
    stages = []
    soups = soupdict[apgcode]
    for x in soups:
        if isvalid(x):
            print(striprle(x.rle_string()))
        else:
            pass
        stages.append(striprle(x.rle_string()))
        for c in cleanup.cleanup(x, apgcode):
            stages.append(striprle(c.rle_string()))
    return stages
      
for x in soupdict:
    print(process(x))
