function [ lambda_new ] = loglinear_GD_opt(lambda, W_t, b, feas_row, labs, num_basis, bunch_size, lr)


disp(size(labs) / 20);

if (size(labs) == 0)
    exit()
end

if (bunch_size == -1)
    bunch_size = size(feas_row, 1);
end

lambda_new = lambda;

fea_dim = size(feas_row, 2);

%disp(bunch_size);
%disp(fea_dim);

%bunch_size = 1;


%disp(size(W_t));

format long;

H = reshape(feas_row', fea_dim / num_basis, []);
zs = W_t * H;
zs = zs - max(max(zs));


[prev_cri, prev_acc] = loglinear_calc_criteria_opt_partial(lambda_new, zs, b, labs, num_basis);


for round = 1 : 100
    for id = 1 : (bunch_size / 20)
        WtHlpb = zs(:, (id * num_basis - 1) : (id * num_basis)) * lambda_new + b;
        expWtHlpb = exp(WtHlpb);
        WtH_t = zs(:, (id * num_basis - 1) : (id * num_basis))';
    
        Z = sum(expWtHlpb);

        expWtHlpb_Z = expWtHlpb / Z;
        cp_expWtHlpb_Z = repmat(expWtHlpb_Z, 1, num_basis)';
        whole = sum(cp_expWtHlpb_Z .* WtH_t, 2);
        whole = whole - WtH_t(:, labs(id));

        lambda_new = lambda_new - lr * whole;
    end
    
    disp('iter=');
    disp(round);
    disp('lambda=');
    disp(lambda_new');
    [cri, acc] = loglinear_calc_criteria_opt(lambda_new, zs, b, labs, num_basis);
    if abs(prev_cri - cri) < 0.01
        break;
    end
    prev_cri = cri;
    prev_acc = acc;
end


disp('final_lambda=');
disp(lambda_new');
