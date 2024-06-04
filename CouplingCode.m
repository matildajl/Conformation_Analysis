%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Coupling constants                            2024-04
% @author: Matilda J. Lindvall
% 
% This program plots the coupling constants from the article
%
% Wenhui Zhang, Reagan Meredith, Qingfeng Pan, Xiaocong Wang, 
% Robert J. Woods, Ian Carmichael, and Anthony S. Serianni (2019) 
% Use of Circular Statistics To Model αMan-(1→2)-αMan and αMan-(1→3)-α/βMan 
% O-Glycosidic Linkage Conformation in 13C-Labeled Disaccharides and 
% High-Mannose Oligosaccharides, 
% Biochemistry 2019 58 (6), 546-560, DOI: 10.1021/acs.biochem.8b01050
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear

%M26 and M2 (1-2) linkage
%Phi
J_c2_c2 = @(phi) 2.05 + 0.47*cosd(phi) - 0.55*sind(phi) - ...
    0.86*cosd(2*phi) - 1.92*sind(2*phi);
J_c2_h1 = @(phi) 4.04 - 1.72*cosd(phi) + 0.18*sind(phi) + ...
    3.70*cosd(2*phi) - 0.91*sind(2*phi);

%Psi
J_c1_c3 = @(psi) 1.31 + 0.21*cosd(psi) + 0.64*sind(psi) - ...
    0.50*cosd(2*psi) + 1.54*sind(2*psi);
J_c1_h2 = @(psi) 4.04 - 1.72*cosd(psi) + 0.18*sind(psi) + ...
    3.70*cosd(2*psi) - 0.91*sind(2*psi);

figure(1)
fplot(@(phi) J_c2_c2(phi), [-180 180], 'r')
hold on
fplot(@(phi) J_c2_h1(phi), [-180 180], 'b')
grid on
ylim([-2 12])
xlabel('$\varphi$ (deg)', 'Interpreter','latex')
ylabel('Calculated ^3J_{xx}')
yline(3.6, 'r', 'LineStyle','--') %J=3.6
yline(4.0, 'b', 'LineStyle','--') %J=4.0
legend("^3J_{C2',C2}", "^3J_{C2,H1'}")

figure(2)
fplot(@(psi) J_c1_c3(psi), [-180 180], 'r')
hold on
fplot(@(psi) J_c1_h2(psi), [-180 180], 'b')
grid on
ylim([-2 12])
xlabel('\Psi (deg)')
ylabel('Calculated ^3J_{xx}')
yline(1.8, 'r', 'LineStyle','--') %J=1.8
yline(4.6, 'b', 'LineStyle','--') %J=4.6
legend("^3J_{C1',C3}", "^3J_{C1',H2}")