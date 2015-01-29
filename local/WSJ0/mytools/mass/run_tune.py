#! /usr/bin/env python


import os
import sys
import re


os.popen('ls workdir > lib/mbt/tune.lst')


lst = open('lib/mbt/tune.lst', 'r')

tot = len(lst.readlines())


x = os.popen('qsub -l qp=low -l generation=70 -t 1-%d -tc 10 -S /bin/bash base/tools/run-array-job.sh lib/mbt/tune.lst /usr/bin/python tune_one_spkr.py SET' % tot)

#for line in lst:
#    x = os.popen("qsub -l qp=low -l generation=70 -S /usr/bin/python tune_one_spkr.py " + line)
