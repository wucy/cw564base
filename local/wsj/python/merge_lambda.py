# /usr/bin/env python


import os
import re

num_basis = 2

spkr_list = os.popen('ls temp/').readlines()


out = open('out/lambda.final', 'w')

out.write('%d %d\n' % (len(spkr_list), num_basis))

for spkr in spkr_list:
    spkr = spkr.strip()
    raw_res = os.popen('cat temp/%s/lambda.est' % (spkr)).readline().strip()
    res = re.split('\s+', raw_res)
    out.write(spkr)
    for b in range(num_basis):
        out.write(' ' + res[b])
    out.write('\n')



out.close()
