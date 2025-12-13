#This is the CLI for the project.
#It includes a set of commands that enable easy compilation and management of rules and syntheses.
#Standard library modules:
import os, platform, math, time
#Project modules:

#Try and import lifelib. If it fails, prompt the user to install it.
try:
    import lifelib
    lifelib_installed = True
    import synthdataman as synthdata
except ImportError:
    print('Lifelib is not installed. Try installing it with \'autoinstall\'.')
    lifelib_installed = False
rule = ''
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
    rule = args[0]
    rule = rule.lower().replace('/', '')
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
    
loadrule(['b3s23'])
synthdata.processfile('syntheses.txt')
