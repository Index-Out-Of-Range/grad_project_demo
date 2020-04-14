import numpy
from .evaluate import evaluate


def test(matrix_cell_test,learned_matrix_cell,test_parameter_cell):
    G = learned_matrix_cell[1]
    P1 = learned_matrix_cell[2]
    P2 = learned_matrix_cell[3]
    g_p_network_validation_first = matrix_cell_test[0]
    g_p_network_validation_second = matrix_cell_test[1]
    predicted_matrix = numpy.concatenate((numpy.dot(G, P1), numpy.dot(G, P2)), axis=1)
    true_matrix = numpy.concatenate((g_p_network_validation_first, g_p_network_validation_second), axis=1)
    test_result = evaluate(predicted_matrix, true_matrix)
    return test_result