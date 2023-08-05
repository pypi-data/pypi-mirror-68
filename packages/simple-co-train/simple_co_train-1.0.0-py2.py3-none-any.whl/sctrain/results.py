import numpy as np
import os


def print_results(e):
    print('Accuracies')
    print(e.accuracies)
    print('F1-scores')
    print(e.f1_scores)
    print('Precisions')
    print(e.precisions)
    print('Recalls')
    print(e.recalls)
    print('Pseudo labelled')
    print(e.unsure_labelled)
    print('Total pseudo labelled')
    print(np.sum(e.unsure_labelled))


def save_results(e, i: int):
    if not os.path.exists('Results'):
        os.mkdir('Results')

    os.mkdir(f'Results/Round {i}')

    np.savetxt(f'./Results/Round {i}/accuracies.csv', e.accuracies, delimiter=',')
    np.savetxt(f'./Results/Round {i}/f1_scores.csv', e.f1_scores, delimiter=',')
    np.savetxt(f'./Results/Round {i}/precisions.csv', e.precisions, delimiter=',')
    np.savetxt(f'./Results/Round {i}/recalls.csv', e.recalls, delimiter=',')
    np.savetxt(f'./Results/Round {i}/unsure_labelled.csv', e.unsure_labelled, delimiter=',')
