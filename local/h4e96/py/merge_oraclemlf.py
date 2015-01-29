#! /usr/bin/env python


import os
import re
import sys

sys.path.insert(0, '/home/mifs/cw564/base/global/python')
from cw564.io import *

INMLF_FN = 'lib/mlabs/dev03.mlf'
INSCP_FN = 'lib/flists.hcopy/dev03.scp'
IN_REAL_SCP_FN = '../../lib/flists.test/dev03.scp'
OUTMLF_FN = 'oracle.mlf'


scpsta_map = dict()
toscp_map = dict()

outmlfs = dict()


def patch_mlf(outmlf, word, sta, end):
    for pos in range(sta, end + 1):
        outmlf[pos] = word





def offset(mlf):
    global scpsta_map
    return scpsta_map[mlf]


def convmap(mlf):
    global toscp_map
    if toscp_map[mlf] not in outmlfs:
        outmlfs[toscp_map[mlf]] = dict()
    return outmlfs[toscp_map[mlf]]


def readscp(scp_fn):
    global scpsta_map
    global toscp_map
    scps = open(scp_fn, 'r')
    for line in scps:
        line = line.strip()
        token = line.split('.')[0]
        sta = int(line.split('[')[1].split(',')[0])
        scpsta_map[token] = sta

        to_token = line.split('/')[-1].split('.')[0]
        toscp_map[token] = to_token
    scps.close()



    


real_scpsta_map = dict()
real_scpend_map = dict()
real_toscp_map = dict()


def readrealscp(real_scp_fn):
    scps = open(real_scp_fn, 'r')
    for line in scps:
        line = line.strip()
        token = line.split('.')[0]
        sta = int(line.split('[')[1].split(',')[0])
        end = int(line.split('[')[1].split(',')[1].split(']')[0])
        to_token = line.split('/')[-1].split('.')[0]
        real_scpsta_map[token] = sta
        real_scpend_map[token] = end
        real_toscp_map[token] = to_token

    scps.close()


readscp(INSCP_FN)
readrealscp(IN_REAL_SCP_FN)


inmlfs = htk.read_mlf(INMLF_FN)
for mlf in inmlfs:
    local_sta = None
    now_wrd = None
    cnt = 0
    while cnt < len(inmlfs[mlf]):
        line = inmlfs[mlf][cnt]
        splits = line.split(' ')
        if len(splits) == 5:
            if now_wrd != None: #no the first non-<s> word
                if now_wrd != '<s>':
                    #print local_sta, local_end, now_wrd
                    outmlf = convmap(mlf)
                    glb_sta = offset(mlf) + local_sta
                    glb_end = offset(mlf) + local_end
                    patch_mlf(outmlf, now_wrd, glb_sta, glb_end)
            local_sta = int((float(splits[0]) + 10.0) / 100.0) * 100 / 100000
            now_wrd = splits[4]
        local_end = int((float(splits[1]) + 10.0) / 100.0) * 100 / 100000 - 1
        cnt += 1

#last is <s>, so no need to care the last wrd



fout = open(OUTMLF_FN, 'w')
fout.write('#!MLF!#\n')
klst = real_toscp_map.keys()
klst.sort()
for mlf in klst:
    finalmlf = list()
    fout.write('"%s.lab"\n' % (mlf))
    sta = real_scpsta_map[mlf]
    end = real_scpend_map[mlf]
    toscp = real_toscp_map[mlf]
    sortedkeys = outmlfs[toscp].keys()
    sortedkeys.sort()
    leftno = False
    key = None
    for key in sortedkeys:
        if key >= sta and key <= end and outmlfs[toscp][key] not in finalmlf:
            if len(finalmlf) == 0:
                left = key - 1
                right = key + 1
                my = outmlfs[toscp][key]
                while left in outmlfs[toscp] and my == outmlfs[toscp][left]:
                    left -= 1
                while right in outmlfs[toscp] and my == outmlfs[toscp][right]:
                    right += 1
                if right - key < key - left:
                    leftno = True
            finalmlf.append(outmlfs[toscp][key])
    rightno = False
    left = key - 1
    right = key + 1
    my = outmlfs[toscp][key]
    while left in outmlfs[toscp] and my == outmlfs[toscp][left]:
        left -= 1
    while right in outmlfs[toscp] and my == outmlfs[toscp][right]:
        right += 1
    if right - key > key - left:
        rightno = True
    if leftno:
        finalmlf = finalmlf[1:]
    if rightno:
        finalmlf = finalmlf[2:-1]
    for item in finalmlf:
        fout.write(item + '\n')
    fout.write('.\n')
fout.close()
