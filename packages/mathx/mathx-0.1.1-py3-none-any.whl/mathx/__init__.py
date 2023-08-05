from .numpyx import asscalar, reshape_vec, vector_dim, vector_dim_shape, nonzero_vec, expand_dims, squeeze_leading, \
    insert_dim, argmax, ind_closest, broadcasted_shape, are_shapes_broadcastable, are_broadcastable, \
    shapes_equal_trailing, set_shape_element, broadcasted_size_along, all_axes_except, off_diag, flip, gal, geale, \
    abs_sqd, norm_max, norm_sum, last_axis, diff, diff_arb, take_broadcast, take_broadcast_inds, find_first_nonzero, \
    find_last_nonzero, dot_along, mat_mult_along, wrap_to_pm, wrap_to_pmh, zero_mod_2pi, unwrap, divide0, \
    round_to_multiple, round_to_odd_multiple, allclose, multiply_and_sum
from .vectorize import index, index_multi, axis_len_broadcast, slice_dim, slice_dims, take, concatenate, \
    iterate_broadcast_op, iterate_broadcast_op_multi, vectorize, subarrays, eval_iterated, eval_array_fun_chunked
from .geometry import subtract_tangent, line_two_points, peak_crossings, peak_crossings_1D, find_peaks_iter_rmv, \
    polar_grid, polar_perm_cart, polar_reg_grid_to_rect, polar_to_cart, cart_to_polar, fwhm
from .iteralg import converge_aitken_series
from .interpolation import interp_at, interp1d_rect, interp1d_polar, get_frac_inds, interpolating_matrix, Interp1D, \
    interp1d, interp1d_to_uniform, interp1d_n_eps, Interp1DUniform, interp1d_assume_uniform, interp1d_lin_reg, \
    interp1d_frac_ind
from .moments import moment, moment2, mean_and_std, mean_and_variance2, diagonalize_2d_covariance, mean_and_variance
from .fit import gaussian, fit_gaussian, fit_sparse_1d_poly, calc_2d_correction_factors
from .spfun import sph_harm, real_sph_harm, log10_bounded, slowing, gegenbauer
from .sigproc import cosine_apod, cosine_window, xcorr_fft_1d, xcorr_fft_2d, thresholded
from .lattices import Lattice, FiniteSquareLattice, RegularFiniteSquareLattice, RegularFiniteCenteredRectangleLattice, \
    RegularOffsetHexLattice, FiniteSquareLatticeLattice, MarginFiniteSquareLattice  # from . import phase
# TODO Don't want numba as mandatory dependency, so remove.
from .numba import *