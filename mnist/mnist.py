#!/usr/bin/python3

import numpy
import sys

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
    s = numpy.asarray(s)
    if s.dtype != numpy.uint8:
        sys.stderr.write("%s: wrong dtype = '%s'\n" % (me, s.dtype))
        sys.exit(2)
    with open(path, "w") as file:
        file.write("P5\n")
        file.write("%d %d\n" % (s.shape[1], s.shape[0]))
        file.write("%d\n" % 0xFF)
        s.tofile(file)
