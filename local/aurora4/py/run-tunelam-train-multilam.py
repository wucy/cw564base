#! /usr/bin/env python


import os
import sys
import re



TSET=sys.argv[1]
MLP=sys.argv[2]
CONFIG=sys.argv[3]
NUM_BASIS=sys.argv[4]
LAMFILE=sys.argv[5]
NUM_RGC=sys.argv[6]
STA2CLS=sys.argv[7]

lst_fn = '../lib/flists.mbt/%s.lst' % (TSET)

lst = open(lst_fn, 'r')

tot = len(lst.readlines())


os.popen('rm -r LOGs/%s/%s' % (TSET, CONFIG))

os.popen('mkdir -p LOGs/%s/%s' % (TSET, CONFIG))


logs = "LOGs/%s/%s/tune_\$TASK_ID.LOG" % (TSET, CONFIG)

cmd = 'qsub -o %s -j y -l qp=low -l generation=80 -t 1-%d -tc 100 -S /bin/bash base/tools/run-array-job.sh %s /usr/bin/python base/local/py/tunelam_one_task_train.py %s %s %s %s %s %s %s SET' % (logs, tot, lst_fn, TSET, MLP, CONFIG, NUM_BASIS, LAMFILE, NUM_RGC, STA2CLS)

print cmd

os.system(cmd)

