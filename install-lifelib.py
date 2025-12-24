try:
    import lifelib
    sess = lifelib.load_rules('b3s23')
    lt = sess.lifetree(n_layers = 1, memory = 1000)
    print('Lifelib is installed correctly.')
except ImportError:
    print('Lifelib is not installed correctly.')
    print('Cloning repo...')
    import os
    os.system('git clone https://gitlab.com/apgoucher/lifelib')
