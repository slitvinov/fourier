#!/usr/bin/python3

import numpy
import ft

N = 20
m = numpy.arange(0, 2*N)
f = numpy.asarray(m > N, dtype=numpy.uint8)

a, b = ft.ft(f)
ft.lanczos(a, b)
f0 = ft.ift(a, b)

f0.tofile("f0", sep="\n", format="%+.16e")
