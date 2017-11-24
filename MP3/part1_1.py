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
    for img_num in range(1000):
        max_p = -sys.maxsize - 1
        max_p_label = -1
        for label in range(10):
            cal_p = 0
            for i in range(28):
                for j in range(28):
                    if test_matrix[img_num][i][j] == 1:
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
        print(matrix[i])








































