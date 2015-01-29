#! /usr/bin/env python


import os
import re
import sys


num_basis = int(sys.argv[1])
config = sys.argv[2]
tset = sys.argv[3]



lam_list = os.popen('ls tunelam/%s/*/%s/lambda.est' % (tset, config)).readlines()





out = open('%s.lam.esti.%s' % (tset, config), 'w')

out.write('%d %d\n' % (len(lam_list), num_basis))

for lam in lam_list:
    lam = lam.strip()
    raw_res = os.popen('cat ' + lam).readlines()
    spkr = re.split('/', lam)[2]
    out.write(spkr)
    for b in range(num_basis):
        out.write(' ' + raw_res[b].strip())
    out.write('\n')



out.close()
