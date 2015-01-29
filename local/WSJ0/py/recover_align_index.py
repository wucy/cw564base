#! /usr/bin/env python


import sys
import os
import re


if __name__ != '__main__':
    exit()

inmlf_fn = sys.argv[1]
outmlf_fn = sys.argv[2]
frommap_fn = sys.argv[3]
tomap_fn = sys.argv[4]


frommap_content = open(frommap_fn, 'r').readlines()
frommap = dict()
for line in frommap_content:
    cont = re.split('\s+|\\n', line)
    if len(cont) < 2:
        continue
    frommap[cont[1]] = cont[0]

tomap_content = open(tomap_fn, 'r').readlines()
tomap = dict()
for line in tomap_content:
    cont = re.split('\s+|\\n', line)
    if len(cont) < 2:
        continue
    tomap[cont[0]] = cont[1]

inmlf = open(inmlf_fn, 'r')
outmlf = open(outmlf_fn, 'w')

for line in inmlf:
    line = line.strip()
    if len(line) == 0 or line == '.' or line[0] == '"' or line[0] == '#':
        outmlf.write(line + '\n')
    else:
        cont = re.split('\s+', line)
        #print cont[2]
        #print frommap[cont[2]]
        #print tomap[frommap[cont[2]]]
        outmlf.write(cont[0] + ' ' + cont[1] + ' ' + tomap[frommap[cont[2]]] + '\n')

inmlf.close()
outmlf.close()







