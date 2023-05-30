import numpy as np
import matplotlib.pyplot as plt


def change_w(weights, num_simulation, score):
    old_weights = np.copy(weights)
    overall_score = []
    for i in range(len(weights)):
        for j in range(num_simulation):

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

            overall_score.append(sum(new_weights_array * score))

            j += 1
    return np.array(overall_score)


def remove_w(weights, score):
    overall_score = []
    for i in range(len(weights)):
        new_weights = np.copy(weights)
        new_score = np.copy(score)
        new_weights = np.delete(new_weights, i)
        new_score = np.delete(new_score, i)

        sum_changed_w = sum(new_weights)
        ratio = 1 / sum_changed_w
        new_weights_array = new_weights * ratio

        overall_score.append(sum(new_weights_array * new_score))

    return np.array(overall_score)


def winner(concepts):
    winners = np.argmax(concepts, axis=0)

    count6 = 0
    count3 = 0
    for _ in winners:
        if (_ + 1) == 6:
            count6 += 1
        else:
            count3 += 1

    print(count6, count3)

    hist, bins = np.histogram(winners, bins=range(1, len(concepts) + 1))
    plt.bar(bins[1:], hist, align='center')
    plt.xticks(range(len(concepts) + 1))
    plt.xlabel('Concepts')
    plt.ylabel('Winning frequency')
    #plt.title(title, fontweight='bold')
    plt.show()


###--------------DEMO--------------###
ws = np.array([0.25, 0.15, 0.2, 0.3, 0.1])  # array of normalized weights
scores = np.array(
    [np.array([2, 4, 4, 1, 2]), np.array([3, 4, 3, 2, 2]), np.array([4, 4, 2, 3, 3]), np.array([2, 3, 3, 1, 3]),
     np.array([2, 3, 2, 2, 3]), np.array([4, 3, 2, 4, 4])])
"""array containing the arrays of the individual score for each concept, in this case in a scale from 1 to 5."""

result_change = []
result_remove = []
n_sim = 10000
for score in scores:
    result_change.append(change_w(ws, n_sim, score))
    result_remove.append(remove_w(ws, score))

result_change = np.array(result_change)
result_remove = np.array(result_remove)
winners_remove = np.argmax(result_remove, axis=0)
for i in range(len(ws)):
    print(f'Removing criteria number {i + 1}, concept number {winners_remove[i] + 1} wins')

winner(result_change)
