function [] = delete_hierarchy()
dataset='yahoomusic';
load([dataset '.mat'],'M');
relation_num=nnz(M);
index=find(M);
del_index1=randperm(floor(0.2*relation_num));
del_index2=randperm(floor(0.4*relation_num));
del_index3=randperm(floor(0.6*relation_num));
del_index4=randperm(floor(0.8*relation_num));
M1=M;
M1(index(del_index1))=0;
M2=M;
M2(index(del_index2))=0;
M3=M;
M3(index(del_index3))=0;
M4=M;
M4(index(del_index4))=0;
M5=zeros(size(M));
save([dataset '.mat'],'M1','M2','M3','M4','M5','-append');
end

