#!/usr/bin/env python3
import numpy
import sys
import mnist
import matplotlib.pyplot

#a = mnist.images(mnist.train_images)
#f = a[0]
f = matplotlib.pyplot.imread("bach.pgm")
g = numpy.fft.fft2(f)

m = numpy.mean(numpy.abs(g))
i = numpy.abs(g) < m
i[0, 0] = True
print(numpy.sum(i))
g[i] = 0

f0 = numpy.fft.ifft2(g)
f0 = numpy.real(f0)
f0 = numpy.asarray(numpy.round(f0), dtype = numpy.uint8)

mnist.pgm("a.pgm", f)
mnist.pgm("b.pgm", f0)

print(numpy.allclose(f, f0))

#r = numpy.fft.rfft(f)
#g1 = numpy.fft.rfft(r.real, axis = 0) + 1j * numpy.fft.rfft(r.imag, axis = 0)
#n = g.shape[0]//2 + 1
#print(numpy.allclose(g[:n, :], g1))

