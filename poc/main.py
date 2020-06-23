import numpy
import math

#f = numpy.random.random(4)
f = numpy.arange(6)
g = numpy.fft.rfft(f)
f0 = numpy.fft.irfft(g)

#print(numpy.allclose(scipy.fftpack.ifft(y), f0))
print(numpy.allclose(f, f0))
