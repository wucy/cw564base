#! /usr/bin/env python

import os
import re
import sys





def gen_gender_dict(raw_gender_fn ,output, bias_weight):
    file = open(raw_gender_fn)
    gender_dict = dict()
    for line in file:
        if len(line) == 0 or line.startswith(';'):
            continue
        spkr_id, gender  = re.split('\s+', line)[0:2]
        spkr_id = '00' + spkr_id.lower()
        if gender == 'M':
            gender_dict[spkr_id] = '%f %f 0' % (bias_weight, 1 - bias_weight)
        elif gender == 'F':
            gender_dict[spkr_id] = '%f 0 %f' % (bias_weight, 1 - bias_weight)
        else:
            print 'Error in parsing the raw gender file.'
            exit(1)
    file.close()

    out = open(output, 'w')
    out.write(str(len(gender_dict)) + ' 3\n')
    for key in gender_dict:
        out.write(key + ' ' + gender_dict[key] + '\n')
    out.close()




if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage : python', __file__, 'RAW_GENDER_FILE OUTPUT BIAS_WEIGHT'
        exit(1)
    gen_gender_dict(sys.argv[1], sys.argv[2], float(sys.argv[3]))

