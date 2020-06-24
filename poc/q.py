#!/usr/bin/python3
import numpy
import math
import os
import ft

fmt = os.environ.get("OutputFmt", "%+.16e %s%03d")

N = 100
n = 2 * N
x = numpy.arange(2 * N)
f = numpy.sqrt(x) * (2 * N - x)
g = numpy.fft.rfft(f)
a = g.real/N
b = -g.imag[1:N]/N
a0, b0 = ft.ft(f)
assert numpy.allclose(a, a0)
assert numpy.allclose(b, b0)

f0 = numpy.fft.irfft(g)
assert numpy.allclose(f, f0)

f0 = ft.ift(a0, b0)
assert numpy.allclose(f0, f)
