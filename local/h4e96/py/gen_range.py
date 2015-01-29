#! /usr/bin/env python


import re
import sys
import os

inrawlst = open(sys.argv[1], 'r')

outrange = open(sys.argv[2], 'w')

lst = inrawlst.readlines()


pos = 0
cnt = 0
prev = None
for line in lst:
    line = line.strip()
    if prev != line:
        if prev != None:
            outrange.write('%s,%d,%d\n' % (prev, pos, pos + cnt - 1))
            pos = pos + cnt
            cnt = 0
        prev = line
    cnt += 1

outrange.write('%s,%d,%d\n' % (prev, pos, pos + cnt - 1))

outrange.close()
inrawlst.close()

