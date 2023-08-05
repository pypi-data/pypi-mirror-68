import math
import logging
from math import pi
from scipy.special import jn_zeros, jv, jvp
import numpy as np
from numpy import tensordot, outer, exp, expand_dims
import mathx
from mathx import last_axis, reshape_vec, abs_sqd
logger = logging.getLogger(__name__)
# TODO: create a sublcass with r_aperture stored (to save typing)


class QDHT:
    """Quasi-discrete Hankel transform.

    Described in:
    Yu, L.; Huang, M.; Chen, M.; Chen, W.; Huang, W. & Zhu, Z.
    Quasi-discrete Hankel transform
    Opt. Lett., OSA, 1998, 23, 409-411

    The only difference from Yu et al is that instead of r_1 and r_2 we use
    r and k, where k=2*pi*r_2 i.e. here we use angular frequency.

    Instances of QDHT are parameterized by single parameter N, the number of 
    sampling points. 

    For all functions, R is the aperture radius. dim is dimension along which
    r or k runs i.e. along which transforms are performed.

    For equal resolution/range in r and k, set R=self.j_Np1**0.5
    """

    def __init__(self, N=32):
        self.N = N
        self.roots = jn_zeros(0, N+1)
        self.j = self.roots[0:-1]
        self.j_Np1 = self.roots[-1]  # S in Yu et al.
        self.J1sqd = jv(1, self.j)**2
        self.C = 2*jv(0, outer(self.j, self.j)/self.j_Np1)/self.J1sqd

    def conj_R(self, R):
        return self.j_Np1/R

    def transform(self, E, R=1, axis=None):
        if axis == None:
            axis = last_axis(E)
        # Move working axis to last
        El = np.rollaxis(E, axis, E.ndim)
        # Inner product (sums along last axes)
        Elm = np.inner(El, self.C)/self.conj_R(R)**2
        # Move last axis back
        Em = np.rollaxis(Elm, -1, axis)
        return Em
        # return tensordot(self.C,E,(1,axis))/self.conj_R(R)**2

    def inv_transform(self, E, R=1, axis=None):
        return self.transform(E, self.conj_R(R), axis)

    def points(self, R=1, dim=-1):
        """Compute r sampling points."""
        return reshape_vec(self.j, dim)/self.j_Np1*R

    def conj_points(self, R=1, dim=-1):
        return self.points(self.conj_R(R), dim)

    def both_points(self, R=1, dim=-1):
        return self.points(R, dim), self.conj_points(R, dim)

    def scale_fac(self, R=1, dim=-1):
        """Parseval's theorem scaling vector.

        The scaling vector s_n such that
        sum_{n=0}^{N-1} abs(f(r_n))**2 s_n
        equals the norm-squared of the signal f(r_n), where r_n is given by QDHT.points.
        """
        return 4*pi*R**2/reshape_vec(self.j_Np1**2*self.J1sqd, dim)

    def conj_scale_fac(self, R=1, dim=-1):
        return self.scale_fac(self.conj_R(R), dim)
        # return 4*pi/R**2/reshape_vec(self.J1sqd,dim)

    def integrate(self, f, R=1, dim=-1, keepdims=False):
        """Integrate a functino over all radii.

        If A is the field (in units sqrt(intensity)) sampled at ht.points(R), then
        ht.integrate(abs(A)**2,R) returns transverse integrated power.

        Args:
            f: the function, sampled at hg.points(R), to be integrated
            R: the radial aperture size
            dim: the radius axis
            keepdims: whether to preserve the integrated-over dimension

        Returns:
            the integral
        """
        return (f*self.scale_fac(R, dim)).sum(dim, keepdims=keepdims)

    def conj_integrate(self, f, R=1, dim=-1, keepdims=False):
        return self.integrate(f, self.conj_R(R), dim, keepdims)

    def transform_to_arb(self, E, R, k, axis=None, deriv=0):
        """

        Args:
            E (array): input vector, with r running along axis
            R (scalar): input aperture
            k (array): transverse k to which to transform
            axis (int): axis along which r runs in E.
            deriv (int): derivative order to calculate

        Returns:

        """
        if axis == None:
            axis = last_axis(E)
        k = np.asarray(k)
        E = expand_dims(E, axis)
        # Now E.shape[axis]=1 and r runs along axis-1.
        if axis > -k.ndim:
            # If k spans axis, then to keep all dimensions aligned need to shift leading axes of k too. New axis in k
            # should be new r axis.
            k = expand_dims(k, axis-1)
        K = self.conj_R(R)
        j = mathx.reshape_vec(self.j, axis-1)
        J1sqd = mathx.reshape_vec(self.J1sqd, axis-1)

        def calc_Et(E, k):
            T = 2*jvp(0, k*j/K, deriv)*((j/K)**deriv/J1sqd)/K**2
            Et = (T*E).sum(axis-1)
            return (Et,)
        # shape returns 32 bit int, need 64 bit to avoid overflow
        working_size = np.prod(
            np.array(mathx.broadcasted_shape(E.shape, k.shape), dtype=np.int64))
        # TODO better available memory test
        size_threshold = 1e7
        if working_size > size_threshold and k.ndim > 0:
            chunk_axis = -k.ndim+np.argmax(k.shape)
            num_chunks = working_size/size_threshold
            chunk_length = int(math.ceil(k.shape[chunk_axis]/num_chunks))
            str = 'QDHT working size %g exceeds %g. Making %d chunks of length %d along axis %d ...'
            logger.info(3, str, working_size, size_threshold,
                       num_chunks, chunk_length, chunk_axis)
            # BUG! If E runs along chunk_axis too, then this fails.
            # Et=mathx.eval_array_fun_chunked(calc_Et_from_k,k,chunk_axis,chunk_length)
            # Et=mathx.iterate_broadcast_op(calc_Et,(E,k),chunk_axis,chunk_length)
            Et = mathx.eval_iterated(calc_Et, (E, k), iter_dims=(chunk_axis,), keep_iter_dims=True, iter_chunk_size=chunk_length,
                                     print_progress=logger.level < 3)[0]
            logger.info(3, '... QDHT done')
            return Et
        else:
            return calc_Et(E, k)[0]

    def inv_transform_to_arb(self, E, R, r, axis=None, deriv=0):
        return self.transform_to_arb(E, self.conj_R(R), r, axis, deriv)


if __name__ == "__main__":
    import pyqtgraph_extended as pg

    def test_self_trans(N=32, R=None):
        """Test self-transform of exp(-r**2/2)"""
        ht = QDHT(N)
        if R is None:
            # For same r and k axes
            R = ht.j_Np1**0.5
        r = ht.points(R)
        k = ht.conj_points(R)
        Er = exp(-r**2/2)
        print(ht.norm_squared(Er, R))
        Ek = ht.transform(Er, R)
        print(ht.conj_norm_squared(Ek, R))
        plt = pg.plot(r, Er)
        plt.plot(k, Ek, pen='r')

    def test_arb_trans():
        ##
        ht = QDHT(64)
        R = 5
        r = ht.points(R)
        k = ht.conj_points(R)
        Er = exp(-r**2/2)
        Ek = ht.transform(Er, R)
        Eka = ht.transform_to_arb(Er, R, k)
        assert np.allclose(Ek, Eka)
        Eka = ht.transform_to_arb(Er, R, mathx.reshape_vec(k, -3))
        assert np.allclose(Ek, Eka.squeeze()) and Eka.shape == (64, 1, 1)

        R = ht.j_Np1**0.5
        r = ht.points(R)
        k = ht.conj_points(R)
        Er = exp(-r**2/2)
        Erp = -r*exp(-r**2/2)
        plt = pg.plot(r, Erp, pen=pg.mkPen('b', width=10))
        plt.plot(k, ht.transform_to_arb(Er, R, k, deriv=1), pen='r')
        ##

    def test_wierd_shapes():
        ##
        ht = QDHT(16)
        for shape, axis in (((2, 3, 16, 4, 5), -3), ((16,), 0), ((16,), -1), ((2, 16), -1), ((2, 16), 1), ((16, 2), 0), ((16, 2), -2)):
            Er = np.ones(shape)
            Ek = ht.transform(Er, axis=axis)
            assert Ek.shape == Er.shape
        ##
    test_arb_trans()
    test_self_trans()
    test_self_trans(R=5)
    test_wierd_shapes()
