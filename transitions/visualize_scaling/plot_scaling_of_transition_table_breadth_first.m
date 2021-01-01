close all
clear
setenv("GNUTERM","qt")

% assumes three columns: step number, total length of snake, and number of trees

two=load('record_2x2_1.dat');
figure; hold on;
semilogy(two(:,1)./two(:,2),two(:,3),'DisplayName','2x2:1','marker','o','color','m')

three=load('record_3x3_1.dat');
semilogy(three(:,1)./three(:,2),three(:,3),'DisplayName','3x3:1','marker','o','color','g')

four=load('record_4x4_1.dat');
semilogy(four(:,1)./four(:,2),four(:,3),'DisplayName','4x4:1','marker','o','color','k')

five=load('record_5x5_1.dat');
semilogy(five(:,1)./five(:,2),five(:,3),'DisplayName','5x5:1','marker','s','color','r')

six=load('record_6x6_1.dat');
semilogy(six(:,1)./six(:,2),six(:,3),'DisplayName','6x6:1','marker','d','color','b')

seven=load('record_7x7_1.dat');
semilogy(seven(:,1)./seven(:,2),seven(:,3),'DisplayName','7x7:1','marker','d','color','m')

xlabel('normalized step number', "fontsize", 14)
ylabel('number of snakes', "fontsize", 14)

h=legend('show')
set(h, 'fontsize',14)


figure; hold on;
semilogy([2,3,4,5,6],[two(end,3),three(end,3),four(end,3),five(end,3),six(end,3)],'marker','o')
xlabel('grid width', 'fontsize',14)
ylabel('number of grid-filling snakes','fontsize',14)
