import os
print('Step 1: Verifying lifelib is installed...')
try:
    import lifelib
    sess = lifelib.load_rules('b3s23')
    lt = sess.lifetree(n_layers = 1, memory = 1000)
    print('Lifelib is installed correctly.')
except ImportError:
    print('Lifelib is not installed correctly.')
    print('Cloning repo...')
    os.system('git clone https://gitlab.com/apgoucher/lifelib')

print('Step 2: Creating directory structure...')
dirs = ['doc', 'rules', 'util', 'tables']
for x in dirs:
    if not os.path.exists(os.getcwd() + '/' + x):
        os.mkdir(os.getcwd() + '/' + x)
print('Setup complete.')
