#! /usr/bin/env python

import os
import sys
import re


MLF1 = 'align/hybrid/lib/mlabs/csrnab_dt_h1.state.mlf'

MLF1 = 'align/hyp_oracle_aln_hybrid/lib/mlabs/csrnab_dt_h1.state.mlf'

MLF1 = 'align/hybrid/basis_align_select/csrnab_dt_h1.index.mlf'

MLF2 = 'align/hyp_oracle_aln_hybrid/basis_align_select/csrnab_dt_h1.index.mlf'

def accum(mlf_fn):
    ret = list()
    contents = open(mlf_fn, 'r').readlines()
    for line in contents:
        splits = re.split('\s+', line)
        if len(splits) < 3:
            continue
        sta = (int(splits[0]) + 10) / 100000
        end = (int(splits[1]) + 10) / 100000
        token = splits[2].strip()
        for i in range(end - sta):
            ret.append(token)

    return ret

a = accum(MLF1)
b = accum(MLF2)

print a[:10]

err = 0
for i in range(len(a)):
    if a[i] != b[i]:
        err += 1


print float(err) / len(a)
