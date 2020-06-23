import scipy.fftpack
import numpy
import math

f = numpy.random.random(100)
g = scipy.fftpack.fft(f)
def ft(f):
    n = f.size
    assert n % 2 == 0
    N = n // 2
    a = numpy.zeros_like(f)
    b = numpy.zeros_like(f)
    for m in range(2 * N):
        for x in range(2 * N):
            om = numpy.pi/N*m*x
            a[m] += f[x] * math.cos(om)
            b[m] += f[x] * math.sin(om)
    return a, b

def ift(a, b):
    n = f.size
    assert n % 2 == 0
    N = n // 2
    y = numpy.zeros_like(f)
    for m in range(2 * N):
        for x in range(2 * N):
            om = numpy.pi/N*m*x
            y[x] += a[m] * math.cos(om)
            y[x] += b[m] * math.sin(om)
    return y/n

a, b = ft(f)
y = a - 1j * b

f0 = ift(a, b)

#print(numpy.allclose(scipy.fftpack.ifft(y), f0))
print(numpy.allclose(f, f0))
