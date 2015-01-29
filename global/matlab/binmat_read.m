function [ mat ] = binmat_read(filename, row_len )

fp = fopen(filename,'rb');

mat = zeros(5e5, row_len);

tot_row = 0;

while feof(fp) == 0
    [line, ele_cnt] = fread(fp, row_len, 'float32');
    if ele_cnt ~= row_len
        break;
    else
        line = line';
        tot_row = tot_row + 1;
        mat(tot_row, :) = line;
    end
end

mat = mat(1 : tot_row, :);
