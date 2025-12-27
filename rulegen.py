import re, copy
def isvalid(rule):
    #Checks if a rule is valid using regex.
    rule = rule.lower().replace('/', '')
    if re.match('b[1-8ceaiknjqrytwz-]*s[0-8ceaiknjqrytwz-]*', rule):
        return True
    else:
        return False
print(isvalid('B3/S23'))
def parserule(rule):
    #Takes a rule and returns a list of birth and survival conditions.
    #I hate having to code parsers.
    #(Still better than the next function, which will be 250+ lines)
    if not isvalid(rule):
        raise ValueError('Rule does not match regex b[1-8ceaiknjqrytwz-]*s[0-8ceaiknjqrytwz-]*')
    
    rule = rule.lower().replace('/', '')
    #Dictionary mapping digits to their Hensel notation letters.
    conditiondict = {
        '0':[''],
        '1':['c', 'e'],
        '2':['a','c','e','i','k','n'],
        '3':['a','c','e','i','j','k','n','q','r','y'],
        '4':['a','c','e','i','j','k','n','q','r','t','w','y','z'],
        '5':['a','c','e','i','j','k','n','q','r','y'],
        '6':['a','c','e','i','k','n'],
        '7':['c', 'e'],
        '8':['']
        }
    conditions = []
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    position = -1
    cstring = ''
    birth = True
    rule = rule + '|' #Using a vertical bar to signify the end of the rulestring.
    for x in range(len(rule)):
        position = x
        character = rule[x]
        
        if character in digits or character in ['b', 's', '|']:
            cstring = cstring.replace('b', '').replace('s', '')
            if cstring != '':
                digit = cstring[0]
                if len(cstring) == 1:
                    for x in conditiondict[cstring]:
                        if birth:
                            conditions.append('B' + cstring + x)
                        else:
                            conditions.append('S' + cstring + x)
                else:
                    subconditions = cstring[1:]
                    if subconditions[0] == '-':
                        temp = copy.deepcopy(conditiondict[digit])
                        for x in cstring[2:]:
                            if x in temp:
                                temp.remove(x)
                        for x in temp:
                            if birth:
                                conditions.append('B' + digit + x)
                            else:
                                conditions.append('S' + digit + x)                        
                    else:
                        temp = []
                        for x in subconditions:
                            if x in conditiondict[digit]:
                                temp.append(x)
                        for x in temp:
                            if birth:
                                conditions.append('B' + digit + x)
                            else:
                                conditions.append('S' + digit + x)
            cstring = ''
                        
        if character == 's':
            birth = False
        cstring = cstring + character
    return conditions

#Ok, here we go.
def makeseparator(rule, pseudo=False):
    #AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    #This was pain. This is pain.
    rule = rule.lower().replace('/', '')
    conditions = parserule(rule)
    ruletable = '@RULE '+rule+'_separate\n'
    ruletable += '\n' + 'The separation algorithm ruletable for '+rule+'.\n'
    ruletable += '@TABLE\n'
    ruletable += 'n_states:3\n'
    ruletable += 'neighborhood:Moore\n'
    ruletable += 'symmetries:rotate4reflect\n'
    ruletable += '''var a = {0,2}
var b = {0,2}
var c = {0,2}
var d = {0,2}
var e = {0,2}
var f = {0,2}
var g = {0,2}
var h = {0,2}
var i = {0,2}

var A = {0,1,2}
var B = {0,1,2}
var C = {0,1,2}
var D = {0,1,2}
var E = {0,1,2}
var F = {0,1,2}
var G = {0,1,2}
var H = {0,1,2}
'''
    #Setting up the conditions.
    #We only need to run this once per rule, so having literally hundreds of if statements won't cause slowdown.
    #Writing it can, however, still cause damage to mental health and sanity.
    if 'B1e' in conditions:
        ruletable += 'a,1,b,c,d,e,f,g,h,1\n'
    if 'B1c' in conditions:
        ruletable += 'a,b,1,c,d,e,f,g,h,1\n'

    if 'B2a' in conditions:
        ruletable += 'a,1,1,b,c,d,e,f,g,1\n'
    if 'B2c' in conditions:
        ruletable += 'a,b,1,c,1,d,e,f,g,1\n'
    if 'B2e' in conditions:
        ruletable += 'a,1,b,1,c,d,e,f,g,1\n'
    if 'B2i' in conditions:
        ruletable += 'a,1,b,c,d,1,e,f,g,1\n'
    if 'B2k' in conditions:
        ruletable += 'a,1,b,c,1,d,e,f,g,1\n'
    if 'B2n' in conditions:
        ruletable += 'a,b,1,c,d,e,f,1,g,1\n'

    if 'B3a' in conditions:
        ruletable += 'a,1,1,1,b,c,d,e,f,1\n'
    if 'B3c' in conditions:
        ruletable += 'a,b,1,c,1,d,1,e,f,1\n'
    if 'B3e' in conditions:
        ruletable += 'a,1,b,1,c,1,d,e,f,1\n'
    if 'B3i' in conditions:
        ruletable += 'a,b,1,1,1,c,d,e,f,1\n'
    if 'B3j' in conditions:
        ruletable += 'a,1,b,1,1,c,d,e,f,1\n'
    if 'B3k' in conditions:
        ruletable += 'a,1,b,1,c,d,1,e,f,1\n'
    if 'B3n' in conditions:
        ruletable += 'a,1,1,b,1,c,d,e,f,1\n'
    if 'B3q' in conditions:
        ruletable += 'a,1,1,b,c,d,1,e,f,1\n'
    if 'B3r' in conditions:
        ruletable += 'a,1,1,b,c,1,d,e,f,1\n'
    if 'B3y' in conditions:
        ruletable += 'a,1,b,c,1,d,1,e,f,1\n'

    if 'B4a' in conditions:
        ruletable += 'a,1,1,1,1,b,c,d,e,1\n'
    if 'B4c' in conditions:
        ruletable += 'a,b,1,c,1,d,1,e,1,1\n'
    if 'B4e' in conditions:
        ruletable += 'a,1,b,1,c,1,d,1,e,1\n'
    if 'B4i' in conditions:
        ruletable += 'a,1,1,b,1,1,c,d,e,1\n'
    if 'B4j' in conditions:
        ruletable += 'a,1,1,b,c,1,d,1,e,1\n'
    if 'B4k' in conditions:
        ruletable += 'a,1,1,b,1,c,d,1,e,1\n'
    if 'B4n' in conditions:
        ruletable += 'a,b,1,c,1,1,1,d,e,1\n'
    if 'B4q' in conditions:
        ruletable += 'a,1,1,1,b,c,1,d,e,1\n'
    if 'B4r' in conditions:
        ruletable += 'a,1,1,1,b,1,c,d,e,1\n'
    if 'B4t' in conditions:
        ruletable += 'a,1,b,c,1,1,1,d,e,1\n'
    if 'B4w' in conditions:
        ruletable += 'a,1,1,b,c,d,1,1,e,1\n'
    if 'B4y' in conditions:
        ruletable += 'a,1,1,b,1,c,1,d,e,1\n'
    if 'B4z' in conditions:
        ruletable += 'a,1,1,b,c,1,1,d,e,1\n'

    if 'B5a' in conditions:
        ruletable += 'a,b,1,1,1,1,1,c,d,1\n'
    if 'B5c' in conditions:
        ruletable += 'a,1,b,1,c,1,1,1,d,1\n'
    if 'B5e' in conditions:
        ruletable += 'a,b,1,1,1,c,1,d,1,1\n'
    if 'B5i' in conditions:
        ruletable += 'a,1,1,1,1,1,b,c,d,1\n'
    if 'B5j' in conditions:
        ruletable += 'a,1,1,1,1,b,1,c,d,1\n'
    if 'B5k' in conditions:
        ruletable += 'a,b,1,1,c,1,1,d,1,1\n'
    if 'B5n' in conditions:
        ruletable += 'a,1,b,1,1,1,1,c,d,1\n'
    if 'B5q' in conditions:
        ruletable += 'a,1,1,1,b,1,1,c,d,1\n'
    if 'B5r' in conditions:
        ruletable += 'a,b,c,1,1,d,1,1,1,1\n'
    if 'B5y' in conditions:
        ruletable += 'a,1,b,1,1,c,1,1,d,1\n'

    if 'B6a' in conditions:
        ruletable += 'a,1,1,1,1,1,1,b,c,1\n'
    if 'B6c' in conditions:
        ruletable += 'a,1,b,1,1,1,1,1,c,1\n'
    if 'B6e' in conditions:
        ruletable += 'a,b,1,c,1,1,1,1,1,1\n'
    if 'B6i' in conditions:
        ruletable += 'a,b,1,1,1,c,1,1,1,1\n'
    if 'B6k' in conditions:
        ruletable += 'a,b,1,1,c,1,1,1,1,1\n'
    if 'B6n' in conditions:
        ruletable += 'a,1,1,1,b,1,1,1,c,1\n'

    if 'B7c' in conditions:
        ruletable += 'a,1,b,1,1,1,1,1,1,1\n'
    if 'B7e' in conditions:
        ruletable += 'a,b,1,1,1,1,1,1,1,1\n'

    if 'B8' in conditions:
        ruletable += 'a,1,1,1,1,1,1,1,1,1\n'
    #These are the conditions for detecting induction coils.
    #They have to be added after the birth conditions so that the birth conditions take priority.
    if 'B3i' in conditions:
        ruletable += 'a,b,1,1,1,c,1,d,e,2\n' #B4n
        ruletable += 'a,b,1,1,1,c,1,1,1,2\n' #B6i
        ruletable += 'a,b,1,1,1,c,1,d,1,2\n' #B5e
        ruletable += 'a,b,1,1,1,c,d,1,e,2\n' #B4t
        ruletable += 'a,b,1,1,1,c,d,1,1,2\n' #B5r
    if 'B3a' in conditions:
        ruletable += 'a,1,1,1,b,c,1,d,e,2\n' #B4q
    if 'B3c' in conditions:
        ruletable += 'a,b,1,c,1,d,1,e,1,2\n' #B4c
    if 'B3n' in conditions:
        ruletable += 'a,b,1,c,d,1,1,e,1,2\n' #B4y
    if 'B3q' in conditions:
        ruletable += 'a,b,1,c,d,1,1,e,1,2\n' #B4y
    if 'B3j' in conditions:
        




    
    #Survival conditions:
    if 'S0' not in conditions:
        ruletable += '1,a,b,c,d,e,f,g,h,2\n'
    
    if 'S1e' not in conditions:
        ruletable += '1,1,b,c,d,e,f,g,h,2\n'
    if 'S1c' not in conditions:
        ruletable += '1,b,1,c,d,e,f,g,h,2\n'

    if 'S2a' not in conditions:
        ruletable += '1,1,1,b,c,d,e,f,g,2\n'
    if 'S2c' not in conditions:
        ruletable += '1,b,1,c,1,d,e,f,g,2\n'
    if 'S2e' not in conditions:
        ruletable += '1,1,b,1,c,d,e,f,g,2\n'
    if 'S2i' not in conditions:
        ruletable += '1,1,b,c,d,1,e,f,g,2\n'
    if 'S2k' not in conditions:
        ruletable += '1,1,b,c,1,d,e,f,g,2\n'
    if 'S2n' not in conditions:
        ruletable += '1,b,1,c,d,e,f,1,g,2\n'

    if 'S3a' not in conditions:
        ruletable += '1,1,1,1,b,c,d,e,f,2\n'
    if 'S3c' not in conditions:
        ruletable += '1,b,1,c,1,d,1,e,f,2\n'
    if 'S3e' not in conditions:
        ruletable += '1,1,b,1,c,1,d,e,f,2\n'
    if 'S3i' not in conditions:
        ruletable += '1,b,1,1,1,c,d,e,f,2\n'
    if 'S3j' not in conditions:
        ruletable += '1,1,b,1,1,c,d,e,f,2\n'
    if 'S3k' not in conditions:
        ruletable += '1,1,b,1,c,d,1,e,f,2\n'
    if 'S3n' not in conditions:
        ruletable += '1,1,1,b,1,c,d,e,f,2\n'
    if 'S3q' not in conditions:
        ruletable += '1,1,1,b,c,d,1,e,f,2\n'
    if 'S3r' not in conditions:
        ruletable += '1,1,1,b,c,1,d,e,f,2\n'
    if 'S3y' not in conditions:
        ruletable += '1,1,b,c,1,d,1,e,f,2\n'

    if 'S4a' not in conditions:
        ruletable += '1,1,1,1,1,b,c,d,e,2\n'
    if 'S4c' not in conditions:
        ruletable += '1,b,1,c,1,d,1,e,1,2\n'
    if 'S4e' not in conditions:
        ruletable += '1,1,b,1,c,1,d,1,e,2\n'
    if 'S4i' not in conditions:
        ruletable += '1,1,1,b,1,1,c,d,e,2\n'
    if 'S4j' not in conditions:
        ruletable += '1,1,1,b,c,1,d,1,e,2\n'
    if 'S4k' not in conditions:
        ruletable += '1,1,1,b,1,c,d,1,e,2\n'
    if 'S4n' not in conditions:
        ruletable += '1,b,1,c,1,1,1,d,e,2\n'
    if 'S4q' not in conditions:
        ruletable += '1,1,1,1,b,c,1,d,e,2\n'
    if 'S4r' not in conditions:
        ruletable += '1,1,1,1,b,1,c,d,e,2\n'
    if 'S4t' not in conditions:
        ruletable += '1,1,b,c,1,1,1,d,e,2\n'
    if 'S4w' not in conditions:
        ruletable += '1,1,1,b,c,d,1,1,e,2\n'
    if 'S4y' not in conditions:
        ruletable += '1,1,1,b,1,c,1,d,e,2\n'
    if 'S4z' not in conditions:
        ruletable += '1,1,1,b,c,1,1,d,e,2\n'

    if 'S5a' not in conditions:
        ruletable += '1,b,1,1,1,1,1,c,d,2\n'
    if 'S5c' not in conditions:
        ruletable += '1,1,b,1,c,1,1,1,d,2\n'
    if 'S5e' not in conditions:
        ruletable += '1,b,1,1,1,c,1,d,1,2\n'
    if 'S5i' not in conditions:
        ruletable += '1,1,1,1,1,1,b,c,d,2\n'
    if 'S5j' not in conditions:
        ruletable += '1,1,1,1,1,b,1,c,d,2\n'
    if 'S5k' not in conditions:
        ruletable += '1,b,1,1,c,1,1,d,1,2\n'
    if 'S5n' not in conditions:
        ruletable += '1,1,b,1,1,1,1,c,d,2\n'
    if 'S5q' not in conditions:
        ruletable += '1,1,1,1,b,1,1,c,d,2\n'
    if 'S5r' not in conditions:
        ruletable += '1,b,c,1,1,d,1,1,1,2\n'
    if 'S5y' not in conditions:
        ruletable += '1,1,b,1,1,c,1,1,d,2\n'

    if 'S6a' not in conditions:
        ruletable += '1,1,1,1,1,1,1,b,c,2\n'
    if 'S6c' not in conditions:
        ruletable += '1,1,b,1,1,1,1,1,c,2\n'
    if 'S6e' not in conditions:
        ruletable += '1,b,1,c,1,1,1,1,1,2\n'
    if 'S6i' not in conditions:
        ruletable += '1,b,1,1,1,c,1,1,1,2\n'
    if 'S6k' not in conditions:
        ruletable += '1,b,1,1,c,1,1,1,1,2\n'
    if 'S6n' not in conditions:
        ruletable += '1,1,1,1,b,1,1,1,c,2\n'

    if 'S7c' not in conditions:
        ruletable += '1,1,b,1,1,1,1,1,1,2\n'
    if 'S7e' not in conditions:
        ruletable += '1,b,1,1,1,1,1,1,1,2\n'

    if 'S8' not in conditions:
        ruletable += '1,1,1,1,1,1,1,1,1,2\n'   
    return ruletable
print(makeseparator('B3/S23-a5'))
