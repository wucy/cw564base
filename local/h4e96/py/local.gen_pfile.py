#! /usr/bin/env python

import os


prefix = 'tunelam/dev03'

spkr_lst = os.popen('ls tunelam/dev03/')
for spkr in spkr_lst:
    spkr = spkr.strip()
    print spkr
    mlf = prefix + '/' + spkr + '/MLF'
    mlf_new = prefix + '/' + spkr + '/MLF.new'
    scp = prefix + '/' + spkr + '/SCP'
    out_fea = prefix + '/' + spkr + '/fea.pfile'
    out_lab = prefix + '/' + spkr + '/lab.pfile'


    map = prefix + '/' + spkr + '/segmap'
    map_py = prefix + '/' + spkr + '/segmap.py'


    feacat_cmd = 'base/nbin/feacat -padframes 4 -ipformat htk -o ' + out_fea + ' -lists ' + scp
    map_cmd = 'base/local/py/pfile_segid_to_spkrid_map.lambda.py ' + scp + ' ' + map + ' ' + map_py
    final_cmd = 'base/local/tools/local.mlf2pfile cdstate 4 mono ' + mlf + ' ' + mlf_new +' ' + map + ' ' + out_lab
    print feacat_cmd
    print map_cmd
    print final_cmd
    #os.system(feacat_cmd)
    #os.system(map_cmd)
    #os.system(final_cmd)

    tot = int(os.popen('wc -l ' + scp).readline().split(' ')[0])
    sta = 0
    end = tot - 1
    nn_cmd = './base/local/ntools/mbt.gpu.gen.lambdadata.run ' + spkr + ' ' + str(sta) + ' ' + str(end) + ' ' + 'dev03'
    print nn_cmd
    #os.system(nn_cmd)


    #for decoding
    raw_scp = 'lib/flists.test/dev03_' + spkr + '.scp'
    out_raw_fea = prefix + '/' + spkr + '/fea.raw.pfile'
    feacat_raw_cmd = 'base/nbin/feacat -padframes 4 -ipformat htk -o ' + out_raw_fea + ' -lists ' + raw_scp
    print feacat_raw_cmd
    os.system(feacat_raw_cmd)


