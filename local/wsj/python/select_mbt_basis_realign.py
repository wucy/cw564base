#! /usr/bin/env python


import os
import re
import sys


NINF= -10000


def gen_log_fn_lst(basis_dir, dataset):
    outcome = os.popen('ls ' + basis_dir + '/' + dataset + '/*/align/LOG')
    ret = list()
    for line in outcome:
        ret.append(line.strip())
    return ret

def parse_log(log_fn, uttr_score_dict):
    text = open(log_fn, 'r')
    header = None
    for line in text:
        splits = re.split('\s+', line)
        if 'Act=' in line:
            print splits
            uttr_score_dict[header] = float(splits[-5])
        elif 'Aligning File: ' in line:
            header = splits[2]

def init_uttr_score_dict(scp_fn):
    ret = dict()
    text = open(scp_fn, 'r')
    for line in text:
        splits = re.split('=', line)
        ret[splits[0]] = NINF
    return ret


def init_spkr_score_dict(lst_fn):
    ret = dict()
    text = open(lst_fn, 'r')
    for line in text:
        ret[line.strip()] = dict()
    return ret

def calc_spkr_score_dict(basis, spkr_score_dict, basis_uttr_score_dict):
    for key, val in basis_uttr_score_dict:
        spkr = re.split('_', key)[0]
        spkr_score_dict[spkr][basis] += val


def new_lambda_dict(spkr_score_dict, num_basis):
    ret = dict()
    for spkr, dd in spkr_score_dict:
        best_basis = None
        best_score = -1e10
        for basis, score in dd:
            if (best_score < score):
                best_score = score
                best_basis = basis - 1 # basis is 0, 1, 2 in storing BUT labeled folder are 1, 2, 3..
        ret[spkr] = list()
        for i in range(num_basis):
            ret[spkr].append(0)
        ret[spkr][best_basis] = 1




if __name__ == '__main__':
    if (len(sys.argv) != 7):
        print 'Usage: python', __file__, '$basis_dir_prefix $spkr_list_fn $lambda_out_fn $scp_fn $num_basis $dataset'
        exit()
    

    basis_dir_prefix = sys.argv[1]
    spkr_list_fn = sys.argv[2]
    lambda_out_fn = sys.argv[3] 
    scp_fn = sys.argv[4] 
    num_basis = int(sys.argv[5])
    dataset = sys.argv[6]
    
    a = gen_log_fn_lst('in/dir.basis.1', dataset)
    basis_res = dict()
    for i in range(1, num_basis + 1):
        basis_res[i] = init_uttr_score_dict(scp_fn)
    
    #print basis_res
    print a 


