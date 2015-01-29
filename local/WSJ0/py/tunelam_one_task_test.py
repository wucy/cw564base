#! /usr/bin/env python


import os
import re
import sys


TSET = sys.argv[1]
MLP = sys.argv[2]
CONFIG = sys.argv[3]
NUM_BASIS = sys.argv[4]
LAMFILE = sys.argv[5]
MY = sys.argv[6]


base = "tunelam"
my_base = './%s/%s/%s/%s/' % (base, TSET, MY, CONFIG)




range_fn = 'lib/flists.test/%s.range' % (TSET)
range_content = os.popen('cat %s | grep %s' % (range_fn, MY)).readline()
raw_range = re.split(',', range_content)
sta = raw_range[1]
end = raw_range[2].strip()

print sta, end

#gen_fake_segmap

segmap = my_base + '/segmap.fake'
os.popen('echo "1" > %s; echo "0 %s" >> %s;' % (segmap, MY, segmap))

#gen_fealab
cmd = "base/local/tools/genlamfile_one_task.sh %s %s %s %s %s %s %s" % (my_base, MLP, NUM_BASIS, LAMFILE, segmap, sta, end)

print cmd

os.popen(cmd)

#tune
cmd2 = "base/local/py/matlab_tune_one_task.py %s" % (my_base)

print cmd2

os.popen(cmd2)


