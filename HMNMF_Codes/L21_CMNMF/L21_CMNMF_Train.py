from .L21_CMNMF_LF import L21_CMNMF_LF


def L21_CMNMF_Train(train_parameter_cell, matrix_cell_train, initial_matrix_cell, process_key):
    A1 = matrix_cell_train[0]
    A2 = matrix_cell_train[1]
    M = matrix_cell_train[2]
    Y1 = matrix_cell_train[3]
    Y2 = matrix_cell_train[4]

    G = initial_matrix_cell[0]
    P1 = initial_matrix_cell[1]
    P2 = initial_matrix_cell[2]

    alpha = train_parameter_cell[0]
    beta = train_parameter_cell[1]
    gamma = train_parameter_cell[2]
    miu = train_parameter_cell[3]
    rou = train_parameter_cell[4]
    max_ites = train_parameter_cell[5]

    [L, G_out, P1_out, P2_out] = L21_CMNMF_LF(max_ites, A1, A2, G, P1, P2, M, Y1, Y2, alpha, beta, gamma, miu, rou, process_key)
    learned_matrix_cell = [L, G_out, P1_out, P2_out]
    return learned_matrix_cell
