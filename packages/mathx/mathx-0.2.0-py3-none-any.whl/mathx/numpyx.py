from itertools import zip_longest

import numpy as np

def asscalar(x):
    """Like Numpy's asscalar but handles inputs that are already scalar."""
    return np.asarray(x).item()


def reshape_vec(vec, axis):
    """Reshape array to lie along given axis.

    If axis>=0, reshapes vec to (1,...,1,n) where the number of ones is axis and
    n is the number of elements. If axis<0, reshapes vec to (n,1,..,1) where
    the number of ones is -(axis+1)."""
    vec = np.array(vec)
    if axis >= 0:
        return vec.reshape((1,)*axis + (-1,))
    else:
        return vec.reshape((-1,) + (1,)*-(axis + 1))


def vector_dim_shape(shape):
    """Returns the dimension (negative) spanned by a vector of given shape.
    ValueError if more
    than one dimension is greater than 1. If no dimensions greater than 1, returns
    the leftmost."""
    ndim = len(shape)
    dims = np.greater(shape, 1).nonzero()[0] - ndim
    if dims.size > 1:
        raise ValueError('Multiple dimensions ' + str(dims) + ' great than 1.')
    if dims.size == 0:
        return -ndim
    else:
        return dims[0]


def vector_dim(a):
    """Returns the dimension (negative) spanned by a vector. ValueError if more
    than one dimension is greater than 1. If no dimensions greater than 1, returns
    the leftmost."""
    return vector_dim_shape(np.asarray(a).shape)


def nonzero_vec(vec):
    """Nonzero elements of vec as a vector along the dimension of vec.

    Useful for advanced indexing.
    """
    vec = np.asarray(vec)
    dim = vector_dim(vec)
    return reshape_vec(vec.nonzero()[dim], dim)


def expand_dims(k, axis):
    """Like np.expand_dims, but corrects weird numpy behaviour.

    I found that:
    np.expand_dims(np.zeros((3,2)),-4).shape
    gives
    (3,1,2)
    which doesn't make much sense.

    This function calls expand dims if axis is spanned by k, otherwise returns
    k doing nothing.
    """
    if -k.ndim <= axis <= k.ndim:
        return np.expand_dims(k, axis)
    else:
        return k


def squeeze_leading(x):
    """Squeeze leading singleton dimensions."""
    x = np.asarray(x)
    n = next((n for n in range(x.ndim) if x.shape[n] > 1), x.ndim)
    x = np.squeeze(x, tuple(range(n)))
    if x.ndim == 0:
        x = x.item()
    return x


def insert_dim(a, axis):
    # Not sure if this function is really necessary
    if axis >= 0 or axis < 0 and -axis <= a.ndim:
        return np.expand_dims(a, axis)
    else:
        return a


def argmax(a, axis=-1):
    """Indices of maximum value along given axis.
    Differs from numpy.argmax in that axis isn't removed from the shape."""
    return np.expand_dims(np.argmax(a, axis), axis)


def ind_closest(array, value, axis=None):
    """Element in array closest to the scalar value."""
    idx = np.abs(array - value).argmin(axis)
    if axis is not None:
        idx = insert_dim(idx, axis)
    return idx


def broadcasted_shape(*shapes):
    shape = []
    for lengths in zip_longest(*[shape[::-1] for shape in shapes], fillvalue=1):
        max_length = max(lengths)
        assert all(length == 1 or length == max_length for length in lengths)
        shape.append(max_length)
    return tuple(shape[::-1])


def are_shapes_broadcastable(*shapes):
    """Test if shapes are Numpy broadcastable."""
    for lengths in zip_longest(*[shape[::-1] for shape in shapes], fillvalue=1):
        max_length = max(lengths)
        if not all(length == 1 or length == max_length for length in lengths):
            return False
    return True


def are_broadcastable(*arrays):
    return are_shapes_broadcastable(*[np.shape(array) for array in arrays])


def shapes_equal_trailing(*shapes):
    """Test if shapes are equal, starting from trailing end, except for leading ones."""
    for lengths in zip_longest(*[shape[::-1] for shape in shapes], fillvalue=1):
        if not all(length == lengths[0] for length in lengths):
            return False
    return True


def set_shape_element(shape, index, value):
    """Set element of shape tuple, adding ones if necessary.
    Examples:
        set_shape_element((2,3),2,4)=(2,3,1,4)
        set_shape_element((2,3),-4,4)=(4,1,2,3)
    """
    if index >= 0:
        return shape[:index] + (1,)*(index - len(shape)) + (value,) + shape[index + 1:]
    else:
        if index == -1:
            trailing = ()
        else:
            trailing = shape[index + 1:]
        return shape[:index] + (value,) + (1,)*(-index - len(shape) - 1) + trailing


def broadcasted_size_along(shape, axis):
    assert axis < len(shape), 'Only makes sense axis less than number of dimensions (including negative)'
    if axis >= 0:
        return shape[axis]
    elif -axis <= len(shape):
        return shape[axis]
    else:
        return 1


def all_axes_except(ndim, axis):
    return tuple(range(-ndim, axis)) + tuple(range(axis + 1, 0))


def off_diag(a):
    """Return off-diagonal elements of array. TODO: semantics for >2 dimensions"""
    n = np.arange(min(a.shape))
    return a[n[:, None] != n]


def flip(a, axis):
    """Flip array along arbitrary axis."""
    a = np.asarray(a)
    if axis >= 0:
        return a[(slice(None),)*axis + (slice(None, None, -1), Ellipsis)]
        #a[[slice(None)]*axis + [slice(None, None, -1)] + [Ellipsis]]
    elif -axis <= a.ndim:
        return a[(Ellipsis, slice(None, None, -1)) + (slice(None),)*(-axis - 1)]
        #a[[Ellipsis] + [slice(None, None, -1)] + [slice(None)]*(-axis - 1)]
    else:
        return a


def gal(x, a, b):
    return (x > a) & (x < b)


def geale(x, a, b):
    """Greater than or equal to and less than or equal to."""
    return (x >= a) & (x <= b)


def abs_sqd(x):
    return np.real(x*np.conj(x))


def norm_max(x, axis=None):
    return x/np.amax(x, axis, keepdims=True)


def norm_sum(x, axis=None):
    return x/np.sum(x, axis, keepdims=True)


def last_axis(a):
    """Negative index of last nonsingleton axis of an array
        e.g. if a has shape (1,3,4,1) then last_axis(a) returns -2"""
    return np.nonzero(np.array(a.shape) != 1)[0][-1] - a.ndim


def diff(x, n=1, axis=None):
    """Central finite difference with non-centred for at edges.

    Returns:
        array: same size as x
    """
    if axis is None:
        axis = last_axis(x)
    x = np.swapaxes(x, axis, 0)
    for _ in range(n):
        x = np.concatenate((x[[1]] - x[[0]], (x[2:] - x[:-2])/2, x[[-1]] - x[[-2]]), 0)
    return np.swapaxes(x, axis, 0)


def diff_arb(x, y, axis=None):
    """Finite difference for non-uniformly sampled array. TODO boundary values"""
    if axis == None:
        axis = last_axis(x)
    x = np.swapaxes(x, axis, -1)
    y = np.swapaxes(y, axis, -1)
    x0 = x[..., :-2]
    x1 = x[..., 1:-1]
    x2 = x[..., 2:]
    y0 = y[..., :-2]
    y1 = y[..., 1:-1]
    y2 = y[..., 2:]
    f = (x2 - x1)/(x2 - x0)
    return np.swapaxes((1 - f)*(y2 - y1)/(x2 - x1) + f*(y1 - y0)/(x1 - x0), axis, -1)



def take_broadcast_inds(shape, inds, axis):
    """Object for indexing along given axis with broadcasting shape.

    This  function returns a selection object for taking indices inds of
    an array of shape along axis. The difference from numpy.take is in the
    treatment of multidimensional inds. Instead of replacing shape[axis] with
    inds.shape in the shape of the result (as in the numpy docs example below),
    this function broadcasts inds with shape.

    From the numpy docs:
        Let x.shape be (10,20,30,40,50) and suppose ind_1 and ind_2 can be
        broadcast to the shape (2,3,4). Then x[:,ind_1,ind_2] has shape
        (10,2,3,4,40,50) because the (20,30)-shaped subspace from X has been
        replaced with the (2,3,4) subspace from the indices.
    """
    if axis >= 0:
        axis = axis - len(shape)
    bc_inds = tuple((reshape_vec(range(shape[n]), n) if n != axis else inds) for n in range(-len(shape), 0))
    return bc_inds


def take_broadcast(array, inds, axis=None):
    if axis is None:
        axis = vector_dim(array)
    return array[take_broadcast_inds(array.shape, inds, axis)]




def find_first_nonzero(x, axis=None):
    """Find indices of first nonzero element along given axis.

    Where there is no nonzero element, the size of x along axis is returned.
    """
    x = np.asarray(x)
    if axis is None:
        axis = vector_dim(x)
    nz = x != 0
    res = nz.argmax(axis)
    res = np.expand_dims(res, axis)
    no_nz = ~nz.any(axis, keepdims=True)
    res[no_nz] = broadcasted_size_along(x.shape, axis)
    # res=squeeze_leading(res)
    return res


def find_last_nonzero(x, axis=None):
    """Find indices of last nonzero element along given axis.

    Where there is no nonzero element, -1 is returned."""
    x = np.asarray(x)
    if axis is None:
        axis = vector_dim(x)
    xf = flip(x, axis)
    resf = find_first_nonzero(xf, axis)
    sx = broadcasted_size_along(x.shape, axis)
    res = sx - 1 - resf
    return res

def dot_along(x, y, axis, keepdim=False):
    if keepdim:
        return sum(x.take([n], axis)*y.take([n], axis) for n in range(x.shape[axis]))
    else:
        return sum(x.take(n, axis)*y.take(n, axis) for n in range(x.shape[axis]))


def mat_mult_along(x, y, axis_x, axis_y=None):
    """Multiply matrices spanning arbitrary axes.

    Returns (sum over n)(x_n*y_n) where n runs of axis_x in x and axis_y in y.

    Args:
        x (array): left matrix
        y (array): right matrix
        axis_x (int): axis of x along which to sum
        axis_y (int): axis of y along which to sum. Defaults to axis_x+1

    Returns:
        matrix product
    """
    if axis_y is None:
        axis_y = axis_x + 1
    assert x.shape[axis_y] == y.shape[axis_x]
    return sum(x.take([n], axis_y)*y.take([n], axis_x) for n in range(x.shape[axis_y]))


def wrap_to_pm(x, to):
    """Wrap x to [-to,to)."""
    return (x + to)%(2*to) - to


def wrap_to_pmh(x, to2):
    """Wrap x to [-to/2,to/2)."""
    to = to2/2
    return (x + to)%to2 - to


def zero_mod_2pi(x):
    """Test if x wrapped to (-pi,pi) is close to zero"""
    return np.allclose(wrap_to_pm(x, np.pi), 0)


def unwrap(p, ind_fixed=0, axis=-1):
    """Unwrap phase, preserving value at given index.
    Args:
        p (array): phase to unwrap
        ind_fixed (int): index along the unwrap axis to preserve the value of
        axis (int): axis along which to unwrap.
    Returns:
        array: unwrapped phase
    """
    pu = np.unwrap(p, axis=axis)
    pu += p.take([ind_fixed], axis) - pu.take([ind_fixed], axis)
    return pu


def divide0(a, b, result=0):
    """Division with quotient=result when divisor is zero.
    http://stackoverflow.com/questions/26248654/numpy-return-0-with-divide-by-zero
    """
    with np.errstate(divide='ignore', invalid='ignore'):
        c = np.asarray(np.true_divide(a, b))
        c[~ np.isfinite(c)] = result  # -inf inf NaN
    return c


def round_to_multiple(x, a):
    """Round x to nearest multiple of a"""
    return a*np.round(x/a)


def round_to_odd_multiple(x, a):
    return a*(2*round((x - a)/(2*a)) + 1)


def allclose(a,b,atol_frac=1e-5,rtol=1e-5,atol=1e-8,equal_nan=False):
    nones=sum(x is None for x in (a,b))
    if nones==2:
        return True
    elif nones==1:
        return False
    atol=max(atol,max(np.max(a),np.max(b))*atol_frac)
    return np.allclose(a,b,rtol=rtol,atol=atol,equal_nan=equal_nan)

def multiply_and_sum(factors,axes,keepdims=False):
    """Equivalent to sum(factors[0]*factors[1]*...,axes,keepdims=keeepdims)."""
    if not isinstance(axes,tuple):
        axes=(axes,)
    assert np.all(axis<0 for axis in axes)
    assert all(np.ndim(factor)<=26 for factor in factors)
    def make_str(ndim):
        return ''.join(chr(ord('z')+1-ndim+n) for n in range(ndim))
    input_subscripts=','.join(make_str(np.ndim(factor)) for factor in factors)
    output_subscripts=''.join(chr(ord('z')+1+n) for n in range(-max(np.ndim(factor) for factor in factors),0) if n not in axes)
    subscripts=input_subscripts+'->'+output_subscripts
    output=np.einsum(subscripts,*factors)
    if keepdims:
        for axis in sorted(axes,reverse=True):
            output=np.expand_dims(output,axis)
    return output