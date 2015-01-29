#! /usr/bin/env python

import sys
import os
import re

def parse_res_file(res_fn, spkrs):
    res = dict()
    
    file = open(res_fn, 'r')
    for line in file:
        splits = re.split('\s+', line)
        if len(splits) >= 3 and splits[2] in spkrs:
            res[splits[2]] = float(splits[-4])

    return res

def gen_spkr_map(spkr_list_fn):
    ret = dict()
    file = open(spkr_list_fn, 'r')
    for line in file:
        id = line.strip()
        id = id[-8:-3] + 'xx'
        ret[id] = line.strip()
    return ret

def gen_oracle_res(basis_reses, skpr_map, num_basis, dataset, dpass, basis_dir_prefix):
    os.popen('mkdir -p temp/' + dataset)
    for spkr in spkr_map:
        best_basis = None
        best_err = 100
        for basis in range(1, num_basis + 1):
            if basis_reses[basis][spkr] < best_err:
                best_err = basis_reses[basis][spkr]
                best_basis = basis

        src =  basis_dir_prefix + str(best_basis) + '/' + dataset + '/' + spkr_map[spkr] + '.1/' + dpass + '/' + dataset + '_' + spkr_map[spkr] + '.mlf'
        tgt_folder = 'temp/' + dataset + '/' + spkr_map[spkr] + '.1/oracle'
        os.popen('mkdir -p ' + tgt_folder);
        os.popen('cp ' + src + ' ' + tgt_folder);

    

if __name__ == '__main__':
    if len(sys.argv) != 7 or len(sys.argv) == 2 and sys.argv[1] == '--help':
        print 'Usage: python' , __file__, 
        print '$NUM_BASIS $BASIS_DIR_PREFIX $SPKLIST $BASIS_RES_PREFIX $DATASET $PASS'
        exit()

    num_basis = int(sys.argv[1])
    basis_dir_prefix = sys.argv[2]
    spkr_list = sys.argv[3]
    basis_res_prefix = sys.argv[4]
    dataset = sys.argv[5]
    dpass = sys.argv[6]


    spkr_map = gen_spkr_map(spkr_list)

    basis_res_maps = dict()

    for basis in range(1, num_basis + 1):
        basis_res_maps[basis] = parse_res_file(basis_res_prefix + str(basis), spkr_map.keys())

    #print basis_res_maps

    gen_oracle_res(basis_res_maps, spkr_map, num_basis, dataset, dpass, basis_dir_prefix)

    

