#! /usr/bin/env python

import os
import sys
import re



SCP = sys.argv[1]
OUT_MLF = sys.argv[2]

NUM_BASIS = 2
logs = ['b1/LOG', 'b2/LOG']
mlfs_fn = ['b1/csrnab_dt_h1.mlf', 'b2/csrnab_dt_h1.mlf']


sys.path.insert(0, '/home/mifs/cw564/base/global/python/')

from cw564.io import *


def parse_log(log_fn):
    os.system('cat %s | egrep "LM=|\.plp" > content' % (log_fn))
    
    ret = dict()

    content = open('content', 'r').readlines()
    cnt = 0
    while cnt < len(content):
        if '.plp' in content[cnt]:
            if cnt == len(content) - 1 or '.plp' in content[cnt + 1]: # error omit
                cnt += 1
                continue
            else:
                token = re.split('\s+', content[cnt])[-2].split('.')[0]
                raw_score = content[cnt + 1]
                score = float(re.split(']\s+', raw_score)[1].split(' ')[0])
                ret[token] = score
                cnt += 2

    return ret


scores = dict()
mlfs = dict()
for i in range(NUM_BASIS):
    scores[i] = parse_log(logs[i])
    mlfs[i] = htk.read_mlf(mlfs_fn[i])

scps = open(SCP, 'r').readlines()



out_mlf = dict()
orders = list()
for line in scps:
    raw_key = line.split('.')[0]
    search_key = '*/' + raw_key
    better_mlf = None
    if scores[0][raw_key] > scores[1][raw_key]:
        better_mlf = mlfs[0][raw_key]
    else:
        better_mlf = mlfs[1][raw_key]
    out_mlf[search_key] = better_mlf
    orders.append(search_key)

htk.write_mlf(OUT_MLF, out_mlf, orders)


