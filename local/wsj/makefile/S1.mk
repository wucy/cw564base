MY_BASE = /home/mifs/cw564/base/
MY_LOCAL = $(MY_BASE)/local/wsj/


LOCAL_LAB_PFILE_WITHSPKRINFO = $(PWD)/../S0/traincv_withspkrinfo_lab.pfile
LOCAL_LAMBDA_INIT = $(PWD)/../S0/lambda.init
LOCAL_SEG2SPKR_MAP = $(PWD)/../S0/seg2spkr.map
LOCAL_INIT_NN = $(PWD)/../S0/DIAG.mat

EXT_FEA_PFILE = /home/bluea/cw564/wsjcsr/WSJ0/exp/S3/mlptrain.debug/data/pfile/traincv.pfile
EXT_TRN_BIN = /home/mifs/cw564/src/quicknet.mbt/qnmultitrn


.PHONY : setup
setup : lab.pfile fea.pfile marco run.tester qn.mbt.bin lambda.init seg2spkr.map

lab.pfile : 
	ln -sf $(LOCAL_LAB_PFILE_WITHSPKRINFO) $@

fea.pfile :
	ln -sf $(EXT_FEA_PFILE) $@

marco :
	mkdir -p marco/work
	ln -sf $(LOCAL_INIT_NN) marco/work/INIT

run.tester :
	ln -sf $(MY_LOCAL)/tester/my.mbt.gpu.run $@

qn.mbt.bin : 
	ln -sf $(EXT_TRN_BIN) $@

lambda.init :
	ln -sf $(LOCAL_LAMBDA_INIT) $@

seg2spkr.map :
	ln -sf $(LOCAL_SEG2SPKR_MAP) $@


.PHONY : clean
clean :
	rm -r marco
	rm lab.pfile fea.pfile run.tester qn.mbt.bin lambda.init seg2spkr.map
