function [ lambda_new ] = loglinear_GD(lambda, W_t, b, feas_row, labs, num_basis, bunch_size, lr)


disp(size(labs));

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

[prev_cri, prev_acc] = loglinear_calc_criteria(lambda_new, W_t, b, feas_row, labs, num_basis);
disp('[criteria, accuracy]=');
disp([prev_cri, prev_acc]);


for round = 1 : 1
    %delta = zeros(size(lambda));
    for id = 1 : bunch_size
        H = reshape(feas_row(id, :), fea_dim / num_basis, num_basis);
        WtH = W_t * H;
        WtHlpb = WtH * lambda_new + b;
        WtHlpbmmax = WtHlpb - max(WtHlpb);
        expWtHlpb = exp(WtHlpbmmax);
        WtH_t = WtH';
        
        Z = sum(expWtHlpb);
        
        expWtHlpb_Z = expWtHlpb / Z;
        
        
        cp_expWtHlpb_Z = repmat(expWtHlpb_Z, 1, num_basis)';
        
        whole = sum(cp_expWtHlpb_Z .* WtH_t, num_basis);
        
        whole = whole - WtH_t(:, labs(id));
        %delta = delta + whole;
        lambda_new = lambda_new - lr * whole / bunch_size;
    end
    
    %lambda_new = lambda_new - lr * delta / bunch_size;
    disp('iter=');
    disp(round);
    disp('lambda=');
    disp(lambda_new');
    [cri, acc] = loglinear_calc_criteria(lambda_new, W_t, b, feas_row, labs, num_basis);
    disp('[criteria, accuracy]=');
    disp([cri, acc]);
    if abs(cri - prev_cri) < 0.001
        break
    end
    prev_cri = cri;
    prev_acc = acc;
end

%disp(final_lambda);
%lambda_new = final_lambda;

disp('final_lambda=');
disp(lambda_new');
