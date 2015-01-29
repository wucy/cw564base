function [ ] = modify_nn( in_nn_file, num_basis )
%in_nn_file = 'INIT.nn';
%num_basis = 2;

load(in_nn_file, '-mat');

%weights12 weights23 weights34 to be block-diag
%bias2 bias3 bias4 to be concat
% weights45 bias5 to be remined

weights12 = func_block_diag_mat(weights12, num_basis);
weights23 = func_block_diag_mat(weights23, num_basis);
weights34 = func_block_diag_mat(weights34, num_basis);


bias2 = repmat(bias2, [1, num_basis]);
bias3 = repmat(bias3, [1, num_basis]);
bias4 = repmat(bias4, [1, num_basis]);

save -v4 NN.MAT weights12 bias2 weights23 bias3 weights34 bias4 weights45 bias5


