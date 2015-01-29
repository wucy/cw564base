#! /usr/bin/env python

import sys
import os
import re

sys.path.insert(0, '/home/mifs/cw564/base/global/python')

from htk_file_parser import *
from mbt_file_parser import *


def max_id(a_list):
    ret = None
    max_val = -1e5
    for i in range(len(a_list)):
        if max_val < a_list[i]:
            ret = i
            max_val = a_list[i]
    return ret + 1

def get_spkr_name(token):
    return re.split('\-', token)[1]

def gen_spkr_new_mlfscp(raw_scp, scp_dict, mlf_dict, lambda_dict):
    new_scp = dict()
    new_mlf = dict()
    for spkr in lambda_dict:
        new_scp[spkr] = dict()
        new_mlf[spkr] = dict()
    for token in raw_scp:
        spkr = get_spkr_name(token)
        basis_id = max_id(lambda_dict[spkr])
        if token not in scp_dict[basis_id]:
            continue
        if token not in mlf_dict[basis_id]:
            continue
        new_scp[spkr][token] = scp_dict[basis_id][token]
        new_mlf[spkr][token] = mlf_dict[basis_id][token]
    return new_scp, new_mlf


def gen_mlfscp_files(scp, mlf, out_dir):
    os.popen('mkdir -p ' + out_dir)
    order = list(scp.keys())
    gen_mlf_file(out_dir + '/MLF', mlf, order)
    gen_scp_file(out_dir + '/SCP', scp, order)





if __name__ == '__main__':
    if len(sys.argv) != 7:
        print 'Usage: python', __file__, '$raw_scp_fn $basis_dir_prefix $dataset $lambda_in_fn $num_basis $out_dir'
        exit()

    raw_scp_fn = sys.argv[1]
    basis_dir_prefix = sys.argv[2]
    dataset = sys.argv[3]
    lambda_in_fn = sys.argv[4]
    num_basis = int(sys.argv[5])
    out_dir = sys.argv[6]


    raw_scp = parse_scp(raw_scp_fn)
    lambda_dict = parse_lambdafile(lambda_in_fn)

    scp_dict = dict()
    mlf_dict = dict()
    for i in range(1, num_basis + 1):
        print basis_dir_prefix + str(i) + '/lib/flists_align/' + dataset + '.scp.new'
        scp_dict[i] = parse_scp(basis_dir_prefix + str(i) + '/lib/flists_align/' + dataset + '.scp.new')
        mlf_dict[i] = parse_mlf(basis_dir_prefix + str(i) + '/lib/mlabs/' + dataset + '.mlf')
        for key in scp_dict[i]:
            if key not in mlf_dict[i]:
                print key

    scps, mlfs = gen_spkr_new_mlfscp(raw_scp, scp_dict, mlf_dict, lambda_dict)

    for spkr in lambda_dict:
        gen_mlfscp_files(scps[spkr], mlfs[spkr], out_dir + '/' + spkr + '/')


