import numpy
import ft
n = 28
f = numpy.random.random((n, n))

a, b = ft.ft(f)

aa, ab = ft.ft(a, axis = 0)
#ba, bb = ft.ft(b, axis = 0)

print(aa.shape)
