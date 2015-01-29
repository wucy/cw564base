#! /usr/bin/env python

import os
import sys
import re


SCP = sys.argv[1]
REFMLF = sys.argv[2]
HYPMLF = sys.argv[3]
OUTMLF = sys.argv[4]


sys.path.insert(0, '/home/mifs/cw564/base/global/python/')

from cw564.io import *

refmlfs = htk.read_mlf(REFMLF)
hypmlfs = htk.read_mlf(HYPMLF)


scps = open(SCP, 'r').readlines()


newmlfs = dict()
orders = list()

for line in scps:
    raw_key = line.split('.')[0]
    search_key = '*/' + raw_key
    orders.append(raw_key)
    if search_key in refmlfs:
        newmlfs[raw_key] = refmlfs[search_key]
    else:
        print raw_key
        newmlfs[raw_key] = hypmlfs[search_key]


htk.write_mlf(OUTMLF, newmlfs, orders)



