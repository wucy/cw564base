#! /usr/bin/env python

import os
import re
import sys


in_fn = sys.argv[1]
out_fn = sys.argv[2]

ifs = open(in_fn, 'r')
ofs = open(out_fn, 'w')

ifs.readline()

raw_content = ifs.readlines()

ofs.write('traincv = [\n');

for line in raw_content:
    splits = re.split('\s+', line)
    ofs.write(splits[1])
    for i in range(2, len(splits)):
        ofs.write('\t' + splits[i])
    ofs.write(';\n')

ofs.write('];')

ifs.close()
ofs.close()

