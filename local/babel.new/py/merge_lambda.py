#! /usr/bin/env python


import os
import re
import sys

num_basis = int(sys.argv[1])

lam_list = os.popen('ls tunelam/*/*/lambda.est').readlines()





out = open('traincv.lam.esti', 'w')

out.write('%d %d\n' % (len(lam_list), num_basis))

for lam in lam_list:
    lam = lam.strip()
    raw_res = os.popen('cat ' + lam).readlines()
    spkr = re.split('/', lam)[2]
    out.write(spkr)
    for b in range(num_basis):
        out.write(' ' + str(float(raw_res[b].strip())))
    out.write('\n')



out.close()
