#! /usr/bin/env python

import os
import re
import sys


_PREFIX = 'WSJCSR-00'
_DIR = './raw/'
_DIM = 2

_OUTPUT = 'init/lambda.init'


def data_gen(prefix = _PREFIX, dir = _DIR, dim = _DIM, output = _OUTPUT):
    dir_list = os.listdir(dir)
    spkr_lambda_dict = dict()
    for file_name in dir_list:
        if 'wgt' not in file_name:
            continue
        file = open(_DIR + file_name)
        for line in file:
            if line.startswith('<CATWEIGHTS>'):
                content = line.strip()
                weight = content.split(' ')[1:dim + 1]
                spkr_lambda_dict[prefix + os.path.splitext(file_name)[0]] = weight
                break
        file.close()
    lambdafile = open(output, 'w')
    lambdafile.write(str(len(spkr_lambda_dict)) + ' ' + str(dim) + '\n')
    for key in spkr_lambda_dict:
        lambdafile.write(key)
        
        delta = 0
        for e in spkr_lambda_dict[key]:
            delta += float(e)
        delta = (delta - 1) / len(spkr_lambda_dict[key])
        for e in spkr_lambda_dict[key]:
            lambdafile.write(' ' + str(float(e) - delta))
        lambdafile.write('\n')
    lambdafile.close()


if __name__ == '__main__':
    data_gen(dim=int(sys.argv[1]))

