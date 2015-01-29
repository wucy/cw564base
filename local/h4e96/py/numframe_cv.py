#! /usr/bin/env python


import os
import re
import sys


raw_cont = open('traincv.lam.esti', 'r').readlines()[2:]

new_cont = dict()

for line in raw_cont:
    line = line.strip()
    split = line.split(' ')
    a = float(split[1])
    b = float(split[2])
    new_cont[split[0]] = [a, b]




raw_cv = open('../lib/flists.mbt/traincv.lst').readlines()[3924:]

cv = set()

out = open("cv.dist", 'w')

for line in raw_cv:
    line = line.strip()
    x = open('tunelam/traincv/%s/MLOG' % line).readlines()
    for line in x:
        if '        1' in line:
            print line
    out.write(line + '\n')

out.close()

