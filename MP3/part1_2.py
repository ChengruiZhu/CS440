from math import log
import sys

n = 2
m = 2
num_color = 2
num_class = 10

total = 5000
constant = 0.1

# read image
# save as 0/1 array
# 0 ' '
# 1 '#'
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


# read label
# save as array
def setup_labels(label_name):
    labels = open(label_name, 'r')
    res = []
    for label in labels.readlines():
        label = label.rstrip('\n')
        res.append(int(label))
    return res


# 1d flat image to 2d image
# n is width 
def transform_to_2d_image(flat_image, n):
  image = []

  pos = 0
  row = []
  for pixel in flat_image:
    pos += 1
    row.append(pixel)
    if pos == n:
      pos = 0
      image.append(row)
      row = []

  return image

# input type 
# image - [][] 2d array please
def form_features(image, n, m, overlap=False):
  # set up step for row
  step_x = n
  step_y = m
  width = len(image[0])
  height = len(image)

  if overlap is True:
    step_x = 1
    step_y = 1

  features = []
  for i in range(0, width, step_x):
    for j in range(0, height, step_y):
      if (i + n <= width) and (j + m <= height):
        feature = form_feature(image, range(i, i + n), range(j, j + m))
        features.append(((i, j), tuple(feature)))

  return features


# return the feature of the image
def form_feature(image, rx, ry):
  feature = []
  for x in rx:
    for y in ry:
      feature.append(image[x][y])
  return feature

# count num of each label/class
def count_label(labels, num_class):
  count  = [0 for i in range(num_class)]
  for label in labels:
    count[label] += 1
  return count

# calculate p[class] / prior 
def calculate_p_class(counts, total=5000):
  p_class = []
  for count in counts:
    temp = count / float(total) 
    p_class.append(temp)
  return p_class

# count pij (do not calculate or smooth yet)
def count_pij(feature_images, labels):
  pij_counts = {}
  for image, label in zip(feature_images, labels):
    for pos, value in image:
      key = (pos, value, label) 
      if key in pij_counts:
        pij_counts[key] += 1
      else:
        pij_counts[key] = 1
  return pij_counts

# calculate pij 
# pij)coutns {pij[][]:count}
def calculate_pij(pij_counts, counts, k, v):
  res = {}
  for key, count in pij_counts.items():
    pos, value, label = key
    res[key] = float(count + k) / (counts[label] + k * v)
  return res


def calculate_pij_zero(label, counts, k, v):
    return float(k) / (counts[label] + k * v)

# calculate v 
def calculate_v(n, m, num_color):
  return num_color * 2 ** (n * m)
  

if __name__ == "__main__":
    # set up training and testing images
    training_image = setup_image('digitdata/trainingimages')
    test_image = setup_image('digitdata/testimages')

     # set up training and testing labels
    training_labels = setup_labels('digitdata/traininglabels')
    test_labels = setup_labels('digitdata/testlabels')
 
    # split input rows to images
    training_matrix = []
    for i in range(5000):
        training_matrix.append(training_image[i * 28: (i + 1) * 28])
    training_matrix[0][0] = [0 for i in range(28)]

    test_matrix = []
    for i in range(1000):
        test_matrix.append(test_image[i * 28: (i + 1) * 28])

    # this will be used for training
    training_feature_images = []
    for image in training_matrix:
      features = form_features(image, n, m, overlap=True)
      training_feature_images.append(features)

    # this will be used for test
    test_feature_images = []
    for image in test_matrix:
      features = form_features(image, n, m, overlap=True)
      test_feature_images.append(features)
      
    counts = count_label(training_labels, num_class)
    p_class = calculate_p_class(counts, total)

    # calculate pij
    pij_counts = count_pij(training_feature_images, training_labels)
    v = calculate_v(n, m, num_color) 
    k = constant
    pij = calculate_pij(pij_counts, counts, k, v)

    # test 
    result = []
    for image in test_feature_images:
      probs = []
      for label in range(num_class):
        prob = log(p_class[label])
        for pos, value in image:
          key = (pos, value, label) 
          if key in pij:
            prob += log(pij[key])
          else:
            prob += log(calculate_pij_zero(label, counts, k, v))
        probs.append((prob, label))
      label = max(probs,key=lambda item:item[0])[1]
      result.append(label)
            
    # calculate correctness rate
    num_test = [0 for i in range(num_class)]
    matrix = [[0 for i in range(num_class)] for j in range(num_class)]
    for i in range(1000):
        num_test[result[i]] += 1
        matrix[test_labels[i]][result[i]] += 1

    for i in range(num_class):
        for j in range(num_class):
            matrix[i][j] /= float(num_test[i])
            matrix[i][j] = format(matrix[i][j], '.3f')
        print(matrix[i])

