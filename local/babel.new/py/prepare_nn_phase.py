#! /usr/bin/env python


import os
import re
import sys




LAM_PHASE = sys.argv[1]

NN_PHASE = sys.argv[2]

TSET = 'traincv'



os.system('mkdir ' + NN_PHASE)
os.chdir(NN_PHASE)

os.system('ln -s ../base')
os.system('ln -s ../data')
os.system('ln -s ../htefiles')
os.system('ln -s ../lib')

os.system('cp base/local/ntools/qnmultitrn.mbt ./')
os.system('ln -s ../%s/%s.lam.esti %s.lam' % (LAM_PHASE, TSET, TSET))
os.system('ln -s ../%s/MLP INIT' % (LAM_PHASE))

