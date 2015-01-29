function [ out_mat ] = func_block_diag_mat( in_mat, num_basis )


out_mat = zeros(size(in_mat) * num_basis);

for i = 0 : num_basis - 1
    range1 = i*size(in_mat, 1) + 1 : (i + 1) * size(in_mat, 1);
    range2 = i*size(in_mat, 2) + 1 : (i + 1) * size(in_mat, 2);
    out_mat(range1, range2) = in_mat;
end

end

