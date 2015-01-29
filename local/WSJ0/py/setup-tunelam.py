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
pfile_dir = whereami + '/align/' + CONFIG + '/data/pfile/'
fea_pfile = pfile_dir + '/' + TSET + '.pfile'
lab_pfile = pfile_dir + '/' + TSET + '_lab.pfile'

tasks = open("lib/flists.test/csrnab_dt_h1.lst", 'r').readlines()


os.popen('mkdir -p lib/mbt/')

init_lam = 'lib/mbt/%s.lam.init' % (TSET)

os.popen('echo "%d %d" > %s' % (len(tasks), NUM_BASIS, init_lam))

for task in tasks:
    task = task.strip()
    os.popen('echo "%s 0.5 0.5" >> %s' % (task, init_lam))
    taskdir = '%s/%s/%s/%s/' % (base, TSET, task, CONFIG)
    os.popen('mkdir -p ' + taskdir)
    os.popen('ln -s %s %s/fea.pfile' % (fea_pfile, taskdir))
    os.popen('ln -s %s %s/lab.pfile' % (lab_pfile, taskdir))

