import scipy.fftpack
import numpy
import math

f = numpy.random.random(12)
g = scipy.fftpack.fft(f)
def ft(f):
    n = f.size
    assert n % 2 == 0
    N = n // 2
    a = numpy.empty_like(f)
    b = numpy.empty_like(f)
    for m in range(2 * N):
        a[m] = 0
        b[m] = 0
        for x in range(2 * N):
            om = numpy.pi/N*m*x
            a[m] += f[x] * math.cos(om)
            b[m] += f[x] * math.sin(om)
    return a, b

def ift(f):
    n = f.size
    assert n % 2 == 0
    N = n // 2
    a = numpy.empty_like(f)
    b = numpy.empty_like(f)
    for m in range(2 * N):
        a[m] = 0
        b[m] = 0
        for x in range(2 * N):
            om = numpy.pi/N*m*x
            a[m] += f[x] * math.cos(om)
            b[m] += f[x] * math.sin(om)
    return a/n, b/n

a, b = ft(f)
y = a - 1j * b

a, b = ift(y)
f0 = a + 1j * b

print(numpy.allclose(scipy.fftpack.ifft(y), f0))
print(numpy.allclose(f, f0))
