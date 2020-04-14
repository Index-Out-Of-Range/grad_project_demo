import os
import time
import numpy
import scipy.io
import datetime
from .learn import learn
from .test import test
from .result_to_db import data_to_db


def l21_cmnmf(parameter_cell):
    # parse parameter
    method_dir = parameter_cell['method_dir']
    dataset = parameter_cell['dataset']
    partition = parameter_cell['partition']
    alpha_set = parameter_cell['alpha_set']
    beta_set = parameter_cell['beta_set']
    gamma_set = parameter_cell['gamma_set']
    miu_set = parameter_cell['miu_set']
    rou_set = parameter_cell['rou_set']
    max_ites = parameter_cell['max_ites']
    cv_criteria = parameter_cell['cv_criteria']
    file_num = parameter_cell['file_num']
    K = parameter_cell['feature_num']
    hier_del = parameter_cell['hier_del']

    # load data
    if not partition:
        path = 'HMNMF_Codes/2_useful_data/' + dataset + '/' + dataset + '.mat'
    else:
        path = 'HMNMF_Codes/2_useful_data/' + dataset + '/' + dataset + '_partition/' + dataset + str(partition) + '.mat'
    data = scipy.io.loadmat(path)
    M = data['M']
    if hier_del == 1:
        M = data['M1']
    elif hier_del == 2:
        M = data['M2']
    elif hier_del == 3:
        M = data['M3']
    elif hier_del == 4:
        M = data['M4']
    elif hier_del == 5:
        M = data['M5']
    A1 = data['g_p_network_first']
    A2 = data['g_p_network_second']
    Y1 = data['indicator_first']
    Y2 = data['indicator_second']
    (g_num, p1_num) = numpy.shape(A1)
    p2_num = numpy.size(A2, 1)

    # initialize matrix with random value
    if partition == 0:
        dir = method_dir + 'data/' + dataset
    else:
        dir = method_dir + 'data/' + dataset + '/' + dataset + '_partition/' + dataset + str(partition)
    name_prefix = 'initial_matrix_fixed'
    get_files_parameter_cell = [file_num, dir, name_prefix, g_num, p1_num, p2_num, K]
    file_name_cell = get_files(get_files_parameter_cell)
    matrix_cell_train = [A1, A2, M, Y1, Y2]
    initial_matrixFileName_cell = file_name_cell

    # validation
    matrix_cell_validation = [data['g_p_network_validation_first'], data['g_p_network_validation_second']]
    input_parameter_cell = [alpha_set, beta_set, gamma_set, miu_set, rou_set, max_ites, cv_criteria, method_dir,
                            dataset, partition]
    time_start = time.time()
    (learned_matrix_cell, best_parameter_array, evaluation_result, loss, learned_matrix_cells) = learn(
        input_parameter_cell, matrix_cell_train, matrix_cell_validation, initial_matrixFileName_cell)
    time_end = time.time()
    print('时间已过', time_end - time_start, '秒')

    # test
    time_start = time.time()
    matrix_cell_test = [data['g_p_network_validation_first'], data['g_p_network_validation_second']]
    test_parameter_cell = [best_parameter_array[0], best_parameter_array[1], max_ites]
    evaluation_test = test(matrix_cell_test, learned_matrix_cell, test_parameter_cell)
    L21_CMNMF_result_cell = [loss, evaluation_test, learned_matrix_cell, learned_matrix_cells, best_parameter_array,
                             evaluation_result, max_ites, alpha_set, beta_set, gamma_set, miu_set, rou_set, hier_del]
    time_end = time.time()
    print('时间已过', time_end - time_start, '秒')

    if partition == 0:
        result_file_name = method_dir + 'old_result/' + dataset + '/L21_CMNMF_result_' + getTimeStr() + '.mat'
    else:
        result_file_name = method_dir + 'old_result/' + dataset + '/' + dataset + '_partition/' + dataset + str(
            partition) + '/L21_CMNMF_result_' + getTimeStr() + '.mat'

    scipy.io.savemat(result_file_name,
                     {'loss': loss, 'evaluation_test': evaluation_test, 'learned_matrix_cell': learned_matrix_cell,
                      'learned_matrix_cells': learned_matrix_cells, 'best_parameter_array': best_parameter_array,
                      'evaluation_result': evaluation_result, 'max_ites': max_ites, 'alpha_set': alpha_set,
                      'beta_set': beta_set, 'gamma_set': gamma_set, 'miu_set': miu_set, 'rou_set': rou_set,
                      'hier_del': hier_del})

    return "Prediction Successuful!!!"


def get_files(get_files_parameter_cell):
    [file_num_need, dir_path, name_prefix, g_num, p1_num, p2_num, K] = get_files_parameter_cell
    fileFolder = os.path.normpath(dir_path)
    fileNames = list(filter(lambda filename: os.path.splitext(filename)[1] == '.mat', os.listdir(fileFolder)))
    count = 0
    file_name_cell = []
    for i in range(len(fileNames)):
        if fileNames[i].startswith(name_prefix[0:7]) != -1:
            count = count + 1
            file_name_cell.append(fileNames[i])
    if count > file_num_need:
        file_name_cell_temp = file_name_cell[len(file_name_cell) - file_num_need:len(file_name_cell)]
        file_name_cell = file_name_cell_temp
    elif count < file_num_need:
        count_temp = count
        for i in range(file_num_need - count):
            file_name_new = 'initial_matrix_fixed_' + getTimeStr() + '.mat'
            G = numpy.random.random((g_num, K))
            P1 = numpy.random.random((K, p1_num))
            P2 = numpy.random.random((K, p2_num))
            scipy.io.savemat(dir_path + '/' + file_name_new, {'G': G, 'P1': P1, 'P2': P2})
            time.sleep(1)
            count_temp = count_temp + 1
            file_name_cell.append(file_name_new)
    return file_name_cell


def getTimeStr():
    now = datetime.datetime.now()
    month = str(now.month) if now.month > 9 else '0' + str(now.month)
    day = str(now.day) if now.day > 9 else '0' + str(now.day)
    hour = str(now.hour) if now.hour > 9 else '0' + str(now.hour)
    minute = str(now.minute) if now.minute > 9 else '0' + str(now.minute)
    second = str(now.second) if now.second > 9 else '0' + str(now.second)
    return str(now.year) + month + day + hour + minute + second
