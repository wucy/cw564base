#! /usr/bin/env python

import os
import sys
import re


SCP = '/home/mifs/cw564/exp/bluea/h4e96/exp/M2/decode-mbt/oracle/seg-cut.v3/lib/flists/dev03.scp'




content = open(SCP, 'r').readlines()


for line in content:
    splits1 = line.split('[')
    my1 = splits1[1]
    splits2 = my1.split(']')
    my2 = splits2[0]
    splits3 = my2.split(',')
    sta = int(splits3[0])
    end = int(splits3[1])
    if end - sta > 3000:
        print line


