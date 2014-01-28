#! /usr/bin/env python

import os
import re
import sys





def gen_gender_dict(raw_gender_fn ,output):
    file = open(raw_gender_fn)
    gender_dict = dict()
    for line in file:
        if len(line) == 0 or line.startswith(';'):
            continue
        spkr_id, gender  = re.split('\s+', line)[0:2]
        spkr_id = spkr_id.lower()
        if gender == 'M':
            gender_dict[spkr_id] = '1 0'
        elif gender == 'F':
            gender_dict[spkr_id] = '0 1'
        else:
            print 'Error in parsing the raw gender file.'
            exit(-1)
    file.close()

    out = open(output, 'w')
    out.write(str(len(gender_dict)) + ' 2\n')
    for key in gender_dict:
        out.write(key + ' ' + gender_dict[key] + '\n')
    out.close()




if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage : python run.py RAW_GENDER_FILE OUTPUT '
        exit(-1)
    gen_gender_dict(sys.argv[1], sys.argv[2])

