#! /usr/bin/env python


import os
import sys
import re




TSET = sys.argv[1]
MLP = sys.argv[2]
CONFIG = sys.argv[3]
NUM_BASIS = sys.argv[4]
LAMFILE = sys.argv[5]
MY = sys.argv[6]

base = 'tunelam'
my_base = './%s/%s/%s/%s/' % (base, TSET, MY, CONFIG)

segmap_fn = my_base + '/segmap.fake'

os.popen('echo "1" > %s ; echo "0 %s" >> %s' % (segmap_fn, MY, segmap_fn))

range_fn = 'lib/flists.test/%s.range' % (TSET)
raw_content = re.split(',', os.popen('cat %s | grep %s' % (range_fn, MY)).readline())
ssta = raw_content[1]
send = raw_content[2].strip()


cmd1 = 'base/local/tools/genlamfile_one_task_test.sh %s %s %s %s %s %s %s' % (my_base, MLP, NUM_BASIS, LAMFILE, segmap_fn, ssta, send)
print cmd1

os.system(cmd1)

cmd2 = './base/local/py/matlab_tunelam_one_task_part_test.py %s %s %s %s %s' % (my_base, MY, LAMFILE, NUM_BASIS, MLP)
print cmd2


os.system(cmd2)

