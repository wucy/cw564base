#!/bin/tcsh
# set verbose

set DIR=finalMLP/work

set APPEND=.1em4

mkdir -p $DIR

source htefiles/HTE.mbt

~/bin/qnmultitrn.mbt.gpu.4h \
  ftr1_file=data/pfile/traincv.pfile \
  ftr1_format=pfile \
  ftr1_width=${DATADIM} \
  ftr2_file= \
  ftr2_format=pfile \
  ftr2_width=0 \
  unary_file= \
  hardtarget_file=data/pfile/traincv_lab_spkr.pfile \
  hardtarget_format=pfile \
  softtarget_file= \
  softtarget_format=pfile \
  softtarget_width=0 \
  ftr1_norm_file= \
  ftr2_norm_file= \
  ftr1_ftr_start=0 \
  ftr2_ftr_start=0 \
  ftr1_ftr_count=${DATADIM} \
  ftr2_ftr_count=0 \
  hardtarget_lastlab_reject=true \
  window_extent=9 \
  ftr1_window_offset=0 \
  ftr2_window_offset=4 \
  unary_window_offset=3 \
  hardtarget_window_offset=4 \
  softtarget_window_offset=0 \
  ftr1_window_len=9 \
  ftr2_window_len=0 \
  ftr1_delta_order=0 \
  ftr1_delta_win=9 \
  ftr1_norm_mode=file \
  ftr1_norm_alpha_m=0.005 \
  ftr1_norm_alpha_v=0.005 \
  ftr2_delta_order=0 \
  ftr2_delta_win=9 \
  ftr2_norm_mode=null \
  ftr2_norm_alpha_m=0.005 \
  ftr2_norm_alpha_v=0.005 \
  train_cache_frames=58442400 \
  train_cache_seed=0 \
  train_sent_range=${TRNSTA}:${TRNEND} \
  cv_sent_range=${CVSTA}:${CVEND} \
  init_random_bias_min=-4.1 \
  init_random_bias_max=-3.9 \
  init_random_weight_min=-0.1 \
  init_random_weight_max=0.1 \
  init_random_seed=0 \
  init_weight_file=INIT \
  init_weight_format=matlab \
  log_weight_file=${DIR}/LogMLP${APPEND} \
  log_weight_format=matlab \
  ckpt_weight_file=${DIR}/MLP_ckpt_%t${APPEND} \
  ckpt_weight_format=matlab \
  ckpt_hours=1 \
  out_weight_file=${DIR}/MLP${APPEND} \
  out_weight_format=matlab \
  learnrate_schedule=list \
  learnrate_vals=0.0001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01 \
  learnrate_epochs=1 \
  learnrate_scale=0.5 \
  unary_size=0 \
  mlp_size=$MLPSIZE \
  mlp_lrmultiplier=1 \
  mlp_output_type=softmax \
  mlp_bunch_size=800 \
  use_blas=false \
  use_pp=true \
  use_fe=false \
  use_cuda=true \
  mlp_threads=1 \
  log_file=${DIR}/LOG${APPEND} \
  verbose=false \
  debug=0 \
  a_min_derror_ramp_start=0.01 \
  a_min_derror_stop=0.05 \
  min_iter_num=100 \
  a_alpha_momentum=0 \
  mlp_hidden_type=sigmoid \
  backprop_criterion=xentropy \
  random_init_type=normal \
  device_no=0 \
  map_file_path= \
  map_opt= \
  lr_ctr=cv \
  bp_num_layer=-1 \
  env_var4dev_id=X_SGE_CUDA_DEVICE \
  weight_decay_factor=0 \
  mbt_num_basis=${NUMBASIS} \
  mbt_init_lambda_file=traincv.lam \
  mbt_out_lambda_file_prefix=${DIR}/lambda.out. \
  mbt_seg2spkr_file=lib/mbt/traincv.segmap

