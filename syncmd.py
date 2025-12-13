#This is the CLI for the project.
#It includes a set of commands that enable easy compilation and management of rules and syntheses.
#Standard library modules:
import os, platform, math, time, sys
#Project modules:
import synthdataman as synthdata
#Try and import lifelib. If it fails, prompt the user to install it.
try:
    import lifelib
    lifelib_installed = True
except ImportError:
    print('Lifelib is not installed. Try installing it with \'autoinstall\'.')
    lifelib_installed = False
rule = ''
running = True
def verifyargs(args, lengths):
    if len(args) not in lengths:
        return False
    else:
        return True

def loadrule(args):
    global rule
    if not verifyargs(args, [1]):
        print('Usage: load <rule>')
        return ''
    newrule = args[0]
    newrule = newrule
    newrule = rule.lower().replace('/', '')
    if newrule != rule:
        synthdata.wipetabulations()
    rule = newrule
    sess = lifelib.load_rules(rule)
    lt = sess.lifetree(n_layers = 1, memory = 1000)
    synthdata.lt = lt
    synthdata.rule = rule
    print('Successfully loaded rule '+rule+'.')
def makesynthesis(args):
    if not verifyargs(args, [1]):
        print('Usage: synth <apgcode>')
        return ''
    if rule == '':
        print('You must specify a rule! Use \'load <rule\' to choose a rule!')
        return ''
    synthdata.assemblesynth(args[0])
def autoinstall(args):
    global lifelib_installed
    if not verifyargs(args, [0]):
        print('Usage: autoinstall')
        return ''
    if not lifelib_installed:
        print('Required module lifelib is not installed.')
        options = []
        operatingsystem = platform.uname()[0]
        options.append(str(len(options)+1)+'). Install with pip')
        if operatingsystem == 'Linux' or operatingsystem.lower().count('cygwin') > 0:
            options.append(str(len(options)+1)+'). Clone repo with git')
        options.append(str(len(options)+1)+'). Install with command of your choice.')
        for x in options:
            print(x)
        choice = input('Choose an option from the above.\n>')
        if choice == '1':
            os.system('pip install python-lifelib')
        elif choice == '2':
            if operatingsystem == 'Linux' or operatingsystem.lower().count('cygwin') > 0:
                os.system('git clone https://gitlab.com/apgoucher/lifelib')
            else:
                command = input('Enter the command you wish to install lifelib with.\nBear in mind the name on PyPi is python-lifelib, not lifelib.\n>')
                os.system(command)
        else:
            command = input('Enter the command you wish to install lifelib with.\nBear in mind the name on PyPi is python-lifelib, not lifelib.\n>')
            os.system(command)
        try:
            import lifelib
            lifelib_installed = True
        except ImportError:
            lifelib_installed = False
        if lifelib_installed:
            print('Success!')
            if operatingsystem == 'Windows':
                print('You must install Cygwin to use lifelib on Windows.')
                choice = input('Do you want to install? (y/n)\n>')
                if choice.lower() == 'y':
                    lifelib.install_cygwin()
                else:
                    print('Quitting program...')
                    time.sleep(10)
                    quit()
        else:
            print('Failed to install lifelib.')
        print('Please restart the program.')
        print('Quitting...')
        time.sleep(10)
        quit()
def parsecommand(command):
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
    global running
    print('Terminating...')
    running = False
def printlicense(args):
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
        command = args[1]
        if os.path.exists(docfolder + command):
            f = open(docfolder + command, 'r')
            print(f.read())
            f.close()
        else:
            print('Could not find command '+command+'. Type \'help\' for a list of commands.')
def executecommand(arguments):
    if len(arguments) > 0:
        command = arguments[0]
    else:
        return ''
    if len(arguments) > 1:
        args = arguments[1:]
    else:
        args = []
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
    print('Command \''+command+'\' not found.\nType \'help\' for a list of commands.')
    return ''

print('This is the CLI for iso-shinjuku.')
print('Type \'help\' or \'license\' for more information.')
while running:
    command = input('>')
    parsedcommand = parsecommand(command)
    executecommand(parsedcommand)
