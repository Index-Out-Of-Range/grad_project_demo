# HMNMF的算法保存在.mat文件中，我需要把结果保存到数据库里面去

import os
import time
import numpy
import scipy.io
import pymysql


# 把gene & phenotype信息插入到数据库
def gene_phenotype_to_result(gene_id, first_and_second_idx, connection):
    cursor = connection.cursor()
    gene_arg = []
    phenotype_arg = []
    for i in range(len(gene_id)):
        gene_arg.append((int(gene_id[i, 0])))
    try:
        cursor.executemany('INSERT INTO `hmnmf_gene` (`gene_name`) VALUES (%s)', gene_arg)
        connection.commit()
    except Exception as e:
        print(e)
        connection.rollback()
    print('GENE insert complete!')

    for i in range(len(first_and_second_idx)):
        phenotype_arg.append((int(first_and_second_idx[i, 0])))
    try:
        cursor.executemany('INSERT INTO `hmnmf_phenotype` (`phenotype_name`) VALUES (%s)', phenotype_arg)
        connection.commit()
    except Exception as e:
        print(e)
        connection.rollback()
    print('PHENOTYPE insert complete!')


# 把gene和phenotype之间已有的或者预测的关系写入到数据库
def matrix_to_db(kind, gene_id, first_and_second_idx, matrix, connection):
    if kind == 1:
        sql = 'INSERT INTO `hmnmf_known_gp_relation` (`gene_id`, `phenotype_id`, `gp_known_relation`) VALUES (%s, %s, %s)'
    elif kind == 2:
        sql = 'INSERT INTO `hmnmf_predict_gp_relation` (`gene_id`, `phenotype_id`, `gp_predict_relation`) VALUES (%s, %s, %s)'
    else:
        raise ValueError('Kind只能是1或2')

    cursor = connection.cursor()

    (m, n) = matrix.shape
    time_start = time.time()
    for i in range(m):
        gene_name = int(gene_id[i, 0])
        execute_arg = []
        for j in range(n):
            phenotype_name = int(first_and_second_idx[j, 0])
            gp_relation = round(float(matrix[i, j]), 6)
            execute_arg.append((gene_name, phenotype_name, gp_relation))
        try:
            effect_row = cursor.executemany(sql, execute_arg)
            connection.commit()
        except Exception as e:
            print(e)
            connection.rollback()
    time_end = time.time()
    print('时间已过{}秒'.format(time_end - time_start))
    print('关系矩阵成功插入到数据库！')


def get_result_file(path):
    # 可能文件夹下生成了多个结果文件，需要找到最新生成的那个结果
    fileNames = list(filter(lambda filename: os.path.splitext(filename)[1] == '.mat', os.listdir(path)))
    file_list = []
    for i in range(len(fileNames)):
        if fileNames[i].startswith('L21_CMNMF_result') != -1:
            file_list.append(fileNames[i])
    return file_list[-1]


def data_to_db(kind):
    pathway_path = 'HMNMF_Codes/2_useful_data/pathway/pathway.mat'
    known_data = scipy.io.loadmat(pathway_path)
    first_and_second_idx = known_data['first_and_second_idx']
    gene_id = known_data['gene_id']
    g_p_network = known_data['g_p_network']

    path = 'HMNMF_Codes/L21_CMNMF/old_result/pathway/'
    result_path = path + get_result_file(path)
    prediction_data = scipy.io.loadmat(result_path)
    learned_matrix_cell = prediction_data['learned_matrix_cell']
    G = learned_matrix_cell[0][1]
    P1 = learned_matrix_cell[0][2]
    P2 = learned_matrix_cell[0][3]
    R = numpy.concatenate((numpy.dot(G, P1), numpy.dot(G, P2)), axis=1)

    # 打开数据库连接
    connection = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 password='dipo123',
                                 db='grad_project',
                                 charset='utf8')

    if kind == 0:
        # 把gene,phenotype插入到数据库
        gene_phenotype_to_result(gene_id, first_and_second_idx, connection)
    elif kind == 1:
        # 把已知的g_p_network插入到数据库
        matrix_to_db(kind, gene_id, first_and_second_idx, g_p_network, connection)
    elif kind == 2:
        # 把预测结果R插入到数据库
        matrix_to_db(kind, gene_id, first_and_second_idx, R, connection)

    connection.close()

    return 'Insert kind {} complete!'.format(kind)
