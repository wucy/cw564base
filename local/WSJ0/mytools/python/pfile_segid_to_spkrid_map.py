#! /usr/bin/env python


import sys
import re
import os

if len(sys.argv) != 3:
    print 'Usage: python', __file__, '$SCP $OUTPUT'
    exit(0)

scpfile = open(sys.argv[1], 'r')

outfile = open(sys.argv[2], 'w')

seg_list = []


cnt = 0
for line in scpfile:
    seg_list.append(str(cnt) + ' ' + line[0:12] + '-xx')
    cnt += 1


scpfile.close()

outfile.write(str(cnt) + '\n')
for line in seg_list:
    outfile.write(line + '\n')

outfile.close()
