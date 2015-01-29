#!/bin/bash

MY_BASE=/home/mifs/cw564/base/
MY_LOCAL=$MY_BASE/local/wsj/

LOCAL_LAB_PFILE_WITHSPKRINFO=$PWD/../prepare/out/traincv_withspkrinfo_lab.pfile
LOCAL_LAMBDA_INIT=$PWD/../prepare/out/lambda.init
LOCAL_SEG2SPKR_MAP=$PWD/../prepare/out/seg2spkr.map
LOCAL_INIT_NN=$PWD/../prepare/out/base2.nn

EXT_FEA_PFILE=/home/bluea/cw564/wsjcsr/WSJ0/exp/S3/mlptrain.gpu/data/pfile/traincv.pfile
EXT_TRN_BIN=/home/mifs/cw564/src/quicknet.mbt/qnmultitrn




mkdir in
mkdir temp
mkdir tool
mkdir out

# in/lab.pfile : 
ln -s $LOCAL_LAB_PFILE_WITHSPKRINFO in/lab.pfile

# in/fea.pfile :
ln -s $EXT_FEA_PFILE in/fea.pfile

# in/lambda.init :
ln -s $LOCAL_LAMBDA_INIT in/lambda.init

# in/seg2spkr.map :
ln -s $LOCAL_SEG2SPKR_MAP in/seg2spkr.map

# in/qn.mbt.bin :
ln -s $EXT_TRN_BIN tool/qn.mbt.bin

ln -s $MY_LOCAL/tester/my.mbt.gpu.run train.run

# temp/marco :
mkdir -p temp/marco/work
ln -s $LOCAL_INIT_NN temp/marco/work/INIT


