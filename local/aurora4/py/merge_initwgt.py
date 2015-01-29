#! /usr/bin/env python


import os
import sys
import re
import random
import math

sys.path.insert(0, '/home/mifs/cw564/base/global/python')
from cw564.io import *


def parse_wgt(wgt_fn):
    ff = open(wgt_fn, 'r')
    
    ret = list()

    for line in ff:
        line = line.strip()
        if '<CATWEIGHTS>' in line:
            splits = re.split('\s+', line)
            for id in range(1, len(splits)):
                ret.append(float(splits[id]))
            break
    ff.close()

    return ret


IN_LST = sys.argv[1]
WGT_DIR = sys.argv[2]

OUT_LAM = sys.argv[3]

NUM_BASIS = sys.argv[4]

inlst = open(IN_LST, 'r').readlines()

outlam = open(OUT_LAM, 'w')


prefix = 'traincv_'

for line in inlst:
    spkr = line.strip()
    wgt_fn = WGT_DIR + '/' + spkr + '.wgt'
    wgt = parse_wgt(wgt_fn)
    for dim in wgt:
        outlam.write(str(dim) + " ")
    outlam.write('\n')


outlam.close()

