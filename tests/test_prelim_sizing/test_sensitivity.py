import numpy as np
import pytest


def weight_change(weights):
    old_weights = np.copy(weights)
    for i in range(len(weights)):
        new_weights = np.copy(weights)
        if new_weights[i] >= 0.15:
            new_weights[i] += np.random.normal(0, 0.1)
        else:
            new_weights[i] += np.random.normal(0, 0.05)

        sum_unchanged_w = 1 - old_weights[i]
        sum_changed_w = 1 - new_weights[i]
        ratio = sum_changed_w / sum_unchanged_w
        new_weights_array = old_weights * ratio
        new_weights_array[i] = new_weights[i]

    return new_weights_array


def test_weight_sum_change():
    weights = np.random.dirichlet(np.ones(5), size=1)[0]
    assert sum(weight_change(weights)) - 1 < 1e-6


def test_len_wight_change():
    weights = np.random.dirichlet(np.ones(5), size=1)[0]
    assert len(weight_change(weights)) == len(weights)


def weight_remove(weights):
    for i in range(len(weights)):
        new_weights = np.copy(weights)
        new_weights = np.delete(new_weights, i)

        sum_changed_w = sum(new_weights)
        ratio = 1 / sum_changed_w
        new_weights_array = new_weights * ratio

    return new_weights_array


def test_weight_sum_remove():
    weights = np.random.dirichlet(np.ones(5), size=1)[0]
    assert sum(weight_remove(weights)) - 1 < 1e-6


def test_len_wight_remove():
    weights = np.random.dirichlet(np.ones(5), size=1)[0]
    assert len(weight_remove(weights)) == (len(weights) - 1)


def final_score(weights, score):
    return weights * score


def test_len_final_score():
    weights = np.array([0.3, 0.2, 0.4, 0.1])
    score = np.array([1, 2, 3, 4])
    assert len(final_score(weights, score)) == 4


def test_score():
    weights = np.array([0.3, 0.2, 0.4, 0.1])
    score = np.array([1, 2, 3, 4])
    hand_score = np.array([0.3, 0.4, 1.2, 0.4])
    assert np.allclose(final_score(weights, score), hand_score)


def winner(concepts):
    return np.argmax(concepts, axis=0)


def test_winner():
    concepts = np.array([[2, 4], [3.4, 3], [4.2, 2], [1, 1], [1.89, 0]])
    winner_concept = np.array([2, 0])
    assert np.alltrue(winner(concepts) == winner_concept)

