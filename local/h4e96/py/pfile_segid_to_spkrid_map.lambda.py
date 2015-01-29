#! /usr/bin/env python


import sys
import re
import os

if len(sys.argv) != 4:
    print 'Usage: python', __file__, '$SCP $OUTPUT $OUTPUT_PY'
    exit(0)

scpfile = open(sys.argv[1], 'r')

outfile = open(sys.argv[2], 'w')

outpyfile = open(sys.argv[3], 'w')

seg_list = []

seg2spkr = dict()

cnt = 0
for line in scpfile:
    token = line[7:12]
    seg_list.append(str(cnt) + ' ' + token)
    seg2spkr[cnt] = token
    cnt += 1


scpfile.close()

outfile.write(str(cnt) + '\n')
for line in seg_list:
    outfile.write(line + '\n')

outfile.close()


outpyfile.write(str(seg2spkr));
outpyfile.close()

