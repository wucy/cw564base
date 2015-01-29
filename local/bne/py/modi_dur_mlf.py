#! /usr/bin/env python


import os
import sys



INMLF = sys.argv[1]
OUTMLF = sys.argv[2]


raw_content = open(INMLF, 'r').readlines()


out_f = open(OUTMLF, 'w')


for line in raw_content:
    splits = line.split(' ')
    if len(splits) > 2:
        sta = str((int(splits[0]) + 100) / 1000 * 1000)
        end = str((int(splits[1]) + 100) / 1000 * 1000)
        out_f.write(sta)
        out_f.write(' ')
        out_f.write(end)
        for i in range(2, len(splits)):
            out_f.write(' ')
            out_f.write(splits[i])
    else:
        out_f.write(line)

out_f.close()

