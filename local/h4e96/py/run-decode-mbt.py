#! /usr/bin/env python


import os
import sys
import re



TSET='dev03'
MLP='decodeMLP/MLP.mbt'
CONFIG='mbt.hyp_hyb_aln_hyb'
NUM_BASIS='2'
LAMFILE='lib/mbt/%s.lam.esti' % (TSET)

lst_fn = 'lib/flists.test/%s.lst' % (TSET)

lst = open(lst_fn, 'r')

tot = len(lst.readlines())

os.popen('rm -r LOGs/decode.mbt')

os.popen('mkdir -p LOGs/decode.mbt/%s/%s' % (TSET, CONFIG))


logs = "LOGs/decode.mbt/%s/%s/decode_\$TASK_ID.LOG" % (TSET, CONFIG)

cmd = 'qsub -o %s -j y -l qp=low -l generation=80 -t 1-%d -tc 500 -S /bin/bash base/tools/run-array-job.sh %s /usr/bin/python base/local/py/decode_mbt_one_task.py %s %s %s %s %s SET' % (logs, tot, lst_fn, TSET, MLP, CONFIG, NUM_BASIS, LAMFILE)

print cmd

os.system(cmd)

