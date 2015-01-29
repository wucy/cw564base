#! /usr/bin/env python

import sys
import os
import re


TSET = sys.argv[1]

NUM_SUBTASKS = int(sys.argv[2])



my_base = 'lib/mbt/%s/%d/' % (TSET, NUM_SUBTASKS)

os.system('mkdir -p ' + my_base)



lst = open('lib/flists.mbt/%s.lst' % (TSET), 'r').readlines()

jobs = list()

for line in lst:
    job = line.strip()
    jobs.append(job)

num_per_task = len(jobs) / NUM_SUBTASKS

cnt = 0
output = None

lst_file = open(my_base + '/LST', 'w')

for i in range(len(jobs)):
    if i % num_per_task == 0:
        if output != None:
            output.close()
        fn = my_base + '/task.%d.lst' % (cnt)
        output = open(fn, 'w')
        lst_file.write(fn + '\n')
        cnt += 1
    output.write(jobs[i] + '\n')

if output != None:
    output.close()


lst_file.close()

