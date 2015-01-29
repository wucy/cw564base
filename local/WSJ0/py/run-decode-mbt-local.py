#! /usr/bin/env python


import os
import sys
import re

sys.path.insert(0, '/home/mifs/cw564/base/global/python/')
from cw564.pc import *


work_schedule = pc_schedule.pc_scheduler(30)


TSET='csrnab_dt_h1'
MLP='decodeMLP/MLP.mbt'
CONFIG='mbt.hyp_ref_aln_slct'
NUM_BASIS='2'
LAMFILE='lib/mbt/%s.lam.esti.hyp_ref_aln_slct' % (TSET)

lst_fn = 'lib/flists.test/%s.lst' % (TSET)

lst = open(lst_fn, 'r')



for line in lst:
    line = line.strip()
    cmd = 'base/local/py/decode_mbt_one_task.py %s %s %s %s %s %s' % (TSET, MLP, CONFIG, NUM_BASIS, LAMFILE, line)
    work_schedule.add_job(cmd)


work_schedule.wait()

