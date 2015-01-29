#! /usr/bin/env python

import sys
import os
import re

sys.path.insert(0, '/home/mifs/cw564/base/global/python/')
from cw564.io import *

if len(sys.argv) != 2:
    print 'Usage:', __file__, 'OUT_LAMBDA'
    exit(-1)

out_lam = sys.argv[1]

lam_dict = dict()
lam_dict['male'] = [1, 0]
lam_dict['female'] = [0, 1]

mbt.write_lambda(out_lam, lam_dict, 2)

