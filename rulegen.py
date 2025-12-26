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
        '0':[],
        '1':['c', 'e'],
        '2':['a','c','e','i','k','n'],
        '3':['a','c','e','i','j','k','n','q','r','y'],
        '4':['a','c','e','i','j','k','n','q','r','t','w','y','z'],
        '5':['a','c','e','i','j','k','n','q','r','y'],
        '6':['a','c','e','i','k','n'],
        '7':['c', 'e'],
        '8':[]
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
