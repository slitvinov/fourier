#!/usr/bin/python3
import numpy
import math
import os

fmt = os.environ.get("OutputFmt", "%+.16e %s%03d")

N = 10
n = 2 * N
x = numpy.arange(2 * N)
f = numpy.sqrt(x) * (2 * N - x)
g = numpy.fft.rfft(f)

a = g.real/N
b = -g.imag[1:N]/N

f0 = numpy.fft.irfft(g)
assert numpy.allclose(f, f0)

print(fmt % (a[0], "a", 0))
for m in range(1, N):
    print(fmt % (a[m], "a", m))
    print(fmt % (b[m - 1], "b", m))
print(fmt % (a[N], "a", N))
