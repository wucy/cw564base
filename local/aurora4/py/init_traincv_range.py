#! /usr/bin/env python

import os
import sys
import re


SCP = sys.argv[1]
PREFIX = sys.argv[2]
OUT_RANGE = sys.argv[3]



scps = open(SCP, 'r').readlines()

out = open(OUT_RANGE, 'w')

prev = None
cnt = 0
for i in range(len(scps)):
    token = PREFIX + '_' + scps[i][0:28]
    if prev != token:
        if prev != None:
            out.write(str(cnt) + '\n')
            cnt += 1
        out.write(token + ',' + str(cnt) + ',')
        prev = token
    else:
        cnt += 1

out.write(str(cnt) + '\n')

out.close()

