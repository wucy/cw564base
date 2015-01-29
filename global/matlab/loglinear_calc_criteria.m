function [ criteria, acc_rate ] = loglinear_calc_criteria( lambda, W_t, b, feas_row, labs, num_basis )

criteria = 0;
acc_rate = 0;


fea_dim = size(feas_row, 2);

% % res = zeros(1, size(feas_row, 1) + 1);
% % res(size(feas_row, 1) + 1) = 1;
% 
% hist=zeros(3000, 1);
% 
% if_yes = zeros(size(feas_row, 1), 1);

for id = 1 : size(feas_row, 1)
        %if mod(id, 1000) == 0
        %    disp(id)
        %end
        H = reshape(feas_row(id, :), fea_dim / num_basis, num_basis);
        WtH = W_t * H;
        WtHlpb = WtH * lambda + b;
        WtHlpbmmax = WtHlpb - max(WtHlpb);
        expWtHlpb = exp(WtHlpbmmax);
        
        Z = sum(expWtHlpb);
        
        expWtHlpb_Z = expWtHlpb / Z;
        criteria = criteria - log(expWtHlpb_Z(labs(id),:)) / size(feas_row, 1);
        [max_val, max_id] = max(expWtHlpb_Z);
        if max_id == labs(id)
%             hist(max_id) = hist(max_id) + 1;
%             if_yes(id) = 1;
            acc_rate = acc_rate + 1;
        end
%         res(1, id) = expWtHlpb_Z(labs(id),:);
end

acc_rate = acc_rate / size(feas_row, 1);

%figure
%plot(1:size(res, 2), res);

%[vals, inds] = sort(hist);

%disp([inds, vals]);
%disp(sum(vals));

end

