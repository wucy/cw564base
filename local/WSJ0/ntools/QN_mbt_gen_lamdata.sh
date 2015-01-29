#!/bin/tcsh

if ( $#argv > 1 ) then
   set HTEDIR = `mktemp -d`
   base/tools/parse2hte $HTEDIR/HTE "$argv"
   while (`echo "$argv[1]" | awk '{print(substr($1,1,1))}'` == "-")
      shift argv
      shift argv
   end
endif

if ( $# != 2 ) then
    echo "Usage: $0 env fea_out_dir"
    exit 1
endif

set MLPENV=$1
set FEA_OUT_DIR=$2

# set default values for training arguments
set ACCELERATE = "cuda"
set THREADNUM  = 1
set CTXFRAME   = 9
set DATADIM    = 52
set LOGPATH    = LOG.mbt.gen_lamdata
set LRBOB_RAMP = 0.05
set LRBOB_STOP = 0.5
set LRTYPE     = "list"
set LRVALS     = 0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001
set BUNCHSIZE  = 800
set MINITERNUM = 8
set MAXITERNUM = 20
set QNMULTRN   = "qnmultitrn_dnn"
set LOGNAME    = "LOG"
set MLPOTYPE   = "softmax"
set MLPHTYPE   = "sigmoid"

set SGN_CUDA   = "true"
set SGN_BLAS   = "false"

# Read the environment file
if ( ! -f $MLPENV ) then
   echo "cannot find environment file $MLPENV"
   exit 1
endif
source $MLPENV

if ($?HTEDIR) then
    source $HTEDIR/HTE
endif


set MLPDIR=workMLP

# Define the file to log all output/errors to
if (! -d $MLPDIR) then
    mkdir -p $MLPDIR
endif



# Copy the test HTE file as a record
cp $MLPENV $MLPDIR/HTE
if ($?HTEDIR) then
    cp  $HTEDIR/HTE $MLPDIR/HTE.cmdline
    rm -r $HTEDIR
endif

if (! $?INITWGTS) then
    set INITWGTS
endif

# Check that everything is included in the environment file
if ( (! $?MLPDATA) || (! $?MLPLABEL) || (! $?MLPSIZE) || (! $?TRNSTA) || (! $?TRNEND) || (! $?CVSTA) || (! $?CVEND) || (! $?MBTSEGMAP) || (! $?MBTLAM) || (! $?MBTNUMBASIS) )  then
    echo "Missing information from ENV file - need: MLPDATA MLPLABEL MLPSIZE TRNSTA TRNEND CVSTA CVEND MBTSEGMAP MBTLAM MBTNUMBASIS"
    exit 1
endif

#set ACCELERATE = "none"

@ WINEXT = 2 * $CTXFRAME + 1
if ($ACCELERATE == "blas") then
    set SGN_BLAS = "true"
    set SGN_CUDA = "false"
else if ($ACCELERATE == "none") then
    set SGN_BLAS = "false"
    set SGN_CUDA = "false"
endif

if (! -d ${MLPDIR}/work) then
    mkdir -p ${MLPDIR}/work
endif

set QNLAMDATAGEN = ./base/local/bin/qn.mbt.lamdatagen.gpu.3h

${QNLAMDATAGEN} \
        ftr1_file=${MLPDATA} \
        ftr1_format=pfile \
        ftr1_width=${DATADIM} \
        ftr2_file= \
        ftr2_format=pfile \
        ftr2_width=0 \
        unary_file= \
        hardtarget_file=${MLPLABEL} \
        hardtarget_lastlab_reject=true \
        hardtarget_format=pfile \
        softtarget_file= \
        softtarget_format=pfile \
        softtarget_width=0 \
        ftr1_norm_file= \
        ftr1_norm_mode=file \
        ftr2_norm_file= \
        ftr1_ftr_start=0 \
        ftr2_ftr_start=0 \
        ftr1_ftr_count=${DATADIM} \
        ftr2_ftr_count=0 \
        window_extent=${WINEXT} \
        hardtarget_window_offset=${CTXFRAME} \
        softtarget_window_offset=0 \
        ftr1_window_len=${WINEXT} \
        ftr2_window_len=0 \
        ftr1_delta_order=0 \
        ftr1_delta_win=9 \
        ftr2_delta_order=0 \
        ftr2_delta_win=9 \
        train_cache_frames=${CACHEFNUM} \
        train_cache_seed=0 \
        train_sent_range=${TRNSTA}:${TRNEND} \
        cv_sent_range=${CVSTA}:${CVEND} \
        init_random_bias_min=-4.1 \
        init_random_bias_max=-3.9 \
        init_random_weight_min=-0.1 \
        init_random_weight_max=0.1 \
        init_random_seed=0 \
        init_weight_file=${INITWGTS} \
	log_weight_file=${MLPDIR}/LogMLP \
        out_weight_file=${MLPDIR}/MLP \
        learnrate_schedule=${LRTYPE} \
        learnrate_vals=${LRVALS} \
        learnrate_epochs=${MAXITERNUM} \
        learnrate_scale=0.5 \
        a_min_derror_ramp_start=${LRBOB_RAMP} \
	a_min_derror_stop=${LRBOB_STOP} \
	min_iter_num=${MINITERNUM} \
	unary_size=0 \
        ckpt_weight_file=${MLPDIR}/work/MLP_ckpt_%t \
        ckpt_hours=1 \
        mlp_size=${MLPSIZE} \
        mlp_output_type=${MLPOTYPE} \
        mlp_bunch_size=${BUNCHSIZE} \
        mlp_threads=${THREADNUM} \
        log_file=${MLPDIR}/${LOGNAME} \
        verbose=false \
        use_cuda=${SGN_CUDA} \
	use_blas=${SGN_BLAS} \
	debug=0\
    mbt_num_basis=${MBTNUMBASIS} \
    mbt_init_lambda_file=${MBTLAM} \
    mbt_seg2spkr_file=${MBTSEGMAP}

