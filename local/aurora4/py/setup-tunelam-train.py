#! /usr/bin/env python


import os
import re
import sys




TSET = sys.argv[1]

CONFIG = sys.argv[2]

NUM_BASIS = sys.argv[3]




base = "tunelam"

whereami = os.getcwd()
pfile_dir = whereami + '/../data/pfile/'
fea_pfile = pfile_dir + '/' + TSET + '.pfile'
lab_pfile = pfile_dir + '/' + TSET + '_lab_spkr.pfile'

tasks = open("../lib/flists.mbt/%s.lst" % (TSET), 'r').readlines()


init_lam = '%s.lam.init' % (TSET)


for task in tasks:
    task = task.strip()
    taskdir = '%s/%s/%s/%s/' % (base, TSET, task, CONFIG)
    os.popen('mkdir -p ' + taskdir)
    os.popen('ln -s %s %s/fea.pfile' % (fea_pfile, taskdir))
    os.popen('ln -s %s %s/lab.pfile' % (lab_pfile, taskdir))

