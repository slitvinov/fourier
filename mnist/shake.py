#!/usr/bin/env python3
import numpy
import sys
import mnist
import ft

a = mnist.images(mnist.train_images)
f = a[0]

a, b = ft.ft(f, axis = 0)
aa, ab = ft.ft(a, axis = 1)
ba, bb = ft.ft(b, axis = 1)

ft.lanczos(aa, ab, axis = 1)
ft.lanczos(ba, bb, axis = 1)

a0 = ft.ift(aa, ab)
b0 = ft.ift(ba, bb)
f0 = ft.ift(a0, b0, axis = 0)

f0 = numpy.asarray(numpy.round(f0), dtype = numpy.uint8)
d = f - f0
#assert numpy.allclose(f, f0)
print(numpy.min(d), numpy.max(d))

mnist.pgm("a.pgm", f)
mnist.pgm("b.pgm", f0)

