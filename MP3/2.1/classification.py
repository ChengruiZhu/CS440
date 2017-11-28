import math


'''
training
'''
prior = 0.0

cols = 10

rows = 25

matrix_y = [[0.5 for col in range(cols)] for row in range(rows)]

matrix_n = [[0.5 for col in range(cols)] for row in range(rows)]

f = open('yesno/yes_train.txt')
line = f.readline()

row = 0

while line:
    if row == 0:
        prior += 1
    for col in range(len(line)):
        if line[col] == '%':
            matrix_y[row][col] += 1

    line = f.readline()
    if line != '\n':
        row += 1
    else:
        row = -1

f.close()

total = prior

for i in range(rows):
    for j in range(cols):
        matrix_y[i][j] /= total+1

# for i in range(rows):
#     print(matrix_y[i])

f = open('yesno/no_train.txt')
line = f.readline()

row = 0

while line:
    if row == 0:
        total += 1
    for col in range(len(line)):
        if line[col] == '%':
            matrix_n[row][col] += 1

    line = f.readline()
    if line != '\n':
        row += 1
    else:
        row = -1

f.close()

for i in range(rows):
    for j in range(cols):
        matrix_n[i][j] /= total-prior+1

prior /= total

# print(prior)

# for i in range(rows):
#     print(matrix_y[i])
#
# print('\n\n\n')
#
# for i in range(rows):
#     print(matrix_n[i])
'''
modeling
'''


def yes_or_no(m):
    Y = math.log(prior)
    N = math.log(1 - prior)

    for i in range(len(m)):
        for j in range(len(m[0])):
            if m[i][j] == '%':
                Y += math.log(matrix_y[i][j])
                N += math.log(matrix_n[i][j])
            else:
                Y += math.log(1 - matrix_y[i][j])
                N += math.log(1 - matrix_n[i][j])
    if Y > N:
        return 1
    else:
        return 0


def accurate(file, label):
    Y = 0.0
    N = 0.0
    f = open(file)
    line = f.readline()
    m = []
    while line:
        if not line == '\n':
            m.append(line[:-1])
        line = f.readline()
        if line == '\n':
            check = yes_or_no(m)
            m = []
            Y += check
            N += 1 - check
        while line == '\n':
            line = f.readline()
    if label == 'yes':
        return Y / (Y + N)
    else:
        return N / (Y + N)

Y = accurate('yesno/yes_test.txt', 'yes')
N = accurate('yesno/no_test.txt', 'no')

conf = [[Y, 1 - Y], [1 - N, N]]

# print(accurate('yesno/yes_test.txt', 'no'))
# print(accurate('yesno/no_test.txt', 'yes'))

print('Confusion Matrix:')
print(conf[0])
print(conf[1])