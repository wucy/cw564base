#! /usr/bin/env python

import os
import sys
import re


convmap_fn = 'dev.convmap'
fea_base = '/home/bluea/mjfg/bne/data/plp'
ctm_fn = 'dev03.stm'



def purge_wrd_lst(wrds):
    ret = list()
    flag1 = False
    flag2 = False
    for wrd in wrds:
        if wrd.startswith('(%'):
            continue
        if wrd.startswith('('):
            wrd = wrd[1:-2]
        if wrd == '{':
            flag1 = True
            continue
        if wrd == '}':
            flag1 = False
            flag2 = False
            continue
        if flag1 and not flag2:
            flag2 = True
            ret.append(wrd)
            continue
        if flag1 and flag2:
            continue
        ret.append(wrd)
    return ret



spkr2id_dict = dict()
def spkr2id(spkr):
    global spkr2id_dict
    if spkr in spkr2id_dict:
        pass
    else:
        raw_id = str(len(spkr2id_dict) + 1)
        final_id = '0' * (5 - len(raw_id)) + raw_id
        spkr2id_dict[spkr] = final_id
    return spkr2id_dict[spkr]

def parse_ctm(ctm_fn):
    ctm_fi = open(ctm_fn, 'r')
    raw_content = ctm_fi.readlines()
    ctm_fi.close()
    
    ret = list()

    for line in raw_content:
        line = line.strip().upper()
        if line.startswith(';;'):
            continue
        if 'EXCLUDED_REGION' in line or 'INTER_SEGMENT_GAP' in line or 'IGNORE_TIME_SEGMENT_IN_SCORING' in line:
            continue
        vals = re.split('\s+', line)
        token = vals[0]
        spkr_id = spkr2id(vals[2])
        ssta = str(int(float(vals[3]) * 100))
        send = str(int(float(vals[4]) * 100))
        wrds = purge_wrd_lst(vals[6:])
        ret.append([token, ssta, send, wrds, spkr_id])

    return ret


def parse_convmap(convmap_fn):
    fp = open(convmap_fn, 'r')
    raw_content = fp.readlines()
    fp.close()

    ret = dict()
    for line in raw_content:
        frm, to = line.strip().split(' ')
        ret[frm] = to
    return ret
    


def gen_scpmlf(ctm, convmap, fea_base, out_scp, out_mlf):
    scp_fp = open(out_scp, 'w')
    mlf_fp = open(out_mlf, 'w')
    mlf_fp.write('#!MLF!#\n')
    for item in ctm:
        #scp
        raw_token = item[0]
        fn_token = convmap[raw_token]
        fn_token = fn_token[0:7] + item[-1] + fn_token[6:]
        raw_token = '+'.join(raw_token.split('_'))
        fn_useless = 'en_XXXXXXX'
        ssta = item[1]
        send = item[2]
        fn_ssta = '0' * (7 - len(ssta)) + ssta
        fn_send = '0' * (7 - len(send)) + send
        fn = '%s-%s_%s_%s' % (fn_token, fn_useless, fn_ssta, fn_send)
        item_scp = '%s.plp=%s/%s.plp[%s,%s]' % (fn, fea_base, raw_token, ssta, send)
        scp_fp.write(item_scp + '\n')

        #mlf
        #mlf start
        mlf_fp.write('"*/%s.lab"\n' % (fn))
        
        wrds = item[3]

        for wrd in wrds:
            mlf_fp.write(wrd + '\n')

        #mlf end
        mlf_fp.write('.\n')


    scp_fp.close()
    mlf_fp.close()


convmap = parse_convmap(convmap_fn)
ctm = parse_ctm(ctm_fn)

gen_scpmlf(ctm, convmap, fea_base, 'oracle.scp', 'oracle.mlf')
print spkr2id_dict
