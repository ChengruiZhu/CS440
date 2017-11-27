from math import log
import sys


def setup_image(image_name):
    image = open(image_name, 'r')
    res = []
    for line in image.readlines():
        line = line.rstrip('\n')
        row = []
        for char in line:
            if char == ' ':
                row.append(0)
            else:
                row.append(1)
        res.append(row)
    return res


def setup_labels(label_name):
    labels = open(label_name, 'r')
    res = []
    for label in labels.readlines():
        label = label.rstrip('\n')
        res.append(int(label))
    return res


if __name__ == "__main__":
    # set up training and testing images
    training_image = setup_image('digitdata/trainingimages')
    test_image = setup_image('digitdata/testimages')

    training_matrix = []
    for i in range(5000):
        training_matrix.append(training_image[i * 28: (i + 1) * 28])
    training_matrix[0][0] = [0 for i in range(28)]

    test_matrix = []
    for i in range(1000):
        test_matrix.append(test_image[i * 28: (i + 1) * 28])

    # set up training and testing labels
    training_labels = setup_labels('digitdata/traininglabels')
    test_labels = setup_labels('digitdata/testlabels')

    # calculate (Pij | class) and P_class
    p_class = [0 for i in range(10)]
    num = [0 for i in range(10)]
    pij0 = [[[0 for i in range(28)] for j in range(28)] for k in range(10)]
    pij1 = [[[0 for i in range(28)] for j in range(28)] for k in range(10)]

    for i in range(5000):
        label = training_labels[i]
        num[label] += 1
        for j in range(28):
            for k in range(28):
                if training_matrix[i][j][k] == 1:
                    pij1[label][j][k] += 1
                else:
                    pij0[label][j][k] += 1

    # smooth
    constant = 0.1
    for i in range(10):
        p_class[i] = num[i] * 1.0 / 5000.0
        for j in range(28):
            for k in range(28):
                pij1[i][j][k] = (pij1[i][j][k] + constant) * 1.0 / (num[i] + 2 * constant) * 1.0
                pij0[i][j][k] = (pij0[i][j][k] + constant) * 1.0 / (num[i] + 2 * constant) * 1.0

    # test
    result = []
    for img_idx in range(1000):
        max_p = -sys.maxsize - 1
        max_p_label = -1
        for label in range(10):
            cal_p = 0
            for i in range(28):
                for j in range(28):
                    if test_matrix[img_idx][i][j] == 1:
                        cal_p += log(pij1[label][i][j])
                    else:
                        cal_p += log(pij0[label][i][j])
            cal_p += log(p_class[label])
            if cal_p > max_p:
                max_p = cal_p
                max_p_label = label
        result.append(max_p_label)

    # calculate correctness rate
    num_test = [0 for i in range(10)]
    matrix = [[0 for i in range(10)] for j in range(10)]
    for i in range(1000):
        num_test[result[i]] += 1
        matrix[test_labels[i]][result[i]] += 1

    for i in range(10):
        for j in range(10):
            matrix[i][j] /= num_test[i]
    print('confusion matrix: ')
    for line in matrix:
        print(line)

    # find highest and lowest posterior probabilities
    max_p_for_each_digit = [(-sys.maxsize - 1) for i in range(10)]
    max_p_idx = [-1 for i in range(10)]
    min_p_for_each_digit = [sys.maxsize for i in range(10)]
    min_p_idx = [-1 for i in range(10)]
    for img_idx in range(1000):
        label = test_labels[img_idx]
        cal_p = 0
        for i in range(28):
            for j in range(28):
                if test_matrix[img_idx][i][j] == 1:
                    cal_p += log(pij1[label][i][j])
                else:
                    cal_p += log(pij0[label][i][j])
        cal_p += log(p_class[label])
        if cal_p > max_p_for_each_digit[label]:
            max_p_for_each_digit[label] = cal_p
            max_p_idx[label] = img_idx
        if cal_p < min_p_for_each_digit[label]:
            min_p_for_each_digit[label] = cal_p
            min_p_idx[label] = img_idx
    print('highest posterior probabilities and index: \n',
          max_p_for_each_digit, '\n',
          max_p_idx, '\n',
          'lowest posterior probabilities and index: \n',
          min_p_for_each_digit, '\n',
          min_p_idx)

    # likelihoods and odd ratios
    likelihood = open('likelihood.txt', 'w')
    for label in range(3, 10):
        # likelihood = open('likelihood.txt', 'a')
        for i in range(28):
            for j in range(28):
                if pij1[label][i][j] > 0.5:
                    likelihood.write('+')
                elif pij1[label][i][j] < 0.3:
                    likelihood.write('-')
                else:
                    likelihood.write(' ')
            likelihood.write('\n')
        likelihood.write('\n')

    odd_ratio53 = open('oddRatio53.txt', 'w')
    for i in range(28):
        for j in range(28):
            if log(pij1[5][i][j] / pij1[3][i][j]) > 0.2:
                odd_ratio53.write('+')
            elif log(pij1[5][i][j] / pij1[3][i][j]) < -0.2:
                odd_ratio53.write('-')
            else:
                odd_ratio53.write(' ')
        odd_ratio53.write('\n')

    odd_ratio49 = open('oddRatio49.txt', 'w')
    for i in range(28):
        for j in range(28):
            if log(pij1[4][i][j] / pij1[9][i][j]) > 0.2:
                odd_ratio49.write('+')
            elif log(pij1[4][i][j] / pij1[9][i][j]) < -0.2:
                odd_ratio49.write('-')
            else:
                odd_ratio49.write(' ')
        odd_ratio49.write('\n')

    odd_ratio79 = open('oddRatio79.txt', 'w')
    for i in range(28):
        for j in range(28):
            if log(pij1[7][i][j] / pij1[9][i][j]) > 0.2:
                odd_ratio79.write('+')
            elif log(pij1[7][i][j] / pij1[9][i][j]) < -0.2:
                odd_ratio79.write('-')
            else:
                odd_ratio79.write(' ')
        odd_ratio79.write('\n')

    odd_ratio89 = open('oddRatio89.txt', 'w')
    for i in range(28):
        for j in range(28):
            if log(pij1[8][i][j] / pij1[9][i][j]) > 0.2:
                odd_ratio89.write('+')
            elif log(pij1[8][i][j] / pij1[9][i][j]) < -0.2:
                odd_ratio89.write('-')
            else:
                odd_ratio89.write(' ')
        odd_ratio89.write('\n')








































