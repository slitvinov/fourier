#!/usr/bin/python3

import sys
import numpy
me = "mnist"
images_path = "train.images.idx3"
labels_path = "train.labels.idx1"

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

a = images(images_path)
l = labels(labels_path)

i = 56
pgm("a.pgm", a[i])
print(l[i])
