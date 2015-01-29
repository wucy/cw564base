#! /usr/bin/env python


import re
import os
import sys


def parse_lambdafile(in_fn):
    ret = dict()
    text = open(in_fn, 'r')
    content = text.readlines()
    text.close()
    tot_spkr, num_basis = [int(s) for s in re.split('\s+', content[0])[0 : 2]]
    for i in range(1, len(content)):
        splits = re.split('\s+', content[i])
        spkr, weights = [splits[0], [float(weight) for weight in splits[1 : num_basis + 1]]]
        ret[spkr] = weights
    return ret

def gen_lambdafile(out_fn, lambda_dict, num_basis):
    out = open(out_fn, 'w')
    out.write(str(len(lambda_dict)) + ' ' + str(num_basis) + '\n')
    for spkr in lambda_dict:
        out.write(spkr)
        for i in range(num_basis):
            out.write(' ' + str(lambda_dict[spkr][i]))
        out.write('\n')
    out.close()




