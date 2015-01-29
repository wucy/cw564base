#! /usr/bin/env python

import sys
import os
import re

sys.path.insert(0, '/home/mifs/cw564/base/global/python/')
from cw564.io import *

if len(sys.argv) != 3:
    print 'Usage:', __file__, 'IN_SCP OUT_LAMBDA'
    exit(-1)

in_scp = sys.argv[1]
out_lam = sys.argv[2]

lam_dict = dict()
#lam_dict['male'] = [1, 0]
#lam_dict['female'] = [0, 1]

scp_file = open(in_scp, 'r')

for line in scp_file:
    id = line[0:12]
    gender = line.split('_')[1][0]
    if gender == 'M':
        lam_dict[id] = [0.9, 0.1]
    else:
        lam_dict[id] = [0.1, 0.9]


mbt.write_lambda(out_lam, lam_dict, 2)

