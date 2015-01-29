#! /usr/bin/env python


import os
import sys
import re
import random



TSET = sys.argv[1]
MLP = sys.argv[2]
CONFIG = sys.argv[3]
NUM_BASIS = sys.argv[4]
LAMFILE = sys.argv[5]
MY = sys.argv[6]



base = 'tunelam'
my_base = './%s/%s/%s/%s/' % (base, TSET, MY, CONFIG)


#setup directory
whereami = os.getcwd()
pfile_dir = whereami + '/../data/pfile/'
fea_pfile = pfile_dir + '/' + TSET + '.pfile'
lab_pfile = pfile_dir + '/' + TSET + '_lab_spkr.pfile'

os.popen('mkdir -p ' + my_base)
os.popen('ln -s %s %s/fea.pfile' % (fea_pfile, my_base))
os.popen('ln -s %s %s/lab.pfile' % (lab_pfile, my_base))


segmap_fn = my_base + '/segmap.fake'

os.popen('echo "1" > %s ; echo "0 %s" >> %s' % (segmap_fn, MY, segmap_fn))

range_fn = '../lib/flists.mbt/%s.range' % (TSET)
raw_content = re.split(',', os.popen('cat %s | grep %s' % (range_fn, MY)).readline())
ssta = raw_content[1]
send = raw_content[2].strip()



tmp_mat = '/tmp/%s.%f.mat' % (MY, random.random())

print tmp_mat


cmd1 = 'base/local/tools/genlamfile_one_task.sh %s %s %s %s %s %s %s %s' % (my_base, MLP, NUM_BASIS, LAMFILE, segmap_fn, ssta, send, tmp_mat)
print cmd1
os.system(cmd1)


cmd2 = './base/local/py/matlab_tunelam_one_task_part.py %s %s %s %s %s %s' % (my_base, MY, LAMFILE, NUM_BASIS, MLP, tmp_mat)
print cmd2
os.system(cmd2)

