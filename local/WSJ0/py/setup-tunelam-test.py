#! /usr/bin/env python


import os
import re
import sys



MLP = "decodeMLP/MLP.mbt"

TSET = "csrnab_dt_h1"

CONFIG = "hyp_hybrid_aln_hybrid"

NUM_BASIS = 2




base = "tunelam"

whereami = os.getcwd()
pfile_dir = whereami + '/align/%s/data/pfile/' % (CONFIG)
fea_pfile = pfile_dir + '/' + TSET + '.pfile'
lab_pfile = pfile_dir + '/' + TSET + '_lab_spkr.pfile'

tasks = open("lib/flists.test/%s.lst" % (TSET), 'r').readlines()


init_lam = 'lib/mbt/%s.lam.init' % (TSET)


for task in tasks:
    task = task.strip()
    taskdir = '%s/%s/%s/%s/' % (base, TSET, task, CONFIG)
    os.popen('mkdir -p ' + taskdir)
    os.popen('ln -s %s %s/fea.pfile' % (fea_pfile, taskdir))
    os.popen('ln -s %s %s/lab.pfile' % (lab_pfile, taskdir))

