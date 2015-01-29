#! /usr/bin/env python


import os
import re
import sys


sys.path.insert(0, '/home/mifs/cw564/base/global/python/')

from cw564.io import htk


log1 = sys.argv[1]
log2 = sys.argv[2]
out_mlf = sys.argv[3]
raw_mlf = sys.argv[4]
mlf1 = sys.argv[5]
mlf2 = sys.argv[6]



mlfs_out = htk.read_mlf(raw_mlf)

mlfs1 = htk.read_mlf(mlf1)
mlfs2 = htk.read_mlf(mlf2)



def parse_log(log_fn):
    cont = open(log_fn, 'r').readlines()
    cnt = 0
    ret = dict()
    while cnt < len(cont):
        line = cont[cnt]
        if line.startswith('Aligning File'):
            token = line.strip().split(' ')[2].split('.')[0]
            token = token[0:7] + token[13:]
            while cnt < len(cont) and 'Act=' not in cont[cnt]:
                cnt += 1
            if cnt < len(cont):
                x = cont[cnt].split('] ')[1].split(' [')[0]
                ret[token] = -float(x)
        cnt += 1
    return ret

score1 =  parse_log(log1)
score2 = parse_log(log2)


for itm in score1:
    if itm not in score2:
        continue
    if score1[itm] > score2[itm]:
        itm = '*/' + itm
        mlfs_out[itm] = mlfs1[itm]
    else:
        itm = '*/' + itm
        mlfs_out[itm] = mlfs2[itm]


htk.write_mlf(out_mlf, mlfs_out)
