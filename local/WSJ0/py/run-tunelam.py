#! /usr/bin/env python


import os
import sys
import re



TSET='csrnab_dt_h1'
MLP='decodeMLP/MLP.mbt'
CONFIG='hyp_hybrid_aln_hybrid'
NUM_BASIS='2'
LAMFILE='lib/mbt/%s.lam.init' % (TSET)

lst_fn = 'lib/flists.test/%s.lst' % (TSET)

lst = open(lst_fn, 'r')

tot = len(lst.readlines())


os.popen('rm -r LOGs/%s/%s' % (TSET, CONFIG))

os.popen('mkdir -p LOGs/%s/%s' % (TSET, CONFIG))


logs = "LOGs/%s/%s/tune_\$TASK_ID.LOG" % (TSET, CONFIG)

cmd = 'qsub -o %s -j y -l qp=low -l generation=80 -t 1-%d -tc 300 -S /bin/bash base/tools/run-array-job.sh %s /usr/bin/python base/local/py/tunelam_one_task.py %s %s %s %s %s SET' % (logs, tot, lst_fn, TSET, MLP, CONFIG, NUM_BASIS, LAMFILE)

print cmd

os.popen(cmd)

