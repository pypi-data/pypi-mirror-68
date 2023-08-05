import numpy as np
import scipy
import mathx

def interp_at(x, y, x_0, der=0, axis=None):
    x = np.array(x)
    y = np.array(y)
    if axis == None:
        axis = mathx.last_axis(x)
    i_0 = np.abs(x - x_0).argmin()
    i_s = max(i_0 - 1, 0)
    i_m = min(i_0 + 2, x.shape[axis])
    return scipy.interpolate.krogh_interpolate(x[..., i_s:i_m], y[..., i_s:i_m], x_0, der)


class interp1d_rect:
    def __init__(self, x, y, kind='linear', axis=-1, copy=True, bounds_error=None, fill_value=float('nan'),
            assume_sorted=False):
        self.real = scipy.interpolate.interp1d(x, y.real, kind, axis, copy, bounds_error, fill_value, assume_sorted)
        self.imag = scipy.interpolate.interp1d(x, y.imag, kind, axis, copy, bounds_error, fill_value, assume_sorted)

    def __call__(self, xi):
        return self.real(xi) + 1j*self.imag(xi)


class interp1d_polar:
    def __init__(self, x, y, kind='linear', axis=-1, copy=True, bounds_error=None, fill_value=float('nan'),
            assume_sorted=False):
        self.abs = scipy.interpolate.interp1d(x, abs(y), kind, axis, copy, bounds_error, fill_value, assume_sorted)
        self.phi = scipy.interpolate.interp1d(x, np.unwrap(np.angle(y), axis=axis), kind, axis, copy, bounds_error,
                                              fill_value, assume_sorted)

    def __call__(self, xi):
        return self.abs(xi)*np.exp(1j*self.phi(xi))

def get_frac_inds(x, xp, axis=None, suppress_degeneracy_error=False):
    """Get fractional indices using linear interpolation.

    For any xp outside the range of x, linear extrapolation based on the closest
    two values of x is used. If these two values are equal, then an inf will result.

    Result is array with squeezed leading dimensions.

    Args:
        x (array): must be nondecreasing along axis.
    """
    x = np.asarray(x)
    if axis is None:
        axis = mathx.vector_dim(x)
    # Because we iterate over xp along axis, it needs to have this dimension
    xp_ndim_orig = np.ndim(xp)
    xp = np.array(xp, ndmin=-axis)
    lx = mathx.broadcasted_size_along(x.shape, axis)

    def get_xixpt(xpi):
        xpt = mathx.take_broadcast(xp, [xpi], axis)
        # Find index of xb, the last value of x which is less than or equal to xpt
        xib = mathx.find_last_nonzero(x <= xpt, axis)
        # Find index of xa, the first value of x which is greater than xpt
        xia = mathx.find_first_nonzero(x > xpt, axis)
        # If all elements of x are greater than xpt, use zeroth and first i.e.
        # linearly extrapolate
        inds = xib == -1
        xib[inds] = 0
        xia[inds] = 1
        # Likewise if all elements of x are smaller than or equal to xpt, use
        # second last and last elements
        inds = xia == lx
        xib[inds] = lx - 2
        xia[inds] = lx - 1
        # Get before and after values of x
        xb = mathx.take_broadcast(x, xib, axis)
        xa = mathx.take_broadcast(x, xia, axis)
        Dx = xa - xb
        if suppress_degeneracy_error:
            delta = mathx.divide0(xpt - xb, Dx)
        else:
            assert Dx.min() > 0
            delta = (xpt - xb)/Dx
        xixpt = xib + delta
        return xixpt

    xixp = mathx.concatenate([get_xixpt(xpi) for xpi in range(mathx.broadcasted_size_along(xp.shape, axis))], axis)
    if xixp.ndim == -axis and xixp.shape[axis] == 1 and xixp.ndim > xp_ndim_orig:
        # The axis over which we interpolated is the leading one, and has length 1 i.e. wasn't spanned by xp. Therefore
        # its presence is an 'artefact' of the interpolation and it should be removed.
        xixp = xixp[0]
    return xixp

def interpolating_matrix(f, n):
    """Compute matrix representing interpolation given interpolation function.

    The interpolation problem is to resample (x,y) to the points xi producing yi.
    This function takes an existing interpolation method and represents it as a
    matrix M such that yi=M*y. This works provided the method is linear. Nearest
    neighbour, linear interpolation and spline interpolation all fall into this
    category.

    Args:
        f (function): y->yi
        n: length of x
    """

    def column(j):
        y = np.zeros(n)
        y[j] = 1
        yi = f(y)
        return yi

    yi = np.array([column(j) for j in range(n)]).T
    return yi


class Interp1D:
    def __init__(self, x, xi, axis=None, extrap=False):
        x = np.asarray(x)
        if axis is None:
            axis = mathx.vector_dim(x)
        neps = get_frac_inds(x, xi, axis)
        n = np.clip(np.floor(neps).astype(int), 0, x.shape[axis] - 2)
        eps = neps - n
        if not extrap:
            eps = np.clip(eps, 0, 1)
        self.n = n
        self.eps = eps
        self.axis = axis

    def __call__(self, y):
        return interp1d_n_eps(y, self.n, self.eps, self.axis)


def interp1d(x, y, xi, axis=None, extrap=False, assume_x_uniform=False):
    """

    Args:
        x:
        y:
        xi:
        axis:
        extrap:
        assume_x_uniform (bool): if x is uniformly spaced.

    Returns:

    """
    if assume_x_uniform:
        yi = interp1d_assume_uniform(x, y, xi, axis, extrap)
    else:
        yi = Interp1D(x, xi, axis, extrap)(y)
    return yi


def interp1d_to_uniform(x, y, axis=None):
    """Resample array to uniformly sampled axis.

    Has some limitations due to use of scipy interp1d.

    Args:
        x (vector): independent variable
        y (array): dependent variable, must broadcast with x
        axis (int): axis along which to resample

    Returns:
        xu: uniformly spaced independent variable
        yu: dependent resampled at xu
    """
    x = np.asarray(x)
    y = np.asarray(y)
    if axis is None:
        axis = mathx.vector_dim(x)
    num = x.shape[axis]
    mn = x.min(axis, keepdims=True)
    mx = x.max(axis, keepdims=True)
    # Limitation of scipy interp1d
    x = x.squeeze()
    mn = mn.squeeze()
    mx = mx.squeeze()
    assert x.ndim == 1
    xu = np.arange(num)/(num - 1)*(mx - mn) + mn
    yu = scipy.interpolate.interp1d(x.squeeze(), y, axis=axis, bounds_error=False)(xu)
    return mathx.reshape_vec(xu, axis), yu


def interp1d_n_eps(y, n, eps, axis):
    """Interpolate array at index specified by integer and offset.

    Args:
        y (array): to interpolate
        n (array of int): index, must be 0<=n<=y.shape[axis]-2.
        eps (array of float): offset. If outside [0,1], extrapolation is performed implicitly.

    Returns:
        array: y sampled at n+eps
    """
    return mathx.take_broadcast(y, n, axis)*(1 - eps) + mathx.take_broadcast(y, n + 1, axis)*eps


class Interp1DUniform:
    def __init__(self, x0, Dx, N, axis, xi, extrap=True):
        """
        Args:
            axis (int): interpolation axis. If None, chooses based on y, which in that
                case must be a vector.
            extrap (bool): if True, use linear extrapolation based on the extreme values.
                If false, nearest neighbour is used for extrapolation instead.
        """
        xi = np.array(xi, ndmin=1, copy=False)
        nf = (xi - x0)/Dx
        n = np.floor(nf).astype(int)
        n[n >= N - 1] = N - 2
        n[n < 0] = 0
        eps = nf - n
        if not extrap:
            eps = np.clip(eps, 0, 1)
        self.n = n
        self.eps = eps
        self.axis = axis

    def __call__(self, y):
        return interp1d_n_eps(y, self.n, self.eps, self.axis)


def interp1d_assume_uniform(x, y, xi, axis=None, extrap=True):
    x = np.asarray(x)
    if axis is None:
        axis = mathx.vector_dim(x)
    x0 = x.take([0], axis)
    Dx = x.take([1], axis) - x0
    yi = interp1d_lin_reg(x0, Dx, y, xi, axis, extrap)
    return yi


def interp1d_lin_reg(x0, Dx, y, xi, axis=None, extrap=True):
    """
    Args:
        axis (int): interpolation axis. If None, chooses based on y, which in that
            case must be a vector.
        extrap (bool): if True, use linear extrapolation based on the extreme values.
            If false, nearest neighbour is used for extrapolation instead.
    """
    y = np.asarray(y)
    if axis is None:
        axis = mathx.vector_dim(y)
    interp = Interp1DUniform(x0, Dx, y.shape[axis], axis, xi, extrap)
    return interp(y)


def interp1d_frac_ind(y, xi, axis=None):
    """Lookup/resample array at fractional indices using linear interpolation.

    Args:
        y: array to resample
        xi: fractional indices
        axis (int): axis indexed by xi

    Returns:
        y indexed at xi
    """
    return interp1d_lin_reg(0, 1, y, xi, axis)

