#!/usr/bin/python3

import sys
import numpy
me = "mnist"
path = "test.images.idx3"
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
    a = a.reshape(n_images, n_rows, n_columns)

s = a[1891]
with open("a.pgm", "w") as file:
    file.write("P5\n")
    file.write("%d %d\n" % s.shape)
    file.write("%d\n" % 0xFF)
    s.tofile(file)
