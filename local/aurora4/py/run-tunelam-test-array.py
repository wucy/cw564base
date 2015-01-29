#! /usr/bin/env python


import os
import sys
import re



TSET=sys.argv[1]
MLP=sys.argv[2]
CONFIG=sys.argv[3]
NUM_BASIS=sys.argv[4]
LAMFILE=sys.argv[5]
NUM_TASKS = sys.argv[6]



lst_fn = 'lib/mbt/%s/%s/LST' % (TSET, NUM_TASKS)

lst = open(lst_fn, 'r')

tot = len(lst.readlines())


os.popen('rm -r LOGs/%s/%s' % (TSET, CONFIG))

os.popen('mkdir -p LOGs/%s/%s' % (TSET, CONFIG))


logs = "LOGs/%s/%s/tune_\$TASK_ID.LOG" % (TSET, CONFIG)

cmd = 'qsub -o %s -j y -l qp=low -t 1-%d -S /bin/bash base/tools/run-array-job.sh %s /usr/bin/python base/local/py/tunelam_one_task_test_array.py %s %s %s %s %s SET' % (logs, tot, lst_fn, TSET, MLP, CONFIG, NUM_BASIS, LAMFILE)

print cmd

os.system(cmd)

