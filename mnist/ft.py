#!/usr/bin/python3

import numpy

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
