#! /usr/bin/env python


import re
import sys


inp = open(sys.argv[1], 'r')

outp = open(sys.argv[2], 'w')

for line in inp:
    if line[0] != '"':
        outp.write(line)
    else:
        newline = re.sub('\-[0-9A-Z]{5}\-', '-', line)
        outp.write(newline)

outp.close()
inp.close()
