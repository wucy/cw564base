#! /usr/bin/env python


import os
import sys
import re
import random
import math





lst = sys.argv[1]
inclust = sys.argv[2]
outlam = sys.argv[3]
num_basis  = sys.argv[4]


lll = open(lst, 'r').readlines()
ccc = open(inclust, 'r').readlines()


ofs = open(outlam, 'w')

ofs.write(str(len(lll)) + ' ' + num_basis + '\n')


for i in range(len(lll)):
    ofs.write(lll[i].strip())
    ind = int(float(re.split('\s+', ccc[i].strip())[0]))
    for j in range(1, int(num_basis) + 1):
        if j == ind:
            ofs.write(' 1')
        else:
            ofs.write(' 0')
    ofs.write('\n')


ofs.close()

