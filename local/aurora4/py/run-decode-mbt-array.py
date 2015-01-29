#! /usr/bin/env python


import os
import sys
import re



TSET=sys.argv[1]
MLP='decodeMLP/MLP.mbt'
CONFIG='mbt.' + sys.argv[2]
NUM_BASIS=sys.argv[3]
NUM_TASKS = sys.argv[4]

LAMFILE='lib/mbt/%s.lam.esti.%s' % (TSET, CONFIG.split('.')[1])

lst_fn = 'lib/mbt/%s/%s/LST' % (TSET, NUM_TASKS)

lst = open(lst_fn, 'r')

tot = len(lst.readlines())

os.popen('rm -r LOGs/decode.mbt/%s/%s' % (TSET, CONFIG))

os.popen('mkdir -p LOGs/decode.mbt/%s/%s' % (TSET, CONFIG))


logs = "LOGs/decode.mbt/%s/%s/decode_\$TASK_ID.LOG" % (TSET, CONFIG)

cmd = 'qsub -o %s -j y -l qp=low -t 1-%d -tc 100 -S /bin/bash base/tools/run-array-job.sh %s /usr/bin/python base/local/py/decode_mbt_one_task_array.py %s %s %s %s %s SET' % (logs, tot, lst_fn, TSET, MLP, CONFIG, NUM_BASIS, LAMFILE)

print cmd

os.system(cmd)

