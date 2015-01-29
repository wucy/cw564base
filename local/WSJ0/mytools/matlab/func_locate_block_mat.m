function [ ret_rowrange, ret_colrange ] = func_locate_block_mat( raw_size, basis_id, num_basis )

new_row = raw_size(1) / num_basis;
new_col = raw_size(2) / num_basis;

ret_rowrange = new_row * (basis_id - 1) + 1 : new_row * basis_id;
ret_colrange = new_col * (basis_id - 1) + 1 : new_col * basis_id;
