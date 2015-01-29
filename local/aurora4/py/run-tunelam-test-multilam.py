#! /usr/bin/env python


import os
import sys
import re



TSET=sys.argv[1]
MLP='decodeMLP/MLP.mbt'
CONFIG=sys.argv[2]
NUM_BASIS=sys.argv[3]



NUM_RGC=sys.argv[4]
STA2CLS=sys.argv[5]

LAMFILE='lib/mbt/%s.lam.init.%s' % (TSET, NUM_RGC)

lst_fn = 'lib/flists.test/%s.lst' % (TSET)

lst = open(lst_fn, 'r')

tot = len(lst.readlines())


os.popen('rm -r LOGs/%s/%s' % (TSET, CONFIG))

os.popen('mkdir -p LOGs/%s/%s' % (TSET, CONFIG))


logs = "LOGs/%s/%s/tune_\$TASK_ID.LOG" % (TSET, CONFIG)




cmd = 'qsub -o %s -j y -l qp=low -l generation=70 -t 1-%d -tc 330 -S /bin/bash base/tools/run-array-job.sh %s /usr/bin/python base/local/py/tunelam_one_task_test-multilam.py %s %s %s %s %s %s %s SET' % (logs, tot, lst_fn, TSET, MLP, CONFIG, NUM_BASIS, LAMFILE, NUM_RGC, STA2CLS)

print cmd

os.system(cmd)

