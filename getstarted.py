#!/usr/bin/python3
import lifelib, os, random, sys, hashlib, time
if len(sys.argv) > 1:
    rule = sys.argv[1]
else:
    rule = input('Please enter a rule.\n>')
sess = lifelib.load_rules(rule)
lt = sess.lifetree(n_layers = 1, memory = 1000)

seed = hashlib.sha1(str(time.time()).encode('utf-8')).hexdigest()
def rewind(synth):
    components = synth.components()
    for x in components:
        if x.wechsler in ['153', '163']:
            displacement = x.displacement
            synth = synth - x
            x2 = x(-displacement[0], -displacement[1])
            synth = synth + x2
    return synth
def isvalid(synth):
    return rewind(synth)[4] == synth
gliders = [lt.pattern('bob$bbo$ooo!'), lt.pattern('bob$obb$ooo!'), lt.pattern('ooo$bbo$bob!'), lt.pattern('ooo$obb$bob!')]
gliders2 = []
for x in gliders:
    for y in range(4):
        gliders2.append(x[y])
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
def striprle(rle):
    for n in range(2):
        rle = rle[rle.find('\n')+1:]
    rle = rle.replace('\n', '')
    return rle
apgcodes = set()
fullstring = ''
pt1 = lt.pattern('xp2_7')
print(pt1[2] == pt1)
def processsynth(pt):
    global apgcodes
    global fullstring
    if isvalid(pt):
        evpt = pt[300]
        if evpt[2].digest() == evpt.digest():
            if evpt.apgcode not in apgcodes:
                print(evpt.apgcode)
                fullstring = fullstring + striprle(pt.rle_string()) + '\n'
                apgcodes.add(evpt.apgcode)
f = open('syntheses.txt', 'w')
f.write('')
f.close()
for g in range(2, 6):
    print('Searching '+str(g)+'G collisions...')
    time.sleep(3)
    fullstring = ''
    for x in range(1, 3001):
        if x%1000 == 0:
            print(str(x)+' out of 10000...')
        processsynth(makesynth(seed + str(x), g))
    f = open('syntheses.txt', 'a')
    f.write(fullstring)
    f.close()
print('Search 1 complete!')
time.sleep(5)
def getcanon(pattern):
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
apgcodes2 = set()
def collide1G(apgcode):
    global apgcodes2, fullstring

    ipt = lt.pattern(apgcode)
    orientations = getcanon(ipt)
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
            evcol = collision[200]
            if evcol == evcol[2]:
                apgcode2 = evcol.apgcode
                if apgcode2 not in apgcodes2:
                    fullstring = fullstring + striprle(collision.rle_string()) + '\n'
                    apgcodes2.add(apgcode2)  
                

fullstring = ''
glider = lt.pattern('bob$2bo$3o!')
for x in apgcodes:
    print(x)
    collide1G(x)
f = open('syntheses.txt', 'a')
f.write(fullstring)
f.close()       
print('Search complete.')
print('Results saved to syntheses.txt.')
print('Use syncmd.py to commit them to the database.')

