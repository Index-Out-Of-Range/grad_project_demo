function [] = add_noise()
file_name='doubanbook.mat';
load(file_name);
if max(g_p_network(:))>1
    flag=1;
else
    flag=0.01;
end

non_zero_idx_first=find(g_p_network_first>0);
non_zero_count_first=length(non_zero_idx_first);
zero_idx_first=find(g_p_network_first==0);
zero_count_first=length(zero_idx_first);
non_zero_idx_second=find(g_p_network_second>0);
non_zero_count_second=length(non_zero_idx_second);
zero_idx_second=find(g_p_network_second==0);
zero_count_second=length(zero_idx_second);

del_idx_first1=non_zero_idx_first(randperm(non_zero_count_first,ceil(0.1*non_zero_count_first)));
del_idx_first2=non_zero_idx_first(randperm(non_zero_count_first,ceil(0.2*non_zero_count_first)));
add_idx_first1=zero_idx_first(randperm(zero_count_first,ceil(0.1*non_zero_count_first)));
add_idx_first2=zero_idx_first(randperm(zero_count_first,ceil(0.2*non_zero_count_first)));
del_idx_second1=non_zero_idx_second(randperm(non_zero_count_second,ceil(0.1*non_zero_count_second)));
del_idx_second2=non_zero_idx_second(randperm(non_zero_count_second,ceil(0.2*non_zero_count_second)));
add_idx_second1=zero_idx_second(randperm(zero_count_second,ceil(0.1*non_zero_count_second)));
add_idx_second2=zero_idx_second(randperm(zero_count_second,ceil(0.2*non_zero_count_second)));

g_p_network_first1=g_p_network_first;
g_p_network_first1(del_idx_first1)=0;
g_p_network_second1=g_p_network_second;
g_p_network_second1(del_idx_second1)=0;
g_p_network1=[g_p_network_first1,g_p_network_second1];

g_p_network_first2=g_p_network_first;
g_p_network_first2(del_idx_first2)=0;
g_p_network_second2=g_p_network_second;
g_p_network_second2(del_idx_second2)=0;
g_p_network2=[g_p_network_first2,g_p_network_second2];

g_p_network_first3=g_p_network_first;
g_p_network_first3(del_idx_first1)=0;
g_p_network_first3(add_idx_first1)=floor(rand()*5*flag)+1;
g_p_network_second3=g_p_network_second;
g_p_network_second3(del_idx_second1)=0;
g_p_network_second3(add_idx_second1)=floor(rand()*5*flag)+1;
g_p_network3=[g_p_network_first3,g_p_network_second3];

g_p_network_first4=g_p_network_first;
g_p_network_first4(del_idx_first2)=0;
g_p_network_first4(add_idx_first2)=floor(rand()*5*flag)+1;
g_p_network_second4=g_p_network_second;
g_p_network_second4(del_idx_second2)=0;
g_p_network_second4(add_idx_second2)=floor(rand()*5*flag)+1;
g_p_network4=[g_p_network_first4,g_p_network_second4];

save(file_name,'g_p_network_first1','g_p_network_second1','g_p_network1',...
    'g_p_network_first2','g_p_network_second2','g_p_network2',...
    'g_p_network_first3','g_p_network_second3','g_p_network3',...
    'g_p_network_first4','g_p_network_second4','g_p_network4')
end

