%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% pKa calculation                           2024-04
% @author: Matilda J. Lindvall
%
% The program will calculate changes in chemical shift and plot it against
% pH. 
%
% The equation used for calculating changes in chemical shift is
% d = sqrt(0.5*(d_H^2 + (a*d_N)^2), description of the formula 
% can be found in the article 
% Williamson, M. P. (2013). Using chemical shift perturbation to 
% characterise ligand binding. Progress in Nuclear Magnetic Resonance 
% Spectroscopy, 73, 1-16. https://doi.org/10.1016/j.pnmrs.2013.02.001
% 
% The formula used for the fit is f(x) = d + (a-d)/(1 + (x/c)^b), 
% which has a sigmoidal shape
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clear

%Import data
T = readtable("pKa.xlsx"); 

dH = T.dH;
dN = T.dN;
pH = T.pH;
a = 0.14; %Alpha is set to 0.14

%Calculate the change in CS
dD = sqrt(0.5*((dH.^2)+(a*dN).^2)); 

y = dD; %Can change this one to see how dN and dH affect individually

%Fit the data
f = fit(pH,y,'logistic4');

%Calculate the derivative of the fitted curve
x = linspace(5,9,50);
f_dif = differentiate(f,x);
[max_f, idx] = max(f_dif);
pKa = round(x(idx),2);

%Plot
subplot(2,1,1)
plot(f,pH,y)
xlabel('pH')
ylabel('Chemical Shift')
subplot(2,1,2)
plot(x,f_dif,'m')
xlabel('pH')
legend('1st derivative')
txt =  ['pK_a: ' num2str(pKa)];
text(8,0.07,txt, "LineStyle","-")
grid on
