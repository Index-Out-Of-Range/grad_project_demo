import os
import numpy
import scipy.io
import pymysql


def relation_to_db(kind, gene_id, first_and_second_idx, matrix, connection):
    if kind == 1:
        sql = 'INSERT INTO hmnmf_known_gp_relation (gene_id, gene_name, phenotype_id, phenotype_name, gp_known_relation) VALUES (%s, %s, %s, %s, %s)'
    elif kind == 2:
        sql = 'INSERT INTO hmnmf_predict_gp_relation (gene_id, gene_name, phenotype_id, phenotype_name, gp_predict_relation) VALUES (%s, %s, %s, %s, %s)'
    cursor = connection.cursor()
    (m, n) = matrix.shape
    phenotype_info = {}
    gene_info = {}
    with open('phenotype_info.txt', 'r') as f:
        for line in f.readlines():
            temp_dict = eval(line)
            phenotype_info[str(int(temp_dict['id']))] = temp_dict['name']
    with open('gene_info.txt', 'r') as f:
        for line in f.readlines():
            temp_dict = eval(line)
            gene_info[str(temp_dict['id'])] = temp_dict['official_full_name'][0]
    for i in range(m):
        single_gene_id = int(gene_id[i, 0])
        single_gene_name = gene_info[str(single_gene_id)]
        execute_arg = []
        for j in range(n):
            single_phenotype_id = int(first_and_second_idx[j, 0])
            single_phenotype_name = phenotype_info[str(single_phenotype_id)]
            gp_relation = round(float(matrix[i, j]), 6)
            # print((single_gene_id, single_gene_name, single_phenotype_id, single_phenotype_name, gp_relation))
            execute_arg.append((single_gene_id, single_gene_name, single_phenotype_id, single_phenotype_name, gp_relation))
        try:
            cursor.executemany(sql, execute_arg)
            connection.commit()
        except Exception as e:
            print(e)
            connection.rollback()
    print('关系矩阵成功插入到数据库！')


def get_result_file(path):
    # 可能文件夹下生成了多个结果文件，需要找到最新生成的那个结果
    fileNames = list(filter(lambda filename: os.path.splitext(filename)[1] == '.mat', os.listdir(path)))
    file_list = []
    for i in range(len(fileNames)):
        if fileNames[i].startswith('L21_CMNMF_result') != -1:
            file_list.append(fileNames[i])
    return file_list[-1]


if __name__ == '__main__':
    pathway_path = r"../../HMNMF_Codes/2_useful_data/pathway/pathway.mat"
    known_data = scipy.io.loadmat(pathway_path)
    first_and_second_idx = known_data['first_and_second_idx']
    gene_id = known_data['gene_id']
    g_p_network = known_data['g_p_network']

    path = '../../HMNMF_Codes/L21_CMNMF/old_result/pathway/'
    result_path = path + get_result_file(path)
    predict_data = scipy.io.loadmat(result_path)
    learned_matrix_cell = predict_data['learned_matrix_cell']
    G = learned_matrix_cell[0][1]
    P1 = learned_matrix_cell[0][2]
    P2 = learned_matrix_cell[0][3]
    R = numpy.concatenate((numpy.dot(G, P1), numpy.dot(G, P2)), axis=1)
    # R1 = numpy.dot(G, numpy.concatenate((P1, P2), axis=1))
    #
    # print(R.shape)
    # print(R1.shape)

    # temp_path = '../../HMNMF_Codes/L21_CMNMF/old_result/Pathway/result.mat'
    # scipy.io.savemat('../../HMNMF_Codes/L21_CMNMF/old_result/Pathway/result.mat', {'R': R, 'R1': R1})

    # connection = pymysql.connect(host='localhost', port=3306, user='root', password='dipo123', db='grad_project', charset='utf8')
    # # relation_to_db(1, gene_id, first_and_second_idx, g_p_network, connection)
    # relation_to_db(2, gene_id, first_and_second_idx, R, connection)
    #
    # connection.close()
