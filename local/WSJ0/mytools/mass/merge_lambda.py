#! /usr/bin/env python


import os
import re

num_basis = 2

lam_list = os.popen('ls workdir/*/lambda.est').readlines()





out = open('lib/mbt/traincv.lam.esti', 'w')

out.write('%d %d\n' % (len(lam_list), num_basis))

for lam in lam_list:
    lam = lam.strip()
    raw_res = os.popen('cat ' + lam).readlines()
    spkr = re.split('/', lam)[1]
    out.write(spkr)
    for b in range(num_basis):
        out.write(' ' + raw_res[b].strip())
    out.write('\n')



out.close()
