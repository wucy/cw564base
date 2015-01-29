#! /usr/bin/env python

import os
import re
import sys


in_left = sys.argv[1]
in_lam = sys.argv[2]
out_lam = sys.argv[3]

left_lst = open(in_left, 'r').readlines()[1:]

for line in left_lst:
    line = line.strip()
    os.system('cat %s | grep %s >> %s' % (in_lam, line, out_lam))
