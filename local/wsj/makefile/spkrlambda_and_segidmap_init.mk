MY_BASE = /home/mifs/cw564/base/
MY_LOCAL = ${MY_BASE}/local/wsj/


EXT_GENDER_INFO = /home/bluea/cw564/wsjcsr/WSJ0/res/wsj0-spkr-info.txt.920128
EXT_SCP = /home/bluea/cw564/wsjcsr/WSJ0/exp/S3/mlptrain.gpu/lib/flists.hcopy/traincv.scp

DIM = 8


.PHONY : run
run : lambda.init pfile_segid.map


gen_lambda.py :
	ln -sf ${MY_LOCAL}/python/init_lambda_from_gender.py $@

gen_segid_map.py :
	ln -sf ${MY_LOCAL}/python/pfile_segid_to_spkrid_map.py $@

gender.info :
	ln -sf ${EXT_GENDER_INFO} $@

flist.scp :
	ln -sf ${EXT_SCP} $@


lambda.init : gen_lambda.py gender.info
	python gen_lambda.py gender.info $@

pfile_segid.map : gen_segid_map.py flist.scp
	python gen_segid_map.py flist.scp $@


.PHONY : clean
clean :
	rm gen_lambda.py gender.info flist.scp lambda.init pfile_segid.map

