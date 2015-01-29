#! /usr/bin/env python

import sys
import re
import os


MY_BASE = sys.argv[1]
MY = sys.argv[2]
LAMFILE = sys.argv[3]
NUM_BASIS = sys.argv[4]
NUM_RGC = sys.argv[5]
STA2CLS = sys.argv[6]
MATFILE = sys.argv[7]
NUM_OUT = 3033


lam_cmd = 'cat %s | grep %s' % (LAMFILE, MY)
print lam_cmd
rawlam = re.split('\s+', os.popen(lam_cmd).readlines()[0])[1:-1]
lam = ' ' + rawlam[0]
for i in range(1,len(rawlam)):
    lam += ' ' + rawlam[i]
lam += ' '

rd=4000
lr=1e-4
stop=1e-6#not use

esti_lam_fn = '%s/lambda.esti' % (MY_BASE)

cmd = '~/src/ext.loglinear/ext_loglinear %s %s %s %s %s %d %f %f %s %s 2> %s/LAMLOG' % (NUM_OUT, NUM_BASIS, NUM_RGC, STA2CLS, MATFILE, rd, lr, stop, esti_lam_fn, lam, MY_BASE)
print cmd
os.system(cmd)

