import math
import numpy as np
from . import divide0

def _sph_harm_norm(order, degree):
    """Normalization factor for spherical harmonics"""
    # we could use scipy.special.poch(degree + order + 1, -2 * order)
    # here, but it's slower for our fairly small degree
    norm = np.sqrt((2*degree + 1.)/(4*np.pi))
    if order != 0:
        norm *= np.sqrt(math.factorial(degree - order)/float(math.factorial(degree + order)))
    return norm


def _sph_harm(order, degree, az, pol, norm=True):
    """Evaluate point in specified multipolar moment. [1]_ Equation 4.
    When using, pay close attention to inputs. Spherical harmonic notation for
    order/degree, and theta/phi are both reversed in original SSS work compared
    to many other sources. See mathworld.wolfram.com/SphericalHarmonic.html for
    more discussion.
    Note that scipy has ``scipy.special.sph_harm``, but that function is
    too slow on old versions (< 0.15) for heavy use.
    Parameters
    ----------
    order : int
        Order of spherical harmonic. (Usually) corresponds to 'm'.
    degree : int
        Degree of spherical harmonic. (Usually) corresponds to 'l'.
    az : float
        Azimuthal (longitudinal) spherical coordinate [0, 2*pi]. 0 is aligned
        with x-axis.
    pol : float
        Polar (or colatitudinal) spherical coordinate [0, pi]. 0 is aligned
        with z-axis.
    norm : bool
        If True, include normalization factor.
    Returns
    -------
    base : complex float
        The spherical harmonic value.
    """
    from scipy.special import lpmv

    # Error checks
    if np.abs(order) > degree:
        raise ValueError('Absolute value of order must be <= degree')
    # Ensure that polar and azimuth angles are arrays
    az = np.asarray(az)
    pol = np.asarray(pol)
    if (np.abs(az) > 2*np.pi).any():
        raise ValueError('Azimuth coords must lie in [-2*pi, 2*pi]')
    if (pol < 0).any() or (pol > np.pi).any():
        raise ValueError('Polar coords must lie in [0, pi]')
    # This is the "seismology" convention on Wikipedia, w/o Condon-Shortley
    if norm:
        norm = _sph_harm_norm(order, degree)
    else:
        norm = 1.
    return norm*lpmv(order, degree, np.cos(pol))*np.exp(1j*order*az)


def sph_harm(l, m, theta, phi):
    """Spherical harmonic using Wikipedia definition, Y^m_l(theta,phi)"""
    return _sph_harm(m, l, phi, theta)


def real_sph_harm(l, m, theta, phi):
    """Real-valued spherical harmonics, Wikipedia definition Y_{lm}(theta,phi)."""
    if m < 0:
        return 1j/2**0.5*(sph_harm(l, m, theta, phi) - (-1)**m*sph_harm(l, -m, theta, phi))
    elif m == 0:
        return sph_harm(l, 0, theta, phi)
    else:
        return 1/2**0.5*(sph_harm(l, -m, theta, phi) + (-1)**m*sph_harm(l, m, theta, phi))

def log10_bounded(x):
    """log10 with non-positive values set to lowest positive value"""
    x=np.array(x)
    xe0=x<=0
    x[xe0]=abs(x[~xe0]).min()
    return np.log10(x)


def slowing(k, a=1):
    """Identity function except it varies slowly around k=0.

    The parameter a is the scale over which the slowdown occurs:
        slowing(a,a)=a/2
    """
    return k/(a**2*divide0(1, k**2) + 1)


def gegenbauer(alpha, n, x):
    """Return nth order Gegenbauer polynomial with weight function (1-x**2)**(alpha-0.5).

    The difference between this and scipy.special.gegenbauer is that here one
    passes the value for which the polynomial is evaluated. This makes it compatible
    with sympy.
    """
    if n == 0:
        return 1
    elif n == 1:
        return 2*alpha*x
    else:
        return (2*x*(n + alpha - 1)*gegenbauer(alpha, n - 1, x) - (n + 2*alpha - 2)*gegenbauer(alpha, n - 2, x))/n