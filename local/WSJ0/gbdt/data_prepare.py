#! /usr/bin/env python


import os
import sys
import re
import numpy




def gen_raw_fealab_lst(fea_fn, lab_fn):
    ret = list()
    feas = open(fea_fn, 'r').readlines()
    labs = open(lab_fn, 'r').readlines()
    if len(feas) != len(labs):
        print "dim fea / lab mismatch!"
        exit(-1)
    current_sent = 0
    current_lst = list()
    for i in range(len(feas)):
        splits = feas[i].strip().split(' ')
        if int(splits[0]) != current_sent:
            print "SENT=%d\tTOT=%d" % (current_sent, len(current_lst))
            current_sent = int(splits[0])
            ret.append(current_lst)
            current_lst = list()

        raw_uttr_fea = splits[2:]
        uttr_lab = int(labs[i].strip().split(' ')[2])
        uttr_fea = list()
        for item in raw_uttr_fea:
            uttr_fea.append(float(item))
        current_lst.append([uttr_lab, uttr_fea])
    print "SENT=%d\tTOT=%d" % (current_sent, len(current_lst))
    ret.append(current_lst)
    return ret


def write_fealab(out_fn, raw_fealab_lst, ncat):
    out = open(out_fn, 'w')
    lab = None
    for sent in raw_fealab_lst:
        for i in range(ncat, len(sent) - ncat):
            lab = sent[i][0]
            fea = list()
            for j in range(i - ncat, i + ncat + 1):
                fea.extend(sent[j][1])
            outlineitm = [str(lab)]
            cnt = 0
            for itm in fea:
                outlineitm.append(str(cnt) + ':' + str(itm))
                cnt += 1
            outline = ' '.join(outlineitm) + '\n'
            out.write(outline)
    out.close()

FEA_DUMP = sys.argv[1]
LAB_DUMP = sys.argv[2]

OUT_FEALAB = sys.argv[3]

NCAT = int(sys.argv[4])



raw_fealab_lst = gen_raw_fealab_lst(FEA_DUMP, LAB_DUMP)
write_fealab(OUT_FEALAB, raw_fealab_lst, NCAT)

