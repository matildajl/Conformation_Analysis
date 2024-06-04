%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Kd calculation slow exchange                     2024-04
% @author: Matilda J. Lindvall
%
% The program will try different values of Kd and plot the value that gave
% the smallest error (SSE) for each amino acid.
%
% Initial steps have been done to the input data, normalized and adjusted. 
% The adjusting step was that the experimental value of fraction bound 
% protein (f(b)) was calculated by taking f(b)=1-f(f)=1-I(f)/I(fstart). 
%
% The equation used for predicting the fraction bound protein is 
% fb = 0.5*(M+1+(k/P)-((M+1+k/P).^2-4*M).^0.5), description of the formula 
% can be found in the article 
% Matei E, Basu R, Furey W, Shi J, Calnan C, Aiken C, Gronenborn AM. (2016) 
% Structure and Glycan Binding of a New Cyanovirin-N Homolog. The Journal 
% of Biological Chemistry 291: 18967–18976. 
% https://doi.org/10.1074/jbc.M116.740415
%
% To calculate sum square error (SSE) this formula was used
% SSE = sum((pred_y-exp_y).^2)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clear

%Import data that is normalized and adjusted
T = readtable("input_data.xlsx");

width_T = width(T);
T_adj = T(:, 2:width_T);

x = T.ratio; %x is the ratio of protein:ligand

K_d = linspace(0,399,400); %The Kd interval

errList = zeros(length(K_d), length(width(T_adj)));

%Calculate SSE for each Kd and save the error in a list
for j = 1:length(K_d)
    K = K_d(j);

    for i = 1:width(T_adj)
        y = T_adj{:,i};
        errList(j, i) = SSE(x, y, K);
    end

end

%Creates a plot with the smallest SSE for each amino acid
for aa = 1:width(T_adj)
    [minSSE, idx] = min(errList(:,aa));
    Kd_est = K_d(idx);

    figure(aa)
    x_plot = linspace(0,4.5,100);
    y_pred = CalcY(x_plot,Kd_est);
    y = T_adj{:,aa};

    plot(x, y, 'ko', 'MarkerFaceColor','k');
    title(T_adj.Properties.VariableNames{aa})
    hold on
    plot(x_plot, y_pred)
    legend('Exp. data', 'Prediction', 'Location', 'southeast')
    xlabel('Molar ratio')
    ylabel('Ib/Ibmax')
    xlim([0 x(end)+0.5])
    dim = [.68 .1 .3 .3];
    str = {['Kd: ' num2str(round(Kd_est)) ' uM'],... 
           ['SSE: ' num2str(round(minSSE,3))]};
    annotation('textbox',dim,'String',str,'FitBoxToText','on');
end 


%%
%Functions

%Predict the bound fraction (f), k=Kd
function f = CalcY(x, k)
    M = x; %Molar ratio sugar/protein
    P = 107; %[P] uM
    f = 0.5*(M+1+(k/P)-((M+1+k/P).^2-4*M).^0.5);
end

%Calculate sum square error, k=Kd
function err = SSE(x, y, k)
    pred = CalcY(x, k);
    err = sum((pred-y).^2);
end

