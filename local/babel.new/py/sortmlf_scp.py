#! /usr/bin/env python



import sys
import os
import re

sys.path.insert(0, '/home/mifs/cw564/base/global/python/')
from cw564.io import *


INMLF = sys.argv[1]
INSCP = sys.argv[2]
OUTMLF = sys.argv[3]


src_mlf = htk.read_mlf(INMLF)


raw_order_lst = os.popen("cat %s | awk -F '.' '{print $1;}'" % (INSCP)).readlines()

order_lst = list()
for line in raw_order_lst:
    order_lst.append(line.strip())


htk.write_mlf(OUTMLF, src_mlf, order_lst)
