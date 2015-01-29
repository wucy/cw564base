function [ ]  = gen_split_basis( nn_fn, nn_out_prefix, num_basis )

rawmat = load(nn_fn, '-mat');

for i = 1 : num_basis    
    [rr, cc] = func_locate_block_mat(size(rawmat.weights12), i, num_basis);
    weights12 = rawmat.weights12(rr, cc);
    bias2 = rawmat.bias2(1, rr);
    
    [rr, cc] = func_locate_block_mat(size(rawmat.weights23), i, num_basis);
    weights23 = rawmat.weights23(rr, cc);
    bias3 = rawmat.bias3(1, rr);
    
    [rr, cc] = func_locate_block_mat(size(rawmat.weights34), i, num_basis);
    weights34 = rawmat.weights23(rr, cc);
    bias4 = rawmat.bias4(1, rr);
    
    weights45 = rawmat.weights45;
    bias5 = rawmat.bias5;
    
    save(strcat(nn_out_prefix, num2str(i)), 'weights12', 'bias2', 'weights23', 'bias3', 'weights34', 'bias4', 'weights45', 'bias5', '-v4');
    
end
