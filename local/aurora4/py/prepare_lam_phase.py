#! /usr/bin/env python


import os
import re
import sys




MLP = 'finalMLP/work/LogMLP'

NN_PHASE = sys.argv[1]
LAM_PHASE = sys.argv[2]


TSET = 'traincv'



os.system('mkdir ' + LAM_PHASE)
os.chdir(LAM_PHASE)

os.system('ln -s ../base')
os.system('ln -s ../data')
os.system('ln -s ../htefiles')
os.system('ln -s ../lib')

os.system('ln -s ../%s/%s.lam %s.lam.init' % (NN_PHASE, TSET, TSET))
os.system('ln -s ../%s/%s MLP' % (NN_PHASE, MLP))

