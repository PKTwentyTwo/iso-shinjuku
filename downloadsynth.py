import lifelib
rule = 'b3s238'
sym = 'Cleanest_Pseudo_5Glider_stdin'
sess = lifelib.load_rules(rule)
lt = sess.lifetree(n_layers = 1, memory = 1000)
import requests, csv, math, os
def rewind(synthesis, amount):
    #A function to rewind the gliders in a synthesis by a given amount. 
    components = synthesis.components()
    newsynth = synthesis
    for x in components:
        if type(x.pdetect_or_advance) != type({}):
            if x.displacement != (0, 0):
                shift = math.ceil(amount/4)
                displacement = x.displacement
                newsynth = newsynth - x
                newglider = x(displacement[0] * -shift, displacement[1] * -shift)[(4-amount)%4]
                newsynth = newsynth + newglider
    return newsynth
def isvalid(synth):
    return rewind(synth, 20)[20] == synth

def getapgcodes(symmetry):
    c = requests.get('https://catagolue.hatsya.com/textcensus/'+rule+'/'+symmetry)
    f = open('censusdata.csv', 'w')
    f.write(c.text)
    f.close()
    with open('censusdata.csv', mode ='r')as file:
      csvFile = csv.reader(file)
      for lines in csvFile:
          if lines[0][0:2] == 'xs':
              apgcodes.append(lines[0])
    os.remove('censusdata.csv')

probable = {}
definite = {}
predictedcosts = {}
def process(apgcode, symmetry):
    pt = lt.pattern(apgcode)
    try:
        soups = pt.download_samples()[symmetry]
        baseobjpop = pt.population
        mincost = 999
        bestsoup = None
        cleanupneeded = True
        for x in soups:
            if isvalid(x):
                evolvedsoup = x[200]
                if evolvedsoup == evolvedsoup[1]:
                    wechslers = [x.wechsler for x in evolvedsoup.components()]
                    if '153' in wechslers or '163' in wechslers:
                        pass
                    else:
                        finalpop = evolvedsoup.population
                        cleanuppop = finalpop - baseobjpop
                        cleanupcost = math.ceil(cleanuppop / (4.45*1.5)) #The average object is 4.45 cells, so I use this to estimate cleanup cost, assuming a glider takes out 1.5 objects on average.
                        estimatedcost = x.population // 5 + cleanupcost
                        if estimatedcost < mincost:
                            mincost = estimatedcost
                            bestsoup = x
                            if cleanupcost == 0:
                                cleanupneeded = False
        if mincost < 999:
            predictedcosts[apgcode] = mincost
            if cleanupneeded:
                probable[apgcode] = bestsoup
            else:
                definite[apgcode] = bestsoup
    except:
        pass
def getcost(apgcode):   
    return 9999999
def striprle(rle):
    for n in range(2):
        rle = rle[rle.find('\n')+1:]
    rle = rle.replace('\n', '')
    return rle
apgcodes = []
getapgcodes(sym)
print(len(apgcodes))
for x in apgcodes:
    print('Now processing: '+x)
    process(x, sym)
definitesynth = lt.pattern('b!')
count = 0
if not os.path.exists(os.getcwd() + '/' + rule):
    os.mkdir(os.getcwd() + '/' + rule)
fullstring = ''
for x in definite:
    apgcode = x
    fullstring = fullstring + striprle(definite[x].rle_string()) + '\n'
##    category = apgcode[0:apgcode.find('_')]
##    if not os.path.exists(os.getcwd() + '/' + rule + '/' + category):
##        os.mkdir(os.getcwd() + '/' + rule + '/'+ category)
    synthtext = '#C '+apgcode+' costs '+str(definite[x].population//5)+' gliders\n'+definite[x].rle_string()
##    f = open(os.getcwd() + '/' + rule + '/' + category + '/' + apgcode + '.txt', 'w')
##    f.write(synthtext)
##    f.close()
##    
##    if predictedcosts[x] < getcost(x):
##        definitesynth = definitesynth + definite[x]((count%10)*100, (count//10)*100)
##        count = count + 1
f = open('syntheses.txt', 'w')
f.write(fullstring)
f.close()
