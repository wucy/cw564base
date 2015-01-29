#! /usr/bin/env python

import os
import sys
import re


SCP = sys.argv[1]
MLF = sys.argv[2]
OUT_MLF = sys.argv[3]

sys.path.insert(0, '/home/mifs/cw564/base/global/python/')

from cw564.io import *

mlfs = htk.read_mlf(MLF)

scps = open(SCP, 'r').readlines()

new_mlfs = dict()


orders = list()
for line in scps:
    raw_key = line.split('.')[0]
    splits = raw_key.split('-')
    splits[1] = 'XXXXX'
    mlf_key = '-'.join(splits)
    new_mlfs[raw_key] = mlfs[mlf_key]
    orders.append(raw_key)


htk.write_mlf(OUT_MLF, new_mlfs, orders)


