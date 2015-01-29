#! /usr/bin/env python

import sys
import os
import re

fin = open(sys.argv[1], 'r')
fout = open(sys.argv[2], 'w')

for line in fin:
    out_line = None
    if line[0] == '\n' or line[0] == '.' or line[0] == '#' or line[0] == '"':
        out_line = line
    else:
        out_line = re.split('\s+', line)[2] + '\n'
    fout.write(out_line)

fin.close()
fout.close()

