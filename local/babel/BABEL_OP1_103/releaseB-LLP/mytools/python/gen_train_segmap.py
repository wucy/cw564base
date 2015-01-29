#! /usr/bin/env python

import sys
import os
import re

sys.path.insert(0, '/home/mifs/cw564/base/global/python/')
from cw564.io import *



def read_babel_gender(fn):
    ret = dict()
    content = open(fn, 'r').readlines()
    for line in content:
        line = line.strip()
        if line.startswith('outputFn'): #first line
            continue
        splits = re.split('\s+', line)
        val = splits[7]

        raw_key = re.split('_', splits[0])
        key1 = 'BPL103'
        key2 = '%s-%s-%s' % tuple(raw_key[3:6])
        key3 = raw_key[6][0:2]
        if key3 != 'in' and key3 != 'ou':
            key3 = 'sc'
        key = key1 + '-' + key2 + '-' + key3
        

        ret[key] = val

    return ret


if (len(sys.argv) != 5):
    print 'Usage:', __file__, 'IN_SCP OUT_SEGMAP IN_GENDER_1 IN_GENDER_2'
    exit(-1)

in_scp = open(sys.argv[1], 'r')
out_sm_fn = sys.argv[2]
in_gender_fn = sys.argv[3]
in_gender_fn_2 = sys.argv[4]

seg_map = dict()


gender_map = read_babel_gender(in_gender_fn)
gender_map.update(read_babel_gender(in_gender_fn_2))

cnt = 0
for line in in_scp:
    token = line.split('_')[0]
    if gender_map[token] == 'F':
        seg_map[str(cnt)] = 'female'
    else:
        seg_map[str(cnt)] = 'male'
    cnt += 1

mbt.write_segmap(out_sm_fn, seg_map)

