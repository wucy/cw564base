#! /usr/bin/env python

import sys
import re
import os


my = sys.argv[1]



mlp = 'fwdMLP/LogMLP.NN1.1em9'

mscr1 = "addpath('~/base/global/matlab/');"
mscr2 = "load('" + mlp + "', '-mat');"
mscr3 = "fealab=binmat_read('%s/fealab', 2001);" % ('workdir/' + my)
mscr4 = "x=fealab(:,2:2001);y=fealab(:,1)+1;"

lam_cmd = 'cat lib/mbt/traincv.lam.init | grep ' + my
print lam_cmd
rawlam = re.split('\s+', os.popen(lam_cmd).readlines()[0])[1:-1]
lam = '[' + rawlam[0]
for i in range(1,len(rawlam)):
    lam += ';' + rawlam[i]
lam += ']'

mscr5 = "lambda=" + lam + ";"

mscr6 = "final_lambda=loglinear_GD(lambda, weights45, bias5', x, y, 2, -1, 0.1);"
mscr7 = "save('%s/lambda.est', 'final_lambda', '-ascii');quit;" % ('workdir/' + my)

mscr =  mscr1 + mscr2 + mscr3 + mscr4 + mscr5 + mscr6 + mscr7
print mscr
os.system('matlab -r "' + mscr + '" > %s/MLOG' % ('workdir/' + my))

