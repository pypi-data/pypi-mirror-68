import numpy as np
import mathx as mx
# import pyqtgraph_extended as pg
import scipy.interpolate


# import sympy

def test_index():
    assert (mx.index(7, 2, 0) == 7)
    assert (np.array_equal(mx.index_multi([5], [[[2, 3, 4]]], [-1]), [[5]]))
    try:
        mx.index([0, 1], 2, 0)
    except IndexError:
        pass
    else:
        raise AssertionError()


def test_iterate_broadcast_op_multi():
    x = mx.reshape_vec(np.arange(2), -2)
    y = mx.reshape_vec(np.arange(3), -3)
    z = mx.reshape_vec(np.arange(4), -4)
    k = mx.reshape_vec(np.arange(5), -5)

    def f(x, y, z):
        return x + y + z + k

    for axes in [[-2, -4], [-3, -2], [-2]]:
        r = mx.iterate_broadcast_op_multi(f, [x, y, z], axes, print_prog=True)
        print(np.all(r == f(x, y, z)))
    k = np.arange(5)

    def f(x, y, z):
        return x + y + z + k

    for axes in [[0, 1], [2]]:
        r = mx.iterate_broadcast_op_multi(f, [x, y, z], axes, print_prog=True)
        print(np.all(r == f(x, y, z)))


def test_interp1d_lin_reg():
    print(mx.interp1d_lin_reg(0, 1, [0, 1, 2], [0, 1, 2]))
    print(mx.interp1d_lin_reg(1., 2., [0., 1., 2.], [-1., 1., 2.]))


def test_interp1d_assume_uniform():
    x = np.linspace(5, 10, 23)
    yf = lambda x: 5*x + 2
    xi = np.random.random((2, 3))*5 + 5
    assert np.allclose(mx.interp1d_assume_uniform(x, yf(x), xi), yf(xi))


def test_take_broadcast():
    array = np.zeros((2, 1, 3, 4))
    assert mx.take_broadcast(array, np.zeros((1, 2, 3, 4), int), 1).shape == (2, 2, 3, 4)


def test_sph_harm():
    ##
    N = 10
    theta = np.random.rand(N)
    phi = np.random.rand(N)
    assert (all(np.isclose(mx.sph_harm(0, 0, theta, phi), 0.5*np.pi**(-0.5))))
    assert (all(np.isclose(mx.sph_harm(1, 0, theta, phi), 0.5*(3/np.pi)**(0.5)*np.cos(theta))))
    assert (all(np.isclose(mx.sph_harm(1, -1, theta, phi), 0.5*(3/(2*np.pi))**(0.5)*np.sin(theta)*np.exp(-1j*phi))))
    assert (all(np.isclose(mx.sph_harm(1, 1, theta, phi), -0.5*(3/(2*np.pi))**(0.5)*np.sin(theta)*np.exp(1j*phi))))
    assert (all(np.isclose(mx.real_sph_harm(0, 0, theta, phi), 0.5*np.pi**(-0.5))))
    assert (all(np.isclose(mx.real_sph_harm(1, -1, theta, phi), (3/(4*np.pi))**0.5*np.sin(theta)*np.sin(phi))))


def test_vectorize():
    ##
    def func_two_vectors(x, y):
        assert (x.ndim == 1 and y.ndim == 1 and len(x) == len(y))
        return x + y, y.max()

    x = np.arange(10)
    y = np.arange(11)[:, None]

    s, m = mx.eval_iterated(func_two_vectors, (x, y), [-1], broadcast_xs=True)
    assert (s.shape == (len(y), len(x)) and m.shape == (len(y), 1))

    s, m = mx.eval_iterated(func_two_vectors, (x, y), [-2], broadcast_xs=True)
    assert (s.shape == (len(y), len(x)) and m.shape == (1, len(x)))

    s, m = mx.eval_iterated(func_two_vectors, (x, y), iter_dims=[-1], broadcast_xs=True)
    assert (s.shape == (len(y), len(x)) and m.shape == (1, len(x)))

    s, m = mx.eval_iterated(func_two_vectors, (x, y), [-2], broadcast_xs=True)
    assert (s.shape == (len(y), len(x)) and m.shape == (1, len(x)))

    s, m = mx.eval_iterated(func_two_vectors, (x, y), iter_dims=[-1], broadcast_xs=True)
    assert (s.shape == (len(y), len(x)) and m.shape == (1, len(x)))

    z = np.arange(12)[:, None, None]

    def func_three_vectors(x, y, z):
        assert (x.ndim == 1 and y.ndim == 1 and z.ndim == 1 and len(x) == len(y) and len(y) == len(z))
        return (x + y + z, y.max())

    s, m = mx.eval_iterated(func_three_vectors, (x, y, z), [-1], broadcast_xs=True)
    assert (s.shape == (len(z), len(y), len(x)) and m.shape == (len(z), len(y), 1))

    s, m = mx.eval_iterated(func_three_vectors, (x, y, z), iter_dims=[-3, -2], broadcast_xs=True)
    assert (s.shape == (len(z), len(y), len(x)) and m.shape == (len(z), len(y), 1))

    def func_two_vectors(tx, ty):
        assert (tx.shape == (1, len(x)) and ty.shape == (1, len(x)))
        return (tx + ty, ty.max())

    s, m = mx.eval_iterated(func_two_vectors, (x, y), vec_dims=[-1], keep_iter_dims=True, broadcast_xs=True)
    assert np.array_equal(s, x + y)
    assert np.array_equal(m, y)

    iter_chunk_size = 2

    def func_two_vectors(tx, ty):
        return (tx + ty, ty - tx)

    s, m = mx.eval_iterated(func_two_vectors, (x, y), [-1], broadcast_xs=True, iter_chunk_size=iter_chunk_size,
                            keep_iter_dims=True)
    assert np.array_equal(s, x + y)
    assert np.array_equal(m, y - x)

    def func_two_vectors(tx, ty):
        assert (tx.shape == (len(y), 1) and ty.shape == (len(y), 1))
        return (tx + ty, ty.max())

    s, m = mx.eval_iterated(func_two_vectors, (x, y), vec_dims=[-2], keep_iter_dims=True, broadcast_xs=True)

    ##


# test_vectorize()
def test_peak_crossings_1D():
    ##
    x = np.arange(-10, 10, 0.01)
    FWHM = 3
    y = np.exp(-(x/(FWHM/1.6651))**2)
    b, a = mx.peak_crossings_1D(x, y)
    assert (abs(a - FWHM/2) < 1e-3 and abs(b + FWHM/2) < 1e-3)  ##


def test_peak_crossings():
    ##
    x = np.arange(-10, 10, 0.01)[:, None]
    FWHM = np.array([3, 4])
    y = np.exp(-(x/(FWHM/1.6651))**2)
    b, a = mx.peak_crossings(x, y)
    assert (np.all(abs(a - FWHM/2) < 1e-3) and np.all(abs(b + FWHM/2) < 1e-3))  ##


def test_dot_along():
    x = np.ones((2, 3, 4))
    y = np.ones((3, 2, 3, 4))
    assert np.array_equal(mx.dot_along(x, y, -2, True), np.ones((3, 2, 1, 4))*3)
    assert np.array_equal(mx.dot_along(x, y, -2, False), np.ones((3, 2, 4))*3)


def test_mat_mult_along():
    x = np.ones((5, 2, 3, 4))
    y = np.ones((2, 4, 7))
    assert np.array_equal(mx.mat_mult_along(x, y, -2), np.ones((5, 2, 3, 7))*4)


def test_peaks_iter_rmv():
    ##
    x = np.arange(1000)

    def peak(x_0, height, Dx):
        return height*np.exp(-((x - x_0)/Dx)**2)

    peaks = (200, 10, 5), (700, 30, 200), (500, 5, 30)
    y = sum(peak(x_0, height, Dx) for x_0, height, Dx in peaks)
    x_peaks = mx.find_peaks_iter_rmv(y, len(
        peaks) + 2)  # TODO can't have plotting here - maybe move to demo?  # plt=pg.plot(x,y)  # plt.plot(x[x_peaks],y[x_peaks],pen=None,symbol='o')  # ##  # x_peaks=find_peaks_iter_rmv(y,2)  # assert x_peaks==[700,513]  # plt=pg.plot(x,y)  # plt.plot(x[x_peaks],y[x_peaks],pen=None,symbol='o')  # ##  # x_peaks=find_peaks_iter_rmv(y,2,min_half_int=300)  # plt=pg.plot(x,y)  # plt.plot(x[x_peaks],y[x_peaks],pen=None,symbol='o')


def test_moment2():
    ##
    x = np.linspace(-50, 50)
    y = np.linspace(-60, 60, 100)[:, None]
    x0 = 5
    y0 = 2
    sx = 4
    sy = 3
    z = np.exp(-0.5*(((x - x0)/sx)**2 + ((y - y0)/sy)**2))

    assert np.isclose(mx.moment2(x, y, z, 1, 0), x0)
    assert np.isclose(mx.moment2(x, y, z, 0, 1), y0)
    assert np.isclose(mx.moment2(x - x0, y - y0, z, 2, 0), sx**2)
    assert np.isclose(mx.moment2(x - x0, y - y0, z, 0, 2), sy**2)
    assert np.isclose(mx.moment2(x - x0, y - y0, z, 1, 1), 0)

    assert np.allclose(mx.mean_and_variance2(x, y, z), (x0, y0, sx**2, sy**2, 0))


def test_diagonalize_2d_covariance():
    ##
    assert np.allclose(mx.diagonalize_2d_covariance(2, 1, 0), (2**0.5, 1, 0))
    assert np.allclose(mx.diagonalize_2d_covariance(1, 2, 0), (2**0.5, 1, np.pi/2))
    assert np.allclose(mx.diagonalize_2d_covariance(1, 1, 1), (2**0.5, 0, np.pi/4))  ##


def test_shapes_broadcastable():
    assert mx.are_shapes_broadcastable([1, 2], [1, 2])
    assert mx.are_shapes_broadcastable([1, 2], [1, 1, 2])
    assert mx.are_shapes_broadcastable([1, 2], [1, 2, 1])
    assert mx.are_shapes_broadcastable([3, 2, 6], [1, 2, 1])
    assert not mx.are_shapes_broadcastable([1, 2], [3])
    assert not mx.are_shapes_broadcastable([5, 1, 2, 3], [2, 1, 2, 3])

    assert mx.are_shapes_broadcastable([3, 1, 2], [1, 2, 1], [3, 2, 2])
    assert mx.are_shapes_broadcastable([3, 1, 2], [1, 2, 1], [3, 1, 2, 2])
    assert not mx.are_shapes_broadcastable([3, 1, 2], [4, 3, 2, 1], [3, 1, 2, 2])


def test_broadcasted_shape():
    assert mx.broadcasted_shape([1, 2], [2, 1]) == (2, 2)
    assert mx.broadcasted_shape((), (3, 2, 1)) == (3, 2, 1)
    assert mx.broadcasted_shape((3, 2, 1), (), (1, 2, 3), (6, 1, 1, 1)) == (6, 3, 2, 3)


def test_shapes_equal_trailing():
    assert mx.shapes_equal_trailing([1, 3, 2], [3, 2])
    assert not mx.shapes_equal_trailing([2, 3, 2], [3, 2])
    assert not mx.shapes_equal_trailing([1, 3, 2], [3, 2], [1, 1, 1, 2])
    assert mx.shapes_equal_trailing([1, 3, 2], [3, 2], [1, 1, 3, 2])


def test_set_shape_element():
    assert mx.set_shape_element((2, 3), 2, 4) == (2, 3, 4)
    assert mx.set_shape_element((2, 3), 0, 4) == (4, 3)
    assert mx.set_shape_element((2, 3), 3, 4) == (2, 3, 1, 4)
    assert mx.set_shape_element((2, 3), 4, 4) == (2, 3, 1, 1, 4)
    assert mx.set_shape_element((2, 3), -1, 4) == (2, 4)
    assert mx.set_shape_element((2, 3), -2, 4) == (4, 3)
    assert mx.set_shape_element((2, 3), -3, 4) == (4, 2, 3)
    assert mx.set_shape_element((2, 3), -4, 4) == (4, 1, 2, 3)
    assert mx.set_shape_element((2, 3), -5, 4) == (4, 1, 1, 2, 3)


def test_interp1d_to_uniform():
    ##
    x = np.linspace(1, 2)**2
    y = np.cos(x)
    xu, yu = mx.interp1d_to_uniform(x, y)
    Dxu = np.diff(xu)
    assert np.allclose(Dxu[0], Dxu)
    assert np.allclose(yu, np.cos(xu), rtol=1e-3)  ##


def test_interp1d():
    # Simple test
    x = np.arange(5)
    alpha = 0.5
    y = x*alpha
    xi = np.array([-0.5, 0.5, 4.5])
    yi = mx.interp1d(x, y, xi, extrap=True)
    yi2 = xi*alpha
    assert np.array_equal(yi, yi2)
    # Complex test
    Dx = np.arange(1, 3)
    n = np.arange(3)[:, None]
    x0 = np.arange(4)[:, None, None]
    alpha = np.arange(5)[:, None, None, None]
    x = x0 + n*Dx
    y = x*alpha
    xi = np.random.random((5, 4, 6, 2))
    yi = mx.interp1d(x, y, xi, axis=-2, extrap=True)
    yi2 = xi*alpha
    assert yi.shape == yi2.shape
    assert np.allclose(yi, yi2)


def test_interpolating_matrix():
    ##
    x = np.arange(10)
    xi = np.arange(0.5, 9.5, 0.5)

    def f(y):
        return scipy.interpolate.interp1d(x, y, 'cubic')(xi)

    m = mx.interpolating_matrix(f, len(x))
    y = np.random.rand(10)
    assert np.allclose(m.dot(y), f(y))


# TODO replace with non sympy-dependent
# def test_gegenbauer():
#     zeta=sympy.symbols("zeta")
#     assert (gegenbauer(1,3,zeta)-(8*zeta**3-4*zeta)).simplify()==0
#     assert (gegenbauer(2,2,zeta)-(12*zeta**2-2)).simplify()==0
##

def test_broadcasted_size_along():
    assert mx.broadcasted_size_along([3, 2], -1) == 2
    assert mx.broadcasted_size_along([3, 2], -2) == 3
    assert mx.broadcasted_size_along([3, 2], -3) == 1
    assert mx.broadcasted_size_along([3, 2], 0) == 3


def test_find_first_nonzero():
    assert mx.find_first_nonzero([0, 1, 0, 1]).item() == 1
    assert mx.find_first_nonzero([0, 0, 0, 0]).item()== 4
    assert np.array_equal(mx.find_first_nonzero([[0, 0, 1], [0, 1, 0]], 0), [[2, 1, 0]])
    assert np.array_equal(mx.find_first_nonzero([[0, 0, 1], [0, 1, 0]], 1), [[2], [1]])


def test_find_last_nonzero():
    assert mx.find_last_nonzero([0, 1, 0, 1]).item() == 3
    assert mx.find_last_nonzero([0, 0, 0, 0]).item() == -1
    assert np.array_equal(mx.find_last_nonzero([[0, 0, 1], [0, 1, 0]], 0), [[-1, 1, 0]])
    assert np.array_equal(mx.find_last_nonzero([[0, 0, 1], [0, 1, 0]], 1), [[2], [1]])


def test_get_frac_inds():
    assert mx.get_frac_inds([0, 1], 0.5) == [0.5]
    assert np.array_equal(mx.get_frac_inds([0, 1], [-0.5, 0, 0.5, 1, 1.5]), [-0.5, 0, 0.5, 1, 1.5])
    xi = [[-1, 0.5, 2], [2, 0.25, -1]]
    assert np.array_equal(mx.get_frac_inds([0, 1], xi), xi)
    assert np.array_equal(mx.get_frac_inds([[1, 5], [2, 4]], 3, -1), [[0.5], [0.5]])
    assert np.array_equal(mx.get_frac_inds([[1, 5], [2, 7]], 3, -2), [2, -1])




def test_allclose():
    assert mx.allclose(5, 5)
    assert not mx.allclose(5, None)
    assert not mx.allclose(None, 5)
    assert mx.allclose(None, None)

# if __name__=="__main__":
#     test_index()
#     test_iterate_broadcast_op_multi()
#     test_interp1d_lin_reg()
#     test_take_broadcast()
#     test_sph_harm()
#     test_vectorize()
#     test_peak_crossings()
#     test_peak_crossings_1D()
#     test_dot_along()
#     test_mat_mult_along()
#     test_peaks_iter_rmv()
#     test_moment2()
#     test_diagonalize_2d_covariance()
#     test_shapes_broadcastable()
#     test_broadcasted_shape()
#     test_shapes_equal_trailing()
#     test_set_shape_element()
#     test_mean()
#     test_interp1d_to_uniform()
#     test_interpolating_matrix()
#     test_gegenbauer()
#     test_broadcasted_size_along()
#     test_find_first_nonzero()
#     test_find_last_nonzero()
#     test_get_frac_inds()
# def test_iter_subset_dims():
#     x=np.zeros(2)
#     y=np.zeros((3,1))
#     z=np.zeros((4,1,1))
#     for xs,ys,zs,idx in iter_subset_dims([-2],x,y,z,yield_idx=True):
#         print(idx,xs.shape,ys.shape,zs.shape)
# test_iter_subset_dims()
# test_interp1d_lin_reg()
# test_take_broadcast()
# test_iterate_broadcast_op_multi()
# test_sph_harm()
