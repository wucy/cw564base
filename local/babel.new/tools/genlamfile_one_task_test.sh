#! /bin/tcsh

set MYBASE=$1
set MLP=$2
set NUMBASIS=$3
set LAM=$4
set SEGMAP=$5
set SSTA=$6
set SEND=$7
set MATFILE=$8



source htefiles/HTE.mbt

~/bin/qn.mbt.lamdatagen.new.4h \
    mbt_num_basis=${NUMBASIS} \
    mbt_init_lambda_file=${LAM} \
    mbt_out_lambda_file_prefix=${MATFILE} \
    mbt_seg2spkr_file=${SEGMAP} \
    ftr1_file=${MYBASE}/fea.pfile \
    ftr1_format=pfile \
    ftr1_width=${DATADIM} \
    ftr2_file= \
    ftr2_format=pfile \
    ftr2_width=0 \
    unary_file= \
    hardtarget_file=${MYBASE}/lab.pfile \
    hardtarget_format=pfile \
    ftr1_norm_file= \
    ftr2_norm_file= \
    ftr1_ftr_start=0 \
    ftr2_ftr_start=0 \
    ftr1_ftr_count=${DATADIM} \
    ftr2_ftr_count=0 \
    hardtarget_lastlab_reject=false \
    window_extent=9 \
    ftr1_window_offset=0 \
    ftr2_window_offset=4 \
    unary_window_offset=3 \
    hardtarget_window_offset=4 \
    ftr1_window_len=9 \
    ftr2_window_len=0 \
    ftr1_delta_order=0 \
    ftr1_delta_win=9 \
    ftr1_norm_mode= \
    ftr1_norm_alpha_m=0.005 \
    ftr1_norm_alpha_v=0.005 \
    ftr2_delta_order=0 \
    ftr2_delta_win=9 \
    ftr2_norm_mode=null \
    ftr2_norm_alpha_m=0.005 \
    ftr2_norm_alpha_v=0.005 \
    fwd_sent_range=${SSTA}:${SEND} \
    init_weight_file=$MLP \
    init_weight_format=matlab \
    unary_size=0 \
    mlp_size=${MLPSIZE} \
    mlp_output_type=softmax \
    mlp_bunch_size=800 \
    use_blas=false \
    use_pp=true   use_fe=false   use_cuda=false   mlp_threads=1   realtime=false   realtime_latency=64   activation_file=/dev/null   activation_format=pfile   log_file=${MYBASE}/QNLOG   verbose=false   debug=0   mlp_hidden_out_type=sigmoid   log_post=true   log_post_norm_file=decodeMLP/LogPriors   sun_path=socket   psd_llr_stats=true   psd_obsv_prior=-135   device_no=0   max_utter_len=5000
