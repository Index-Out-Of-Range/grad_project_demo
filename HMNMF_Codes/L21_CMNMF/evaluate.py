import numpy
import scipy.io


def evaluate(predicted_matrix, true_matrix):
    gene_num = numpy.size(predicted_matrix, 0)
    pheno_num = numpy.size(predicted_matrix, 1)

    if gene_num < 200:
        A_predict = predicted_matrix
        A_vali = true_matrix
        A_predict[numpy.where(A_vali == -1)] = -1
        A_vali[numpy.where(A_vali == -1)] = 0

        for j in range(15):
            index = numpy.argsort(-A_predict[:, j])
            vali_num = len(numpy.where(A_vali[:, j] == 1)[0])
            A_predict[:, j] = 0
            A_predict[index[0:vali_num], j] = 1

        hit_rates = numpy.zeros((15, 1))
        for j in range(15):
            hit_rates[j][0] = numpy.sum(A_predict[:, j] * A_vali[:, j]) / len(numpy.nonzero(A_vali[:, j])[0])
        hit_rates[numpy.isnan(hit_rates)] = -1
        evaluation_result = numpy.zeros((1, 31))
        evaluation_result[0][0] = numpy.mean(hit_rates[hit_rates != -1])
        evaluation_result[0][1:16] = hit_rates.transpose()

        return evaluation_result

    m = max(true_matrix.flatten('F'))
    if m > 1:
        true_matrix = numpy.where((0 < true_matrix) & (true_matrix < m - 1), 0, true_matrix)
        true_matrix = numpy.where(true_matrix >= m - 1, 1, true_matrix)

    predicted_matrix[numpy.where(true_matrix == -1)] = -1
    predicted_matrix = predicted_matrix + numpy.random.rand(numpy.size(predicted_matrix, 0),
                                                            numpy.size(predicted_matrix, 1)) * pow(10, -10)

    # data = scipy.io.loadmat(r'D:\STUDY\GradProject\MyCodes\evaluate_para.mat')
    # predicted_matrix = data['predicted_matrix']

    AUC20s = numpy.zeros((pheno_num, 1))
    AUC50s = numpy.zeros((pheno_num, 1))
    AUC100s = numpy.zeros((pheno_num, 1))
    AUC200s = numpy.zeros((pheno_num, 1))
    AUCs = numpy.zeros((pheno_num, 1))
    P_counts = numpy.zeros((pheno_num, 1))

    # I_all = numpy.empty((1, pheno_num), dtype=object)
    # true_scores_all = numpy.empty((1, pheno_num), dtype=object)
    # predict_count_all = numpy.empty((1, pheno_num), dtype=object)
    # P_all = numpy.empty((5, pheno_num), dtype=object)
    # N_all = numpy.empty((5, pheno_num), dtype=object)

    for j in range(pheno_num):
        if len(numpy.nonzero(predicted_matrix[:, j])[0]) == 0:
            continue
        sorted_scores = numpy.sort(-predicted_matrix[:, j])
        I = numpy.argsort(-predicted_matrix[:, j])
        true_scores = true_matrix[I, j]
        predict_count = len(numpy.where(true_scores != -1)[0])
        P_counts[j][0] = len(numpy.where(true_scores == 1)[0])

        # I_all[0][j] = (I + 1).reshape(-1, 1)
        # true_scores_all[0][j] = true_scores.reshape(-1, 1)
        # predict_count_all[0][j] = predict_count

        P20 = 0
        N20 = 0
        P50 = 0
        N50 = 0
        P100 = 0
        N100 = 0
        P200 = 0
        N200 = 0
        P = 0
        N = 0

        for k in range(20):
            if true_scores[k] == 1:
                P20 = P20 + 1
                P50 = P50 + 1
                P100 = P100 + 1
                P200 = P200 + 1
                P = P + 1
            else:
                N20 = N20 + 1
                N50 = N50 + 1
                N100 = N100 + 1
                N200 = N200 + 1
                N = N + 1
        for k in range(20, 50):
            if true_scores[k] == 1:
                P50 = P50 + 1
                P100 = P100 + 1
                P200 = P200 + 1
                P = P + 1
            else:
                N50 = N50 + 1
                N100 = N100 + 1
                N200 = N200 + 1
                N = N + 1
        for k in range(50, 100):
            if true_scores[k] == 1:
                P100 = P100 + 1
                P200 = P200 + 1
                P = P + 1
            else:
                N100 = N100 + 1
                N200 = N200 + 1
                N = N + 1
        for k in range(100, 200):
            if true_scores[k] == 1:
                P200 = P200 + 1
                P = P + 1
            else:
                N200 = N200 + 1
                N = N + 1
        for k in range(200, predict_count):
            if true_scores[k] == 1:
                P = P + 1
            else:
                N = N + 1

        # P_all[:, j] = (P20, P50, P100, P200, P)
        # N_all[:, j] = (N20, N50, N100, N200, N)

        if P20 == 0:
            AUC20s[j][0] = 0
        elif N20 == 0:
            AUC20s[j][0] = 1
        else:
            s = 0
            for k in range(20):
                if true_scores[k] == 1:
                    s = s + 21 - k-1
            AUC20s[j][0] = (s - (P20 + 1) * P20 / 2) / (P20 * N20)
        if P50 == 0:
            AUC50s[j][0] = 0
        elif N50 == 0:
            AUC50s[j][0] = 1
        else:
            s = 0
            for k in range(50):
                if true_scores[k] == 1:
                    s = s + 51 - k-1
            AUC50s[j][0] = (s - (P50 + 1) * P50 / 2) / (P50 * N50)
        if P100 == 0:
            AUC100s[j][0] = 0
        elif N100 == 0:
            AUC100s[j][0] = 1
        else:
            s = 0
            for k in range(100):
                if true_scores[k] == 1:
                    s = s + 101 - k-1
            AUC100s[j][0] = (s - (P100 + 1) * P100 / 2) / (P100 * N100)
        if P200 == 0:
            AUC200s[j][0] = 0
        elif N200 == 0:
            AUC200s[j][0] = 1
        else:
            s = 0
            for k in range(200):
                if true_scores[k] == 1:
                    s = s + 201 - k-1
            AUC200s[j][0] = (s - (P200 + 1) * P200 / 2) / (P200 * N200)
        if P == 0:
            AUCs[j][0] = 0
        elif N == 0:
            AUCs[j][0] = 1
        else:
            s = 0
            for k in range(predict_count):
                if true_scores[k] == 1:
                    s = s + predict_count + 1 - k-1
            AUCs[j][0] = (s - (P + 1) * P / 2) / (P * N)

    # scipy.io.savemat('python.mat', {'python_P_counts': P_counts,
    #                                 'python_I_all': I_all,
    #                                 'python_true_scores_all': true_scores_all,
    #                                 'python_predict_count_all': predict_count_all,
    #                                 'python_P_all': P_all,
    #                                 'python_N_all': N_all,
    #                                 'python_predicted_matrix': predicted_matrix,
    #                                 'python_AUC20s':AUC20s,
    #                                 'python_AUC50s':AUC50s,
    #                                 'python_AUC100s':AUC100s,
    #                                 'python_AUC200s':AUC200s,
    #                                 'python_AUCs':AUCs})

    # print('AUC20s: ', numpy.sum(AUC20s))
    # print('AUC50s: ', numpy.sum(AUC50s))
    # print('AUC100s: ', numpy.sum(AUC100s))
    # print('AUC200s: ', numpy.sum(AUC200s))
    # print('AUCs: ', numpy.sum(AUCs))
    # print('P_counts: ', numpy.sum(P_counts))

    AUC20 = numpy.sum(AUC20s * P_counts) / numpy.sum(P_counts)
    AUC50 = numpy.sum(AUC50s * P_counts) / numpy.sum(P_counts)
    AUC100 = numpy.sum(AUC100s * P_counts) / numpy.sum(P_counts)
    AUC200 = numpy.sum(AUC200s * P_counts) / numpy.sum(P_counts)
    AUC = numpy.sum(AUCs * P_counts) / numpy.sum(P_counts)

    predict_count = len(numpy.where(true_matrix != -1)[0])
    I = numpy.argsort(-predicted_matrix.flatten('F'))

    true_scores = true_matrix.flatten('F')[I]

    P = 0
    N = 0
    vec_precision = numpy.zeros((predict_count, 1))
    for j in range(predict_count):
        if true_scores[j] == 1:
            P = P + 1
            vec_precision[j][0] = P / (P + N)
        else:
            N = N + 1
    AUPR = numpy.mean(vec_precision)

    RMSE = 0
    HR5000 = 0
    HR2000 = 0
    HR1000 = 0
    HR500 = 0
    HR200 = 0
    HR100 = 0
    HR50 = 0
    HR20 = 0
    HR10 = 0
    HR5 = 0
    HR2 = 0
    HR1 = 0
    ARHR5000 = 0
    ARHR2000 = 0
    ARHR1000 = 0
    ARHR500 = 0
    ARHR200 = 0
    ARHR100 = 0
    ARHR50 = 0
    ARHR20 = 0
    ARHR10 = 0
    ARHR5 = 0
    ARHR2 = 0
    ARHR1 = 0

    evaluation_result = [AUC20, AUC50, AUC100, AUC200, AUC, AUPR, RMSE, HR5000, HR2000, HR1000, HR500, HR200, HR100,
                         HR50, HR20, HR10, HR5, HR2, HR1, ARHR5000, ARHR2000, ARHR1000, ARHR500, ARHR200, ARHR100,
                         ARHR50, ARHR20, ARHR10, ARHR5, ARHR2, ARHR1]

    print('evaluation_result: ', evaluation_result)
    return evaluation_result
