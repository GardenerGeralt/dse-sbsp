import numpy as np
import pytest


def weight_sum_change(weights):
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

    return sum(new_weights_array)


def test_weight_sum_change():
    weights = np.random.dirichlet(np.ones(5), size=1)[0]
    assert weight_sum_change(weights) - 1 < 1e-6


def weight_sum_remove(weights):
    for i in range(len(weights)):
        new_weights = np.copy(weights)
        new_weights = np.delete(new_weights, i)

        sum_changed_w = sum(new_weights)
        ratio = 1 / sum_changed_w
        new_weights_array = new_weights * ratio

    return sum(new_weights_array)


def test_weight_sum_remove():
    weights = np.random.dirichlet(np.ones(5), size=1)[0]
    assert weight_sum_remove(weights) - 1 < 1e-6
