#! /usr/bin/env python


import os
import re
import sys



MLP = "decodeMLP/MLP.mbt"

TSET = sys.argv[1]

CONFIG = "mbt." + sys.argv[2]

NUM_BASIS = 2




lam_fn = 'lib/mbt/%s.lam.esti.%s' % (TSET, CONFIG.split('.')[1])


base = "test"


whereami = os.getcwd()
fea_pfile = '%s/data/pfile/%s.pfile' % (whereami, TSET)

tasks = open("lib/flists.test/%s.lst" % (TSET), 'r').readlines()




for task in tasks:
    task = task.strip()
    taskdir = '%s/%s/%s.1/decode.%s/' % (base, TSET, task, CONFIG)
    os.popen('mkdir -p ' + taskdir)
    #os.popen('mkdir -p %s/rescore/tg_11.0_0.0/lattices' % (taskdir))
    os.popen('ln -s %s %s/fea.pfile' % (fea_pfile, taskdir))

    segmap_fn = taskdir + '/segmap.fake'
    os.popen('echo "1" > %s ; echo "0 %s" >> %s' % (segmap_fn, task, segmap_fn))
    raw_content = re.split('\s+', os.popen('cat %s | grep %s' % (lam_fn, task)).readline())
    
    #rescale lm scale
    sumlam = 0
    print task
    for i in range(NUM_BASIS):
        sumlam += float(raw_content[i + 1].strip())
    
    new_scale = 11.0
    my_hte_lat = '%s/HTE.lat_decode' % (taskdir)
    precmd1 = 'cp htefiles/HTE.lat_decode %s' % (my_hte_lat)
    precmd2 = 'echo "\nset HVGSCALE = %f\n" >> %s' % (new_scale, my_hte_lat)
    os.popen(precmd1)
    os.popen(precmd2)

