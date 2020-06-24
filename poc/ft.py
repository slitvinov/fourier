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
    index = numpy.arange(1, g.shape[-1] - 1)
    a = g.real
    b = -g.imag.take(index, axis=axis)
    return a, b

def ift(a, b, axis = -1):
    N = a.shape[-1] - 1
    if b.shape[-1] != N - 1:
        raise RuntimeError("wrong dimensions for a and b")
    g = numpy.zeros_like(a, dtype = 'complex128')
    g.real = a
    g.imag[1:-1] = -b
    return N * numpy.fft.irfft(g, axis=axis)
