import numpy
import scipy.io
from .L21_CMNMF_Train import L21_CMNMF_Train
from .L21_CMNMF_Evaluate import L21_CMNMF_Evaluate


def learn(input_parameter_cell, matrix_cell_train, matrix_cell_validation, initial_matrixFileName_cell, process_key):
    [alpha_set, beta_set, gamma_set, miu_set, rou_set, max_ites, cv_criteria, method_dir, dataset,
     partition] = input_parameter_cell
    i = 1

    # evaluation_result:每组参数组合下，十次随机初始化学习到十次结果的平均值
    evaluation_num = 31
    evaluation_result = numpy.zeros((1, evaluation_num + 5))
    file_num = len(initial_matrixFileName_cell)
    arg_num = 1
    evaluation_result_all = numpy.zeros((1, file_num, evaluation_num + 5))
    loss = numpy.empty((arg_num, file_num + 5), dtype=object)
    learned_matrix_cells = numpy.empty((arg_num, file_num), dtype=object)
    for j in range(1):
        print('arg_index= ' + str(j))
        cv_parameter_cell = [alpha_set, beta_set, gamma_set, miu_set, rou_set, max_ites, cv_criteria, method_dir,
                             dataset, partition]
        # (evaluation_result[i - 1][0: evaluation_num], evaluation_result_all[i - 1][:][0: evaluation_num],
        # loss[i - 1][:], learned_matrix_cells[i - 1][:]) = cv_train(cv_parameter_cell, matrix_cell_train,
        # matrix_cell_validation, initial_matrixFileName_cell)
        (r1, r2, r3, r4) = cv_train(cv_parameter_cell, matrix_cell_train, matrix_cell_validation, initial_matrixFileName_cell, process_key)
        evaluation_result[i - 1][0: evaluation_num]=r1
        evaluation_result_all[i - 1][:][0][0: evaluation_num] = r2[0]
        loss[i - 1][:] = r3
        learned_matrix_cells[i - 1][:] = r4

        evaluation_result[i - 1][evaluation_num:] = [alpha_set, beta_set, gamma_set, miu_set, rou_set]
        i = i + 1

    (arg_index, best_parameter_array) = get_best_parameter(evaluation_result, cv_criteria)
    file_index = numpy.argmax(evaluation_result_all[arg_index, :, 1])
    learned_matrix_cell = learned_matrix_cells[arg_index, file_index]

    return learned_matrix_cell, best_parameter_array, evaluation_result, loss, learned_matrix_cells


def cv_train(cv_parameter_cell, matrix_cell_train, matrix_cell_validation, initial_matrixFileName_cell, process_key):
    train_parameter_cell = cv_parameter_cell
    method_dir = cv_parameter_cell[7]
    dataset = cv_parameter_cell[8]
    partition = cv_parameter_cell[9]
    if not partition:
        method_data_dir = method_dir + 'data/' + dataset + '/'
    else:
        method_data_dir = method_dir + 'data/' + dataset + '/' + dataset + '_partition/' + dataset + str(
            partition) + '/'
    evaluation_num = 31
    file_num = len(initial_matrixFileName_cell)
    evaluation_result = numpy.zeros((file_num, evaluation_num))
    loss = numpy.empty((1, file_num + 5), dtype=object)
    learned_matrix_cells = numpy.empty((file_num, 1), dtype=object)
    for j in range(file_num):
        print('file_index=' + str(j))
        file_name = method_data_dir + initial_matrixFileName_cell[j]
        data = scipy.io.loadmat(file_name)
        initial_matrix_cell = [data['G'], data['P1'], data['P2']]
        learned_matrix_cell = L21_CMNMF_Train(train_parameter_cell, matrix_cell_train, initial_matrix_cell, process_key)
        evaluation_result[j] = L21_CMNMF_Evaluate(learned_matrix_cell, matrix_cell_validation, train_parameter_cell)
        loss[0][j] = learned_matrix_cell[0]
        learned_matrix_cells[j][0] = learned_matrix_cell

    loss[0][file_num] = cv_parameter_cell[0]
    loss[0][file_num + 1] = cv_parameter_cell[1]
    loss[0][file_num + 2] = cv_parameter_cell[2]
    loss[0][file_num + 3] = cv_parameter_cell[3]
    loss[0][file_num + 4] = cv_parameter_cell[4]

    if file_num == 1:
        evaluation_result_average = evaluation_result
    else:
        evaluation_result_average = numpy.mean(evaluation_result, axis=0)

    return evaluation_result_average, evaluation_result, loss, learned_matrix_cells


def get_best_parameter(evaluation_result, cv_criteria):
    evaluation_set = ['AUC20', 'AUC50', 'AUC100', 'AUC200', 'AUC', 'AUPR', 'RMSE', 'HR5000', 'HR2000', 'HR1000',
                      'HR500', 'HR200', 'HR100', 'HR50', 'HR20', 'HR10', 'HR5', 'HR2', 'HR1', 'ARHR5000', 'ARHR2000',
                      'ARHR1000', 'ARHR500', 'ARHR200', 'ARHR100', 'ARHR50', 'ARHR20', 'ARHR10', 'ARHR5', 'ARHR2',
                      'ARHR1']

    if cv_criteria == evaluation_set[6]:
        M = numpy.min(evaluation_result[:6])
        I = numpy.argmin(evaluation_result[:, 6])
        best_parameter_array = evaluation_result[I, -1 - 4:]
        arg_index = I
    else:
        for j in range(len(evaluation_set)):
            if j == 6:
                continue
            if cv_criteria == evaluation_set[j]:
                M = numpy.max(evaluation_result[:j])
                I = numpy.argmax(evaluation_result[:, j])
                best_parameter_array = evaluation_result[I, -1 - 4:]
                arg_index = I

    return arg_index, best_parameter_array
