#! /usr/bin/env python

import sys
import os
import re

sys.path.insert(0, '/home/mifs/cw564/base/global/python/')
from cw564.io import *

if (len(sys.argv) != 3):
    print 'Usage:', __file__, 'IN_SCP OUT_SEGMAP'
    exit(-1)

in_scp = open(sys.argv[1], 'r')
out_sm_fn = sys.argv[2]

seg_map = dict()

cnt = 0
for line in in_scp:
    token = line[7:12]
    seg_map[str(cnt)] = token
    cnt += 1

mbt.write_segmap(out_sm_fn, seg_map)

