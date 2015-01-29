#! /usr/bin/env python


import os
import sys
import re



LMS = 11.0



TSET = sys.argv[1]
MLP = sys.argv[2]
CONFIG = sys.argv[3]
NUM_BASIS = sys.argv[4]
LAMFILE = sys.argv[5]
MY = sys.argv[6]



raw_lam = os.popen('cat %s | grep %s' % (LAMFILE, MY)).readline()
split_lam = re.split('\s+', raw_lam)

sumlam = 0
for i in range(int(NUM_BASIS)):
    sumlam += float(split_lam[i + 1].strip())

lmscale = LMS * sumlam
lmscale = 11.0

base = 'test'
my_base = './%s/%s/%s.1/decode.%s/' % (base, TSET, MY, CONFIG)

segmap_fn = my_base + '/segmap.fake'

range_fn = 'lib/flists.test/%s.range' % (TSET)
raw_content = re.split(',', os.popen('cat %s | grep %s' % (range_fn, MY)).readline())
ssta = raw_content[1]
send = raw_content[2].strip()

socket = 'socket'

os.popen('rm %s/%s' % (my_base, socket))

fea_pfile = '%s/fea.pfile' % (my_base)
tmp_pfile = '%s/tmp.pfile' % (my_base)




qncmd = '"./base/local/ntools/QN_qnmultifwd.net.sh -TRNSTA %s -TRNEND %s -ACCELERATE none -THREADNUM 1 htefiles/HTE.mbt decodeMLP %s %s %s %s %s %s %s"' % (ssta, send, fea_pfile, tmp_pfile, my_base, socket, segmap_fn, LAMFILE, NUM_BASIS)

hte = '%s/HTE.lat_decode' % (my_base)


hdecmd = '"sleep 0.1;./base/dtools/htest-hybrid -HVBIN ./base/bin/HDecode.hybrid %s %s %s decode.%s %s"' % (hte, TSET, MY, CONFIG, socket)

viterbi_cmd = 'python base/tools/MultiThreadInterface.py %s %s' % (qncmd, hdecmd)

print viterbi_cmd

os.system(viterbi_cmd)






hlr_base = my_base + '/rescore/tg_11.0_0.0/'
os.system('mkdir %s' % (hlr_base))

hlr_out_mlf = '%s/%s_%s.mlf' % (hlr_base, TSET, MY)
hlr_lat = hlr_base + '/lattices'


os.system('mkdir %s/flists' % (hlr_base))
hlr_lat_scp = hlr_base + '/flists/%s_lattices.scp' % (MY)
os.system('ls %s/lattices/* | sed \'s/\.gz//g\' > %s' %(my_base, hlr_lat_scp))

hlr_log = hlr_base + '/LOG'

hlr_cmd = 'base/bin/HLRescore -A -D -V -C base/lib/cfgs/hlrescore.cfg -L %s/lattices -T 1 -t 300.0 300.0 -s %f -p 0.0 -n lib/lms/tg_train.lm -f -i %s -w -l %s -C lib/cfgs/local.cfg -S %s lib/dicts/test.lv.dct > %s' % (my_base, lmscale, hlr_out_mlf, hlr_lat, hlr_lat_scp, hlr_log)


print hlr_cmd


os.system(hlr_cmd)

cn_base = my_base + '/rescore/tg_11.0_0.0_cn/'
cn_lat = cn_base + '/lattices/'

os.system('mkdir %s' % (cn_base))
os.system('mkdir %s/flists' % (cn_base))
os.system('mkdir %s' % (cn_lat))

cn_out_mlf = '%s/%s_%s.mlf' % (cn_base, TSET, MY)

cn_lat_scp = cn_base + '/flists/%s_lattices.scp' % (MY)
os.system('ls %s/lattices/* | sed \'s/\.gz//g\' > %s' %(hlr_base, cn_lat_scp))

cn_log = cn_base + '/LOG'

cn_cmd = 'base/bin/HLConf -A -D -V -i %s -C base/lib/cfgs/hlconf.cfg -T 1 -a %f -s 1.0 -r 1.0 -r 1.0 -p 0.0 -z -Z -l %s -C lib/cfgs/local.cfg -S %s lib/dicts/test.lv.dct > %s' % (cn_out_mlf, 1 / lmscale, cn_lat, cn_lat_scp, cn_log)


print cn_cmd

os.system(cn_cmd)



