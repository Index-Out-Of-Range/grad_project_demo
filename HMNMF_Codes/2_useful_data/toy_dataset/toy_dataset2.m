clear;

g_p_network_first=zeros(20,5);
g_p_network_second=zeros(20,10);
g_p_network_validation_first=zeros(20,5);
g_p_network_validation_second=zeros(20,10);
M=zeros(5,10);

for i=1:5
    M(i,[2*i-1,2*i])=1;
end

g_p_network_first(1,1)=1;
g_p_network_second(3,[1,2])=1;
g_p_network_validation_first(3,1)=1;
g_p_network_validation_second(1,[1,2])=1;

g_p_network_second(5,3)=1;
g_p_network_second(7,4)=1;
g_p_network_validation_second(7,3)=1;
g_p_network_validation_second(5,4)=1;
g_p_network_validation_first([5,7],2)=1;

g_p_network_second([9,11],6)=1;
g_p_network_validation_first([9,11],3)=1;
g_p_network_validation_second([9,11],5)=1;

g_p_network_first(13,4)=1;
g_p_network_second(15,8)=1;
g_p_network_validation_first(15,4)=1;
g_p_network_validation_second(13,8)=1;
g_p_network_validation_second([13,15],7)=1;

g_p_network_first([17,19],5)=1;
g_p_network_validation_second([17,19],[9,10])=1;

g_p_network_validation_first(g_p_network_first==1)=-1;
g_p_network_validation_second(g_p_network_second==1)=-1;

g_p_network=[g_p_network_first,g_p_network_second];
g_p_network_validation=[g_p_network_validation_first,g_p_network_validation_second];

indicator_first=g_p_network_first;
indicator_second=g_p_network_second;
indicator=g_p_network;

save('toy_dataset.mat','g_p_network','g_p_network_first','g_p_network_second','g_p_network_validation',...
'g_p_network_validation_first','g_p_network_validation_second','indicator','indicator_first','indicator_second','M');

clear;
