#! /usr/bin/env python

import sys
import re
import os


MY_BASE = sys.argv[1]
MY = sys.argv[2]
LAMFILE = sys.argv[3]
NUM_BASIS = sys.argv[4]
MLP = sys.argv[5]

mscr1 = "addpath('/home/mifs/cw564/base/global/matlab/');"
mscr2 = "load('" + MLP + "', '-mat');"
mscr3 = "fealab=binmat_read('%s/fealab.mat', 2001);" % (MY_BASE)
mscr4 = "x=fealab(:,2:2001);y=mod(fealab(:,1)+1,10000);"

lam_cmd = 'cat %s | grep %s' % (LAMFILE, MY)
print lam_cmd
rawlam = re.split('\s+', os.popen(lam_cmd).readlines()[0])[1:-1]
lam = '[' + rawlam[0]
for i in range(1,len(rawlam)):
    lam += ';' + rawlam[i]
lam += ']'

mscr5 = "lambda=" + lam + ";"

mscr6 = "final_lambda=loglinear_GD_opt(lambda, weights67, bias7', x, y, 2, -1, 0.002);"
mscr7 = "save('%s/lambda.est', 'final_lambda', '-ascii');quit;" % (MY_BASE)

mscr =  mscr1 + mscr2 + mscr3 + mscr4 + mscr5 + mscr6 + mscr7
print mscr
os.system('matlab -r "' + mscr + '" > %s/MLOG' % (MY_BASE))


