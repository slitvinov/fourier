#!/usr/bin/python3

import numpy
import math

def ft(f, axis = -1):
    f = numpy.asarray(f)
    n = f.shape[axis]
    if n % 2 != 0:
        raise RuntimeError("f.shape[%d]=%d is not even" % (axis, n))
    N = n // 2
    g = numpy.fft.rfft(f, axis=axis)
    g /= N
    index = [slice(None)] * g.ndim
    index[axis] = slice(1, -1)
    index = tuple(index)
    a = g.real
    b = -g.imag[index]
    return a, b

def ift(a, b, axis = -1):
    N = a.shape[axis] - 1
    if b.shape[axis] != N - 1:
        raise RuntimeError("wrong dimensions for a and b")
    g = numpy.zeros_like(a, dtype = 'complex128')
    index = [slice(None)] * g.ndim
    index[axis] = slice(1, -1)
    index = tuple(index)
    g.real = a
    g.imag[index] = -b
    return N * numpy.fft.irfft(g, axis=axis)

def lanczos(a, b, axis = -1):
    N = a.shape[axis] - 1
    if b.shape[axis] != N - 1:
        raise RuntimeError("wrong dimensions for a and b")
    m = numpy.arange(1, N)
    sigma = numpy.sin(math.pi * m / N) / (math.pi * m / N)

    index = [None] * a.ndim
    index[axis] = slice(None)
    index = tuple(index)

    sigma = sigma[index]
    b *= sigma

    index = [slice(None)] * a.ndim
    index[axis] = slice(1, -1)
    index = tuple(index)
    a[index] *= sigma
