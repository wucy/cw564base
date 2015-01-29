#! /usr/bin/env python




import os
import re
import sys

sys.path.insert(0, '/home/mifs/cw564/base/global/python/')
from mbt_file_parser import *


NINF= -10000


def gen_log_fn_lst(basis_dir, dataset):
    outcome = os.popen('ls ' + basis_dir + '/' + dataset + '/*/align/LOG')
    ret = list()
    for line in outcome:
        ret.append(line.strip())
    return ret

def parse_log(log_fn):
    ret = dict()
    text = open(log_fn, 'r')
    header = None
    for line in text:
        splits = re.split('\s+', line)
        if 'Act=' in line:
            ret[header] = ret.setdefault(header, 0) + float(splits[-5])
        elif 'Aligning File: ' in line:
            header = splits[2].split('-')[1]
    return ret


def init_spkr_score_dict(lst_fn):
    ret = dict()
    text = open(lst_fn, 'r')
    for line in text:
        ret[line.split('-')[1]] = dict()
    return ret

def new_lambda_dict(spkr_score_dict, num_basis):
    ret = dict()
    for spkr in spkr_score_dict:
        dd = spkr_score_dict[spkr]
        best_basis = None
        best_score = -1e10
        for basis in dd:
            score = dd[basis]
            if (best_score < score):
                best_score = score
                best_basis = basis
        ret[spkr] = list()
        for i in range(num_basis):
            ret[spkr].append(0)
        ret[spkr][best_basis - 1] = 1
    return ret


def gen_spkr_map(spkr_list_fn):
    ret = dict()
    file = open(spkr_list_fn, 'r')
    for line in file:
        id = line.strip()
        id = id[-8:-3]
        ret[id] = line.strip()
    return ret


def update_spkr_score_dict(log_lst, spkr_score_dict, basis):
   for log_fn in log_lst:
        log_res = parse_log(log_fn)
        for spkr in log_res:
            spkr_score_dict[spkr][basis] = spkr_score_dict[spkr].setdefault(basis, 0) + log_res[spkr]


def gen_realign_res(lambda_dict, spkr_map, num_basis, dataset, dpass, basis_dir_prefix):
    os.popen('mkdir -p temp/' + dataset)
    for spkr in spkr_map:
        best_basis = None
        for i in range(num_basis):
            if lambda_dict[spkr][i] == 1:
                best_basis = i
                break
        src =  basis_dir_prefix + str(best_basis + 1) + '/' + dataset + '/' + spkr_map[spkr] + '.1/' + dpass + '/' + dataset + '_' + spkr_map[spkr] + '.mlf'
        tgt_folder = 'temp/' + dataset + '/' + spkr_map[spkr] + '.1/realign'
        os.popen('mkdir -p ' + tgt_folder)
        os.popen('cp ' + src + ' ' + tgt_folder)





if __name__ == '__main__':
    if (len(sys.argv) != 9):
        print 'Usage: python', __file__, '$basis_dir_prefix $spkr_list_fn $lambda_out_fn $scp_fn $num_basis $dataset, $dpass $basis_decode_dir'
        exit()
    

    basis_dir_prefix = sys.argv[1]
    spkr_list_fn = sys.argv[2]
    lambda_out_fn = sys.argv[3] 
    num_basis = int(sys.argv[5])
    dataset = sys.argv[6]
    dpass = sys.argv[7]
    basis_decode_dir_prefix = sys.argv[8]
    
    spkr_score_dict = init_spkr_score_dict(spkr_list_fn)
    spkr_map = gen_spkr_map(spkr_list_fn)


    for basis in range(1, 1 + num_basis):
        log_lst = gen_log_fn_lst('in/dir.basis.' + str(basis), dataset)
        update_spkr_score_dict(log_lst, spkr_score_dict, basis)
    lambda_dict = new_lambda_dict(spkr_score_dict, num_basis)
    

    print spkr_score_dict
    print lambda_dict

    gen_realign_res(lambda_dict, spkr_map, num_basis, dataset, dpass, basis_decode_dir_prefix)
    gen_lambdafile(lambda_out_fn, lambda_dict, num_basis)


