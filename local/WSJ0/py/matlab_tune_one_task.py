#! /usr/bin/env python

import sys
import re
import os


my = sys.argv[1]



mlp = 'decodeMLP/MLP.mbt'

mscr1 = "addpath('~/base/global/matlab/');"
mscr2 = "load('" + mlp + "', '-mat');"
mscr3 = "fealab=binmat_read('%s/fealab.mat', 2001);" % my
mscr4 = "x=fealab(:,2:2001);y=fealab(:,1)+1;"

#lam_cmd = 'cat lib/mbt/traincv.lam.init | grep ' + my
#print lam_cmd
#rawlam = re.split('\s+', os.popen(lam_cmd).readlines()[0])[1:-1]
#lam = '[' + rawlam[0]
#for i in range(1,len(rawlam)):
#    lam += ';' + rawlam[i]
#lam += ']'

lam = '[0.5; 0.5]'

mscr5 = "lambda=" + lam + ";"

mscr6 = "final_lambda=loglinear_GD_opt_many(lambda, weights45, bias5', x, y, 2, -1, 0.002);"
mscr7 = "save('%s/lambda.est', 'final_lambda', '-ascii');quit;" % my

mscr =  mscr1 + mscr2 + mscr3 + mscr4 + mscr5 + mscr6 + mscr7
print mscr
os.system('matlab -nosplash -nojvm -nodisplay -nodesktop -r "' + mscr + ('" > %s/MLOG' % my))

