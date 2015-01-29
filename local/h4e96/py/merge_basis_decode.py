#! /usr/bin/env python


import re
import os
import sys



tset = sys.argv[1]
old_pass = sys.argv[2]
new_pass = sys.argv[3]

raw_dir = sys.argv[4]


os.system('mkdir -p test')

lst = os.popen('ls ' + raw_dir + '/' + tset)

for spkr in lst:
    os.system('mkdir -p test/' + tset + '/' + spkr.strip() + '/' + new_pass)
    os.system('cp -r ' + raw_dir + '/' + tset + '/' + spkr.strip() + '/' + old_pass + '/* ' + 'test/' + tset + '/' + spkr.strip() + '/' + new_pass)


