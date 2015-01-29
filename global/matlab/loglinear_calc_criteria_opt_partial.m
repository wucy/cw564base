function [ criteria, acc_rate ] = loglinear_calc_criteria_opt( lambda, zs, b, labs, num_basis )

criteria = 0;
acc_rate = 0;



total = size(zs, 2) / num_basis;

for id = 1 : total / 20
        WtHlpb = zs(:, (id * num_basis - 1) : (id * num_basis)) * lambda + b;
        expWtHlpb = exp(WtHlpb);

        Z = sum(expWtHlpb);
        expWtHlpb_Z = expWtHlpb / Z;

        criteria = criteria - log(expWtHlpb_Z(labs(id),:));
        [max_val, max_id] = max(expWtHlpb_Z);
        if max_id == labs(id)
            acc_rate = acc_rate + 1;
        end
end

acc_rate = acc_rate / total;

disp('[criteria, accuracy]=');
disp([criteria, acc_rate]);

end

