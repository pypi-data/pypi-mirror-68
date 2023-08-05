import numba
import numpy as np
import math

__all__ = ['expj', 'abs_sqd', 'sum_abs_sqd_1d', 'sum_abs_sqd']

@numba.vectorize([numba.complex64(numba.float64)], nopython=True, cache=True)
def expj(x):
    return math.cos(x) + 1j*math.sin(x)

@numba.vectorize(cache=True)  # ([numba.float64(numba.complex128),numba.float32(numba.complex64)])
def abs_sqd(x):
    return x.real**2 + x.imag**2


@numba.jit(cache=True)
def sum_abs_sqd_1d(x, cache=True):
    r = 0
    for i in range(len(x)):
        xi = x[i]
        r += xi.real**2 + xi.imag**2
    return r

def sum_abs_sqd(x):
    return sum_abs_sqd_1d(np.ravel(x))