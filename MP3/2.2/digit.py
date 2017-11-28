import math

'''training'''
prior = [0.0 for i in range(5)]

cols = 13
rows = 30

matrix = [[[0.5 for col in range(cols)] for row in range(rows)] for i in range(5)]

f1 = open('data22/training_data.txt')
f2 = open('data22/training_labels.txt')
line1 = f1.readline()
line2 = f2.readline()

row = 0
prior[int(line2[0]) - 1] += 1

while line1:
    for col in range(len(line1[:-1])):
        if line1[col] == '%':
            matrix[int(line2[0]) - 1][row][col] += 1
    line1 = f1.readline()
    if line1 != '\n':
        row += 1
    else:
        line2 = f2.readline()
        while line1 == '\n':
            line1 = f1.readline()
        row = 0
        if not line2 == '':
            prior[int(line2[0]) - 1] += 1

f1.close()
f2.close()

for i in range(5):
    for j in range(rows):
        for k in range(cols):
            matrix[i][j][k] /= 13.0

'''modeling'''


def digit(m):
    numb = [0.0 for i in range(5)]

    for i in range(len(m)):
        for j in range(len(m[0])-1):
            if m[i][j] == '%':
                for k in range(5):
                    numb[k] += math.log(matrix[k][i][j])
            else:
                for k in range(5):
                    numb[k] += math.log(1 - matrix[k][i][j])

    index = 0
    max_numb = numb[0]
    for i in range(5):
        if numb[i] >= max_numb:
            max_numb = numb[i]
            index = i
    return index

conf = [[0.0 for i in range(5)] for j in range(5)]

f1 = open('data22/testing_data.txt')
f2 = open('data22/testing_labels.txt')
line1 = f1.readline()
line2 = f2.readline()

row = 0
# prior[int(line2[0]) - 1] += 1
m = []

while line1:
    if line1 != '\n':
        m.append(line1)
    line1 = f1.readline()
    if line1 == '\n':
        if line2 != '':
            conf[int(line2[0]) - 1][digit(m)] += 1
        m = []
        while line1 == '\n':
            line1 = f1.readline()
        line2 = f2.readline()

f1.close()
f2.close()

sum = 0.0

for i in range(5):
    sum += conf[i][i]
    for j in range(5):
        conf[i][j] /= 8.0

sum /= 40

print('Confustion Matrix:')

for i in range(5):
    print(conf[i])

print('\nTotal Accuracy:')
print(sum)