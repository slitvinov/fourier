import numpy
import ft
n = 28
f = numpy.random.random((n, n))

a, b = ft.ft(f, axis = 0)
aa, ab = ft.ft(a, axis = 1)
ba, bb = ft.ft(b, axis = 1)

a0 = ft.ift(aa, ab)
b0 = ft.ift(ba, bb)
f0 = ft.ift(a0, b0, axis = 0)

assert numpy.allclose(a, a0)
assert numpy.allclose(b, b0)
assert numpy.allclose(f, f0)
print(f0.shape)
