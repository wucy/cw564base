#! /usr/bin/env python


import os
import sys
import re


TSET = sys.argv[1]
MLP = sys.argv[2]
CONFIG = sys.argv[3]
NUM_BASIS = sys.argv[4]
LAMFILE = sys.argv[5]
MYLST = sys.argv[6]



lst = open(MYLST, 'r').readlines()


for task in lst:
    task = task.strip()
    os.system('base/local/py/decode_mbt_one_task.py %s %s %s %s %s %s' % (TSET, MLP, CONFIG, NUM_BASIS, LAMFILE, task))

