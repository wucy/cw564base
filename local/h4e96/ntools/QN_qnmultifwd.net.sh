#!/bin/tcsh
# set verbose

# code to generate commandline HTE for options
set ALLARGS=($*)
set cmdline
if ( $#argv > 1 ) then
   set HTEDIR = `mktemp -d`
   base/tools/parse2hte $HTEDIR/HTE "$argv"
   while (`echo "$argv[1]" | awk '{print(substr($1,1,1))}'` == "-" )
      shift argv
      shift argv
   end
endif

if ( $# != 9 ) then
    echo "Usage: $0 env mlp-dir pfile-in pfile-out workingdir socketname segmap lambda_file num_basis"
    exit 1
endif

set MLPENV=$1
set MLPDIR=$2
set IPFILE=$3
set OPFILE=$4
set BASEDIR=$5
set SOCKNAME=$6
set SEGMAP=$7
set LAMBDA=$8
set NUMBASIS=$9

if (! -d CMDs) mkdir CMDs
set TRAINSET=QN_qnmultifwd
echo "------------------------------------" >> CMDs/${TRAINSET}.cmds
echo "$0 $ALLARGS" >> CMDs/${TRAINSET}.cmds
echo "------------------------------------" >> CMDs/${TRAINSET}.cmds


# Read the environment file
if ( ! -f $MLPENV ) then
   echo "herest: cannot find environment file $1"
   exit 1
endif
source $MLPENV
if ($?HTEDIR) then 
    source $HTEDIR/HTE
endif

# Define the file to log all output/errors to
if (! -d $MLPDIR) then 
    echo "MLP $MLPDIR does not exist"
    exit 1
endif

if (! -d $BASEDIR) then 
    echo "Work dir $BASEDIR does not exist"
    exit 1
endif

# Copy the test HTE file as a record
cp $MLPENV $BASEDIR/HTE
if ($?HTEDIR) then
    cp  $HTEDIR/HTE $BASEDIR/HTE.cmdline
    rm -r $HTEDIR
endif

# Check that everything is included in the environment file
if ( (! $?MLPSIZE) || (! $?DATADIM) || (! $?TRNSTA) || (! $?TRNEND) )  then
    echo "Missing information from ENV file - need: MLPSIZE TRNEND"
    exit 1
endif



if (! $?QNMULFWD) then
#     set QNFWDTool = base/nbin/qnmultifwd_glibc5.net.CPU
     set QNFWDTool = ~/bin/qnmultifwd.mbt.cpu.5h
#     set QNFWDTool = ~/src/quicknet.mbt/qnmultifwd
#     set QNFWDTool = ~/code/quicknet-v3_40pre1-DNN.Hybrid/qnmultifwd
else
    set QNFWDTool = $QNMULFWD
endif

set UseCUDA = "false"
set UseBLAS = "false"

if (! $?MLPOTYPE) then
    set MLPOTYPE = "softmax"
endif

if (! $?MLPHTYPE) then
    set MLPHTYPE = "sigmoid"
endif

if (! $?OBSVPRIOR) then
    set OBSVPRIOR = -135.0
endif

if (! $?MAXUTTRLEN) then
    set MAXUTTRLEN = 5000
endif

@ WINEXT = 2 * $CTXFRAME + 1




${QNFWDTool} \
        ftr1_file=${IPFILE} \
        ftr1_format=pfile \
        ftr1_width=${DATADIM} \
        ftr2_file= \
        ftr2_format=pfile \
        ftr2_width=0 \
        unary_file= \
        ftr1_norm_file= \
        ftr1_norm_mode= \
        ftr2_norm_file= \
        ftr1_ftr_start=0 \
        ftr2_ftr_start=0 \
        ftr1_ftr_count=${DATADIM} \
        ftr2_ftr_count=0 \
        window_extent=${WINEXT} \
        hardtarget_window_offset=0 \
        ftr1_window_len=${WINEXT} \
        ftr2_window_len=0 \
        ftr1_delta_order=0 \
        ftr1_delta_win=9 \
        ftr2_delta_order=0 \
        ftr2_delta_win=9 \
        fwd_sent_range=${TRNSTA}:${TRNEND} \
        init_weight_file=${MLPDIR}/MLP.mbt \
        init_weight_format=matlab \
        unary_size=0 \
	mlp_size=${MLPSIZE} \
        mlp_output_type=${MLPOTYPE} \
        mlp_bunch_size=${BUNCHSIZE} \
        mlp_threads=${THREADNUM} \
        activation_file=${BASEDIR}/FAKEOUT.pfile \
	activation_format=pfile \
        log_file=${BASEDIR}/QNLOG \
	use_cuda=${UseCUDA} \
	use_blas=${UseBLAS} \
        log_post=true \
        log_post_norm_file=${MLPDIR}/LogPriors \
        sun_path=${BASEDIR}/${SOCKNAME} \
	psd_llr_stats=true \
	psd_obsv_prior=${OBSVPRIOR} \
	max_utter_len=${MAXUTTRLEN} \
	mlp_hidden_out_type=${MLPHTYPE} \
        verbose=FALSE \
        debug=0\
        mbt_init_lambda_file=${LAMBDA}\
        mbt_seg2spkr_file=${SEGMAP}\
        mbt_num_basis=${NUMBASIS}


