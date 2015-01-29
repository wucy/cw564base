#! /bin/bash


MY_BASE=/home/mifs/cw564/base/
MY_LOCAL=${MY_BASE}/local/wsj/


EXT_SCP=/home/bluea/cw564/wsjcsr/WSJ0/exp/S3/mlptrain.gpu/lib/flists.hcopy/traincv.scp
EXT_MLF_INDEX=/home/bluea/cw564/wsjcsr/WSJ0/exp/S3/mlptrain.gpu/lib/mlabs/traincv.index.mlf
EXT_INIT_NN=/home/bluea/cw564/wsjcsr/WSJ0/exp/S3/mlptrain.gpu/mlp3.finetune/MLP

EXT_GENDER_INFO=/home/bluea/cw564/wsjcsr/WSJ0/convert/lib/gender/wsj0-spkr-info.txt.920128

# dir : 
mkdir in
mkdir out
mkdir temp
mkdir tool

# tool/gen_lambda.py :
ln -s ${MY_LOCAL}/python/init_lambda_from_gender.py tool/gen_lambda.py
# tool/gen_seg2spkr_map.py :
ln -s ${MY_LOCAL}/python/pfile_segid_to_spkrid_map.py tool/gen_seg2spkr_map.py

# in/gender.info :
ln -s ${EXT_GENDER_INFO} in/gender.info

# in/traincv.scp :
ln -s ${EXT_SCP} in/traincv.scp

# out/lambda.init : gen_lambda.py in/gender.info
python tool/gen_lambda.py in/gender.info out/lambda.init

# out/seg2spkr.map temp/seg2spkr.map.Py : in/traincv.scp
python tool/gen_seg2spkr_map.py in/traincv.scp out/seg2spkr.map temp/seg2spkr.map.Py

# tool/gen_labpfile.py : 
ln -s ${MY_BASE}/global/python/MLPeasyTools.py tool/gen_labpfile.py

# in/traincv.mlf : 
ln -s ${EXT_MLF_INDEX} in/traincv.mlf

# out/traincv_withspkrinfo_lab.pfile : temp/seg2spkr.map.Py in/traincv.mlf
python tool/gen_labpfile.py -qn-mlf2pfile-withspkr in/traincv.mlf 100000 4 out/traincv_withspkrinfo_lab.pfile temp/seg2spkr.map.Py

# modify_nn.m :
ln -s ${MY_LOCAL}/matlab/modify_nn.m tool/modify_nn.m

# in/INIT.nn : 
ln -sf ${EXT_INIT_NN} in/INIT.nn

# out/base2.nn : in/INIT.nn
/tools/apps/matlab/matlabR2011b/bin/matlab \
	-nodisplay \
	-r "addpath('${MY_LOCAL}/matlab/');addpath('./tool/');modify_nn('in/INIT.nn',2);quit;"
mv NN.MAT out/base2.nn

