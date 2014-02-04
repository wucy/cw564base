#! /usr/bin/env python

import sys
import os
import re


if len(sys.argv) != 4 or sys.argv[1] == '--help':
    print 'Usage: python', __file__, 'INPUT_TRAINCV_SCP OUTPUT_TRAINCV_SCP NUM_UTTR_PER_SPKR'
    exit()


scp_file = open(sys.argv[1], 'r')
num_uttr_spkr = int(sys.argv[3])


unique_dict = dict()


for line in scp_file:
    if len(unique_dict.setdefault(line[0:12], [])) < num_uttr_spkr:
        unique_dict[line[0:12]].append(line)

scp_file.close()

output = open(sys.argv[2], 'w')

for key in unique_dict:
    for val in unique_dict[key]:
        output.write(val)

output.close()
