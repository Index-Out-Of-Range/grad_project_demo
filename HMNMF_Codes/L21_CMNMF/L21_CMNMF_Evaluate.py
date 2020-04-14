import numpy
from .evaluate import evaluate


def L21_CMNMF_Evaluate(learned_matrix_cell, matrix_cell_validation,train_parameter_cell):
    G = learned_matrix_cell[1]
    P1 = learned_matrix_cell[2]
    P2 = learned_matrix_cell[3]
    g_p_network_validation_first = matrix_cell_validation[0]
    g_p_network_validation_second = matrix_cell_validation[1]
    predicted_matrix = numpy.concatenate((numpy.dot(G, P1), numpy.dot(G, P2)), axis=1)

    true_matrix = numpy.concatenate((g_p_network_validation_first, g_p_network_validation_second), axis=1)
    evaluation_result = evaluate(predicted_matrix, true_matrix)
    return evaluation_result