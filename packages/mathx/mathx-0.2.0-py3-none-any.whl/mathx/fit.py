"""General mathematical functions"""
import numpy as np
import math
from scipy.interpolate import krogh_interpolate, interp1d
import scipy.special
from scipy import optimize
import mathx as mx


def gaussian(peak, mu, sigma):
    def f(x):
        return peak*np.exp(-(x - mu)**2/(2*sigma**2))

    return f


def fit_gaussian(x, f):
    # Don't want NaNs for initial guess.
    mu_0, sigma_0 = mx.mean_and_std(x, abs(f))
    peak_0 = max(f)

    def err_fun(params):
        return gaussian(*params)(x) - f

    params, success = optimize.leastsq(err_fun, np.array((peak_0, mu_0, sigma_0)))
    return params


def fit_sparse_1d_poly(x, y, f, pows):
    """Fit a sparse polynomial - one with a given set of terms.

    Returns the vector c such that the polynomial p(x)=sum_n c[n] x^{pows[n]} is
    the least-squares fit to the set of points (x,y), weighted by f. Broadcasting
    is allowed, so x, y, and f could define the axes and data of an image.

    Args:
        x (array): x axis
        y (array): y axis
        f (array): function to fit to
        pows (sequence): powers of x

    Returns:
        array: the coefficients c

    Derivation:
        Have f(x,y). Want to fit y=p(x) where p(x)=sum_n c_n x^{b_n}. Want stationary
        points of
            sum f(x,y)(y-p(x))^2
        i.e. zeros of
            sum f(x,y)(y-p(x))dpdc_m(x)
            = sum f(x,y)(y- sum_n c_n x^{b_n})x^{b_m}
            sum f(x,y)yx^{b_m}= sum_n f(x,y) x^{b_n} x^{b_m} c_n
    """
    x = np.asarray(x)
    y = np.asarray(y)
    N = len(pows)
    mat = np.zeros((N, N))
    rhs = np.zeros(N)
    for m in range(N):
        for n in range(N):
            if m > n:
                mat[m, n] = mat[n, m]
            else:
                mat[m, n] = (f*x**(pows[m] + pows[n])).sum()
        rhs[m] = (f*y*x**pows[m]).sum()
    c = np.linalg.solve(mat, rhs)
    return c


def calc_2d_correction_factors(m1, m2, tolerance=1e-6, max_iterations=1e6):
    """Calculate row- and column- dependent factors that when applied to m2 minimize its mean-square deviation from m1."""
    N, M = m1.shape
    assert m2.shape == (N, M)
    fr = np.ones(N)[:, None]
    fc = np.ones(M)
    num_iterations = 0
    while num_iterations < max_iterations:
        frl = fr
        fcl = fc
        fr = (m1*m2*fc).sum(1, keepdims=True)/(m2**2*fc**2).sum(1, keepdims=True)
        fc = (m1*m2*fr).sum(0)/(m2**2*fr**2).sum(0)
        if ((((fr - frl)**2).sum()/(fr**2).sum() + ((fc - fcl)**2).sum())/(fc**2).sum()) < tolerance:
            break
        num_iterations += 1
    return fr, fc, num_iterations
