#!/usr/bin/python3

import numpy
import scipy
import sys
import sklearn.linear_model

me = "mnist"
train_images = "train.images.idx3"
train_labels = "train.labels.idx1"

test_images = "test.images.idx3"
test_labels = "test.labels.idx1"

def images(path):
    MAGIC = 2051
    with open(path) as file:
        magic, = numpy.fromfile(file, dtype=">u4", count=1)
        if magic != MAGIC:
            sys.stderr.write("%s: wrong magic number %d\n" % (me, magic))
            sys.exit(2)
        n_images, n_rows, n_columns = numpy.fromfile(file, dtype=">u4", count=3)
        a = numpy.fromfile(file, dtype = "u1")
        if numpy.size(a) != n_images * n_rows * n_columns:
            sys.stderr.write("%s: wrong file size\n" % me)
            sys.exit(2)
    return a.reshape(n_images, n_rows, n_columns)
def labels(path):
    MAGIC = 2049
    with open(path) as file:
        magic, = numpy.fromfile(file, dtype=">u4", count=1)
        if magic != MAGIC:
            sys.stderr.write("%s: wrong magic number %d\n" % (me, magic))
            sys.exit(2)
        n_items, = numpy.fromfile(file, dtype=">u4", count=1)
        a = numpy.fromfile(file, dtype = "u1")
        if numpy.size(a) != n_items:
            sys.stderr.write("%s: wrong file size\n" % me)
            sys.exit(2)
    return a
def pgm(path, s):
    with open(path, "w") as file:
        file.write("P5\n")
        file.write("%d %d\n" % s.shape)
        file.write("%d\n" % 0xFF)
        s.tofile(file)

def to(a):
    n = a.shape[0]
    b = []
    for i in range(n):
        f = scipy.fft.fft2(a[i])
        f = numpy.array((f.real, f.imag))
        f = f.ravel()
        b.append(f)
        if i % 10000 == 0:
            sys.stderr.write("%s: %05d/%05d\n" % (me, i, n))
    return b

a = images(train_images)
l = labels(train_labels)
b = to(a)

reg = sklearn.linear_model.LogisticRegression(solver = 'lbfgs', max_iter=10000)
reg.fit(b, l)
print(reg.score(b, l))

a0 = images(test_images)
l0 = labels(test_labels)
b0 = to(a0)
print(reg.score(b0, l0))
