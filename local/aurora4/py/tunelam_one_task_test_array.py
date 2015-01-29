#! /usr/bin/env python


import os
import sys
import re
import random



TSET = sys.argv[1]
MLP = sys.argv[2]
CONFIG = sys.argv[3]
NUM_BASIS = sys.argv[4]
LAMFILE = sys.argv[5]
MYLST = sys.argv[6]



lst = open(MYLST, 'r').readlines()


for task in lst:
    task = task.strip()
    my_lam = "tunelam/%s/%s/%s/lambda.est" % (TSET, task, CONFIG)
    while not os.path.exists(my_lam):
        os.system('base/local/py/tunelam_one_task_test.py %s %s %s %s %s %s' % (TSET, MLP, CONFIG, NUM_BASIS, LAMFILE, task))


