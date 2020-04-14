g_p_network_first_all=zeros(100,5);
g_p_network_second_all=zeros(100,10);
g_p_network_first=zeros(100,5);
g_p_network_second=zeros(100,10);
g_p_network_validation_first=zeros(100,5);
g_p_network_validation_second=zeros(100,10);
M=zeros(5,10);

for i=1:5
    one_idxs=randperm(100,10);
    g_p_network_first_all(one_idxs,i)=1;
    g_p_network_second_all(one_idxs(1:10),2*i-1)=1;
    g_p_network_second_all(one_idxs(1:10),2*i)=1;
    zero_idxs=find(g_p_network_second_all(:,2*i-1)==0);
    one_idx1=zero_idxs(randperm(5,1));
    one_idx2=zero_idxs(randperm(5,1));
    %g_p_network_second_all(one_idx1,2*i-1)=1;
    %g_p_network_second_all(one_idx2,2*i)=1;
    
    g_p_network_first(one_idxs(1:5),i)=1;
    g_p_network_second(one_idxs(6:10),2*i-1)=1;
    g_p_network_second(one_idxs(6:10),2*i)=1;
    %g_p_network_first(one_idxs(10),i)=1;
    %g_p_network_second(one_idx1,2*i-1)=1;
    %g_p_network_second(one_idx2,2*i)=1;
    g_p_network_validation_first(one_idxs(6:10),i)=1;
    g_p_network_validation_second(one_idxs(1:5),2*i-1)=1;
    g_p_network_validation_second(one_idxs(1:5),2*i)=1;
    
    M(i,(2*i-1):(2*i))=1;
end

g_p_network_first(:,1)=0;
g_p_network_second(:,1:2)=g_p_network_second_all(:,1:2);
g_p_network_second(:,8:10)=0;
g_p_network_second(:,7)=g_p_network_second_all(:,7);
g_p_network_first(:,4:5)=g_p_network_first_all(:,4:5);
g_p_network_validation_first(:,1)=g_p_network_first_all(:,1);
g_p_network_validation_second(:,1:2)=0;
g_p_network_validation_second(:,8:10)=g_p_network_second_all(:,8:10);
g_p_network_validation_second(:,7)=0;
g_p_network_validation_first(:,4:5)=0;

g_p_network_validation_first(g_p_network_first==1)=-1;
g_p_network_validation_second(g_p_network_second==1)=-1;

g_p_network=[g_p_network_first,g_p_network_second];
g_p_network_validation=[g_p_network_validation_first,g_p_network_validation_second];

indicator_first=g_p_network_first;
indicator_second=g_p_network_second;
indicator=g_p_network;

save('toy_dataset.mat','g_p_network','g_p_network_first','g_p_network_second','g_p_network_validation',...
'g_p_network_validation_first','g_p_network_validation_second','indicator','indicator_first','indicator_second','M');
