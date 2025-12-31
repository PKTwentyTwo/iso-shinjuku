#!/usr/bin/python3
#This is the CLI for the project.
#It includes a set of commands that enable easy compilation and management of rules and syntheses.
#Standard library modules:
import os, time, sys, tarfile, random
#Project modules:
import synthdataman as synthdata
#Try and import lifelib. If it fails, prompt the user to install it.
try:
    import lifelib
    lifelib_installed = True
except ImportError:
    print('Lifelib is not installed. Look in /doc for documentation on how to install it, or run setup.sh.')
    lifelib_installed = False
    print('Quitting in 60 seconds...')
    time.sleep(60)
    quit()
rule = ''
running = True
def verifyargs(args, lengths):
    '''Checks that the right number of arguments have been supplied for a command.'''
    if len(args) not in lengths:
        return False
    else:
        return True
def loadrule(args):
    '''Loads a rule, meaning it is used for all operations until a new one is loaded.'''
    #This is key as a lifetree can only support a single rule.
    global rule
    if not verifyargs(args, [1]):
        print('Usage: load <rule>')
        return ''
    newrule = args[0]
    newrule = newrule
    newrule = newrule.lower().replace('/', '')
    if newrule != rule:
        synthdata.wipetabulations()
    rule = newrule
    try:
        sess = lifelib.load_rules(rule)
    except ValueError:
        print('Invalid rule!')
        print('Resetting rule to b3s23')
        loadrule(['b3s23'])
        return ''
    lt = sess.lifetree(n_layers = 1, memory = 1000)
    synthdata.lt = lt
    synthdata.rule = rule
    print('Successfully loaded rule '+rule+'.')
def makesynthesis(args):
    '''Assembles a synthesis for a given apgcode.'''
    if not verifyargs(args, [1]):
        print('Usage: synth <apgcode>')
        return ''
    if rule == '':
        print('You must specify a rule! Use \'load <rule>\' to choose a rule!')
        return ''
    synthdata.assemblesynth(args[0])
def parsecommand(command):
    '''Parses a command.'''
    #Elements are separated by spaces, unless inside quotes.
    #Comments are achieved with hashtags.
    commandlength = len(command)
    parsed = []
    currentarg = ''
    inquotes = False
    for x in range(commandlength):
        if command[x] == '#':
            if currentarg != '':
                parsed.append(currentarg)
            currentarg = ''
            break
        if command[x] == '\"' or command[x] == '\'':
            inquotes = not inquotes
        elif command[x] == ' ' and not inquotes:
            parsed.append(currentarg)
            currentarg = ''
        else:
            currentarg = currentarg + command[x]
    if currentarg != '':
        parsed.append(currentarg)
    return parsed
def exitshell(args):
    '''Exits the current session.'''
    global running
    print('Terminating...')
    running = False
def procfile(args):
    '''Processes a file, committing any new components to the database.'''
    if not verifyargs(args, [1]):
        print('Usage: process <file>')
        return ''
    if rule == '':
        print('You must specify a rule! Use \'load <rule>\' to choose a rule!')
        return ''
    file = args[0]
    if os.path.isfile(os.getcwd() + '/' + file):
        synthdata.processfile(os.getcwd() + '/' + file)
    elif os.path.isfile(file):
        synthdata.processfile(file)
    else:
        print('Error: Unable to locate file '+file)
        return ''
    print('Succesfully processed file.')
def compress(args):
    '''Compresses all csv files in a rule's folder.'''
    #Useful when committing using Git.
    #It uses the tar.gz format, since Python has good support for both tar and gzip.
    if not verifyargs(args, [0]):
        print('Usage: compress')
        return ''
    if rule == '':
        print('You must specify a rule! Use \'load <rule>\' to choose a rule!')
        return ''
    if not os.path.exists(os.getcwd() + '/rules/' + rule):
        print('No data has yet been saved for rule '+rule+'.')
        return ''
    filesize1 = 0
    with tarfile.open(os.getcwd() + '/rules/' + rule + '/' + rule + '.tar.gz', 'w:gz') as tf:
        files = os.listdir(os.getcwd() + '/rules/' + rule)
        for f in files:
            if f.endswith('.csv'):
                filesize1 += os.path.getsize(os.getcwd() + '/rules/' + rule + '/' + f)
                tf.add(os.getcwd() + '/rules/' + rule + '/' + f, arcname = f)
    filesize2 = os.path.getsize(os.getcwd() + '/rules/' + rule + '/' + rule + '.tar.gz')
    filesize1 = round(filesize1/1000)
    filesize2 = round(filesize2/1000)
    print('Compression completed successfully.')
    print('Compression rate: '+str(filesize1)+' KB -> '+str(filesize2)+' KB') #Most files will range in the kilobytes, although xp2.csv can reach megabytes.   
def decompress(args):
    '''Decompresses a saved .tar.gz archive, if one can be located for the loaded rule.'''
    if not verifyargs(args, [0]):
        print('Usage: decompress')
        return ''
    if rule == '':
        print('You must specify a rule! Use \'load <rule>\' to choose a rule!')
        return ''
    if not os.path.exists(os.getcwd() + '/rules/' + rule + '/' + rule + '.tar.gz'):
        print('Could not find compressed file for rule '+rule)
        return ''
    tar = tarfile.open(os.getcwd() + '/rules/' + rule + '/' + rule + '.tar.gz', "r:gz")
    tar.extractall('./rules/' + rule)
    tar.close()
    print('Decompression successful.')
def clean(args):
    '''Wipes a rule or tabulation.'''
    #To prevent accidental wiping, the user has to enter one of five control sentences.
    if not verifyargs(args, [0, 1]):
        print('Usage: decompress')
        return ''
    if rule == '':
        print('You must specify a rule! Use \'load <rule>\' to choose a rule!')
        return ''
    if not os.path.exists(os.getcwd() + '/rules/' + rule):
        print('There is no data on '+rule+' to wipe!')
        return ''
    #The user has to enter a pangram to prevent accidental wiping.
    control_sentences = ['The quick brown fox jumps over the lazy dog', 'Jackdaws love my big sphinx of quartz', 'We promptly judged antique ivory buckles for the next prize', 'Waltz bad nymph for quick jigs vex', 'Pack my box with five dozen liquor jugs']
    sentence = random.choice(control_sentences)
    print('To prevent accidental wiping, please enter the below sentence:')
    print(sentence)
    response = input()
    if response.lower().replace(' ', '').replace('.', '') != sentence.lower().replace(' ', '').replace('.', ''):
        print('Sentences do not match.')
        return ''
    ruledir = os.getcwd() + '/rules/' + rule
    if len(args) == 0:
        files = os.listdir(ruledir)
        for f in files:
            if not f.endswith('.tar.gz'):
                os.remove(ruledir + '/' + f)
        print('Successfully cleaned all data files.')
        if len(os.listdir(ruledir)) != 0:
            print('The tar.gz archive has been ignored.')
    else:
        if os.path.exists(ruledir + '/' + args[0] + '.csv'):
            os.remove(ruledir + '/' + args[0] + '.csv')
            print('Successfully removed '+args[0] + '.csv')
        else:
            print('Unable to locate '+args[0] + '.csv')                
def printlicense(args):
    '''Prints the project's license.'''
    if os.path.exists(os.getcwd() + '/LICENSE'):
        f = open('LICENSE', 'r')
        print(f.read())
        f.close()
    else:
        print('Could not find license file, defaulting to MIT:')
        print('''MIT License

Copyright (c) 2025 PK22

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.''')
def providehelp(args):
    '''Checks /doc/cmd for details about commands.'''
    if not verifyargs(args, [0,1]):
        print('Usage: \'help <command>\' or \'help\'')
        return ''
    docfolder = os.getcwd() + '/doc/cmd/'
    if not os.path.exists(docfolder):
        print('Error: could not find documentation folder!')
        return ''
    if len(args) == 0:   
        print('Avaliable commands:') 
        helpstring = ''
        files = os.listdir(docfolder)
        files.sort()
        for x in files:
            f = open(docfolder + x, 'r')
            lines = f.read().split('\n')
            f.close()
            if len(lines) > 1:
                helpstring = helpstring + x + ' ' * (16 - len(x)) + lines[1] + '\n'
        print(helpstring)
    else:
        command = args[0]
        if os.path.exists(docfolder + command):
            f = open(docfolder + command, 'r')
            print(f.read())
            f.close()
        else:
            print('Could not find command '+command+'. Type \'help\' for a list of commands.')
def executecommand(arguments):
    '''Executes a command given the parsed arguments.'''
    if len(arguments) > 0:
        command = arguments[0]
    else:
        return ''
    if len(arguments) > 1:
        args = arguments[1:]
    else:
        args = []
    command = command.lower()
    match command:
        case 'load':
            loadrule(args)
            return ''
        case 'synth':
            makesynthesis(args)
            return ''
        case 'help':
            providehelp(args)
            return ''
        case 'quit':
            exitshell(args)
            return ''
        case 'exit':
            exitshell(args)
            return ''
        case 'license':
            printlicense(args)
            return ''
        case 'process':
            procfile(args)
            return ''
        case 'compress':
            compress(args)
            return ''
        case 'decompress':
            decompress(args)
            return ''
        case 'clean':
            clean(args)
            return ''
    print('Command \''+command+'\' not found.\nType \'help\' for a list of commands.')
    return ''
if len(sys.argv) > 1:
    #This is to let other scripts execute specific commands.
    executecommand(sys.argv[1:])
else:
    #Start the main loop:
    print('This is the CLI for iso-shinjuku.')
    print('Type \'help\' or \'license\' for more information.')
    while running:
        command = input('>')
        parsedcommand = parsecommand(command)
        executecommand(parsedcommand)
