#This is a script to find syntheses based on Catagolue glider stdin symmetries.
#The first such stdin was b3s23/5Glider_stdin, and there have been many others.
import lifelib, sys, os, re, sys, urllib.request
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
objects = urllib.request.urlopen('https://catagolue.hatsya.com/textcensus/'+rule+'/'+symmetry).read().decode('utf-8')
objects = objects.split('\n')
apgcodes = []
for x in objects:
    if x.count(',') > 0 and x != 'apgcode,occurences':
        apgcodes.append(x[0:x.find(',')].replace('\"', ''))
for x in apgcodes:
    try:
        soups = lt.download_samples(x, rule)[symmetry]
    except KeyError:
        continue
    if len(soups) > 0:
        print(soups[0].rle_string())
