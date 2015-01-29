#! /usr/bin/env python


import os
import sys
import re

sys.path.insert(0, '/home/mifs/cw564/base/global/python/')
from cw564.pc import *

TSET='csrnab_dt_h1'
MLP='decodeMLP/MLP.mbt'
CONFIG='hyp_hybrid_aln_hybrid'
NUM_BASIS='2'
LAMFILE='lib/mbt/%s.lam.init' % (TSET)

lst_fn = 'lib/flists.test/%s.lst' % (TSET)

lst = open(lst_fn, 'r')

content = lst.readlines()


work_schedule = pc_schedule.pc_scheduler(30)

for line in content:
    line = line.strip()
    cmd = '/usr/bin/python base/local/py/tunelam_one_task_test.py %s %s %s %s %s %s' % (TSET, MLP, CONFIG    , NUM_BASIS, LAMFILE, line)
    print cmd
    work_schedule.add_job(cmd)


work_schedule.wait()

