#! /usr/bin/env python

import os
import sys
import re


LST = sys.argv[1]
NUM_BASIS = int(sys.argv[2])
OUT_LAM = sys.argv[3]


spkrs = open(LST, 'r').readlines()

out = open(OUT_LAM, 'w')

out.write('%d %d\n' % (len(spkrs), NUM_BASIS))

for spkr in spkrs:
    spkr = spkr.strip()
    out.write(spkr)
    lam = 1.0 / NUM_BASIS
    for i in range(NUM_BASIS):
        out.write(' %f' % (lam))
    out.write('\n')

out.close()

