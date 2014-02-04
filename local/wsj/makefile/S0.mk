MY_BASE = /home/mifs/cw564/base/
MY_LOCAL = ${MY_BASE}/local/wsj/

EXT_SEG2SPKR_MAP_PY = /home/bluea/cw564/wsjcsr/WSJ0/enigma/lambda/S0/seg2spkr.map.Py
EXT_MLF_INDEX = /home/bluea/cw564/wsjcsr/WSJ0/exp/S3/mlptrain.debug/lib/mlabs/traincv.index.mlf
EXT_GENDER_INFO = /home/bluea/cw564/wsjcsr/WSJ0/res/wsj0-spkr-info.txt.920128
EXT_SCP = /home/bluea/cw564/wsjcsr/WSJ0/exp/S3/mlptrain.debug/lib/flists.hcopy/traincv.scp



.PHONY : run
run : lambda.init seg2spkr.map traincv_withspkrinfo_lab.pfile


gen_lambda.py :
	ln -sf ${MY_LOCAL}/python/init_lambda_from_gender.py $@

gen_seg2spkr_map.py :
	ln -sf ${MY_LOCAL}/python/pfile_segid_to_spkrid_map.py $@

gender.info :
	ln -sf ${EXT_GENDER_INFO} $@

traincv.scp :
	ln -sf ${EXT_SCP} $@

lambda.init : gen_lambda.py gender.info
	python gen_lambda.py gender.info $@

seg2spkr.map : gen_seg2spkr_map.py traincv.scp
	python gen_seg2spkr_map.py traincv.scp $@ $@.Py

seg2spkr.map.Py : seg2spkr.map

gen_seg2spkr.py : 
	ln -sf ${MY_BASE}/global/python/MLPeasyTools.py $@

traincv.mlf : 
	ln -sf ${EXT_MLF_INDEX} $@

traincv_withspkrinfo_lab.pfile : gen_seg2spkr.py seg2spkr.map.Py traincv.mlf
	python gen_seg2spkr.py -qn-mlf2pfile-withspkr \
		traincv.mlf 100000 4 $@ seg2spkr.map.Py


.PHONY : clean
clean :
	rm gen_lambda.py gen_seg2spkr_map.py gender.info traincv.scp lambda.init seg2spkr.map \
		seg2spkr.map.Py gen_seg2spkr.py traincv.mlf traincv_withspkrinfo_lab.pfile

