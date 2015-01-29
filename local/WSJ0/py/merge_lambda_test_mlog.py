#! /usr/bin/env python


import os
import re

num_basis = 2


config = 'hyp_oracle_aln_hybrid'

lam_list = os.popen('ls tunelam/*/*/%s/MLOG' % (config)).readlines()





out = open('test.lam.esti', 'w')

out.write('%d %d\n' % (len(lam_list), num_basis))

for lam in lam_list:
    lam = lam.strip()
    raw_res = os.popen('cat ' + lam).readlines()
    now = len(raw_res) - 1
    while 'lambda' not in raw_res[now]:
        now -= 1
    now += 1
    splits = re.split('\s+', raw_res[now])
    spkr = re.split('/', lam)[2]
    out.write(spkr)
    for b in range(1, num_basis + 1):
        out.write(' ' + splits[b])
    out.write('\n')



out.close()
