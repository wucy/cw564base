#! /usr/bin/env python

import sys
import os
import re

TOKEN_FN = sys.argv[1]
CNT_FN = sys.argv[2]
OUT_FN = sys.argv[3]

tokens = open(TOKEN_FN, 'r').readlines()
cnts = open(CNT_FN, 'r').readlines()


out = open(OUT_FN, 'w')


now = 0

for i in range(len(tokens)):
    end = now + int(cnts[i].strip()) - 1
    out.write(tokens[i].strip() + ',' + str(now) + ',' + str(end) + '\n')
    now = end + 1

out.close()
